#!/usr/bin/env python3
"""Search folding for three scripts (WEB-PLAN.md §12).

⚠⚠ FOLDED AT BUILD TIME, NEVER AT QUERY TIME, and never over the display text.
A reader who types `αγαπη` must find ἀγάπην, one who types `caelum` must find
`cœlum`, and one who types a Hebrew word without points must find it pointed.
Each line therefore carries a parallel folded field; the display text is
untouched.

⚠⚠⚠ THIS LOGIC EXISTS TWICE — here, and in site/src/lib/fold.ts, because the
query is folded in the browser. That is exactly the duplication this repo has
paid for before ("a JS reimplementation would be a third parser, and the drift
would be invisible"). It cannot be avoided without shipping Python to the
client, so instead it is MEASURED: `fold_tests()` emits input/expected pairs
into the index, and the client folds them itself on load and reports any
disagreement. The drift becomes loud instead of silent.
"""
import re
import unicodedata

# The Hebrew block's points and accents: niqqud, cantillation, meteg, sof
# pasuq. The consonants (U+05D0-U+05EA) are kept.
HEBREW_MARKS = re.compile(r"[֑-ׇ]")


def fold(text: str, hebrew: bool = False) -> str:
    """One line (or one query) reduced to its searchable form."""
    if hebrew:
        t = HEBREW_MARKS.sub("", text)
    else:
        # NFD then drop combining marks: this is what takes the accents and
        # breathings off polytonic Greek and the diacritics off Latin.
        t = unicodedata.normalize("NFD", text)
        t = "".join(c for c in t if not unicodedata.combining(c))
        t = t.lower()
        # ligatures the 1853 sets and a reader will not type
        t = t.replace("æ", "ae").replace("œ", "oe")
        # final sigma is the same letter
        t = t.replace("ς", "σ")
        # the 1853's orthography: v/u and j/i are one letter each in Latin
        t = t.replace("v", "u").replace("j", "i")
    t = re.sub(r"[^\w\s]", " ", t, flags=re.UNICODE)
    return " ".join(t.split())


def fold_spans(spans) -> str:
    """A line's spans -> its folded text, Hebrew spans folded as Hebrew."""
    out = []
    for s in spans:
        if s.get("kind") == "gap":
            continue
        t = s.get("text", "")
        if s.get("kind") == "strong":
            for c in s.get("children", []):
                out.append(fold(c.get("text", "")))
            continue
        if not t:
            continue
        out.append(fold(t, hebrew=s.get("kind") == "hebrew"))
    return " ".join(x for x in out if x)


def fold_tests():
    """Cases the browser must reproduce exactly. Chosen to exercise each rule
    on text this volume actually contains."""
    cases = [
        "ἀγάπην",          # Greek: breathing + accent
        "Δόξα σοι, Κύριε",  # Greek: capital, comma, final vowel
        "τοὺς φοβουμένους",  # Greek: two accents
        "ΤΗΣ ΠΡΩΤΗΣ ΗΜΕΡΑΣ",  # Greek: all caps
        "Cœlum",           # Latin: oe ligature
        "misericordiæ",    # Latin: ae ligature
        "Jesum Christum",  # Latin: j -> i
        "vivificans",      # Latin: v -> u
    ]
    out = [{"in": c, "out": fold(c)} for c in cases]
    out.append({"in": "יִצֶר טוֹב", "out": fold("יִצֶר טוֹב", hebrew=True), "hebrew": True})
    return out


if __name__ == "__main__":
    for t in fold_tests():
        print(f'{t["in"]!r:34} -> {t["out"]!r}')
