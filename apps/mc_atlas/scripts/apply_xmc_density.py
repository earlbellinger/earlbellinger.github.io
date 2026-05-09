from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import prepare_data as prep  # noqa: E402


DEFAULT_DATASET = ROOT / "public" / "data" / "magellanic-clouds.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fold XMC RC density counts into the generated atlas JSON.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--density", type=Path, default=prep.XMC_DENSITY_COUNTS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = json.loads(args.dataset.read_text(encoding="utf-8"))
    rows = payload["datasets"]["redClump"]
    for row in rows:
        del row[6:]

    density_counts, density_meta = prep.load_red_clump_density_counts(args.density)
    summary = prep.attach_red_clump_density(rows, density_counts)

    payload["fields"]["redClump"] = [
        "x",
        "y",
        "z",
        "distanceKpc",
        "galLonDeg",
        "galLatDeg",
        "densityCount",
        "densityUnit",
    ]
    payload["meta"][
        "redClumpDensityNote"
    ] = "Optional XMC surface opacity uses a smoothed Gaia DR3 broad red-clump count proxy binned on the same 0.25 degree galactic grid; it is for visual density only, not a reproduced Oden et al. RC catalog."
    payload["meta"]["redClumpDensitySource"] = density_meta
    payload["counts"].update(summary)

    dataset_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    args.dataset.write_bytes(dataset_bytes)
    brotli_bytes = prep.compress_brotli(dataset_bytes)
    brotli_path = args.dataset.with_suffix(args.dataset.suffix + ".br")
    gzip_path = args.dataset.with_suffix(args.dataset.suffix + ".gz")
    if brotli_bytes is not None:
        brotli_path.write_bytes(brotli_bytes)
    elif brotli_path.exists():
        brotli_path.unlink()
    gzip_path.write_bytes(gzip.compress(dataset_bytes, compresslevel=9, mtime=0))
    print(json.dumps(summary, indent=2))
    print(f"Wrote {args.dataset}")
    if brotli_bytes is not None:
        print(f"Wrote {brotli_path}")
    print(f"Wrote {gzip_path}")


if __name__ == "__main__":
    main()
