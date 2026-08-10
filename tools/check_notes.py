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
    # ⚠ "jud" -> JUDGES, not Jude. The 1853 abbreviates Judges `Jud.` (printed 282,
    # Abimelech and the men of Shechem). The two collapse here on purpose: this map
    # only has to make a tag and the plate agree with each other, and a missed
    # disagreement is far cheaper than a false one sent to an editorial pass.
    "zach": "zech", "zech": "zech", "os": "hos", "hos": "hos", "jud": "judg",
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
# ⚠ The epistle numeral gets its own group AND its own optional period. The 1853
# prints `1. *Pet.* v. 6.` as well as `1 *Pet.* v. 6.`; folding the numeral into
# the book group meant "1. Pet." parsed as plain "Pet." — a different book — so a
# correctly-keyed tag was reported as citing something not on its page.
CITE = re.compile(r"(?:([12I])\.?\s*)?([A-Za-z]+)\.?\s*([ivxlcIVXLC]+)\.?\s*(\d+)")


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
    prefix, book, chap, verse = m.groups()
    prefix = "1" if prefix == "I" else (prefix or "")
    key = BOOKS.get(book.strip().lower())
    ch = roman_value(chap)
    if not key or ch is None:
        return None
    return (prefix, key, ch, int(verse))


def parity_unsafe():
    """Printed pages whose English and originals do NOT have the same sense-line
    count — the pages `check_lineparity.py` says cannot carry line-keyed notes.

    ⚠ Read from the BUILT FRAGMENTS, the same source check_lineparity counts, so
    the two tools can never disagree about which pages are safe.
    """
    frag = ROOT / "prototypes" / "fragments"
    if not frag.exists():
        return set()
    pl = re.compile(r"\\pl\{")

    def count(name):
        f = frag / f"{name}.tex"
        return len(pl.findall(f.read_text())) if f.exists() else None

    # ⚠⚠ The column that must agree with the English is the one CARRYING THE
    # REFERENCES — in Part I that is the LATIN RECTO, not the Greek verso. An
    # earlier version gated on Greek-vs-English and so declared printed 48, 86,
    # 258 and 262 safe to compare when the Latin runs +6, -2, -1 and +1 lines
    # against them; the checker then lined tags up against references from a
    # different line entirely and reported a tag on 1 Cor. xi as disagreeing with
    # Colossians. The 20 openings where Latin and Greek differ are exactly the
    # ones check_lineparity's second table names.
    out = set()
    for f in frag.glob("en*.tex"):
        # ⚠ the fragment directory also holds split variants (`en204-h2`) left
        # over from the M2 prototypes; only the plain three-digit pages are units.
        m = re.match(r"^en(\d{3})$", f.stem)
        if not m:
            continue
        n = int(m.group(1))
        en = count(f.stem)
        # Part I: the references are on the Latin recto facing this page.
        ref_col = count(f"la{n + 1:03d}") if count(f"gr{n:03d}") is not None \
            else count(f"la{n:03d}")
        if ref_col is None or en is None or ref_col != en:
            if ref_col is not None and en is not None:
                out.add(n)
    return out


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
    # ⚠ EXPAND MULTI-VERSE REFERENCES. The 1853 prints `*Mat.* viii. 2, 8.` and
    # `*Act.* x. 9, 11.` — one reference naming two verses — and reading only the
    # first number makes the second invisible. Both tags on Matt. viii were
    # reported as disagreeing with a plate that cites exactly what they cite.
    plate = {}
    for p, rows in idx.items():
        for ln, ref in rows:
            c = citation(ref)
            if not c:
                continue
            plate.setdefault(p, {}).setdefault(ln, set()).add(c)
            tail = ref[ref.index(str(c[3])) + len(str(c[3])):]
            for extra in re.findall(r"[,&]\s*(\d+)", tail):
                plate[p][ln].add((c[0], c[1], c[2], int(extra)))

    order_bad, missing, mismatch = [], [], []
    supplied, unchecked = [], []
    unsafe = parity_unsafe()
    for p in pages:
        entries = notes[p]
        # 1. order, within each stream
        for stream in "VSR":
            seen = [ln for s, ln, _ in entries if s == stream and ln is not None]
            if seen != sorted(seen):
                order_bad.append((p, stream, seen))

        # ⚠⚠ CHECK 2 IS LINE-KEYED, and it has to be. Comparing a tag against
        # every reference anywhere on the page produced mostly noise: printed 2
        # tags Ps. cxix. 164 (the seven-times-a-day verse, which the plate does
        # not print at all) and the page happens to carry Ps. cxix. 62, so a
        # perfectly good tag was reported as disagreeing with a plate it never
        # touched. Same book and chapter is not the same reference.
        #
        # So the only real question is: on the line this tag is keyed to, does
        # the plate print a reference, and does it print the SAME verse?
        #   - plate prints nothing there  -> the tag SUPPLIES a reference the
        #     1853 left unmarked. Normal, and often the best thing on the page.
        #   - plate prints a different verse -> a real disagreement, the reader
        #     sees both figures on one opening, and it must be adjudicated.
        #
        # ⚠ A parity-mismatched page cannot be compared at all: there the tag's
        # English line number and the plate's line number are different counts,
        # so line N on one side is not line N on the other. Those pages are
        # reported as UNCHECKED rather than silently compared, which is the same
        # discipline check_lineparity applies to writing the notes in the first
        # place.
        refpage = p + 1 if (p <= 263 and p % 2 == 0) else p
        by_line = plate.get(refpage, {})
        if p in unsafe:
            unchecked.append(p)
            continue

        tagged = set()
        for stream, ln, body in entries:
            if stream != "S" or ln is None:
                continue
            here = by_line.get(ln, set())
            for m in CITE.finditer(re.sub(r"^\d+\s+", "", body)):
                c = citation(m.group(0))
                if not c:
                    continue
                tagged.add(c)
                # ⚠ Only a SAME-BOOK difference is a disagreement. A line may
                # carry the plate's reference and a second one the pass supplied
                # from a different book entirely — printed 210 line 18 is the
                # plate's Luke xvii. 5 plus our Heb. iii. 6, which is an addition,
                # not a contradiction. Flagging those as numbering errors would
                # send an editorial pass to change a figure that is not wrong.
                same_book = [x for x in here if x[:2] == c[:2]]
                if not here:
                    supplied.append((p, ln, m.group(0).strip()))
                elif c in here:
                    pass
                elif same_book:
                    mismatch.append((p, ln, m.group(0).strip(), sorted(same_book)))
                else:
                    supplied.append((p, ln, m.group(0).strip()))

        on_plate = set()
        for s in by_line.values():
            on_plate |= s

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
    for p, ln, tag, here in mismatch:
        seen = ", ".join(show(c) for c in here)
        print(f"  printed {p:>3} line {ln:>2}  tag `{tag}`   plate prints: {seen}")
    print(f"  {len(mismatch)} disagreements\n")

    print("=" * 70)
    print("2b. SUPPLIED — tag names a reference the plate does not print there")
    print("=" * 70)
    print(f"  {len(supplied)} supplied references "
          f"(informational: the 1853 left the line unmarked and the pass named it)")
    if unchecked:
        print(f"  ⚠ {len(unchecked)} pages NOT compared — parity mismatch, the two "
              f"columns are on different line counts: {unchecked}")
    print()

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
