from __future__ import annotations

import argparse
import csv
import json
import math
import time
from pathlib import Path
from urllib.parse import urljoin

import requests


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RAW_GAIA = ROOT / "data" / "raw" / "gaia"

DEFAULT_OUTPUT = PROCESSED / "xmc_rc_gaia_full.csv"
DEFAULT_CHUNK_DIR = RAW_GAIA / "xmc_rc_gaia_full_chunks"
GAIA_TAP_ASYNC = "https://gea.esac.esa.int/tap-server/tap/async"
GAIA_DR3_SOURCE_COUNT = 1_811_709_771
COLUMNS = ("l", "b", "phot_g_mean_mag", "bp_rp", "pmra", "pmdec")
TABLES = {
    "source": "gaiadr3.gaia_source",
    "source-lite": "gaiadr3.gaia_source_lite",
}


def build_query(
    args: argparse.Namespace,
    lower_random_index: int | None = None,
    upper_random_index: int | None = None,
    lower_ra: float | None = None,
    upper_ra: float | None = None,
) -> str:
    random_index_filter = ""
    if lower_random_index is not None and upper_random_index is not None:
        random_index_filter = f"""
  AND random_index >= {lower_random_index:d}
  AND random_index < {upper_random_index:d}"""
    ra_filter = ""
    if lower_ra is not None and upper_ra is not None:
        ra_filter = f"""
  AND ra >= {lower_ra:.8f}
  AND ra < {upper_ra:.8f}"""
    astrometric_excess_noise_filter = ""
    if args.table == "source":
        astrometric_excess_noise_filter = (
            f"\n  AND astrometric_excess_noise < {args.astrometric_excess_noise_max:.6f}"
        )

    return f"""
SELECT
  l,
  b,
  phot_g_mean_mag,
  bp_rp,
  pmra,
  pmdec
FROM {TABLES[args.table]}
WHERE
  (
    CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 81.28, -69.78, 30.0)) = 1
    OR CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', 13.10, -72.82, 15.0)) = 1
  )
{random_index_filter}
{ra_filter}
  AND phot_g_mean_mag BETWEEN {args.query_g_min:.6f} AND {args.query_g_max:.6f}
  AND bp_rp BETWEEN {args.query_bp_rp_min:.6f} AND {args.query_bp_rp_max:.6f}
  AND ruwe < {args.ruwe_max:.6f}
{astrometric_excess_noise_filter}
  AND parallax IS NOT NULL
  AND parallax_over_error < {args.parallax_over_error_max:.6f}
  AND pmra IS NOT NULL
  AND pmdec IS NOT NULL
  AND (
    POWER(pmra - ({args.lmc_pmra:.6f}), 2) + POWER(pmdec - ({args.lmc_pmdec:.6f}), 2) < POWER({args.query_pm_radius:.6f}, 2)
    OR POWER(pmra - ({args.smc_pmra:.6f}), 2) + POWER(pmdec - ({args.smc_pmdec:.6f}), 2) < POWER({args.query_pm_radius:.6f}, 2)
  )
"""


def chunk_bounds(chunk_count: int) -> list[tuple[int, int]]:
    bounds = []
    for index in range(chunk_count):
        lower = math.floor(GAIA_DR3_SOURCE_COUNT * index / chunk_count)
        upper = math.floor(GAIA_DR3_SOURCE_COUNT * (index + 1) / chunk_count)
        bounds.append((lower, upper))
    bounds[-1] = (bounds[-1][0], GAIA_DR3_SOURCE_COUNT)
    return bounds


def ra_chunk_bounds(chunk_count: int) -> list[tuple[float, float]]:
    return [(360.0 * index / chunk_count, 360.0 * (index + 1) / chunk_count) for index in range(chunk_count)]


def count_csv_rows(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def validate_csv_header(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
    if tuple(header or ()) != COLUMNS:
        raise ValueError(f"{path} has unexpected CSV header: {header!r}")


def manifest_path_for_chunk(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".json")


def chunk_is_complete(path: Path) -> bool:
    manifest_path = manifest_path_for_chunk(path)
    if not path.exists() or not manifest_path.exists():
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_csv_header(path)
        return manifest.get("status") == "completed" and int(manifest.get("rows", -1)) == count_csv_rows(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return False


def write_chunk_manifest(path: Path, payload: dict[str, object]) -> None:
    manifest_path_for_chunk(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def tap_async_query_to_file(
    query: str,
    output: Path,
    timeout: int,
    poll_seconds: float,
    maxrec: int,
) -> dict[str, object]:
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

    job_url = urljoin(GAIA_TAP_ASYNC, response.headers.get("Location") or response.url)
    print(f"Gaia TAP job: {job_url}", flush=True)

    phase_response = session.post(f"{job_url}/phase", data={"PHASE": "RUN"}, timeout=60)
    try:
        phase_response.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(phase_response.text) from error

    started = time.monotonic()
    last_phase = ""
    while True:
        phase = session.get(f"{job_url}/phase", timeout=60).text.strip().upper()
        if phase == "COMPLETED":
            break
        if phase in {"ERROR", "ABORTED"}:
            error = session.get(f"{job_url}/error", timeout=60).text
            raise RuntimeError(f"Gaia TAP job ended with phase {phase}:\n{error}")
        if time.monotonic() - started > timeout:
            raise TimeoutError(f"Gaia TAP job did not complete within {timeout} seconds; job URL: {job_url}")
        if phase != last_phase:
            print(f"Gaia TAP phase: {phase}", flush=True)
            last_phase = phase
        time.sleep(poll_seconds)

    output.parent.mkdir(parents=True, exist_ok=True)
    part_path = output.with_suffix(output.suffix + ".part")
    with session.get(f"{job_url}/results/result", stream=True, timeout=300) as result:
        try:
            result.raise_for_status()
        except requests.HTTPError as error:
            raise RuntimeError(result.text) from error
        with part_path.open("wb") as handle:
            for chunk in result.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    part_path.replace(output)
    validate_csv_header(output)
    rows = count_csv_rows(output)
    if rows >= maxrec:
        raise RuntimeError(f"{output} has {rows} rows, which reached MAXREC={maxrec}; chunk may be truncated")
    return {
        "status": "completed",
        "jobUrl": job_url,
        "rows": rows,
        "bytes": output.stat().st_size,
        "seconds": round(time.monotonic() - started, 3),
    }


def concatenate_chunks(chunks: list[Path], output: Path, force: bool = False) -> int:
    if output.exists() and not force:
        print(f"Output already exists; leaving it in place: {output}", flush=True)
        return count_csv_rows(output)

    output.parent.mkdir(parents=True, exist_ok=True)
    part_path = output.with_suffix(output.suffix + ".part")
    total_rows = 0
    with part_path.open("w", encoding="utf-8", newline="") as out_handle:
        writer = csv.writer(out_handle, lineterminator="\n")
        writer.writerow(COLUMNS)
        for chunk in chunks:
            validate_csv_header(chunk)
            with chunk.open("r", encoding="utf-8", newline="") as in_handle:
                reader = csv.reader(in_handle)
                next(reader, None)
                for row in reader:
                    writer.writerow(row)
                    total_rows += 1
    part_path.replace(output)
    return total_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the full Gaia DR3 XMC red-clump analysis row set in resumable random_index chunks."
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--chunk-dir", type=Path, default=DEFAULT_CHUNK_DIR)
    parser.add_argument("--table", choices=tuple(TABLES), default="source")
    parser.add_argument("--chunk-count", type=int, default=20)
    parser.add_argument("--chunk-mode", choices=("random-index", "ra"), default="random-index")
    parser.add_argument("--start-chunk", type=int, default=0)
    parser.add_argument("--stop-chunk", type=int, default=None)
    parser.add_argument("--single-query", action="store_true", help="Download the full filtered footprint in one TAP job without a random_index range.")
    parser.add_argument("--timeout", type=int, default=14400)
    parser.add_argument("--poll-seconds", type=float, default=30.0)
    parser.add_argument("--maxrec", type=int, default=2_500_000)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-concat", action="store_true")
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.chunk_count <= 0:
        raise ValueError("--chunk-count must be positive")

    if args.single_query:
        query = build_query(args)
        if args.dry_run:
            print(query.strip())
            return
        if args.output.exists() and not args.force:
            print(f"Output already exists; leaving it in place: {args.output}", flush=True)
            rows = count_csv_rows(args.output)
            bytes_written = args.output.stat().st_size
        else:
            result = tap_async_query_to_file(query, args.output, args.timeout, args.poll_seconds, args.maxrec)
            rows = int(result["rows"])
            bytes_written = int(result["bytes"])
            print(f"Single-query export complete: {rows} rows, {bytes_written} bytes", flush=True)
        manifest = {
            "source": "Gaia DR3 gaiadr3.gaia_source",
            "method": "full-xmc-rc-gaia-row-download-single-footprint-query",
            "sourceTable": TABLES[args.table],
            "columns": list(COLUMNS),
            "rows": rows,
            "bytes": bytes_written,
            "output": str(args.output.relative_to(ROOT) if args.output.is_relative_to(ROOT) else args.output),
            "query": query.strip(),
            "filters": {
                "queryG": [args.query_g_min, args.query_g_max],
                "queryBpRp": [args.query_bp_rp_min, args.query_bp_rp_max],
                "queryPmRadiusMasYr": args.query_pm_radius,
                "parallaxOverErrorMax": args.parallax_over_error_max,
                "ruweMax": args.ruwe_max,
                "astrometricExcessNoiseMax": args.astrometric_excess_noise_max if args.table == "source" else None,
            },
        }
        manifest_path = args.output.with_suffix(args.output.suffix + ".manifest.json")
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(json.dumps(manifest, indent=2))
        print(f"Wrote manifest {manifest_path}")
        return

    bounds = chunk_bounds(args.chunk_count) if args.chunk_mode == "random-index" else ra_chunk_bounds(args.chunk_count)
    stop_chunk = args.stop_chunk if args.stop_chunk is not None else args.chunk_count
    selected = list(enumerate(bounds))[args.start_chunk : stop_chunk]
    if args.dry_run:
        for index, (lower, upper) in selected:
            label = "random_index" if args.chunk_mode == "random-index" else "ra"
            print(f"-- chunk {index:03d}: {label} [{lower}, {upper})")
            if args.chunk_mode == "random-index":
                print(build_query(args, lower_random_index=int(lower), upper_random_index=int(upper)).strip())
            else:
                print(build_query(args, lower_ra=float(lower), upper_ra=float(upper)).strip())
            print()
        return

    args.chunk_dir.mkdir(parents=True, exist_ok=True)
    chunk_prefix = "xmc_rc_gaia_full_ra" if args.chunk_mode == "ra" else "xmc_rc_gaia_full"
    all_chunk_paths = [args.chunk_dir / f"{chunk_prefix}_{index:03d}.csv" for index in range(args.chunk_count)]
    completed_rows = 0
    for index, (lower, upper) in selected:
        chunk_path = all_chunk_paths[index]
        if not args.force and chunk_is_complete(chunk_path):
            rows = count_csv_rows(chunk_path)
            completed_rows += rows
            print(f"Chunk {index:03d} already complete: {rows} rows", flush=True)
            continue

        label = "random_index" if args.chunk_mode == "random-index" else "ra"
        print(f"Downloading chunk {index:03d}/{args.chunk_count - 1:03d}: {label} [{lower}, {upper})", flush=True)
        if args.chunk_mode == "random-index":
            query = build_query(args, lower_random_index=int(lower), upper_random_index=int(upper))
        else:
            query = build_query(args, lower_ra=float(lower), upper_ra=float(upper))
        try:
            result = tap_async_query_to_file(query, chunk_path, args.timeout, args.poll_seconds, args.maxrec)
        except Exception:
            write_chunk_manifest(
                chunk_path,
                {
                    "status": "failed",
                    "chunk": index,
                    "chunkMode": args.chunk_mode,
                    "lowerBound": lower,
                    "upperBound": upper,
                    "query": query.strip(),
                    "updatedUnixSeconds": time.time(),
                },
            )
            raise

        result.update(
            {
                "chunk": index,
                "chunkMode": args.chunk_mode,
                "lowerBound": lower,
                "upperBound": upper,
                "query": query.strip(),
                "updatedUnixSeconds": time.time(),
            }
        )
        write_chunk_manifest(chunk_path, result)
        completed_rows += int(result["rows"])
        print(f"Chunk {index:03d} complete: {result['rows']} rows, {result['bytes']} bytes", flush=True)

    complete_chunks = [path for path in all_chunk_paths if chunk_is_complete(path)]
    manifest = {
        "source": "Gaia DR3 gaiadr3.gaia_source",
        "method": "full-xmc-rc-gaia-row-download-random-index-chunks",
        "sourceTable": TABLES[args.table],
        "columns": list(COLUMNS),
        "chunkMode": args.chunk_mode,
        "chunkCount": args.chunk_count,
        "completeChunks": len(complete_chunks),
        "selectedRowsThisRun": completed_rows,
        "output": str(args.output.relative_to(ROOT) if args.output.is_relative_to(ROOT) else args.output),
        "chunkDir": str(args.chunk_dir.relative_to(ROOT) if args.chunk_dir.is_relative_to(ROOT) else args.chunk_dir),
        "filters": {
            "queryG": [args.query_g_min, args.query_g_max],
            "queryBpRp": [args.query_bp_rp_min, args.query_bp_rp_max],
            "queryPmRadiusMasYr": args.query_pm_radius,
            "parallaxOverErrorMax": args.parallax_over_error_max,
            "ruweMax": args.ruwe_max,
            "astrometricExcessNoiseMax": args.astrometric_excess_noise_max if args.table == "source" else None,
        },
    }

    if len(complete_chunks) == args.chunk_count and not args.no_concat:
        rows = concatenate_chunks(all_chunk_paths, args.output, force=args.force)
        manifest["outputRows"] = rows
        manifest["outputBytes"] = args.output.stat().st_size
        print(f"Combined {rows} rows into {args.output}", flush=True)
    elif len(complete_chunks) != args.chunk_count:
        print(f"{len(complete_chunks)}/{args.chunk_count} chunks complete; skipping concatenation for now.", flush=True)

    manifest_path = args.output.with_suffix(args.output.suffix + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    print(f"Wrote manifest {manifest_path}")


if __name__ == "__main__":
    main()
