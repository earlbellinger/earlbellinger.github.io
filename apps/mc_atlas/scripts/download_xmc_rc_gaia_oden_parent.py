from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import download_xmc_rc_gaia_calibrated as gaia


ROOT = gaia.ROOT
PROCESSED = ROOT / "data" / "processed"
RAW_GAIA = ROOT / "data" / "raw" / "gaia"

DEFAULT_CHUNK_DIR = RAW_GAIA / "xmc_rc_gaia_oden_parent_chunks"
DEFAULT_OUTPUT = PROCESSED / "xmc_rc_gaia_oden_parent.csv"
COUNT_COLUMNS = ("row_count",)


@dataclass(frozen=True)
class OdenRegion:
    name: str
    ra_deg: float
    dec_deg: float
    radius_deg: float
    description: str


REGIONS = {
    "PRIMARY": OdenRegion(
        name="PRIMARY",
        ra_deg=81.28,
        dec_deg=-69.78,
        radius_deg=30.0,
        description="Oden main 30 degree LMC/XMC circle",
    ),
    "SMC_SUPPLEMENT": OdenRegion(
        name="SMC_SUPPLEMENT",
        ra_deg=13.10,
        dec_deg=-72.82,
        radius_deg=15.0,
        description="Oden supplementary 15 degree SMC circle",
    ),
}


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_region_list(value: str) -> list[str]:
    aliases = {
        "LMC": "PRIMARY",
        "SMC": "SMC_SUPPLEMENT",
        "MAIN": "PRIMARY",
        "SUPPLEMENT": "SMC_SUPPLEMENT",
    }
    regions: list[str] = []
    for raw in value.split(","):
        name = raw.strip().upper().replace("-", "_")
        if not name:
            continue
        name = aliases.get(name, name)
        if name not in REGIONS:
            choices = ", ".join(REGIONS)
            raise argparse.ArgumentTypeError(f"unknown Oden region {raw!r}; expected {choices}")
        if name not in regions:
            regions.append(name)
    if not regions:
        raise argparse.ArgumentTypeError("at least one Oden region is required")
    return regions


def chunk_path_for(args: argparse.Namespace, region: str, index: int) -> Path:
    table_tag = args.table.replace("-", "_")
    query_tag = "count" if args.count_only else "rows"
    return args.chunk_dir / f"{table_tag}_{region.lower()}_{query_tag}_ri{args.chunk_count:05d}_{index:05d}.csv"


def manifest_path_for_chunk(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".json")


def count_csv_rows(path: Path) -> int:
    return gaia.count_csv_rows(path)


def validate_csv_header(path: Path, expected_columns: tuple[str, ...]) -> None:
    gaia.validate_csv_header(path, expected_columns)


def read_count_result(path: Path) -> int:
    validate_csv_header(path, COUNT_COLUMNS)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        row = next(reader, None)
    if row is None:
        raise ValueError(f"{path} did not contain a row_count result")
    return int(float(row["row_count"]))


def write_chunk_manifest(path: Path, payload: dict[str, object]) -> None:
    manifest_path_for_chunk(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def output_manifest_path(args: argparse.Namespace) -> Path:
    if args.count_only:
        return args.output.with_name(f"{args.output.stem}_counts{args.output.suffix}.manifest.json")
    return args.output.with_suffix(args.output.suffix + ".manifest.json")


def spatial_condition(args: argparse.Namespace, region_name: str) -> str:
    region = REGIONS[region_name]
    ra = float(getattr(args, f"{region_name.lower()}_ra"))
    dec = float(getattr(args, f"{region_name.lower()}_dec"))
    radius = float(getattr(args, f"{region_name.lower()}_radius"))
    return f"""CONTAINS(
    POINT('ICRS', ra, dec),
    CIRCLE('ICRS', {ra:.8f}, {dec:.8f}, {radius:.8f})
  ) = 1"""


def build_query(
    args: argparse.Namespace,
    region: str,
    lower_random_index: int,
    upper_random_index: int,
    *,
    count_only: bool | None = None,
) -> str:
    if count_only is None:
        count_only = bool(args.count_only)

    select_clause = "COUNT(*) AS row_count" if count_only else ",\n  ".join(gaia.table_columns(args.table))
    astrometric_excess_noise_filter = ""
    if args.table == "source" and not args.no_astrometric_excess_noise_cut:
        astrometric_excess_noise_filter = (
            f"\n  AND astrometric_excess_noise < {args.astrometric_excess_noise_max:.6f}"
        )

    parallax_over_error_filter = ""
    if not args.no_parallax_over_error_cut:
        parallax_over_error_filter = f"\n  AND parallax_over_error < {args.parallax_over_error_max:.6f}"

    return f"""
SELECT
  {select_clause}
FROM {gaia.TABLES[args.table]}
WHERE
  random_index >= {lower_random_index:d}
  AND random_index < {upper_random_index:d}
  AND {spatial_condition(args, region)}
  AND phot_g_mean_mag BETWEEN {args.query_g_min:.6f} AND {args.query_g_max:.6f}
  AND bp_rp BETWEEN {args.query_bp_rp_min:.6f} AND {args.query_bp_rp_max:.6f}
  AND ruwe < {args.ruwe_max:.6f}
{astrometric_excess_noise_filter}
  AND parallax IS NOT NULL
{parallax_over_error_filter}
  AND pmra IS NOT NULL
  AND pmdec IS NOT NULL
"""


def chunk_is_complete(
    path: Path,
    expected_columns: tuple[str, ...],
    args: argparse.Namespace,
    region: str,
    chunk_index: int,
    lower_random_index: int,
    upper_random_index: int,
) -> bool:
    manifest_path = manifest_path_for_chunk(path)
    if not path.exists() or not manifest_path.exists():
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_csv_header(path, expected_columns)
        if manifest.get("status") != "completed":
            return False
        if manifest.get("region") != region or int(manifest.get("chunk", -1)) != chunk_index:
            return False
        if int(manifest.get("chunkCount", -1)) != args.chunk_count:
            return False
        if manifest.get("sourceTable") != gaia.TABLES[args.table]:
            return False
        if bool(manifest.get("countOnly")) != bool(args.count_only):
            return False
        if int(manifest.get("lowerRandomIndex", -1)) != lower_random_index:
            return False
        if int(manifest.get("upperRandomIndex", -1)) != upper_random_index:
            return False
        query = build_query(args, region, lower_random_index, upper_random_index).strip()
        if manifest.get("query") != query:
            return False
        if args.count_only:
            return count_csv_rows(path) == 1 and int(manifest.get("rows", -1)) == read_count_result(path)
        return int(manifest.get("rows", -1)) == count_csv_rows(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return False


def execute_tap_query(
    args: argparse.Namespace,
    query: str,
    output: Path,
    expected_columns: tuple[str, ...],
) -> dict[str, object]:
    if args.tap_mode == "sync":
        return gaia.tap_sync_query_to_file(query, output, args.timeout, args.maxrec, expected_columns)
    return gaia.tap_async_query_to_file(
        query,
        output,
        args.timeout,
        args.poll_seconds,
        args.maxrec,
        expected_columns,
    )


def concatenate_chunks(
    chunk_records: list[tuple[str, int, Path]],
    output: Path,
    expected_columns: tuple[str, ...],
    *,
    force: bool = False,
) -> dict[str, int]:
    if output.exists() and not force:
        print(f"Output already exists; leaving it in place: {output}", flush=True)
        return {
            "rows": count_csv_rows(output),
            "duplicateSourceIds": 0,
        }

    output.parent.mkdir(parents=True, exist_ok=True)
    part_path = output.with_suffix(output.suffix + ".part")
    source_id_index = expected_columns.index("source_id")
    total_rows = 0
    duplicates = 0
    seen_source_ids: set[str] = set()

    with part_path.open("w", encoding="utf-8", newline="") as out_handle:
        writer = csv.writer(out_handle, lineterminator="\n")
        writer.writerow(("region",) + expected_columns)
        for region, _, chunk in chunk_records:
            validate_csv_header(chunk, expected_columns)
            with chunk.open("r", encoding="utf-8", newline="") as in_handle:
                reader = csv.reader(in_handle)
                next(reader, None)
                for row in reader:
                    source_id = row[source_id_index]
                    if source_id in seen_source_ids:
                        duplicates += 1
                        continue
                    seen_source_ids.add(source_id)
                    writer.writerow((region,) + tuple(row))
                    total_rows += 1

    part_path.replace(output)
    return {
        "rows": total_rows,
        "duplicateSourceIds": duplicates,
    }


def filters_manifest(args: argparse.Namespace) -> dict[str, object]:
    return {
        "queryG": [args.query_g_min, args.query_g_max],
        "queryBpRp": [args.query_bp_rp_min, args.query_bp_rp_max],
        "ruweMax": args.ruwe_max,
        "parallaxRequired": True,
        "parallaxOverErrorMax": None if args.no_parallax_over_error_cut else args.parallax_over_error_max,
        "pmraPmdecRequired": True,
        "astrometricExcessNoiseMax": (
            None
            if args.table != "source" or args.no_astrometric_excess_noise_cut
            else args.astrometric_excess_noise_max
        ),
        "properMotionCut": None,
        "footprints": {
            name: {
                "raDeg": float(getattr(args, f"{name.lower()}_ra")),
                "decDeg": float(getattr(args, f"{name.lower()}_dec")),
                "radiusDeg": float(getattr(args, f"{name.lower()}_radius")),
                "description": REGIONS[name].description,
            }
            for name in args.regions
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download the broad Gaia DR3 parent catalog matching the Oden et al. "
            "2025 red-clump parent query. This intentionally does not apply "
            "the Oden global or local proper-motion cuts."
        )
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--chunk-dir", type=Path, default=DEFAULT_CHUNK_DIR)
    parser.add_argument("--table", choices=tuple(gaia.TABLES), default="source")
    parser.add_argument("--regions", type=parse_region_list, default=parse_region_list("PRIMARY,SMC_SUPPLEMENT"))
    parser.add_argument("--chunk-count", type=int, default=4000)
    parser.add_argument("--start-chunk", type=int, default=0)
    parser.add_argument("--stop-chunk", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--poll-seconds", type=float, default=20.0)
    parser.add_argument("--maxrec", type=int, default=250_000)
    parser.add_argument("--tap-mode", choices=("sync", "async"), default="sync")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--count-only", action="store_true")
    parser.add_argument("--no-concat", action="store_true")
    parser.add_argument("--allow-partial-concat", action="store_true")
    parser.add_argument("--query-g-min", type=float, default=17.0)
    parser.add_argument("--query-g-max", type=float, default=20.25)
    parser.add_argument("--query-bp-rp-min", type=float, default=0.0)
    parser.add_argument("--query-bp-rp-max", type=float, default=4.75)
    parser.add_argument("--ruwe-max", type=float, default=1.4)
    parser.add_argument("--astrometric-excess-noise-max", type=float, default=2.5)
    parser.add_argument("--no-astrometric-excess-noise-cut", action="store_true")
    parser.add_argument("--parallax-over-error-max", type=float, default=4.0)
    parser.add_argument("--no-parallax-over-error-cut", action="store_true")
    parser.add_argument("--primary-ra", type=float, default=REGIONS["PRIMARY"].ra_deg)
    parser.add_argument("--primary-dec", type=float, default=REGIONS["PRIMARY"].dec_deg)
    parser.add_argument("--primary-radius", type=float, default=REGIONS["PRIMARY"].radius_deg)
    parser.add_argument("--smc-supplement-ra", type=float, default=REGIONS["SMC_SUPPLEMENT"].ra_deg)
    parser.add_argument("--smc-supplement-dec", type=float, default=REGIONS["SMC_SUPPLEMENT"].dec_deg)
    parser.add_argument("--smc-supplement-radius", type=float, default=REGIONS["SMC_SUPPLEMENT"].radius_deg)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.chunk_count <= 0:
        raise ValueError("--chunk-count must be positive")
    if args.start_chunk < 0:
        raise ValueError("--start-chunk must be non-negative")
    stop_chunk = args.stop_chunk if args.stop_chunk is not None else args.chunk_count
    if stop_chunk < args.start_chunk or stop_chunk > args.chunk_count:
        raise ValueError("--stop-chunk must be between --start-chunk and --chunk-count")
    if args.table != "source" and not args.no_astrometric_excess_noise_cut:
        print("source-lite has no astrometric_excess_noise column; omitting that Oden quality cut.", flush=True)

    expected_columns = COUNT_COLUMNS if args.count_only else gaia.table_columns(args.table)
    bounds = gaia.chunk_bounds(args.chunk_count)
    selected_indices = list(range(args.start_chunk, stop_chunk))
    selected_records = [
        (region, index, chunk_path_for(args, region, index), bounds[index][0], bounds[index][1])
        for region in args.regions
        for index in selected_indices
    ]

    if args.dry_run:
        for region, index, _, lower, upper in selected_records:
            print(f"-- {region} chunk {index:05d}: random_index [{lower}, {upper})")
            print(build_query(args, region, lower, upper).strip())
            print()
        return

    args.chunk_dir.mkdir(parents=True, exist_ok=True)
    completed_rows_this_run = 0
    for region, index, chunk_path, lower, upper in selected_records:
        if not args.force and chunk_is_complete(chunk_path, expected_columns, args, region, index, lower, upper):
            rows = read_count_result(chunk_path) if args.count_only else count_csv_rows(chunk_path)
            completed_rows_this_run += rows
            print(f"{region} chunk {index:05d} already complete: {rows} rows", flush=True)
            continue

        print(
            f"Downloading {region} chunk {index:05d}/{args.chunk_count - 1:05d}: "
            f"random_index [{lower}, {upper})",
            flush=True,
        )
        query = build_query(args, region, lower, upper)
        try:
            result = execute_tap_query(args, query, chunk_path, expected_columns)
        except Exception:
            write_chunk_manifest(
                chunk_path,
                {
                    "status": "failed",
                    "region": region,
                    "chunk": index,
                    "chunkCount": args.chunk_count,
                    "countOnly": args.count_only,
                    "lowerRandomIndex": lower,
                    "upperRandomIndex": upper,
                    "sourceTable": gaia.TABLES[args.table],
                    "query": query.strip(),
                    "updatedUnixSeconds": time.time(),
                },
            )
            raise

        csv_rows = int(result["rows"])
        scientific_rows = read_count_result(chunk_path) if args.count_only else csv_rows
        result.update(
            {
                "region": region,
                "chunk": index,
                "chunkCount": args.chunk_count,
                "countOnly": args.count_only,
                "lowerRandomIndex": lower,
                "upperRandomIndex": upper,
                "sourceTable": gaia.TABLES[args.table],
                "columns": list(expected_columns),
                "rows": scientific_rows,
                "csvRows": csv_rows,
                "query": query.strip(),
                "updatedUnixSeconds": time.time(),
            }
        )
        write_chunk_manifest(chunk_path, result)
        completed_rows_this_run += scientific_rows
        print(
            f"{region} chunk {index:05d} complete: {scientific_rows} rows, {result['bytes']} bytes",
            flush=True,
        )

    all_records = [
        (region, index, chunk_path_for(args, region, index), lower, upper)
        for region in args.regions
        for index, (lower, upper) in enumerate(bounds)
    ]
    complete_records = [
        (region, index, path)
        for region, index, path, lower, upper in all_records
        if chunk_is_complete(path, expected_columns, args, region, index, lower, upper)
    ]

    expected_chunks = len(args.regions) * args.chunk_count
    if args.count_only:
        complete_rows = sum(read_count_result(path) for _, _, path in complete_records)
    else:
        complete_rows = sum(count_csv_rows(path) for _, _, path in complete_records)

    manifest: dict[str, object] = {
        "source": "Gaia DR3",
        "method": "oden-2025-broad-parent-gaia-download-split-region-random-index",
        "sourceTable": gaia.TABLES[args.table],
        "columns": ["region", *gaia.table_columns(args.table)] if not args.count_only else list(COUNT_COLUMNS),
        "regions": args.regions,
        "countOnly": args.count_only,
        "tapMode": args.tap_mode,
        "chunkCount": args.chunk_count,
        "expectedChunks": expected_chunks,
        "completeChunks": len(complete_records),
        "completeRowsBeforeDedupe": complete_rows,
        "selectedRowsThisRun": completed_rows_this_run,
        "output": relative_path(args.output),
        "chunkDir": relative_path(args.chunk_dir),
        "filters": filters_manifest(args),
        "notes": [
            "This is the broad Oden parent query, not an RC-selected catalog.",
            "No proper-motion clipping is applied here; global iterative PM clipping and local PM selection are downstream science steps.",
            "The two Oden sky circles overlap; output concatenation deduplicates rows by Gaia source_id.",
            "The default astrometric_excess_noise cut follows the Oden appendix query value of 2.5.",
            "The default parallax_over_error < 4 represents the Oden parallax quality cut after requiring non-null parallax.",
        ],
    }

    can_concat = (not args.count_only) and (len(complete_records) == expected_chunks or args.allow_partial_concat)
    if can_concat and not args.no_concat:
        concat = concatenate_chunks(complete_records, args.output, gaia.table_columns(args.table), force=args.force)
        manifest["outputRows"] = concat["rows"]
        manifest["duplicateSourceIds"] = concat["duplicateSourceIds"]
        manifest["outputBytes"] = args.output.stat().st_size
        print(
            f"Combined {concat['rows']} deduplicated rows into {args.output} "
            f"({concat['duplicateSourceIds']} duplicate source_id rows skipped)",
            flush=True,
        )
    elif args.count_only:
        print(f"{len(complete_records)}/{expected_chunks} count chunks complete; no data concatenation needed.", flush=True)
    elif len(complete_records) != expected_chunks:
        print(f"{len(complete_records)}/{expected_chunks} chunks complete; skipping concatenation for now.", flush=True)

    manifest_path = output_manifest_path(args)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"Wrote manifest {manifest_path}")


if __name__ == "__main__":
    main()
