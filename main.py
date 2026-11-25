#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Stdlib-only entrypoint. It copies the pre-rendered comic PNG that ships
next to this file (entry.png) to $ENTRY_OUT/entry.png (default
/output/entry.png). No third-party libraries, no system fonts -- the
grader container only needs a plain Python 3 stdlib.

The image itself is a 3-panel comic (1024x1024): the user asks the agent
to "just clear my inbox while I'm on holiday"; the agent takes it
literally and tells the boss, the landlord and mum that the user is
dead. Punchline: "INBOX ZERO."

The artwork was rendered by draw.py (archived in this repo, PIL-based)
and stored as entry.png; this file only ships the finished PNG.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MAX_BYTES = 1_048_576  # 1 MiB cap

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

OUT_DIR = os.environ.get(
    "MAKEFUN_OUTPUT_DIR", os.environ.get("ENTRY_OUT", "/output")
)
OUT_PATH = os.path.join(OUT_DIR, "entry.png")


def main():
    if not os.path.isfile(SRC):
        raise SystemExit(f"missing bundled artwork: {SRC}")
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT_PATH)

    size = os.path.getsize(OUT_PATH)
    assert size <= MAX_BYTES, f"entry.png exceeds 1 MiB ({size} bytes)"
    with open(OUT_PATH, "rb") as fh:
        magic = fh.read(8)
    assert magic == b"\x89PNG\r\n\x1a\n", "entry.png is not a valid PNG"
    print(f"Wrote {OUT_PATH}: 1024x1024, {size} bytes")


if __name__ == "__main__":
    main()
