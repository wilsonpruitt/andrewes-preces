#!/usr/bin/env python3.11
r"""⚠ Sweep for LEAKED ASTERISKS in the built TeX — the eleventh tool-blindness class.

An unresolved markdown marker prints as a literal `*` in the finished book and
scrambles the emphasis around it. It is invisible in every other check: the band
looks complete, `check_notes` is happy, `--fit` says the page fits.

The cause was `[^*]+` in the bold regex (`proof2tex.md_emph`), which made
`**bold *italic* bold**` unmatchable, so the italic rule fired on the leftovers.
72 stood in the Part II TeX alone, every one of them in a note already committed.

⚠ The 1853 has footnote marks of its OWN — `τὸν νοῦν ἀδόκιμον.*` with its note in
§Deprecation (printed 202/203), and the Pliny note under ΥΜΝΟΣ ΕΩΘΙΝΟΣ (388).
Those must print, and are reported separately as expected.

⚠⚠ Classify by WHERE the asterisk is, not by what it looks like. A first version
asked "is an emphasis macro nearby?" and under-reported: it waved through
`\emph{.}* The prayer does not ask` and `}my grace is sufficient* to Paul`, two
genuinely scrambled notes, because the macro sat outside its window. The plate's
marks live in transcribed BODY lines (`\pl{}{}`) and nowhere else; an asterisk in
a band, a heading or a running head is markdown that failed to resolve.

⚠ The loeb build keeps its body in `fragments/` and only its BANDS inline, so both
are scanned — scanning the .tex alone would report the body clean however bad it got.

    python3.11 tools/audit_emphasis.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTO = ROOT / "prototypes"
# TeX's own asterisks: starred macros and lengths (\vspace*, 0.5\textheight*, \\*).
BENIGN = re.compile(r"(?:\\[A-Za-z@]+|\})\*(?=[{\\\d])|\*\{|\*\\|\\\\\*")
PL = re.compile(r"\\pl\{[-\d.]+\}\{")
# preamble.tex is hand-written TeX, not generated from markdown: its `*` are
# fontspec (`BoldFont={* Bold}`) and arithmetic inside comments.
SKIP = {"preamble.tex"}


def in_pl_body(s: str, pos: int) -> bool:
    r"""Is `pos` inside the second argument of a \pl{}{} line? Brace-counted, because
    a body line legitimately contains \emph{...} and a naive `}` test mis-reads it."""
    for m in PL.finditer(s):
        if m.end() > pos:
            return False
        depth, end = 1, len(s)
        for k in range(m.end(), len(s)):
            if s[k] == "{":
                depth += 1
            elif s[k] == "}":
                depth -= 1
                if depth == 0:
                    end = k
                    break
        if m.end() <= pos < end:
            return True
    return False


def scan(path: Path):
    broken, plate = [], []
    for i, line in enumerate(path.read_text().splitlines(), 1):
        s = BENIGN.sub("", line)
        if "*" not in s:
            continue
        for m in re.finditer(r"\*", s):
            a, b = max(0, m.start() - 50), m.start() + 50
            ctx = s[a:b].strip()
            (plate if in_pl_body(s, m.start()) else broken).append((i, ctx))
    return broken, plate


def main() -> int:
    targets = [t for t in sorted(PROTO.glob("*.tex"))
               + sorted((PROTO / "fragments").glob("*.tex"))
               if t.name not in SKIP]
    if not targets:
        print("no built .tex found — run transcript2tex.py first")
        return 0
    # ⚠ `proof2tex.py` and `transcript2tex.py` with no --part write ONLY the
    # volume-* files, so part1-proof.tex &c. can sit for weeks holding defects that
    # were fixed long ago. Reporting those as live findings sends a session hunting
    # a bug that is not there — which is exactly how this audit first misread itself.
    src = max(p.stat().st_mtime for p in
              [ROOT / "apparatus" / "print-notes.md", ROOT / "tools" / "proof2tex.py"])
    stale = [t for t in targets if t.stat().st_mtime < src]
    targets = [t for t in targets if t.stat().st_mtime >= src]
    if stale:
        print(f"⚠ skipping {len(stale)} STALE artefact(s), older than the sources "
              f"they were built from — rebuild before trusting them:")
        print("    " + ", ".join(sorted(t.name for t in stale)[:8])
              + (" …" if len(stale) > 8 else "") + "\n")

    nb = npl = 0
    for t in targets:
        broken, plate = scan(t)
        nb += len(broken)
        npl += len(plate)
        if broken:
            print(f"⚠⚠ {t.name}: {len(broken)} CONVERSION FAILURE(S)")
            for ln, ctx in broken[:10]:
                print(f"    line {ln}: …{ctx}…")
            if len(broken) > 10:
                print(f"    … and {len(broken) - 10} more")
    if npl:
        print(f"\n({npl} asterisk(s) inside transcribed body lines — the 1853's own "
              f"footnote marks. Expected; they must print.)")
    print("\n✅ no conversion failures." if not nb else
          "\n⚠⚠ Each prints as a literal asterisk in the book. Check the "
          "** / * pairing of the note in apparatus/ or the transcript.")
    return 1 if nb else 0


if __name__ == "__main__":
    sys.exit(main())
