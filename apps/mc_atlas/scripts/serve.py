from __future__ import annotations

import argparse
import functools
import posixpath
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DATA_DIR = (ROOT / "public" / "data").resolve()


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
        if request_path.startswith("/public/data/") and request_path.endswith(".json"):
            identity_path = (ROOT / request_path.lstrip("/")).resolve()
            try:
                identity_path.relative_to(PUBLIC_DATA_DIR)
            except ValueError:
                return super().send_head()
            if not identity_path.exists():
                return super().send_head()

            accept_encoding = self.headers.get("Accept-Encoding", "")
            brotli_path = identity_path.with_suffix(identity_path.suffix + ".br")
            gzip_path = identity_path.with_suffix(identity_path.suffix + ".gz")
            if accepts_encoding(accept_encoding, "br") and brotli_path.exists():
                return self.send_json_variant(brotli_path, "br", identity_path)
            if accepts_encoding(accept_encoding, "gzip") and gzip_path.exists():
                return self.send_json_variant(gzip_path, "gzip", identity_path)
            return self.send_json_variant(identity_path, None, identity_path)

        return super().send_head()

    def send_json_variant(self, path: Path, content_encoding: str | None, identity_path: Path):
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
            self.send_header("X-Uncompressed-Content-Length", str(identity_path.stat().st_size))
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
    print("Public JSON negotiation: br -> gzip -> identity")
    server.serve_forever()


if __name__ == "__main__":
    main()
