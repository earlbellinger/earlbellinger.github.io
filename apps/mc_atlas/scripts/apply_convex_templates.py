"""Apply local nonnegative template dictionaries to pulsators at scale.

This batch pass uses the high-quality Fourier feature cache as a dictionary of
real pulsator lightcurve shapes. Each target is fitted as a nonnegative mixture
of nearby same-mode templates in log-period, with a global phase shift and
coherence-preserving residual clipping. V band is fitted as a mean and
amplitude response to the I-derived carrier.

Outputs:
  data/processed/convex_template_curves_v1.json
  diagnostics/convex_template_batch_diagnostics.csv
  diagnostics/convex_template_batch_summary.json
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import math
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import nnls

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prepare_data as prep  # noqa: E402


VERSION = 1
SAMPLES = prep.COLOR_CURVE_SAMPLES
FEATURE_CACHE = prep.PCA_FEATURE_CACHE
BASELINE_CURVE_CACHE = prep.PROCESSED / f"ogle_color_curves_v{prep.COLOR_CURVE_VERSION}_before_template_promotion.json"
CURRENT_CURVE_CACHE = BASELINE_CURVE_CACHE if BASELINE_CURVE_CACHE.exists() else prep.COLOR_CURVE_CACHE
OUT_CACHE = prep.PROCESSED / "convex_template_curves_v1.json"
OUT_CSV = prep.ROOT / "diagnostics" / "convex_template_batch_diagnostics.csv"
OUT_SUMMARY = prep.ROOT / "diagnostics" / "convex_template_batch_summary.json"

DICTIONARY_NEIGHBORS = 96
RIDGE_STRENGTH = 0.45
PERIOD_RIDGE_STRENGTH = 0.65
SHIFT_MIN = -0.12
SHIFT_MAX = 0.12
SHIFT_COARSE_COUNT = 25
SHIFT_REFINE_WIDTH = 0.012
SHIFT_REFINE_COUNT = 9
EFFECTIVE_ERROR_FLOOR = 0.018
EFFECTIVE_ERROR_CEILING = 0.08
V_ERROR_FLOOR = 0.018
V_ERROR_CEILING = 0.12


FEATURES_BY_FAMILY: dict[str, dict[str, np.ndarray]] = {}


def init_worker(features_by_family: dict[str, dict[str, np.ndarray]]) -> None:
    global FEATURES_BY_FAMILY
    FEATURES_BY_FAMILY = features_by_family


def round_number(value: float, digits: int = 6) -> float | None:
    if not math.isfinite(value):
        return None
    return round(float(value), digits)


def robust_stats(residual: np.ndarray, mask: np.ndarray | None = None) -> tuple[float, float, float]:
    values = np.asarray(residual if mask is None else residual[mask], dtype=float)
    values = values[np.isfinite(values)]
    if values.size == 0:
        return math.nan, math.nan, math.nan
    center = float(np.median(values))
    mad = float(1.4826 * np.median(np.abs(values - center)))
    rms = float(np.sqrt(np.mean(values * values)))
    return center, mad, rms


def percentile_span(values: np.ndarray, low: float = 5.0, high: float = 95.0) -> float:
    if values.size == 0:
        return math.nan
    p_low, p_high = np.percentile(values, [low, high])
    return float(p_high - p_low)


def periodic_interp_1d(values: np.ndarray, phase: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    n = values.size
    scaled = np.mod(phase, 1.0) * n
    left = np.floor(scaled).astype(np.int64)
    frac = scaled - left
    right = (left + 1) % n
    return values[left] * (1.0 - frac) + values[right] * frac


def interpolate_shapes(shapes: np.ndarray, phase: np.ndarray, shift: float) -> np.ndarray:
    n = shapes.shape[1]
    scaled = np.mod(phase + shift, 1.0) * n
    left = np.floor(scaled).astype(np.int64)
    frac = scaled - left
    right = (left + 1) % n
    return (shapes[:, left].T * (1.0 - frac[:, None])) + (shapes[:, right].T * frac[:, None])


def weighted_mean(values: np.ndarray, weights: np.ndarray, axis: int = 0) -> np.ndarray:
    return np.sum(values * weights, axis=axis) / np.sum(weights, axis=axis)


def coherence_preserving_rejection_mask(
    phase: np.ndarray,
    residual: np.ndarray,
    err: np.ndarray,
    current_mask: np.ndarray,
    *,
    sigma_multiplier: float = 4.0,
    local_window: float = 0.055,
    coherent_sigma: float = 1.6,
) -> np.ndarray:
    center, mad, _ = robust_stats(residual, current_mask)
    if not math.isfinite(mad):
        return current_mask
    sigma = max(0.012, mad, float(np.median(np.clip(err[current_mask], 0.008, 0.08))))
    scaled = (residual - center) / sigma
    candidate = np.abs(scaled) > sigma_multiplier
    next_mask = current_mask.copy()
    wrapped_phase = np.mod(phase, 1.0)

    for index in np.flatnonzero(candidate):
        distance = np.abs(wrapped_phase - wrapped_phase[index])
        distance = np.minimum(distance, 1.0 - distance)
        local = distance <= local_window
        if int(local.sum()) < 4:
            next_mask[index] = False
            continue
        same_sign = np.sign(scaled) == np.sign(scaled[index])
        coherent = local & same_sign & (np.abs(scaled) >= coherent_sigma)
        strong = local & same_sign & (np.abs(scaled) >= 0.75 * sigma_multiplier)
        next_mask[index] = bool(int(coherent.sum()) >= 5 and int(strong.sum()) >= 2)
    return next_mask


def encode_light_curve(offsets: np.ndarray) -> str:
    lower = np.iinfo(np.int16).min / prep.LIGHT_CURVE_INT16_SCALE
    upper = np.iinfo(np.int16).max / prep.LIGHT_CURVE_INT16_SCALE
    quantized = np.rint(np.clip(offsets, lower, upper) * prep.LIGHT_CURVE_INT16_SCALE).astype("<i2")
    return base64.b64encode(quantized.tobytes()).decode("ascii")


def encode_color_curve(offsets: np.ndarray) -> str:
    quantized = np.rint(np.clip(offsets, -0.63, 0.63) * prep.COLOR_CURVE_SCALE + prep.COLOR_CURVE_ZERO).astype(np.uint8)
    return base64.b64encode(bytes(quantized)).decode("ascii")


def decode_current_i(current: dict[str, Any] | None, i_mag: float, phase: np.ndarray) -> np.ndarray | None:
    if not current or not isinstance(current.get("iCurve"), str):
        return None
    offsets = np.frombuffer(base64.b64decode(str(current["iCurve"])), dtype="<i2").astype(float) / prep.LIGHT_CURVE_INT16_SCALE
    return i_mag + periodic_interp_1d(offsets, phase)


def decode_current_color(current: dict[str, Any] | None, v_minus_i: float, phase: np.ndarray) -> np.ndarray | None:
    if not current or not isinstance(current.get("curve"), str):
        return None
    offsets = (np.frombuffer(base64.b64decode(str(current["curve"])), dtype=np.uint8).astype(float) - prep.COLOR_CURVE_ZERO) / prep.COLOR_CURVE_SCALE
    return v_minus_i + periodic_interp_1d(offsets, phase)


def current_model_i(current: dict[str, Any] | None, i_mag: float, phase: np.ndarray) -> np.ndarray | None:
    return decode_current_i(current, i_mag, phase)


def current_model_v(current: dict[str, Any] | None, i_mag: float, v_minus_i: float, phase: np.ndarray) -> np.ndarray | None:
    i_model = decode_current_i(current, i_mag, phase)
    if i_model is None:
        return None
    color = decode_current_color(current, v_minus_i, phase)
    if color is None:
        color = np.full_like(phase, v_minus_i, dtype=float)
    return i_model + color


def select_dictionary(family: str, obj_id: str, logp: float) -> dict[str, np.ndarray] | None:
    feature_group = FEATURES_BY_FAMILY.get(family)
    if feature_group is None:
        return None
    ids = feature_group["ids"]
    logps = feature_group["logp"]
    shapes = feature_group["shapes"]
    distances = np.abs(logps - logp)
    order = np.argsort(distances)
    selected: list[int] = []
    for index in order:
        if str(ids[index]) == obj_id:
            continue
        selected.append(int(index))
        if len(selected) >= DICTIONARY_NEIGHBORS:
            break
    if len(selected) < 8:
        return None
    selected_idx = np.asarray(selected, dtype=np.int64)
    selected_distances = distances[selected_idx]
    sigma = max(0.035, float(np.percentile(selected_distances, 70)))
    return {
        "ids": ids[selected_idx],
        "logp": logps[selected_idx],
        "shapes": shapes[selected_idx],
        "distances": selected_distances,
        "sigma": np.asarray([sigma], dtype=float),
    }


def solve_nonnegative_mix(
    template_values: np.ndarray,
    mag: np.ndarray,
    err: np.ndarray,
    distances: np.ndarray,
    sigma: float,
) -> tuple[float, np.ndarray, np.ndarray]:
    weights = 1.0 / np.clip(err, EFFECTIVE_ERROR_FLOOR, EFFECTIVE_ERROR_CEILING) ** 2
    mean_y = float(np.average(mag, weights=weights))
    mean_x = np.average(template_values, axis=0, weights=weights)
    sqrt_w = np.sqrt(weights)
    matrix = (template_values - mean_x) * sqrt_w[:, None]
    rhs = (mag - mean_y) * sqrt_w

    period_units = distances / max(sigma, 1e-5)
    penalties = RIDGE_STRENGTH * (1.0 + PERIOD_RIDGE_STRENGTH * period_units**2)
    matrix = np.vstack([matrix, np.diag(penalties)])
    rhs = np.concatenate([rhs, np.zeros(template_values.shape[1], dtype=float)])

    try:
        alpha, _ = nnls(matrix, rhs, maxiter=max(300, template_values.shape[1] * 8))
    except RuntimeError:
        alpha, _ = nnls(matrix, rhs, maxiter=max(900, template_values.shape[1] * 20))
    model_without_mean = template_values @ alpha
    mean = float(np.average(mag - model_without_mean, weights=weights))
    return mean, alpha, mean + model_without_mean


def score_residual(residual: np.ndarray) -> float:
    _, mad, rms = robust_stats(residual)
    if not math.isfinite(rms):
        return math.inf
    return float(rms + 0.12 * (mad if math.isfinite(mad) else 0.0))


def fit_i_dictionary(star: dict[str, Any], phot_i: np.ndarray, dictionary: dict[str, np.ndarray]) -> dict[str, Any] | None:
    phase = np.mod((phot_i[:, 0] - float(star["t0"])) / float(star["period"]), 1.0)
    mag = phot_i[:, 1]
    err = phot_i[:, 2]
    shapes = dictionary["shapes"]
    distances = dictionary["distances"]
    sigma = float(dictionary["sigma"][0])
    mask = np.ones(phase.size, dtype=bool)
    best_shift = 0.0
    best_mean = float(np.median(mag))
    best_alpha = np.zeros(shapes.shape[0], dtype=float)
    best_model = np.full(phase.size, best_mean, dtype=float)

    if phase.size < 25:
        return None

    for iteration in range(5):
        shifts = np.linspace(SHIFT_MIN, SHIFT_MAX, SHIFT_COARSE_COUNT)
        if iteration > 0:
            shifts = np.unique(
                np.concatenate(
                    [
                        shifts,
                        best_shift + np.linspace(-SHIFT_REFINE_WIDTH, SHIFT_REFINE_WIDTH, SHIFT_REFINE_COUNT),
                    ]
                )
            )
        best_score = math.inf
        for shift in shifts:
            if shift < SHIFT_MIN or shift > SHIFT_MAX:
                continue
            values = interpolate_shapes(shapes, phase[mask], float(shift))
            mean, alpha, model = solve_nonnegative_mix(values, mag[mask], err[mask], distances, sigma)
            residual = mag[mask] - model
            total_alpha = float(np.sum(alpha))
            weights = alpha / total_alpha if total_alpha > 0 else np.zeros_like(alpha)
            entropy = float(-np.sum(weights[weights > 0] * np.log(weights[weights > 0]))) if total_alpha > 0 else 0.0
            active = int(np.sum(alpha > max(1e-4, 0.01 * float(np.max(alpha)) if alpha.size and np.max(alpha) > 0 else 1e-4)))
            score = score_residual(residual) + 0.0005 * active + 0.0008 * entropy
            if score < best_score:
                best_score = score
                best_shift = float(shift)
                best_mean = mean
                best_alpha = alpha

        values_all = interpolate_shapes(shapes, phase, best_shift)
        best_model = best_mean + values_all @ best_alpha
        residual_all = mag - best_model
        next_mask = coherence_preserving_rejection_mask(phase, residual_all, err, mask)
        if int(next_mask.sum()) < max(20, int(0.55 * phase.size)):
            next_mask = mask
        if np.array_equal(next_mask, mask):
            break
        mask = next_mask

    values_masked = interpolate_shapes(shapes, phase[mask], best_shift)
    best_mean, best_alpha, _ = solve_nonnegative_mix(values_masked, mag[mask], err[mask], distances, sigma)
    values_all = interpolate_shapes(shapes, phase, best_shift)
    best_model = best_mean + values_all @ best_alpha
    residual = mag - best_model
    _, kept_mad, kept_rms = robust_stats(residual, mask)
    _, all_mad, all_rms = robust_stats(residual)

    dense = np.linspace(0.0, 1.0, SAMPLES, endpoint=False)
    dense_values = interpolate_shapes(shapes, dense, best_shift)
    dense_model = best_mean + dense_values @ best_alpha
    total_alpha = float(np.sum(best_alpha))
    template_weights = best_alpha / total_alpha if total_alpha > 0 else np.zeros_like(best_alpha)
    active_threshold = max(1e-4, 0.01 * float(np.max(best_alpha)) if best_alpha.size and np.max(best_alpha) > 0 else 1e-4)
    active = int(np.sum(best_alpha > active_threshold))
    effective = float(1.0 / np.sum(template_weights**2)) if np.sum(template_weights**2) > 0 else 0.0

    return {
        "phase": phase,
        "mean": best_mean,
        "alpha": best_alpha,
        "weights": template_weights,
        "model": best_model,
        "denseModel": dense_model,
        "residual": residual,
        "mask": mask,
        "keptMad": kept_mad,
        "keptRms": kept_rms,
        "allMad": all_mad,
        "allRms": all_rms,
        "phaseShift": best_shift,
        "activeTemplates": active,
        "effectiveTemplates": effective,
        "amplitude": total_alpha,
    }


def fit_v_on_i_carrier(
    star: dict[str, Any],
    phot_v: np.ndarray,
    dictionary: dict[str, np.ndarray],
    i_fit: dict[str, Any],
) -> dict[str, Any] | None:
    if phot_v.shape[0] < 8:
        return None
    phase = np.mod((phot_v[:, 0] - float(star["t0"])) / float(star["period"]), 1.0)
    shapes = dictionary["shapes"]
    carrier = interpolate_shapes(shapes, phase, float(i_fit["phaseShift"])) @ np.asarray(i_fit["weights"], dtype=float)
    center = float(np.mean(carrier))
    span = percentile_span(carrier)
    if not math.isfinite(span) or span < 1e-4:
        return None
    x = (carrier - center) / span
    y = phot_v[:, 1]
    err = phot_v[:, 2]
    mask = np.ones(y.size, dtype=bool)
    coeffs = np.asarray([float(np.median(y)), percentile_span(y)], dtype=float)
    for _ in range(5):
        weights = 1.0 / np.clip(err[mask], V_ERROR_FLOOR, V_ERROR_CEILING) ** 2
        matrix = np.column_stack([np.ones(int(mask.sum())), x[mask]])
        weighted_matrix = matrix * np.sqrt(weights)[:, None]
        weighted_y = y[mask] * np.sqrt(weights)
        coeffs, *_ = np.linalg.lstsq(weighted_matrix, weighted_y, rcond=None)
        model = coeffs[0] + coeffs[1] * x
        residual = y - model
        center_resid, mad, _ = robust_stats(residual, mask)
        sigma = max(0.025, mad, float(np.median(np.clip(err[mask], V_ERROR_FLOOR, V_ERROR_CEILING))))
        next_mask = np.abs(residual - center_resid) <= 4.5 * sigma
        if int(next_mask.sum()) < max(5, int(0.55 * y.size)):
            next_mask = mask
        if np.array_equal(next_mask, mask):
            break
        mask = next_mask

    model = coeffs[0] + coeffs[1] * x
    residual = y - model
    _, kept_mad, kept_rms = robust_stats(residual, mask)
    _, all_mad, all_rms = robust_stats(residual)
    dense = np.linspace(0.0, 1.0, SAMPLES, endpoint=False)
    carrier_dense = interpolate_shapes(shapes, dense, float(i_fit["phaseShift"])) @ np.asarray(i_fit["weights"], dtype=float)
    dense_x = (carrier_dense - center) / span
    dense_model = coeffs[0] + coeffs[1] * dense_x
    return {
        "phase": phase,
        "model": model,
        "denseModel": dense_model,
        "residual": residual,
        "mask": mask,
        "keptMad": kept_mad,
        "keptRms": kept_rms,
        "allMad": all_mad,
        "allRms": all_rms,
        "mean": float(coeffs[0]),
        "amplitude": float(coeffs[1]),
    }


def fit_job(job: dict[str, Any]) -> dict[str, Any]:
    star = job["star"]
    phot_i = job["photI"]
    phot_v = job.get("photV")
    current = job.get("current")
    family = str(star["family"])
    dictionary = select_dictionary(family, str(star["id"]), float(star["logp"]))
    if dictionary is None:
        return {"id": star["id"], "status": "no_dictionary"}

    i_fit = fit_i_dictionary(star, phot_i, dictionary)
    if i_fit is None:
        return {"id": star["id"], "status": "i_fit_failed"}

    current_i = current_model_i(current, float(star["iMag"]), i_fit["phase"])
    current_i_resid = phot_i[:, 1] - current_i if current_i is not None else np.full(phot_i.shape[0], np.nan)
    _, current_i_mad, current_i_rms = robust_stats(current_i_resid)

    dense_i_offsets = np.asarray(i_fit["denseModel"], dtype=float) - float(np.mean(i_fit["denseModel"]))
    curve: dict[str, Any] = {
        "iCurve": encode_light_curve(dense_i_offsets),
        "lightQuality": int(current.get("lightQuality", 2)) if isinstance(current, dict) else 2,
        "iRms": round_number(float(i_fit["keptRms"]), 4),
        "iN": int(phot_i.shape[0]),
        "iSpan": round_number(percentile_span(np.asarray(i_fit["denseModel"], dtype=float)), 4),
        "rawRms": round_number(float(i_fit["allRms"]), 4),
        "templateSource": "convex-dictionary-v1",
        "dictionaryActive": int(i_fit["activeTemplates"]),
        "dictionaryEffective": round_number(float(i_fit["effectiveTemplates"]), 3),
        "dictionaryPhaseOffset": round_number(float(i_fit["phaseShift"]), 6),
        "dictionaryRawKept": int(np.sum(i_fit["mask"])),
        "dictionaryRawRejected": int(np.sum(~np.asarray(i_fit["mask"], dtype=bool))),
    }
    if isinstance(current, dict) and "variabilityFlags" in current:
        curve["variabilityFlags"] = current.get("variabilityFlags", [])

    row: dict[str, Any] = {
        "id": star["id"],
        "dataset": star["dataset"],
        "location": star["location"],
        "family": family,
        "period": star["period"],
        "logP": star["logp"],
        "iN": int(phot_i.shape[0]),
        "vN": int(phot_v.shape[0]) if isinstance(phot_v, np.ndarray) else 0,
        "currentLightQuality": current.get("lightQuality", 0) if isinstance(current, dict) else 0,
        "currentColorQuality": current.get("quality", 0) if isinstance(current, dict) else 0,
        "currentIMad": current_i_mad,
        "currentIRms": current_i_rms,
        "dictIMad": float(i_fit["allMad"]),
        "dictIRms": float(i_fit["allRms"]),
        "dictIKeptMad": float(i_fit["keptMad"]),
        "dictIKeptRms": float(i_fit["keptRms"]),
        "dictIRejected": int(np.sum(~np.asarray(i_fit["mask"], dtype=bool))),
        "dictPhaseOffset": float(i_fit["phaseShift"]),
        "dictActive": int(i_fit["activeTemplates"]),
        "dictEffective": float(i_fit["effectiveTemplates"]),
        "hasCurrentColor": bool(isinstance(current, dict) and "curve" in current),
        "status": "ok",
    }

    if isinstance(phot_v, np.ndarray) and phot_v.size:
        v_fit = fit_v_on_i_carrier(star, phot_v, dictionary, i_fit)
        if v_fit is not None:
            current_v = current_model_v(current, float(star["iMag"]), float(star["vMinusI"]), v_fit["phase"])
            current_v_resid = phot_v[:, 1] - current_v if current_v is not None else np.full(phot_v.shape[0], np.nan)
            _, current_v_mad, current_v_rms = robust_stats(current_v_resid)
            color_curve = np.asarray(v_fit["denseModel"], dtype=float) - np.asarray(i_fit["denseModel"], dtype=float)
            color_offsets = color_curve - float(np.mean(color_curve))
            curve.update(
                {
                    "curve": encode_color_curve(color_offsets),
                    "quality": int(current.get("quality", 2)) if isinstance(current, dict) and current.get("quality", 0) else 2,
                    "vRms": round_number(float(v_fit["keptRms"]), 4),
                    "vN": int(phot_v.shape[0]),
                    "span": round_number(percentile_span(color_offsets), 4),
                    "vAmplitude": round_number(float(prep.peak_to_peak(np.asarray(v_fit["denseModel"], dtype=float))), 4),
                    "sharedPhaseOffset": round_number(float(i_fit["phaseShift"]), 6),
                    "vTemplateSource": "convex-i-carrier-v1",
                }
            )
            row.update(
                {
                    "currentVMad": current_v_mad,
                    "currentVRms": current_v_rms,
                    "dictVMad": float(v_fit["allMad"]),
                    "dictVRms": float(v_fit["allRms"]),
                    "dictVKeptMad": float(v_fit["keptMad"]),
                    "dictVKeptRms": float(v_fit["keptRms"]),
                    "dictVRejected": int(np.sum(~np.asarray(v_fit["mask"], dtype=bool))),
                }
            )

    return {"id": star["id"], "status": "ok", "curve": curve, "row": row}


def load_feature_groups(stars_by_id: dict[str, prep.CatalogStar]) -> dict[str, dict[str, np.ndarray]]:
    with np.load(FEATURE_CACHE, allow_pickle=False) as payload:
        ids = payload["ids"].astype(str)
        shapes = payload["shapes"].astype(float)
    grouped: dict[str, list[tuple[str, float, np.ndarray]]] = {family: [] for family in prep.PCA_FAMILIES}
    for index, obj_id in enumerate(ids):
        star = stars_by_id.get(str(obj_id))
        if star is None or star.dataset not in {"cepheids", "rrlyrae", "anomalousCepheids"} or star.light_curve is None:
            continue
        family = prep.template_family(star)
        if family not in grouped:
            continue
        period = float(star.light_curve.get("period", star.period))
        grouped[family].append((str(obj_id), math.log10(period), shapes[index]))

    result: dict[str, dict[str, np.ndarray]] = {}
    for family, rows in grouped.items():
        rows.sort(key=lambda item: item[1])
        result[family] = {
            "ids": np.asarray([item[0] for item in rows]),
            "logp": np.asarray([item[1] for item in rows], dtype=float),
            "shapes": np.asarray([item[2] for item in rows], dtype=float),
        }
    return result


def load_current_curves() -> dict[str, dict[str, Any]]:
    if not CURRENT_CURVE_CACHE.exists():
        return {}
    payload = json.loads(CURRENT_CURVE_CACHE.read_text(encoding="utf-8"))
    return payload.get("curves", {})


def build_jobs(limit: int | None = None) -> tuple[list[dict[str, Any]], dict[str, dict[str, np.ndarray]], dict[str, dict[str, Any]]]:
    pulsators = (
        prep.parse_cepheids(prep.RAW / "ogle_cepheids_table3.dat")
        + prep.parse_rr_lyrae(prep.RAW / "ogle_rrlyrae_table2.dat")
        + prep.parse_anomalous_cepheids()
    )
    light_curve_parameters = prep.load_light_curve_parameters()
    for star in pulsators:
        star.light_curve = light_curve_parameters.get(star.obj_id)
    stars_by_id = {star.obj_id: star for star in pulsators}
    features_by_family = load_feature_groups(stars_by_id)
    current_curves = load_current_curves()

    grouped: dict[tuple[str, str], list[prep.CatalogStar]] = {}
    for star in pulsators:
        if star.light_curve is None:
            continue
        family = prep.template_family(star)
        if family not in set(prep.PCA_FAMILIES):
            continue
        group = prep.photometry_archive_group(star)
        if group is not None:
            grouped.setdefault(group, []).append(star)

    jobs: list[dict[str, Any]] = []
    for group, stars in grouped.items():
        wanted = {star.obj_id for star in stars}
        archive = prep.PHOTOMETRY_ARCHIVES[group]
        photometry = prep.read_photometry_archive(Path(archive["path"]), wanted)
        for star in stars:
            bands = photometry.get(star.obj_id, {})
            phot_i = bands.get("I")
            if phot_i is None or phot_i.shape[0] < 25:
                continue
            period = float(star.light_curve.get("period", star.period)) if star.light_curve else star.period
            t0 = float(star.light_curve["t0"]) if star.light_curve else 0.0
            star_payload = {
                "id": star.obj_id,
                "dataset": star.dataset,
                "location": star.location,
                "family": prep.template_family(star),
                "period": period,
                "logp": math.log10(period),
                "t0": t0,
                "iMag": star.i_mag,
                "vMag": star.v_mag,
                "vMinusI": star.v_mag - star.i_mag,
            }
            jobs.append(
                {
                    "star": star_payload,
                    "photI": phot_i,
                    "photV": bands.get("V"),
                    "current": current_curves.get(star.obj_id, {}),
                }
            )
            if limit is not None and len(jobs) >= limit:
                return jobs, features_by_family, current_curves
    return jobs, features_by_family, current_curves


def summarize_values(values: list[float]) -> dict[str, Any]:
    arr = np.asarray([value for value in values if math.isfinite(float(value))], dtype=float)
    if arr.size == 0:
        return {"count": 0}
    return {
        "count": int(arr.size),
        "median": round_number(float(np.median(arr)), 5),
        "p10": round_number(float(np.percentile(arr, 10)), 5),
        "p25": round_number(float(np.percentile(arr, 25)), 5),
        "p75": round_number(float(np.percentile(arr, 75)), 5),
        "p90": round_number(float(np.percentile(arr, 90)), 5),
    }


def improvement_summary(rows: list[dict[str, Any]], current_key: str, new_key: str) -> dict[str, Any]:
    pairs = [
        (float(row[current_key]), float(row[new_key]))
        for row in rows
        if row.get(current_key) not in (None, "") and row.get(new_key) not in (None, "")
        and math.isfinite(float(row[current_key]))
        and math.isfinite(float(row[new_key]))
        and float(row[current_key]) > 0
    ]
    if not pairs:
        return {"count": 0}
    current = np.asarray([pair[0] for pair in pairs], dtype=float)
    new = np.asarray([pair[1] for pair in pairs], dtype=float)
    ratio = new / current
    delta = current - new
    return {
        "count": int(len(pairs)),
        "currentMedian": round_number(float(np.median(current)), 5),
        "newMedian": round_number(float(np.median(new)), 5),
        "medianRatio": round_number(float(np.median(ratio)), 5),
        "p10Ratio": round_number(float(np.percentile(ratio, 10)), 5),
        "p90Ratio": round_number(float(np.percentile(ratio, 90)), 5),
        "improvedFraction": round_number(float(np.mean(delta > 0)), 4),
        "medianImprovement": round_number(float(np.median(delta)), 5),
    }


def build_summary(rows: list[dict[str, Any]], failures: dict[str, int], jobs: int, elapsed: float) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "version": VERSION,
        "jobs": jobs,
        "fitCount": len(rows),
        "failures": failures,
        "elapsedSeconds": round_number(elapsed, 3),
        "settings": {
            "dictionaryNeighbors": DICTIONARY_NEIGHBORS,
            "ridgeStrength": RIDGE_STRENGTH,
            "periodRidgeStrength": PERIOD_RIDGE_STRENGTH,
            "shiftRange": [SHIFT_MIN, SHIFT_MAX],
            "shiftCoarseCount": SHIFT_COARSE_COUNT,
        },
        "overall": {},
        "byFamily": {},
    }
    summary["overall"] = {
        "iRms": improvement_summary(rows, "currentIRms", "dictIRms"),
        "iMad": improvement_summary(rows, "currentIMad", "dictIMad"),
        "vRms": improvement_summary(rows, "currentVRms", "dictVRms"),
        "vMad": improvement_summary(rows, "currentVMad", "dictVMad"),
        "activeTemplates": summarize_values([float(row["dictActive"]) for row in rows if "dictActive" in row]),
        "effectiveTemplates": summarize_values([float(row["dictEffective"]) for row in rows if "dictEffective" in row]),
    }
    for family in sorted({str(row["family"]) for row in rows}):
        family_rows = [row for row in rows if str(row["family"]) == family]
        summary["byFamily"][family] = {
            "count": len(family_rows),
            "iRms": improvement_summary(family_rows, "currentIRms", "dictIRms"),
            "iMad": improvement_summary(family_rows, "currentIMad", "dictIMad"),
            "vRms": improvement_summary(family_rows, "currentVRms", "dictVRms"),
            "vMad": improvement_summary(family_rows, "currentVMad", "dictVMad"),
            "activeTemplates": summarize_values([float(row["dictActive"]) for row in family_rows if "dictActive" in row]),
            "effectiveTemplates": summarize_values([float(row["dictEffective"]) for row in family_rows if "dictEffective" in row]),
        }
    return summary


def write_outputs(curves: dict[str, dict[str, Any]], rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    OUT_CACHE.parent.mkdir(parents=True, exist_ok=True)
    OUT_CACHE.write_text(
        json.dumps(
            {
                "version": VERSION,
                "samples": SAMPLES,
                "lightEncoding": "int16le",
                "lightScale": prep.LIGHT_CURVE_INT16_SCALE,
                "colorScale": prep.COLOR_CURVE_SCALE,
                "colorZero": prep.COLOR_CURVE_ZERO,
                "summary": summary,
                "curves": curves,
            },
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "dataset",
        "location",
        "family",
        "period",
        "logP",
        "iN",
        "vN",
        "currentLightQuality",
        "currentColorQuality",
        "hasCurrentColor",
        "currentIMad",
        "dictIMad",
        "currentIRms",
        "dictIRms",
        "dictIKeptMad",
        "dictIKeptRms",
        "dictIRejected",
        "currentVMad",
        "dictVMad",
        "currentVRms",
        "dictVRms",
        "dictVKeptMad",
        "dictVKeptRms",
        "dictVRejected",
        "dictPhaseOffset",
        "dictActive",
        "dictEffective",
    ]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--workers", type=int, default=max(1, min(8, (prep.os.cpu_count() or 2) - 1)))
    args = parser.parse_args()

    import time

    start = time.perf_counter()
    jobs, features_by_family, _ = build_jobs(args.limit)
    failures: dict[str, int] = {}
    rows: list[dict[str, Any]] = []
    curves: dict[str, dict[str, Any]] = {}

    if args.workers <= 1:
        init_worker(features_by_family)
        for index, job in enumerate(jobs, 1):
            result = fit_job(job)
            status = str(result.get("status", "unknown"))
            if status == "ok":
                rows.append(result["row"])
                curves[str(result["id"])] = result["curve"]
            else:
                failures[status] = failures.get(status, 0) + 1
            if index % 250 == 0:
                print(f"Processed {index}/{len(jobs)}")
    else:
        with ProcessPoolExecutor(max_workers=args.workers, initializer=init_worker, initargs=(features_by_family,)) as executor:
            futures = [executor.submit(fit_job, job) for job in jobs]
            for index, future in enumerate(as_completed(futures), 1):
                result = future.result()
                status = str(result.get("status", "unknown"))
                if status == "ok":
                    rows.append(result["row"])
                    curves[str(result["id"])] = result["curve"]
                else:
                    failures[status] = failures.get(status, 0) + 1
                if index % 250 == 0:
                    print(f"Processed {index}/{len(jobs)}")

    elapsed = time.perf_counter() - start
    summary = build_summary(rows, failures, len(jobs), elapsed)
    write_outputs(curves, rows, summary)
    print(json.dumps(summary, indent=2))
    print(f"Wrote {OUT_CACHE}")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_SUMMARY}")


if __name__ == "__main__":
    main()
