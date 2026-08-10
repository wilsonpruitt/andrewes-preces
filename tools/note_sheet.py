#!/usr/bin/env python3
"""Worksheet for writing an opening's notes: the English page, numbered, with the
references that belong to it.

    python3.11 tools/note_sheet.py 34        # one opening
    python3.11 tools/note_sheet.py 30 70     # a range of openings

WHY. The `S:` note goes on the ENGLISH recto and is keyed to an ENGLISH line, but
in Part I the references are printed on the LATIN recto and `ref_index.py` reports
them by their LATIN line. Those agree on 111 of Part I's 131 openings and not on
20, so a Latin line number cannot simply be copied across.

⚠ AND IT CANNOT BE AUTOMATED. The obvious theory — that the Latin's extra lines
are cells and turned lines continuing onto a second line — was tested against all
20 mismatched openings and explains exactly ONE (printed 48/49, the table). Several
mismatches run the other way, the Latin being SHORTER than the Greek, which no
continuation rule can produce. They are the plate's own differences. So this prints
the two side by side and a person maps them; do not write a mapper.

The English line is the one that says what the reference is attached to. Read, do
not count.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ref_index import MARK, index  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def page_lines(page, pattern):
    for f in sorted(ROOT.glob(pattern)):
        cur, out = None, []
        for raw in f.read_text().splitlines():
            m = MARK.match(raw.strip())
            if m:
                cur = int(m.group(1))
                continue
            if raw.startswith("## "):
                cur = None
                continue
            if cur == page and raw.strip():
                out.append(raw.strip())
        if out:
            return out
    return []


def sheet(n, idx):
    en = page_lines(n, "part*/*-english.md")
    if not en:
        return
    refs = [(l, r, n) for l, r in idx.get(n, [])] + \
           [(l, r, n + 1) for l, r in idx.get(n + 1, [])]
    print(f"\n{'=' * 72}\n=== opening {n}/{n + 1} — {len(en)} English lines, "
          f"{len(refs)} references\n{'=' * 72}")
    print("--- references, by the line of the page they are PRINTED on ---")
    for l, r, pg in refs:
        src = page_lines(pg, "part*/*-transcript.md")
        txt = src[l - 1][:70] if l <= len(src) else ""
        print(f"   p{pg} L{l:>2}  {r:<22} | {txt}")
    print("--- the English recto, numbered: key the note to THESE figures ---")
    for i, line in enumerate(en, 1):
        print(f"   {i:>2}  {line[:96]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("first", type=int)
    ap.add_argument("last", type=int, nargs="?")
    a = ap.parse_args()
    idx = index()
    for n in range(a.first, (a.last or a.first) + 1, 2):
        sheet(n, idx)


if __name__ == "__main__":
    main()
