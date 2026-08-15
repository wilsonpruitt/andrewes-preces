#!/usr/bin/env python3.11
"""Bring the English layer's REFERENCE FORM into line with the plate.

The rule (BRIEF-notes-pass.md §6b): a reference the 1853 prints inside the text
is body text and follows the plate; a reference WE supplied is ours and follows
our own convention.

⚠ The decisive test is not the reference's appearance but whether the PLATE
prints one at that place — and the transcript and the English are line-keyed
1:1, so the test is exact: line i of a page in the transcript against line i of
the same page in the English. Verified before this tool was written: all 43
Part III pages align line-for-line with zero mismatches.

Two defects are being repaired, and the second is the serious one:

  1. arabic-colon (`[Job 14:14]`) where the plate prints roman (`*Job.* xiv. 14.`)
  2. ⚠⚠ OUR BRACKETS ERASE THE 1853 EDITOR'S. The plate distinguishes its own
     references from the ones its editor supplied by putting HIS in square
     brackets. The English brackets both alike, so a reader cannot tell whose
     hand put a reference there. NOTES-CONVENTIONS §7.4 exists to keep the three
     kinds of attribution apart; this is the one place in the edition that
     breaks it.

⚠ Bracket PLACEMENT on the plate varies (`[*Rom.* ix. 22.]` but `*Gen.* i. [31.]`),
so bracketing is copied from the plate per reference, never applied as a rule.

The English book abbreviation is kept as the English file already has it — this
tool does not translate book names, it only fixes numerals and brackets.

    python3.11 tools/refform.py            # dry run: report, change nothing
    python3.11 tools/refform.py --apply
"""
import re
import sys
import glob
from pathlib import Path

# an arabic reference as the English layer currently sets it: [Job 14:14]
ENG = re.compile(r"\[\s*((?:[123]\s*)?[A-Za-z][A-Za-z.]*)\s*(\d+):(\d+((?:\s*[,–-]\s*\d+)*))\s*\]")

# A reference as the PLATE sets it, on the raw transcript line, brackets included.
# ⚠⚠ THE FIRST FORM OF THIS PATTERN REQUIRED AN ITALIC BOOK TOKEN AND A LEADING
# BRACKET, and it silently mis-filed 52 references as "ours" — the safe-looking
# direction, and the wrong one. Two shapes defeated it, and both are common here:
#   (a) a BARE CHAPTER continuation, where the plate does not repeat the book
#       because the psalm is still running: `cxxxviii. 10.`
#   (b) an INTERIOR bracket, where the editor supplied only the verse figure and
#       the brackets fall inside the reference: `*Psal.* lxxxix. [46.]`
# (b) is exactly the distinction this tool exists to preserve, so missing it
# would have defeated the whole job while reporting success.
# §11b's rule applies: a widened pattern is diffed reference by reference against
# the old one, and its count proves nothing.
PLATE = re.compile(
    r"(?P<ob>\[)?\s*(?P<book>(?:[123]\s+)?\*[A-Za-z][A-Za-z.]*\*)?\s*"
    r"(?P<ib>\[)?\s*(?P<chap>[ivxlc]+)\.\s*"
    r"(?P<vb>\[)?\s*(?P<verse>\d+(?:\s*[,.]\s*\d+)*)\.?\s*(?P<cb>\])?",
    re.I)

ROMAN = [(100, "c"), (90, "xc"), (50, "l"), (40, "xl"), (10, "x"),
         (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]


def roman(n: int) -> str:
    out = []
    for v, s in ROMAN:
        while n >= v:
            out.append(s)
            n -= v
    return "".join(out)


def unroman(s: str) -> int:
    vals = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100}
    s = s.lower()
    tot = 0
    for i, ch in enumerate(s):
        v = vals[ch]
        tot += -v if i + 1 < len(s) and v < vals[s[i + 1]] else v
    return tot


def pages(path):
    """{printed page: [(file line index, text)]} — body lines only, 1:1 keyed."""
    out, cur = {}, None
    for i, ln in enumerate(Path(path).read_text().splitlines()):
        if re.match(r"\s*##\s", ln):        # Translator's flags &c. end the body
            cur = None
            continue
        m = re.match(r"\s*<!--\s*printed (\d+)", ln)
        if m:
            cur = int(m.group(1))
            out.setdefault(cur, [])
            continue
        if cur is None or ln.strip().startswith("<!--") or not ln.strip():
            continue
        out[cur].append((i, ln))
    return out


def main():
    apply = "--apply" in sys.argv
    tally = {"converted": 0, "ours": 0, "eyes": 0, "bare": 0}
    eyes = []

    for tpath in sorted(glob.glob("part3/*-transcript.md")):
        epath = tpath.replace("-transcript.md", "-english.md")
        T, E = pages(tpath), pages(epath)
        elines = Path(epath).read_text().splitlines()
        changed = False

        for p in sorted(set(T) & set(E)):
            if len(T[p]) != len(E[p]):
                eyes.append(f"p{p}: page line counts differ — skipped whole page")
                continue
            for (ti, traw), (ei, eraw) in zip(T[p], E[p]):
                erefs = list(ENG.finditer(eraw))
                if not erefs:
                    continue
                prefs = list(PLATE.finditer(traw))
                if not prefs:
                    # the plate prints nothing here: the reference is OURS
                    tally["ours"] += len(erefs)
                    continue
                if len(prefs) != len(erefs):
                    tally["eyes"] += len(erefs)
                    eyes.append(f"p{p} line {ti+1}: plate has {len(prefs)} ref(s), "
                                f"english has {len(erefs)} — {eraw.strip()[:70]}")
                    continue
                new = eraw
                # splice from the right so earlier spans stay valid
                for pm, em in sorted(zip(prefs, erefs), key=lambda z: -z[1].start()):
                    book, chap, verse = em.group(1), int(em.group(2)), em.group(3)
                    pchap = unroman(pm.group("chap"))
                    if pchap != chap:
                        tally["eyes"] += 1
                        eyes.append(f"p{p} line {ti+1}: chapter disagrees — "
                                    f"plate {pm.group('chap')}. ({pchap}) vs english {chap}")
                        continue
                    if not pm.group("book"):
                        # ⚠ THE PLATE DOES NOT REPEAT THE BOOK HERE. Whether our
                        # English may supply it, and how it should be marked as
                        # supplied, is a CONVENTION QUESTION and Wilson's to rule.
                        # Left exactly as it stands rather than guessed at.
                        tally["bare"] += 1
                        continue
                    verse = re.sub(r"\s*,\s*", ", ", verse.strip())
                    body = f"*{book.strip()}* {roman(chap)}. {verse}."
                    if pm.group("ob"):                      # whole reference his
                        tgt = f"[{body}]"
                    elif pm.group("vb") or pm.group("ib"):  # only the figure his
                        tgt = f"*{book.strip()}* {roman(chap)}. [{verse}.]"
                    else:
                        tgt = body
                    new = new[:em.start()] + tgt + new[em.end():]
                    tally["converted"] += 1
                if new != eraw:
                    elines[ei] = new
                    changed = True

        if apply and changed:
            Path(epath).write_text("\n".join(elines) + "\n")

    print(f"  plate-printed, reformatted to the plate : {tally['converted']}")
    print(f"  BARE continuation (plate omits the book): {tally['bare']}  <- Wilson's call, untouched")
    print(f"  OURS (plate prints nothing there), left : {tally['ours']}")
    print(f"  need eyes                               : {tally['eyes']}")
    for e in eyes[:40]:
        print("     ", e)
    if not apply:
        print("\n  dry run — nothing written. Re-run with --apply.")


if __name__ == "__main__":
    main()
