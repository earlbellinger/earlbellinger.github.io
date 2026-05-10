"""Promote validated template fits into the atlas color-curve cache.

This script keeps the existing OGLE ingestion/cache build intact and applies a
separate, auditable policy layer using the trial diagnostics:

* Fundamental-mode pulsators share one dictionary family across FU Cepheids,
  anomalous Cepheids, and RRab stars, but RRab stars keep their older
  empirical fits unless the shared dictionary is a clear residual improvement.
* First-overtone pulsators share a second dictionary family across FO Cepheids,
  anomalous Cepheids, and future RRc stars.
* V-band curves use independent cap-3 Fourier fits or the I-carrier convex
  model according to residual diagnostics, not hard class boundaries.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import math
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prepare_data as prep  # noqa: E402


VERSION = 2
BASE_CACHE = prep.COLOR_CURVE_CACHE
BACKUP_CACHE = prep.PROCESSED / f"ogle_color_curves_v{prep.COLOR_CURVE_VERSION}_before_template_promotion.json"
CONVEX_CACHE = prep.PROCESSED / "convex_template_curves_v1.json"
V_CAP3_CACHE = prep.PROCESSED / "v_fourier_cap3_curves_v1.json"
CONVEX_DIAGNOSTICS = prep.ROOT / "diagnostics" / "convex_template_batch_diagnostics.csv"
CEPHEID_V_DIAGNOSTICS = prep.ROOT / "diagnostics" / "v_fourier_order_benchmark_cepheids.csv"
ANOMALOUS_V_DIAGNOSTICS = prep.ROOT / "diagnostics" / "v_fourier_order_benchmark_anomalousCepheids.csv"
RRLYRAE_V_DIAGNOSTICS = prep.ROOT / "diagnostics" / "v_fourier_order_benchmark_rrlyrae.csv"
ALL_V_DIAGNOSTICS = prep.ROOT / "diagnostics" / "v_fourier_order_benchmark_all.csv"
DECISION_CSV = prep.ROOT / "diagnostics" / "promoted_curve_policy_decisions.csv"
SUMMARY_JSON = prep.ROOT / "diagnostics" / "promoted_curve_policy_summary.json"

SAMPLES = prep.COLOR_CURVE_SAMPLES
LIGHT_SCALE = prep.LIGHT_CURVE_INT16_SCALE
COLOR_SCALE = prep.COLOR_CURVE_SCALE
COLOR_ZERO = prep.COLOR_CURVE_ZERO


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def finite_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def round_number(value: float | None, digits: int = 6) -> float | None:
    if value is None or not math.isfinite(value):
        return None
    return round(float(value), digits)


def decode_i_offsets(curve: dict[str, Any] | None) -> np.ndarray | None:
    if not curve or not isinstance(curve.get("iCurve"), str):
        return None
    raw = base64.b64decode(str(curve["iCurve"]))
    return np.frombuffer(raw, dtype="<i2").astype(np.float64) / LIGHT_SCALE


def decode_color_offsets(curve: dict[str, Any] | None) -> np.ndarray | None:
    if not curve or not isinstance(curve.get("curve"), str):
        return None
    raw = base64.b64decode(str(curve["curve"]))
    return (np.frombuffer(raw, dtype=np.uint8).astype(np.float64) - COLOR_ZERO) / COLOR_SCALE


def decode_v_cap_offsets(curve: dict[str, Any] | None) -> np.ndarray | None:
    if not curve or not isinstance(curve.get("vCurve"), str):
        return None
    raw = base64.b64decode(str(curve["vCurve"]))
    return np.frombuffer(raw, dtype="<i2").astype(np.float64) / LIGHT_SCALE


def encode_i_offsets(offsets: np.ndarray) -> str:
    lower = np.iinfo(np.int16).min / LIGHT_SCALE
    upper = np.iinfo(np.int16).max / LIGHT_SCALE
    quantized = np.rint(np.clip(offsets, lower, upper) * LIGHT_SCALE).astype("<i2")
    return base64.b64encode(quantized.tobytes()).decode("ascii")


def encode_color_offsets(offsets: np.ndarray) -> str:
    quantized = np.rint(np.clip(offsets, -0.63, 0.63) * COLOR_SCALE + COLOR_ZERO).astype(np.uint8)
    return base64.b64encode(bytes(quantized)).decode("ascii")


def centered(values: np.ndarray) -> np.ndarray:
    return values - float(np.mean(values))


def curve_roughness(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    if values.size < 5:
        return math.inf
    amplitude = float(np.ptp(values))
    if not math.isfinite(amplitude) or amplitude <= 1e-6:
        return math.inf
    wrapped = np.concatenate([[values[-1]], values, [values[0]]])
    second_difference = np.diff(wrapped, n=2)
    return float(np.sqrt(np.mean(second_difference**2)) / amplitude)


def reject_visibly_rougher_curve(
    current_offsets: np.ndarray,
    candidate_offsets: np.ndarray | None,
    current_rms: float | None,
    candidate_rms: float | None,
) -> bool:
    if candidate_offsets is None:
        return False
    current_roughness = curve_roughness(current_offsets)
    candidate_roughness = curve_roughness(candidate_offsets)
    if not math.isfinite(current_roughness) or not math.isfinite(candidate_roughness):
        return False
    roughness_limit = max(current_roughness * 1.6, current_roughness + 0.003)
    if candidate_roughness <= roughness_limit:
        return False
    return not ratio_ok(candidate_rms, current_rms, 0.90)


def metric(row: dict[str, Any] | None, key: str) -> float | None:
    if row is None:
        return None
    return finite_float(row.get(key))


def ratio_ok(new: float | None, old: float | None, factor: float) -> bool:
    if new is None:
        return False
    if old is None or old <= 0:
        return True
    return new <= old * factor


def read_csv_by_id(paths: list[Path]) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                obj_id = row.get("id")
                if obj_id:
                    rows[obj_id] = row
    return rows


def load_catalog() -> dict[str, prep.CatalogStar]:
    stars = (
        prep.parse_cepheids(prep.RAW / "ogle_cepheids_table3.dat")
        + prep.parse_rr_lyrae(prep.RAW / "ogle_rrlyrae_table2.dat")
        + prep.parse_anomalous_cepheids()
    )
    light_curve_parameters = prep.load_light_curve_parameters()
    for star in stars:
        star.light_curve = light_curve_parameters.get(star.obj_id)
    return {star.obj_id: star for star in stars}


def load_convex_curves() -> dict[str, dict[str, Any]]:
    curves: dict[str, dict[str, Any]] = {}
    if CONVEX_CACHE.exists():
        curves.update(load_json(CONVEX_CACHE).get("curves", {}))
    return curves


def current_i_metrics(base: dict[str, Any], convex_row: dict[str, Any] | None) -> tuple[float | None, float | None]:
    return (
        metric(convex_row, "currentIRms") or finite_float(base.get("iRms")),
        metric(convex_row, "currentIMad"),
    )


def current_v_metrics(
    base: dict[str, Any],
    convex_row: dict[str, Any] | None,
    v_row: dict[str, Any] | None,
) -> tuple[float | None, float | None]:
    return (
        metric(v_row, "currentVRms") or metric(convex_row, "currentVRms") or finite_float(base.get("vRms")),
        metric(v_row, "currentVMad") or metric(convex_row, "currentVMad"),
    )


def choose_i_source(
    dataset: str,
    family: str,
    base: dict[str, Any],
    convex_curve: dict[str, Any] | None,
    convex_row: dict[str, Any] | None,
) -> tuple[str, str]:
    if convex_curve is None or not isinstance(convex_curve.get("iCurve"), str):
        return "current", "missing-dictionary"

    current_rms, current_mad = current_i_metrics(base, convex_row)
    dict_rms = metric(convex_row, "dictIRms") or finite_float(convex_curve.get("iRms"))
    dict_mad = metric(convex_row, "dictIMad")

    if dataset == "rrlyrae" and family == prep.TEMPLATE_FAMILY_FUNDAMENTAL:
        if ratio_ok(dict_rms, current_rms, 0.90) and ratio_ok(dict_mad, current_mad, 1.00):
            return "convex-dictionary-v1", "rrab-clear-i-improvement"
        return "current", "rrab-current-preferred"

    if family == prep.TEMPLATE_FAMILY_FUNDAMENTAL:
        if ratio_ok(dict_rms, current_rms, 1.15) and ratio_ok(dict_mad, current_mad, 1.60):
            return "convex-dictionary-v1", "fundamental-default"
        return "current", "fundamental-guard"

    if family == prep.TEMPLATE_FAMILY_FIRST_OVERTONE:
        if ratio_ok(dict_rms, current_rms, 0.98) and ratio_ok(dict_mad, current_mad, 1.15):
            return "convex-dictionary-v1", "first-overtone-clear-i-improvement"
        return "current", "first-overtone-current-preferred"

    return "current", "unhandled-family"


def choose_v_source(
    dataset: str,
    family: str,
    base: dict[str, Any],
    convex_curve: dict[str, Any] | None,
    v_cap_curve: dict[str, Any] | None,
    convex_row: dict[str, Any] | None,
    v_row: dict[str, Any] | None,
) -> tuple[str, str]:
    has_current = isinstance(base.get("curve"), str)
    cap_n = int(finite_float(v_cap_curve.get("vN") if v_cap_curve else None) or 0)
    convex_n = int(finite_float(convex_curve.get("vN") if convex_curve else None) or 0)
    has_cap = v_cap_curve is not None and isinstance(v_cap_curve.get("vCurve"), str) and cap_n >= 8
    has_convex = convex_curve is not None and isinstance(convex_curve.get("curve"), str) and convex_n >= 8

    current_rms, current_mad = current_v_metrics(base, convex_row, v_row)
    cap_rms = metric(v_row, "cap3Rms") or finite_float(v_cap_curve.get("vRms") if v_cap_curve else None)
    cap_mad = metric(v_row, "cap3Mad") or finite_float(v_cap_curve.get("vMad") if v_cap_curve else None)
    dict_rms = metric(convex_row, "dictVRms") or finite_float(convex_curve.get("vRms") if convex_curve else None)
    dict_mad = metric(convex_row, "dictVMad")

    if family == prep.TEMPLATE_FAMILY_FIRST_OVERTONE:
        if has_cap and (not has_current or (ratio_ok(cap_rms, current_rms, 0.98) and ratio_ok(cap_mad, current_mad, 1.15))):
            return "v-fourier-cap3-v1", "first-overtone-cap3-preferred"
        if has_convex and has_current and ratio_ok(dict_rms, current_rms, 0.90) and ratio_ok(dict_mad, current_mad, 1.35):
            return "convex-i-carrier-v1", "first-overtone-convex-v-fallback"
        return ("current", "first-overtone-current-v-preferred") if has_current else ("none", "missing-v-source")

    if dataset == "rrlyrae" and family == prep.TEMPLATE_FAMILY_FUNDAMENTAL:
        cap_ok = has_cap and (
            not has_current
            or (ratio_ok(cap_rms, current_rms, 0.98) and ratio_ok(cap_mad, current_mad, 1.10))
        )
        if cap_ok:
            return "v-fourier-cap3-v1", "rrab-cap3-preferred"
        return ("current", "rrab-current-v-preferred") if has_current else ("none", "missing-v-source")

    if family == prep.TEMPLATE_FAMILY_FUNDAMENTAL:
        convex_ok = has_convex and (
            (not has_current and ratio_ok(dict_rms, cap_rms, 1.10) and ratio_ok(dict_mad, cap_mad, 2.50))
            or (has_current and ratio_ok(dict_rms, current_rms, 0.85) and ratio_ok(dict_mad, current_mad, 2.50))
        )
        cap_ok = has_cap and (not has_current or (ratio_ok(cap_rms, current_rms, 0.98) and ratio_ok(cap_mad, current_mad, 1.15)))
        if convex_ok and cap_ok:
            convex_score = (dict_rms or math.inf) + 0.12 * (dict_mad or 0.0)
            cap_score = (cap_rms or math.inf) + 0.12 * (cap_mad or 0.0)
            return ("convex-i-carrier-v1", "fundamental-v-best-score") if convex_score <= cap_score else ("v-fourier-cap3-v1", "fundamental-v-best-score")
        if convex_ok:
            return "convex-i-carrier-v1", "fundamental-large-v-rms-gain"
        if cap_ok:
            return "v-fourier-cap3-v1", "fundamental-cap3-guarded"
        return ("current", "fundamental-current-v-preferred") if has_current else ("none", "missing-v-source")

    return ("current", "unhandled-family") if has_current else ("none", "missing-v-source")


def apply_i_source(
    promoted: dict[str, Any],
    source: str,
    base_i_offsets: np.ndarray,
    convex_curve: dict[str, Any] | None,
    convex_row: dict[str, Any] | None,
) -> np.ndarray:
    if source != "convex-dictionary-v1" or convex_curve is None:
        promoted.setdefault("templateSource", "current")
        return base_i_offsets

    convex_i_offsets = decode_i_offsets(convex_curve)
    if convex_i_offsets is None:
        promoted.setdefault("templateSource", "current")
        return base_i_offsets

    promoted["iCurve"] = encode_i_offsets(convex_i_offsets)
    promoted["templateSource"] = "convex-dictionary-v1"
    promoted["iRms"] = round_number(metric(convex_row, "dictIRms") or finite_float(convex_curve.get("iRms")), 4)
    promoted["rawRms"] = round_number(metric(convex_row, "dictIKeptRms") or finite_float(convex_curve.get("rawRms")), 4)
    promoted["iSpan"] = round_number(float(prep.percentile_span(convex_i_offsets)), 4)
    promoted["iPeakSpan"] = round_number(float(prep.peak_to_peak(convex_i_offsets)), 4)
    promoted["iExtrema"] = int(prep.significant_extrema_count(convex_i_offsets))
    for key in (
        "dictionaryActive",
        "dictionaryEffective",
        "dictionaryPhaseOffset",
        "dictionaryRawKept",
        "dictionaryRawRejected",
    ):
        if key in convex_curve:
            promoted[key] = convex_curve[key]
    flags = set(promoted.get("variabilityFlags") or [])
    flags.update(convex_curve.get("variabilityFlags") or [])
    promoted["variabilityFlags"] = sorted(flags)
    return convex_i_offsets


def source_v_shape(
    source: str,
    base_i_offsets: np.ndarray,
    base: dict[str, Any],
    convex_curve: dict[str, Any] | None,
    v_cap_curve: dict[str, Any] | None,
) -> np.ndarray | None:
    if source == "current":
        color = decode_color_offsets(base)
        return None if color is None else base_i_offsets + color
    if source == "convex-i-carrier-v1":
        convex_i = decode_i_offsets(convex_curve)
        convex_color = decode_color_offsets(convex_curve)
        if convex_i is None or convex_color is None:
            return None
        return convex_i + convex_color
    if source == "v-fourier-cap3-v1":
        return decode_v_cap_offsets(v_cap_curve)
    return None


def apply_v_source(
    promoted: dict[str, Any],
    source: str,
    selected_i_offsets: np.ndarray,
    base_i_offsets: np.ndarray,
    base: dict[str, Any],
    convex_curve: dict[str, Any] | None,
    v_cap_curve: dict[str, Any] | None,
    convex_row: dict[str, Any] | None,
    v_row: dict[str, Any] | None,
) -> bool:
    shape = source_v_shape(source, base_i_offsets, base, convex_curve, v_cap_curve)
    if shape is None:
        promoted.pop("curve", None)
        promoted.pop("quality", None)
        promoted.pop("vAmplitude", None)
        return False

    color_offsets = centered(shape - selected_i_offsets)
    promoted["curve"] = encode_color_offsets(color_offsets)
    promoted["span"] = round_number(float(prep.percentile_span(color_offsets)), 4)
    promoted["peakSpan"] = round_number(float(prep.peak_to_peak(color_offsets)), 4)
    promoted["vAmplitude"] = round_number(float(prep.peak_to_peak(shape)), 4)
    promoted["vTemplateSource"] = source

    if source == "current":
        promoted.setdefault("vTemplateSource", "current-harmonic")
        return True

    if source == "convex-i-carrier-v1":
        promoted["vRms"] = round_number(metric(convex_row, "dictVRms") or finite_float(convex_curve.get("vRms") if convex_curve else None), 4)
        promoted["vMad"] = round_number(metric(convex_row, "dictVMad"), 4)
        promoted["vN"] = int(finite_float(convex_curve.get("vN") if convex_curve else None) or promoted.get("vN") or 0)
        promoted["sharedPhaseOffset"] = round_number(metric(convex_row, "dictPhaseOffset"), 6)
        promoted["quality"] = int(promoted.get("quality") or (convex_curve or {}).get("quality") or 2)
        return True

    if source == "v-fourier-cap3-v1":
        promoted["vRms"] = round_number(metric(v_row, "cap3Rms") or finite_float(v_cap_curve.get("vRms") if v_cap_curve else None), 4)
        promoted["vMad"] = round_number(metric(v_row, "cap3Mad") or finite_float(v_cap_curve.get("vMad") if v_cap_curve else None), 4)
        promoted["vN"] = int(finite_float(v_cap_curve.get("vN") if v_cap_curve else None) or promoted.get("vN") or 0)
        promoted["vH"] = int(finite_float(v_cap_curve.get("vH") if v_cap_curve else None) or 3)
        promoted["vFitSamples"] = int(finite_float(v_cap_curve.get("vFitSamples") if v_cap_curve else None) or 0)
        promoted["sharedPhaseOffset"] = 0.0
        promoted["quality"] = int(promoted.get("quality") or 2)
        return True

    return True


def selected_metric(
    source: str,
    current_value: float | None,
    dict_value: float | None,
    cap_value: float | None,
) -> float | None:
    if source == "convex-dictionary-v1" or source == "convex-i-carrier-v1":
        return dict_value
    if source == "v-fourier-cap3-v1":
        return cap_value
    if source == "current":
        return current_value
    return None


def summarize_decisions(rows: list[dict[str, Any]]) -> dict[str, Any]:
    def summarize_subset(subset: list[dict[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {"count": len(subset)}
        for source_key in ("iSource", "vSource"):
            result[source_key] = dict(Counter(str(row[source_key]) for row in subset))
        for metric_name in ("iRmsRatio", "vRmsRatio", "iMadRatio", "vMadRatio"):
            values = np.asarray([float(row[metric_name]) for row in subset if row.get(metric_name) not in (None, "")], dtype=float)
            values = values[np.isfinite(values)]
            if values.size:
                result[metric_name] = {
                    "count": int(values.size),
                    "median": round(float(np.median(values)), 5),
                    "p10": round(float(np.percentile(values, 10)), 5),
                    "p90": round(float(np.percentile(values, 90)), 5),
                    "improvedFraction": round(float(np.mean(values < 1.0)), 4),
                }
        return result

    summary: dict[str, Any] = {
        "version": VERSION,
        "policy": {
            "rrab_I": "keep current fit unless shared dictionary improves RMS by >=10% without increasing MAD",
            "rrab_V": "use current or guarded cap-3 V; do not promote merged convex carrier for RRab",
            "fundamental_I": "convex dictionary unless RMS is >15% worse or MAD is >60% worse",
            "first_overtone_I": "convex dictionary only for clear RMS improvement with MAD guard",
            "fundamental_V": "choose guarded convex I-carrier or cap-3 Fourier by robust residual score",
            "first_overtone_V": "guarded independent V cap-3 Fourier, with rare convex fallback",
        },
        "overall": summarize_subset(rows),
        "byDatasetFamily": {},
    }
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[f"{row['dataset']}/{row['family']}"].append(row)
    summary["byDatasetFamily"] = {key: summarize_subset(value) for key, value in sorted(grouped.items())}
    return summary


def promote(dry_run: bool = False) -> dict[str, Any]:
    source_cache = BACKUP_CACHE if BACKUP_CACHE.exists() else BASE_CACHE
    payload = load_json(source_cache)
    base_curves: dict[str, dict[str, Any]] = payload.get("curves", {})
    promoted_curves: dict[str, dict[str, Any]] = {}
    catalog = load_catalog()
    convex_curves = load_convex_curves()
    v_cap_curves = load_json(V_CAP3_CACHE).get("curves", {})
    convex_rows = read_csv_by_id([CONVEX_DIAGNOSTICS])
    v_rows = read_csv_by_id([CEPHEID_V_DIAGNOSTICS, ANOMALOUS_V_DIAGNOSTICS, RRLYRAE_V_DIAGNOSTICS, ALL_V_DIAGNOSTICS])
    decision_rows: list[dict[str, Any]] = []

    for obj_id, base in base_curves.items():
        star = catalog.get(obj_id)
        if star is None:
            promoted_curves[obj_id] = dict(base)
            continue
        base_i_offsets = decode_i_offsets(base)
        if base_i_offsets is None:
            promoted_curves[obj_id] = dict(base)
            continue

        dataset = star.dataset
        family = prep.template_family(star)
        convex_curve = convex_curves.get(obj_id)
        v_cap_curve = v_cap_curves.get(obj_id)
        convex_row = convex_rows.get(obj_id)
        v_row = v_rows.get(obj_id)

        promoted = dict(base)
        i_source, i_reason = choose_i_source(dataset, family, base, convex_curve, convex_row)
        current_i_rms, current_i_mad = current_i_metrics(base, convex_row)
        dict_i_rms = metric(convex_row, "dictIRms") or finite_float(convex_curve.get("iRms") if convex_curve else None)
        convex_i_offsets = decode_i_offsets(convex_curve) if i_source == "convex-dictionary-v1" else None
        if reject_visibly_rougher_curve(base_i_offsets, convex_i_offsets, current_i_rms, dict_i_rms):
            i_source = "current"
            i_reason = f"{i_reason}:roughness-guard"
        selected_i_offsets = apply_i_source(promoted, i_source, base_i_offsets, convex_curve, convex_row)
        v_source, v_reason = choose_v_source(dataset, family, base, convex_curve, v_cap_curve, convex_row, v_row)
        has_color = apply_v_source(
            promoted,
            v_source,
            selected_i_offsets,
            base_i_offsets,
            base,
            convex_curve,
            v_cap_curve,
            convex_row,
            v_row,
        )
        promoted["templatePromotionVersion"] = VERSION
        promoted["templatePromotionReason"] = f"{i_reason};{v_reason}"
        promoted_curves[obj_id] = promoted

        current_v_rms, current_v_mad = current_v_metrics(base, convex_row, v_row)
        dict_i_mad = metric(convex_row, "dictIMad")
        dict_v_rms = metric(convex_row, "dictVRms") or finite_float(convex_curve.get("vRms") if convex_curve else None)
        dict_v_mad = metric(convex_row, "dictVMad")
        cap_v_rms = metric(v_row, "cap3Rms") or finite_float(v_cap_curve.get("vRms") if v_cap_curve else None)
        cap_v_mad = metric(v_row, "cap3Mad") or finite_float(v_cap_curve.get("vMad") if v_cap_curve else None)
        selected_i_rms = selected_metric(i_source, current_i_rms, dict_i_rms, None)
        selected_i_mad = selected_metric(i_source, current_i_mad, dict_i_mad, None)
        selected_v_rms = selected_metric(v_source, current_v_rms, dict_v_rms, cap_v_rms)
        selected_v_mad = selected_metric(v_source, current_v_mad, dict_v_mad, cap_v_mad)

        decision_rows.append(
            {
                "id": obj_id,
                "dataset": dataset,
                "location": star.location,
                "family": family,
                "period": round_number(float(star.light_curve["period"] if star.light_curve else star.period), 7),
                "iSource": i_source,
                "iReason": i_reason,
                "vSource": v_source if has_color else "none",
                "vReason": v_reason,
                "currentIRms": round_number(current_i_rms),
                "selectedIRms": round_number(selected_i_rms),
                "iRmsRatio": round_number((selected_i_rms / current_i_rms) if selected_i_rms is not None and current_i_rms else None),
                "currentIMad": round_number(current_i_mad),
                "selectedIMad": round_number(selected_i_mad),
                "iMadRatio": round_number((selected_i_mad / current_i_mad) if selected_i_mad is not None and current_i_mad else None),
                "currentVRms": round_number(current_v_rms),
                "selectedVRms": round_number(selected_v_rms),
                "vRmsRatio": round_number((selected_v_rms / current_v_rms) if selected_v_rms is not None and current_v_rms else None),
                "currentVMad": round_number(current_v_mad),
                "selectedVMad": round_number(selected_v_mad),
                "vMadRatio": round_number((selected_v_mad / current_v_mad) if selected_v_mad is not None and current_v_mad else None),
            }
        )

    summary = summarize_decisions(decision_rows)
    summary["baselineCache"] = str(source_cache.relative_to(prep.ROOT))
    payload["curves"] = promoted_curves
    payload.setdefault("summary", {})
    payload["summary"]["templatePromotion"] = summary

    if not dry_run:
        if BASE_CACHE.exists() and not BACKUP_CACHE.exists():
            shutil.copy2(BASE_CACHE, BACKUP_CACHE)
        BASE_CACHE.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
        SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        with DECISION_CSV.open("w", encoding="utf-8", newline="") as handle:
            fieldnames = list(decision_rows[0].keys()) if decision_rows else []
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(decision_rows)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    summary = promote(dry_run=args.dry_run)
    print(json.dumps(summary, indent=2))
    if args.dry_run:
        print("Dry run only; cache was not modified.")
    else:
        print(f"Wrote {BASE_CACHE}")
        print(f"Wrote {SUMMARY_JSON}")
        print(f"Wrote {DECISION_CSV}")


if __name__ == "__main__":
    main()
