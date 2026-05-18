from __future__ import annotations

import gzip
import json
from pathlib import Path

from eclipsing_binary_distances import apply_eclipsing_binary_distance_anchors


ROOT = Path(__file__).resolve().parent.parent
ATLAS_JSON = ROOT / "public" / "data" / "magellanic-clouds.json"
ATLAS_BROTLI = ATLAS_JSON.with_suffix(".json.br")
ATLAS_GZIP = ATLAS_JSON.with_suffix(".json.gz")


def compress_brotli(data: bytes) -> bytes | None:
    for module_name in ("brotli", "brotlicffi"):
        try:
            brotli_module = __import__(module_name)
        except ImportError:
            continue
        return brotli_module.compress(data, quality=11)
    return None


def main() -> None:
    payload = json.loads(ATLAS_JSON.read_text(encoding="utf-8"))
    summary = apply_eclipsing_binary_distance_anchors(payload, root=ROOT)
    atlas_json_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    ATLAS_JSON.write_bytes(atlas_json_bytes)

    brotli_bytes = compress_brotli(atlas_json_bytes)
    if brotli_bytes is not None:
        ATLAS_BROTLI.write_bytes(brotli_bytes)
    elif ATLAS_BROTLI.exists():
        ATLAS_BROTLI.unlink()
    ATLAS_GZIP.write_bytes(gzip.compress(atlas_json_bytes, compresslevel=9, mtime=0))
    print(json.dumps(summary, indent=2))
    print(f"Wrote {ATLAS_JSON}")
    if brotli_bytes is not None:
        print(f"Wrote {ATLAS_BROTLI}")
    else:
        print("Skipped Brotli output; install brotli or brotlicffi to generate it.")
    print(f"Wrote {ATLAS_GZIP}")


if __name__ == "__main__":
    main()
