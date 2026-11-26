"""Entry program for make.fun news-image-20261126.

Copies the pre-rendered front page (entry.png, drawn by draw_news.py)
to the grader's output directory as entry.png. Standard library only,
no network, deterministic: both runs write identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    with open(SRC, "rb") as f:
        head = f.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")
    size = os.path.getsize(SRC)
    if size > 1048576:
        raise SystemExit("entry.png exceeds the 1 MiB limit")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst, size, "bytes")


if __name__ == "__main__":
    main()
