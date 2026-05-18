from __future__ import annotations

import numpy as np

import build_xmc_rc_density_advanced as density


LMC_PM_CENTER = (1.91, 0.23)
SMC_PM_CENTER = (0.77, -1.12)
ODEN_LIKE_LMC_PM_RADIUS = 1.5
ODEN_LIKE_SMC_PM_RADIUS = 1.2
ODEN_LIKE_PM_CLIP_RADII = {
    "LMC": (6.0, 4.0, 2.5, ODEN_LIKE_LMC_PM_RADIUS),
    "SMC": (6.0, 4.0, 2.5, ODEN_LIKE_SMC_PM_RADIUS),
}

LOCAL_CMD_MAG_SIGMA = 1.2
LOCAL_CMD_COLOR_SIGMA = 1.5
LOCAL_CMD_MAX_RADIUS_CELLS = 8
LOCAL_CMD_MIN_NEIGHBORS = 80
LOCAL_CMD_ABSOLUTE_MIN_NEIGHBORS = 25
LOCAL_CMD_G_SIGMA_FLOOR = 0.12
LOCAL_CMD_COLOR_SIGMA_FLOOR = 0.035


def iterative_pm_clip(
    pmra: np.ndarray,
    pmdec: np.ndarray,
    base_mask: np.ndarray,
    clip_radii: tuple[float, ...],
) -> tuple[np.ndarray, dict[str, object]]:
    current = base_mask.copy()
    centers = []
    for radius in clip_radii:
        if not np.any(current):
            break
        center_ra = float(np.median(pmra[current]))
        center_dec = float(np.median(pmdec[current]))
        current = base_mask & (np.hypot(pmra - center_ra, pmdec - center_dec) <= radius)
        centers.append(
            {
                "radiusMasYr": radius,
                "centerPmra": center_ra,
                "centerPmdec": center_dec,
                "sampleRows": int(np.count_nonzero(current)),
            }
        )
    return current, {"steps": centers}


def oden_like_iterative_pm_mask(
    pmra: np.ndarray,
    pmdec: np.ndarray,
    nearest_cloud: np.ndarray,
) -> tuple[np.ndarray, dict[str, object]]:
    masks = {}
    stats = {}
    for cloud, radii in ODEN_LIKE_PM_CLIP_RADII.items():
        masks[cloud], stats[cloud] = iterative_pm_clip(pmra, pmdec, nearest_cloud == cloud, radii)
    return masks["LMC"] | masks["SMC"], stats


def build_local_cmd_core_scores(
    g0: np.ndarray,
    color0: np.ndarray,
    lon_bin: np.ndarray,
    lat_bin: np.ndarray,
    candidate_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    indices_by_bin: dict[tuple[int, int], list[int]] = {}
    for index in np.flatnonzero(candidate_mask):
        key = (int(lon_bin[index]), int(lat_bin[index]))
        indices_by_bin.setdefault(key, []).append(int(index))

    offsets_by_radius = {
        radius: density.circular_offsets(radius)
        for radius in range(LOCAL_CMD_MAX_RADIUS_CELLS + 1)
    }
    stats_by_bin: dict[tuple[int, int], tuple[float, float, float, float, int, int]] = {}

    for key in sorted(indices_by_bin):
        gathered: list[int] = []
        used_radius = LOCAL_CMD_MAX_RADIUS_CELLS
        for radius in range(LOCAL_CMD_MAX_RADIUS_CELLS + 1):
            gathered = []
            for dx, dy in offsets_by_radius[radius]:
                gathered.extend(indices_by_bin.get((key[0] + dx, key[1] + dy), ()))
            if len(gathered) >= LOCAL_CMD_MIN_NEIGHBORS:
                used_radius = radius
                break
        if len(gathered) < LOCAL_CMD_ABSOLUTE_MIN_NEIGHBORS:
            continue

        local_g0 = g0[gathered]
        local_color0 = color0[gathered]
        median_g0 = float(np.median(local_g0))
        median_color0 = float(np.median(local_color0))
        sigma_g0 = max(
            LOCAL_CMD_G_SIGMA_FLOOR,
            1.4826 * float(np.median(np.abs(local_g0 - median_g0))),
        )
        sigma_color0 = max(
            LOCAL_CMD_COLOR_SIGMA_FLOOR,
            1.4826 * float(np.median(np.abs(local_color0 - median_color0))),
        )
        stats_by_bin[key] = (
            median_g0,
            median_color0,
            sigma_g0,
            sigma_color0,
            used_radius,
            len(gathered),
        )

    mag_score = np.full(len(g0), np.inf, dtype=float)
    color_score = np.full(len(g0), np.inf, dtype=float)
    missing = 0
    for index in np.flatnonzero(candidate_mask):
        stats = stats_by_bin.get((int(lon_bin[index]), int(lat_bin[index])))
        if stats is None:
            missing += 1
            continue
        median_g0, median_color0, sigma_g0, sigma_color0, _, _ = stats
        mag_score[index] = abs(float(g0[index] - median_g0)) / sigma_g0
        color_score[index] = abs(float(color0[index] - median_color0)) / sigma_color0

    radii = np.array([row[4] for row in stats_by_bin.values()], dtype=float)
    neighbors = np.array([row[5] for row in stats_by_bin.values()], dtype=float)
    summary = {
        "bins": len(stats_by_bin),
        "candidateRowsMissingLocalCmdStats": missing,
        "magSigmaMax": LOCAL_CMD_MAG_SIGMA,
        "colorSigmaMax": LOCAL_CMD_COLOR_SIGMA,
        "minNeighbors": LOCAL_CMD_MIN_NEIGHBORS,
        "absoluteMinNeighbors": LOCAL_CMD_ABSOLUTE_MIN_NEIGHBORS,
        "maxRadiusCells": LOCAL_CMD_MAX_RADIUS_CELLS,
        "maxRadiusDeg": LOCAL_CMD_MAX_RADIUS_CELLS / density.BIN_SCALE,
        "medianRadiusCells": float(np.median(radii)) if len(radii) else None,
        "p90RadiusCells": float(np.percentile(radii, 90)) if len(radii) else None,
        "medianNeighbors": float(np.median(neighbors)) if len(neighbors) else None,
        "gSigmaFloorMag": LOCAL_CMD_G_SIGMA_FLOOR,
        "colorSigmaFloorMag": LOCAL_CMD_COLOR_SIGMA_FLOOR,
    }
    return mag_score, color_score, summary


def local_observed_cmd_core_mask(
    g0: np.ndarray,
    color0: np.ndarray,
    lon_bin: np.ndarray,
    lat_bin: np.ndarray,
    candidate_mask: np.ndarray,
    mag_sigma: float = LOCAL_CMD_MAG_SIGMA,
    color_sigma: float = LOCAL_CMD_COLOR_SIGMA,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, object]]:
    mag_score, color_score, stats = build_local_cmd_core_scores(
        g0,
        color0,
        lon_bin,
        lat_bin,
        candidate_mask,
    )
    selected = candidate_mask & (mag_score <= mag_sigma) & (color_score <= color_sigma)
    stats = {
        **stats,
        "magSigmaMax": mag_sigma,
        "colorSigmaMax": color_sigma,
        "selectedSampleRows": int(np.count_nonzero(selected)),
    }
    return selected, mag_score, color_score, stats
