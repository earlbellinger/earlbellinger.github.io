from __future__ import annotations

import argparse
import gzip
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import brotli
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))
sys.path.insert(0, str(ROOT / "scripts"))

import build_xmc_rc_density_advanced as density  # noqa: E402
import validate_oden_recovery as recovery  # noqa: E402
import xmc_rc_selection as rc_selection  # noqa: E402


DEFAULT_OUTPUT = ROOT / "public" / "data" / "xmc-red-clump-volume-5pct-calibrated.json"
DEFAULT_VALIDATION = ROOT / "diagnostics" / "oden_recovery_validation_5pct_calibrated.json"
DEFAULT_ATLAS = ROOT / "public" / "data" / "magellanic-clouds.json"
DEFAULT_SAMPLE_FRACTION = 0.05
DEFAULT_MIN_COUNT = 90
DEFAULT_MAX_RADIUS_CELLS = 10
ANCHOR_ODEN = "oden"
ANCHOR_PHOTOMETRIC = "photometric"
LMC_INNER_SIGMA_KPC = 1.5
LMC_OUTER_SIGMA_KPC = 2.35
SMC_CORE_SIGMA_KPC = 2.9
SMC_EXTENDED_SIGMA_KPC = 5.0
LMC_PHOTOMETRIC_SIGMA_KPC = 10.6
SMC_PHOTOMETRIC_SIGMA_KPC = 8.8
VOLUME_CONFIDENCE_FLOOR = 0.1
VOLUME_CONFIDENCE_MIN_COUNT = 20.0
VOLUME_CONFIDENCE_FULL_COUNT = 200.0


def round_float(value: float, digits: int = 4) -> float:
    if not math.isfinite(value):
        return 0.0
    return round(float(value), digits)


def clamp(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))


def smooth_step(value: float) -> float:
    value = clamp(value, 0.0, 1.0)
    return value * value * (3.0 - 2.0 * value)


def wrap_degrees(value: float) -> float:
    return ((value + 180.0) % 360.0) - 180.0


def angular_sep_scalar(lon: float, lat: float, center: tuple[float, float]) -> float:
    lon1 = math.radians(lon)
    lat1 = math.radians(lat)
    lon2 = math.radians(center[0])
    lat2 = math.radians(center[1])
    cos_sep = math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)
    return math.degrees(math.acos(clamp(cos_sep, -1.0, 1.0)))


def smc_wing_unit(lon: float, lat: float) -> float:
    smc_to_lmc_lat = recovery.LMC_CENTER[1] - recovery.SMC_CENTER[1]
    smc_to_lmc_lon = wrap_degrees(recovery.LMC_CENTER[0] - recovery.SMC_CENTER[0]) * math.cos(
        math.radians((recovery.LMC_CENTER[1] + recovery.SMC_CENTER[1]) * 0.5)
    )
    row_from_smc_lat = lat - recovery.SMC_CENTER[1]
    row_from_smc_lon = wrap_degrees(lon - recovery.SMC_CENTER[0]) * math.cos(
        math.radians((lat + recovery.SMC_CENTER[1]) * 0.5)
    )
    smc_to_lmc_length = math.hypot(smc_to_lmc_lon, smc_to_lmc_lat) or 1.0
    projection_toward_lmc = (
        row_from_smc_lon * smc_to_lmc_lon + row_from_smc_lat * smc_to_lmc_lat
    ) / smc_to_lmc_length
    cross_track = abs(
        row_from_smc_lon * smc_to_lmc_lat - row_from_smc_lat * smc_to_lmc_lon
    ) / smc_to_lmc_length
    toward_lmc = smooth_step((projection_toward_lmc - 1.2) / 5.5)
    narrow = 1.0 - smooth_step((cross_track - 3.2) / 4.5)
    return toward_lmc * narrow


def line_of_sight_sigma_kpc(q16: float, q84: float, nearest_cloud: str, lon: float, lat: float) -> float:
    observed_sigma = max(0.0, float(q84 - q16) * 0.5)
    if nearest_cloud == "LMC":
        separation = angular_sep_scalar(lon, lat, recovery.LMC_CENTER)
        prior_sigma = LMC_INNER_SIGMA_KPC + (LMC_OUTER_SIGMA_KPC - LMC_INNER_SIGMA_KPC) * smooth_step(
            (separation - 4.0) / 7.0
        )
        excess = math.sqrt(max(0.0, observed_sigma * observed_sigma - LMC_PHOTOMETRIC_SIGMA_KPC**2))
        return clamp(prior_sigma + min(0.85, excess * 0.12), 0.85, 3.2)

    separation = angular_sep_scalar(lon, lat, recovery.SMC_CENTER)
    wing_unit = smc_wing_unit(lon, lat)
    prior_sigma = SMC_CORE_SIGMA_KPC + (SMC_EXTENDED_SIGMA_KPC - SMC_CORE_SIGMA_KPC) * smooth_step(
        (separation - 2.0) / 6.0
    )
    prior_sigma += wing_unit * 1.2
    excess = math.sqrt(max(0.0, observed_sigma * observed_sigma - SMC_PHOTOMETRIC_SIGMA_KPC**2))
    return clamp(prior_sigma + min(1.6, excess * 0.2), 1.8, 7.5)


def load_validation_summary(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    experiments = payload.get("experiments", {})
    best_name = next(
        (
            name
            for name in (
                "native_min50",
                "native_min20",
                "native_min10",
                "adaptive_min100_max8",
                "adaptive_min50_max6",
                "adaptive_min200_max10",
            )
            if name in experiments
        ),
        None,
    )
    experiment = experiments.get(best_name, {}) if best_name else {}
    return {
        "method": payload.get("method"),
        "selectionMode": payload.get("selectionMode"),
        "counts": payload.get("counts"),
        "bestHeldOutExperiment": best_name,
        "summaries": experiment.get("summaries"),
    }


def js_round(value: float) -> int:
    return math.floor(value + 0.5)


def load_red_clump_density_by_key(path: Path) -> dict[tuple[int, int], tuple[float, float]]:
    if not path.exists():
        return {}

    payload = json.loads(path.read_text(encoding="utf-8"))
    fields = {name: index for index, name in enumerate(payload.get("fields", {}).get("redClump", []))}
    required = ("galLonDeg", "galLatDeg", "densityCount", "densityUnit")
    if any(name not in fields for name in required):
        return {}

    density_by_key: dict[tuple[int, int], tuple[float, float]] = {}
    for row in payload.get("datasets", {}).get("redClump", []):
        lon = float(row[fields["galLonDeg"]])
        lat = float(row[fields["galLatDeg"]])
        key = (js_round(lon * density.BIN_SCALE), js_round(lat * density.BIN_SCALE))
        density_by_key[key] = (
            float(row[fields["densityCount"]]),
            float(row[fields["densityUnit"]]),
        )
    return density_by_key


def select_rc_sample(sample_path: Path, filter_args: SimpleNamespace, oden_by_key: dict[tuple[int, int], tuple[float, float, float]]):
    frame = pd.read_csv(
        sample_path,
        usecols=list(recovery.GAIA_USECOLS),
        dtype=recovery.GAIA_DTYPES,
    )
    lon = frame["l"].to_numpy(dtype=float)
    lat = frame["b"].to_numpy(dtype=float)
    g = frame["phot_g_mean_mag"].to_numpy(dtype=float)
    bp_rp = frame["bp_rp"].to_numpy(dtype=float)
    pmra = frame["pmra"].to_numpy(dtype=float)
    pmdec = frame["pmdec"].to_numpy(dtype=float)

    image, wcs = density.load_reddening_map()
    ebv = density.reddening_at(lon, lat, image, wcs)
    valid_extinction = np.isfinite(ebv) & (ebv >= -0.05) & (ebv <= 2.0)
    g0 = g - density.A_G_PER_EBV * ebv
    color0 = bp_rp - density.E_BP_RP_PER_EBV * ebv

    rc_cmd = valid_extinction & (
        (
            (g0 >= filter_args.lmc_g0_min)
            & (g0 <= filter_args.lmc_g0_max)
            & (color0 >= filter_args.lmc_bp_rp0_min)
            & (color0 <= filter_args.lmc_bp_rp0_max)
        )
        | (
            (g0 >= filter_args.smc_g0_min)
            & (g0 <= filter_args.smc_g0_max)
            & (color0 >= filter_args.smc_bp_rp0_min)
            & (color0 <= filter_args.smc_bp_rp0_max)
        )
    )

    lon_bin, lat_bin = density.sky_bins(lon, lat)
    lmc_sep = recovery.angular_sep_deg(lon, lat, recovery.LMC_CENTER)
    smc_sep = recovery.angular_sep_deg(lon, lat, recovery.SMC_CENTER)
    nearest_cloud_all = np.where(lmc_sep <= smc_sep, "LMC", "SMC")
    oden_like_pm, iterative_pm_stats = rc_selection.oden_like_iterative_pm_mask(pmra, pmdec, nearest_cloud_all)
    candidate = oden_like_pm & rc_cmd
    local_cmd_core, _, _, local_cmd_stats = rc_selection.local_observed_cmd_core_mask(
        g0,
        color0,
        lon_bin,
        lat_bin,
        candidate,
    )
    selected_all = np.flatnonzero(local_cmd_core)
    oden_distance = np.array(
        [oden_by_key.get((int(x), int(y)), (np.nan, np.nan, np.nan))[2] for x, y in zip(lon_bin[selected_all], lat_bin[selected_all])],
        dtype=float,
    )
    in_oden = np.isfinite(oden_distance)
    selected = selected_all[in_oden]
    oden_distance = oden_distance[in_oden]
    nearest_cloud = nearest_cloud_all[selected]

    return {
        "frameRows": len(frame),
        "validExtinctionRows": int(np.count_nonzero(valid_extinction)),
        "rcCmdRows": int(np.count_nonzero(rc_cmd)),
        "odenLikePmRows": int(np.count_nonzero(oden_like_pm)),
        "odenLikePmRcRows": int(np.count_nonzero(candidate)),
        "localObservedCmdCoreRows": int(len(selected_all)),
        "selectedRowsInOdenCells": int(len(selected)),
        "selected": selected,
        "lon": lon,
        "lat": lat,
        "lonBin": lon_bin,
        "latBin": lat_bin,
        "g0": g0,
        "color0": color0,
        "odenDistance": oden_distance,
        "nearestCloud": nearest_cloud,
        "iterativePmStats": iterative_pm_stats,
        "localObservedCmdStats": local_cmd_stats,
    }


def fit_models(sample: dict[str, object]) -> dict[str, dict[str, object]]:
    selected = sample["selected"]
    color0 = sample["color0"][selected]
    g0 = sample["g0"][selected]
    oden_distance = sample["odenDistance"]
    nearest_cloud = sample["nearestCloud"]
    implied_absolute_g = g0 - recovery.distance_modulus(oden_distance)

    models: dict[str, dict[str, object]] = {}
    for cloud in ("LMC", "SMC"):
        mask = nearest_cloud == cloud
        models[cloud] = recovery.robust_polyfit(color0[mask], implied_absolute_g[mask])
    return models


def predict_distances(sample: dict[str, object], models: dict[str, dict[str, object]]) -> np.ndarray:
    selected = sample["selected"]
    color0 = sample["color0"][selected]
    g0 = sample["g0"][selected]
    nearest_cloud = sample["nearestCloud"]
    absolute_g = np.empty(len(selected), dtype=float)
    for cloud in ("LMC", "SMC"):
        mask = nearest_cloud == cloud
        absolute_g[mask] = recovery.evaluate_model(color0[mask], models[cloud])
    predicted = 10 ** ((g0 - absolute_g + 5.0) / 5.0) / 1000.0
    predicted[~np.isfinite(predicted)] = np.nan
    predicted[(predicted < 30.0) | (predicted > 90.0)] = np.nan
    return predicted


def predict_ruiz_dern_distances(sample: dict[str, object]) -> np.ndarray:
    selected = sample["selected"]
    color0 = sample["color0"][selected]
    g0 = sample["g0"][selected]
    absolute_g = recovery.ruiz_dern_absolute_g_from_bp_rp0(color0)
    predicted = 10 ** ((g0 - absolute_g + 5.0) / 5.0) / 1000.0
    predicted[~np.isfinite(predicted)] = np.nan
    predicted[(predicted < 30.0) | (predicted > 90.0)] = np.nan
    return predicted


def kmeans_two_components(values: np.ndarray) -> tuple[np.ndarray, np.ndarray] | None:
    if len(values) < 120:
        return None
    centers = np.percentile(values, [30, 70]).astype(float)
    assignments = np.zeros(len(values), dtype=int)
    for _ in range(40):
        distances = np.abs(values[:, None] - centers[None, :])
        next_assignments = np.argmin(distances, axis=1)
        next_centers = centers.copy()
        for component in (0, 1):
            group = values[next_assignments == component]
            if len(group) > 0:
                next_centers[component] = float(np.median(group))
        if np.array_equal(assignments, next_assignments) and np.allclose(centers, next_centers):
            break
        assignments = next_assignments
        centers = next_centers

    order = np.argsort(centers)
    remapped = np.zeros_like(assignments)
    for new_index, old_index in enumerate(order):
        remapped[assignments == old_index] = new_index
    centers = centers[order]
    return centers, remapped


def bic_for_groups(values: np.ndarray, assignments: np.ndarray | None) -> float:
    n = len(values)
    if n == 0:
        return float("inf")
    if assignments is None:
        variance = np.var(values)
        parameters = 2
    else:
        variance_sum = 0.0
        for component in (0, 1):
            group = values[assignments == component]
            if len(group) == 0:
                return float("inf")
            variance_sum += float(np.sum((group - np.mean(group)) ** 2))
        variance = variance_sum / n
        parameters = 5
    variance = max(variance, 1e-4)
    return n * math.log(variance) + parameters * math.log(n)


def component_rows_for_cell(
    values: np.ndarray,
    oden_distance: float,
    nearest_cloud: str,
    lon_deg: float,
    lat_deg: float,
    anchor_mode: str,
    min_component_fraction: float = 0.32,
) -> list[dict[str, float | int]]:
    q05, q16, q50, q84, q95 = np.percentile(values, [5, 16, 50, 84, 95])
    if anchor_mode == ANCHOR_ODEN:
        shift = oden_distance - float(q50)
        modeled = values + shift
        center_distance = oden_distance
        q05, q16, q50, q84, q95 = np.percentile(modeled, [5, 16, 50, 84, 95])
    elif anchor_mode == ANCHOR_PHOTOMETRIC:
        modeled = values
        center_distance = float(q50)
    else:
        raise ValueError(f"Unsupported volume anchor mode: {anchor_mode}")

    base_sigma = line_of_sight_sigma_kpc(float(q16), float(q84), nearest_cloud, lon_deg, lat_deg)
    base = {
        "median": float(q50),
        "q05": float(q05),
        "q16": float(q16),
        "q84": float(q84),
        "q95": float(q95),
    }

    wing_unit = smc_wing_unit(lon_deg, lat_deg)
    if nearest_cloud != "SMC" or wing_unit < 0.35 or (q95 - q05) < 8.0:
        return [{**base, "center": center_distance, "sigma": base_sigma, "weight": 1.0}]

    split = kmeans_two_components(modeled)
    if split is None:
        return [{**base, "center": center_distance, "sigma": base_sigma, "weight": 1.0}]

    centers, assignments = split
    groups = [modeled[assignments == component] for component in (0, 1)]
    fractions = np.array([len(group) / len(modeled) for group in groups])
    separation = float(abs(centers[1] - centers[0]))
    bic_single = bic_for_groups(modeled, None)
    bic_double = bic_for_groups(modeled, assignments)
    if (
        np.min(fractions) < min_component_fraction
        or separation < 7.0
        or separation > 20.0
        or bic_double > bic_single - 35.0
    ):
        return [{**base, "center": center_distance, "sigma": base_sigma, "weight": 1.0}]

    components: list[dict[str, float | int]] = []
    for component, group in enumerate(groups):
        c16, c50, c84 = np.percentile(group, [16, 50, 84])
        components.append(
            {
                **base,
                "center": float(c50),
                "sigma": clamp(
                    line_of_sight_sigma_kpc(float(c16), float(c84), nearest_cloud, lon_deg, lat_deg) * 0.86,
                    1.4,
                    6.5,
                ),
                "weight": float(fractions[component]),
            }
        )
    return components


def build_volume_components(
    sample: dict[str, object],
    predicted_distance: np.ndarray,
    oden_by_key: dict[tuple[int, int], tuple[float, float, float]],
    density_by_key: dict[tuple[int, int], tuple[float, float]],
    min_count: int,
    max_radius_cells: int,
    anchor_mode: str,
) -> tuple[list[list[float | int]], dict[str, object]]:
    selected = sample["selected"]
    sel_lon_bin = sample["lonBin"][selected]
    sel_lat_bin = sample["latBin"][selected]
    nearest_cloud = sample["nearestCloud"]
    selected_oden_distance = sample["odenDistance"]
    valid = np.isfinite(predicted_distance)

    values_by_key: dict[tuple[int, int], list[float]] = defaultdict(list)
    clouds_by_key: dict[tuple[int, int], list[str]] = defaultdict(list)
    for x, y, cloud, value, reference_distance in zip(
        sel_lon_bin[valid],
        sel_lat_bin[valid],
        nearest_cloud[valid],
        predicted_distance[valid],
        selected_oden_distance[valid],
    ):
        key = (int(x), int(y))
        if anchor_mode == ANCHOR_ODEN:
            residual = float(value - reference_distance)
            if not math.isfinite(residual) or abs(residual) > 25.0:
                continue
            values_by_key[key].append(residual)
        elif anchor_mode == ANCHOR_PHOTOMETRIC:
            distance_value = float(value)
            if not math.isfinite(distance_value) or distance_value < 25.0 or distance_value > 95.0:
                continue
            values_by_key[key].append(distance_value)
        else:
            raise ValueError(f"Unsupported volume anchor mode: {anchor_mode}")
        clouds_by_key[key].append(str(cloud))

    offsets_by_radius = {radius: density.circular_offsets(radius) for radius in range(max_radius_cells + 1)}
    rows: list[list[float | int]] = []
    cell_count = 0
    two_component_cells = 0
    radius_values: list[int] = []
    sample_counts: list[int] = []
    density_counts: list[float] = []
    confidence_values: list[float] = []

    for key, (lon, lat, oden_distance) in sorted(oden_by_key.items(), key=lambda item: (item[0][1], item[0][0])):
        gathered: list[float] = []
        clouds: list[str] = []
        used_radius = max_radius_cells
        for radius in range(max_radius_cells + 1):
            gathered = []
            clouds = []
            for dx, dy in offsets_by_radius[radius]:
                neighbor = (key[0] + dx, key[1] + dy)
                gathered.extend(values_by_key.get(neighbor, ()))
                clouds.extend(clouds_by_key.get(neighbor, ()))
            if len(gathered) >= min_count:
                used_radius = radius
                break
        if len(gathered) < min_count:
            continue

        if anchor_mode == ANCHOR_ODEN:
            values = oden_distance + np.array(gathered, dtype=float)
        else:
            values = np.array(gathered, dtype=float)
        nearest = "LMC" if clouds.count("LMC") >= clouds.count("SMC") else "SMC"
        cloud_index = 0 if nearest == "LMC" else 1
        components = component_rows_for_cell(values, oden_distance, nearest, lon, lat, anchor_mode)
        if len(components) > 1:
            two_component_cells += 1
        cell_count += 1
        radius_values.append(used_radius)
        sample_counts.append(len(values))
        cell_density_count, cell_density_unit = density_by_key.get(key, (0.0, 0.0))
        support_unit = math.log1p(len(values)) / math.log1p(1400)
        confidence_unit = VOLUME_CONFIDENCE_FLOOR + (1.0 - VOLUME_CONFIDENCE_FLOOR) * smooth_step(
            (cell_density_count - VOLUME_CONFIDENCE_MIN_COUNT)
            / (VOLUME_CONFIDENCE_FULL_COUNT - VOLUME_CONFIDENCE_MIN_COUNT)
        )
        density_counts.append(cell_density_count)
        confidence_values.append(confidence_unit)
        for component_index, component in enumerate(components):
            rows.append(
                [
                    key[0],
                    key[1],
                    round_float(lon, 4),
                    round_float(lat, 4),
                    round_float(float(component["center"]), 3),
                    round_float(float(component["sigma"]), 3),
                    round_float(float(component["weight"]), 4),
                    len(values),
                    used_radius,
                    round_float(float(component["median"]), 3),
                    round_float(float(component["q05"]), 3),
                    round_float(float(component["q16"]), 3),
                    round_float(float(component["q84"]), 3),
                    round_float(float(component["q95"]), 3),
                    len(components),
                    component_index,
                    round_float(clamp(cell_density_unit, 0.0, 1.0), 4),
                    cloud_index,
                    round_float(cell_density_count, 2),
                    round_float(clamp(support_unit, 0.0, 1.0), 4),
                    round_float(clamp(confidence_unit, VOLUME_CONFIDENCE_FLOOR, 1.0), 4),
                ]
            )

    stats = {
        "cells": cell_count,
        "components": len(rows),
        "twoComponentCells": two_component_cells,
        "radiusCellsMedian": float(np.median(radius_values)) if radius_values else None,
        "radiusCellsP90": float(np.percentile(radius_values, 90)) if radius_values else None,
        "sampleCountMedian": float(np.median(sample_counts)) if sample_counts else None,
        "sampleCountP90": float(np.percentile(sample_counts, 90)) if sample_counts else None,
        "densityCountMedian": float(np.median(density_counts)) if density_counts else None,
        "densityCountP90": float(np.percentile(density_counts, 90)) if density_counts else None,
        "confidenceMedian": float(np.median(confidence_values)) if confidence_values else None,
        "confidenceP90": float(np.percentile(confidence_values, 90)) if confidence_values else None,
    }
    return rows, stats


def write_compressed_siblings(path: Path, text: str) -> None:
    (path.with_suffix(path.suffix + ".gz")).write_bytes(gzip.compress(text.encode("utf-8"), compresslevel=9))
    (path.with_suffix(path.suffix + ".br")).write_bytes(brotli.compress(text.encode("utf-8"), quality=11))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Gaia red-clump line-of-sight volume asset.")
    parser.add_argument("--sample", type=Path, default=recovery.SAMPLE_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--atlas", type=Path, default=DEFAULT_ATLAS)
    parser.add_argument("--sample-fraction", type=float, default=DEFAULT_SAMPLE_FRACTION)
    parser.add_argument(
        "--distance-model",
        choices=("empirical-oden", "ruiz-dern-first-order"),
        default="empirical-oden",
        help=(
            "Star-level photometric distance model used for the line-of-sight component distribution. "
            "empirical-oden fits M_G((BP-RP)_0) to Oden cells. ruiz-dern-first-order uses Oden Eq. 8/9."
        ),
    )
    parser.add_argument(
        "--volume-anchor",
        choices=(ANCHOR_ODEN, ANCHOR_PHOTOMETRIC),
        default=ANCHOR_ODEN,
        help=(
            "oden shifts each local Gaia distance distribution onto the Oden cell median. "
            "photometric leaves the volume in the unanchored Gaia photometric distance distribution."
        ),
    )
    parser.add_argument("--min-count", type=int, default=DEFAULT_MIN_COUNT)
    parser.add_argument("--max-radius-cells", type=int, default=DEFAULT_MAX_RADIUS_CELLS)
    args = parser.parse_args()

    filter_args = recovery.load_filter_namespace(recovery.DENSITY_COUNTS_PATH)
    oden_by_key = recovery.load_oden_distance_map(recovery.ODEN_DISTANCE_FITS)
    density_by_key = load_red_clump_density_by_key(args.atlas)
    sample = select_rc_sample(args.sample, filter_args, oden_by_key)
    if args.distance_model == "empirical-oden":
        models = fit_models(sample)
        predicted_distance = predict_distances(sample, models)
        distance_note = (
            "Star-level photometric distances use a quadratic M_G((BP-RP)_0) relation fitted to Oden cell "
            "distances separately for LMC-nearest and SMC-nearest stars."
        )
    else:
        models = {}
        predicted_distance = predict_ruiz_dern_distances(sample)
        distance_note = (
            "Star-level photometric distances use Oden Eq. 8/9 directly: (BP-RP)_0 is transformed to "
            "(G-Ks)_0 and the Ruiz-Dern M_G((G-Ks)_0) RC calibration is applied."
        )
    if args.volume_anchor == ANCHOR_ODEN:
        anchor_label = "oden-anchored"
        source_suffix = "Oden et al. 2025 distance and reddening maps"
        anchor_note = (
            "Each component is anchored to the public Oden median-distance cell. Local "
            "photometric-distance residuals relative to each star's own Oden cell estimate "
            "line-of-sight structure."
        )
    else:
        anchor_label = "gaia-photometric-unanchored"
        source_suffix = "Oden et al. 2025 footprint/reddening maps"
        anchor_note = (
            "Component centers and q05/q95 depth bounds are computed directly from Gaia "
            "photometric red-clump distances. The Oden median-distance sheet is not used for "
            "volume placement."
        )
    components, volume_stats = build_volume_components(
        sample,
        predicted_distance,
        oden_by_key,
        density_by_key,
        min_count=args.min_count,
        max_radius_cells=args.max_radius_cells,
        anchor_mode=args.volume_anchor,
    )
    sample_fraction = float(args.sample_fraction)
    is_full_sample = sample_fraction >= 0.999
    method_prefix = "full-gaia" if is_full_sample else f"{sample_fraction:g}-fraction-gaia"
    source_prefix = "Gaia DR3 Oden-footprint tile download" if is_full_sample else "Gaia DR3 random_index sample"
    estimated_full_core = (
        int(sample["localObservedCmdCoreRows"])
        if is_full_sample or sample_fraction <= 0
        else int(round(int(sample["localObservedCmdCoreRows"]) / sample_fraction))
    )

    payload = {
        "meta": {
            "method": f"{method_prefix}-rc-calibrated-local-cmd-{anchor_label}-los-density-volume",
            "source": f"{source_prefix} + {source_suffix}",
            "sampleFraction": sample_fraction,
            "distanceModel": args.distance_model,
            "volumeAnchor": args.volume_anchor,
            "minCount": args.min_count,
            "maxRadiusCells": args.max_radius_cells,
            "maxRadiusDeg": args.max_radius_cells / density.BIN_SCALE,
            "densitySource": str(args.atlas.relative_to(ROOT) if args.atlas.is_relative_to(ROOT) else args.atlas),
            "confidence": {
                "floor": VOLUME_CONFIDENCE_FLOOR,
                "minCount": VOLUME_CONFIDENCE_MIN_COUNT,
                "fullCount": VOLUME_CONFIDENCE_FULL_COUNT,
                "note": "Volume opacity is gated by the target atlas RC density, not by the adaptive neighborhood used for LOS fitting.",
            },
            "note": (
                "Each component uses a calibrated Gaia local-CMD-core red-clump selection. "
                + anchor_note
                + " Sparse adaptive neighborhoods should be treated as low-confidence structure rather "
                "than independent distance recovery. "
                + distance_note
            ),
            "selection": {
                "method": "oden-like-iterative-pm-plus-local-observed-cmd-core",
                "note": (
                    "The broad fixed RC CMD boxes are tightened with Oden-like iterative proper-motion clipping "
                    "and a local observed-CMD core cut. The local core cut does not use Oden distances."
                ),
                "pmClipRadiiMasYr": rc_selection.ODEN_LIKE_PM_CLIP_RADII,
                "localObservedCmdCore": {
                    "magSigmaMax": rc_selection.LOCAL_CMD_MAG_SIGMA,
                    "colorSigmaMax": rc_selection.LOCAL_CMD_COLOR_SIGMA,
                    "gSigmaFloorMag": rc_selection.LOCAL_CMD_G_SIGMA_FLOOR,
                    "colorSigmaFloorMag": rc_selection.LOCAL_CMD_COLOR_SIGMA_FLOOR,
                    "minNeighbors": rc_selection.LOCAL_CMD_MIN_NEIGHBORS,
                    "absoluteMinNeighbors": rc_selection.LOCAL_CMD_ABSOLUTE_MIN_NEIGHBORS,
                    "maxRadiusCells": rc_selection.LOCAL_CMD_MAX_RADIUS_CELLS,
                },
            },
            "clouds": ["LMC", "SMC"],
            "depthCalibration": {
                "lmcInnerSigmaKpc": LMC_INNER_SIGMA_KPC,
                "lmcOuterSigmaKpc": LMC_OUTER_SIGMA_KPC,
                "smcCoreSigmaKpc": SMC_CORE_SIGMA_KPC,
                "smcExtendedSigmaKpc": SMC_EXTENDED_SIGMA_KPC,
                "lmcPhotometricSigmaKpc": LMC_PHOTOMETRIC_SIGMA_KPC,
                "smcPhotometricSigmaKpc": SMC_PHOTOMETRIC_SIGMA_KPC,
                "basis": "Oden 2025 depth scale, Choi 2018 LMC thickness, and Tatton 2020 SMC/wing depth.",
            },
            "selectionCounts": {
                "sampleRows": int(sample["frameRows"]),
                "validExtinctionRows": int(sample["validExtinctionRows"]),
                "rcCmdRows": int(sample["rcCmdRows"]),
                "odenLikePmRows": int(sample["odenLikePmRows"]),
                "odenLikePmRcRows": int(sample["odenLikePmRcRows"]),
                "localObservedCmdCoreRows": int(sample["localObservedCmdCoreRows"]),
                "selectedRowsInOdenCells": int(sample["selectedRowsInOdenCells"]),
                "estimatedFullLocalObservedCmdCoreRows": estimated_full_core,
            },
            "iterativePmStats": sample["iterativePmStats"],
            "localObservedCmdStats": sample["localObservedCmdStats"],
            "models": models,
            "volumeStats": volume_stats,
            "validation": load_validation_summary(args.validation),
        },
        "fields": {
            "components": [
                "lonBin",
                "latBin",
                "lonDeg",
                "latDeg",
                "centerDistanceKpc",
                "sigmaKpc",
                "weight",
                "sampleCount",
                "radiusCells",
                "medianDistanceKpc",
                "q05DistanceKpc",
                "q16DistanceKpc",
                "q84DistanceKpc",
                "q95DistanceKpc",
                "componentCount",
                "componentIndex",
                "densityUnit",
                "cloud",
                "cellDensityCount",
                "supportUnit",
                "confidenceUnit",
            ]
        },
        "components": components,
    }

    text = json.dumps(payload, separators=(",", ":"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    write_compressed_siblings(args.output, text)
    print(json.dumps(payload["meta"]["volumeStats"], indent=2))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
