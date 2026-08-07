from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.ndimage import gaussian_filter

from build_oden_author_rc_volume import (
    DEFAULT_ARCHIVE,
    DEFAULT_OUTPUT as DEFAULT_POINT_VOLUME_OUTPUT,
    GALACTIC_TO_MAGELLANIC_STREAM,
    ICRS_TO_GALACTIC,
    ROOT,
    compress_json,
    git_version,
    icrs_unit_vectors,
    load_catalog,
    lon_lat_from_vectors,
    now_iso,
    profile,
    sha256_file,
    write_json,
)


DEFAULT_OUTPUT = ROOT / "public" / "data" / "oden-author-red-clump-volume-v2.json"
DEFAULT_SCIENCE_OUTPUT = (
    ROOT
    / "data"
    / "processed"
    / "rc_publication"
    / "rc_volume_observed_likelihood_v2.npz"
)
DEFAULT_DIAGNOSTIC_DIR = (
    ROOT / "diagnostics" / "figures" / "oden_author_red_clump_likelihood_volume_v2"
)
DEFAULT_REPORT = DEFAULT_DIAGNOSTIC_DIR / "report.md"

ODEN_BRIDGE_CENTER_MS_DEG = (-9.2, -6.3)
ODEN_BRIDGE_RADIUS_DEG = 1.25


def weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    valid = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    if not np.any(valid):
        return float("nan")
    values = values[valid]
    weights = weights[valid]
    order = np.argsort(values)
    cumulative = np.cumsum(weights[order], dtype=np.float64)
    midpoint = cumulative[-1] * 0.5
    return float(values[order[np.searchsorted(cumulative, midpoint, side="left")]])


def distance_modulus_kernel(
    sigma_mag: float,
    support_sigma: float,
    sample_count: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if sigma_mag <= 0:
        raise ValueError("Distance-modulus sigma must be positive")
    if support_sigma < 3:
        raise ValueError("Kernel support must extend to at least 3 sigma")
    if sample_count < 9 or sample_count % 2 == 0:
        raise ValueError("Kernel sample count must be an odd integer >= 9")

    sigma_offsets = np.linspace(-support_sigma, support_sigma, sample_count)
    weights = np.exp(-0.5 * sigma_offsets**2)
    # The endpoint half-weights implement the trapezoidal integration rule.
    weights[[0, -1]] *= 0.5
    weights /= weights.sum()
    modulus_offsets = sigma_offsets * sigma_mag
    distance_scales = 10 ** (modulus_offsets / 5.0)
    return modulus_offsets, distance_scales, weights


def grid_geometry(
    vectors_kpc: np.ndarray,
    distance_scales: np.ndarray,
    voxel_size_kpc: float,
    margin_voxels: int,
) -> tuple[np.ndarray, tuple[int, int, int]]:
    scaled_low = vectors_kpc * float(distance_scales.min())
    scaled_high = vectors_kpc * float(distance_scales.max())
    minimum = np.floor(np.minimum(scaled_low, scaled_high).min(axis=0) / voxel_size_kpc).astype(np.int32)
    maximum = np.floor(np.maximum(scaled_low, scaled_high).max(axis=0) / voxel_size_kpc).astype(np.int32)
    minimum -= margin_voxels
    maximum += margin_voxels
    shape = tuple(int(value) for value in maximum - minimum + 1)
    return minimum, shape


def flattened_voxel_indexes(
    vectors_kpc: np.ndarray,
    scale: float,
    voxel_size_kpc: float,
    origin_index: np.ndarray,
    shape: tuple[int, int, int],
) -> np.ndarray:
    indexes = np.floor(vectors_kpc * scale / voxel_size_kpc).astype(np.int32)
    indexes -= origin_index
    return (indexes[:, 0] * shape[1] + indexes[:, 1]) * shape[2] + indexes[:, 2]


def build_likelihood_grid(
    vectors_kpc: np.ndarray,
    *,
    voxel_size_kpc: float,
    sigma_mag: float,
    support_sigma: float,
    sample_count: int,
    anti_alias_sigma_voxels: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, tuple[int, int, int], dict[str, Any]]:
    modulus_offsets, distance_scales, kernel_weights = distance_modulus_kernel(
        sigma_mag,
        support_sigma,
        sample_count,
    )
    margin_voxels = max(2, int(np.ceil(anti_alias_sigma_voxels * 4)))
    origin_index, shape = grid_geometry(
        vectors_kpc,
        distance_scales,
        voxel_size_kpc,
        margin_voxels,
    )
    flat_size = int(np.prod(shape))

    point_indexes = flattened_voxel_indexes(
        vectors_kpc,
        1.0,
        voxel_size_kpc,
        origin_index,
        shape,
    )
    source_count_grid = np.bincount(point_indexes, minlength=flat_size).reshape(shape).astype(np.uint32)

    likelihood_flat = np.zeros(flat_size, dtype=np.float32)
    for distance_scale, weight in zip(distance_scales, kernel_weights):
        indexes = flattened_voxel_indexes(
            vectors_kpc,
            float(distance_scale),
            voxel_size_kpc,
            origin_index,
            shape,
        )
        node_weights = np.full(len(indexes), float(weight), dtype=np.float32)
        likelihood_flat += np.bincount(
            indexes,
            weights=node_weights,
            minlength=flat_size,
        ).astype(np.float32)

    pre_smooth_mass = float(likelihood_flat.sum(dtype=np.float64))
    likelihood_grid = likelihood_flat.reshape(shape)
    if anti_alias_sigma_voxels > 0:
        likelihood_grid = gaussian_filter(
            likelihood_grid,
            sigma=anti_alias_sigma_voxels,
            mode="constant",
            truncate=3.0,
        )
    post_smooth_mass = float(likelihood_grid.sum(dtype=np.float64))
    likelihood_grid *= len(vectors_kpc) / post_smooth_mass

    summary = {
        "gridOriginIndex": [int(value) for value in origin_index],
        "voxelGridShape": [int(value) for value in shape],
        "voxelSizeKpc": voxel_size_kpc,
        "distanceKernel": {
            "distribution": "Gaussian in distance modulus",
            "sigmaMag": sigma_mag,
            "fractionalSigmaLinearApproximation": round(float(np.log(10) * sigma_mag / 5), 8),
            "supportSigma": support_sigma,
            "sampleCount": sample_count,
            "modulusOffsetsMag": [round(float(value), 6) for value in modulus_offsets],
            "normalizedWeights": [round(float(value), 10) for value in kernel_weights],
        },
        "antiAliasKernel": {
            "distribution": "isotropic Gaussian on the Cartesian voxel grid",
            "sigmaVoxels": anti_alias_sigma_voxels,
            "sigmaKpc": round(anti_alias_sigma_voxels * voxel_size_kpc, 6),
            "role": "numerical density-estimator anti-aliasing, not an astrophysical distance error",
        },
        "pointGridMass": int(source_count_grid.sum(dtype=np.uint64)),
        "preAntiAliasLikelihoodMass": pre_smooth_mass,
        "postAntiAliasLikelihoodMassBeforeNormalization": post_smooth_mass,
        "postAntiAliasLikelihoodMass": float(likelihood_grid.sum(dtype=np.float64)),
    }
    return source_count_grid, likelihood_grid, origin_index, shape, summary


def centers_for_indexes(
    indexes: np.ndarray,
    origin_index: np.ndarray,
    voxel_size_kpc: float,
) -> np.ndarray:
    return (indexes.astype(np.float64) + origin_index + 0.5) * voxel_size_kpc


def stream_coordinates_for_centers(centers_kpc: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    unit = centers_kpc / np.linalg.norm(centers_kpc, axis=1)[:, None]
    stream_vectors = unit @ GALACTIC_TO_MAGELLANIC_STREAM.T
    return lon_lat_from_vectors(stream_vectors)


def bridge_mask(stream_lon_deg: np.ndarray, stream_lat_deg: np.ndarray) -> np.ndarray:
    center_lon, center_lat = ODEN_BRIDGE_CENTER_MS_DEG
    return (
        (stream_lon_deg - center_lon) ** 2 + (stream_lat_deg - center_lat) ** 2
        <= ODEN_BRIDGE_RADIUS_DEG**2
    )


def summarize_grid_validation(
    distance_kpc: np.ndarray,
    source_stream_lon_deg: np.ndarray,
    source_stream_lat_deg: np.ndarray,
    likelihood_grid: np.ndarray,
    serialized_mask: np.ndarray,
    origin_index: np.ndarray,
    voxel_size_kpc: float,
) -> dict[str, Any]:
    evaluation_mask = likelihood_grid >= 1e-4
    evaluation_indexes = np.argwhere(evaluation_mask)
    evaluation_weights = likelihood_grid[evaluation_mask].astype(np.float64)
    centers = centers_for_indexes(evaluation_indexes, origin_index, voxel_size_kpc)
    distances = np.linalg.norm(centers, axis=1)
    stream_lon_deg, stream_lat_deg = stream_coordinates_for_centers(centers)
    smc = (stream_lon_deg + 19.0) ** 2 + (stream_lat_deg + 12.5) ** 2 <= 13.0**2
    bridge = bridge_mask(stream_lon_deg, stream_lat_deg)

    source_smc = (source_stream_lon_deg + 19.0) ** 2 + (source_stream_lat_deg + 12.5) ** 2 <= 13.0**2
    source_bridge = bridge_mask(source_stream_lon_deg, source_stream_lat_deg)

    serialized_weights = likelihood_grid[serialized_mask].astype(np.float64)
    serialized_indexes = np.argwhere(serialized_mask)
    serialized_centers = centers_for_indexes(serialized_indexes, origin_index, voxel_size_kpc)
    serialized_lon, serialized_lat = stream_coordinates_for_centers(serialized_centers)
    serialized_bridge = bridge_mask(serialized_lon, serialized_lat)

    full_mass = float(likelihood_grid.sum(dtype=np.float64))
    evaluated_mass = float(evaluation_weights.sum(dtype=np.float64))
    serialized_mass = float(serialized_weights.sum(dtype=np.float64))
    return {
        "sourceCombinedMedianKpc": round(float(np.median(distance_kpc)), 6),
        "likelihoodCombinedMedianKpc": round(weighted_median(distances, evaluation_weights), 6),
        "sourceLmcMedianKpc": round(float(np.median(distance_kpc[~source_smc])), 6),
        "likelihoodLmcMedianKpc": round(weighted_median(distances[~smc], evaluation_weights[~smc]), 6),
        "sourceSmcMedianKpc": round(float(np.median(distance_kpc[source_smc])), 6),
        "likelihoodSmcMedianKpc": round(weighted_median(distances[smc], evaluation_weights[smc]), 6),
        "sourceBridgeCount": int(np.count_nonzero(source_bridge)),
        "fullGridBridgeLikelihoodMass": round(float(evaluation_weights[bridge].sum()), 6),
        "serializedBridgeLikelihoodMass": round(float(serialized_weights[serialized_bridge].sum()), 6),
        "evaluationMassFraction": round(evaluated_mass / full_mass, 10),
        "serializedLikelihoodMass": round(serialized_mass, 6),
        "serializedMassFraction": round(serialized_mass / full_mass, 10),
        "serializedVoxelCount": int(np.count_nonzero(serialized_mask)),
    }


def build_browser_rows(
    source_count_grid: np.ndarray,
    likelihood_grid: np.ndarray,
    serialized_mask: np.ndarray,
    origin_index: np.ndarray,
    voxel_size_kpc: float,
    density_reference_quantile: float,
) -> tuple[list[list[float | int]], dict[str, Any]]:
    indexes = np.argwhere(serialized_mask)
    centers = centers_for_indexes(indexes, origin_index, voxel_size_kpc)
    source_counts = source_count_grid[serialized_mask]
    likelihood_counts = likelihood_grid[serialized_mask].astype(np.float64)
    reference = max(1.0, float(np.quantile(likelihood_counts, density_reference_quantile)))
    density_unit = np.clip(np.log1p(likelihood_counts) / np.log1p(reference), 0.0, 1.0)

    rows: list[list[float | int]] = []
    for center, source_count, likelihood_count, density in zip(
        centers,
        source_counts,
        likelihood_counts,
        density_unit,
    ):
        rows.append(
            [
                round(float(center[0]), 3),
                round(float(center[1]), 3),
                round(float(center[2]), 3),
                int(source_count),
                round(float(likelihood_count), 5),
                round(float(density), 5),
            ]
        )

    summary = {
        "serializedVoxelCount": int(len(rows)),
        "densityReferenceQuantile": density_reference_quantile,
        "densityReferenceLikelihoodStarsPerVoxel": round(reference, 6),
        "serializedLikelihoodCountMedian": round(float(np.median(likelihood_counts)), 6),
        "serializedLikelihoodCountP90": round(float(np.quantile(likelihood_counts, 0.9)), 6),
        "serializedLikelihoodCountMax": round(float(np.max(likelihood_counts)), 6),
        "galacticCartesianBoundsKpc": {
            axis: [round(float(centers[:, index].min()), 3), round(float(centers[:, index].max()), 3)]
            for index, axis in enumerate(("x", "y", "z"))
        },
    }
    return rows, summary


def write_science_grid(
    path: Path,
    source_count_grid: np.ndarray,
    likelihood_grid: np.ndarray,
    origin_index: np.ndarray,
    voxel_size_kpc: float,
    sigma_mag: float,
    serialized_threshold: float,
) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("wb") as handle:
        np.savez_compressed(
            handle,
            source_star_count=source_count_grid,
            likelihood_star_count=likelihood_grid.astype(np.float32),
            grid_origin_index=origin_index.astype(np.int32),
            voxel_size_kpc=np.array(voxel_size_kpc, dtype=np.float64),
            distance_modulus_sigma_mag=np.array(sigma_mag, dtype=np.float64),
            browser_serialization_threshold=np.array(serialized_threshold, dtype=np.float64),
        )
    temporary.replace(path)
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def projection(array: np.ndarray, horizontal_axis: int, vertical_axis: int) -> np.ndarray:
    summed_axis = ({0, 1, 2} - {horizontal_axis, vertical_axis}).pop()
    projected = array.sum(axis=summed_axis, dtype=np.float64)
    remaining_axes = [axis for axis in range(3) if axis != summed_axis]
    if remaining_axes != [horizontal_axis, vertical_axis]:
        projected = projected.T
    return projected.T


def build_comparison_diagnostic(
    path: Path,
    source_count_grid: np.ndarray,
    likelihood_grid: np.ndarray,
    origin_index: np.ndarray,
    voxel_size_kpc: float,
    sigma_mag: float,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    shape = source_count_grid.shape
    bounds = [
        (
            (origin_index[axis] + 0.5) * voxel_size_kpc,
            (origin_index[axis] + shape[axis] - 0.5) * voxel_size_kpc,
        )
        for axis in range(3)
    ]
    panels = [
        (projection(source_count_grid, 0, 1), 0, 1, "Point estimates: face projection"),
        (projection(likelihood_grid, 0, 1), 0, 1, "Likelihood volume: face projection"),
        (projection(source_count_grid, 0, 2), 0, 2, "Point estimates: depth projection"),
        (projection(likelihood_grid, 0, 2), 0, 2, "Likelihood volume: depth projection"),
    ]
    transformed = [np.log10(1 + values) for values, _, _, _ in panels]
    limits = {
        (0, 1): max(float(np.max(transformed[0])), float(np.max(transformed[1]))),
        (0, 2): max(float(np.max(transformed[2])), float(np.max(transformed[3]))),
    }

    figure, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
    images = []
    for axis, (values, horizontal, vertical, title), image_values in zip(axes.flat, panels, transformed):
        image = axis.imshow(
            image_values,
            origin="lower",
            interpolation="nearest",
            extent=[bounds[horizontal][0], bounds[horizontal][1], bounds[vertical][0], bounds[vertical][1]],
            cmap="magma",
            vmin=0,
            vmax=limits[(horizontal, vertical)],
            aspect="equal",
        )
        axis.set_xlabel(f"Galactic {'XYZ'[horizontal]} (kpc)")
        axis.set_ylabel(f"Galactic {'XYZ'[vertical]} (kpc)")
        axis.set_title(title)
        images.append(image)
    figure.colorbar(images[0], ax=axes[0, :], label="log10(1 + projected stars)", shrink=0.92)
    figure.colorbar(images[2], ax=axes[1, :], label="log10(1 + projected stars)", shrink=0.92)
    figure.suptitle(
        f"Oden author catalog: point density versus {sigma_mag:.2f}-mag LOS likelihood convolution",
        fontsize=15,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=220)
    plt.close(figure)


def build_kernel_diagnostic(path: Path, sigma_mag: float, distance_profiles: dict[str, float]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    modulus = np.linspace(-0.42, 0.42, 1200)
    figure, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)

    for candidate, color in zip((0.07, sigma_mag, 0.13), ("#5aa9e6", "#fca311", "#d1495b")):
        density = np.exp(-0.5 * (modulus / candidate) ** 2)
        density /= np.trapz(density, modulus)
        axes[0].plot(modulus, density, color=color, linewidth=2, label=f"sigma_mu = {candidate:.2f} mag")
    axes[0].set_xlabel("Distance-modulus offset (mag)")
    axes[0].set_ylabel("Probability density")
    axes[0].set_title("Documented kernel and sensitivity bracket")
    axes[0].legend(frameon=False)

    for label, distance in distance_profiles.items():
        for candidate, color, alpha in zip(
            (0.07, sigma_mag, 0.13),
            ("#5aa9e6", "#fca311", "#d1495b"),
            (0.7, 1.0, 0.7),
        ):
            distance_axis = distance * 10 ** (modulus / 5)
            density = np.exp(-0.5 * (modulus / candidate) ** 2)
            density *= 5 / (np.log(10) * distance_axis)
            density /= np.trapz(density, distance_axis)
            axes[1].plot(
                distance_axis,
                density,
                color=color,
                alpha=alpha,
                linewidth=2 if candidate == sigma_mag else 1.2,
                linestyle="-" if label == "LMC" else "--",
            )
    axes[1].set_xlabel("Distance (kpc)")
    axes[1].set_ylabel("Probability density")
    axes[1].set_title("LOS kernels at the LMC (solid) and SMC (dashed)")
    axes[1].set_xlim(42, 73)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=220)
    plt.close(figure)


def build_report(
    path: Path,
    *,
    source_count: int,
    grid_summary: dict[str, Any],
    browser_summary: dict[str, Any],
    validation: dict[str, Any],
    comparison_path: Path,
    kernel_path: Path,
) -> None:
    kernel = grid_summary["distanceKernel"]
    anti_alias = grid_summary["antiAliasKernel"]
    text = f"""# Oden author-catalog RC likelihood volume v2

## Result

The exact `{source_count:,}` author-supplied point distances remain preserved in the local v1 archive. The v2 product represents each point as a Gaussian likelihood in distance modulus with `sigma_mu = {kernel['sigmaMag']:.2f} mag`, then deposits that likelihood only along the star's heliocentric line of sight. The sky coordinates are not broadened by the distance uncertainty.

This is an **uncertainty-convolved observed-density visualization**, not a deconvolved physical density. It must not be used to measure the intrinsic line-of-sight thickness of either Cloud.

## Scientific basis

- Oden et al. 2025 report about `0.10 mag` uncertainty in the empirical RC absolute-magnitude/color calibration, corresponding to about `2.3 kpc` at the LMC and `2.8 kpc` at the SMC (`papers/oden_2025.tex`, systematic-effects discussion).
- A Gaussian in distance modulus is transformed exactly to distance scaling with `d' = d * 10^(Delta_mu/5)`.
- The kernel is sampled at `{kernel['sampleCount']}` nodes over `+/-{kernel['supportSigma']:.1f} sigma` and normalized to unit mass.
- A much smaller `{anti_alias['sigmaKpc']:.2f} kpc` Cartesian Gaussian suppresses voxel aliasing. It is a numerical density-estimation kernel, not an added stellar-distance uncertainty.

## Validation

| Check | Result |
|---|---:|
| Source point count | {source_count:,} |
| Point-grid count | {grid_summary['pointGridMass']:,} |
| Full likelihood mass | {grid_summary['postAntiAliasLikelihoodMass']:.3f} |
| Browser likelihood mass retained | {validation['serializedMassFraction'] * 100:.4f}% |
| Browser voxels | {browser_summary['serializedVoxelCount']:,} |
| Source / likelihood combined median | {validation['sourceCombinedMedianKpc']:.3f} / {validation['likelihoodCombinedMedianKpc']:.3f} kpc |
| Source / likelihood LMC median | {validation['sourceLmcMedianKpc']:.3f} / {validation['likelihoodLmcMedianKpc']:.3f} kpc |
| Source / likelihood SMC median | {validation['sourceSmcMedianKpc']:.3f} / {validation['likelihoodSmcMedianKpc']:.3f} kpc |
| Oden Bridge source count | {validation['sourceBridgeCount']} |
| Bridge likelihood mass in browser export | {validation['serializedBridgeLikelihoodMass']:.2f} star-equivalents |

## Interpretation limits

- Oden's supplied FITS file contains only RA, Dec, and a point distance; it has no per-star uncertainty or covariance columns.
- The `0.10 mag` calibration term is treated as an independent marginal kernel for display. If part of that term is globally or spatially correlated, the true joint uncertainty is a coherent distance-scale shift rather than independent diffusion.
- Physical depth and distance uncertainty are therefore not separated here. A physical 3D density requires a hierarchical forward model and deconvolution/injection validation.
- Completeness and RC population-selection weights are not present in the supplied file and are not invented by this build.

## Figures

- Point estimate versus likelihood projections: `{comparison_path}`
- Kernel and sensitivity bracket: `{kernel_path}`
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build(args: argparse.Namespace) -> dict[str, Any]:
    archive_info = {
        "path": str(args.archive),
        "bytes": args.archive.stat().st_size,
        "sha256": sha256_file(args.archive),
    }
    ra_deg, dec_deg, distance_kpc, fits_metadata = load_catalog(args.archive)
    icrs_vectors = icrs_unit_vectors(ra_deg, dec_deg)
    galactic_unit = icrs_vectors @ ICRS_TO_GALACTIC.T
    galactic_vectors = galactic_unit * distance_kpc[:, None]
    stream_vectors = galactic_unit @ GALACTIC_TO_MAGELLANIC_STREAM.T
    stream_lon_deg, stream_lat_deg = lon_lat_from_vectors(stream_vectors)
    smc_mask = (stream_lon_deg + 19.0) ** 2 + (stream_lat_deg + 12.5) ** 2 <= 13.0**2

    source_count_grid, likelihood_grid, origin_index, shape, grid_summary = build_likelihood_grid(
        galactic_vectors,
        voxel_size_kpc=args.voxel_size_kpc,
        sigma_mag=args.distance_modulus_sigma_mag,
        support_sigma=args.kernel_support_sigma,
        sample_count=args.kernel_sample_count,
        anti_alias_sigma_voxels=args.anti_alias_sigma_voxels,
    )
    serialized_mask = likelihood_grid >= args.serialization_threshold
    validation = summarize_grid_validation(
        distance_kpc,
        stream_lon_deg,
        stream_lat_deg,
        likelihood_grid,
        serialized_mask,
        origin_index,
        args.voxel_size_kpc,
    )
    rows, browser_summary = build_browser_rows(
        source_count_grid,
        likelihood_grid,
        serialized_mask,
        origin_index,
        args.voxel_size_kpc,
        args.density_reference_quantile,
    )

    profiles = {
        "combined": profile(distance_kpc),
        "lmcOdenStreamSplit": profile(distance_kpc[~smc_mask]),
        "smcOdenStreamSplit": profile(distance_kpc[smc_mask]),
    }
    kernel = grid_summary["distanceKernel"]
    payload = {
        "schemaVersion": 2,
        "artifact": "oden_author_red_clump_observed_likelihood_volume_v2",
        "representation": "uncertainty-convolved-observed-distance-likelihood-density",
        "fields": {
            "voxels": [
                "galacticXKpc",
                "galacticYKpc",
                "galacticZKpc",
                "sourceStarCount",
                "likelihoodStarCount",
                "densityUnit",
            ]
        },
        "meta": {
            "sourceStarCount": int(len(distance_kpc)),
            "sourceArchiveSha256": archive_info["sha256"],
            "sourceFitsSha256": fits_metadata["memberSha256"],
            "coordinateFrame": "heliocentric Galactic Cartesian IAU J2000",
            "distanceField": "author-supplied point estimate in kpc",
            "densityMeaning": "sum of per-source line-of-sight distance likelihoods per Cartesian voxel",
            "physicalVolumeFlag": False,
            "displayJitterFraction": 0.0,
            "limitations": [
                "The supplied FITS file has no per-star uncertainty or covariance columns.",
                "The Oden 0.10-mag calibration uncertainty is applied as an independent marginal kernel; correlated systematics are not represented.",
                "No completeness correction is applied.",
                "This observed likelihood field cannot be interpreted as intrinsic physical line-of-sight depth.",
            ],
            **grid_summary,
            **browser_summary,
            "serializationThresholdExpectedStarsPerVoxel": args.serialization_threshold,
            "profiles": profiles,
            "validation": validation,
        },
        "source": {
            "name": "Oden et al. 2025 author-supplied Gaia red-clump catalog",
            "url": "https://github.com/slateroden/XMC_DistanceMap",
            "role": "atlas red-clump base catalog",
            "uncertaintyProvenance": {
                "source": "papers/oden_2025.tex systematic-effects section",
                "statement": "The empirical M_G/color calibration contributes approximately 0.10 mag uncertainty.",
                "adoptedDistanceModulusSigmaMag": kernel["sigmaMag"],
            },
        },
        "voxels": rows,
    }
    raw = write_json(args.output, payload, compact=True)
    output_records = compress_json(args.output, raw)
    science_record = write_science_grid(
        args.science_output,
        source_count_grid,
        likelihood_grid,
        origin_index,
        args.voxel_size_kpc,
        args.distance_modulus_sigma_mag,
        args.serialization_threshold,
    )

    comparison_path = args.diagnostic_dir / "point_vs_likelihood_volume.png"
    kernel_path = args.diagnostic_dir / "distance_kernel_sensitivity.png"
    build_comparison_diagnostic(
        comparison_path,
        source_count_grid,
        likelihood_grid,
        origin_index,
        args.voxel_size_kpc,
        args.distance_modulus_sigma_mag,
    )
    build_kernel_diagnostic(
        kernel_path,
        args.distance_modulus_sigma_mag,
        {
            "LMC": profiles["lmcOdenStreamSplit"]["medianKpc"],
            "SMC": profiles["smcOdenStreamSplit"]["medianKpc"],
        },
    )
    build_report(
        args.report,
        source_count=len(distance_kpc),
        grid_summary=grid_summary,
        browser_summary=browser_summary,
        validation=validation,
        comparison_path=comparison_path,
        kernel_path=kernel_path,
    )

    manifest = {
        "artifact": "oden_author_red_clump_likelihood_volume_build_manifest_v2",
        "createdUtc": now_iso(),
        "codeVersion": git_version(),
        "source": {**archive_info, "fits": fits_metadata},
        "configuration": {
            "voxelSizeKpc": args.voxel_size_kpc,
            "distanceModulusSigmaMag": args.distance_modulus_sigma_mag,
            "kernelSupportSigma": args.kernel_support_sigma,
            "kernelSampleCount": args.kernel_sample_count,
            "antiAliasSigmaVoxels": args.anti_alias_sigma_voxels,
            "serializationThresholdExpectedStarsPerVoxel": args.serialization_threshold,
            "densityReferenceQuantile": args.density_reference_quantile,
        },
        "profiles": profiles,
        "gridSummary": grid_summary,
        "browserSummary": browser_summary,
        "validation": validation,
        "outputs": {
            **output_records,
            "scienceGrid": science_record,
            "comparisonDiagnostic": {
                "path": str(comparison_path),
                "bytes": comparison_path.stat().st_size,
                "sha256": sha256_file(comparison_path),
            },
            "kernelDiagnostic": {
                "path": str(kernel_path),
                "bytes": kernel_path.stat().st_size,
                "sha256": sha256_file(kernel_path),
            },
            "report": {
                "path": str(args.report),
                "bytes": args.report.stat().st_size,
                "sha256": sha256_file(args.report),
            },
        },
        "scientificStatus": {
            "atlasReady": True,
            "physicalVolumeFlag": False,
            "label": "uncertainty-convolved observed red-clump distance-likelihood volume",
            "pointEstimatePredecessor": str(DEFAULT_POINT_VOLUME_OUTPUT),
        },
    }
    manifest_path = args.output.with_suffix(args.output.suffix + ".manifest.json")
    write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a LOS-uncertainty-convolved 3D likelihood volume from the Oden author RC catalog."
    )
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--science-output", type=Path, default=DEFAULT_SCIENCE_OUTPUT)
    parser.add_argument("--diagnostic-dir", type=Path, default=DEFAULT_DIAGNOSTIC_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--voxel-size-kpc", type=float, default=0.5)
    parser.add_argument("--distance-modulus-sigma-mag", type=float, default=0.10)
    parser.add_argument("--kernel-support-sigma", type=float, default=3.5)
    parser.add_argument("--kernel-sample-count", type=int, default=31)
    parser.add_argument("--anti-alias-sigma-voxels", type=float, default=0.8)
    parser.add_argument("--serialization-threshold", type=float, default=0.03)
    parser.add_argument("--density-reference-quantile", type=float, default=0.995)
    return parser.parse_args()


def main() -> None:
    manifest = build(parse_args())
    print(json.dumps(manifest, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
