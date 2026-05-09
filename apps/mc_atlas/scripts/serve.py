from __future__ import annotations

import argparse
import functools
import posixpath
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ATLAS_URL_PATH = "/public/data/magellanic-clouds.json"
ATLAS_JSON = ROOT / "public" / "data" / "magellanic-clouds.json"
ATLAS_BR = ROOT / "public" / "data" / "magellanic-clouds.json.br"
ATLAS_GZIP = ROOT / "public" / "data" / "magellanic-clouds.json.gz"


def accepts_encoding(header: str, coding: str) -> bool:
    for item in header.split(","):
        token, *params = item.strip().split(";")
        token = token.strip().lower()
        if token not in {coding, "*"}:
            continue

        q = 1.0
        for param in params:
            key, _, value = param.strip().partition("=")
            if key.lower() == "q":
                try:
                    q = float(value)
                except ValueError:
                    q = 0.0
        return q > 0
    return False


class CompressedAtlasHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        request_path = posixpath.normpath(unquote(urlsplit(self.path).path))
        if request_path == ATLAS_URL_PATH:
            accept_encoding = self.headers.get("Accept-Encoding", "")
            if accepts_encoding(accept_encoding, "br") and ATLAS_BR.exists():
                return self.send_atlas_variant(ATLAS_BR, "br")
            if accepts_encoding(accept_encoding, "gzip") and ATLAS_GZIP.exists():
                return self.send_atlas_variant(ATLAS_GZIP, "gzip")
            return self.send_atlas_variant(ATLAS_JSON, None)

        return super().send_head()

    def send_atlas_variant(self, path: Path, content_encoding: str | None):
        try:
            stat = path.stat()
        except OSError:
            self.send_error(404, "File not found")
            return None

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(stat.st_size))
        self.send_header("Last-Modified", self.date_time_string(stat.st_mtime))
        self.send_header("Vary", "Accept-Encoding")
        if content_encoding:
            self.send_header("Content-Encoding", content_encoding)
            if ATLAS_JSON.exists():
                self.send_header("X-Uncompressed-Content-Length", str(ATLAS_JSON.stat().st_size))
        self.end_headers()

        if self.command == "HEAD":
            return None
        return path.open("rb")


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the atlas with Brotli/gzip data negotiation.")
    parser.add_argument("port", nargs="?", type=int, default=5173)
    args = parser.parse_args()

    handler = functools.partial(CompressedAtlasHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("", args.port), handler)
    print(f"Serving {ROOT} at http://localhost:{args.port}/")
    print("Atlas data negotiation: br -> gzip -> identity")
    server.serve_forever()


if __name__ == "__main__":
    main()
