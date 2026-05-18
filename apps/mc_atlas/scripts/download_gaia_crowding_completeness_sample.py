from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import download_xmc_rc_gaia_calibrated as gaia


ROOT = Path(__file__).resolve().parents[1]
RAW_GAIA = ROOT / "data" / "raw" / "gaia"
PROCESSED = ROOT / "data" / "processed"

DEFAULT_CHUNK_DIR = RAW_GAIA / "crowding_completeness_chunks"
DEFAULT_OUTPUT = PROCESSED / "gaia_crowding_completeness_sample.csv"

SAMPLE_COLUMNS = (
    "source_id",
    "ra",
    "dec",
    "l",
    "b",
    "phot_g_mean_mag",
    "bp_rp",
    "phot_bp_rp_excess_factor",
    "pmra",
    "pmdec",
    "parallax",
    "parallax_over_error",
    "ruwe",
    "astrometric_excess_noise",
)


@dataclass(frozen=True)
class Region:
    name: str
    ra_deg: float
    dec_deg: float
    radius_deg: float


REGIONS = {
    "LMC_INNER": Region("LMC_INNER", 80.44, -69.87, 3.0),
    "SMC_INNER": Region("SMC_INNER", 13.05, -72.83, 2.0),
}


def chunk_bounds(index: int, chunk_count: int) -> tuple[int, int]:
    lower = math.floor(gaia.GAIA_DR3_SOURCE_COUNT * index / chunk_count)
    upper = math.floor(gaia.GAIA_DR3_SOURCE_COUNT * (index + 1) / chunk_count)
    if index == chunk_count - 1:
        upper = gaia.GAIA_DR3_SOURCE_COUNT
    return lower, upper


def parse_regions(value: str) -> list[str]:
    out = []
    for raw in value.split(","):
        name = raw.strip().upper()
        if not name:
            continue
        if name not in REGIONS:
            raise argparse.ArgumentTypeError(f"unknown region {raw!r}; expected one of {', '.join(REGIONS)}")
        if name not in out:
            out.append(name)
    if not out:
        raise argparse.ArgumentTypeError("at least one region is required")
    return out


def chunk_path(args: argparse.Namespace, region: str, index: int) -> Path:
    kind = "count" if args.count_only else "rows"
    return args.chunk_dir / f"{region.lower()}_{kind}_ri{args.chunk_count:05d}_{index:05d}.csv"


def manifest_path(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".json")


def spatial_condition(region_name: str) -> str:
    region = REGIONS[region_name]
    return f"""CONTAINS(
    POINT('ICRS', ra, dec),
    CIRCLE('ICRS', {region.ra_deg:.8f}, {region.dec_deg:.8f}, {region.radius_deg:.8f})
  ) = 1"""


def build_query(args: argparse.Namespace, region: str, lower: int, upper: int, *, count_only: bool | None = None) -> str:
    if count_only is None:
        count_only = bool(args.count_only)
    select_clause = "COUNT(*) AS row_count" if count_only else ",\n  ".join(SAMPLE_COLUMNS)
    parallax_filter = "" if args.keep_nearby else f"\n  AND (parallax IS NULL OR parallax_over_error < {args.parallax_over_error_max:.6f})"
    return f"""
SELECT
  {select_clause}
FROM gaiadr3.gaia_source
WHERE
  random_index >= {lower:d}
  AND random_index < {upper:d}
  AND {spatial_condition(region)}
  AND phot_g_mean_mag BETWEEN {args.g_min:.6f} AND {args.g_max:.6f}
  AND bp_rp BETWEEN {args.bp_rp_min:.6f} AND {args.bp_rp_max:.6f}
  AND ruwe < {args.ruwe_max:.6f}
  AND astrometric_excess_noise < {args.astrometric_excess_noise_max:.6f}
{parallax_filter}
"""


def validate_header(path: Path, expected: tuple[str, ...]) -> None:
    gaia.validate_csv_header(path, expected)


def count_csv_rows(path: Path) -> int:
    return gaia.count_csv_rows(path)


def read_count_result(path: Path) -> int:
    validate_header(path, ("row_count",))
    with path.open("r", encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))
    return int(float(row["row_count"]))


def chunk_complete(args: argparse.Namespace, path: Path, expected: tuple[str, ...], region: str, index: int, lower: int, upper: int) -> bool:
    mpath = manifest_path(path)
    if not path.exists() or not mpath.exists():
        return False
    try:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
        validate_header(path, expected)
        return (
            manifest.get("status") == "completed"
            and manifest.get("region") == region
            and int(manifest.get("chunk", -1)) == index
            and int(manifest.get("lowerRandomIndex", -1)) == lower
            and int(manifest.get("upperRandomIndex", -1)) == upper
            and manifest.get("query") == build_query(args, region, lower, upper).strip()
        )
    except (OSError, ValueError, json.JSONDecodeError):
        return False


def write_manifest(path: Path, payload: dict[str, object]) -> None:
    manifest_path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_tag(args: argparse.Namespace) -> str:
    return f"ri{args.chunk_count:05d}_{args.chunk_start:05d}_{args.chunk_end:05d}"


def run_manifest_path(args: argparse.Namespace) -> Path:
    if args.count_only:
        return args.output.with_name(f"{args.output.stem}_counts_{run_tag(args)}{args.output.suffix}.manifest.json")
    if args.chunk_start == 0 and args.chunk_end == args.chunk_count:
        return args.output.with_suffix(args.output.suffix + ".manifest.json")
    return args.output.with_name(f"{args.output.stem}_{run_tag(args)}{args.output.suffix}.manifest.json")


def run_chunk(args: argparse.Namespace, region: str, index: int, lower: int, upper: int, expected: tuple[str, ...]) -> tuple[str, int, Path, int]:
    path = chunk_path(args, region, index)
    if not args.force and chunk_complete(args, path, expected, region, index, lower, upper):
        rows = read_count_result(path) if args.count_only else count_csv_rows(path)
        print(f"skip complete {region} chunk {index}: {rows:,} rows", flush=True)
        return region, index, path, rows
    path.parent.mkdir(parents=True, exist_ok=True)
    query = build_query(args, region, lower, upper)
    if args.tap_mode == "sync":
        result = gaia.tap_sync_query_to_file(query, path, args.timeout, args.maxrec, expected)
    else:
        result = gaia.tap_async_query_to_file(query, path, args.timeout, args.poll_seconds, args.maxrec, expected)
    rows = int(result["rows"])
    if args.count_only:
        rows = read_count_result(path)
    write_manifest(
        path,
        {
            "status": "completed",
            "region": region,
            "chunk": index,
            "chunkCount": args.chunk_count,
            "lowerRandomIndex": lower,
            "upperRandomIndex": upper,
            "rows": rows,
            "countOnly": bool(args.count_only),
            "query": query.strip(),
        },
    )
    print(f"downloaded {region} chunk {index}: {rows:,} rows", flush=True)
    return region, index, path, rows


def run_chunk_with_retries(
    args: argparse.Namespace,
    region: str,
    index: int,
    lower: int,
    upper: int,
    expected: tuple[str, ...],
) -> tuple[str, int, Path, int]:
    for attempt in range(args.retries + 1):
        try:
            return run_chunk(args, region, index, lower, upper, expected)
        except Exception as error:
            path = chunk_path(args, region, index)
            if attempt >= args.retries:
                write_manifest(
                    path,
                    {
                        "status": "failed",
                        "region": region,
                        "chunk": index,
                        "chunkCount": args.chunk_count,
                        "lowerRandomIndex": lower,
                        "upperRandomIndex": upper,
                        "countOnly": bool(args.count_only),
                        "query": build_query(args, region, lower, upper).strip(),
                        "error": repr(error),
                        "updatedUnixSeconds": time.time(),
                    },
                )
                raise
            delay = args.retry_seconds * (attempt + 1)
            print(
                f"{region} chunk {index} failed on attempt {attempt + 1}/{args.retries + 1}: "
                f"{error!r}; retrying in {delay:.1f}s",
                flush=True,
            )
            time.sleep(delay)
    raise RuntimeError("unreachable retry state")


def concatenate(records: list[tuple[str, int, Path, int]], output: Path, expected: tuple[str, ...]) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    part = output.with_suffix(output.suffix + ".part")
    seen: set[str] = set()
    rows = 0
    source_index = expected.index("source_id")
    with part.open("w", encoding="utf-8", newline="") as out_handle:
        writer = csv.writer(out_handle, lineterminator="\n")
        writer.writerow(("region",) + expected)
        for region, _, path, _ in sorted(records, key=lambda item: (item[0], item[1])):
            validate_header(path, expected)
            with path.open("r", encoding="utf-8", newline="") as in_handle:
                reader = csv.reader(in_handle)
                next(reader, None)
                for row in reader:
                    source_id = row[source_index]
                    if source_id in seen:
                        continue
                    seen.add(source_id)
                    writer.writerow((region,) + tuple(row))
                    rows += 1
    part.replace(output)
    return rows


def main() -> None:
    args = parse_args()
    args.chunk_dir.mkdir(parents=True, exist_ok=True)
    expected = ("row_count",) if args.count_only else SAMPLE_COLUMNS
    jobs = []
    for region in args.regions:
        for index in range(args.chunk_start, args.chunk_end):
            lower, upper = chunk_bounds(index, args.chunk_count)
            jobs.append((region, index, lower, upper))

    records: list[tuple[str, int, Path, int]] = []
    total = 0
    if args.workers <= 1:
        for region, index, lower, upper in jobs:
            record = run_chunk_with_retries(args, region, index, lower, upper, expected)
            records.append(record)
            total += record[3]
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = [
                executor.submit(run_chunk_with_retries, args, region, index, lower, upper, expected)
                for region, index, lower, upper in jobs
            ]
            for future in as_completed(futures):
                record = future.result()
                records.append(record)
                total += record[3]
    manifest = {
        "method": "gaia-crowding-completeness-sample",
        "source": "Gaia DR3 gaiadr3.gaia_source",
        "columns": list(expected),
        "regions": args.regions,
        "chunkCount": args.chunk_count,
        "chunkStart": args.chunk_start,
        "chunkEnd": args.chunk_end,
        "countOnly": bool(args.count_only),
        "rowsOrCount": int(total),
        "chunkDir": str(args.chunk_dir),
        "output": str(args.output),
        "queryParameters": {
            "g": [args.g_min, args.g_max],
            "bpRp": [args.bp_rp_min, args.bp_rp_max],
            "ruweMax": args.ruwe_max,
            "astrometricExcessNoiseMax": args.astrometric_excess_noise_max,
            "parallaxOverErrorMax": None if args.keep_nearby else args.parallax_over_error_max,
        },
    }
    if not args.count_only:
        if len(records) == len(args.regions) * args.chunk_count and args.chunk_start == 0 and args.chunk_end == args.chunk_count:
            manifest["deduplicatedRows"] = concatenate(records, args.output, expected)
    manifest_path = run_manifest_path(args)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2), flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download Gaia auxiliary data for RC crowding/completeness diagnostics.")
    parser.add_argument("--regions", type=parse_regions, default=list(REGIONS))
    parser.add_argument("--chunk-dir", type=Path, default=DEFAULT_CHUNK_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--chunk-count", type=int, default=200)
    parser.add_argument("--chunk-start", type=int, default=0)
    parser.add_argument("--chunk-end", type=int, default=None)
    parser.add_argument("--count-only", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--tap-mode", choices=("async", "sync"), default="async")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--poll-seconds", type=float, default=5.0)
    parser.add_argument("--maxrec", type=int, default=-1)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-seconds", type=float, default=45.0)
    parser.add_argument("--g-min", type=float, default=17.0)
    parser.add_argument("--g-max", type=float, default=21.2)
    parser.add_argument("--bp-rp-min", type=float, default=0.0)
    parser.add_argument("--bp-rp-max", type=float, default=4.75)
    parser.add_argument("--ruwe-max", type=float, default=1.4)
    parser.add_argument("--astrometric-excess-noise-max", type=float, default=2.5)
    parser.add_argument("--parallax-over-error-max", type=float, default=4.0)
    parser.add_argument("--keep-nearby", action="store_true")
    args = parser.parse_args()
    if args.chunk_count <= 0:
        raise ValueError("--chunk-count must be positive")
    if args.chunk_start < 0:
        raise ValueError("--chunk-start must be non-negative")
    if args.chunk_end is None:
        args.chunk_end = args.chunk_count
    if args.chunk_end < args.chunk_start or args.chunk_end > args.chunk_count:
        raise ValueError("--chunk-end must be between --chunk-start and --chunk-count")
    if args.workers <= 0:
        raise ValueError("--workers must be positive")
    return args


if __name__ == "__main__":
    main()
