from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from astropy.io import fits
from scipy.ndimage import gaussian_filter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARCHIVE = ROOT / "data" / "raw" / "mc_rc_parallax_less_strict_small.fits.zip"
DEFAULT_OUTPUT = (
    ROOT
    / "data"
    / "processed"
    / "legacy"
    / "oden-author-red-clump-point-volume-v1"
    / "oden-author-red-clump-volume-v1.json"
)
DEFAULT_DIAGNOSTIC = (
    ROOT
    / "diagnostics"
    / "figures"
    / "oden_author_red_clump_volume_v1"
    / "oden_author_red_clump_volume_v1.png"
)
DEFAULT_LEGACY_DIR = (
    ROOT / "data" / "processed" / "legacy" / "red-clump-surface-pre-oden-author-volume-v1"
)

# IAU J2000 ICRS-to-Galactic rotation used by Astropy/ERFA to numerical precision.
ICRS_TO_GALACTIC = np.array(
    [
        [-0.0548755604162154, -0.8734370902348850, -0.4838350155487132],
        [0.4941094278755837, -0.4448296299600112, 0.7469822444972189],
        [-0.8676661490190047, -0.1980763734312015, 0.4559837761750669],
    ],
    dtype=np.float64,
)

# Nidever et al. Magellanic Stream frame rotation, matching the publication pipeline.
GALACTIC_TO_MAGELLANIC_STREAM = np.array(
    [
        [0.1941363186857826, -0.8216119141972937, -0.5359710367325748],
        [-0.0286980627772346, -0.5508887911951839, 0.8340851041280758],
        [-0.9805546955473550, -0.1465448811271413, -0.1305261922200516],
    ],
    dtype=np.float64,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def git_version() -> str | None:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout.strip() or None


def write_json(path: Path, payload: dict[str, Any], *, compact: bool = False) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        text = json.dumps(payload, separators=(",", ":"), allow_nan=False)
    else:
        text = json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    raw = text.encode("utf-8")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(raw)
    temporary.replace(path)
    return raw


def compress_json(path: Path, raw: bytes) -> dict[str, Any]:
    gzip_path = path.with_suffix(path.suffix + ".gz")
    gzip_path.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
    outputs: dict[str, Any] = {
        "json": {"path": str(path), "bytes": len(raw), "sha256": sha256_bytes(raw)},
        "gzip": {
            "path": str(gzip_path),
            "bytes": gzip_path.stat().st_size,
            "sha256": sha256_file(gzip_path),
        },
    }
    try:
        import brotli

        brotli_path = path.with_suffix(path.suffix + ".br")
        brotli_path.write_bytes(brotli.compress(raw, quality=11))
        outputs["brotli"] = {
            "path": str(brotli_path),
            "bytes": brotli_path.stat().st_size,
            "sha256": sha256_file(brotli_path),
        }
    except ImportError:
        outputs["brotli"] = {"available": False}
    return outputs


def find_fits_member(archive: zipfile.ZipFile) -> str:
    members = [
        name
        for name in archive.namelist()
        if name.lower().endswith(".fits") and not name.startswith("__MACOSX/")
    ]
    if len(members) != 1:
        raise RuntimeError(f"Expected exactly one FITS table in archive; found {members}")
    return members[0]


def load_catalog(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, Any]]:
    with zipfile.ZipFile(path) as archive:
        member = find_fits_member(archive)
        member_info = archive.getinfo(member)
        fits_bytes = archive.read(member)

    with fits.open(io.BytesIO(fits_bytes), memmap=False) as hdus:
        table_hdus = [hdu for hdu in hdus if isinstance(hdu, fits.BinTableHDU)]
        if len(table_hdus) != 1:
            raise RuntimeError(f"Expected one binary table HDU; found {len(table_hdus)}")
        table_hdu = table_hdus[0]
        names = {name.lower(): name for name in table_hdu.columns.names}
        missing = sorted({"ra", "dec", "distance"} - set(names))
        if missing:
            raise RuntimeError(f"FITS table is missing required columns: {missing}")
        ra_deg = np.asarray(table_hdu.data[names["ra"]], dtype=np.float64)
        dec_deg = np.asarray(table_hdu.data[names["dec"]], dtype=np.float64)
        distance_kpc = np.asarray(table_hdu.data[names["distance"]], dtype=np.float64)
        schema = [
            {
                "name": column.name,
                "format": column.format,
                "unit": column.unit,
            }
            for column in table_hdu.columns
        ]

    valid = (
        np.isfinite(ra_deg)
        & np.isfinite(dec_deg)
        & np.isfinite(distance_kpc)
        & (ra_deg >= 0)
        & (ra_deg < 360)
        & (dec_deg >= -90)
        & (dec_deg <= 90)
        & (distance_kpc > 0)
    )
    if not np.all(valid):
        raise RuntimeError(f"Catalog has {int(np.count_nonzero(~valid))} invalid rows")

    metadata = {
        "member": member,
        "memberBytes": int(member_info.file_size),
        "memberCompressedBytes": int(member_info.compress_size),
        "memberCrc32": f"{member_info.CRC:08X}",
        "memberSha256": sha256_bytes(fits_bytes),
        "rowCount": int(len(ra_deg)),
        "schema": schema,
    }
    return ra_deg, dec_deg, distance_kpc, metadata


def icrs_unit_vectors(ra_deg: np.ndarray, dec_deg: np.ndarray) -> np.ndarray:
    ra = np.deg2rad(ra_deg)
    dec = np.deg2rad(dec_deg)
    cos_dec = np.cos(dec)
    return np.column_stack((cos_dec * np.cos(ra), cos_dec * np.sin(ra), np.sin(dec)))


def lon_lat_from_vectors(vectors: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    radius = np.linalg.norm(vectors, axis=1)
    lon = np.rad2deg(np.arctan2(vectors[:, 1], vectors[:, 0]))
    lon = (lon + 180.0) % 360.0 - 180.0
    lat = np.rad2deg(np.arcsin(np.clip(vectors[:, 2] / radius, -1.0, 1.0)))
    return lon, lat


def profile(values: np.ndarray) -> dict[str, Any]:
    quantiles = np.quantile(values, [0.05, 0.16, 0.5, 0.84, 0.95])
    return {
        "count": int(len(values)),
        "meanKpc": round(float(np.mean(values)), 6),
        "stdKpc": round(float(np.std(values)), 6),
        "p05Kpc": round(float(quantiles[0]), 6),
        "p16Kpc": round(float(quantiles[1]), 6),
        "medianKpc": round(float(quantiles[2]), 6),
        "p84Kpc": round(float(quantiles[3]), 6),
        "p95Kpc": round(float(quantiles[4]), 6),
        "minKpc": round(float(np.min(values)), 6),
        "maxKpc": round(float(np.max(values)), 6),
    }


def voxelize(
    galactic_vectors_kpc: np.ndarray,
    voxel_size_kpc: float,
    smoothing_sigma_voxels: float,
    density_reference_quantile: float,
) -> tuple[list[list[float | int]], dict[str, Any]]:
    indexes = np.floor(galactic_vectors_kpc / voxel_size_kpc).astype(np.int16)
    unique_indexes, counts = np.unique(indexes, axis=0, return_counts=True)
    minimum = unique_indexes.min(axis=0)
    shifted = unique_indexes - minimum
    shape = tuple((shifted.max(axis=0) + 1).astype(int))
    dense = np.zeros(shape, dtype=np.float32)
    dense[tuple(shifted.T)] = counts.astype(np.float32)
    smoothed = gaussian_filter(dense, sigma=smoothing_sigma_voxels, mode="constant")
    smoothed_counts = smoothed[tuple(shifted.T)].astype(np.float64)
    reference = float(np.quantile(smoothed_counts, density_reference_quantile))
    reference = max(reference, 1.0)
    density_unit = np.clip(np.log1p(smoothed_counts) / np.log1p(reference), 0.0, 1.0)
    centers = (unique_indexes.astype(np.float64) + 0.5) * voxel_size_kpc

    rows: list[list[float | int]] = []
    for center, count, smooth_count, density in zip(
        centers,
        counts,
        smoothed_counts,
        density_unit,
    ):
        rows.append(
            [
                round(float(center[0]), 3),
                round(float(center[1]), 3),
                round(float(center[2]), 3),
                int(count),
                round(float(smooth_count), 4),
                round(float(density), 5),
            ]
        )

    summary = {
        "voxelSizeKpc": voxel_size_kpc,
        "occupiedVoxelCount": int(len(rows)),
        "voxelGridShape": [int(value) for value in shape],
        "smoothingSigmaVoxels": smoothing_sigma_voxels,
        "smoothingSigmaKpc": round(voxel_size_kpc * smoothing_sigma_voxels, 6),
        "densityReferenceQuantile": density_reference_quantile,
        "densityReferenceSmoothedStarsPerVoxel": round(reference, 6),
        "occupiedVoxelStarCountMedian": float(np.median(counts)),
        "occupiedVoxelStarCountP90": float(np.quantile(counts, 0.9)),
        "occupiedVoxelStarCountMax": int(np.max(counts)),
        "singleStarVoxelFraction": round(float(np.mean(counts == 1)), 8),
        "galacticCartesianBoundsKpc": {
            axis: [round(float(centers[:, index].min()), 3), round(float(centers[:, index].max()), 3)]
            for index, axis in enumerate(("x", "y", "z"))
        },
    }
    return rows, summary


def build_diagnostic(
    path: Path,
    ra_deg: np.ndarray,
    dec_deg: np.ndarray,
    galactic_vectors: np.ndarray,
    distance_kpc: np.ndarray,
) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm

    sample_step = max(1, len(ra_deg) // 500_000)
    sample = slice(None, None, sample_step)
    figure, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
    panels = [
        (ra_deg[sample], dec_deg[sample], "RA (deg)", "Dec (deg)", "Sky density"),
        (galactic_vectors[sample, 0], galactic_vectors[sample, 1], "Galactic X (kpc)", "Galactic Y (kpc)", "Face projection"),
        (galactic_vectors[sample, 0], galactic_vectors[sample, 2], "Galactic X (kpc)", "Galactic Z (kpc)", "Depth projection X-Z"),
        (galactic_vectors[sample, 1], galactic_vectors[sample, 2], "Galactic Y (kpc)", "Galactic Z (kpc)", "Depth projection Y-Z"),
    ]
    for axis, (x, y, xlabel, ylabel, title) in zip(axes.flat, panels):
        histogram = axis.hist2d(x, y, bins=240, norm=LogNorm(), cmap="magma")
        axis.set_xlabel(xlabel)
        axis.set_ylabel(ylabel)
        axis.set_title(title)
        axis.set_aspect("equal", adjustable="box")
        figure.colorbar(histogram[3], ax=axis, label="sampled stars per bin")
    axes[0, 0].invert_xaxis()
    figure.suptitle(
        f"Oden author-supplied red-clump catalog: {len(distance_kpc):,} stars, "
        f"median {np.median(distance_kpc):.2f} kpc",
        fontsize=15,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=220)
    plt.close(figure)


def write_legacy_manifest(legacy_dir: Path) -> Path:
    records = []
    for path in sorted(legacy_dir.rglob("*")):
        if not path.is_file() or path.name == "legacy_manifest_v1.json":
            continue
        records.append(
            {
                "relativePath": path.relative_to(legacy_dir).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    manifest = {
        "artifact": "red_clump_surface_legacy_snapshot_v1",
        "createdUtc": now_iso(),
        "purpose": "Immutable rollback snapshot made before replacing the cell surface with the Oden author-catalog volume.",
        "files": records,
    }
    path = legacy_dir / "legacy_manifest_v1.json"
    write_json(path, manifest)
    return path


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
    ms_vectors = galactic_unit @ GALACTIC_TO_MAGELLANIC_STREAM.T
    ms_lon_deg, ms_lat_deg = lon_lat_from_vectors(ms_vectors)
    # Oden defines this as a circle in the projected (L_MS, B_MS) plane.
    smc_mask = (ms_lon_deg + 19.0) ** 2 + (ms_lat_deg + 12.5) ** 2 <= 13.0**2
    lmc_mask = ~smc_mask
    bridge_mask = (
        (ms_lon_deg >= -13.0)
        & (ms_lon_deg <= -3.0)
        & (ms_lat_deg >= -10.0)
        & (ms_lat_deg <= 1.0)
    )

    voxels, voxel_summary = voxelize(
        galactic_vectors,
        args.voxel_size_kpc,
        args.smoothing_sigma_voxels,
        args.density_reference_quantile,
    )
    profiles = {
        "combined": profile(distance_kpc),
        "lmcOdenStreamSplit": profile(distance_kpc[lmc_mask]),
        "smcOdenStreamSplit": profile(distance_kpc[smc_mask]),
        "bridgeCorridor": profile(distance_kpc[bridge_mask]),
    }
    payload = {
        "schemaVersion": 1,
        "artifact": "oden_author_red_clump_observed_density_volume_v1",
        "representation": "observed-first-order-distance-density",
        "fields": {
            "voxels": [
                "galacticXKpc",
                "galacticYKpc",
                "galacticZKpc",
                "starCount",
                "smoothedStarCount",
                "densityUnit",
            ]
        },
        "meta": {
            "sourceStarCount": int(len(distance_kpc)),
            "sourceArchiveSha256": archive_info["sha256"],
            "sourceFitsSha256": fits_metadata["memberSha256"],
            "coordinateFrame": "heliocentric Galactic Cartesian IAU J2000",
            "distanceField": "author-supplied point estimate in kpc",
            "densityMeaning": "raw selected-star count per fixed Cartesian voxel; display transfer uses a Gaussian-smoothed count",
            "physicalVolumeFlag": False,
            "limitations": [
                "No completeness correction is applied.",
                "Point distances are not deconvolved for red-clump intrinsic width or measurement uncertainty.",
                "The exact less-strict selection and distance-processing stage await author metadata confirmation.",
            ],
            **voxel_summary,
            "profiles": profiles,
        },
        "source": {
            "name": "Oden et al. 2025 author-supplied Gaia red-clump catalog",
            "url": "https://github.com/slateroden/XMC_DistanceMap",
            "role": "atlas red-clump base catalog",
        },
        "voxels": voxels,
    }
    raw = write_json(args.output, payload, compact=True)
    output_records = compress_json(args.output, raw)
    build_diagnostic(args.diagnostic, ra_deg, dec_deg, galactic_vectors, distance_kpc)
    legacy_manifest = write_legacy_manifest(args.legacy_dir)

    manifest = {
        "artifact": "oden_author_red_clump_volume_build_manifest_v1",
        "createdUtc": now_iso(),
        "codeVersion": git_version(),
        "source": {**archive_info, "fits": fits_metadata},
        "configuration": {
            "voxelSizeKpc": args.voxel_size_kpc,
            "smoothingSigmaVoxels": args.smoothing_sigma_voxels,
            "densityReferenceQuantile": args.density_reference_quantile,
        },
        "profiles": profiles,
        "voxelSummary": voxel_summary,
        "outputs": {
            **output_records,
            "diagnostic": {
                "path": str(args.diagnostic),
                "bytes": args.diagnostic.stat().st_size,
                "sha256": sha256_file(args.diagnostic),
            },
            "legacyManifest": str(legacy_manifest),
        },
        "scientificStatus": {
            "atlasReady": True,
            "physicalVolumeFlag": False,
            "label": "observed first-order-distance density volume",
        },
    }
    manifest_path = args.output.with_suffix(args.output.suffix + ".manifest.json")
    write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a browser-ready 3D density volume from the Oden author-supplied RC catalog."
    )
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--diagnostic", type=Path, default=DEFAULT_DIAGNOSTIC)
    parser.add_argument("--legacy-dir", type=Path, default=DEFAULT_LEGACY_DIR)
    parser.add_argument("--voxel-size-kpc", type=float, default=0.5)
    parser.add_argument("--smoothing-sigma-voxels", type=float, default=0.8)
    parser.add_argument("--density-reference-quantile", type=float, default=0.995)
    return parser.parse_args()


def main() -> None:
    manifest = build(parse_args())
    print(json.dumps(manifest, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
