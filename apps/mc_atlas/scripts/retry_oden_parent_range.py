from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHUNK_DIR = ROOT / "data" / "raw" / "gaia" / "xmc_rc_gaia_oden_parent_chunks"


def chunk_path(region: str, chunk_count: int, index: int) -> Path:
    return CHUNK_DIR / f"source_{region.lower()}_rows_ri{chunk_count:05d}_{index:05d}.csv"


def manifest_path(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".json")


def is_complete(region: str, chunk_count: int, index: int) -> bool:
    path = chunk_path(region, chunk_count, index)
    manifest = manifest_path(path)
    if not path.exists() or not manifest.exists():
        return False
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        payload.get("status") == "completed"
        and payload.get("region") == region
        and int(payload.get("chunk", -1)) == index
        and int(payload.get("chunkCount", -1)) == chunk_count
        and not payload.get("countOnly")
    )


def missing_chunks(region: str, chunk_count: int, start: int, stop: int) -> list[int]:
    return [index for index in range(start, stop) if not is_complete(region, chunk_count, index)]


def run_chunk(args: argparse.Namespace, index: int) -> int:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "download_xmc_rc_gaia_oden_parent.py"),
        "--no-concat",
        "--chunk-count",
        str(args.chunk_count),
        "--start-chunk",
        str(index),
        "--stop-chunk",
        str(index + 1),
        "--regions",
        args.region,
        "--tap-mode",
        args.tap_mode,
        "--timeout",
        str(args.timeout),
        "--maxrec",
        str(args.maxrec),
        "--output",
        str(args.output),
    ]
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] trying {args.region} chunk {index:05d}", flush=True)
    completed = subprocess.run(command, cwd=ROOT)
    return completed.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retry a resumable Oden parent Gaia chunk range with backoff.")
    parser.add_argument("--region", choices=("PRIMARY", "SMC_SUPPLEMENT"), required=True)
    parser.add_argument("--start-chunk", type=int, required=True)
    parser.add_argument("--stop-chunk", type=int, required=True)
    parser.add_argument("--chunk-count", type=int, default=4000)
    parser.add_argument("--tap-mode", choices=("sync", "async"), default="sync")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--maxrec", type=int, default=250_000)
    parser.add_argument("--backoff-seconds", type=int, default=600)
    parser.add_argument("--pass-sleep-seconds", type=int, default=60)
    parser.add_argument("--failure-backoff-after", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.stop_chunk <= args.start_chunk:
        raise ValueError("--stop-chunk must be greater than --start-chunk")
    if args.failure_backoff_after <= 0:
        raise ValueError("--failure-backoff-after must be positive")

    consecutive_failures = 0
    while True:
        missing = missing_chunks(args.region, args.chunk_count, args.start_chunk, args.stop_chunk)
        if not missing:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] all chunks complete for {args.region}", flush=True)
            return

        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {len(missing)} chunks still missing for "
            f"{args.region}; next={missing[0]:05d}",
            flush=True,
        )
        made_progress = False
        for index in missing:
            result = run_chunk(args, index)
            if result == 0 and is_complete(args.region, args.chunk_count, index):
                consecutive_failures = 0
                made_progress = True
                continue

            consecutive_failures += 1
            print(
                f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {args.region} chunk {index:05d} failed "
                f"(consecutive failures={consecutive_failures})",
                flush=True,
            )
            if consecutive_failures >= args.failure_backoff_after:
                print(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] backing off for {args.backoff_seconds} seconds",
                    flush=True,
                )
                time.sleep(args.backoff_seconds)
                consecutive_failures = 0
                break

        if not made_progress:
            time.sleep(args.pass_sleep_seconds)


if __name__ == "__main__":
    main()
