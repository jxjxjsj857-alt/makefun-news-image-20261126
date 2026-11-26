"""make.fun news-image-20261126 entrypoint.

Writes the front page for Thursday 26 November 2026 to the grader's
output directory. The page itself is pre-drawn (see draw_news.py) and
stored beside this file as entry.png; this program only validates it
and places an identical copy at the required location.

Standard library only, no network, deterministic: repeated runs emit
byte-identical output.
"""
import os
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
SOURCE_NAME = "entry.png"


def locate_source() -> Path:
    here = Path(__file__).resolve().parent
    return here / SOURCE_NAME


def destination() -> Path:
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out.mkdir(parents=True, exist_ok=True)
    return out / SOURCE_NAME


def run() -> None:
    src = locate_source()
    payload = src.read_bytes()
    if payload[:8] != PNG_MAGIC:
        raise SystemExit(f"{src} does not start with a PNG signature")
    if len(payload) > MAX_BYTES:
        raise SystemExit(f"{src} is {len(payload)} bytes, over the 1 MiB cap")
    dst = destination()
    dst.write_bytes(payload)
    print(f"entry written to {dst} ({len(payload)} bytes)")


if __name__ == "__main__":
    run()
