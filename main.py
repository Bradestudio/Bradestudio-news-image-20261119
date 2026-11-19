#!/usr/bin/env python3
"""Ship the round-2 front page for Thursday 19 November 2026.

The graded program is intentionally small: it copies the newspaper
image rendered at build time (entry.png, 1024 by 1024, sitting next
to this file) into $MAKEFUN_OUTPUT_DIR/entry.png. The picture is
round 2 of the 19 November front page — 44 stories across six
continents, led by the Jeffries Speaker nomination and the Shenzhen
trilateral, with the evening's ICJ Rohingya ruling and the Anthropic
IPO, a UTC timeline of the day, a BY THE NUMBERS strip and a world
map with numbered pins.

Standard library only. No network, no randomness, no clock reads,
so running it twice writes byte-identical output every time.

Example:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def ship_front_page():
    """Copy entry.png to the output directory, checking the copy."""
    destination_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    source = HERE / "entry.png"
    target = destination_dir / "entry.png"
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise SystemExit("entry.png copy is incomplete")
    print("wrote", target, target.stat().st_size, "bytes")


if __name__ == "__main__":
    ship_front_page()
