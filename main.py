#!/usr/bin/env python3
"""Deliver the 19 November front page as the graded output.

The graded program is deliberately tiny: it copies the newspaper
image drawn at build time (entry.png, 1024 by 1024, next to this
file) to $MAKEFUN_OUTPUT_DIR/entry.png. The picture sums up
Thursday 19 November 2026 — the Jeffries nomination leads, followed
by the Shenzhen trilateral, the GTA VI launch, Voyager 1's
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
from pathlib import Path

HERE = Path(__file__).resolve().parent


def deliver():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    source = HERE / "entry.png"
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    # A short copy is a broken entry: refuse it loudly.
    if target.stat().st_size != source.stat().st_size:
        raise SystemExit("copy came out short")
    print("wrote", target, target.stat().st_size, "bytes")


if __name__ == "__main__":
    deliver()
