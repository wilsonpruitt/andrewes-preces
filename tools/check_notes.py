#!/usr/bin/env python3.11
"""Three checks on apparatus/print-notes.md that nothing else can see.

    python3.11 tools/check_notes.py            # all three, whole book
    python3.11 tools/check_notes.py 286 290    # one printed range

⚠ WHY THIS EXISTS. Two silent failures got into committed work before it did,
and neither was visible in the built PDF, in `--fit`, or by reading the page:

1. **ORDER.** The builder groups band entries in the order the FILE gives them,
   not in line order. A tag inserted next to the wrong neighbour prints its
   roman out of sequence, and the markers above then run i, iii, ii down the
   page. Nothing errors; the page just quietly stops being usable.

2. **COVERAGE.** `ref_index.py` is where a tag's line number comes from, so a
   reference the index cannot see is a reference the pass never learns exists.
   *Ephes.* iv. 30 (printed 290, the Seal among the Spirit's four titles) was
   missing from BOOK for the whole of Part I and half of Part II: the plate
   showed four titles and the index offered three. Thirteen references were
   dropped that way. Coverage is reported as a WARNING, not an error — §8 of
   NOTES-CONVENTIONS says to SELECT on a crowded page, so an untagged reference
   is often the right call. The point is to make the choice visible.

3. **NUMBERING.** ⚠ The one to read carefully. Where a tag cites a chapter-and-
   verse that the plate does not print, one of three quite different things is
   true, and they must not be levelled:
     - the plate is using the PRAYER BOOK's numbering and is RIGHT (Ps. xxxi. 6
       is BCP for the AV's xxxi. 5) — NOTES-CONVENTIONS §6 forbids correcting it;
     - the plate has a genuine misprint (Ps. cxli. 8 for cxli. 3, which is verse
       3 in AV, BCP and Vulgate alike) — kept as printed, true verse NAMED;
     - the reference is the 1853 EDITOR's, in his brackets, and the slip is his
       (the `[1 Cor. viii. 12]` → 2 Cor. at printed 62).
   This check cannot tell them apart. It only says: here the band and the plate
   above it disagree, and a reader will see both. Never auto-fix from it.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ref_index  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "apparatus" / "print-notes.md"

# Enough of a book map to compare a tag's citation with the plate's. Both sides
# are abbreviations of the same book, so this only has to make them agree with
# each other — it is not a canon list.
BOOKS = {
    "psal": "ps", "ps": "ps", "matth": "mt", "matt": "mt", "mat": "mt",
    "marc": "mk", "mar": "mk", "mark": "mk", "luc": "lk", "luke": "lk",
    "luk": "lk", "jo": "jn", "joh": "jn", "john": "jn", "act": "ac",
    "acts": "ac", "rom": "rom", "coloss": "col", "col": "col",
    "galat": "gal", "gal": "gal", "ephes": "eph", "eph": "eph",
    "jerem": "jer", "jer": "jer", "pro": "prov", "prov": "prov",
    "eccl": "eccl", "eccles": "eccl", "is": "is", "isai": "is", "isa": "is",
    "heb": "heb", "tit": "tit", "titus": "tit", "jac": "jas", "jas": "jas", "sam": "sam",
    "reg": "reg", "kings": "reg", "cor": "cor", "thess": "th", "tim": "tim",
    "pet": "pet", "rev": "rev", "apoc": "rev", "gen": "gen", "exod": "ex",
    "ex": "ex", "deut": "dt", "dt": "dt", "job": "job", "dan": "dan",
    "zach": "zech", "zech": "zech", "os": "hos", "hos": "hos", "jud": "jud",
    "jude": "jud", "num": "num", "lev": "lev", "judg": "judg", "neh": "neh",
    "esth": "esth", "cant": "cant", "lam": "lam", "ezek": "ezek",
    "ezech": "ezek", "mic": "mic", "hab": "hab", "zeph": "zeph", "mal": "mal",
    "jon": "jon", "joel": "joel", "am": "am", "nah": "nah", "bar": "bar",
    "sap": "sap", "ecclus": "ecclus", "tob": "tob", "mac": "mac",
    "chr": "chr", "esd": "esd", "philem": "philem", "phil": "phil",
    "ruth": "ruth", "jos": "jos", "obad": "obad", "soph": "soph",
    "agg": "agg", "judith": "judith", "wisd": "sap",
}
NUMERALS = [("m", 1000), ("cm", 900), ("d", 500), ("cd", 400), ("c", 100),
            ("xc", 90), ("l", 50), ("xl", 40), ("x", 10), ("ix", 9),
            ("v", 5), ("iv", 4), ("i", 1)]
CITE = re.compile(r"([12I]?\s*[A-Za-z]+)\.?\s*([ivxlcIVXLC]+)\.?\s*(\d+)")


def roman_value(s):
    s, n, i = s.lower(), 0, 0
    while i < len(s):
        for r, v in NUMERALS:
            if s.startswith(r, i):
                n += v
                i += len(r)
                break
        else:
            return None
    return n


def citation(text):
    """('1', 'cor', 11, 29) from any of `1 Cor. xi. 29`, `1 *Cor.* xi. 29.`"""
    m = CITE.match(text.strip().lstrip("[").replace("*", "").strip())
    if not m:
        return None
    book, chap, verse = m.groups()
    book = book.strip()
    prefix = ""
    if book and book[0] in "12I":
        prefix, book = ("1" if book[0] == "I" else book[0]), book[1:].strip()
    key = BOOKS.get(book.lower())
    ch = roman_value(chap)
    if not key or ch is None:
        return None
    return (prefix, key, ch, int(verse))


def load_notes():
    """printed page -> list of (stream, line number or None, body)."""
    out, page = {}, None
    for raw in NOTES.read_text().splitlines():
        line = raw.strip()
        m = re.match(r"^## (\d+)$", line)
        if m:
            page = int(m.group(1))
            continue
        m = re.match(r"^([VRS]): (.+)$", line)
        if m and page is not None:
            body = m.group(2)
            n = re.match(r"^(\d+)(?:\s|$)", body)
            out.setdefault(page, []).append(
                (m.group(1), int(n.group(1)) if n else None, body))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lo", nargs="?", type=int)
    ap.add_argument("hi", nargs="?", type=int)
    args = ap.parse_args()

    notes, idx = load_notes(), ref_index.index()
    pages = sorted(notes)
    if args.lo:
        hi = args.hi or args.lo
        pages = [p for p in pages if args.lo <= p <= hi]

    # the plate's own citations, by page and by line
    plate = {}
    for p, rows in idx.items():
        for ln, ref in rows:
            c = citation(ref)
            if c:
                plate.setdefault(p, {}).setdefault(ln, set()).add(c)

    order_bad, missing, mismatch = [], [], []
    for p in pages:
        entries = notes[p]
        # 1. order, within each stream
        for stream in "VSR":
            seen = [ln for s, ln, _ in entries if s == stream and ln is not None]
            if seen != sorted(seen):
                order_bad.append((p, stream, seen))

        # ⚠ p OR p+1, never both. This is `ref_index --stub`'s own rule: in Part I
        # the references are printed on the LATIN recto and filed under the even
        # page facing it, so the plate's citations live under p+1; in Parts II–III
        # each page carries its own. Unioning the two charges every page with its
        # neighbour's references and reports a page as uncovered because the NEXT
        # page's refs are untagged.
        on_plate = set()
        for s in (plate.get(p) or plate.get(p + 1, {})).values():
            on_plate |= s

        tagged = set()
        for stream, _, body in entries:
            if stream != "S":
                continue
            # ⚠ strip the leading sense-line figure first. "11 Acts i. 7" parses
            # otherwise as *1 Acts* — the line figure swallowed as the book's
            # first/second-epistle prefix — so every tag on a line numbered 1, 2
            # or 12 gets reported as disagreeing with a plate that agrees with it.
            # ⚠ scan the WHOLE entry, not the part before the first em dash: a
            # line carrying two references is ONE tag with two citations —
            # "Gal. iv. 19 — Paul in travail …; Eph. iv. 13 — *unto a perfect
            # man*" — and splitting on the dash throws the second one away, so
            # a reference that IS tagged gets reported as uncovered.
            for m in CITE.finditer(re.sub(r"^\d+\s+", "", body)):
                c = citation(m.group(0))
                if not c:
                    continue
                tagged.add(c)
                if c not in on_plate:
                    near = sorted(x for x in on_plate if x[:3] == c[:3])
                    mismatch.append((p, m.group(0).strip(), near))

        # 3. coverage — a plate reference with no tag anywhere on the page
        for c in sorted(on_plate - tagged):
            missing.append((p, c))

    def show(c):
        return "%s%s %d:%d" % (c[0] + " " if c[0] else "", c[1], c[2], c[3])

    print("=" * 70)
    print("1. ORDER — S:/R:/V: entries out of line order (ERROR: fix these)")
    print("=" * 70)
    for p, stream, seen in order_bad:
        print(f"  printed {p:>3}  {stream}:  {seen}")
    print(f"  {len(order_bad)} pages out of order\n")

    print("=" * 70)
    print("2. NUMBERING — band and plate disagree (ADJUDICATE, never auto-fix)")
    print("=" * 70)
    for p, tag, near in mismatch:
        seen = ", ".join(show(c) for c in near) or "— not on the page at all —"
        print(f"  printed {p:>3}  tag `{tag}`   plate: {seen}")
    print(f"  {len(mismatch)} disagreements\n")

    print("=" * 70)
    print("3. COVERAGE — plate references carrying no tag (WARNING: often right)")
    print("=" * 70)
    by_page = {}
    for p, c in missing:
        by_page.setdefault(p, []).append(show(c))
    for p in sorted(by_page):
        print(f"  printed {p:>3}  {', '.join(by_page[p])}")
    print(f"  {len(missing)} untagged on {len(by_page)} pages\n")

    return 1 if order_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
