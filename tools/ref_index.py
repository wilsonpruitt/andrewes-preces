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
BOOK = (r"Gen|Exod|Ex|Lev|Num|Deut|Josh|Jos|Judic|Judg|Ruth|Reg|Sam|Paralip|Paral"
        r"|Chron|Chr|Esd|Nehem|Neh|Tob|Judith"
        r"|Esth|Job|Psal|Ps|Prov|Pro|Ecclus|Eccles|Eccl|Cant|Sap|Syr|Isai|Isa|Es|Is"
        r"|Jerem|Jer|Thren|Lam|Bar"
        r"|Ezech|Ezek|Ezr|Ez|Dan|Hos|Os|Joel|Amos|Am|Obad|Jon|Mich|Mic|Nah|Abac|Hab"
        r"|Soph|Zeph|Agg|Zech|Zach|Mal"
        r"|Mac|Matth|Matt|Mat|Marc|Mar|Luc|Luk|Joan|Joh|Jo|Act|Rom|Cor|Galat|Gal"
        r"|Ephes|Eph|Phil|Coloss|Col"
        r"|Thess|Tim|Tit|Philem|Heb|Jac|Pet|Jud|Apoc|Rev")
# ⚠ SIXTH INSTANCE of the same silent failure, found 2026-08-10 while opening printed
# 324: `*Thren.* iii. 59` (Threni = Lamentations) was absent, so the fourteenth and
# last term of §17's catalogue — *And all this Thou hast seen* — was not in the index
# at all. A volume-wide sweep of every italicised token followed by a roman numeral
# then turned up ~70 invisible references under NINETEEN missing forms: the Vulgate's
# `Joan` `Thren` `Ezech` `Mich` `Abac` `Judic` `Paralip`/`Paral` `Syr` (= Ecclesiasticus,
# which the 1853 itself glosses `[i. e. *Ecclus.*]`), the contracted `Es` (= Esaias,
# NOT Esther or Esdras — verified against all six: lxiv. 5, vi. 3, xxx. 15, li. 5,
# lvii. 11, l. 4) and `Ez` (= Ezekiel — ix. 6, xviii. 23, xxxiii. 11), and the plain
# English `Isa` `Josh` `Amos` `Zech` `Chron` `Nehem` `Eccles` `Ezr`.
# ⚠ `*Servitus.*` (printed 331, a heading) and `*sec.* LXX` are NOT books and must
# stay out: they match the token shape but not a reference. The sweep that found the
# nineteen is worth re-running whenever a new part is opened — see the recipe in
# `NOTES-CONVENTIONS.md` §11.
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
# The same pattern `proof2tex` strips before it decides a line is empty. Kept
# identical to it on purpose: the index must count exactly the lines the builder
# sets, or the band's figures and the page's ruler drift apart in silence.
COMMENT = re.compile(r"<!--.*?-->")


def index():
    """printed page -> [(line number, reference as printed)]

    ⚠⚠ LINE NUMBERS RUN CONTINUOUSLY ACROSS A PAGE THAT IS MARKED TWICE. 49 pages
    are marked in more than one section file — a section closing and the next
    opening on the same leaf — and the BUILDER concatenates both blocks into one
    fragment, so the page's sense-lines run 1..N straight through. An earlier
    version restarted the count at every marker, so every reference in a page's
    SECOND block was numbered relative to that block: on printed 299, where the
    Allegatio ends and the Confessio Laudis opens lower down, the fragment has 24
    lines and the index reported 1..18 and then 5, 6 — eighteen lines adrift, and
    pointing at real lines, so nothing looked wrong.
    """
    out = {}
    seen_lines = {}
    for path in sorted(glob.glob(str(ROOT / "part*" / "*-transcript.md"))):
        page, line_no = None, 0
        for raw in Path(path).read_text().splitlines():
            m = MARK.match(raw.strip())
            if m:
                page = int(m.group(1))
                line_no = seen_lines.get(page, 0)
                out.setdefault(page, [])
                continue
            # The trailing apparatus prose is not part of the page.
            if raw.startswith("## "):
                page = None
                continue
            if page is None or not raw.strip():
                continue
            # ⚠⚠ A COMMENT-ONLY LINE IS NOT A SENSE-LINE. The transcripts carry
            # editorial notes inline (`<!-- right brace over the three lines -->`,
            # `<!-- print unclear: οὗ / οὐ -->`), and `proof2tex.render_line` drops
            # them: they are not set, so they take no place in the printed column
            # and none on the margin's ruler. Counting them here put the index
            # AHEAD of the printed page by one for every comment above a
            # reference — printed 115's *Cruce* is the ninth line of the Latin and
            # was indexed as the eleventh — and since every tag takes its figure
            # from this count, the marker landed two lines below its own text on
            # every page that carries an inline comment. 58 pages do.
            if not COMMENT.sub("", raw).strip():
                continue
            line_no += 1
            seen_lines[page] = line_no
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
