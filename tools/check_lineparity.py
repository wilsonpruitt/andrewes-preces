#!/usr/bin/env python3
"""Check that the three columns agree LINE FOR LINE, which the anchors depend on.

    python3.11 tools/transcript2tex.py        # build the fragments first
    python3.11 tools/check_lineparity.py

WHY THIS EXISTS. The note markers are keyed to a sense-line number, and one
numbering is made to serve all three columns: the figure set beside the Greek is
supposed to name the same line in the Latin recto and in the English. That holds
only if the columns have the same number of sense-lines. Where they do not, a
marker points at the wrong line AND LOOKS PERFECTLY RIGHT — nothing on the page
reveals it. So it is checked mechanically, over every page, before any note is
written against a line number.

⚠ It counts \\pl calls in the BUILT FRAGMENTS, not lines in the markdown. That is
the same thing the renderer numbers, so a line the parser drops (a comment, a
blank, a marker) is dropped here identically. Counting the source would measure
something the reader never sees.

⚠ A mismatch is NOT automatically an error in the files. The 1853 itself sets a
Latin page that runs a line longer or shorter than its Greek, and CONVENTIONS
keeps the plate as printed. What a mismatch means is: THIS PAGE CANNOT CARRY
LINE-KEYED NOTES until someone has looked. Report, do not repair.
"""
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAG = ROOT / "prototypes" / "fragments"
PL = re.compile(r"\\pl\{")


def count(name):
    p = FRAG / f"{name}.tex"
    return len(PL.findall(p.read_text())) if p.exists() else None


def main():
    if not FRAG.exists():
        raise SystemExit("no fragments — run tools/transcript2tex.py first")

    pages = defaultdict(dict)
    for f in FRAG.glob("*.tex"):
        m = re.match(r"^(gr|la|en)(\d{3})$", f.stem)
        if m:
            pages[int(m.group(2))][m.group(1)] = count(f.stem)

    bad_en, bad_la, checked = [], [], 0
    for n in sorted(pages):
        gr, la, en = (pages[n].get("gr"), pages.get(n + 1, {}).get("la"),
                      pages[n].get("en"))
        # The originals column for this unit: Greek in Part I, else whatever the
        # single column is.
        orig = gr if gr is not None else pages[n].get("la")
        if orig is None or en is None:
            continue
        checked += 1
        if orig != en:
            bad_en.append((n, orig, en))
        # ⚠ Only a real Part I OPENING is a facing-page parallel: an even Greek
        # verso with its own odd Latin recto. Parts II--III have Greek pages and
        # Latin pages but no parallel between them, so pairing n with n+1 there
        # compares two unrelated pages and invents mismatches.
        if gr is not None and la is not None and n <= 263 and n % 2 == 0 and gr != la:
            bad_la.append((n, gr, la))

    print(f"checked {checked} pages that carry both an original and an English\n")
    print(f"ENGLISH vs ORIGINAL — {len(bad_en)} mismatched")
    for n, o, e in bad_en:
        print(f"   printed {n:>3}: original {o:>3} lines, English {e:>3}"
              f"   ({e - o:+d})")
    print(f"\nLATIN recto vs GREEK verso (Part I) — {len(bad_la)} mismatched")
    for n, g, l in bad_la:
        print(f"   printed {n:>3}/{n + 1:>3}: Greek {g:>3}, Latin {l:>3}"
              f"   ({l - g:+d})")

    if bad_en or bad_la:
        print("\n⚠ Pages listed above CANNOT take line-keyed notes until someone "
              "has looked at them.\n  A mismatch may well be the plate's own — "
              "report, do not repair.")


if __name__ == "__main__":
    main()
