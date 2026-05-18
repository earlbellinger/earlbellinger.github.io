from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

import download_xmc_rc_gaia_calibrated as gaia
import download_xmc_rc_gaia_oden_parent as parent


ROOT = parent.ROOT
DEFAULT_OUTPUT = parent.DEFAULT_OUTPUT
DEFAULT_CHUNK_DIR = parent.DEFAULT_CHUNK_DIR
REGIONS = ("PRIMARY", "SMC_SUPPLEMENT")


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def chunk_path(chunk_dir: Path, region: str, chunk_count: int, index: int) -> Path:
    return chunk_dir / f"source_{region.lower()}_rows_ri{chunk_count:05d}_{index:05d}.csv"


def manifest_path(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".json")


def completed_chunk(path: Path, region: str, chunk_count: int, index: int, expected_columns: tuple[str, ...]) -> int:
    manifest = manifest_path(path)
    if not path.exists() or not manifest.exists():
        raise FileNotFoundError(f"missing chunk or manifest for {region} {index:05d}: {path}")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    if payload.get("status") != "completed":
        raise ValueError(f"{path} manifest status is not completed: {payload.get('status')!r}")
    if payload.get("region") != region:
        raise ValueError(f"{path} manifest region mismatch: {payload.get('region')!r}")
    if int(payload.get("chunk", -1)) != index:
        raise ValueError(f"{path} manifest chunk mismatch: {payload.get('chunk')!r}")
    if int(payload.get("chunkCount", -1)) != chunk_count:
        raise ValueError(f"{path} manifest chunkCount mismatch: {payload.get('chunkCount')!r}")
    if payload.get("countOnly"):
        raise ValueError(f"{path} is a count-only chunk")
    gaia.validate_csv_header(path, expected_columns)
    return int(payload.get("rows", 0))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Concatenate and deduplicate completed Oden parent Gaia chunks.")
    parser.add_argument("--chunk-dir", type=Path, default=DEFAULT_CHUNK_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--chunk-count", type=int, default=4000)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--progress-every", type=int, default=100)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    expected_columns = gaia.table_columns("source")
    output_columns = ("region",) + expected_columns
    if args.output.exists() and not args.force:
        raise FileExistsError(f"{args.output} already exists; pass --force to replace it")

    records: list[tuple[str, int, Path, int]] = []
    for region in REGIONS:
        for index in range(args.chunk_count):
            path = chunk_path(args.chunk_dir, region, args.chunk_count, index)
            rows = completed_chunk(path, region, args.chunk_count, index, expected_columns)
            records.append((region, index, path, rows))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    part_path = args.output.with_suffix(args.output.suffix + ".part")
    source_id_index = expected_columns.index("source_id")
    seen_source_ids: set[str] = set()
    total_rows_before_dedupe = 0
    total_rows = 0
    duplicates = 0
    started = time.monotonic()
    last_report = started

    with part_path.open("w", encoding="utf-8", newline="") as out_handle:
        writer = csv.writer(out_handle, lineterminator="\n")
        writer.writerow(output_columns)
        for record_index, (region, index, path, manifest_rows) in enumerate(records, start=1):
            total_rows_before_dedupe += manifest_rows
            with path.open("r", encoding="utf-8", newline="") as in_handle:
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

            if record_index % args.progress_every == 0:
                now = time.monotonic()
                print(
                    f"{record_index}/{len(records)} chunks; "
                    f"{total_rows:,} unique rows; {duplicates:,} duplicates; "
                    f"{now - last_report:.1f}s since last report",
                    flush=True,
                )
                last_report = now

    part_path.replace(args.output)
    elapsed = time.monotonic() - started
    manifest = {
        "source": "Gaia DR3",
        "method": "oden-2025-broad-parent-gaia-concatenate-deduplicate",
        "sourceTable": gaia.TABLES["source"],
        "columns": list(output_columns),
        "regions": list(REGIONS),
        "chunkCount": args.chunk_count,
        "expectedChunks": len(records),
        "completeChunks": len(records),
        "completeRowsBeforeDedupe": total_rows_before_dedupe,
        "outputRows": total_rows,
        "duplicateSourceIds": duplicates,
        "outputBytes": args.output.stat().st_size,
        "elapsedSeconds": elapsed,
        "output": relative_path(args.output),
        "chunkDir": relative_path(args.chunk_dir),
        "updatedUnixSeconds": time.time(),
        "notes": [
            "Rows are concatenated in PRIMARY then SMC_SUPPLEMENT order.",
            "Duplicate Gaia source_id rows from overlapping sky circles are skipped.",
            "This is the broad Oden-style parent catalog before global/local PM and CMD RC selection.",
        ],
    }
    manifest_path = args.output.with_suffix(args.output.suffix + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2), flush=True)
    print(f"Wrote {args.output}", flush=True)
    print(f"Wrote {manifest_path}", flush=True)


if __name__ == "__main__":
    main()
