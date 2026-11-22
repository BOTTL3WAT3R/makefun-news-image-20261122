#!/usr/bin/env python3
"""make.fun entrypoint for news-image-20261122 (stdlib only).

The poster (entry.png) is rendered at build time by render_poster.py and
committed to this repository. This entrypoint simply copies it, byte for
byte, to /output/entry.png. It needs no third-party packages, no network,
and writes identical bytes on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
