#!/usr/bin/env python3
"""Index every scripture reference in the plate by PRINTED PAGE and SENSE-LINE.

    python3.11 tools/ref_index.py 35          # one page
    python3.11 tools/ref_index.py --all       # the whole volume, as a count
    python3.11 tools/ref_index.py --stub 35   # print-notes.md S: lines, ready to fill

WHY THIS EXISTS. The scripture notes have to be anchored to a line or the reader
cannot tell which of fourteen references belongs to which line. The line number is
the edition's own coordinate — the 1853's apparatus keys everything as PAGE. LINE
and our transcripts are line-faithful, so our sense-line count IS its line count
(verified at printed 34, where Τὰ ἔργα τῶν χειρῶν σου is line 27, exactly as class
A says).

⚠ AND IT CHANGES WHAT THE NOTE PASS COSTS. The line number and the reference are
both already in the transcript; only the SITUATION has to be written. So this tool
emits the scaffold and the authored pass fills one clause per reference, instead of
locating 1,954 references by hand and getting the line numbers wrong.

⚠ Line numbers count \\pl calls — sense-lines, not typeset lines — because that is
what the renderer numbers and what the 1853 counted. Blank lines and the page
marker are not lines. A reference sitting on a line of its own (the plate does this
in the reference column of Part III) is reported on that line, which is where the
reader will look for it.

⚠ In Part I the references are printed on the LATIN recto, and the note goes on the
ENGLISH recto of the same opening. That is sound because the Latin is line-for-line
with the Greek and the English is line-keyed to the Greek: line N is the same line
on all three. Verified at printed 34/35.
"""
import argparse
import glob
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ⚠ The 1853 does not hold to ONE abbreviation per book: it prints *Matth.* beside
# *Matt.*, *Coloss.* beside *Col.*, *Ephes.*, *Galat.*, *Jerem.* Every long form must
# be listed in its own right and BEFORE its short form. Python backtracks into a
# later alternative when the first one fails, so short-first is not fatal — but a
# long form that is absent altogether matches nothing and the reference simply
# never enters the index. That is how *Ephes.* iv. 30 (printed 290, the Seal among
# the Spirit's four titles) went missing: the page showed four titles and the index
# offered three, and nothing anywhere said a reference had been dropped.
BOOK = (r"Gen|Exod|Ex|Lev|Num|Deut|Jos|Judg|Ruth|Reg|Sam|Chr|Esd|Neh|Tob|Judith"
        r"|Esth|Job|Psal|Ps|Prov|Pro|Eccl|Cant|Sap|Ecclus|Isai|Is|Jerem|Jer|Lam|Bar"
        r"|Ezek|Dan|Hos|Os|Joel|Am|Obad|Jon|Mic|Nah|Hab|Soph|Zeph|Agg|Zach|Mal"
        r"|Mac|Matth|Matt|Mat|Marc|Mar|Luc|Luk|Joh|Jo|Act|Rom|Cor|Galat|Gal"
        r"|Ephes|Eph|Phil|Coloss|Col"
        r"|Thess|Tim|Tit|Philem|Heb|Jac|Pet|Jud|Apoc|Rev")
# ⚠ `[12I]\.?` — the epistle numeral may carry its OWN period. The 1853 prints
# both `1 *Pet.* v. 6.` (meditations) and `1. *Pet.* v. 6.` (front matter, printed
# 18), and `2. *Sam.* ix. 8.` beside `2 *Sam.* xxiv. 16.` Without the optional dot
# the numeral is silently dropped and the reference indexes as plain `Pet. v. 6` —
# which reads as a DIFFERENT BOOK, and made four tags look as though they cited
# something not on their page at all.
# ⚠ `\b` before the numeral is load-bearing once the period is optional: with
# re.I, `[12I]\.?` otherwise matches the final letter of `ELI.` and indexes
# `[*Matth.* xxvii. 46.]` at printed 155 as **1** Matthew.
REF = re.compile(r"((?:\b[12I]\.?\s*)?(?:%s)\.?\s*[ivxlc]+\.?\s*[\d,\s.]*\d)" % BOOK,
                 re.I)
MARK = re.compile(r"<!--\s*printed (\d+)")


def index():
    """printed page -> [(line number, reference as printed)]"""
    out = {}
    for path in sorted(glob.glob(str(ROOT / "part*" / "*-transcript.md"))):
        page, line_no = None, 0
        for raw in Path(path).read_text().splitlines():
            m = MARK.match(raw.strip())
            if m:
                page, line_no = int(m.group(1)), 0
                out.setdefault(page, [])
                continue
            # The trailing apparatus prose is not part of the page.
            if raw.startswith("## "):
                page = None
                continue
            if page is None or not raw.strip():
                continue
            line_no += 1
            clean = re.sub(r"[*`\[\]]", "", raw)
            for ref in REF.findall(clean):
                out[page].append((line_no, re.sub(r"\s+", " ", ref).strip()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--stub", type=int,
                    help="emit print-notes.md S: lines for this page")
    args = ap.parse_args()
    idx = index()

    if args.stub:
        # In Part I the refs sit on the Latin recto; the note belongs to the
        # Greek page facing it, which is the one print-notes.md is keyed by.
        # print-notes.md is keyed by the UNIT, which in Part I is the even Greek
        # page — so an odd page's references are filed under the page before it.
        n = args.stub
        rows = idx.get(n) or idx.get(n + 1, [])
        key = n if idx.get(n) else n + 1
        if key % 2 == 1:
            key -= 1
        print(f"## {key}")
        for line, ref in rows:
            print(f"S: {line} {ref} — ")
        return

    if args.page:
        for line, ref in idx.get(args.page, []):
            print(f"  line {line:>3}   {ref}")
        return

    tot = sum(len(v) for v in idx.values())
    have = {k: v for k, v in idx.items() if v}
    d = sorted(len(v) for v in have.values())
    print(f"{tot} references on {len(have)} printed pages")
    print(f"per page — median {d[len(d) // 2]}, max {max(d)}")
    b = Counter(min(len(v), 15) for v in have.values())
    for k in sorted(b):
        print(f"   {k}{'+' if k == 15 else ''} refs: {b[k]} pages")


if __name__ == "__main__":
    main()
