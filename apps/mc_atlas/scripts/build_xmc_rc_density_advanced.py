from __future__ import annotations

import argparse
import csv
import json
import math
import struct
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin

import numpy as np
import requests


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"

DEFAULT_SAMPLE = PROCESSED / "xmc_rc_gaia_sample_5pct.csv"
DEFAULT_OUTPUT = PROCESSED / "xmc_rc_density_counts.json"
REDDENING_FITS = RAW / "oden_ebv_3arcmin.fits"
REDDENING_URL = "https://raw.githubusercontent.com/slateroden/XMCreddeningmap/main/oden_ebv_3arcmin.fits"

GAIA_TAP_ASYNC = "https://gea.esac.esa.int/tap-server/tap/async"
GAIA_DR3_SOURCE_COUNT = 1_811_709_771

R_V = 3.1
A_G_PER_EBV = 0.73165 * R_V
E_BP_RP_PER_EBV = (1.02557 - 0.55644) * R_V

BIN_SCALE = 4


def percentile(values: list[int] | np.ndarray, fraction: float) -> float:
    if len(values) == 0:
        return 0.0
    return float(np.percentile(values, fraction * 100))


def random_index_max(sample_fraction: float) -> int:
    return max(1, min(GAIA_DR3_SOURCE_COUNT, round(GAIA_DR3_SOURCE_COUNT * sample_fraction)))


def build_row_query(args: argparse.Namespace) -> str:
    return f"""
SELECT
  l,
  b,
  phot_g_mean_mag,
  bp_rp,
  pmra,
  pmdec
FROM gaiadr3.gaia_source
WHERE
  (
    CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 81.28, -69.78, 30.0)) = 1
    OR CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 13.10, -72.82, 15.0)) = 1
  )
  AND random_index < {random_index_max(args.sample_fraction):d}
  AND phot_g_mean_mag BETWEEN {args.query_g_min:.6f} AND {args.query_g_max:.6f}
  AND bp_rp BETWEEN {args.query_bp_rp_min:.6f} AND {args.query_bp_rp_max:.6f}
  AND ruwe < {args.ruwe_max:.6f}
  AND astrometric_excess_noise < {args.astrometric_excess_noise_max:.6f}
  AND parallax IS NOT NULL
  AND parallax_over_error < {args.parallax_over_error_max:.6f}
  AND pmra IS NOT NULL
  AND pmdec IS NOT NULL
  AND (
    POWER(pmra - ({args.lmc_pmra:.6f}), 2) + POWER(pmdec - ({args.lmc_pmdec:.6f}), 2) < POWER({args.query_pm_radius:.6f}, 2)
    OR POWER(pmra - ({args.smc_pmra:.6f}), 2) + POWER(pmdec - ({args.smc_pmdec:.6f}), 2) < POWER({args.query_pm_radius:.6f}, 2)
  )
"""


def tap_async_query_to_file(query: str, output: Path, timeout: int, poll_seconds: float, maxrec: int) -> None:
    session = requests.Session()
    response = session.post(
        GAIA_TAP_ASYNC,
        data={
            "REQUEST": "doQuery",
            "LANG": "ADQL",
            "FORMAT": "csv",
            "QUERY": query,
            "MAXREC": str(maxrec),
        },
        allow_redirects=False,
        timeout=60,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(response.text) from error

    job_url = response.headers.get("Location") or response.url
    job_url = urljoin(GAIA_TAP_ASYNC, job_url)
    print(f"Gaia TAP job: {job_url}", flush=True)

    phase_response = session.post(f"{job_url}/phase", data={"PHASE": "RUN"}, timeout=60)
    try:
        phase_response.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(phase_response.text) from error

    started = time.monotonic()
    while True:
        phase = session.get(f"{job_url}/phase", timeout=60).text.strip().upper()
        if phase == "COMPLETED":
            break
        if phase in {"ERROR", "ABORTED"}:
            error = session.get(f"{job_url}/error", timeout=60).text
            raise RuntimeError(f"Gaia TAP job ended with phase {phase}:\n{error}")
        if time.monotonic() - started > timeout:
            raise TimeoutError(f"Gaia TAP job did not complete within {timeout} seconds; job URL: {job_url}")
        print(f"Gaia TAP phase: {phase}", flush=True)
        time.sleep(poll_seconds)

    output.parent.mkdir(parents=True, exist_ok=True)
    with session.get(f"{job_url}/results/result", stream=True, timeout=300) as result:
        try:
            result.raise_for_status()
        except requests.HTTPError as error:
            raise RuntimeError(result.text) from error
        with output.open("wb") as handle:
            for chunk in result.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)


def download_reddening_map() -> None:
    if REDDENING_FITS.exists():
        return
    REDDENING_FITS.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(REDDENING_URL, stream=True, timeout=300) as response:
        response.raise_for_status()
        with REDDENING_FITS.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)


def parse_fits_header(raw: bytes) -> tuple[int, dict[str, str]]:
    cards: dict[str, str] = {}
    for offset in range(0, len(raw), 80):
        card = raw[offset : offset + 80].decode("ascii", errors="ignore")
        key = card[:8].strip()
        if key:
            cards[key] = card[10:30].strip()
        if key == "END":
            header_end = ((offset + 80 + 2879) // 2880) * 2880
            return header_end, cards
    raise ValueError(f"No FITS END card found in {REDDENING_FITS}")


def load_reddening_map() -> tuple[np.ndarray, dict[str, float]]:
    download_reddening_map()
    raw = REDDENING_FITS.read_bytes()
    header_end, cards = parse_fits_header(raw)
    n1 = int(cards["NAXIS1"])
    n2 = int(cards["NAXIS2"])
    data = np.frombuffer(raw, dtype=">f4", count=n1 * n2, offset=header_end).astype(np.float32)
    image = data.reshape((n2, n1))
    wcs = {
        "crpix1": float(cards["CRPIX1"]),
        "crpix2": float(cards["CRPIX2"]),
        "cdelt1": float(cards["CDELT1"]),
        "cdelt2": float(cards["CDELT2"]),
        "crval1": float(cards["CRVAL1"]),
        "crval2": float(cards["CRVAL2"]),
    }
    return image, wcs


def reddening_at(lon: np.ndarray, lat: np.ndarray, image: np.ndarray, wcs: dict[str, float]) -> np.ndarray:
    x = (lon - wcs["crval1"]) / wcs["cdelt1"] + wcs["crpix1"] - 1
    y = (lat - wcs["crval2"]) / wcs["cdelt2"] + wcs["crpix2"] - 1
    x0 = np.floor(x).astype(int)
    y0 = np.floor(y).astype(int)
    x1 = x0 + 1
    y1 = y0 + 1
    valid = (x0 >= 0) & (y0 >= 0) & (x1 < image.shape[1]) & (y1 < image.shape[0])
    ebv = np.full(lon.shape, np.nan, dtype=np.float32)
    if not np.any(valid):
        return ebv

    xv = x[valid]
    yv = y[valid]
    x0v = x0[valid]
    y0v = y0[valid]
    dx = xv - x0v
    dy = yv - y0v
    v00 = image[y0v, x0v]
    v10 = image[y0v, x0v + 1]
    v01 = image[y0v + 1, x0v]
    v11 = image[y0v + 1, x0v + 1]
    ebv[valid] = (
        v00 * (1 - dx) * (1 - dy)
        + v10 * dx * (1 - dy)
        + v01 * (1 - dx) * dy
        + v11 * dx * dy
    )
    return ebv


def load_sample(path: Path) -> dict[str, np.ndarray]:
    columns: dict[str, list[float]] = defaultdict(list)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            for key in ("l", "b", "phot_g_mean_mag", "bp_rp", "pmra", "pmdec"):
                columns[key].append(float(row[key]))
    return {key: np.array(value, dtype=np.float64) for key, value in columns.items()}


def sky_bins(lon: np.ndarray, lat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return np.rint(lon * BIN_SCALE).astype(np.int32), np.rint(lat * BIN_SCALE).astype(np.int32)


def bin_key(x: int, y: int) -> tuple[int, int]:
    return (int(x), int(y))


def circular_offsets(radius: int) -> list[tuple[int, int]]:
    radius2 = radius * radius
    return [(dx, dy) for dy in range(-radius, radius + 1) for dx in range(-radius, radius + 1) if dx * dx + dy * dy <= radius2]


def robust_local_pm_filter(
    lon_bin: np.ndarray,
    lat_bin: np.ndarray,
    pmra: np.ndarray,
    pmdec: np.ndarray,
    local_parent_mask: np.ndarray,
    needed_mask: np.ndarray,
    args: argparse.Namespace,
) -> tuple[np.ndarray, dict[str, float | int]]:
    parent_indices_by_bin: dict[tuple[int, int], list[int]] = defaultdict(list)
    parent_indices = np.flatnonzero(local_parent_mask)
    for index in parent_indices:
        parent_indices_by_bin[bin_key(lon_bin[index], lat_bin[index])].append(int(index))

    needed_bins = sorted({bin_key(lon_bin[index], lat_bin[index]) for index in np.flatnonzero(needed_mask)})
    stat_by_bin: dict[tuple[int, int], tuple[float, float, float, int, int]] = {}
    offsets_by_radius = {radius: circular_offsets(radius) for radius in range(args.local_pm_min_radius_cells, args.local_pm_max_radius_cells + 1)}

    for key in needed_bins:
        gathered: list[int] = []
        used_radius = args.local_pm_max_radius_cells
        for radius in range(args.local_pm_min_radius_cells, args.local_pm_max_radius_cells + 1):
            gathered = []
            for dx, dy in offsets_by_radius[radius]:
                gathered.extend(parent_indices_by_bin.get((key[0] + dx, key[1] + dy), ()))
            if len(gathered) >= args.local_pm_min_neighbors:
                used_radius = radius
                break
        if len(gathered) < args.local_pm_absolute_min_neighbors:
            continue
        local_pmra = pmra[gathered]
        local_pmdec = pmdec[gathered]
        center_ra = float(np.median(local_pmra))
        center_dec = float(np.median(local_pmdec))
        radius_dist = np.sqrt((local_pmra - center_ra) ** 2 + (local_pmdec - center_dec) ** 2)
        sigma = max(float(np.percentile(radius_dist, 68)), args.local_pm_sigma_floor)
        stat_by_bin[key] = (center_ra, center_dec, sigma, len(gathered), used_radius)

    passes = np.zeros(len(pmra), dtype=bool)
    missing = 0
    for index in np.flatnonzero(needed_mask):
        stat = stat_by_bin.get(bin_key(lon_bin[index], lat_bin[index]))
        if stat is None:
            missing += 1
            continue
        center_ra, center_dec, sigma, _, _ = stat
        distance = math.hypot(float(pmra[index] - center_ra), float(pmdec[index] - center_dec))
        passes[index] = distance <= args.local_pm_sigma_scale * sigma

    radii = [stat[4] for stat in stat_by_bin.values()]
    neighbors = [stat[3] for stat in stat_by_bin.values()]
    return passes, {
        "localPmBins": len(stat_by_bin),
        "localPmMissingCandidateRows": missing,
        "localPmMedianRadiusCells": percentile(np.array(radii), 0.5) if radii else 0,
        "localPmP90RadiusCells": percentile(np.array(radii), 0.9) if radii else 0,
        "localPmMedianNeighbors": percentile(np.array(neighbors), 0.5) if neighbors else 0,
    }


def density_counts_from_sample(args: argparse.Namespace) -> dict[str, object]:
    sample = load_sample(args.sample)
    image, wcs = load_reddening_map()

    lon = sample["l"]
    lat = sample["b"]
    g = sample["phot_g_mean_mag"]
    bp_rp = sample["bp_rp"]
    pmra = sample["pmra"]
    pmdec = sample["pmdec"]

    ebv = reddening_at(lon, lat, image, wcs)
    valid_extinction = np.isfinite(ebv) & (ebv >= -0.05) & (ebv <= 2.0)
    g0 = g - A_G_PER_EBV * ebv
    color0 = bp_rp - E_BP_RP_PER_EBV * ebv

    local_parent = (
        valid_extinction
        & (g0 >= args.local_parent_g_min)
        & (g0 <= args.local_parent_g_max)
        & (color0 >= args.local_parent_bp_rp_min)
        & (color0 <= args.local_parent_bp_rp_max)
    )
    rc_cmd = valid_extinction & (
        (
            (g0 >= args.lmc_g0_min)
            & (g0 <= args.lmc_g0_max)
            & (color0 >= args.lmc_bp_rp0_min)
            & (color0 <= args.lmc_bp_rp0_max)
        )
        | (
            (g0 >= args.smc_g0_min)
            & (g0 <= args.smc_g0_max)
            & (color0 >= args.smc_bp_rp0_min)
            & (color0 <= args.smc_bp_rp0_max)
        )
    )

    lon_bin, lat_bin = sky_bins(lon, lat)
    local_pm_pass, local_pm_stats = robust_local_pm_filter(
        lon_bin,
        lat_bin,
        pmra,
        pmdec,
        local_parent,
        rc_cmd,
        args,
    )
    selected = rc_cmd & local_pm_pass

    count_scale = 1.0 / args.sample_fraction
    counts: dict[tuple[int, int], int] = defaultdict(int)
    sample_counts: dict[tuple[int, int], int] = defaultdict(int)
    for x, y in zip(lon_bin[selected], lat_bin[selected]):
        key = bin_key(x, y)
        sample_counts[key] += 1

    for key, count in sample_counts.items():
        counts[key] = int(round(count * count_scale))

    count_values = list(counts.values())
    bins = [
        {
            "lonBin": key[0],
            "latBin": key[1],
            "lonDeg": round(key[0] / BIN_SCALE, 6),
            "latDeg": round(key[1] / BIN_SCALE, 6),
            "count": count,
            "sampleCount": sample_counts[key],
        }
        for key, count in counts.items()
    ]
    bins.sort(key=lambda item: (item["latBin"], item["lonBin"]))

    return {
        "meta": {
            "source": "Gaia DR3 gaiadr3.gaia_source + Oden et al. XMC reddening map",
            "binScale": BIN_SCALE,
            "binSizeDeg": round(1 / BIN_SCALE, 6),
            "note": "Approximate XMC red-clump density proxy from a Gaia random_index sample. Gaia rows are dereddened with the public Oden E(B-V) map, selected with fixed dereddened LMC/SMC red-clump CMD boxes, and filtered with an adaptive local proper-motion cut.",
            "method": "5pct-extinction-aware-cmd-local-pm",
            "sampleFraction": args.sample_fraction,
            "randomIndexMax": random_index_max(args.sample_fraction),
            "countScale": count_scale,
            "query": build_row_query(args).strip(),
            "filters": {
                "queryG": [args.query_g_min, args.query_g_max],
                "queryBpRp": [args.query_bp_rp_min, args.query_bp_rp_max],
                "queryPmRadiusMasYr": args.query_pm_radius,
                "parallaxOverErrorMax": args.parallax_over_error_max,
                "localParentG0": [args.local_parent_g_min, args.local_parent_g_max],
                "localParentBpRp0": [args.local_parent_bp_rp_min, args.local_parent_bp_rp_max],
                "lmcRcBox": {
                    "g0": [args.lmc_g0_min, args.lmc_g0_max],
                    "bpRp0": [args.lmc_bp_rp0_min, args.lmc_bp_rp0_max],
                },
                "smcRcBox": {
                    "g0": [args.smc_g0_min, args.smc_g0_max],
                    "bpRp0": [args.smc_bp_rp0_min, args.smc_bp_rp0_max],
                },
                "localPm": {
                    "sigmaScale": args.local_pm_sigma_scale,
                    "sigmaFloorMasYr": args.local_pm_sigma_floor,
                    "minNeighbors": args.local_pm_min_neighbors,
                    "absoluteMinNeighbors": args.local_pm_absolute_min_neighbors,
                    "radiusCells": [args.local_pm_min_radius_cells, args.local_pm_max_radius_cells],
                    **local_pm_stats,
                },
                "extinction": {
                    "reddeningMap": str(REDDENING_FITS.relative_to(ROOT)),
                    "aGPerEbv": A_G_PER_EBV,
                    "eBpRpPerEbv": E_BP_RP_PER_EBV,
                },
            },
            "stats": {
                "sampleRows": int(len(lon)),
                "validExtinctionRows": int(np.count_nonzero(valid_extinction)),
                "localParentRows": int(np.count_nonzero(local_parent)),
                "rcCmdRows": int(np.count_nonzero(rc_cmd)),
                "localPmPassRows": int(np.count_nonzero(rc_cmd & local_pm_pass)),
                "bins": len(bins),
                "sampleTotalCount": int(np.count_nonzero(selected)),
                "estimatedTotalCount": int(sum(count_values)),
                "medianCount": percentile(np.array(count_values), 0.5),
                "p90Count": percentile(np.array(count_values), 0.9),
                "p98Count": percentile(np.array(count_values), 0.98),
                "maxCount": max(count_values) if count_values else 0,
            },
        },
        "bins": bins,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a 5% Gaia DR3 XMC red-clump density proxy with dereddened CMD cuts and local PM filtering."
    )
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sample-fraction", type=float, default=0.05)
    parser.add_argument("--timeout", type=int, default=14400)
    parser.add_argument("--poll-seconds", type=float, default=30.0)
    parser.add_argument("--maxrec", type=int, default=2_500_000)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--reuse-sample", action="store_true")
    parser.add_argument("--fetch-only", action="store_true")
    parser.add_argument("--process-only", action="store_true")
    parser.add_argument("--query-g-min", type=float, default=17.0)
    parser.add_argument("--query-g-max", type=float, default=20.35)
    parser.add_argument("--query-bp-rp-min", type=float, default=0.2)
    parser.add_argument("--query-bp-rp-max", type=float, default=2.0)
    parser.add_argument("--ruwe-max", type=float, default=1.4)
    parser.add_argument("--astrometric-excess-noise-max", type=float, default=2.0)
    parser.add_argument("--parallax-over-error-max", type=float, default=4.0)
    parser.add_argument("--query-pm-radius", type=float, default=4.0)
    parser.add_argument("--lmc-pmra", type=float, default=1.91)
    parser.add_argument("--lmc-pmdec", type=float, default=0.23)
    parser.add_argument("--smc-pmra", type=float, default=0.77)
    parser.add_argument("--smc-pmdec", type=float, default=-1.12)
    parser.add_argument("--local-parent-g-min", type=float, default=17.0)
    parser.add_argument("--local-parent-g-max", type=float, default=20.2)
    parser.add_argument("--local-parent-bp-rp-min", type=float, default=0.55)
    parser.add_argument("--local-parent-bp-rp-max", type=float, default=1.45)
    parser.add_argument("--lmc-g0-min", type=float, default=18.25)
    parser.add_argument("--lmc-g0-max", type=float, default=19.25)
    parser.add_argument("--lmc-bp-rp0-min", type=float, default=0.83)
    parser.add_argument("--lmc-bp-rp0-max", type=float, default=1.07)
    parser.add_argument("--smc-g0-min", type=float, default=18.4)
    parser.add_argument("--smc-g0-max", type=float, default=19.7)
    parser.add_argument("--smc-bp-rp0-min", type=float, default=0.77)
    parser.add_argument("--smc-bp-rp0-max", type=float, default=1.07)
    parser.add_argument("--local-pm-sigma-scale", type=float, default=2.0)
    parser.add_argument("--local-pm-sigma-floor", type=float, default=0.12)
    parser.add_argument("--local-pm-min-neighbors", type=int, default=35)
    parser.add_argument("--local-pm-absolute-min-neighbors", type=int, default=12)
    parser.add_argument("--local-pm-min-radius-cells", type=int, default=1)
    parser.add_argument("--local-pm-max-radius-cells", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    query = build_row_query(args)
    if args.dry_run:
        print(query.strip())
        return

    if args.process_only and not args.sample.exists():
        raise FileNotFoundError(args.sample)

    if not args.process_only and not (args.reuse_sample and args.sample.exists()):
        tap_async_query_to_file(query, args.sample, args.timeout, args.poll_seconds, args.maxrec)
        print(f"Wrote Gaia sample {args.sample}", flush=True)

    if args.fetch_only:
        return

    payload = density_counts_from_sample(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload["meta"]["stats"], indent=2))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
