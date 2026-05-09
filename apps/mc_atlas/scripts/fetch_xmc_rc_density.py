from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from urllib.parse import urljoin

import requests


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
DEFAULT_OUTPUT = PROCESSED / "xmc_rc_density_counts.json"

GAIA_TAP_SYNC = "https://gea.esac.esa.int/tap-server/tap/sync"
GAIA_TAP_ASYNC = "https://gea.esac.esa.int/tap-server/tap/async"
GAIA_DR3_SOURCE_COUNT = 1_811_709_771


def percentile(values: list[int], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    blend = position - lower
    return float(ordered[lower] * (1 - blend) + ordered[upper] * blend)


def build_query(args: argparse.Namespace) -> str:
    spatial_filter = """
      (
        CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 81.28, -69.78, 30.0)) = 1
        OR CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 13.10, -72.82, 15.0)) = 1
      )
    """

    pm_filter = ""
    if not args.no_pm:
        pm_filter = f"""
          AND pmra IS NOT NULL
          AND pmdec IS NOT NULL
          AND (
            POWER(pmra - ({args.lmc_pmra:.6f}), 2) + POWER(pmdec - ({args.lmc_pmdec:.6f}), 2) < POWER({args.pm_radius:.6f}, 2)
            OR POWER(pmra - ({args.smc_pmra:.6f}), 2) + POWER(pmdec - ({args.smc_pmdec:.6f}), 2) < POWER({args.pm_radius:.6f}, 2)
          )
        """

    sample_filter = ""
    if not args.full_scan:
        sample_filter = f"AND random_index < {random_index_max(args):d}"

    return f"""
SELECT lon_bin, lat_bin, COUNT(*) AS n
FROM (
  SELECT
    CAST(FLOOR(l * {args.bin_scale:d} + 0.5) AS INTEGER) AS lon_bin,
    CAST(FLOOR(b * {args.bin_scale:d} + 0.5) AS INTEGER) AS lat_bin
  FROM gaiadr3.gaia_source
  WHERE
    {spatial_filter}
    AND phot_g_mean_mag BETWEEN {args.g_min:.6f} AND {args.g_max:.6f}
    AND bp_rp BETWEEN {args.bp_rp_min:.6f} AND {args.bp_rp_max:.6f}
    AND ruwe < {args.ruwe_max:.6f}
    AND astrometric_excess_noise < {args.astrometric_excess_noise_max:.6f}
    AND parallax IS NOT NULL
    AND parallax_over_error < {args.parallax_over_error_max:.6f}
    {sample_filter}
    {pm_filter}
) AS rc_like
GROUP BY lon_bin, lat_bin
"""


def random_index_max(args: argparse.Namespace) -> int:
    if args.random_index_max is not None:
        return args.random_index_max
    return max(1, min(GAIA_DR3_SOURCE_COUNT, round(GAIA_DR3_SOURCE_COUNT * args.sample_fraction)))


def effective_sample_fraction(args: argparse.Namespace) -> float:
    if args.full_scan:
        return 1.0
    return random_index_max(args) / GAIA_DR3_SOURCE_COUNT


def sync_query(query: str, timeout: int) -> dict[str, object]:
    response = requests.post(
        GAIA_TAP_SYNC,
        data={
            "REQUEST": "doQuery",
            "LANG": "ADQL",
            "FORMAT": "json",
            "QUERY": query,
            "MAXREC": "1000000",
        },
        timeout=timeout,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(response.text) from error
    return response.json()


def async_query(query: str, timeout: int, poll_seconds: float) -> dict[str, object]:
    session = requests.Session()
    response = session.post(
        GAIA_TAP_ASYNC,
        data={
            "REQUEST": "doQuery",
            "LANG": "ADQL",
            "FORMAT": "json",
            "QUERY": query,
            "MAXREC": "1000000",
        },
        allow_redirects=False,
        timeout=60,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(response.text) from error

    job_url = response.headers.get("Location")
    if not job_url:
        job_url = response.url
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

    result = session.get(f"{job_url}/results/result", timeout=300)
    try:
        result.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(result.text) from error
    return result.json()


def normalize_result(raw: dict[str, object], args: argparse.Namespace, query: str) -> dict[str, object]:
    bins = []
    counts = []
    sample_counts = []
    sample_fraction = effective_sample_fraction(args)
    count_scale = 1.0 / sample_fraction
    for row in raw.get("data", []):
        lon_bin = int(row[0])
        lat_bin = int(row[1])
        sample_count = int(row[2])
        count = int(round(sample_count * count_scale))
        counts.append(count)
        sample_counts.append(sample_count)
        bins.append(
            {
                "lonBin": lon_bin,
                "latBin": lat_bin,
                "lonDeg": round(lon_bin / args.bin_scale, 6),
                "latDeg": round(lat_bin / args.bin_scale, 6),
                "count": count,
                "sampleCount": sample_count,
            }
        )

    bins.sort(key=lambda item: (item["latBin"], item["lonBin"]))
    return {
        "meta": {
            "source": "Gaia DR3 gaiadr3.gaia_source",
            "binScale": args.bin_scale,
            "binSizeDeg": round(1 / args.bin_scale, 6),
            "note": "Approximate XMC red-clump density proxy: server-side Gaia counts in galactic lon/lat bins after broad observed RC color/magnitude, astrometric-quality, parallax-SNR, and proper-motion cuts. Counts are scaled from the random_index sample unless fullScan is true.",
            "fullScan": args.full_scan,
            "sampleFraction": sample_fraction,
            "randomIndexMax": None if args.full_scan else random_index_max(args),
            "filters": {
                "gMag": [args.g_min, args.g_max],
                "bpRp": [args.bp_rp_min, args.bp_rp_max],
                "ruweMax": args.ruwe_max,
                "astrometricExcessNoiseMax": args.astrometric_excess_noise_max,
                "parallaxOverErrorMax": args.parallax_over_error_max,
                "properMotion": None
                if args.no_pm
                else {
                    "lmc": [args.lmc_pmra, args.lmc_pmdec],
                    "smc": [args.smc_pmra, args.smc_pmdec],
                    "radiusMasYr": args.pm_radius,
                },
            },
            "query": query.strip(),
            "stats": {
                "bins": len(bins),
                "sampleTotalCount": sum(sample_counts),
                "estimatedTotalCount": sum(counts),
                "medianCount": percentile(counts, 0.5),
                "p90Count": percentile(counts, 0.9),
                "p98Count": percentile(counts, 0.98),
                "maxCount": max(counts) if counts else 0,
            },
        },
        "bins": bins,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch an approximate red-clump density layer from Gaia DR3 as binned counts."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sync", action="store_true", help="Use Gaia TAP sync instead of async.")
    parser.add_argument("--dry-run", action="store_true", help="Print the ADQL query without submitting it.")
    parser.add_argument("--timeout", type=int, default=7200)
    parser.add_argument("--poll-seconds", type=float, default=15.0)
    parser.add_argument("--bin-scale", type=int, default=4, help="Bins per degree; 4 matches the XMC 0.25 deg grid.")
    parser.add_argument("--full-scan", action="store_true", help="Scan all Gaia rows instead of using random_index.")
    parser.add_argument("--sample-fraction", type=float, default=0.01, help="Gaia random_index fraction to scan.")
    parser.add_argument("--random-index-max", type=int, default=None, help="Override the random_index upper bound.")
    parser.add_argument("--g-min", type=float, default=18.0)
    parser.add_argument("--g-max", type=float, default=20.2)
    parser.add_argument("--bp-rp-min", type=float, default=0.55)
    parser.add_argument("--bp-rp-max", type=float, default=1.65)
    parser.add_argument("--ruwe-max", type=float, default=1.4)
    parser.add_argument("--astrometric-excess-noise-max", type=float, default=2.0)
    parser.add_argument("--parallax-over-error-max", type=float, default=4.0)
    parser.add_argument("--no-pm", action="store_true", help="Skip the broad MC proper-motion filter.")
    parser.add_argument("--pm-radius", type=float, default=2.5)
    parser.add_argument("--lmc-pmra", type=float, default=1.91)
    parser.add_argument("--lmc-pmdec", type=float, default=0.23)
    parser.add_argument("--smc-pmra", type=float, default=0.77)
    parser.add_argument("--smc-pmdec", type=float, default=-1.12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    query = build_query(args)
    if args.dry_run:
        print(query.strip())
        return

    raw = sync_query(query, args.timeout) if args.sync else async_query(query, args.timeout, args.poll_seconds)
    payload = normalize_result(raw, args, query)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload["meta"]["stats"], indent=2))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
