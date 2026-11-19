#!/usr/bin/env python3
"""Ship the 19 November front page to the output directory.

This is the whole graded program: it takes the newspaper image that
gen_image.py drew at build time (entry.png, 1024 by 1024) and places
an identical copy at $MAKEFUN_OUTPUT_DIR/entry.png. The picture sums
up Thursday 19 November 2026 — the Jeffries nomination leads,
followed by the Shenzhen trilateral, the GTA VI launch, Voyager 1's
light-day, Cyclone Akvan, 29 further stories, a numbers strip and a
world map.

Only the Python standard library is used. Nothing is fetched from
the network and nothing is random, so every run writes the same
bytes as the last one.

Example:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    original = os.path.join(ROOT, "entry.png")
    duplicate = os.path.join(target_dir, "entry.png")
    shutil.copyfile(original, duplicate)
    # Refuse a truncated write: the copy must match the shipped
    # image byte for byte in size, or the entry is not valid.
    if os.path.getsize(duplicate) != os.path.getsize(original):
        raise SystemExit("copy came out short")
    print("wrote", duplicate, os.path.getsize(duplicate), "bytes")


if __name__ == "__main__":
    main()
