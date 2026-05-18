"""Build production wire/structure metadata for the atlas annotation toggle.

This post-processes the generated atlas payload. It keeps the simple triaxial
Mira envelopes, draws LMC Cepheids as a fitted thick disk plus bar mixture,
draws SMC Cepheids as a Student-t primary component plus Gaussian secondary
component, draws RR Lyrae from simultaneous errors-in-variables mixtures, and
keeps Mira envelopes as simple triaxial summaries.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import os
from pathlib import Path

import numpy as np

from compare_wireframe_models import (
    DEFAULT_ATLAS,
    EIGEN_FLOOR,
    fit_gaussian_mixture,
    fit_single_gaussian,
    fit_surface_params,
    galactic_vector,
    positive_semidefinite,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = DEFAULT_ATLAS
CONFIDENCE_RADIUS = 1.878
PLANE_GRID_LINES = 5
PLANE_QUANTILE_RANGE = (0.04, 0.96)
CONTOUR_GRID_SIZE = 76
CONTOUR_LEVELS = (0.56, 0.84)
KDE3D_GRID_SHAPE = (48, 48, 34)
KDE3D_CONTAINMENT_LEVELS = (0.45, 0.74)
KDE3D_DEPTH_QUANTILES = (0.28, 0.5, 0.72)
KDE3D_ISOSURFACE_CONTAINMENT = 0.62
KDE3D_ISOSURFACE_MAX_SEGMENTS = 4200
LMC_CEPHEID_DISK_GMM_COMPONENTS = 7
LMC_CEPHEID_CORE_DENSITY_QUANTILE = 0.70
LMC_CEPHEID_RING_FOURIER_DEGREE = 3
LMC_CEPHEID_RING_ANGULAR_COMPONENTS = 5
LMC_CEPHEID_RING_ANGULAR_MASS = 0.95
LMC_CEPHEID_RING_RENDER_SAMPLES = 240
LMC_CEPHEID_RING_INNER_SIGMA = -0.25
LMC_CEPHEID_RING_OUTER_SIGMA = 1.2815515655
LMC_CEPHEID_RING_MIN_RADIUS = 1.55
LMC_CEPHEID_RESIDUAL_MASS_FRACTION = 0.32
LMC_CEPHEID_INITIAL_MAIN_FRACTION = 0.68
LMC_CEPHEID_MAIN_PRIOR = 0.68
LMC_CEPHEID_EM_ITERATIONS = 14
LMC_CEPHEID_RIPEPI_BAR_POLYGON_RA_DEC = (
    (88.90, -70.45),
    (76.30, -68.01),
    (74.28, -69.03),
    (87.95, -71.49),
)
LMC_CEPHEID_RIPEPI_CENTER_RA_DEC = (81.28, -69.78)
LMC_CEPHEID_RIPEPI_CONTOUR_LEVELS = (0.58, 0.94)
LMC_CEPHEID_DISK_CONTOUR_LEVELS = (0.58, 0.90)
LMC_CEPHEID_DISK_DENSITY_GRID_SIZE = 74
LMC_CEPHEID_DISK_THICKNESS_TICKS = 20
LMC_CEPHEID_BAR_DISK_SURFACE_MODELS = ("tilted-plane", "quadratic-warp")
LMC_CEPHEID_BAR_DISK_COMPONENT_OPTIONS = (2, 3, 4)
LMC_CEPHEID_BAR_DISK_EM_ITERATIONS = 40
LMC_CEPHEID_BAR_DISK_GMM_ITERATIONS = 70
LMC_CEPHEID_BAR_DISK_TOL = 8e-5
LMC_CEPHEID_RIPEPI_FEATURES = (
    {
        "id": "lmc-cepheids-eastern-bar",
        "label": "Eastern Bar",
        "selection": "ripepi-bar-east",
        "fontSizePx": 14,
        "featureScale": "major",
    },
    {
        "id": "lmc-cepheids-western-bar",
        "label": "Western Bar",
        "selection": "ripepi-bar-west",
        "fontSizePx": 14,
        "featureScale": "major",
    },
    {
        "id": "lmc-cepheids-northern-arms",
        "label": "Northern Arms",
        "selection": "multi-sky-seed",
        "seeds": (
            {
                "raDeg": 79.48,
                "decDeg": -66.08,
                "radiusRaDeg": 0.9,
                "radiusDecDeg": 0.75,
            },
            {
                "raDeg": 82.38,
                "decDeg": -64.98,
                "radiusRaDeg": 1.05,
                "radiusDecDeg": 0.8,
            },
        ),
        "fontSizePx": 13,
        "featureScale": "major",
    },
    {
        "id": "lmc-cepheids-southern-arm",
        "label": "Southern Arm",
        "seedRaDeg": 83.08,
        "seedDecDeg": -72.48,
        "radiusRaDeg": 0.95,
        "radiusDecDeg": 0.75,
        "fontSizePx": 13,
        "featureScale": "major",
    },
)
SMC_CEPHEID_CENTER_RA_DEC = (12.54, -73.11)
SMC_CEPHEID_LITERATURE_FEATURES = (
    {
        "id": "smc-cepheids-bar",
        "label": "SMC Bar",
        "selection": "sky-seed",
        "seedRaDeg": 12.54,
        "seedDecDeg": -73.11,
        "radiusRaDeg": 1.1,
        "radiusDecDeg": 1.1,
        "fontSizePx": 14,
        "featureScale": "major",
    },
    {
        "id": "smc-cepheids-shapley-wing",
        "label": "SMC Shapley Wing",
        "selection": "sky-seed",
        "seedRaDeg": 20.0,
        "seedDecDeg": -73.5,
        "radiusRaDeg": 0.8,
        "radiusDecDeg": 0.65,
        "fontSizePx": 14,
        "featureScale": "major",
    },
    {
        "id": "smc-cepheids-counter-bridge",
        "label": "SMC Counter-Bridge",
        "selection": "counter-bridge",
        "fontSizePx": 11,
        "featureScale": "minor",
    },
)
RR_SHELL_CONTAINMENT = (0.5, 0.84)
EIV_GMM_SKY_CORE_FRACTION = 0.55
EIV_GMM_SKY_WEIGHT_POWER = 2
EIV_GMM_DEPTH_ENDPOINT_CONTAINMENT = 0.995
EIV_GMM_DEPTH_ENDPOINT_WEIGHT = 0.2
EIV_GMM_COMPONENT_COUNTS = (1, 2, 3)
EIV_GMM_MAX_ITER = 240
EIV_GMM_TOL = 1e-6
EIV_GMM_ENVELOPE_CONTAINMENT = 0.82
STUDENT_T_DF_GRID = (3.0, 4.0, 6.0, 10.0, 20.0, 50.0)
STUDENT_T_BODY_CONTAINMENT = 0.68

EQ_TO_GAL = np.array(
    [
        [-0.0548755604162154, -0.8734370902348850, -0.4838350155487132],
        [0.4941094278755837, -0.4448296299600112, 0.7469822444972189],
        [-0.8676661490190047, -0.1980763734312015, 0.4559837761750669],
    ],
    dtype=float,
)
DEFAULT_VIEW_AXIS_ROTATION_DEGREES = 15.0

POPULATIONS = {
    "cepheids": {
        "label": "Cepheids",
        "dataset": 0,
        "color": "112, 227, 255",
    },
    "rrlyrae": {
        "label": "RR Lyrae",
        "dataset": 1,
        "color": "255, 217, 128",
    },
    "miras": {
        "label": "Miras",
        "dataset": 3,
        "color": "252, 163, 17",
    },
}
CLOUDS = {
    "lmc": {"label": "LMC", "location": 0, "lineDash": []},
    "smc": {"label": "SMC", "location": 1, "lineDash": []},
}
MAIN_COMPONENT_LINE_DASH: list[int] = []
SECONDARY_COMPONENT_LINE_DASH: list[int] = [6, 5]


def round_number(value: float, digits: int = 6) -> float | None:
    value = float(value)
    if not math.isfinite(value):
        return None
    rounded = round(value, digits)
    return 0.0 if rounded == -0.0 else rounded


def rounded_vector(vector: np.ndarray, digits: int = 6) -> list[float | None]:
    return [round_number(component, digits) for component in vector]


def compress_brotli(data: bytes) -> bytes | None:
    for module_name in ("brotli", "brotlicffi"):
        try:
            brotli = __import__(module_name)
        except ImportError:
            continue
        return brotli.compress(data, quality=11)
    return None


def equatorial_from_galactic(vector: np.ndarray) -> np.ndarray:
    return EQ_TO_GAL.T @ vector


def ra_dec_from_equatorial(vector: np.ndarray) -> tuple[float, float]:
    radius = float(np.linalg.norm(vector))
    if radius <= 0:
        return 0.0, 0.0
    x, y, z = vector / radius
    return math.atan2(y, x), math.asin(max(-1.0, min(1.0, z)))


def make_basis(origin: np.ndarray) -> dict[str, np.ndarray]:
    radial = origin / np.linalg.norm(origin)
    ra, dec = ra_dec_from_equatorial(equatorial_from_galactic(radial))
    east_eq = np.array([-math.sin(ra), math.cos(ra), 0.0])
    north_eq = np.array(
        [
            -math.sin(dec) * math.cos(ra),
            -math.sin(dec) * math.sin(ra),
            math.cos(dec),
        ]
    )
    east = EQ_TO_GAL @ east_eq
    north = EQ_TO_GAL @ north_eq
    angle = math.radians(DEFAULT_VIEW_AXIS_ROTATION_DEGREES)
    axis_cos = math.cos(angle)
    axis_sin = math.sin(angle)
    return {
        "east": east * axis_cos - north * axis_sin,
        "north": east * axis_sin + north * axis_cos,
        "radial": radial,
    }


def vector_from_local(local: np.ndarray, origin: np.ndarray, basis: dict[str, np.ndarray]) -> np.ndarray:
    return origin + basis["east"] * local[0] + basis["north"] * local[1] + basis["radial"] * local[2]


def local_from_vector(vector: np.ndarray, origin: np.ndarray, basis: dict[str, np.ndarray]) -> np.ndarray:
    delta = vector - origin
    return np.array([float(delta @ basis["east"]), float(delta @ basis["north"]), float(delta @ basis["radial"])])


def finite_row(row: list[object], indexes: dict[str, int]) -> bool:
    names = ("distanceKpc", "galLonDeg", "galLatDeg", "distanceErrorKpc", "x", "y", "z")
    values = [row[indexes[name]] for name in names]
    return (
        all(isinstance(value, (int, float)) and math.isfinite(value) for value in values)
        and row[indexes["distanceKpc"]] > 0
        and row[indexes["distanceErrorKpc"]] > 0
    )


def subset_arrays(payload: dict[str, object], indexes: dict[str, int], population_id: str, cloud_id: str) -> dict[str, object]:
    population = POPULATIONS[population_id]
    cloud = CLOUDS[cloud_id]
    rows = [
        row
        for row in payload["datasets"]["catalog"]  # type: ignore[index]
        if row[indexes["datasetIndex"]] == population["dataset"]
        and row[indexes["locationIndex"]] == cloud["location"]
        and finite_row(row, indexes)
    ]
    distance = np.asarray([row[indexes["distanceKpc"]] for row in rows], dtype=float)
    lon = np.asarray([row[indexes["galLonDeg"]] for row in rows], dtype=float)
    lat = np.asarray([row[indexes["galLatDeg"]] for row in rows], dtype=float)
    sigma = np.asarray([row[indexes["distanceErrorKpc"]] for row in rows], dtype=float)
    position = galactic_vector(lon, lat, distance)
    unit = position / np.linalg.norm(position, axis=1)[:, None]
    measurement = sigma[:, None, None] ** 2 * unit[:, :, None] * unit[:, None, :]
    local = np.asarray([[row[indexes["x"]], row[indexes["y"]], row[indexes["z"]]] for row in rows], dtype=float)
    ids = [row[indexes["id"]] for row in rows]
    return {
        "rows": rows,
        "position": position,
        "measurement": measurement,
        "local": local,
        "sigma": sigma,
        "ids": ids,
    }


def ellipsoid_payload(
    population_id: str,
    cloud_id: str,
    center: np.ndarray,
    covariance: np.ndarray,
    count: int,
    *,
    label: str,
    alpha: float = 0.82,
    line_width: float = 1.15,
    line_dash: list[int] | None = None,
    extra: dict[str, object] | None = None,
) -> dict[str, object]:
    values, vectors = np.linalg.eigh(positive_semidefinite(covariance))
    order = np.argsort(values)[::-1]
    values = np.maximum(values[order], EIGEN_FLOOR)
    vectors = vectors[:, order]
    axes = []
    for index in range(3):
        axis = vectors[:, index]
        pivot = int(np.argmax(np.abs(axis)))
        if axis[pivot] < 0:
            axis = -axis
        axes.append(axis)
    population = POPULATIONS[population_id]
    cloud = CLOUDS[cloud_id]
    item: dict[str, object] = {
        "type": "ellipsoid",
        "id": f"{population_id}-{cloud_id}-{label.lower().replace(' ', '-')}",
        "label": label,
        "populationId": population_id,
        "cloudId": cloud_id,
        "count": count,
        "color": population["color"],
        "lineDash": list(MAIN_COMPONENT_LINE_DASH if line_dash is None else line_dash),
        "alpha": alpha,
        "lineWidth": line_width,
        "centerVector": rounded_vector(center),
        "axes": [rounded_vector(axis) for axis in axes],
        "axesKpc": [round_number(math.sqrt(float(value)) * CONFIDENCE_RADIUS, 3) for value in values],
        "axisSigmaKpc": [round_number(math.sqrt(float(value)), 3) for value in values],
    }
    if extra:
        item.update(extra)
    return item


def plane_z(coefficients: np.ndarray, x: float, y: float, model: str) -> float:
    if model == "tilted-plane":
        return float(coefficients[0] + coefficients[1] * x + coefficients[2] * y)
    x_norm = x
    y_norm = y
    return float(
        coefficients[0]
        + coefficients[1] * x
        + coefficients[2] * y
        + coefficients[3] * x_norm * x_norm
        + coefficients[4] * x_norm * y_norm
        + coefficients[5] * y_norm * y_norm
    )


def surface_design_matrix(xy: np.ndarray, model: str) -> np.ndarray:
    x = xy[:, 0]
    y = xy[:, 1]
    if model == "tilted-plane":
        return np.column_stack([np.ones(len(xy)), x, y])
    if model == "quadratic-warp":
        return np.column_stack([np.ones(len(xy)), x, y, x * x, x * y, y * y])
    raise ValueError(model)


def fit_surface_params_weighted(
    xyz_local: np.ndarray,
    sigma_z: np.ndarray,
    model: str,
    sample_weights: np.ndarray,
) -> tuple[np.ndarray, float]:
    xy = xyz_local[:, :2]
    z = xyz_local[:, 2]
    design = surface_design_matrix(xy, model)
    sample_weights = np.maximum(np.asarray(sample_weights, dtype=float), 0)
    if not np.any(sample_weights > 0):
        sample_weights = np.ones(len(xyz_local), dtype=float)
    scatter2 = max(0.01, float(np.average((z - np.average(z, weights=sample_weights)) ** 2, weights=sample_weights) - np.median(sigma_z) ** 2))
    coefficients = np.zeros(design.shape[1])
    for _iteration in range(30):
        variance = np.maximum(sigma_z**2 + scatter2, 1e-6)
        weights = sample_weights / variance
        sqrt_weights = np.sqrt(np.maximum(weights, 1e-12))
        weighted_design = design * sqrt_weights[:, None]
        weighted_z = z * sqrt_weights
        coefficients = np.linalg.lstsq(weighted_design, weighted_z, rcond=None)[0]
        residual = z - design @ coefficients
        next_scatter2 = max(0.01, float(np.average(residual**2, weights=weights) - np.average(sigma_z**2, weights=weights)))
        if abs(next_scatter2 - scatter2) < 1e-5:
            scatter2 = next_scatter2
            break
        scatter2 = 0.6 * scatter2 + 0.4 * next_scatter2
    return coefficients, scatter2


def line_segment_vectors(
    start: tuple[float, float],
    end: tuple[float, float],
    coefficients: np.ndarray,
    model: str,
    local_mean: np.ndarray,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
    samples: int = 2,
) -> list[list[float | None]]:
    vectors = []
    for index in range(samples):
        fraction = index / max(1, samples - 1)
        x = start[0] + (end[0] - start[0]) * fraction
        y = start[1] + (end[1] - start[1]) * fraction
        local = local_mean + np.array([x, y, plane_z(coefficients, x, y, model)])
        vectors.append(rounded_vector(vector_from_local(local, origin, basis)))
    return vectors


def kde_density_grid(
    x: np.ndarray,
    y: np.ndarray,
    grid_size: int = CONTOUR_GRID_SIZE,
    weights: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if weights is None:
        weights = np.ones(len(x), dtype=float)
    weights = np.maximum(np.asarray(weights, dtype=float), 0)
    if not np.any(weights > 0):
        weights = np.ones(len(x), dtype=float)
    x_min = weighted_quantile(x, weights, PLANE_QUANTILE_RANGE[0])
    x_max = weighted_quantile(x, weights, PLANE_QUANTILE_RANGE[1])
    y_min = weighted_quantile(y, weights, PLANE_QUANTILE_RANGE[0])
    y_max = weighted_quantile(y, weights, PLANE_QUANTILE_RANGE[1])
    x_pad = max(0.25, (x_max - x_min) * 0.08)
    y_pad = max(0.25, (y_max - y_min) * 0.08)
    xs = np.linspace(x_min - x_pad, x_max + x_pad, grid_size)
    ys = np.linspace(y_min - y_pad, y_max + y_pad, grid_size)
    _mean, std = weighted_mean_and_std(np.column_stack([x, y]), weights)
    x_std = float(std[0]) or 1.0
    y_std = float(std[1]) or 1.0
    factor = max(8.0, effective_weight_count(weights)) ** (-1 / 6)
    hx = max(0.22, 0.72 * x_std * factor)
    hy = max(0.22, 0.72 * y_std * factor)
    density = np.zeros((len(ys), len(xs)), dtype=float)
    xx = xs[None, :]
    for start in range(0, len(y), 256):
        stop = min(len(y), start + 256)
        dx2 = ((xx - x[start:stop, None]) / hx) ** 2
        chunk_weights = weights[start:stop]
        for y_index, y_value in enumerate(ys):
            dy2 = ((y_value - y[start:stop]) / hy) ** 2
            density[y_index] += (np.exp(-0.5 * (dx2 + dy2[:, None])) * chunk_weights[:, None]).sum(axis=0)
    density /= max(float(np.sum(weights)), 1e-12) * 2 * math.pi * hx * hy
    return xs, ys, density


def density_level_for_mass(xs: np.ndarray, ys: np.ndarray, density: np.ndarray, enclosed_mass: float) -> float:
    cell_area = float((xs[1] - xs[0]) * (ys[1] - ys[0])) if len(xs) > 1 and len(ys) > 1 else 1.0
    flat = np.sort(density.ravel())[::-1]
    cumulative = np.cumsum(flat * cell_area)
    if cumulative[-1] <= 0:
        return float(np.max(density))
    target = enclosed_mass * cumulative[-1]
    index = int(np.searchsorted(cumulative, target, side="left"))
    return float(flat[min(index, len(flat) - 1)])


def interpolate_edge(
    p0: tuple[float, float],
    p1: tuple[float, float],
    v0: float,
    v1: float,
    level: float,
) -> tuple[float, float]:
    if v0 == v1:
        fraction = 0.5
    else:
        fraction = (level - v0) / (v1 - v0)
    fraction = max(0.0, min(1.0, fraction))
    return (p0[0] + (p1[0] - p0[0]) * fraction, p0[1] + (p1[1] - p0[1]) * fraction)


def marching_squares_segments(xs: np.ndarray, ys: np.ndarray, density: np.ndarray, level: float) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
    for y_index in range(len(ys) - 1):
        for x_index in range(len(xs) - 1):
            bl = float(density[y_index, x_index])
            br = float(density[y_index, x_index + 1])
            tr = float(density[y_index + 1, x_index + 1])
            tl = float(density[y_index + 1, x_index])
            points = [
                (xs[x_index], ys[y_index]),
                (xs[x_index + 1], ys[y_index]),
                (xs[x_index + 1], ys[y_index + 1]),
                (xs[x_index], ys[y_index + 1]),
            ]
            values = [bl, br, tr, tl]
            crossings = []
            for edge_index, (first, second) in enumerate(((0, 1), (1, 2), (2, 3), (3, 0))):
                if (values[first] >= level) == (values[second] >= level):
                    continue
                crossings.append(interpolate_edge(points[first], points[second], values[first], values[second], level))
            if len(crossings) == 2:
                segments.append((crossings[0], crossings[1]))
            elif len(crossings) == 4:
                segments.append((crossings[0], crossings[1]))
                segments.append((crossings[2], crossings[3]))
    return segments


def build_density_contours(
    payload: dict[str, object],
    indexes: dict[str, int],
    population_id: str,
    cloud_id: str,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> dict[str, object]:
    arrays = subset_arrays(payload, indexes, population_id, cloud_id)
    local = arrays["local"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    local_mean = local.mean(axis=0)
    centered = local - local_mean
    coefficients, scatter2 = fit_surface_params(centered, sigma, "tilted-plane")
    xs, ys, density = kde_density_grid(centered[:, 0], centered[:, 1])
    segments = []
    for level_index, enclosed_mass in enumerate(CONTOUR_LEVELS):
        level = density_level_for_mass(xs, ys, density, enclosed_mass)
        samples = 2 if level_index else 3
        for start, end in marching_squares_segments(xs, ys, density, level):
            segments.append(
                line_segment_vectors(
                    start,
                    end,
                    coefficients,
                    "tilted-plane",
                    local_mean,
                    origin,
                    basis,
                    samples=samples,
                )
            )
    x_label = float(np.quantile(centered[:, 0], 0.72))
    y_label = float(np.quantile(centered[:, 1], 0.72))
    label_local = local_mean + np.array([x_label, y_label, plane_z(coefficients, x_label, y_label, "tilted-plane")])
    population = POPULATIONS[population_id]
    cloud = CLOUDS[cloud_id]
    return {
        "type": "contours",
        "id": f"{population_id}-{cloud_id}-density-contours",
        "label": f"{population['label']} {cloud['label']} density",
        "populationId": population_id,
        "cloudId": cloud_id,
        "count": len(arrays["rows"]),  # type: ignore[arg-type]
        "color": population["color"],
        "lineDash": cloud["lineDash"],
        "alpha": 0.76,
        "lineWidth": 1.05,
        "structureModel": "tilted-plane-kde-density-contours",
        "intrinsicScatterKpc": round_number(math.sqrt(float(scatter2)), 3),
        "contourMassFractions": [round_number(value, 2) for value in CONTOUR_LEVELS],
        "segments": segments,
        "labelVector": rounded_vector(vector_from_local(label_local, origin, basis)),
    }


def point_in_polygon(x: float, y: float, polygon: tuple[tuple[float, float], ...]) -> bool:
    inside = False
    previous = len(polygon) - 1
    for index, (xi, yi) in enumerate(polygon):
        xj, yj = polygon[previous]
        if ((yi > y) != (yj > y)) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        previous = index
    return inside


def mode_counts(rows: list[object], indexes: dict[str, int]) -> dict[str, int]:
    counts: dict[str, int] = {}
    mode_index = indexes.get("mode")
    if mode_index is None:
        return counts
    for row in rows:
        if not isinstance(row, list) or mode_index >= len(row):
            continue
        mode = str(row[mode_index])
        counts[mode] = counts.get(mode, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def lmc_cepheid_ripepi_bar_mask(rows: list[object], indexes: dict[str, int]) -> np.ndarray:
    ra_index = indexes["raDeg"]
    dec_index = indexes["decDeg"]
    mask = []
    for row in rows:
        if not isinstance(row, list):
            mask.append(False)
            continue
        mask.append(
            point_in_polygon(
                float(row[ra_index]),
                float(row[dec_index]),
                LMC_CEPHEID_RIPEPI_BAR_POLYGON_RA_DEC,
            )
        )
    return np.asarray(mask, dtype=bool)


def angular_delta_deg(value: float, reference: float) -> float:
    return (float(value) - float(reference) + 180.0) % 360.0 - 180.0


def sky_seed_mask(
    rows: list[object],
    indexes: dict[str, int],
    seed_ra_deg: float,
    seed_dec_deg: float,
    radius_ra_deg: float,
    radius_dec_deg: float,
    min_count: int = 12,
) -> tuple[np.ndarray, float]:
    ra_index = indexes["raDeg"]
    dec_index = indexes["decDeg"]
    ra_delta = np.asarray([angular_delta_deg(float(row[ra_index]), seed_ra_deg) for row in rows], dtype=float)
    dec = np.asarray([float(row[dec_index]) for row in rows], dtype=float)
    cos_dec = math.cos(math.radians(seed_dec_deg))
    for expansion in (1.0, 1.2, 1.5, 2.0):
        dx = ra_delta * cos_dec / (radius_ra_deg * expansion)
        dy = (dec - seed_dec_deg) / (radius_dec_deg * expansion)
        mask = (dx * dx + dy * dy) <= 1.0
        if int(mask.sum()) >= min_count:
            return mask, expansion
    return mask, 2.0


def feature_label_payload(
    rows: list[object],
    positions: np.ndarray,
    indexes: dict[str, int],
    mask: np.ndarray,
    spec: dict[str, object],
    selection_note: str,
    selection_region: str,
    *,
    population_id: str = "cepheids",
    cloud_id: str = "lmc",
    source_model: str = "literature feature label + atlas median anchor",
) -> dict[str, object] | None:
    if int(mask.sum()) <= 0:
        return None
    selected_rows = [row for row, selected in zip(rows, mask) if selected]
    selected_positions = positions[mask]
    ra_values = np.asarray([row[indexes["raDeg"]] for row in selected_rows], dtype=float)
    dec_values = np.asarray([row[indexes["decDeg"]] for row in selected_rows], dtype=float)
    distance_values = np.asarray([row[indexes["distanceKpc"]] for row in selected_rows], dtype=float)
    distance_error_values = np.asarray([row[indexes["distanceErrorKpc"]] for row in selected_rows], dtype=float)
    feature_scale = str(spec.get("featureScale", "minor"))
    return {
        "type": "featureLabel",
        "id": str(spec["id"]),
        "label": str(spec["label"]),
        "populationId": population_id,
        "cloudId": cloud_id,
        "count": int(mask.sum()),
        "color": POPULATIONS[population_id]["color"],
        "alpha": 0.98 if feature_scale == "major" else 0.92,
        "fontSizePx": int(spec.get("fontSizePx", 11)),
        "fontWeight": 800 if feature_scale == "major" else 700,
        "featureScale": feature_scale,
        "componentRole": "feature-label",
        "structureModel": "literature-feature-label",
        "sourceModel": source_model,
        "selectionRegion": selection_region,
        "selectionNote": selection_note,
        "labelVector": rounded_vector(np.median(selected_positions, axis=0)),
        "raDeg": round_number(float(np.median(ra_values)), 4),
        "decDeg": round_number(float(np.median(dec_values)), 4),
        "distanceKpc": round_number(float(np.median(distance_values)), 3),
        "medianDistanceErrorKpc": round_number(float(np.median(distance_error_values)), 3),
        "modeCounts": mode_counts(selected_rows, indexes),
    }


def build_lmc_cepheid_ripepi_feature_labels(
    payload: dict[str, object],
    indexes: dict[str, int],
) -> list[dict[str, object]]:
    arrays = subset_arrays(payload, indexes, "cepheids", "lmc")
    rows = arrays["rows"]  # type: ignore[assignment]
    positions = arrays["position"]  # type: ignore[assignment]
    bar_mask = lmc_cepheid_ripepi_bar_mask(rows, indexes)
    center_ra, _center_dec = LMC_CEPHEID_RIPEPI_CENTER_RA_DEC
    ra_index = indexes["raDeg"]
    ra_values = np.asarray([float(row[ra_index]) for row in rows], dtype=float)
    structures: list[dict[str, object]] = []
    for spec in LMC_CEPHEID_RIPEPI_FEATURES:
        selection = spec.get("selection")
        if selection == "ripepi-bar-east":
            mask = bar_mask & (ra_values > center_ra)
            selection_region = "inside Ripepi VMC bar polygon, east of the adopted LMC centre"
            selection_note = (
                "The eastern-bar label is anchored to the median of atlas LMC Cepheids "
                "inside the Ripepi bar polygon with RA greater than the adopted centre."
            )
        elif selection == "ripepi-bar-west":
            mask = bar_mask & (ra_values <= center_ra)
            selection_region = "inside Ripepi VMC bar polygon, west of the adopted LMC centre"
            selection_note = (
                "The western-bar label is anchored to the median of atlas LMC Cepheids "
                "inside the Ripepi bar polygon with RA less than or equal to the adopted centre."
            )
        elif selection == "multi-sky-seed":
            masks = []
            seed_summaries = []
            for seed in spec["seeds"]:
                seed_ra = float(seed["raDeg"])
                seed_dec = float(seed["decDeg"])
                radius_ra = float(seed["radiusRaDeg"])
                radius_dec = float(seed["radiusDecDeg"])
                seed_mask, expansion = sky_seed_mask(rows, indexes, seed_ra, seed_dec, radius_ra, radius_dec)
                masks.append(seed_mask)
                seed_summaries.append(
                    f"RA={seed_ra:.2f} deg, Dec={seed_dec:.2f} deg; "
                    f"elliptical radius {radius_ra * expansion:.2f} x {radius_dec * expansion:.2f} deg"
                )
            mask = np.logical_or.reduce(masks)
            selection_region = "near Ripepi Fig. 13 seeds " + "; ".join(seed_summaries)
            selection_note = (
                "The label is anchored to the median 3D position of atlas LMC Cepheids near "
                "the merged northern-arm sky locations inferred from the Ripepi substructure map and text."
            )
        else:
            seed_ra = float(spec["seedRaDeg"])
            seed_dec = float(spec["seedDecDeg"])
            radius_ra = float(spec["radiusRaDeg"])
            radius_dec = float(spec["radiusDecDeg"])
            mask, expansion = sky_seed_mask(rows, indexes, seed_ra, seed_dec, radius_ra, radius_dec)
            selection_region = (
                f"near Ripepi Fig. 13 seed RA={seed_ra:.2f} deg, Dec={seed_dec:.2f} deg; "
                f"elliptical radius {radius_ra * expansion:.2f} x {radius_dec * expansion:.2f} deg"
            )
            selection_note = (
                "The label is anchored to the median 3D position of atlas LMC Cepheids near "
                "the sky location inferred from the Ripepi substructure map and text."
            )
        label = feature_label_payload(
            rows,
            positions,
            indexes,
            mask,
            spec,
            selection_note,
            selection_region,
            population_id="cepheids",
            cloud_id="lmc",
            source_model="Ripepi et al. 2022 LMC Cepheid substructure label + atlas Cepheid median anchor",
        )
        if label is not None:
            structures.append(label)
    return structures


def smc_ra_offsets(rows: list[object], indexes: dict[str, int]) -> np.ndarray:
    center_ra, _center_dec = SMC_CEPHEID_CENTER_RA_DEC
    ra_index = indexes["raDeg"]
    return np.asarray([angular_delta_deg(float(row[ra_index]), center_ra) for row in rows], dtype=float)


def build_smc_cepheid_literature_feature_labels(
    payload: dict[str, object],
    indexes: dict[str, int],
) -> list[dict[str, object]]:
    arrays = subset_arrays(payload, indexes, "cepheids", "smc")
    rows = arrays["rows"]  # type: ignore[assignment]
    positions = arrays["position"]  # type: ignore[assignment]
    ra_offset = smc_ra_offsets(rows, indexes)
    dec = np.asarray([float(row[indexes["decDeg"]]) for row in rows], dtype=float)
    distance = np.asarray([float(row[indexes["distanceKpc"]]) for row in rows], dtype=float)
    structures: list[dict[str, object]] = []
    for spec in SMC_CEPHEID_LITERATURE_FEATURES:
        selection = spec.get("selection")
        if selection == "sky-seed":
            seed_ra = float(spec["seedRaDeg"])
            seed_dec = float(spec["seedDecDeg"])
            radius_ra = float(spec["radiusRaDeg"])
            radius_dec = float(spec["radiusDecDeg"])
            mask, expansion = sky_seed_mask(rows, indexes, seed_ra, seed_dec, radius_ra, radius_dec)
            selection_region = (
                f"near literature sky seed RA={seed_ra:.2f} deg, Dec={seed_dec:.2f} deg; "
                f"elliptical radius {radius_ra * expansion:.2f} x {radius_dec * expansion:.2f} deg"
            )
            selection_note = (
                "The label is anchored to the median 3D position of atlas SMC Cepheids "
                "near the literature sky location."
            )
        elif selection == "eastern-foreground":
            mask = (ra_offset > 2.5) & (distance < 60.0)
            selection_region = "east of the SMC centre and closer than 60 kpc"
            selection_note = (
                "Ripepi et al. describe the <60 kpc Cepheids as strongly off-centred "
                "towards the E/NE direction; this label uses atlas SMC Cepheids matching that depth and side."
            )
        elif selection == "north-eastern-structure":
            mask = (ra_offset > 1.5) & (dec > -73.3) & (dec < -71.5) & (distance >= 60.0) & (distance <= 65.0)
            selection_region = "north-east of the SMC centre, 60-65 kpc"
            selection_note = (
                "Ripepi et al. note NE substructures among young Cepheids between about 60 and 65 kpc; "
                "this label anchors that Bridge-side structure in the atlas data."
            )
        elif selection == "south-western-distant-structure":
            mask = (ra_offset < -1.0) & (dec < -73.2) & (distance > 65.0)
            selection_region = "south-west of the SMC centre and farther than 65 kpc"
            selection_note = (
                "Ripepi et al. describe an old-Cepheid SW structure extending to large distances; "
                "this label anchors the matching far south-western atlas Cepheids."
            )
        elif selection == "counter-bridge":
            mask = (ra_offset < -2.0) & (distance > 70.0)
            selection_region = "west of the SMC centre and farther than 70 kpc"
            selection_note = (
                "The Counter-Bridge label follows literature terminology, while its exact stellar counterpart "
                "remains model-dependent and low-density."
            )
        else:
            continue
        label = feature_label_payload(
            rows,
            positions,
            indexes,
            mask,
            spec,
            selection_note,
            selection_region,
            population_id="cepheids",
            cloud_id="smc",
            source_model="Ripepi et al. 2017 / Deb et al. 2019 / Tatton et al. 2021 SMC substructure label + atlas Cepheid median anchor",
        )
        if label is not None:
            structures.append(label)
    return structures


def sheet_point(
    local_mean: np.ndarray,
    coefficients: np.ndarray,
    x: float,
    y: float,
    model: str,
    normal: np.ndarray,
    height_offset: float,
) -> np.ndarray:
    z = plane_z(coefficients, x, y, model)
    return local_mean + np.array([x, y, z]) + normal * height_offset


def sheet_segment_vectors(
    start: tuple[float, float],
    end: tuple[float, float],
    coefficients: np.ndarray,
    model: str,
    local_mean: np.ndarray,
    normal: np.ndarray,
    height_offset: float,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
    samples: int = 2,
) -> list[list[float | None]]:
    vectors = []
    for index in range(samples):
        fraction = index / max(1, samples - 1)
        x = start[0] + (end[0] - start[0]) * fraction
        y = start[1] + (end[1] - start[1]) * fraction
        vectors.append(rounded_vector(vector_from_local(sheet_point(local_mean, coefficients, x, y, model, normal, height_offset), origin, basis)))
    return vectors


def build_thick_sheet_density_contours(
    local: np.ndarray,
    sigma_z: np.ndarray,
    rows: list[object],
    indexes: dict[str, int],
    population_id: str,
    cloud_id: str,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
    *,
    label: str,
    structure_model: str,
    component_role: str,
    line_dash: list[int],
    alpha: float,
    density_weights: np.ndarray | None = None,
    local_mean: np.ndarray | None = None,
    surface_model: str = "tilted-plane",
    surface_coefficients: np.ndarray | None = None,
    surface_scatter2: float | None = None,
    count_override: int | None = None,
    extra_metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    if density_weights is None:
        density_weights = np.ones(len(local), dtype=float)
    density_weights = np.maximum(np.asarray(density_weights, dtype=float), 0)
    if not np.any(density_weights > 0):
        density_weights = np.ones(len(local), dtype=float)
    if local_mean is None:
        local_mean = (local * density_weights[:, None]).sum(axis=0) / max(float(np.sum(density_weights)), 1e-12)
    centered = local - local_mean
    if surface_coefficients is None or surface_scatter2 is None:
        coefficients, scatter2 = fit_surface_params_weighted(centered, sigma_z, surface_model, density_weights)
    else:
        coefficients = np.asarray(surface_coefficients, dtype=float)
        scatter2 = float(surface_scatter2)
    thickness = math.sqrt(float(scatter2))
    normal = np.array([-coefficients[1], -coefficients[2], 1.0], dtype=float)
    normal /= max(float(np.linalg.norm(normal)), 1e-12)
    xs, ys, density = kde_density_grid(centered[:, 0], centered[:, 1], weights=density_weights)
    segments = []
    connector_stride = 28
    segment_index = 0
    for level_index, enclosed_mass in enumerate(LMC_CEPHEID_RIPEPI_CONTOUR_LEVELS):
        level = density_level_for_mass(xs, ys, density, enclosed_mass)
        samples = 3 if level_index == 0 else 2
        for start, end in marching_squares_segments(xs, ys, density, level):
            for height_offset in (-thickness, thickness):
                segments.append(
                    sheet_segment_vectors(
                        start,
                        end,
                        coefficients,
                        surface_model,
                        local_mean,
                        normal,
                        height_offset,
                        origin,
                        basis,
                        samples=samples,
                    )
                )
            if segment_index % connector_stride == 0:
                for point in (start, end):
                    segments.append(
                        [
                            rounded_vector(vector_from_local(sheet_point(local_mean, coefficients, point[0], point[1], surface_model, normal, -thickness), origin, basis)),
                            rounded_vector(vector_from_local(sheet_point(local_mean, coefficients, point[0], point[1], surface_model, normal, thickness), origin, basis)),
                        ]
                    )
            segment_index += 1

    x_label = weighted_quantile(centered[:, 0], density_weights, 0.74)
    y_label = weighted_quantile(centered[:, 1], density_weights, 0.70)
    label_local = sheet_point(local_mean, coefficients, x_label, y_label, surface_model, normal, thickness)
    population = POPULATIONS[population_id]
    item = {
        "type": "contours",
        "id": f"{population_id}-{cloud_id}-{label.lower().replace(' ', '-')}",
        "label": label,
        "populationId": population_id,
        "cloudId": cloud_id,
        "count": int(count_override if count_override is not None else len(rows)),
        "color": population["color"],
        "lineDash": line_dash,
        "alpha": alpha,
        "lineWidth": 1.06,
        "componentRole": component_role,
        "structureModel": structure_model,
        "sourceModel": f"{surface_model}-kde-density-contours",
        "contourMassFractions": [round_number(value, 2) for value in LMC_CEPHEID_RIPEPI_CONTOUR_LEVELS],
        "intrinsicScatterKpc": round_number(thickness, 3),
        "planeCoefficientsLocal": [round_number(value, 6) for value in coefficients],
        "modeCounts": mode_counts(rows, indexes),
        "segments": segments,
        "labelVector": rounded_vector(vector_from_local(label_local, origin, basis)),
    }
    if extra_metadata:
        item.update(extra_metadata)
    return item


def gaussian_mixture_density_grid_2d(
    means: np.ndarray,
    covariances: np.ndarray,
    weights: np.ndarray,
    xs: np.ndarray,
    ys: np.ndarray,
) -> np.ndarray:
    xx = xs[None, :]
    yy = ys[:, None]
    density = np.zeros((len(ys), len(xs)), dtype=float)
    weights = np.maximum(np.asarray(weights, dtype=float), 0)
    weights = weights / max(float(np.sum(weights)), 1e-12)
    for mean, covariance, weight in zip(means, covariances, weights):
        if weight <= 0:
            continue
        covariance = positive_semidefinite_2d(np.asarray(covariance, dtype=float), 1e-5)
        det = max(float(np.linalg.det(covariance)), 1e-12)
        inverse = np.linalg.inv(covariance)
        dx = xx - float(mean[0])
        dy = yy - float(mean[1])
        quadratic = inverse[0, 0] * dx * dx + 2 * inverse[0, 1] * dx * dy + inverse[1, 1] * dy * dy
        density += weight * np.exp(-0.5 * quadratic) / (2 * math.pi * math.sqrt(det))
    return density


def plane_normal_from_coefficients(coefficients: np.ndarray, model: str, x: float = 0.0, y: float = 0.0) -> np.ndarray:
    coefficients = np.asarray(coefficients, dtype=float)
    dz_dx = float(coefficients[1]) if len(coefficients) > 1 else 0.0
    dz_dy = float(coefficients[2]) if len(coefficients) > 2 else 0.0
    if model == "quadratic-warp" and len(coefficients) >= 6:
        dz_dx += 2 * float(coefficients[3]) * x + float(coefficients[5]) * y
        dz_dy += 2 * float(coefficients[4]) * y + float(coefficients[5]) * x
    normal = np.array([-dz_dx, -dz_dy, 1.0], dtype=float)
    normal /= max(float(np.linalg.norm(normal)), 1e-12)
    return normal


def build_fitted_disk_density_contours(
    local: np.ndarray,
    sigma_z: np.ndarray,
    rows: list[object],
    indexes: dict[str, int],
    population_id: str,
    cloud_id: str,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
    *,
    label: str,
    structure_model: str,
    component_role: str,
    line_dash: list[int],
    alpha: float,
    density_weights: np.ndarray,
    local_mean: np.ndarray,
    surface_model: str,
    surface_coefficients: np.ndarray,
    surface_scatter2: float,
    inplane_weights: np.ndarray,
    inplane_means: np.ndarray,
    inplane_covariances: np.ndarray,
    count_override: int | None = None,
    extra_metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    density_weights = np.maximum(np.asarray(density_weights, dtype=float), 0)
    if not np.any(density_weights > 0):
        density_weights = np.ones(len(local), dtype=float)
    local_mean = np.asarray(local_mean, dtype=float)
    coefficients = np.asarray(surface_coefficients, dtype=float)
    centered = local - local_mean
    thickness = math.sqrt(float(surface_scatter2))

    x_min = weighted_quantile(centered[:, 0], density_weights, PLANE_QUANTILE_RANGE[0])
    x_max = weighted_quantile(centered[:, 0], density_weights, PLANE_QUANTILE_RANGE[1])
    y_min = weighted_quantile(centered[:, 1], density_weights, PLANE_QUANTILE_RANGE[0])
    y_max = weighted_quantile(centered[:, 1], density_weights, PLANE_QUANTILE_RANGE[1])
    x_pad = max(0.35, (x_max - x_min) * 0.10)
    y_pad = max(0.35, (y_max - y_min) * 0.10)
    xs = np.linspace(x_min - x_pad, x_max + x_pad, LMC_CEPHEID_DISK_DENSITY_GRID_SIZE)
    ys = np.linspace(y_min - y_pad, y_max + y_pad, LMC_CEPHEID_DISK_DENSITY_GRID_SIZE)
    density = gaussian_mixture_density_grid_2d(
        np.asarray(inplane_means, dtype=float),
        np.asarray(inplane_covariances, dtype=float),
        np.asarray(inplane_weights, dtype=float),
        xs,
        ys,
    )

    normal = plane_normal_from_coefficients(coefficients, surface_model)
    midplane_segments: list[list[list[float | None]]] = []
    thickness_segments: list[list[list[float | None]]] = []
    outer_segments_2d: list[tuple[tuple[float, float], tuple[float, float]]] = []

    for level_index, enclosed_mass in enumerate(LMC_CEPHEID_DISK_CONTOUR_LEVELS):
        level = density_level_for_mass(xs, ys, density, enclosed_mass)
        contour_segments = marching_squares_segments(xs, ys, density, level)
        if level_index == len(LMC_CEPHEID_DISK_CONTOUR_LEVELS) - 1:
            outer_segments_2d = contour_segments
        samples = 3 if level_index == 0 else 2
        for start, end in contour_segments:
            midplane_segments.append(
                sheet_segment_vectors(
                    start,
                    end,
                    coefficients,
                    surface_model,
                    local_mean,
                    normal,
                    0.0,
                    origin,
                    basis,
                    samples=samples,
                )
            )

    if outer_segments_2d:
        stride = max(1, len(outer_segments_2d) // LMC_CEPHEID_DISK_THICKNESS_TICKS)
        for start, end in outer_segments_2d[::stride][:LMC_CEPHEID_DISK_THICKNESS_TICKS]:
            x = (start[0] + end[0]) * 0.5
            y = (start[1] + end[1]) * 0.5
            tick_normal = plane_normal_from_coefficients(coefficients, surface_model, x, y)
            thickness_segments.append(
                [
                    rounded_vector(vector_from_local(sheet_point(local_mean, coefficients, x, y, surface_model, tick_normal, -thickness), origin, basis)),
                    rounded_vector(vector_from_local(sheet_point(local_mean, coefficients, x, y, surface_model, tick_normal, thickness), origin, basis)),
                ]
            )

    if outer_segments_2d:
        endpoints = np.asarray([point for segment in outer_segments_2d for point in segment], dtype=float)
        label_anchor_xy = endpoints[int(np.argmax(endpoints[:, 1] + 0.18 * endpoints[:, 0]))]
    else:
        label_anchor_xy = np.array([
            weighted_quantile(centered[:, 0], density_weights, 0.72),
            weighted_quantile(centered[:, 1], density_weights, 0.74),
        ])
    label_xy = label_anchor_xy + np.array([0.15, 0.55])
    center_local = sheet_point(local_mean, coefficients, 0.0, 0.0, surface_model, normal, 0.0)
    label_anchor_local = sheet_point(
        local_mean,
        coefficients,
        float(label_anchor_xy[0]),
        float(label_anchor_xy[1]),
        surface_model,
        plane_normal_from_coefficients(coefficients, surface_model, float(label_anchor_xy[0]), float(label_anchor_xy[1])),
        0.0,
    )
    label_local = sheet_point(
        local_mean,
        coefficients,
        float(label_xy[0]),
        float(label_xy[1]),
        surface_model,
        plane_normal_from_coefficients(coefficients, surface_model, float(label_xy[0]), float(label_xy[1])),
        thickness * 0.35,
    )
    segments = midplane_segments + thickness_segments
    population = POPULATIONS[population_id]
    item = {
        "type": "contours",
        "id": f"{population_id}-{cloud_id}-{label.lower().replace(' ', '-')}",
        "label": label,
        "populationId": population_id,
        "cloudId": cloud_id,
        "count": int(count_override if count_override is not None else len(rows)),
        "color": population["color"],
        "lineDash": line_dash,
        "alpha": alpha,
        "hoverAlpha": 0.96,
        "lineWidth": 0.86,
        "hoverLineWidth": 2.05,
        "pickRadiusPx": 9,
        "componentRole": component_role,
        "structureModel": structure_model,
        "sourceModel": f"{surface_model}-analytic-gmm-density-contours",
        "displayModel": "analytic in-plane GMM midplane contours with sparse +/-1 sigma thickness ticks",
        "contourMassFractions": [round_number(value, 2) for value in LMC_CEPHEID_DISK_CONTOUR_LEVELS],
        "intrinsicScatterKpc": round_number(thickness, 3),
        "planeCoefficientsLocal": [round_number(value, 6) for value in coefficients],
        "modeCounts": mode_counts(rows, indexes),
        "segments": segments,
        "segmentGroups": {
            "midplane": midplane_segments,
            "thickness": thickness_segments,
        },
        "targetVector": rounded_vector(vector_from_local(center_local, origin, basis)),
        "labelAnchorVector": rounded_vector(vector_from_local(label_anchor_local, origin, basis)),
        "labelVector": rounded_vector(vector_from_local(label_local, origin, basis)),
    }
    if extra_metadata:
        item.update(extra_metadata)
    return item


def lmc_cepheid_disk_model_moments(disk_params: dict[str, object]) -> tuple[np.ndarray, np.ndarray]:
    local_mean = np.asarray(disk_params["localMean"], dtype=float)
    coefficients = np.asarray(disk_params["coefficients"], dtype=float)
    surface_model = str(disk_params["surfaceModel"])
    inplane_weights = np.maximum(np.asarray(disk_params["inplaneWeights"], dtype=float), 0)
    inplane_weights = inplane_weights / max(float(np.sum(inplane_weights)), 1e-12)
    inplane_means = np.asarray(disk_params["inplaneMeans"], dtype=float)
    inplane_covariances = np.asarray(disk_params["inplaneCovariances"], dtype=float)

    mean_xy = np.sum(inplane_weights[:, None] * inplane_means, axis=0)
    covariance_xy = np.zeros((2, 2), dtype=float)
    for weight, mean, covariance in zip(inplane_weights, inplane_means, inplane_covariances):
        delta = mean - mean_xy
        covariance_xy += weight * (positive_semidefinite_2d(covariance) + np.outer(delta, delta))
    covariance_xy = positive_semidefinite_2d(covariance_xy)

    if surface_model == "quadratic-warp" and len(coefficients) >= 6:
        second_x = covariance_xy[0, 0] + mean_xy[0] * mean_xy[0]
        second_y = covariance_xy[1, 1] + mean_xy[1] * mean_xy[1]
        second_xy = covariance_xy[0, 1] + mean_xy[0] * mean_xy[1]
        z_mean = (
            coefficients[0]
            + coefficients[1] * mean_xy[0]
            + coefficients[2] * mean_xy[1]
            + coefficients[3] * second_x
            + coefficients[4] * second_y
            + coefficients[5] * second_xy
        )
    else:
        z_mean = plane_z(coefficients, float(mean_xy[0]), float(mean_xy[1]), surface_model)

    slope = np.array(
        [
            coefficients[1] + (2 * coefficients[3] * mean_xy[0] + coefficients[5] * mean_xy[1] if surface_model == "quadratic-warp" and len(coefficients) >= 6 else 0),
            coefficients[2] + (2 * coefficients[4] * mean_xy[1] + coefficients[5] * mean_xy[0] if surface_model == "quadratic-warp" and len(coefficients) >= 6 else 0),
        ],
        dtype=float,
    )
    covariance_xz = covariance_xy @ slope
    variance_z = float(slope @ covariance_xy @ slope + float(disk_params["scatter2"]))
    covariance = np.array(
        [
            [covariance_xy[0, 0], covariance_xy[0, 1], covariance_xz[0]],
            [covariance_xy[1, 0], covariance_xy[1, 1], covariance_xz[1]],
            [covariance_xz[0], covariance_xz[1], variance_z],
        ],
        dtype=float,
    )
    mean = local_mean + np.array([mean_xy[0], mean_xy[1], z_mean], dtype=float)
    return mean, positive_semidefinite(covariance)


def effective_weight_count(weights: np.ndarray) -> float:
    total = float(np.sum(weights))
    square_total = float(np.sum(weights * weights))
    return total * total / square_total if square_total > 0 else 0.0


def weighted_mean_and_std(values: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    safe_weights = np.maximum(np.asarray(weights, dtype=float), 0)
    total = float(np.sum(safe_weights))
    if total <= 0:
        return np.mean(values, axis=0), np.std(values, axis=0)
    mean = (values * safe_weights[:, None]).sum(axis=0) / total
    variance = ((values - mean) ** 2 * safe_weights[:, None]).sum(axis=0) / total
    return mean, np.sqrt(np.maximum(variance, 0))


def weighted_quantile(values: np.ndarray, weights: np.ndarray, quantile: float) -> float:
    values = np.asarray(values, dtype=float)
    weights = np.maximum(np.asarray(weights, dtype=float), 0)
    if len(values) == 0:
        return 0.0
    if not np.any(weights > 0):
        return float(np.quantile(values, quantile))
    order = np.argsort(values)
    sorted_values = values[order]
    cumulative = np.cumsum(weights[order])
    target = max(0.0, min(1.0, quantile)) * float(cumulative[-1])
    return float(np.interp(target, cumulative, sorted_values))


def kde_density_volume(
    local: np.ndarray,
    sigma: np.ndarray,
    weights: np.ndarray | None = None,
    bounds_local: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, tuple[float, float, float]]:
    if weights is None:
        weights = np.ones(len(local), dtype=float)
    weights = np.maximum(np.asarray(weights, dtype=float), 0)
    if not np.any(weights > 0):
        weights = np.ones(len(local), dtype=float)
    bounds_source = bounds_local if bounds_local is not None else local
    quantile_min = np.quantile(bounds_source, 0.02, axis=0)
    quantile_max = np.quantile(bounds_source, 0.98, axis=0)
    span = np.maximum(quantile_max - quantile_min, np.array([1.0, 1.0, 1.0]))
    padding = np.maximum(0.35, span * 0.12)
    lower = quantile_min - padding
    upper = quantile_max + padding
    nx, ny, nz = KDE3D_GRID_SHAPE
    xs = np.linspace(lower[0], upper[0], nx)
    ys = np.linspace(lower[1], upper[1], ny)
    zs = np.linspace(lower[2], upper[2], nz)

    _, std = weighted_mean_and_std(local, weights)
    std = np.maximum(std, np.array([0.35, 0.35, 0.35]))
    n_eff = max(8.0, effective_weight_count(weights))
    factor = n_eff ** (-1 / 7)
    hx = max(0.18, 0.72 * float(std[0]) * factor)
    hy = max(0.18, 0.72 * float(std[1]) * factor)
    hz_base = max(0.18, 0.72 * float(std[2]) * factor)
    density = np.zeros((nx, ny, nz), dtype=float)
    norm_xy = 1 / (2 * math.pi * hx * hy)
    for start in range(0, len(local), 192):
        stop = min(len(local), start + 192)
        chunk = local[start:stop]
        chunk_sigma = np.maximum(sigma[start:stop], 0.05)
        chunk_weights = weights[start:stop]
        hz = np.sqrt(hz_base * hz_base + chunk_sigma * chunk_sigma)
        kx = np.exp(-0.5 * ((xs[None, :] - chunk[:, 0, None]) / hx) ** 2)
        ky = np.exp(-0.5 * ((ys[None, :] - chunk[:, 1, None]) / hy) ** 2)
        kz = np.exp(-0.5 * ((zs[None, :] - chunk[:, 2, None]) / hz[:, None]) ** 2) / hz[:, None]
        density += np.einsum("n,nx,ny,nz->xyz", chunk_weights, kx, ky, kz, optimize=True) * norm_xy
    density /= max(float(np.sum(weights)), 1e-12) * math.sqrt(2 * math.pi)
    return xs, ys, zs, density, (hx, hy, hz_base)


def cell_volume(xs: np.ndarray, ys: np.ndarray, zs: np.ndarray) -> float:
    if len(xs) < 2 or len(ys) < 2 or len(zs) < 2:
        return 1.0
    return float((xs[1] - xs[0]) * (ys[1] - ys[0]) * (zs[1] - zs[0]))


def normalized_volume_density(xs: np.ndarray, ys: np.ndarray, zs: np.ndarray, density: np.ndarray) -> np.ndarray:
    total = float(np.sum(density) * cell_volume(xs, ys, zs))
    if total <= 0 or not math.isfinite(total):
        return density
    return density / total


def density_volume_level_for_mass(
    xs: np.ndarray,
    ys: np.ndarray,
    zs: np.ndarray,
    density: np.ndarray,
    enclosed_mass: float,
) -> float:
    volume = cell_volume(xs, ys, zs)
    flat = np.sort(density.ravel())[::-1]
    cumulative = np.cumsum(flat * volume)
    if cumulative[-1] <= 0:
        return float(np.max(density))
    target = enclosed_mass * cumulative[-1]
    index = int(np.searchsorted(cumulative, target, side="left"))
    return float(flat[min(index, len(flat) - 1)])


def nearest_grid_index(values: np.ndarray, value: float) -> int:
    return int(np.argmin(np.abs(values - value)))


def local_slice_segment_vectors(
    start: tuple[float, float],
    end: tuple[float, float],
    mapper,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
    samples: int = 2,
) -> list[list[float | None]]:
    vectors = []
    for index in range(samples):
        fraction = index / max(1, samples - 1)
        first = start[0] + (end[0] - start[0]) * fraction
        second = start[1] + (end[1] - start[1]) * fraction
        vectors.append(rounded_vector(vector_from_local(mapper(first, second), origin, basis)))
    return vectors


def slice_contour_segments(
    horizontal: np.ndarray,
    vertical: np.ndarray,
    slice_density: np.ndarray,
    level: float,
    mapper,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
    samples: int = 2,
) -> list[list[list[float | None]]]:
    return [
        local_slice_segment_vectors(start, end, mapper, origin, basis, samples=samples)
        for start, end in marching_squares_segments(horizontal, vertical, slice_density, level)
    ]


def build_3d_density_contours(
    payload: dict[str, object],
    indexes: dict[str, int],
    population_id: str,
    cloud_id: str,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> dict[str, object]:
    arrays = subset_arrays(payload, indexes, population_id, cloud_id)
    local = arrays["local"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    xs, ys, zs, density, bandwidth = kde_density_volume(local, sigma)
    levels = [density_volume_level_for_mass(xs, ys, zs, density, mass) for mass in KDE3D_CONTAINMENT_LEVELS]
    z_slices = [nearest_grid_index(zs, float(np.quantile(local[:, 2], quantile))) for quantile in KDE3D_DEPTH_QUANTILES]
    x_slices = [nearest_grid_index(xs, float(np.quantile(local[:, 0], 0.5)))]
    y_slices = [nearest_grid_index(ys, float(np.quantile(local[:, 1], 0.5)))]
    segments = []
    for level_index, level in enumerate(levels):
        samples = 3 if level_index == 0 else 2
        for z_index in z_slices:
            z_value = float(zs[z_index])
            segments.extend(
                slice_contour_segments(
                    xs,
                    ys,
                    density[:, :, z_index].T,
                    level,
                    lambda x, y, z_value=z_value: np.array([x, y, z_value]),
                    origin,
                    basis,
                    samples=samples,
                )
            )
        for x_index in x_slices:
            x_value = float(xs[x_index])
            segments.extend(
                slice_contour_segments(
                    ys,
                    zs,
                    density[x_index, :, :].T,
                    level,
                    lambda y, z, x_value=x_value: np.array([x_value, y, z]),
                    origin,
                    basis,
                    samples=samples,
                )
            )
        for y_index in y_slices:
            y_value = float(ys[y_index])
            segments.extend(
                slice_contour_segments(
                    xs,
                    zs,
                    density[:, y_index, :].T,
                    level,
                    lambda x, z, y_value=y_value: np.array([x, y_value, z]),
                    origin,
                    basis,
                    samples=samples,
                )
            )
    label_local = np.quantile(local, [0.66], axis=0)[0]
    population = POPULATIONS[population_id]
    cloud = CLOUDS[cloud_id]
    return {
        "type": "contours",
        "id": f"{population_id}-{cloud_id}-3d-kde-contours",
        "label": f"{population['label']} {cloud['label']} 3-D density",
        "populationId": population_id,
        "cloudId": cloud_id,
        "count": len(arrays["rows"]),  # type: ignore[arg-type]
        "color": population["color"],
        "lineDash": cloud["lineDash"],
        "alpha": 0.72,
        "lineWidth": 0.95,
        "structureModel": "3d-kde-volume-contour-slices",
        "containmentLevels": [round_number(value, 2) for value in KDE3D_CONTAINMENT_LEVELS],
        "bandwidthKpc": [round_number(value, 3) for value in bandwidth],
        "zSliceKpc": [round_number(float(zs[index]), 3) for index in z_slices],
        "xSliceKpc": [round_number(float(xs[index]), 3) for index in x_slices],
        "ySliceKpc": [round_number(float(ys[index]), 3) for index in y_slices],
        "segments": segments,
        "labelVector": rounded_vector(vector_from_local(label_local, origin, basis)),
    }


SURFACE_NET_CORNERS = (
    (0, 0, 0),
    (1, 0, 0),
    (1, 1, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (1, 1, 1),
    (0, 1, 1),
)
SURFACE_NET_EDGES = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
)


def grid_point(xs: np.ndarray, ys: np.ndarray, zs: np.ndarray, i: int, j: int, k: int) -> np.ndarray:
    return np.array([xs[i], ys[j], zs[k]], dtype=float)


def surface_net_vertices(
    xs: np.ndarray,
    ys: np.ndarray,
    zs: np.ndarray,
    density: np.ndarray,
    level: float,
) -> tuple[dict[tuple[int, int, int], int], list[np.ndarray]]:
    cell_to_vertex: dict[tuple[int, int, int], int] = {}
    vertices: list[np.ndarray] = []
    nx, ny, nz = density.shape
    for i in range(nx - 1):
        for j in range(ny - 1):
            for k in range(nz - 1):
                values = np.array([density[i + dx, j + dy, k + dz] for dx, dy, dz in SURFACE_NET_CORNERS], dtype=float)
                above = values >= level
                if bool(np.all(above)) or not bool(np.any(above)):
                    continue
                crossings = []
                for first, second in SURFACE_NET_EDGES:
                    if above[first] == above[second]:
                        continue
                    first_offset = SURFACE_NET_CORNERS[first]
                    second_offset = SURFACE_NET_CORNERS[second]
                    first_point = grid_point(xs, ys, zs, i + first_offset[0], j + first_offset[1], k + first_offset[2])
                    second_point = grid_point(xs, ys, zs, i + second_offset[0], j + second_offset[1], k + second_offset[2])
                    first_value = values[first]
                    second_value = values[second]
                    fraction = 0.5 if first_value == second_value else (level - first_value) / (second_value - first_value)
                    crossings.append(first_point + np.clip(fraction, 0, 1) * (second_point - first_point))
                if not crossings:
                    continue
                cell_to_vertex[(i, j, k)] = len(vertices)
                vertices.append(np.mean(crossings, axis=0))
    return cell_to_vertex, vertices


def add_surface_quad_edges(edge_set: set[tuple[int, int]], cell_to_vertex: dict[tuple[int, int, int], int], cells: list[tuple[int, int, int]]) -> None:
    vertex_ids = [cell_to_vertex[cell] for cell in cells if cell in cell_to_vertex]
    if len(vertex_ids) != 4:
        return
    for first, second in zip(vertex_ids, (*vertex_ids[1:], vertex_ids[0])):
        if first != second:
            edge_set.add(tuple(sorted((first, second))))


def surface_net_edge_set(
    density: np.ndarray,
    level: float,
    cell_to_vertex: dict[tuple[int, int, int], int],
) -> set[tuple[int, int]]:
    nx, ny, nz = density.shape
    edge_set: set[tuple[int, int]] = set()
    for i in range(nx - 1):
        for j in range(ny):
            for k in range(nz):
                if (density[i, j, k] >= level) == (density[i + 1, j, k] >= level):
                    continue
                add_surface_quad_edges(edge_set, cell_to_vertex, [(i, j - 1, k - 1), (i, j, k - 1), (i, j, k), (i, j - 1, k)])
    for i in range(nx):
        for j in range(ny - 1):
            for k in range(nz):
                if (density[i, j, k] >= level) == (density[i, j + 1, k] >= level):
                    continue
                add_surface_quad_edges(edge_set, cell_to_vertex, [(i - 1, j, k - 1), (i, j, k - 1), (i, j, k), (i - 1, j, k)])
    for i in range(nx):
        for j in range(ny):
            for k in range(nz - 1):
                if (density[i, j, k] >= level) == (density[i, j, k + 1] >= level):
                    continue
                add_surface_quad_edges(edge_set, cell_to_vertex, [(i - 1, j - 1, k), (i, j - 1, k), (i, j, k), (i - 1, j, k)])
    return edge_set


def decimated_edges(edge_set: set[tuple[int, int]], max_segments: int = KDE3D_ISOSURFACE_MAX_SEGMENTS) -> list[tuple[int, int]]:
    edges = sorted(edge_set)
    if len(edges) <= max_segments:
        return edges
    step = math.ceil(len(edges) / max_segments)
    return edges[::step]


def build_3d_density_isosurface(
    payload: dict[str, object],
    indexes: dict[str, int],
    population_id: str,
    cloud_id: str,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> dict[str, object]:
    arrays = subset_arrays(payload, indexes, population_id, cloud_id)
    local = arrays["local"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    xs, ys, zs, density, bandwidth = kde_density_volume(local, sigma)
    level = density_volume_level_for_mass(xs, ys, zs, density, KDE3D_ISOSURFACE_CONTAINMENT)
    cell_to_vertex, vertices = surface_net_vertices(xs, ys, zs, density, level)
    edge_set = surface_net_edge_set(density, level, cell_to_vertex)
    kept_edges = decimated_edges(edge_set)
    segments = [
        [
            rounded_vector(vector_from_local(vertices[first], origin, basis)),
            rounded_vector(vector_from_local(vertices[second], origin, basis)),
        ]
        for first, second in kept_edges
    ]
    maximum = np.unravel_index(int(np.argmax(density)), density.shape)
    label_local = grid_point(xs, ys, zs, maximum[0], maximum[1], maximum[2])
    population = POPULATIONS[population_id]
    cloud = CLOUDS[cloud_id]
    return {
        "type": "isosurface",
        "id": f"{population_id}-{cloud_id}-3d-kde-isosurface",
        "label": f"{population['label']} {cloud['label']} 3-D isosurface",
        "populationId": population_id,
        "cloudId": cloud_id,
        "count": len(arrays["rows"]),  # type: ignore[arg-type]
        "color": population["color"],
        "lineDash": cloud["lineDash"],
        "alpha": 0.68,
        "lineWidth": 0.85,
        "structureModel": "3d-kde-isosurface-surface-net",
        "containment": round_number(KDE3D_ISOSURFACE_CONTAINMENT, 3),
        "densityLevel": round_number(level, 8),
        "bandwidthKpc": [round_number(value, 3) for value in bandwidth],
        "surfaceVertices": len(vertices),
        "surfaceEdges": len(edge_set),
        "displayedSurfaceEdges": len(kept_edges),
        "segments": segments,
        "labelVector": rounded_vector(vector_from_local(label_local, origin, basis)),
    }


def fit_payload_by_id(payload: dict[str, object], fit_id: str) -> dict[str, object] | None:
    fits = payload.get("meta", {}).get("annotationFits", {}).get("fits", [])  # type: ignore[union-attr]
    for fit in fits:
        if isinstance(fit, dict) and fit.get("id") == fit_id:
            return fit
    return None


def local_gaussian_from_fit_payload(
    fit: dict[str, object],
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> tuple[np.ndarray, np.ndarray] | None:
    center = fit.get("centerVector")
    axes = fit.get("axes")
    sigma = fit.get("axisSigmaKpc")
    axes_kpc = fit.get("axesKpc")
    if not isinstance(center, list) or not isinstance(axes, list):
        return None
    if not isinstance(sigma, list):
        if not isinstance(axes_kpc, list):
            return None
        sigma = [float(value) / CONFIDENCE_RADIUS for value in axes_kpc]
    center_vector = np.asarray(center, dtype=float)
    local_center = local_from_vector(center_vector, origin, basis)
    covariance = np.zeros((3, 3), dtype=float)
    for axis, axis_sigma in zip(axes, sigma):
        axis_vector = np.asarray(axis, dtype=float)
        local_axis = np.array(
            [
                float(axis_vector @ basis["east"]),
                float(axis_vector @ basis["north"]),
                float(axis_vector @ basis["radial"]),
            ]
        )
        norm = float(np.linalg.norm(local_axis))
        if norm <= 0:
            continue
        local_axis /= norm
        covariance += float(axis_sigma) ** 2 * np.outer(local_axis, local_axis)
    return local_center, positive_semidefinite(covariance)


def gaussian_density_volume(
    xs: np.ndarray,
    ys: np.ndarray,
    zs: np.ndarray,
    mean: np.ndarray,
    covariance: np.ndarray,
) -> np.ndarray:
    covariance = positive_semidefinite(covariance)
    inverse = np.linalg.inv(covariance)
    sign, logdet = np.linalg.slogdet(covariance)
    if sign <= 0:
        return np.zeros((len(xs), len(ys), len(zs)), dtype=float)
    x_grid, y_grid, z_grid = np.meshgrid(xs, ys, zs, indexing="ij")
    delta = np.stack([x_grid - mean[0], y_grid - mean[1], z_grid - mean[2]], axis=-1)
    mahalanobis = np.einsum("...i,ij,...j->...", delta, inverse, delta)
    norm = math.exp(-0.5 * (3 * math.log(2 * math.pi) + logdet))
    return norm * np.exp(-0.5 * mahalanobis)


def local_measurement_covariances(
    position: np.ndarray,
    sigma: np.ndarray,
    basis: dict[str, np.ndarray],
) -> np.ndarray:
    unit = position / np.linalg.norm(position, axis=1)[:, None]
    local_unit = np.column_stack(
        [
            unit @ basis["east"],
            unit @ basis["north"],
            unit @ basis["radial"],
        ]
    )
    return sigma[:, None, None] ** 2 * local_unit[:, :, None] * local_unit[:, None, :]


def weighted_eiv_gaussian(local: np.ndarray, measurement: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    weights = np.maximum(np.asarray(weights, dtype=float), 0)
    total = float(np.sum(weights))
    if total <= 0:
        weights = np.ones(len(local), dtype=float)
        total = float(len(local))
    mean = (local * weights[:, None]).sum(axis=0) / total
    delta = local - mean
    scatter = np.einsum("n,ni,nj->ij", weights, delta, delta) / total
    mean_measurement = (measurement * weights[:, None, None]).sum(axis=0) / total
    return mean, positive_semidefinite(scatter - mean_measurement)


def log_gaussian_eiv_local(local: np.ndarray, measurement: np.ndarray, mean: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    total = covariance[None, :, :] + measurement + np.eye(3)[None, :, :] * 1e-6
    total = (total + np.swapaxes(total, 1, 2)) * 0.5
    sign, logdet = np.linalg.slogdet(total)
    if np.any(sign <= 0):
        total[sign <= 0] += np.eye(3) * 1e-3
        sign, logdet = np.linalg.slogdet(total)
    inverse = np.linalg.inv(total)
    delta = local - mean
    mahalanobis = np.einsum("ni,nij,nj->n", delta, inverse, delta)
    return -0.5 * (3 * math.log(2 * math.pi) + logdet + mahalanobis)


def log_student_t_eiv_local(
    local: np.ndarray,
    measurement: np.ndarray,
    mean: np.ndarray,
    covariance: np.ndarray,
    degrees_of_freedom: float,
) -> np.ndarray:
    dimension = 3
    total = covariance[None, :, :] + measurement + np.eye(dimension)[None, :, :] * 1e-6
    total = (total + np.swapaxes(total, 1, 2)) * 0.5
    sign, logdet = np.linalg.slogdet(total)
    if np.any(sign <= 0):
        total[sign <= 0] += np.eye(dimension) * 1e-3
        sign, logdet = np.linalg.slogdet(total)
    inverse = np.linalg.inv(total)
    delta = local - mean
    mahalanobis = np.einsum("ni,nij,nj->n", delta, inverse, delta)
    norm = (
        math.lgamma((degrees_of_freedom + dimension) * 0.5)
        - math.lgamma(degrees_of_freedom * 0.5)
        - 0.5 * dimension * math.log(degrees_of_freedom * math.pi)
    )
    return norm - 0.5 * logdet - 0.5 * (degrees_of_freedom + dimension) * np.log1p(
        mahalanobis / degrees_of_freedom
    )


def _beta_continued_fraction(a: float, b: float, x: float) -> float:
    epsilon = 3e-12
    tiny = 1e-300
    qab = a + b
    qap = a + 1
    qam = a - 1
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for iteration in range(1, 200):
        m2 = 2 * iteration
        aa = iteration * (b - iteration) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + iteration) * (qab + iteration) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < epsilon:
            break
    return h


def regularized_beta(a: float, b: float, x: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    beta_term = math.exp(
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + a * math.log(x)
        + b * math.log1p(-x)
    )
    if x < (a + 1) / (a + b + 2):
        return beta_term * _beta_continued_fraction(a, b, x) / a
    return 1 - beta_term * _beta_continued_fraction(b, a, 1 - x) / b


def student_t_containment_radius(
    degrees_of_freedom: float,
    containment: float = STUDENT_T_BODY_CONTAINMENT,
    dimension: int = 3,
) -> float:
    def radial_cdf(radius: float) -> float:
        f_value = radius * radius / dimension
        x = dimension * f_value / (dimension * f_value + degrees_of_freedom)
        return regularized_beta(dimension * 0.5, degrees_of_freedom * 0.5, x)

    low = 0.0
    high = CONFIDENCE_RADIUS
    while radial_cdf(high) < containment:
        high *= 1.5
    for _iteration in range(70):
        mid = (low + high) * 0.5
        if radial_cdf(mid) < containment:
            low = mid
        else:
            high = mid
    return (low + high) * 0.5


def logsumexp_rows(values: np.ndarray) -> np.ndarray:
    maximum = np.max(values, axis=1)
    return maximum + np.log(np.exp(values - maximum[:, None]).sum(axis=1))


def eiv_mixture_component_logs(
    local: np.ndarray,
    measurement: np.ndarray,
    weights: np.ndarray,
    means: np.ndarray,
    covariances: np.ndarray,
) -> np.ndarray:
    logs = []
    for weight, mean, covariance in zip(weights, means, covariances):
        logs.append(np.log(max(float(weight), 1e-12)) + log_gaussian_eiv_local(local, measurement, mean, covariance))
    return np.vstack(logs).T


def log_eiv_mixture_local(
    local: np.ndarray,
    measurement: np.ndarray,
    weights: np.ndarray,
    means: np.ndarray,
    covariances: np.ndarray,
) -> np.ndarray:
    return logsumexp_rows(eiv_mixture_component_logs(local, measurement, weights, means, covariances))


def projected_core_seed_weights(local: np.ndarray) -> np.ndarray:
    xy = local[:, :2]
    sky_median = np.median(xy, axis=0)
    sky_mad = np.maximum(np.median(np.abs(xy - sky_median), axis=0) * 1.4826, 0.2)
    sky_radius = np.sqrt(np.sum(((xy - sky_median) / sky_mad) ** 2, axis=1))
    body_cutoff = max(float(np.quantile(sky_radius, EIV_GMM_SKY_CORE_FRACTION)), 1e-6)
    body_weights = np.clip(1 - (sky_radius / body_cutoff) ** 2, 0, 1) ** EIV_GMM_SKY_WEIGHT_POWER
    depth_residual = local[:, 2] - float(np.median(local[:, 2]))
    depth_endpoint = float(np.quantile(np.abs(depth_residual), EIV_GMM_DEPTH_ENDPOINT_CONTAINMENT))
    body_weights[np.abs(depth_residual) > depth_endpoint] *= EIV_GMM_DEPTH_ENDPOINT_WEIGHT
    return body_weights


def fit_eiv_gaussian_mixture_from_seeds(
    local: np.ndarray,
    measurement: np.ndarray,
    initial_weights: np.ndarray,
    initial_means: np.ndarray,
    initial_covariances: np.ndarray,
) -> dict[str, object]:
    weights = np.asarray(initial_weights, dtype=float)
    weights = np.maximum(weights, 1e-5)
    weights /= weights.sum()
    means = np.asarray(initial_means, dtype=float)
    covariances = np.asarray([positive_semidefinite(covariance) for covariance in initial_covariances], dtype=float)
    component_count = len(weights)
    previous_log_likelihood = -np.inf
    responsibilities = np.full((len(local), component_count), 1 / component_count, dtype=float)
    log_likelihood = float("-inf")
    iterations = 0
    converged = False

    for iterations in range(1, EIV_GMM_MAX_ITER + 1):
        component_logs = eiv_mixture_component_logs(local, measurement, weights, means, covariances)
        log_denominator = logsumexp_rows(component_logs)
        log_likelihood = float(log_denominator.sum())
        responsibilities = np.exp(component_logs - log_denominator[:, None])
        component_totals = responsibilities.sum(axis=0)

        next_weights = np.maximum(component_totals / len(local), 1e-5)
        next_weights /= next_weights.sum()
        next_means = []
        next_covariances = []
        for component in range(component_count):
            if component_totals[component] < 50:
                next_means.append(means[component])
                next_covariances.append(covariances[component])
                continue
            mean, covariance = weighted_eiv_gaussian(local, measurement, responsibilities[:, component])
            next_means.append(mean)
            next_covariances.append(covariance)

        weights = next_weights
        means = np.asarray(next_means, dtype=float)
        covariances = np.asarray(next_covariances, dtype=float)
        if (
            iterations > 4
            and log_likelihood - previous_log_likelihood
            < EIV_GMM_TOL * max(1.0, abs(previous_log_likelihood))
        ):
            converged = True
            break
        previous_log_likelihood = log_likelihood

    return {
        "weights": weights,
        "means": means,
        "covariances": covariances,
        "responsibilities": responsibilities,
        "logLikelihood": log_likelihood,
        "iterations": iterations,
        "converged": converged,
    }


def fit_eiv_gmm_model_selection(
    local: np.ndarray,
    measurement: np.ndarray,
) -> list[dict[str, object]]:
    full_mean, full_covariance = weighted_eiv_gaussian(local, measurement, np.ones(len(local), dtype=float))
    body_seed_weights = projected_core_seed_weights(local)
    body_mean, body_covariance = weighted_eiv_gaussian(local, measurement, body_seed_weights)
    halo_seed_weights = np.clip(1 - 0.72 * body_seed_weights / max(float(np.max(body_seed_weights)), 1e-6), 0.28, 1)
    halo_mean, halo_covariance = weighted_eiv_gaussian(local, measurement, halo_seed_weights)
    broad_covariance = positive_semidefinite(full_covariance * 12.25)

    candidates: list[dict[str, object]] = []
    for component_count in EIV_GMM_COMPONENT_COUNTS:
        if component_count == 1:
            weights = np.array([1.0], dtype=float)
            means = full_mean[None, :]
            covariances = full_covariance[None, :, :]
            log_likelihood = float(log_eiv_mixture_local(local, measurement, weights, means, covariances).sum())
            responsibilities = np.ones((len(local), 1), dtype=float)
            iterations = 1
            converged = True
        elif component_count == 2:
            initial_weights = np.array([0.35, 0.65], dtype=float)
            initial_means = np.asarray([body_mean, halo_mean], dtype=float)
            initial_covariances = np.asarray([body_covariance, halo_covariance], dtype=float)
            fit = fit_eiv_gaussian_mixture_from_seeds(local, measurement, initial_weights, initial_means, initial_covariances)
            weights = fit["weights"]  # type: ignore[assignment]
            means = fit["means"]  # type: ignore[assignment]
            covariances = fit["covariances"]  # type: ignore[assignment]
            responsibilities = fit["responsibilities"]  # type: ignore[assignment]
            log_likelihood = float(fit["logLikelihood"])
            iterations = int(fit["iterations"])
            converged = bool(fit["converged"])
        else:
            initial_weights = np.array([0.3, 0.65, 0.05], dtype=float)
            initial_means = np.asarray([body_mean, halo_mean, full_mean], dtype=float)
            initial_covariances = np.asarray([body_covariance, halo_covariance, broad_covariance], dtype=float)
            fit = fit_eiv_gaussian_mixture_from_seeds(local, measurement, initial_weights, initial_means, initial_covariances)
            weights = fit["weights"]  # type: ignore[assignment]
            means = fit["means"]  # type: ignore[assignment]
            covariances = fit["covariances"]  # type: ignore[assignment]
            responsibilities = fit["responsibilities"]  # type: ignore[assignment]
            log_likelihood = float(fit["logLikelihood"])
            iterations = int(fit["iterations"])
            converged = bool(fit["converged"])

        parameter_count = component_count * 9 + component_count - 1
        candidates.append(
            {
                "componentCount": component_count,
                "weights": weights,
                "means": means,
                "covariances": covariances,
                "responsibilities": responsibilities,
                "logLikelihood": log_likelihood,
                "aic": 2 * parameter_count - 2 * log_likelihood,
                "bic": parameter_count * math.log(len(local)) - 2 * log_likelihood,
                "parameterCount": parameter_count,
                "iterations": iterations,
                "converged": converged,
            }
        )
    return candidates


def fit_student_t_ellipsoid(
    local: np.ndarray,
    measurement: np.ndarray,
) -> dict[str, object]:
    best: dict[str, object] | None = None
    for degrees_of_freedom in STUDENT_T_DF_GRID:
        mean, covariance = weighted_eiv_gaussian(local, measurement, np.ones(len(local), dtype=float))
        previous_log_likelihood = -np.inf
        log_likelihood = float("-inf")
        iterations = 0
        converged = False

        for iterations in range(1, EIV_GMM_MAX_ITER + 1):
            total = covariance[None, :, :] + measurement + np.eye(3)[None, :, :] * 1e-6
            total = (total + np.swapaxes(total, 1, 2)) * 0.5
            sign, _logdet = np.linalg.slogdet(total)
            if np.any(sign <= 0):
                total[sign <= 0] += np.eye(3) * 1e-3
            inverse = np.linalg.inv(total)
            delta = local - mean
            mahalanobis = np.einsum("ni,nij,nj->n", delta, inverse, delta)
            robust_weights = (degrees_of_freedom + 3) / (degrees_of_freedom + np.maximum(mahalanobis, 0))
            mean, covariance = weighted_eiv_gaussian(local, measurement, robust_weights)
            log_likelihood = float(log_student_t_eiv_local(local, measurement, mean, covariance, degrees_of_freedom).sum())

            if (
                iterations > 4
                and log_likelihood - previous_log_likelihood
                < EIV_GMM_TOL * max(1.0, abs(previous_log_likelihood))
            ):
                converged = True
                break
            previous_log_likelihood = log_likelihood

        log_likelihood = float(log_student_t_eiv_local(local, measurement, mean, covariance, degrees_of_freedom).sum())
        parameter_count = 10
        candidate = {
            "degreesOfFreedom": degrees_of_freedom,
            "mean": mean,
            "covariance": covariance,
            "logLikelihood": log_likelihood,
            "aic": 2 * parameter_count - 2 * log_likelihood,
            "bic": parameter_count * math.log(len(local)) - 2 * log_likelihood,
            "parameterCount": parameter_count,
            "iterations": iterations,
            "converged": converged,
        }
        if best is None or float(candidate["bic"]) < float(best["bic"]):
            best = candidate

    assert best is not None
    return best


def fit_student_t_body_gaussian_tail(
    local: np.ndarray,
    measurement: np.ndarray,
    gmm_candidates: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    if gmm_candidates is None:
        gmm_candidates = fit_eiv_gmm_model_selection(local, measurement)
    seed = next(candidate for candidate in gmm_candidates if int(candidate["componentCount"]) == 2)
    seed_weights = seed["weights"]  # type: ignore[assignment]
    seed_means = seed["means"]  # type: ignore[assignment]
    seed_covariances = seed["covariances"]  # type: ignore[assignment]
    body_index = int(np.argmax(seed_weights))
    tail_index = 1 - body_index
    best: dict[str, object] | None = None

    for degrees_of_freedom in STUDENT_T_DF_GRID:
        weights = np.array([float(seed_weights[body_index]), float(seed_weights[tail_index])], dtype=float)
        weights /= weights.sum()
        body_mean = np.asarray(seed_means[body_index], dtype=float)
        body_covariance = np.asarray(seed_covariances[body_index], dtype=float)
        tail_mean = np.asarray(seed_means[tail_index], dtype=float)
        tail_covariance = np.asarray(seed_covariances[tail_index], dtype=float)
        responsibilities = np.zeros((len(local), 2), dtype=float)
        previous_log_likelihood = -np.inf
        log_likelihood = float("-inf")
        converged = False
        iterations = 0

        for iterations in range(1, EIV_GMM_MAX_ITER + 1):
            body_log = math.log(max(float(weights[0]), 1e-12)) + log_student_t_eiv_local(
                local,
                measurement,
                body_mean,
                body_covariance,
                degrees_of_freedom,
            )
            tail_log = math.log(max(float(weights[1]), 1e-12)) + log_gaussian_eiv_local(
                local,
                measurement,
                tail_mean,
                tail_covariance,
            )
            stacked = np.column_stack([body_log, tail_log])
            denominator = logsumexp_rows(stacked)
            responsibilities = np.exp(stacked - denominator[:, None])

            total = body_covariance[None, :, :] + measurement + np.eye(3)[None, :, :] * 1e-6
            total = (total + np.swapaxes(total, 1, 2)) * 0.5
            inverse = np.linalg.inv(total)
            delta = local - body_mean
            mahalanobis = np.einsum("ni,nij,nj->n", delta, inverse, delta)
            robust_body_weights = responsibilities[:, 0] * (degrees_of_freedom + 3) / (
                degrees_of_freedom + np.maximum(mahalanobis, 0)
            )
            body_mean, body_covariance = weighted_eiv_gaussian(local, measurement, robust_body_weights)
            tail_mean, tail_covariance = weighted_eiv_gaussian(local, measurement, responsibilities[:, 1])
            weights = np.maximum(responsibilities.sum(axis=0) / len(local), 1e-5)
            weights /= weights.sum()
            log_likelihood = float(denominator.sum())

            if (
                iterations > 4
                and log_likelihood - previous_log_likelihood
                < EIV_GMM_TOL * max(1.0, abs(previous_log_likelihood))
            ):
                converged = True
                break
            previous_log_likelihood = log_likelihood

        body_log = math.log(max(float(weights[0]), 1e-12)) + log_student_t_eiv_local(
            local,
            measurement,
            body_mean,
            body_covariance,
            degrees_of_freedom,
        )
        tail_log = math.log(max(float(weights[1]), 1e-12)) + log_gaussian_eiv_local(
            local,
            measurement,
            tail_mean,
            tail_covariance,
        )
        stacked = np.column_stack([body_log, tail_log])
        denominator = logsumexp_rows(stacked)
        responsibilities = np.exp(stacked - denominator[:, None])
        log_likelihood = float(denominator.sum())
        parameter_count = 20
        candidate = {
            "degreesOfFreedom": degrees_of_freedom,
            "weights": weights,
            "bodyMean": body_mean,
            "bodyCovariance": body_covariance,
            "tailMean": tail_mean,
            "tailCovariance": tail_covariance,
            "responsibilities": responsibilities,
            "logLikelihood": log_likelihood,
            "aic": 2 * parameter_count - 2 * log_likelihood,
            "bic": parameter_count * math.log(len(local)) - 2 * log_likelihood,
            "parameterCount": parameter_count,
            "iterations": iterations,
            "converged": converged,
        }
        if best is None or float(candidate["bic"]) < float(best["bic"]):
            best = candidate

    assert best is not None
    return best


def ellipsoid_axis_metrics(covariance: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, float]:
    values, vectors = np.linalg.eigh(positive_semidefinite(covariance))
    order = np.argsort(values)[::-1]
    values = np.maximum(values[order], EIGEN_FLOOR)
    vectors = vectors[:, order]
    axes = np.sqrt(values) * CONFIDENCE_RADIUS
    line_of_sight_major_axis_cosine = abs(float(vectors[2, 0]))
    projected_sky_area = math.sqrt(max(float(np.linalg.det(positive_semidefinite(covariance[:2, :2]))), 1e-12))
    return axes, vectors, line_of_sight_major_axis_cosine, projected_sky_area


def ordered_covariance_axes(covariance: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(positive_semidefinite(covariance))
    order = np.argsort(values)[::-1]
    values = np.maximum(values[order], EIGEN_FLOOR)
    vectors = vectors[:, order]
    for index in range(3):
        pivot = int(np.argmax(np.abs(vectors[:, index])))
        if vectors[pivot, index] < 0:
            vectors[:, index] *= -1
    return np.sqrt(values) * CONFIDENCE_RADIUS, vectors


def positive_semidefinite_2d(covariance: np.ndarray, floor: float = EIGEN_FLOOR) -> np.ndarray:
    covariance = (covariance + covariance.T) * 0.5
    values, vectors = np.linalg.eigh(covariance)
    values = np.maximum(values, floor)
    return (vectors * values) @ vectors.T


def weighted_eiv_gaussian_2d(local_xy: np.ndarray, measurement_xy: np.ndarray, weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    weights = np.maximum(np.asarray(weights, dtype=float), 0)
    total = float(np.sum(weights))
    if total <= 0:
        weights = np.ones(len(local_xy), dtype=float)
        total = float(len(local_xy))
    mean = (local_xy * weights[:, None]).sum(axis=0) / total
    delta = local_xy - mean
    scatter = np.einsum("n,ni,nj->ij", weights, delta, delta) / total
    mean_measurement = (measurement_xy * weights[:, None, None]).sum(axis=0) / total
    return mean, positive_semidefinite_2d(scatter - mean_measurement)


def log_gaussian_eiv_2d(local_xy: np.ndarray, measurement_xy: np.ndarray, mean: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    total = covariance[None, :, :] + measurement_xy + np.eye(2)[None, :, :] * 1e-6
    total = (total + np.swapaxes(total, 1, 2)) * 0.5
    sign, logdet = np.linalg.slogdet(total)
    if np.any(sign <= 0):
        total[sign <= 0] += np.eye(2) * 1e-3
        sign, logdet = np.linalg.slogdet(total)
    inverse = np.linalg.inv(total)
    delta = local_xy - mean
    mahalanobis = np.einsum("ni,nij,nj->n", delta, inverse, delta)
    return -0.5 * (2 * math.log(2 * math.pi) + logdet + mahalanobis)


def log_eiv_mixture_2d(
    local_xy: np.ndarray,
    measurement_xy: np.ndarray,
    weights: np.ndarray,
    means: np.ndarray,
    covariances: np.ndarray,
) -> np.ndarray:
    component_logs = [
        math.log(max(float(weight), 1e-12)) + log_gaussian_eiv_2d(local_xy, measurement_xy, mean, covariance)
        for weight, mean, covariance in zip(weights, means, covariances)
    ]
    return logsumexp_rows(np.vstack(component_logs).T)


def fit_eiv_gaussian_mixture_2d(
    local_xy: np.ndarray,
    measurement_xy: np.ndarray,
    component_count: int,
    seed: int,
    sample_weights: np.ndarray | None = None,
    max_iterations: int = EIV_GMM_MAX_ITER,
) -> dict[str, object]:
    rng = np.random.default_rng(seed)
    if sample_weights is None:
        sample_weights = np.ones(len(local_xy), dtype=float)
    sample_weights = np.maximum(np.asarray(sample_weights, dtype=float), 0)
    if not np.any(sample_weights > 0):
        sample_weights = np.ones(len(local_xy), dtype=float)
    sample_total = max(float(np.sum(sample_weights)), 1e-12)
    full_mean, full_covariance = weighted_eiv_gaussian_2d(local_xy, measurement_xy, sample_weights)
    values, vectors = np.linalg.eigh(full_covariance)
    major_axis = vectors[:, int(np.argmax(values))]
    projected = (local_xy - full_mean) @ major_axis
    cuts = np.quantile(projected, np.linspace(0, 1, component_count + 1)[1:-1]) if component_count > 1 else []
    labels = np.digitize(projected, cuts) if component_count > 1 else np.zeros(len(local_xy), dtype=int)

    weights = []
    means = []
    covariances = []
    for component in range(component_count):
        mask = labels == component
        if int(mask.sum()) < 25:
            mask = rng.random(len(local_xy)) < 1 / component_count
        component_weights = sample_weights * mask.astype(float)
        mean, covariance = weighted_eiv_gaussian_2d(local_xy, measurement_xy, component_weights)
        weights.append(max(float(component_weights.sum() / sample_total), 1e-5))
        means.append(mean)
        covariances.append(covariance)

    weights_array = np.asarray(weights, dtype=float)
    weights_array /= weights_array.sum()
    means_array = np.asarray(means, dtype=float)
    covariances_array = np.asarray(covariances, dtype=float)
    previous_log_likelihood = -np.inf
    log_likelihood = float("-inf")
    iterations = 0
    converged = False
    responsibilities = np.full((len(local_xy), component_count), 1 / component_count, dtype=float)

    for iterations in range(1, max_iterations + 1):
        component_logs = [
            math.log(max(float(weight), 1e-12)) + log_gaussian_eiv_2d(local_xy, measurement_xy, mean, covariance)
            for weight, mean, covariance in zip(weights_array, means_array, covariances_array)
        ]
        stacked = np.vstack(component_logs).T
        denominator = logsumexp_rows(stacked)
        log_likelihood = float((sample_weights * denominator).sum())
        responsibilities = np.exp(stacked - denominator[:, None])
        weighted_responsibilities = responsibilities * sample_weights[:, None]
        totals = weighted_responsibilities.sum(axis=0)

        if (
            iterations > 4
            and log_likelihood - previous_log_likelihood
            < EIV_GMM_TOL * max(1.0, abs(previous_log_likelihood))
        ):
            converged = True
            break
        previous_log_likelihood = log_likelihood

        weights_array = np.maximum(totals / sample_total, 1e-5)
        weights_array /= weights_array.sum()
        next_means = []
        next_covariances = []
        for component in range(component_count):
            if totals[component] < max(12.0, 0.003 * sample_total):
                next_means.append(local_xy[int(rng.integers(0, len(local_xy)))])
                next_covariances.append(full_covariance)
                continue
            mean, covariance = weighted_eiv_gaussian_2d(local_xy, measurement_xy, weighted_responsibilities[:, component])
            next_means.append(mean)
            next_covariances.append(covariance)
        means_array = np.asarray(next_means, dtype=float)
        covariances_array = np.asarray(next_covariances, dtype=float)

    log_likelihood = float((sample_weights * log_eiv_mixture_2d(local_xy, measurement_xy, weights_array, means_array, covariances_array)).sum())
    return {
        "componentCount": component_count,
        "weights": weights_array,
        "means": means_array,
        "covariances": covariances_array,
        "responsibilities": responsibilities,
        "logLikelihood2d": log_likelihood,
        "iterations": iterations,
        "converged": converged,
    }


def weighted_center(values: np.ndarray, weights: np.ndarray) -> np.ndarray:
    weights = np.maximum(np.asarray(weights, dtype=float), 0)
    if not np.any(weights > 0):
        return values.mean(axis=0)
    return (values * weights[:, None]).sum(axis=0) / max(float(np.sum(weights)), 1e-12)


def fit_lmc_cepheid_disk_density_params(
    local: np.ndarray,
    measurement: np.ndarray,
    disk_weights: np.ndarray,
    surface_model: str,
    disk_component_count: int,
    seed: int,
) -> dict[str, object]:
    disk_weights = np.maximum(np.asarray(disk_weights, dtype=float), 1e-8)
    local_mean = weighted_center(local, disk_weights)
    centered = local - local_mean
    sigma_z = np.sqrt(np.maximum(measurement[:, 2, 2], 1e-6))
    coefficients, scatter2 = fit_surface_params_weighted(centered, sigma_z, surface_model, disk_weights)
    inplane = fit_eiv_gaussian_mixture_2d(
        centered[:, :2],
        measurement[:, :2, :2],
        disk_component_count,
        seed=seed,
        sample_weights=disk_weights,
        max_iterations=LMC_CEPHEID_BAR_DISK_GMM_ITERATIONS,
    )
    return {
        "surfaceModel": surface_model,
        "componentCount": disk_component_count,
        "localMean": local_mean,
        "coefficients": coefficients,
        "scatter2": scatter2,
        "inplaneWeights": inplane["weights"],
        "inplaneMeans": inplane["means"],
        "inplaneCovariances": inplane["covariances"],
        "inplaneLogLikelihood2d": inplane["logLikelihood2d"],
        "inplaneConverged": inplane["converged"],
        "inplaneIterations": inplane["iterations"],
    }


def lmc_cepheid_disk_log_density(
    local: np.ndarray,
    measurement: np.ndarray,
    disk_params: dict[str, object],
) -> np.ndarray:
    local_mean = disk_params["localMean"]  # type: ignore[assignment]
    centered = local - local_mean
    log_xy = log_eiv_mixture_2d(
        centered[:, :2],
        measurement[:, :2, :2],
        disk_params["inplaneWeights"],  # type: ignore[arg-type]
        disk_params["inplaneMeans"],  # type: ignore[arg-type]
        disk_params["inplaneCovariances"],  # type: ignore[arg-type]
    )
    design = surface_design_matrix(centered[:, :2], str(disk_params["surfaceModel"]))
    residual = centered[:, 2] - design @ disk_params["coefficients"]  # type: ignore[operator]
    variance = np.maximum(measurement[:, 2, 2] + float(disk_params["scatter2"]), 1e-6)
    log_z = -0.5 * (np.log(2 * math.pi * variance) + residual**2 / variance)
    return log_xy + log_z


def lmc_cepheid_bar_disk_parameter_count(surface_model: str, disk_component_count: int) -> int:
    surface_parameters = surface_design_matrix(np.zeros((1, 2), dtype=float), surface_model).shape[1] + 1
    disk_inplane_parameters = disk_component_count * 5 + (disk_component_count - 1)
    return 1 + 9 + 3 + surface_parameters + disk_inplane_parameters


def lmc_cepheid_bar_disk_component_logs(
    local: np.ndarray,
    measurement: np.ndarray,
    bar_mean: np.ndarray,
    bar_covariance: np.ndarray,
    disk_params: dict[str, object],
    pi_bar: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    log_bar = math.log(max(pi_bar, 1e-9)) + log_gaussian_eiv_local(local, measurement, bar_mean, bar_covariance)
    log_disk = math.log(max(1 - pi_bar, 1e-9)) + lmc_cepheid_disk_log_density(local, measurement, disk_params)
    stacked = np.column_stack([log_bar, log_disk])
    denominator = logsumexp_rows(stacked)
    return log_bar, log_disk, denominator


def fit_lmc_cepheid_bar_disk_candidate(
    local: np.ndarray,
    measurement: np.ndarray,
    initial_bar_responsibility: np.ndarray,
    surface_model: str,
    disk_component_count: int,
    seed: int,
    *,
    fixed_membership: bool = False,
) -> dict[str, object]:
    n = len(local)
    if fixed_membership:
        responsibilities = (initial_bar_responsibility >= 0.5).astype(float)
    else:
        responsibilities = np.clip(initial_bar_responsibility.astype(float), 0.02, 0.98)
    previous_log_likelihood = -np.inf
    converged = fixed_membership
    iterations = 1

    for iterations in range(1, (1 if fixed_membership else LMC_CEPHEID_BAR_DISK_EM_ITERATIONS) + 1):
        pi_bar = min(0.98, max(0.02, float(np.mean(responsibilities))))
        bar_mean, bar_covariance = weighted_eiv_gaussian(local, measurement, responsibilities)
        disk_params = fit_lmc_cepheid_disk_density_params(
            local,
            measurement,
            1 - responsibilities,
            surface_model,
            disk_component_count,
            seed + iterations * 37,
        )
        log_bar, _log_disk, denominator = lmc_cepheid_bar_disk_component_logs(
            local,
            measurement,
            bar_mean,
            bar_covariance,
            disk_params,
            pi_bar,
        )
        log_likelihood = float(denominator.sum())
        posterior_bar = np.exp(log_bar - denominator)
        membership_delta = float(np.mean(np.abs(posterior_bar - responsibilities)))
        if fixed_membership:
            break
        if (
            iterations > 2
            and (
                log_likelihood - previous_log_likelihood
                < LMC_CEPHEID_BAR_DISK_TOL * max(1.0, abs(previous_log_likelihood))
                or membership_delta < 2e-4
            )
        ):
            responsibilities = posterior_bar
            converged = True
            break
        previous_log_likelihood = log_likelihood
        responsibilities = 0.72 * posterior_bar + 0.28 * responsibilities

    pi_bar = min(0.98, max(0.02, float(np.mean(responsibilities))))
    bar_mean, bar_covariance = weighted_eiv_gaussian(local, measurement, responsibilities)
    disk_params = fit_lmc_cepheid_disk_density_params(
        local,
        measurement,
        1 - responsibilities,
        surface_model,
        disk_component_count,
        seed + 991,
    )
    log_bar, _log_disk, denominator = lmc_cepheid_bar_disk_component_logs(
        local,
        measurement,
        bar_mean,
        bar_covariance,
        disk_params,
        pi_bar,
    )
    log_likelihood = float(denominator.sum())
    posterior_bar = np.exp(log_bar - denominator)
    if not fixed_membership:
        responsibilities = posterior_bar
        pi_bar = min(0.98, max(0.02, float(np.mean(responsibilities))))
        bar_mean, bar_covariance = weighted_eiv_gaussian(local, measurement, responsibilities)
        disk_params = fit_lmc_cepheid_disk_density_params(
            local,
            measurement,
            1 - responsibilities,
            surface_model,
            disk_component_count,
            seed + 1237,
        )
        log_bar, _log_disk, denominator = lmc_cepheid_bar_disk_component_logs(
            local,
            measurement,
            bar_mean,
            bar_covariance,
            disk_params,
            pi_bar,
        )
        log_likelihood = float(denominator.sum())
        responsibilities = np.exp(log_bar - denominator)
        pi_bar = min(0.98, max(0.02, float(np.mean(responsibilities))))
        bar_mean, bar_covariance = weighted_eiv_gaussian(local, measurement, responsibilities)
        disk_params = fit_lmc_cepheid_disk_density_params(
            local,
            measurement,
            1 - responsibilities,
            surface_model,
            disk_component_count,
            seed + 1499,
        )
        _log_bar, _log_disk, denominator = lmc_cepheid_bar_disk_component_logs(
            local,
            measurement,
            bar_mean,
            bar_covariance,
            disk_params,
            pi_bar,
        )
        log_likelihood = float(denominator.sum())

    parameter_count = lmc_cepheid_bar_disk_parameter_count(surface_model, disk_component_count)
    bic = -2 * log_likelihood + parameter_count * math.log(max(n, 2))
    aic = -2 * log_likelihood + 2 * parameter_count
    model_name = (
        f"{'fixed Ripepi split' if fixed_membership else 'soft EM'}; "
        f"{surface_model} disk; {disk_component_count}-component in-plane GMM; 3D EIV bar"
    )
    return {
        "model": model_name,
        "fixedMembership": fixed_membership,
        "surfaceModel": surface_model,
        "diskComponentCount": disk_component_count,
        "barMean": bar_mean,
        "barCovariance": bar_covariance,
        "diskParams": disk_params,
        "responsibilities": responsibilities,
        "piBar": pi_bar,
        "logLikelihood": log_likelihood,
        "parameterCount": parameter_count,
        "bic": bic,
        "aic": aic,
        "iterations": iterations,
        "converged": converged,
    }


def fit_lmc_cepheid_bar_disk_model_selection(
    local: np.ndarray,
    measurement: np.ndarray,
    ripepi_bar_mask: np.ndarray,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    initial = np.where(ripepi_bar_mask, 0.86, 0.08).astype(float)
    candidates: list[dict[str, object]] = [
        fit_lmc_cepheid_bar_disk_candidate(
            local,
            measurement,
            initial,
            "tilted-plane",
            3,
            seed=5101,
            fixed_membership=True,
        )
    ]
    seed = 5200
    for surface_model in LMC_CEPHEID_BAR_DISK_SURFACE_MODELS:
        for disk_component_count in LMC_CEPHEID_BAR_DISK_COMPONENT_OPTIONS:
            candidates.append(
                fit_lmc_cepheid_bar_disk_candidate(
                    local,
                    measurement,
                    initial,
                    surface_model,
                    disk_component_count,
                    seed=seed,
                )
            )
            seed += 97
    candidates.sort(key=lambda item: float(item["bic"]))
    best_bic = float(candidates[0]["bic"])
    relative = np.asarray([math.exp(-0.5 * min(float(item["bic"]) - best_bic, 700.0)) for item in candidates], dtype=float)
    relative /= max(float(relative.sum()), 1e-300)
    summary = []
    for item, weight in zip(candidates, relative):
        summary.append(
            {
                "model": item["model"],
                "surfaceModel": item["surfaceModel"],
                "diskComponentCount": item["diskComponentCount"],
                "fixedMembership": item["fixedMembership"],
                "logLikelihood": round_number(float(item["logLikelihood"]), 3),
                "parameters": int(item["parameterCount"]),
                "bic": round_number(float(item["bic"]), 3),
                "deltaBic": round_number(float(item["bic"]) - best_bic, 3),
                "aic": round_number(float(item["aic"]), 3),
                "bicWeight": round_number(float(weight), 6),
                "iterations": int(item["iterations"]),
                "converged": bool(item["converged"]),
            }
        )
    return candidates[0], summary


def sigmoid_array(values: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-np.clip(values, -50, 50)))


def fourier_design_matrix(theta: np.ndarray, degree: int) -> np.ndarray:
    columns = [np.ones(len(theta), dtype=float)]
    for order in range(1, degree + 1):
        columns.append(np.cos(order * theta))
        columns.append(np.sin(order * theta))
    return np.column_stack(columns)


def fit_weighted_fourier_series(
    theta: np.ndarray,
    values: np.ndarray,
    weights: np.ndarray,
    degree: int,
    ridge: float = 0.05,
) -> np.ndarray:
    design = fourier_design_matrix(theta, degree)
    sqrt_weights = np.sqrt(np.maximum(weights, 1e-9))
    weighted_design = design * sqrt_weights[:, None]
    weighted_values = values * sqrt_weights
    lhs = weighted_design.T @ weighted_design + np.eye(design.shape[1]) * ridge
    rhs = weighted_design.T @ weighted_values
    return np.linalg.solve(lhs, rhs)


def evaluate_fourier_series(theta: np.ndarray, coefficients: np.ndarray) -> np.ndarray:
    degree = (len(coefficients) - 1) // 2
    return fourier_design_matrix(theta, degree) @ coefficients


def approximate_von_mises_kappa(resultant_length: float) -> float:
    value = max(0.0, min(0.999, float(resultant_length)))
    if value < 1e-6:
        return 0.05
    if value < 0.53:
        kappa = 2 * value + value**3 + 5 * value**5 / 6
    elif value < 0.85:
        kappa = -0.4 + 1.39 * value + 0.43 / (1 - value)
    else:
        kappa = 1 / (value**3 - 4 * value**2 + 3 * value)
    return float(np.clip(kappa, 0.05, 10.0))


def log_von_mises(theta: np.ndarray, mean_angle: float, kappa: float) -> np.ndarray:
    return (
        float(kappa) * np.cos(theta - float(mean_angle))
        - math.log(2 * math.pi)
        - math.log(float(np.i0(float(kappa))))
    )


def fit_weighted_von_mises_mixture(
    theta: np.ndarray,
    weights: np.ndarray,
    component_count: int,
    iterations: int = 80,
) -> dict[str, np.ndarray]:
    weights = np.maximum(np.asarray(weights, dtype=float), 0)
    if not np.any(weights > 0):
        weights = np.ones(len(theta), dtype=float)
    bin_edges = np.linspace(0, 2 * math.pi, 73)
    histogram = np.zeros(72, dtype=float)
    bin_index = np.clip(np.digitize(theta, bin_edges) - 1, 0, len(histogram) - 1)
    for index, weight in zip(bin_index, weights):
        histogram[index] += float(weight)
    means = []
    for _component in range(component_count):
        peak = int(np.argmax(histogram))
        means.append((bin_edges[peak] + bin_edges[peak + 1]) * 0.5)
        for offset in range(-4, 5):
            histogram[(peak + offset) % len(histogram)] = 0

    means_array = np.asarray(means, dtype=float)
    mixture_weights = np.full(component_count, 1 / component_count, dtype=float)
    kappas = np.full(component_count, 1.5, dtype=float)

    for _iteration in range(iterations):
        component_logs = [
            math.log(max(float(weight), 1e-12)) + log_von_mises(theta, mean, kappa)
            for weight, mean, kappa in zip(mixture_weights, means_array, kappas)
        ]
        stacked = np.vstack(component_logs).T
        denominator = logsumexp_rows(stacked)
        responsibilities = np.exp(stacked - denominator[:, None])
        totals = (weights[:, None] * responsibilities).sum(axis=0) + 1e-9
        mixture_weights = totals / totals.sum()
        for component in range(component_count):
            component_weights = weights * responsibilities[:, component]
            cosine = float(np.sum(component_weights * np.cos(theta)))
            sine = float(np.sum(component_weights * np.sin(theta)))
            total = max(float(np.sum(component_weights)), 1e-9)
            means_array[component] = math.atan2(sine, cosine)
            kappas[component] = approximate_von_mises_kappa(math.hypot(cosine, sine) / total)

    return {
        "weights": mixture_weights,
        "means": means_array,
        "kappas": kappas,
    }


def log_von_mises_mixture(theta: np.ndarray, model: dict[str, np.ndarray]) -> np.ndarray:
    weights = model["weights"]
    means = model["means"]
    kappas = model["kappas"]
    component_logs = [
        math.log(max(float(weight), 1e-12)) + log_von_mises(theta, mean, kappa)
        for weight, mean, kappa in zip(weights, means, kappas)
    ]
    return logsumexp_rows(np.vstack(component_logs).T)


def disk_basis_from_core(
    core_covariance: np.ndarray,
    coefficients: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    normal = np.array([-float(coefficients[1]), -float(coefficients[2]), 1.0], dtype=float)
    normal /= np.linalg.norm(normal)
    values, vectors = np.linalg.eigh(positive_semidefinite(core_covariance[:2, :2]))
    order = np.argsort(values)[::-1]
    values = np.maximum(values[order], 0.05)
    vectors = vectors[:, order]
    lifted_axes = []
    for index in range(2):
        vector_xy = vectors[:, index]
        vector = np.array(
            [
                float(vector_xy[0]),
                float(vector_xy[1]),
                float(coefficients[1] * vector_xy[0] + coefficients[2] * vector_xy[1]),
            ],
            dtype=float,
        )
        vector = vector - normal * float(vector @ normal)
        vector /= np.linalg.norm(vector)
        lifted_axes.append(vector)
    first = lifted_axes[0]
    second = lifted_axes[1] - first * float(lifted_axes[1] @ first)
    second /= np.linalg.norm(second)
    return first, second, normal, np.sqrt(values)


def annular_coordinates(
    local: np.ndarray,
    center: np.ndarray,
    first_axis: np.ndarray,
    second_axis: np.ndarray,
    normal: np.ndarray,
    scale: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    delta = local - center
    first = delta @ first_axis / scale[0]
    second = delta @ second_axis / scale[1]
    radius = np.sqrt(first * first + second * second)
    angle = np.mod(np.arctan2(second, first), 2 * math.pi)
    height = delta @ normal
    return radius, angle, height


def angular_density_threshold(model: dict[str, np.ndarray], enclosed_mass: float, samples: int) -> tuple[np.ndarray, np.ndarray, float]:
    theta = np.linspace(0, 2 * math.pi, samples, endpoint=False)
    density = np.exp(log_von_mises_mixture(theta, model))
    dtheta = 2 * math.pi / samples
    order = np.argsort(density)[::-1]
    cumulative = np.cumsum(density[order] * dtheta)
    target = float(enclosed_mass) * float(cumulative[-1])
    index = int(np.searchsorted(cumulative, target, side="left"))
    return theta, density, float(density[order[min(index, len(order) - 1)]])


def annular_tube_point(
    center: np.ndarray,
    first_axis: np.ndarray,
    second_axis: np.ndarray,
    normal: np.ndarray,
    scale: np.ndarray,
    radius: float,
    theta: float,
    height: float,
) -> np.ndarray:
    return (
        center
        + first_axis * (float(scale[0]) * float(radius) * math.cos(float(theta)))
        + second_axis * (float(scale[1]) * float(radius) * math.sin(float(theta)))
        + normal * float(height)
    )


def tilted_disk_gmm_to_local_gaussians(
    coefficients: np.ndarray,
    scatter2: float,
    weights: np.ndarray,
    means_xy: np.ndarray,
    covariances_xy: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    beta = np.array([float(coefficients[1]), float(coefficients[2])], dtype=float)
    means = []
    covariances = []
    for mean_xy, covariance_xy in zip(means_xy, covariances_xy):
        z_mean = float(coefficients[0] + beta @ mean_xy)
        mean = np.array([float(mean_xy[0]), float(mean_xy[1]), z_mean], dtype=float)
        cross = covariance_xy @ beta
        covariance = np.zeros((3, 3), dtype=float)
        covariance[:2, :2] = covariance_xy
        covariance[:2, 2] = cross
        covariance[2, :2] = cross
        covariance[2, 2] = float(beta @ covariance_xy @ beta + scatter2)
        means.append(mean)
        covariances.append(positive_semidefinite(covariance))
    return np.asarray(weights, dtype=float), np.asarray(means, dtype=float), np.asarray(covariances, dtype=float)


def gaussian_mixture_density_volume(
    xs: np.ndarray,
    ys: np.ndarray,
    zs: np.ndarray,
    weights: np.ndarray,
    means: np.ndarray,
    covariances: np.ndarray,
) -> np.ndarray:
    density = np.zeros((len(xs), len(ys), len(zs)), dtype=float)
    for weight, mean, covariance in zip(weights, means, covariances):
        density += float(weight) * gaussian_density_volume(xs, ys, zs, mean, covariance)
    return density


def model_density_grid_bounds(local: np.ndarray, means: np.ndarray, covariances: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lower = np.quantile(local, 0.01, axis=0)
    upper = np.quantile(local, 0.99, axis=0)
    for mean, covariance in zip(means, covariances):
        values, vectors = np.linalg.eigh(positive_semidefinite(covariance))
        values = np.maximum(values, EIGEN_FLOOR)
        extent = np.sum(np.abs(vectors) * (np.sqrt(values) * 3.1)[None, :], axis=1)
        lower = np.minimum(lower, mean - extent)
        upper = np.maximum(upper, mean + extent)
    span = np.maximum(upper - lower, np.array([1.0, 1.0, 1.0]))
    padding = np.maximum(0.25, span * 0.06)
    return lower - padding, upper + padding


def fitted_mixture_density_volume(
    local: np.ndarray,
    weights: np.ndarray,
    means: np.ndarray,
    covariances: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    lower, upper = model_density_grid_bounds(local, means, covariances)
    nx, ny, nz = KDE3D_GRID_SHAPE
    xs = np.linspace(lower[0], upper[0], nx)
    ys = np.linspace(lower[1], upper[1], ny)
    zs = np.linspace(lower[2], upper[2], nz)
    density = gaussian_mixture_density_volume(xs, ys, zs, weights, means, covariances)
    return xs, ys, zs, density


def surface_segments_for_density_level(
    xs: np.ndarray,
    ys: np.ndarray,
    zs: np.ndarray,
    density: np.ndarray,
    level: float,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
    max_segments: int = KDE3D_ISOSURFACE_MAX_SEGMENTS,
) -> tuple[list[list[list[float | None]]], int, int, int]:
    cell_to_vertex, vertices = surface_net_vertices(xs, ys, zs, density, level)
    edge_set = surface_net_edge_set(density, level, cell_to_vertex)
    kept_edges = decimated_edges(edge_set, max_segments=max_segments)
    segments = [
        [
            rounded_vector(vector_from_local(vertices[first], origin, basis)),
            rounded_vector(vector_from_local(vertices[second], origin, basis)),
        ]
        for first, second in kept_edges
    ]
    return segments, len(vertices), len(edge_set), len(kept_edges)


def weighted_kde_at_points(
    local: np.ndarray,
    sigma: np.ndarray,
    weights: np.ndarray,
    bandwidth_scale: float = 1.18,
) -> tuple[np.ndarray, tuple[float, float, float]]:
    weights = np.maximum(np.asarray(weights, dtype=float), 0)
    if not np.any(weights > 0):
        weights = np.ones(len(local), dtype=float)
    _, std = weighted_mean_and_std(local, weights)
    std = np.maximum(std, np.array([0.35, 0.35, 0.35]))
    factor = max(8.0, effective_weight_count(weights)) ** (-1 / 7)
    hx = max(0.18, bandwidth_scale * float(std[0]) * factor)
    hy = max(0.18, bandwidth_scale * float(std[1]) * factor)
    hz_base = max(0.18, bandwidth_scale * float(std[2]) * factor)
    total_weight = float(np.sum(weights))
    densities = np.zeros(len(local), dtype=float)
    norm_xy = 1 / (2 * math.pi * hx * hy * math.sqrt(2 * math.pi))
    for start in range(0, len(local), 192):
        stop = min(len(local), start + 192)
        target = local[start:stop]
        density = np.zeros(len(target), dtype=float)
        for source_start in range(0, len(local), 192):
            source_stop = min(len(local), source_start + 192)
            source = local[source_start:source_stop]
            source_weights = weights[source_start:source_stop]
            hz = np.sqrt(hz_base * hz_base + np.maximum(sigma[source_start:source_stop], 0.05) ** 2)
            dx2 = ((target[:, None, 0] - source[None, :, 0]) / hx) ** 2
            dy2 = ((target[:, None, 1] - source[None, :, 1]) / hy) ** 2
            dz2 = ((target[:, None, 2] - source[None, :, 2]) / hz[None, :]) ** 2
            kernel = np.exp(-0.5 * (dx2 + dy2 + dz2)) / hz[None, :]
            density += (kernel * source_weights[None, :]).sum(axis=1) * norm_xy
        densities[start:stop] = density / max(total_weight, 1e-12)
    return np.maximum(densities, 1e-300), (hx, hy, hz_base)


def local_covariance_to_galactic(covariance: np.ndarray, basis: dict[str, np.ndarray]) -> np.ndarray:
    transform = np.column_stack([basis["east"], basis["north"], basis["radial"]])
    return transform @ covariance @ transform.T


def fit_lmc_cepheid_semiparametric_components(
    local: np.ndarray,
    position: np.ndarray,
    sigma: np.ndarray,
    basis: dict[str, np.ndarray],
) -> dict[str, object]:
    measurement = local_measurement_covariances(position, sigma, basis)
    median = np.median(local, axis=0)
    mad = np.median(np.abs(local - median), axis=0) * 1.4826
    mad = np.maximum(mad, np.array([0.4, 0.4, 0.4]))
    robust_distance = np.sqrt(np.sum(((local - median) / mad) ** 2, axis=1))
    cutoff = np.quantile(robust_distance, LMC_CEPHEID_INITIAL_MAIN_FRACTION)
    initial_main_weights = (robust_distance <= cutoff).astype(float)
    main_weights = initial_main_weights.copy()
    mean, covariance = weighted_eiv_gaussian(local, measurement, main_weights)
    residual_weights = 1 - main_weights
    prior_main = LMC_CEPHEID_MAIN_PRIOR

    for _iteration in range(LMC_CEPHEID_EM_ITERATIONS):
        log_main = log_gaussian_eiv_local(local, measurement, mean, covariance)
        residual_density, bandwidth = weighted_kde_at_points(local, sigma, residual_weights)
        log_residual = np.log(residual_density)
        log_main_prior = math.log(max(prior_main, 1e-6)) + log_main
        log_residual_prior = math.log(max(1 - prior_main, 1e-6)) + log_residual
        max_log = np.maximum(log_main_prior, log_residual_prior)
        denominator = max_log + np.log(np.exp(log_main_prior - max_log) + np.exp(log_residual_prior - max_log))
        next_main_weights = np.exp(log_main_prior - denominator)
        # Keep the main body robust: stars in the distant likelihood tails should not pull the ellipsoid.
        inverse = np.linalg.inv(positive_semidefinite(covariance))
        mahalanobis = np.einsum("ni,ij,nj->n", local - mean, inverse, local - mean)
        student_weight = (6 + 3) / (6 + np.maximum(mahalanobis, 0))
        regularized_main_weights = 0.78 * next_main_weights + 0.22 * initial_main_weights
        fit_weights = regularized_main_weights * np.clip(student_weight, 0.25, 1.25)
        next_mean, next_covariance = weighted_eiv_gaussian(local, measurement, fit_weights)
        shift = float(np.linalg.norm(next_mean - mean))
        mean, covariance = next_mean, next_covariance
        main_weights = next_main_weights
        residual_weights = 1 - main_weights
        if shift < 0.005:
            break

    entropy = -(
        main_weights * np.log(np.clip(main_weights, 1e-9, 1))
        + residual_weights * np.log(np.clip(residual_weights, 1e-9, 1))
    )
    _, residual_bandwidth = weighted_kde_at_points(local, sigma, residual_weights)
    return {
        "mean": mean,
        "covariance": covariance,
        "mainWeights": main_weights,
        "residualWeights": residual_weights,
        "mainFraction": float(np.mean(main_weights)),
        "effectiveResidualCount": effective_weight_count(residual_weights),
        "membershipEntropy": float(np.mean(entropy)),
        "uncertainMembershipFraction": float(np.mean((main_weights > 0.25) & (main_weights < 0.75))),
        "residualBandwidth": residual_bandwidth,
    }


def residual_density_for_target_mass(
    xs: np.ndarray,
    ys: np.ndarray,
    zs: np.ndarray,
    kde_density: np.ndarray,
    main_density: np.ndarray,
    target_mass: float,
) -> tuple[np.ndarray, float, float]:
    kde_density = normalized_volume_density(xs, ys, zs, kde_density)
    main_density = normalized_volume_density(xs, ys, zs, main_density)
    volume = cell_volume(xs, ys, zs)

    def residual_mass(scale: float) -> float:
        return float(np.maximum(kde_density - scale * main_density, 0).sum() * volume)

    low = 0.0
    high = 1.0
    while residual_mass(high) > target_mass and high < 64:
        high *= 2
    for _iteration in range(50):
        mid = (low + high) * 0.5
        if residual_mass(mid) > target_mass:
            low = mid
        else:
            high = mid
    scale = (low + high) * 0.5
    residual = np.maximum(kde_density - scale * main_density, 0)
    mass = float(residual.sum() * volume)
    return residual, scale, mass


def build_lmc_cepheid_two_ellipsoids(
    payload: dict[str, object],
    indexes: dict[str, int],
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> list[dict[str, object]]:
    arrays = subset_arrays(payload, indexes, "cepheids", "lmc")
    local = arrays["local"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    position = arrays["position"]  # type: ignore[assignment]
    measurement = local_measurement_covariances(position, sigma, basis)
    local_mean = np.mean(local, axis=0)
    centered = local - local_mean
    sigma_z = np.sqrt(np.maximum(measurement[:, 2, 2], 1e-6))
    coefficients, scatter2 = fit_surface_params(centered, sigma_z, "tilted-plane")
    inplane = fit_eiv_gaussian_mixture_2d(
        centered[:, :2],
        measurement[:, :2, :2],
        LMC_CEPHEID_DISK_GMM_COMPONENTS,
        seed=20260514 + LMC_CEPHEID_DISK_GMM_COMPONENTS * 31,
    )
    inplane_weights = inplane["weights"]  # type: ignore[assignment]
    inplane_means = inplane["means"]  # type: ignore[assignment]
    inplane_covariances = inplane["covariances"]  # type: ignore[assignment]
    weights, means, covariances = tilted_disk_gmm_to_local_gaussians(
        coefficients,
        scatter2,
        inplane_weights,
        inplane_means,
        inplane_covariances,
    )
    disk_log_likelihood = float(log_eiv_mixture_local(centered, measurement, weights, means, covariances).sum())
    disk_parameter_count = 4 + LMC_CEPHEID_DISK_GMM_COMPONENTS * 5 + LMC_CEPHEID_DISK_GMM_COMPONENTS - 1
    disk_aic = 2 * disk_parameter_count - 2 * disk_log_likelihood
    disk_bic = disk_parameter_count * math.log(len(centered)) - 2 * disk_log_likelihood
    inplane_log_density = log_eiv_mixture_2d(
        centered[:, :2],
        measurement[:, :2, :2],
        inplane_weights,
        inplane_means,
        inplane_covariances,
    )
    density_cut = float(np.quantile(inplane_log_density, LMC_CEPHEID_CORE_DENSITY_QUANTILE))
    density_scale = max(0.12, float(np.std(inplane_log_density)) * 0.10)
    core_weights = 1 / (1 + np.exp(-np.clip((inplane_log_density - density_cut) / density_scale, -50, 50)))
    core_mean, core_covariance = weighted_eiv_gaussian(centered, measurement, core_weights)

    ring_axis_1, ring_axis_2, ring_normal, ring_scale = disk_basis_from_core(core_covariance, coefficients)
    annular_radius, annular_angle, annular_height = annular_coordinates(
        centered,
        core_mean,
        ring_axis_1,
        ring_axis_2,
        ring_normal,
        ring_scale,
    )
    density_floor = float(np.quantile(inplane_log_density, 0.08))
    ring_weights = (
        (1 - core_weights)
        * sigmoid_array((annular_radius - 1.2) / 0.18)
        * sigmoid_array((inplane_log_density - density_floor) / 0.25)
    )
    ring_radius_coefficients = fit_weighted_fourier_series(
        annular_angle,
        annular_radius,
        ring_weights,
        LMC_CEPHEID_RING_FOURIER_DEGREE,
    )
    ring_center_radius_at_star = np.maximum(evaluate_fourier_series(annular_angle, ring_radius_coefficients), 0.3)
    ring_radial_sigma = math.sqrt(
        max(float(np.average((annular_radius - ring_center_radius_at_star) ** 2, weights=ring_weights)), 0.03)
    )
    ring_vertical_sigma = math.sqrt(max(float(np.average(annular_height * annular_height, weights=ring_weights)), 0.03))
    angular_model = fit_weighted_von_mises_mixture(
        annular_angle,
        ring_weights,
        LMC_CEPHEID_RING_ANGULAR_COMPONENTS,
    )
    theta_samples, angular_density, angular_threshold = angular_density_threshold(
        angular_model,
        LMC_CEPHEID_RING_ANGULAR_MASS,
        LMC_CEPHEID_RING_RENDER_SAMPLES,
    )
    active_theta = angular_density >= angular_threshold

    def tube_radius(theta: float, sigma_offset: float) -> float:
        center_radius = float(evaluate_fourier_series(np.array([theta], dtype=float), ring_radius_coefficients)[0])
        radius = center_radius + sigma_offset * ring_radial_sigma
        return max(LMC_CEPHEID_RING_MIN_RADIUS, radius)

    def tube_point(theta: float, sigma_offset: float, height_offset: float) -> np.ndarray:
        return local_mean + annular_tube_point(
            core_mean,
            ring_axis_1,
            ring_axis_2,
            ring_normal,
            ring_scale,
            tube_radius(theta, sigma_offset),
            theta,
            height_offset * ring_vertical_sigma,
        )

    ring_segments = []
    radial_offsets = (LMC_CEPHEID_RING_INNER_SIGMA, LMC_CEPHEID_RING_OUTER_SIGMA)
    height_offsets = (-1.0, 1.0)
    for index, theta in enumerate(theta_samples):
        next_index = (index + 1) % len(theta_samples)
        next_theta = theta_samples[next_index]
        if active_theta[index] and active_theta[next_index]:
            for radial_offset in radial_offsets:
                ring_segments.append(
                    [
                        rounded_vector(vector_from_local(tube_point(theta, radial_offset, 0.0), origin, basis)),
                        rounded_vector(vector_from_local(tube_point(next_theta, radial_offset, 0.0), origin, basis)),
                    ]
                )
            for height_offset in height_offsets:
                ring_segments.append(
                    [
                        rounded_vector(vector_from_local(tube_point(theta, 0.0, height_offset), origin, basis)),
                        rounded_vector(vector_from_local(tube_point(next_theta, 0.0, height_offset), origin, basis)),
                    ]
                )
            if index % 32 == 0:
                ring_segments.append(
                    [
                        rounded_vector(vector_from_local(tube_point(theta, radial_offsets[0], 0.0), origin, basis)),
                        rounded_vector(vector_from_local(tube_point(theta, radial_offsets[1], 0.0), origin, basis)),
                    ]
                )
                ring_segments.append(
                    [
                        rounded_vector(vector_from_local(tube_point(theta, 0.0, height_offsets[0]), origin, basis)),
                        rounded_vector(vector_from_local(tube_point(theta, 0.0, height_offsets[1]), origin, basis)),
                    ]
                )
        if active_theta[index] and (not active_theta[next_index] or not active_theta[(index - 1) % len(theta_samples)]):
            ring_segments.append(
                [
                    rounded_vector(vector_from_local(tube_point(theta, radial_offsets[0], 0.0), origin, basis)),
                    rounded_vector(vector_from_local(tube_point(theta, radial_offsets[1], 0.0), origin, basis)),
                ]
            )
            ring_segments.append(
                [
                    rounded_vector(vector_from_local(tube_point(theta, 0.0, height_offsets[0]), origin, basis)),
                    rounded_vector(vector_from_local(tube_point(theta, 0.0, height_offsets[1]), origin, basis)),
                ]
            )

    outlier_weights = np.clip(1 - core_weights - ring_weights, 0, 1)
    outlier_mean, outlier_covariance = weighted_eiv_gaussian(centered, measurement, outlier_weights)
    outlier_covariance = positive_semidefinite(outlier_covariance * 6.0)

    gmm_candidates = fit_eiv_gmm_model_selection(local, measurement)
    student_t = fit_student_t_ellipsoid(local, measurement)
    student_t_plus_gaussian = fit_student_t_body_gaussian_tail(local, measurement, gmm_candidates)
    best_bic = min(
        disk_bic,
        *(float(candidate["bic"]) for candidate in gmm_candidates),
        float(student_t["bic"]),
        float(student_t_plus_gaussian["bic"]),
    )
    model_comparison = [
        {
            "model": f"tilted-disk-inplane-eiv-gmm-{LMC_CEPHEID_DISK_GMM_COMPONENTS}",
            "components": LMC_CEPHEID_DISK_GMM_COMPONENTS,
            "basisRole": "in-plane surface-density basis functions, not separate stellar populations",
            "logLikelihood": round_number(disk_log_likelihood, 2),
            "aic": round_number(disk_aic, 2),
            "bic": round_number(disk_bic, 2),
            "deltaBic": round_number(disk_bic - best_bic, 2),
            "iterations": int(inplane["iterations"]),
            "converged": bool(inplane["converged"]),
        },
        *[
        {
            "model": f"eiv-gmm-{int(candidate['componentCount'])}",
            "components": int(candidate["componentCount"]),
            "logLikelihood": round_number(float(candidate["logLikelihood"]), 2),
            "aic": round_number(float(candidate["aic"]), 2),
            "bic": round_number(float(candidate["bic"]), 2),
            "deltaBic": round_number(float(candidate["bic"]) - best_bic, 2),
            "iterations": int(candidate["iterations"]),
            "converged": bool(candidate["converged"]),
        }
        for candidate in gmm_candidates
        ],
    ]
    model_comparison.extend(
        [
            {
                "model": "student-t-ellipsoid",
                "components": 1,
                "degreesOfFreedom": round_number(float(student_t["degreesOfFreedom"]), 3),
                "logLikelihood": round_number(float(student_t["logLikelihood"]), 2),
                "aic": round_number(float(student_t["aic"]), 2),
                "bic": round_number(float(student_t["bic"]), 2),
                "deltaBic": round_number(float(student_t["bic"]) - best_bic, 2),
                "iterations": int(student_t["iterations"]),
                "converged": bool(student_t["converged"]),
            },
            {
                "model": "student-t-primary-gaussian-secondary",
                "components": 2,
                "degreesOfFreedom": round_number(float(student_t_plus_gaussian["degreesOfFreedom"]), 3),
                "logLikelihood": round_number(float(student_t_plus_gaussian["logLikelihood"]), 2),
                "aic": round_number(float(student_t_plus_gaussian["aic"]), 2),
                "bic": round_number(float(student_t_plus_gaussian["bic"]), 2),
                "deltaBic": round_number(float(student_t_plus_gaussian["bic"]) - best_bic, 2),
                "iterations": int(student_t_plus_gaussian["iterations"]),
                "converged": bool(student_t_plus_gaussian["converged"]),
            },
        ]
    )
    model_comparison.sort(key=lambda item: float(item["bic"]))  # type: ignore[arg-type]

    two_component = next(candidate for candidate in gmm_candidates if int(candidate["componentCount"]) == 2)
    component_weights = np.asarray(two_component["weights"], dtype=float)
    component_means = np.asarray(two_component["means"], dtype=float)
    component_covariances = np.asarray(two_component["covariances"], dtype=float)
    responsibilities = np.asarray(two_component["responsibilities"], dtype=float)
    order = np.argsort(component_weights)[::-1]

    structures = []
    for display_index, component_index in enumerate(order):
        covariance = component_covariances[component_index]
        axis_sigma, _axis_vectors, los_cosine, sky_area = ellipsoid_axis_metrics(covariance)
        soft_count = float(np.sum(responsibilities[:, component_index]))
        is_primary = display_index == 0
        label = "LMC Cepheids primary" if is_primary else "LMC Cepheids secondary"
        extra: dict[str, object] = {
            "componentRole": "main" if is_primary else "secondary",
            "structureModel": "eiv-gmm-2-component-ellipsoid",
            "sourceModel": "eiv-gmm-2",
            "mixtureWeight": round_number(float(component_weights[component_index]), 4),
            "softMembershipCount": round_number(soft_count, 1),
            "componentIndex": int(component_index),
            "axisKpc68": [round_number(value, 3) for value in axis_sigma],
            "lineOfSightMajorAxisCosine": round_number(los_cosine, 4),
            "projectedSkyAreaKpc2": round_number(sky_area, 4),
            "medianDistanceErrorKpc": round_number(float(np.median(sigma)), 3),
            "uncertaintyTreatment": "distance errors are projected into local measurement covariance; ellipsoid covariance is intrinsic EIV covariance from a two-component Gaussian mixture",
        }
        if is_primary:
            extra["modelComparison"] = model_comparison
            extra["selectionNote"] = (
                "Displayed as a simple two-ellipsoid summary. "
                "The more flexible tilted-disk density model remains favored by BIC, but this representation is easier to read."
            )
        structures.append(
            ellipsoid_payload(
                "cepheids",
                "lmc",
                vector_from_local(component_means[component_index], origin, basis),
                local_covariance_to_galactic(covariance, basis),
                int(round(soft_count)),
                label=label,
                alpha=0.78 if is_primary else 0.74,
                line_width=1.08 if is_primary else 1.02,
                line_dash=MAIN_COMPONENT_LINE_DASH if is_primary else SECONDARY_COMPONENT_LINE_DASH,
                extra=extra,
            )
        )
    return structures


def build_lmc_cepheid_bar_disk(
    payload: dict[str, object],
    indexes: dict[str, int],
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> list[dict[str, object]]:
    arrays = subset_arrays(payload, indexes, "cepheids", "lmc")
    local = arrays["local"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    position = arrays["position"]  # type: ignore[assignment]
    rows = arrays["rows"]  # type: ignore[assignment]
    measurement = local_measurement_covariances(position, sigma, basis)
    sigma_z = np.sqrt(np.maximum(measurement[:, 2, 2], 1e-6))
    ripepi_bar_mask = lmc_cepheid_ripepi_bar_mask(rows, indexes)
    best, model_comparison = fit_lmc_cepheid_bar_disk_model_selection(local, measurement, ripepi_bar_mask)
    bar_responsibility = np.clip(best["responsibilities"], 0, 1)  # type: ignore[arg-type]
    disk_responsibility = 1 - bar_responsibility
    hard_bar_mask = bar_responsibility >= 0.5
    hard_disk_mask = ~hard_bar_mask
    disk_rows = [row for row, selected in zip(rows, hard_disk_mask) if selected]
    bar_rows = [row for row, selected in zip(rows, hard_bar_mask) if selected]
    disk_params = best["diskParams"]  # type: ignore[assignment]
    selected_model = str(best["model"])
    selected_summary = {
        "model": selected_model,
        "surfaceModel": best["surfaceModel"],
        "diskComponentCount": best["diskComponentCount"],
        "fixedMembership": best["fixedMembership"],
        "logLikelihood": round_number(float(best["logLikelihood"]), 3),
        "parameters": int(best["parameterCount"]),
        "bic": round_number(float(best["bic"]), 3),
        "aic": round_number(float(best["aic"]), 3),
        "iterations": int(best["iterations"]),
        "converged": bool(best["converged"]),
    }

    disk_mean, disk_covariance = lmc_cepheid_disk_model_moments(disk_params)
    disk_axis_sigma, _disk_axis_vectors, disk_los_cosine, disk_sky_area = ellipsoid_axis_metrics(disk_covariance)
    disk = ellipsoid_payload(
        "cepheids",
        "lmc",
        vector_from_local(disk_mean, origin, basis),
        local_covariance_to_galactic(disk_covariance, basis),
        int(round(float(disk_responsibility.sum()))),
        label="LMC Cepheids disk",
        alpha=0.68,
        line_width=1.12,
        line_dash=MAIN_COMPONENT_LINE_DASH,
        extra={
            "componentRole": "disk",
            "hoverAlpha": 0.96,
            "hoverLineWidth": 2.15,
            "pickRadiusPx": 9,
            "structureModel": "joint-em-moment-matched-3d-thick-disk-ellipsoid",
            "displayModel": "single 3-D moment-matched thick-disk ellipsoid from the fitted disk component",
            "sourceModel": selected_model,
            "selectedModel": selected_summary,
            "modelComparison": model_comparison,
            "softMembershipCount": round_number(float(disk_responsibility.sum()), 1),
            "hardMembershipCount": int(hard_disk_mask.sum()),
            "ripepiPolygonSeedCount": int(ripepi_bar_mask.sum()),
            "barPolygonRaDecDeg": [[round_number(ra, 3), round_number(dec, 3)] for ra, dec in LMC_CEPHEID_RIPEPI_BAR_POLYGON_RA_DEC],
            "selectionNote": (
                "The Ripepi et al. eastern-bar polygon is used only to initialize the bar component. "
                "Displayed disk is the moment-matched 3-D envelope of the fitted disk component, so in-plane GMM saddles are not rendered as physical holes."
            ),
            "distanceUncertaintyTreatment": (
                "published distance errors are projected into local covariance; disk scoring uses the in-plane EIV covariance "
                "and the line-of-sight projected variance in the conditional thickness model"
            ),
            "inPlaneGaussianWeights": [round_number(float(value), 4) for value in disk_params["inplaneWeights"]],  # type: ignore[index]
            "inPlaneGaussianCount": int(best["diskComponentCount"]),
            "surfaceModel": best["surfaceModel"],
            "intrinsicScatterKpc": round_number(math.sqrt(float(disk_params["scatter2"])), 3),
            "axisKpc68": [round_number(value, 3) for value in disk_axis_sigma],
            "lineOfSightMajorAxisCosine": round_number(disk_los_cosine, 4),
            "projectedSkyAreaKpc2": round_number(disk_sky_area, 4),
            "modeCounts": mode_counts(disk_rows, indexes),
            "medianDistanceErrorKpc": round_number(float(np.median(sigma[hard_disk_mask])), 3) if int(hard_disk_mask.sum()) else None,
        },
    )

    bar_mean = best["barMean"]  # type: ignore[assignment]
    bar_covariance = best["barCovariance"]  # type: ignore[assignment]
    axis_sigma, _axis_vectors, los_cosine, sky_area = ellipsoid_axis_metrics(bar_covariance)
    bar = ellipsoid_payload(
        "cepheids",
        "lmc",
        vector_from_local(bar_mean, origin, basis),
        local_covariance_to_galactic(bar_covariance, basis),
        int(round(float(bar_responsibility.sum()))),
        label="LMC Cepheids bar",
        alpha=0.9,
        line_width=1.45,
        line_dash=MAIN_COMPONENT_LINE_DASH,
        extra={
            "componentRole": "bar",
            "hoverAlpha": 0.98,
            "hoverLineWidth": 2.55,
            "pickRadiusPx": 9,
            "structureModel": "joint-em-eiv-bar-ellipsoid",
            "sourceModel": selected_model,
            "selectedModel": selected_summary,
            "selectionRegion": "soft posterior bar membership; initialized from the Ripepi VMC eastern-bar polygon",
            "barPolygonRaDecDeg": [[round_number(ra, 3), round_number(dec, 3)] for ra, dec in LMC_CEPHEID_RIPEPI_BAR_POLYGON_RA_DEC],
            "softMembershipCount": round_number(float(bar_responsibility.sum()), 1),
            "hardMembershipCount": int(hard_bar_mask.sum()),
            "ripepiPolygonSeedCount": int(ripepi_bar_mask.sum()),
            "axisKpc68": [round_number(value, 3) for value in axis_sigma],
            "lineOfSightMajorAxisCosine": round_number(los_cosine, 4),
            "projectedSkyAreaKpc2": round_number(sky_area, 4),
            "modeCounts": mode_counts(bar_rows, indexes),
            "medianDistanceErrorKpc": round_number(float(np.median(sigma[hard_bar_mask])), 3) if int(hard_bar_mask.sum()) else None,
            "uncertaintyTreatment": (
                "distance errors are projected into full local measurement covariance; bar covariance is an intrinsic EIV covariance "
                "estimated from soft posterior memberships"
            ),
        },
    )
    return [disk, bar]


def build_plane_structure(
    payload: dict[str, object],
    indexes: dict[str, int],
    population_id: str,
    cloud_id: str,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> dict[str, object]:
    arrays = subset_arrays(payload, indexes, population_id, cloud_id)
    local = arrays["local"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    local_mean = local.mean(axis=0)
    centered = local - local_mean
    model = "tilted-plane"
    coefficients, scatter2 = fit_surface_params(centered, sigma, model)
    x_min, x_max = np.quantile(centered[:, 0], PLANE_QUANTILE_RANGE)
    y_min, y_max = np.quantile(centered[:, 1], PLANE_QUANTILE_RANGE)
    x_values = np.linspace(x_min, x_max, PLANE_GRID_LINES)
    y_values = np.linspace(y_min, y_max, PLANE_GRID_LINES)
    segments = []
    segments.append(line_segment_vectors((x_min, y_min), (x_max, y_min), coefficients, model, local_mean, origin, basis))
    segments.append(line_segment_vectors((x_max, y_min), (x_max, y_max), coefficients, model, local_mean, origin, basis))
    segments.append(line_segment_vectors((x_max, y_max), (x_min, y_max), coefficients, model, local_mean, origin, basis))
    segments.append(line_segment_vectors((x_min, y_max), (x_min, y_min), coefficients, model, local_mean, origin, basis))
    for x in x_values[1:-1]:
        segments.append(line_segment_vectors((x, y_min), (x, y_max), coefficients, model, local_mean, origin, basis))
    for y in y_values[1:-1]:
        segments.append(line_segment_vectors((x_min, y), (x_max, y), coefficients, model, local_mean, origin, basis))
    label_local = local_mean + np.array(
        [
            x_min + 0.68 * (x_max - x_min),
            y_min + 0.62 * (y_max - y_min),
            plane_z(coefficients, x_min + 0.68 * (x_max - x_min), y_min + 0.62 * (y_max - y_min), model),
        ]
    )
    population = POPULATIONS[population_id]
    cloud = CLOUDS[cloud_id]
    label_noun = "plane" if cloud_id == "lmc" else "sheet"
    return {
        "type": "plane",
        "id": f"{population_id}-{cloud_id}-{label_noun}",
        "label": f"{population['label']} {cloud['label']} {label_noun}",
        "populationId": population_id,
        "cloudId": cloud_id,
        "count": len(arrays["rows"]),  # type: ignore[arg-type]
        "color": population["color"],
        "lineDash": cloud["lineDash"],
        "alpha": 0.78,
        "lineWidth": 1.05,
        "structureModel": model,
        "intrinsicScatterKpc": round_number(math.sqrt(float(scatter2)), 3),
        "xExtentKpc": [round_number(x_min, 3), round_number(x_max, 3)],
        "yExtentKpc": [round_number(y_min, 3), round_number(y_max, 3)],
        "coefficients": [round_number(value, 6) for value in coefficients],
        "segments": segments,
        "labelVector": rounded_vector(vector_from_local(label_local, origin, basis)),
    }


def build_rrlyrae_components(
    payload: dict[str, object],
    indexes: dict[str, int],
    cloud_id: str,
) -> list[dict[str, object]]:
    arrays = subset_arrays(payload, indexes, "rrlyrae", cloud_id)
    params = fit_gaussian_mixture(
        arrays["position"],  # type: ignore[arg-type]
        arrays["measurement"],  # type: ignore[arg-type]
        2,
        seed=2213 if cloud_id == "lmc" else 3319,
    )
    order = np.argsort(params["weights"])[::-1]
    structures = []
    for output_index, component_index in enumerate(order):
        weight = float(params["weights"][component_index])
        label = f"RR Lyrae {CLOUDS[cloud_id]['label']} {'main' if output_index == 0 else 'secondary'}"
        structures.append(
            ellipsoid_payload(
                "rrlyrae",
                cloud_id,
                params["means"][component_index],
                params["covariances"][component_index],
                int(round(weight * len(arrays["rows"]))),  # type: ignore[arg-type]
                label=label,
                alpha=0.78 if output_index == 0 else 0.58,
                line_width=1.08 if output_index == 0 else 0.92,
                extra={
                    "structureModel": "2-component-gaussian-mixture",
                    "componentIndex": int(output_index),
                    "componentWeight": round_number(weight, 4),
                },
            )
        )
    return structures


def build_population_components(
    payload: dict[str, object],
    indexes: dict[str, int],
    population_id: str,
    cloud_id: str,
    component_count: int,
    seed: int,
) -> list[dict[str, object]]:
    arrays = subset_arrays(payload, indexes, population_id, cloud_id)
    params = fit_gaussian_mixture(
        arrays["position"],  # type: ignore[arg-type]
        arrays["measurement"],  # type: ignore[arg-type]
        component_count,
        seed=seed,
    )
    order = np.argsort(params["weights"])[::-1]
    structures = []
    for output_index, component_index in enumerate(order):
        weight = float(params["weights"][component_index])
        population = POPULATIONS[population_id]
        cloud = CLOUDS[cloud_id]
        visible_label = f"{population['label']} {cloud['label']}" if output_index == 0 else None
        structures.append(
            ellipsoid_payload(
                population_id,
                cloud_id,
                params["means"][component_index],
                params["covariances"][component_index],
                int(round(weight * len(arrays["rows"]))),  # type: ignore[arg-type]
                label=visible_label or f"{population['label']} {cloud['label']} component {output_index + 1}",
                alpha=max(0.38, 0.78 - output_index * 0.13),
                line_width=max(0.82, 1.08 - output_index * 0.08),
                extra={
                    "label": visible_label,
                    "structureModel": f"{component_count}-component-gaussian-mixture",
                    "componentIndex": int(output_index),
                    "componentWeight": round_number(weight, 4),
                },
            )
        )
    return structures


def build_rrlyrae_shells(
    payload: dict[str, object],
    indexes: dict[str, int],
    cloud_id: str,
) -> list[dict[str, object]]:
    arrays = subset_arrays(payload, indexes, "rrlyrae", cloud_id)
    params = fit_single_gaussian(arrays["position"], arrays["measurement"])  # type: ignore[arg-type]
    mean = params["means"][0]
    covariance = params["covariances"][0]
    inverse = np.linalg.inv(positive_semidefinite(covariance))
    delta = arrays["position"] - mean  # type: ignore[operator]
    mahalanobis = np.einsum("ni,ij,nj->n", delta, inverse, delta)
    structures = []
    for index, containment in enumerate(RR_SHELL_CONTAINMENT):
        radius_scale = math.sqrt(float(np.quantile(mahalanobis, containment)))
        label = f"RR Lyrae {CLOUDS[cloud_id]['label']} {'inner' if index == 0 else 'outer'}"
        structures.append(
            ellipsoid_payload(
                "rrlyrae",
                cloud_id,
                mean,
                covariance * radius_scale * radius_scale / (CONFIDENCE_RADIUS * CONFIDENCE_RADIUS),
                int(round(containment * len(arrays["rows"]))),  # type: ignore[arg-type]
                label=label,
                alpha=0.72 if index == 0 else 0.48,
                line_width=1.08 if index == 0 else 0.9,
                extra={
                    "structureModel": "nested-triaxial-density-shell",
                    "containment": round_number(containment, 3),
                    "empiricalMahalanobisRadius": round_number(radius_scale, 3),
                },
            )
        )
    return structures


def build_eiv_gmm_body_envelope(
    payload: dict[str, object],
    indexes: dict[str, int],
    population_id: str,
    cloud_id: str,
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
    *,
    body_label: str,
    envelope_label: str,
    body_selection: str,
    body_structure_model: str,
    envelope_structure_model: str,
    body_alpha: float = 0.82,
    envelope_alpha: float = 0.44,
) -> list[dict[str, object]]:
    arrays = subset_arrays(payload, indexes, population_id, cloud_id)
    local = arrays["local"]  # type: ignore[assignment]
    position = arrays["position"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    measurement = local_measurement_covariances(position, sigma, basis)

    candidates = fit_eiv_gmm_model_selection(local, measurement)
    best = min(candidates, key=lambda candidate: float(candidate["bic"]))
    weights = best["weights"]  # type: ignore[assignment]
    means = best["means"]  # type: ignore[assignment]
    covariances = best["covariances"]  # type: ignore[assignment]
    responsibilities = best["responsibilities"]  # type: ignore[assignment]
    model_comparison = [
        {
            "components": int(candidate["componentCount"]),
            "logLikelihood": round_number(float(candidate["logLikelihood"]), 2),
            "aic": round_number(float(candidate["aic"]), 2),
            "bic": round_number(float(candidate["bic"]), 2),
            "deltaBic": round_number(float(candidate["bic"]) - float(best["bic"]), 2),
            "iterations": int(candidate["iterations"]),
            "converged": bool(candidate["converged"]),
        }
        for candidate in candidates
    ]

    metrics = [ellipsoid_axis_metrics(covariance) for covariance in covariances]
    if body_selection == "dominant":
        body_index = int(np.argmax(weights))
    elif body_selection == "compact-los":
        body_index = min(
            range(len(weights)),
            key=lambda index: metrics[index][3] / max(metrics[index][2], 0.2),
        )
    else:
        body_index = min(range(len(weights)), key=lambda index: metrics[index][3])

    body_mean = means[body_index]
    body_covariance = covariances[body_index]
    body_weights = responsibilities[:, body_index]
    body_axes, _body_vectors, los_major_axis_cosine, body_sky_area = metrics[body_index]

    nonbody_component_weights = [
        round_number(float(weight), 4)
        for index, weight in enumerate(weights)
        if index != body_index
    ]
    body = ellipsoid_payload(
        population_id,
        cloud_id,
        vector_from_local(body_mean, origin, basis),
        local_covariance_to_galactic(body_covariance, basis),
        int(round(float(body_weights.sum()))),
        label=body_label,
        alpha=body_alpha,
        line_width=1.12,
        extra={
            "componentRole": "main",
            "structureModel": body_structure_model,
            "bodySelection": body_selection,
            "mixtureComponents": int(best["componentCount"]),
            "mixtureWeight": round_number(float(weights[body_index]), 4),
            "softMembershipCount": round_number(float(body_weights.sum()), 1),
            "kishEffectiveSampleSize": round_number(effective_weight_count(body_weights), 1),
            "lineOfSightMajorAxisCosine": round_number(los_major_axis_cosine, 4),
            "projectedSkyAreaKpc2": round_number(body_sky_area, 4),
            "medianDistanceErrorKpc": round_number(float(np.median(sigma)), 3),
            "uncertaintyTreatment": "distance errors included as measurement covariance; wireframe covariance is intrinsic EIV covariance",
            "modelComparison": model_comparison,
            "componentWeights": [round_number(float(weight), 4) for weight in weights],
            "bodyComponentIndex": int(body_index),
        },
    )
    structures = [body]

    if len(weights) > 1:
        envelope_weights = np.maximum(1 - body_weights, 0)
        envelope_mean, envelope_covariance = weighted_eiv_gaussian(local, measurement, envelope_weights)
        envelope_inverse = np.linalg.inv(positive_semidefinite(envelope_covariance))
        envelope_mahalanobis = np.einsum(
            "ni,ij,nj->n",
            local - envelope_mean,
            envelope_inverse,
            local - envelope_mean,
        )
        envelope_scale = (
            math.sqrt(weighted_quantile(envelope_mahalanobis, envelope_weights, EIV_GMM_ENVELOPE_CONTAINMENT))
            / CONFIDENCE_RADIUS
        )
        structures.append(
            ellipsoid_payload(
                population_id,
                cloud_id,
                vector_from_local(envelope_mean, origin, basis),
                local_covariance_to_galactic(envelope_covariance * envelope_scale * envelope_scale, basis),
                int(round(float(envelope_weights.sum()))),
                label=envelope_label,
                alpha=envelope_alpha,
                line_width=0.9,
                line_dash=SECONDARY_COMPONENT_LINE_DASH,
                extra={
                    "componentRole": "secondary",
                    "structureModel": envelope_structure_model,
                    "containment": round_number(EIV_GMM_ENVELOPE_CONTAINMENT, 3),
                    "summarizedMixtureComponents": int(best["componentCount"]) - 1,
                    "nonBodyComponentWeights": nonbody_component_weights,
                    "bodyMembershipWeightFraction": round_number(float(body_weights.sum() / len(body_weights)), 4),
                },
            )
        )
    return structures


def build_smc_cepheid_student_t_body_tail(
    payload: dict[str, object],
    indexes: dict[str, int],
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> list[dict[str, object]]:
    arrays = subset_arrays(payload, indexes, "cepheids", "smc")
    local = arrays["local"]  # type: ignore[assignment]
    position = arrays["position"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    measurement = local_measurement_covariances(position, sigma, basis)
    gmm_candidates = fit_eiv_gmm_model_selection(local, measurement)
    model = fit_student_t_body_gaussian_tail(local, measurement, gmm_candidates)
    best_bic = min(float(model["bic"]), *(float(candidate["bic"]) for candidate in gmm_candidates))
    model_comparison = [
        {
            "model": f"eiv-gmm-{int(candidate['componentCount'])}",
            "components": int(candidate["componentCount"]),
            "logLikelihood": round_number(float(candidate["logLikelihood"]), 2),
            "aic": round_number(float(candidate["aic"]), 2),
            "bic": round_number(float(candidate["bic"]), 2),
            "deltaBic": round_number(float(candidate["bic"]) - best_bic, 2),
            "iterations": int(candidate["iterations"]),
            "converged": bool(candidate["converged"]),
        }
        for candidate in gmm_candidates
    ]
    model_comparison.append(
        {
            "model": "student-t-primary-gaussian-secondary",
            "components": 2,
            "degreesOfFreedom": round_number(float(model["degreesOfFreedom"]), 3),
            "logLikelihood": round_number(float(model["logLikelihood"]), 2),
            "aic": round_number(float(model["aic"]), 2),
            "bic": round_number(float(model["bic"]), 2),
            "deltaBic": round_number(float(model["bic"]) - best_bic, 2),
            "iterations": int(model["iterations"]),
            "converged": bool(model["converged"]),
        }
    )
    model_comparison.sort(key=lambda item: float(item["bic"]))  # type: ignore[arg-type]

    degrees_of_freedom = float(model["degreesOfFreedom"])
    body_weights = model["responsibilities"][:, 0]  # type: ignore[index]
    tail_weights = model["responsibilities"][:, 1]  # type: ignore[index]
    body_covariance = model["bodyCovariance"]  # type: ignore[assignment]
    body_radius = student_t_containment_radius(degrees_of_freedom)
    body_display_covariance = body_covariance * (body_radius / CONFIDENCE_RADIUS) ** 2
    _body_axes, _body_vectors, body_los_cosine, body_sky_area = ellipsoid_axis_metrics(body_covariance)
    body = ellipsoid_payload(
        "cepheids",
        "smc",
        vector_from_local(model["bodyMean"], origin, basis),  # type: ignore[arg-type]
        local_covariance_to_galactic(body_display_covariance, basis),
        int(round(float(body_weights.sum()))),
        label="SMC Bar Cepheids",
        alpha=0.76,
        line_width=1.12,
        extra={
            "componentRole": "main",
            "structureModel": "student-t-primary-component",
            "mixtureWeight": round_number(float(model["weights"][0]), 4),  # type: ignore[index]
            "softMembershipCount": round_number(float(body_weights.sum()), 1),
            "kishEffectiveSampleSize": round_number(effective_weight_count(body_weights), 1),
            "degreesOfFreedom": round_number(degrees_of_freedom, 3),
            "bodyContainment": round_number(STUDENT_T_BODY_CONTAINMENT, 3),
            "studentTContainmentRadius": round_number(body_radius, 4),
            "lineOfSightMajorAxisCosine": round_number(body_los_cosine, 4),
            "projectedSkyAreaKpc2": round_number(body_sky_area, 4),
            "medianDistanceErrorKpc": round_number(float(np.median(sigma)), 3),
            "uncertaintyTreatment": "distance errors included as measurement covariance; wireframe covariance is intrinsic EIV covariance",
            "modelComparison": model_comparison,
        },
    )

    tail_covariance = model["tailCovariance"]  # type: ignore[assignment]
    tail_mean = model["tailMean"]  # type: ignore[assignment]
    tail_inverse = np.linalg.inv(positive_semidefinite(tail_covariance))
    tail_mahalanobis = np.einsum("ni,ij,nj->n", local - tail_mean, tail_inverse, local - tail_mean)
    tail_scale = math.sqrt(weighted_quantile(tail_mahalanobis, tail_weights, EIV_GMM_ENVELOPE_CONTAINMENT)) / CONFIDENCE_RADIUS
    _tail_axes, _tail_vectors, tail_los_cosine, tail_sky_area = ellipsoid_axis_metrics(tail_covariance)
    tail = ellipsoid_payload(
        "cepheids",
        "smc",
        vector_from_local(tail_mean, origin, basis),
        local_covariance_to_galactic(tail_covariance * tail_scale * tail_scale, basis),
        int(round(float(tail_weights.sum()))),
        label="SMC Wing Cepheids",
        alpha=0.44,
        line_width=0.9,
        line_dash=SECONDARY_COMPONENT_LINE_DASH,
        extra={
            "componentRole": "secondary",
            "structureModel": "student-t-gaussian-secondary-component",
            "containment": round_number(EIV_GMM_ENVELOPE_CONTAINMENT, 3),
            "mixtureWeight": round_number(float(model["weights"][1]), 4),  # type: ignore[index]
            "softMembershipCount": round_number(float(tail_weights.sum()), 1),
            "kishEffectiveSampleSize": round_number(effective_weight_count(tail_weights), 1),
            "lineOfSightMajorAxisCosine": round_number(tail_los_cosine, 4),
            "projectedSkyAreaKpc2": round_number(tail_sky_area, 4),
            "primaryMembershipWeightFraction": round_number(float(body_weights.sum() / len(body_weights)), 4),
        },
    )
    return [body, tail]


def build_lmc_rrlyrae_body_halo(
    payload: dict[str, object],
    indexes: dict[str, int],
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> list[dict[str, object]]:
    return build_eiv_gmm_body_envelope(
        payload,
        indexes,
        "rrlyrae",
        "lmc",
        origin,
        basis,
        body_label="LMC Core RR Lyrae",
        envelope_label="LMC Halo RR Lyrae",
        body_selection="compact-los",
        body_structure_model="eiv-gmm-line-of-sight-body",
        envelope_structure_model="eiv-gmm-nonbody-halo-envelope",
    )


def build_smc_rrlyrae_student_t_ellipsoid(
    payload: dict[str, object],
    indexes: dict[str, int],
    origin: np.ndarray,
    basis: dict[str, np.ndarray],
) -> dict[str, object]:
    arrays = subset_arrays(payload, indexes, "rrlyrae", "smc")
    local = arrays["local"]  # type: ignore[assignment]
    position = arrays["position"]  # type: ignore[assignment]
    sigma = arrays["sigma"]  # type: ignore[assignment]
    measurement = local_measurement_covariances(position, sigma, basis)
    gmm_candidates = fit_eiv_gmm_model_selection(local, measurement)
    student_t = fit_student_t_ellipsoid(local, measurement)
    two_component = fit_student_t_body_gaussian_tail(local, measurement, gmm_candidates)
    best_bic = min(
        float(student_t["bic"]),
        float(two_component["bic"]),
        *(float(candidate["bic"]) for candidate in gmm_candidates),
    )
    model_comparison = [
        {
            "model": f"eiv-gmm-{int(candidate['componentCount'])}",
            "components": int(candidate["componentCount"]),
            "logLikelihood": round_number(float(candidate["logLikelihood"]), 2),
            "aic": round_number(float(candidate["aic"]), 2),
            "bic": round_number(float(candidate["bic"]), 2),
            "deltaBic": round_number(float(candidate["bic"]) - best_bic, 2),
            "iterations": int(candidate["iterations"]),
            "converged": bool(candidate["converged"]),
        }
        for candidate in gmm_candidates
    ]
    model_comparison.extend(
        [
            {
                "model": "student-t-ellipsoid",
                "components": 1,
                "degreesOfFreedom": round_number(float(student_t["degreesOfFreedom"]), 3),
                "logLikelihood": round_number(float(student_t["logLikelihood"]), 2),
                "aic": round_number(float(student_t["aic"]), 2),
                "bic": round_number(float(student_t["bic"]), 2),
                "deltaBic": round_number(float(student_t["bic"]) - best_bic, 2),
                "iterations": int(student_t["iterations"]),
                "converged": bool(student_t["converged"]),
            },
            {
                "model": "student-t-extended-gaussian-compact",
                "components": 2,
                "degreesOfFreedom": round_number(float(two_component["degreesOfFreedom"]), 3),
                "logLikelihood": round_number(float(two_component["logLikelihood"]), 2),
                "aic": round_number(float(two_component["aic"]), 2),
                "bic": round_number(float(two_component["bic"]), 2),
                "deltaBic": round_number(float(two_component["bic"]) - best_bic, 2),
                "iterations": int(two_component["iterations"]),
                "converged": bool(two_component["converged"]),
            },
        ]
    )
    model_comparison.sort(key=lambda item: float(item["bic"]))  # type: ignore[arg-type]

    degrees_of_freedom = float(student_t["degreesOfFreedom"])
    covariance = student_t["covariance"]  # type: ignore[assignment]
    radius = student_t_containment_radius(degrees_of_freedom)
    display_covariance = covariance * (radius / CONFIDENCE_RADIUS) ** 2
    _axes, _vectors, los_cosine, sky_area = ellipsoid_axis_metrics(covariance)
    return ellipsoid_payload(
        "rrlyrae",
        "smc",
        vector_from_local(student_t["mean"], origin, basis),  # type: ignore[arg-type]
        local_covariance_to_galactic(display_covariance, basis),
        len(arrays["rows"]),  # type: ignore[arg-type]
        label="SMC RR Lyrae",
        alpha=0.7,
        line_width=1.12,
        extra={
            "componentRole": "main",
            "structureModel": "student-t-ellipsoid",
            "mixtureWeight": 1.0,
            "softMembershipCount": len(arrays["rows"]),  # type: ignore[arg-type]
            "degreesOfFreedom": round_number(degrees_of_freedom, 3),
            "studentTContainment": round_number(STUDENT_T_BODY_CONTAINMENT, 3),
            "studentTContainmentRadius": round_number(radius, 4),
            "lineOfSightMajorAxisCosine": round_number(los_cosine, 4),
            "projectedSkyAreaKpc2": round_number(sky_area, 4),
            "medianDistanceErrorKpc": round_number(float(np.median(sigma)), 3),
            "uncertaintyTreatment": "distance errors included as measurement covariance; wireframe covariance is intrinsic EIV covariance",
            "selectionNote": "Single Student-t ellipsoid chosen as conservative default visualization; mixture alternatives remain in modelComparison.",
            "modelComparison": model_comparison,
        },
    )


def existing_fit_ellipsoid_or_single(
    payload: dict[str, object],
    indexes: dict[str, int],
    population_id: str,
    cloud_id: str,
    *,
    label: str,
    structure_model: str = "triaxial-gaussian",
    alpha: float = 0.82,
    line_width: float = 1.15,
) -> dict[str, object]:
    existing = {
        fit.get("id"): fit
        for fit in payload.get("meta", {}).get("annotationFits", {}).get("fits", [])  # type: ignore[union-attr]
        if isinstance(fit, dict)
    }
    fit_id = f"{population_id}-{cloud_id}"
    if fit_id in existing:
        fit = dict(existing[fit_id])
        fit.update(
            {
                "type": "ellipsoid",
                "id": f"{population_id}-{cloud_id}-envelope",
                "label": label,
                "structureModel": structure_model,
                "color": POPULATIONS[population_id]["color"],
                "lineDash": list(MAIN_COMPONENT_LINE_DASH),
                "componentRole": "main",
                "alpha": alpha,
                "lineWidth": line_width,
            }
        )
        return fit

    arrays = subset_arrays(payload, indexes, population_id, cloud_id)
    params = fit_single_gaussian(arrays["position"], arrays["measurement"])  # type: ignore[arg-type]
    return ellipsoid_payload(
        population_id,
        cloud_id,
        params["means"][0],
        params["covariances"][0],
        len(arrays["rows"]),  # type: ignore[arg-type]
        label=label,
        alpha=alpha,
        line_width=line_width,
        extra={"componentRole": "main", "structureModel": structure_model},
    )


def existing_mira_or_single(
    payload: dict[str, object],
    indexes: dict[str, int],
    cloud_id: str,
) -> dict[str, object]:
    return existing_fit_ellipsoid_or_single(
        payload,
        indexes,
        "miras",
        cloud_id,
        label=f"{CLOUDS[cloud_id]['label']} Miras",
        structure_model="triaxial-gaussian",
    )


def update_payload(payload: dict[str, object]) -> dict[str, object]:
    fields = payload["fields"]["catalog"]  # type: ignore[index]
    indexes = {name: index for index, name in enumerate(fields)}
    origin = np.asarray(payload["meta"]["coordinateCenters"]["sampleGalacticVectorKpc"], dtype=float)  # type: ignore[index]
    basis = make_basis(origin)
    structures = []
    structures.extend(build_lmc_cepheid_bar_disk(payload, indexes, origin, basis))
    structures.extend(build_lmc_cepheid_ripepi_feature_labels(payload, indexes))
    structures.extend(build_smc_cepheid_student_t_body_tail(payload, indexes, origin, basis))
    structures.extend(build_smc_cepheid_literature_feature_labels(payload, indexes))
    structures.extend(build_lmc_rrlyrae_body_halo(payload, indexes, origin, basis))
    structures.append(build_smc_rrlyrae_student_t_ellipsoid(payload, indexes, origin, basis))
    for cloud_id in ("lmc", "smc"):
        structures.append(existing_mira_or_single(payload, indexes, cloud_id))

    annotation = payload.setdefault("meta", {}).setdefault("annotationFits", {})  # type: ignore[union-attr]
    annotation.update(
        {
            "version": 31,
            "representation": "model-selected",
            "method": (
                "Tracer-specific atlas structures selected by local AIC/BIC and held-out likelihood: "
                "LMC Cepheids use a Ripepi-style thick disk density contour model plus a separately selected "
                "errors-in-variables bar ellipsoid and literature feature labels anchored to atlas Cepheid medians, "
                "SMC Cepheids use a Student-t primary component "
                "plus Gaussian secondary component selected by BIC and held-out likelihood, with literature "
                "feature labels anchored to atlas Cepheid medians, "
                "LMC RR Lyrae use simultaneous errors-in-variables Gaussian mixtures with "
                "a line-of-sight body and non-body halo envelope, SMC RR Lyrae use a single "
                "Student-t ellipsoid as a conservative default visualization, and Miras retain "
                "single triaxial envelopes."
            ),
            "lineStyleEncoding": "main components use solid lines; secondary and halo components use dashed lines",
            "structureSelection": {
                "cepheids": {
                    "lmc": "ripepi-style-thick-disk-density-contours + ripepi-style-eiv-bar-ellipsoid + Ripepi feature labels",
                    "smc": "student-t-primary-component + student-t-gaussian-secondary-component + SMC literature feature labels",
                },
                "rrlyrae": {
                    "lmc": "eiv-gmm-line-of-sight-body + eiv-gmm-nonbody-halo-envelope",
                    "smc": "student-t-ellipsoid",
                },
                "miras": "triaxial-gaussian",
            },
            "confidenceRadius": CONFIDENCE_RADIUS,
            "confidenceRadiusNote": "Gaussian ellipsoid radii are sqrt(eigenvalue) multiplied by 1.878, the 68 percent containment radius for a 3-D Gaussian. Student-t primary-component radii use the fitted Student-t 68 percent containment radius.",
            "structures": structures,
        }
    )
    return payload


def write_payload(payload: dict[str, object], atlas_path: Path) -> None:
    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    def replace_bytes(path: Path, content: bytes) -> None:
        temp_path = path.with_name(f"{path.name}.tmp")
        temp_path.write_bytes(content)
        os.replace(temp_path, path)

    replace_bytes(atlas_path, data)
    brotli_bytes = compress_brotli(data)
    brotli_path = atlas_path.with_suffix(atlas_path.suffix + ".br")
    if brotli_bytes is not None:
        replace_bytes(brotli_path, brotli_bytes)
    elif brotli_path.exists():
        brotli_path.unlink()
    replace_bytes(atlas_path.with_suffix(atlas_path.suffix + ".gz"), gzip.compress(data, compresslevel=9, mtime=0))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas", type=Path, default=DEFAULT_ATLAS)
    args = parser.parse_args()
    payload = json.loads(args.atlas.read_text(encoding="utf-8"))
    update_payload(payload)
    write_payload(payload, args.atlas)
    structures = payload["meta"]["annotationFits"]["structures"]
    print(json.dumps([(item["id"], item["type"], item["structureModel"]) for item in structures], indent=2))


if __name__ == "__main__":
    main()
