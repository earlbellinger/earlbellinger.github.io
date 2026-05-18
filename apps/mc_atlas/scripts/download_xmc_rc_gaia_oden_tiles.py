from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))
sys.path.insert(0, str(ROOT / "scripts"))

import download_xmc_rc_gaia_calibrated as gaia_download  # noqa: E402
import validate_oden_recovery as recovery  # noqa: E402


PROCESSED = ROOT / "data" / "processed"
RAW_GAIA = ROOT / "data" / "raw" / "gaia"

DEFAULT_OUTPUT = PROCESSED / "xmc_rc_gaia_oden_tiles_full.csv"
DEFAULT_TILE_DIR = RAW_GAIA / "xmc_rc_gaia_oden_tile_chunks"
DEFAULT_PLAN = PROCESSED / "xmc_rc_gaia_oden_tile_plan.json"


@dataclass(frozen=True)
class OdenTile:
    tile_id: int
    ix: int
    iy: int
    l_min: float
    l_max: float
    b_min: float
    b_max: float
    oden_cell_count: int


@dataclass(frozen=True)
class WorkUnit:
    tile: OdenTile
    ri_index: int | None
    ri_count: int | None
    lower_random_index: int | None
    upper_random_index: int | None


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_oden_tiles(tile_size_deg: float, margin_deg: float, sort_by: str) -> list[OdenTile]:
    oden_by_key = recovery.load_oden_distance_map(recovery.ODEN_DISTANCE_FITS)
    cells_by_tile: dict[tuple[int, int], int] = {}
    lon_values = []
    lat_values = []
    for lon, lat, _ in oden_by_key.values():
        lon_values.append(lon)
        lat_values.append(lat)
        ix = math.floor(lon / tile_size_deg)
        iy = math.floor(lat / tile_size_deg)
        cells_by_tile[(ix, iy)] = cells_by_tile.get((ix, iy), 0) + 1

    if not cells_by_tile:
        raise ValueError("No valid Oden cells found")

    global_l_min = min(lon_values) - margin_deg
    global_l_max = max(lon_values) + margin_deg
    global_b_min = min(lat_values) - margin_deg
    global_b_max = max(lat_values) + margin_deg

    tiles = []
    for next_id, ((ix, iy), cell_count) in enumerate(sorted(cells_by_tile.items())):
        l_min = max(global_l_min, ix * tile_size_deg - margin_deg)
        l_max = min(global_l_max, (ix + 1) * tile_size_deg + margin_deg)
        b_min = max(global_b_min, iy * tile_size_deg - margin_deg)
        b_max = min(global_b_max, (iy + 1) * tile_size_deg + margin_deg)
        tiles.append(OdenTile(next_id, ix, iy, l_min, l_max, b_min, b_max, cell_count))

    if sort_by == "dense":
        tiles.sort(key=lambda tile: (-tile.oden_cell_count, tile.l_min, tile.b_min))
    elif sort_by == "sky":
        tiles.sort(key=lambda tile: (tile.l_min, tile.b_min))
    else:
        raise ValueError(f"Unsupported sort order {sort_by!r}")
    return [
        OdenTile(index, tile.ix, tile.iy, tile.l_min, tile.l_max, tile.b_min, tile.b_max, tile.oden_cell_count)
        for index, tile in enumerate(tiles)
    ]


def row_passes_sample_filters(args: argparse.Namespace, row: dict[str, str]) -> bool:
    g = float(row["phot_g_mean_mag"])
    color = float(row["bp_rp"])
    if g < args.query_g_min or g > args.query_g_max:
        return False
    if color < args.query_bp_rp_min or color > args.query_bp_rp_max:
        return False
    pmra = float(row["pmra"])
    pmdec = float(row["pmdec"])
    lmc = math.hypot(pmra - args.lmc_pmra, pmdec - args.lmc_pmdec) <= args.lmc_pm_radius
    smc = math.hypot(pmra - args.smc_pmra, pmdec - args.smc_pmdec) <= args.smc_pm_radius
    bridge = math.hypot(pmra - args.bridge_mid_pmra, pmdec - args.bridge_mid_pmdec) <= args.bridge_mid_pm_radius
    return lmc or smc or bridge


def estimate_tile_rows_from_sample(args: argparse.Namespace, tiles: list[OdenTile]) -> dict[int, int]:
    if args.skip_sample_estimate:
        return {}
    if not args.sample.exists():
        print(f"Sample estimate skipped; missing sample file: {args.sample}", flush=True)
        return {}

    counts = {tile.tile_id: 0 for tile in tiles}
    tiles_by_index = {(tile.ix, tile.iy): tile for tile in tiles}
    with args.sample.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if not row_passes_sample_filters(args, row):
                continue
            lon = float(row["l"])
            lat = float(row["b"])
            ix_min = math.floor((lon - args.tile_margin_deg) / args.tile_size_deg)
            ix_max = math.floor((lon + args.tile_margin_deg) / args.tile_size_deg)
            iy_min = math.floor((lat - args.tile_margin_deg) / args.tile_size_deg)
            iy_max = math.floor((lat + args.tile_margin_deg) / args.tile_size_deg)
            for ix in range(ix_min, ix_max + 1):
                for iy in range(iy_min, iy_max + 1):
                    tile = tiles_by_index.get((ix, iy))
                    if tile is None:
                        continue
                    if tile.l_min <= lon < tile.l_max and tile.b_min <= lat < tile.b_max:
                        counts[tile.tile_id] += 1

    scale = 1.0 / args.sample_fraction
    return {tile_id: int(round(count * scale)) for tile_id, count in counts.items()}


def adaptive_ri_count(args: argparse.Namespace, tile: OdenTile, estimated_rows_by_tile: dict[int, int]) -> int:
    if args.ri_chunk_count > 0:
        return args.ri_chunk_count
    if not args.adaptive_from_sample:
        return 0
    estimated_rows = estimated_rows_by_tile.get(tile.tile_id)
    if not estimated_rows:
        return 0
    return max(0, math.ceil(estimated_rows / args.max_estimated_rows_per_unit))


def selected_work_units(
    args: argparse.Namespace,
    tiles: list[OdenTile],
    estimated_rows_by_tile: dict[int, int],
) -> list[WorkUnit]:
    stop_tile = args.stop_tile if args.stop_tile is not None else len(tiles)
    if args.start_tile < 0 or stop_tile < args.start_tile or stop_tile > len(tiles):
        raise ValueError("--stop-tile must be between --start-tile and the tile count")
    selected_tiles = tiles[args.start_tile:stop_tile]
    if args.max_tiles is not None:
        selected_tiles = selected_tiles[: args.max_tiles]

    units = []
    for tile in selected_tiles:
        ri_count = adaptive_ri_count(args, tile, estimated_rows_by_tile)
        if ri_count <= 0:
            units.append(WorkUnit(tile, None, None, None, None))
            continue
        ri_bounds = gaia_download.chunk_bounds(ri_count)
        start_ri = args.start_ri if args.start_ri is not None else 0
        stop_ri = args.stop_ri if args.stop_ri is not None else ri_count
        if start_ri < 0 or stop_ri < start_ri or stop_ri > ri_count:
            raise ValueError("--start-ri/--stop-ri must be within the tile's random-index split count")
        for ri_index, (lower, upper) in list(enumerate(ri_bounds))[start_ri:stop_ri]:
            units.append(WorkUnit(tile, ri_index, ri_count, lower, upper))
    return units


def work_unit_tag(unit: WorkUnit) -> str:
    if unit.ri_index is None:
        return f"tile{unit.tile.tile_id:04d}"
    return f"tile{unit.tile.tile_id:04d}_ri{unit.ri_index:05d}"


def chunk_path_for(args: argparse.Namespace, unit: WorkUnit) -> Path:
    table_tag = args.table.replace("-", "_")
    return args.chunk_dir / f"{table_tag}_{work_unit_tag(unit)}.csv"


def count_path_for(args: argparse.Namespace, unit: WorkUnit) -> Path:
    table_tag = args.table.replace("-", "_")
    return args.chunk_dir / f"{table_tag}_{work_unit_tag(unit)}.count.csv"


def random_index_condition(unit: WorkUnit) -> str:
    if unit.ri_index is None:
        return ""
    return f"""
  AND random_index >= {unit.lower_random_index:d}
  AND random_index < {unit.upper_random_index:d}"""


def inclusive_pm_condition(args: argparse.Namespace) -> str:
    return f"""(
    POWER(pmra - ({args.lmc_pmra:.6f}), 2) + POWER(pmdec - ({args.lmc_pmdec:.6f}), 2) <= POWER({args.lmc_pm_radius:.6f}, 2)
    OR POWER(pmra - ({args.smc_pmra:.6f}), 2) + POWER(pmdec - ({args.smc_pmdec:.6f}), 2) <= POWER({args.smc_pm_radius:.6f}, 2)
    OR POWER(pmra - ({args.bridge_mid_pmra:.6f}), 2) + POWER(pmdec - ({args.bridge_mid_pmdec:.6f}), 2) <= POWER({args.bridge_mid_pm_radius:.6f}, 2)
  )"""


def build_query(args: argparse.Namespace, unit: WorkUnit, *, count_only: bool = False) -> str:
    astrometric_excess_noise_filter = ""
    if args.table == "source":
        astrometric_excess_noise_filter = (
            f"\n  AND astrometric_excess_noise < {args.astrometric_excess_noise_max:.6f}"
        )
    select_clause = "COUNT(*) AS row_count" if count_only else ",\n  ".join(gaia_download.table_columns(args.table))
    tile = unit.tile
    return f"""
SELECT
  {select_clause}
FROM {gaia_download.TABLES[args.table]}
WHERE
  l >= {tile.l_min:.8f}
  AND l < {tile.l_max:.8f}
  AND b >= {tile.b_min:.8f}
  AND b < {tile.b_max:.8f}{random_index_condition(unit)}
  AND phot_g_mean_mag BETWEEN {args.query_g_min:.6f} AND {args.query_g_max:.6f}
  AND bp_rp BETWEEN {args.query_bp_rp_min:.6f} AND {args.query_bp_rp_max:.6f}
  AND ruwe < {args.ruwe_max:.6f}
{astrometric_excess_noise_filter}
  AND parallax IS NOT NULL
  AND parallax_over_error < {args.parallax_over_error_max:.6f}
  AND pmra IS NOT NULL
  AND pmdec IS NOT NULL
  AND {inclusive_pm_condition(args)}
"""


def read_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        row = next(reader, None)
    if row is None or "row_count" not in row:
        raise ValueError(f"{path} does not contain a row_count result")
    return int(row["row_count"])


def manifest_path_for(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".json")


def write_manifest(path: Path, payload: dict[str, object]) -> None:
    manifest_path_for(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def unit_manifest(args: argparse.Namespace, unit: WorkUnit, query: str, rows: int, result: dict[str, object]) -> dict[str, object]:
    tile = unit.tile
    return {
        **result,
        "tileId": tile.tile_id,
        "tileIndex": [tile.ix, tile.iy],
        "tileBounds": {
            "galacticLonDeg": [tile.l_min, tile.l_max],
            "galacticLatDeg": [tile.b_min, tile.b_max],
        },
        "odenCellCount": tile.oden_cell_count,
        "riIndex": unit.ri_index,
        "riCount": unit.ri_count,
        "lowerRandomIndex": unit.lower_random_index,
        "upperRandomIndex": unit.upper_random_index,
        "rowCount": rows,
        "sourceTable": gaia_download.TABLES[args.table],
        "tapMode": args.tap_mode,
        "query": query.strip(),
        "updatedUnixSeconds": time.time(),
    }


def unit_is_complete(
    path: Path,
    args: argparse.Namespace,
    unit: WorkUnit,
    expected_columns: tuple[str, ...],
    *,
    count_only: bool = False,
) -> bool:
    manifest_path = manifest_path_for(path)
    if not path.exists() or not manifest_path.exists():
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_query = build_query(args, unit, count_only=count_only).strip()
        if manifest.get("status") != "completed":
            return False
        if int(manifest.get("tileId", -1)) != unit.tile.tile_id:
            return False
        if manifest.get("sourceTable") != gaia_download.TABLES[args.table]:
            return False
        if manifest.get("query") != expected_query:
            return False
        if count_only:
            gaia_download.validate_csv_header(path, ("row_count",))
            return int(manifest.get("rowCount", -1)) == read_row_count(path)

        gaia_download.validate_csv_header(path, expected_columns)
        return int(manifest.get("rows", -1)) == gaia_download.count_csv_rows(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return False


def write_tile_plan(
    path: Path,
    tiles: list[OdenTile],
    args: argparse.Namespace,
    estimated_rows_by_tile: dict[int, int],
) -> None:
    payload = {
        "method": "oden-valid-cell-galactic-tile-plan",
        "tileSizeDeg": args.tile_size_deg,
        "tileMarginDeg": args.tile_margin_deg,
        "tileCount": len(tiles),
        "tiles": [
            {
                "tileId": tile.tile_id,
                "tileIndex": [tile.ix, tile.iy],
                "galacticLonDeg": [tile.l_min, tile.l_max],
                "galacticLatDeg": [tile.b_min, tile.b_max],
                "odenCellCount": tile.oden_cell_count,
                "estimatedRowsFromSample": estimated_rows_by_tile.get(tile.tile_id),
            }
            for tile in tiles
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def concatenate_units(
    complete_units: list[tuple[WorkUnit, Path]],
    output: Path,
    expected_columns: tuple[str, ...],
    force: bool = False,
) -> dict[str, int]:
    if output.exists() and not force:
        print(f"Output already exists; leaving it in place: {output}", flush=True)
        return {
            "rows": gaia_download.count_csv_rows(output),
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
        writer.writerow(("tileId",) + expected_columns)
        for unit, chunk in complete_units:
            gaia_download.validate_csv_header(chunk, expected_columns)
            with chunk.open("r", encoding="utf-8", newline="") as in_handle:
                reader = csv.reader(in_handle)
                next(reader, None)
                for row in reader:
                    source_id = row[source_id_index]
                    if source_id in seen_source_ids:
                        duplicates += 1
                        continue
                    seen_source_ids.add(source_id)
                    writer.writerow((unit.tile.tile_id,) + tuple(row))
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
        "parallaxOverErrorMax": args.parallax_over_error_max,
        "ruweMax": args.ruwe_max,
        "astrometricExcessNoiseMax": args.astrometric_excess_noise_max if args.table == "source" else None,
        "inclusivePm": {
            "lmc": {"pmra": args.lmc_pmra, "pmdec": args.lmc_pmdec, "radiusMasYr": args.lmc_pm_radius},
            "smc": {"pmra": args.smc_pmra, "pmdec": args.smc_pmdec, "radiusMasYr": args.smc_pm_radius},
            "bridgeMid": {
                "pmra": args.bridge_mid_pmra,
                "pmdec": args.bridge_mid_pmdec,
                "radiusMasYr": args.bridge_mid_pm_radius,
            },
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Gaia DR3 XMC RC candidates using Oden-valid-cell Galactic tiles."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--chunk-dir", type=Path, default=DEFAULT_TILE_DIR)
    parser.add_argument("--plan-output", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--table", choices=tuple(gaia_download.TABLES), default="source")
    parser.add_argument("--tile-size-deg", type=float, default=2.0)
    parser.add_argument("--tile-margin-deg", type=float, default=0.25)
    parser.add_argument("--sort-by", choices=("sky", "dense"), default="sky")
    parser.add_argument("--sample", type=Path, default=PROCESSED / "xmc_rc_gaia_sample_5pct.csv")
    parser.add_argument("--sample-fraction", type=float, default=0.05)
    parser.add_argument("--skip-sample-estimate", action="store_true")
    parser.add_argument("--start-tile", type=int, default=0)
    parser.add_argument("--stop-tile", type=int, default=None)
    parser.add_argument("--max-tiles", type=int, default=None)
    parser.add_argument("--ri-chunk-count", type=int, default=0)
    parser.add_argument("--start-ri", type=int, default=None)
    parser.add_argument("--stop-ri", type=int, default=None)
    parser.add_argument("--adaptive-from-sample", action="store_true")
    parser.add_argument("--max-estimated-rows-per-unit", type=int, default=75_000)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--count-only", action="store_true")
    parser.add_argument("--allow-partial-concat", action="store_true")
    parser.add_argument("--no-concat", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--poll-seconds", type=float, default=20.0)
    parser.add_argument("--tap-mode", choices=("async", "sync"), default="async")
    parser.add_argument("--maxrec", type=int, default=100_000)
    parser.add_argument("--query-g-min", type=float, default=18.0)
    parser.add_argument("--query-g-max", type=float, default=20.35)
    parser.add_argument("--query-bp-rp-min", type=float, default=0.65)
    parser.add_argument("--query-bp-rp-max", type=float, default=1.85)
    parser.add_argument("--ruwe-max", type=float, default=1.4)
    parser.add_argument("--astrometric-excess-noise-max", type=float, default=2.0)
    parser.add_argument("--parallax-over-error-max", type=float, default=4.0)
    parser.add_argument("--lmc-pmra", type=float, default=1.776499)
    parser.add_argument("--lmc-pmdec", type=float, default=0.391679)
    parser.add_argument("--lmc-pm-radius", type=float, default=2.5)
    parser.add_argument("--smc-pmra", type=float, default=0.715272)
    parser.add_argument("--smc-pmdec", type=float, default=-1.229752)
    parser.add_argument("--smc-pm-radius", type=float, default=2.5)
    parser.add_argument("--bridge-mid-pmra", type=float, default=1.245886)
    parser.add_argument("--bridge-mid-pmdec", type=float, default=-0.419037)
    parser.add_argument("--bridge-mid-pm-radius", type=float, default=2.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.tile_size_deg <= 0:
        raise ValueError("--tile-size-deg must be positive")
    if args.tile_margin_deg < 0:
        raise ValueError("--tile-margin-deg must be non-negative")
    if args.ri_chunk_count < 0:
        raise ValueError("--ri-chunk-count must be non-negative")
    if args.sample_fraction <= 0:
        raise ValueError("--sample-fraction must be positive")
    if args.max_estimated_rows_per_unit <= 0:
        raise ValueError("--max-estimated-rows-per-unit must be positive")

    tiles = load_oden_tiles(args.tile_size_deg, args.tile_margin_deg, args.sort_by)
    estimated_rows_by_tile = estimate_tile_rows_from_sample(args, tiles)
    write_tile_plan(args.plan_output, tiles, args, estimated_rows_by_tile)
    print(f"Planned {len(tiles)} Oden-footprint tiles; wrote {args.plan_output}", flush=True)
    if args.plan_only:
        return

    units = selected_work_units(args, tiles, estimated_rows_by_tile)
    expected_columns = gaia_download.table_columns(args.table)
    if args.dry_run:
        for unit in units:
            print(f"-- {work_unit_tag(unit)}")
            print(build_query(args, unit, count_only=args.count_only).strip())
            print()
        return

    args.chunk_dir.mkdir(parents=True, exist_ok=True)
    completed_rows_this_run = 0
    if args.count_only:
        for unit in units:
            count_path = count_path_for(args, unit)
            if not args.force and unit_is_complete(count_path, args, unit, ("row_count",), count_only=True):
                row_count = read_row_count(count_path)
                completed_rows_this_run += row_count
                print(f"{work_unit_tag(unit)} count already complete: {row_count} rows", flush=True)
                continue

            query = build_query(args, unit, count_only=True)
            print(f"Counting {work_unit_tag(unit)}", flush=True)
            if args.tap_mode == "sync":
                result = gaia_download.tap_sync_query_to_file(
                    query,
                    count_path,
                    args.timeout,
                    maxrec=10,
                    expected_columns=("row_count",),
                )
            else:
                result = gaia_download.tap_async_query_to_file(
                    query,
                    count_path,
                    args.timeout,
                    args.poll_seconds,
                    maxrec=10,
                    expected_columns=("row_count",),
                )
            row_count = read_row_count(count_path)
            write_manifest(count_path, unit_manifest(args, unit, query, row_count, result))
            completed_rows_this_run += row_count
            print(f"{work_unit_tag(unit)} count complete: {row_count} rows", flush=True)
    else:
        for unit in units:
            chunk_path = chunk_path_for(args, unit)
            if not args.force and unit_is_complete(chunk_path, args, unit, expected_columns):
                rows = gaia_download.count_csv_rows(chunk_path)
                completed_rows_this_run += rows
                print(f"{work_unit_tag(unit)} already complete: {rows} rows", flush=True)
                continue

            query = build_query(args, unit)
            print(f"Downloading {work_unit_tag(unit)}", flush=True)
            if args.tap_mode == "sync":
                result = gaia_download.tap_sync_query_to_file(
                    query,
                    chunk_path,
                    args.timeout,
                    args.maxrec,
                    expected_columns,
                )
            else:
                result = gaia_download.tap_async_query_to_file(
                    query,
                    chunk_path,
                    args.timeout,
                    args.poll_seconds,
                    args.maxrec,
                    expected_columns,
                )
            rows = int(result["rows"])
            write_manifest(chunk_path, unit_manifest(args, unit, query, rows, result))
            completed_rows_this_run += rows
            print(f"{work_unit_tag(unit)} complete: {rows} rows, {result['bytes']} bytes", flush=True)

    all_units = selected_work_units(
        argparse.Namespace(
            **{
                **vars(args),
                "start_tile": 0,
                "stop_tile": len(tiles),
                "max_tiles": None,
                "start_ri": None,
                "stop_ri": None,
                "tap_mode": args.tap_mode,
            }
        ),
        tiles,
        estimated_rows_by_tile,
    )
    complete_units = [
        (unit, chunk_path_for(args, unit))
        for unit in all_units
        if unit_is_complete(chunk_path_for(args, unit), args, unit, expected_columns)
    ]
    expected_units = len(all_units)
    manifest: dict[str, object] = {
        "source": "Gaia DR3",
        "method": "oden-footprint-galactic-tile-gaia-download",
        "sourceTable": gaia_download.TABLES[args.table],
        "columns": ["tileId", *expected_columns],
        "tilePlan": relative_path(args.plan_output),
        "tileSizeDeg": args.tile_size_deg,
        "tileMarginDeg": args.tile_margin_deg,
        "tileCount": len(tiles),
        "riChunkCount": args.ri_chunk_count,
        "adaptiveFromSample": args.adaptive_from_sample,
        "maxEstimatedRowsPerUnit": args.max_estimated_rows_per_unit if args.adaptive_from_sample else None,
        "expectedUnits": expected_units,
        "completeUnits": len(complete_units),
        "selectedRowsThisRun": completed_rows_this_run,
        "output": relative_path(args.output),
        "chunkDir": relative_path(args.chunk_dir),
        "filters": filters_manifest(args),
        "notes": [
            "The footprint is defined by valid Oden 2025 Galactic-coordinate cells, expanded by tile margin.",
            "The PM filter is intentionally inclusive to preserve possible bridge stars.",
            "Use --adaptive-from-sample to split dense tiles using the local 5 percent sample estimate.",
            "Use --count-only on representative tiles to validate the sample estimate before a full run.",
        ],
    }

    can_concat = len(complete_units) == expected_units or args.allow_partial_concat
    if can_concat and not args.count_only and not args.no_concat:
        concat = concatenate_units(complete_units, args.output, expected_columns, force=args.force)
        manifest["outputRows"] = concat["rows"]
        manifest["duplicateSourceIds"] = concat["duplicateSourceIds"]
        manifest["outputBytes"] = args.output.stat().st_size
        print(
            f"Combined {concat['rows']} deduplicated rows into {args.output} "
            f"({concat['duplicateSourceIds']} duplicate source_id rows skipped)",
            flush=True,
        )
    elif len(complete_units) != expected_units and not args.count_only:
        print(f"{len(complete_units)}/{expected_units} units complete; skipping concatenation for now.", flush=True)

    manifest_path = args.output.with_suffix(args.output.suffix + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"Wrote manifest {manifest_path}")


if __name__ == "__main__":
    main()
