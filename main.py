"""Run the news-image-20261119 front page entry.

The picture was painted ahead of time by gen_image.py and is shipped
here as entry.png, right next to this file. All this program does is
place that one picture where the grader looks for it, so it needs
nothing beyond the standard library, touches no network, and always
writes the exact same bytes.

Try it outside the grader with a stand-in folder:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path


def entry_dir():
    return Path(__file__).resolve().parent


def destination():
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def run():
    out = destination()
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(entry_dir() / "entry.png", out / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(run())
