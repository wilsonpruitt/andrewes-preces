#!/usr/bin/env python3
"""Merge the scripture index from its TWO sources (WEB-PLAN.md §9).

    marked      — the plate printed the reference. Source: ref_index.index().
    identified  — the `S:` band names a verse the plate never marked.

⚠⚠ THE MERGE EXISTS BECAUSE AN INDEX BUILT FROM THE MARKS UNDER-REPORTS, and
the notes pass proved it. §37 (printed 374--379) is six unmarked leaves: the
plate cites nothing on any of them and the confession is built of allusion it
never references. Printed 335's brace fastens `ariditas` to Is. xxiv. 16 and
the fountain of tears to Jer. ix. 1, and BOTH return unreferenced at 376 and
378. An index that joins only the marks joins none of §37.

⚠ The two are tagged distinctly and never blended. A mark is the 1853's own
act; an identification is this edition's reading, and a reader must be able to
tell which they are looking at.

⚠⚠ NOTHING HERE RENUMBERS A PSALM. The volume is not on one Psalter — plain AV
(300), plain Vulgate (274), BCP (433, 356), and a hybrid at 344 and 353 that
sets the Vulgate's verse-figure under the Hebrew psalm-number. The index
carries the figure AS PRINTED and, where the note says which Psalter it is,
shows the note. The notes pass already recorded this per reference, in prose
("the plate's figure, which is the Vulgate's numbering of the psalm our Bibles
call cxviii"; "Prayer Book numbering"), so the discriminator is READ, not
inferred.

⚠ Wrong references are kept as printed and flagged, never mended: `Jer. l. 24`
is a roman FIFTY, `Eph. i. 8` wants i. 18, `Dan. vi. 4` wants vi. 10. The `S:`
band already says so in its own words ("the plate's figure ... Kept as
printed"), so the flag here only surfaces the note.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ref_index
import transcript2tex
from bible_books import (BOOKS, BOOK_ORDER, ALIASES, AMBIGUOUS_JUD,
                         INSTANCE_OVERRIDES, LONG_FORMS, resolve, roman_to_int)

# Every abbreviation either source actually uses, longest first so `Matth`
# wins over `Matt` over `Mat`. Built FROM the alias table rather than written
# out again, so a book can never be in one and missing from the other.
# ⚠⚠ ONE alternation over BOTH the plain forms and the book-part of the
# numbered ones (`1 Cor.` -> `cor`), sorted LONGEST FIRST. Keeping them in two
# groups tried `jo` (from `1 Jo.`) before `job` and matched inside the word
# JOB, so `Job xxxiii. 27` parsed as a bookless fragment and sixty perfectly
# good notes were refused. Alternation order is not cosmetic here.
_FORMS = sorted(
    {f for f in set(ALIASES) | AMBIGUOUS_JUD if not f[0].isdigit()}
    | {f[1:] for f in set(ALIASES) if f[0].isdigit()},
    key=len, reverse=True,
)
_ALT = "|".join(re.escape(f) for f in _FORMS)

# A citation: optional epistle numeral, book, optional roman chapter, verses.
# ⚠ The left-hand guard is ref_index.py's `NOLETTER`, and it is load-bearing
# for the same reason it is there: without it the alternation matches the TAIL
# of an ordinary word — the `am` of *quoniam* as Amos, the `is` of *nobis* as
# Isaiah — and manufactures references that look perfectly plausible.
# ⚠ The right-hand `(?![A-Za-z])` is the same guard on the other side, and it
# is what stops a short form matching the HEAD of a longer word.
CITE = re.compile(
    r"(?<![^\W\d_])"
    r"(?:(?P<num>[123])\.?\s*)?"
    r"(?P<book>%s)(?![A-Za-z])\.?\s*"
    r"(?:(?P<roman>[ivxlc]+)(?![A-Za-z])\s*[.·]?\s*)?"
    r"(?P<verses>\d+(?:\s*[–—-]\s*\d+)?(?:\s*[,.]\s*\d+(?:\s*[–—-]\s*\d+)?)*)?"
    % _ALT,
    re.I,
)

# ⚠ The `R:` band is PROSE and names its books in full ("Romans vii. 18 stands
# here word for word and unmarked"), so it gets its own, WIDER alternation. It
# is deliberately NOT used on the plate or the `S:` band: widening a pattern
# that already works is how this project manufactured five ghost references.
_ALT_PROSE = "|".join(re.escape(f) for f in sorted(
    set(_FORMS) | set(LONG_FORMS), key=len, reverse=True))
CITE_PROSE = re.compile(
    r"(?<![^\W\d_])"
    r"(?:(?P<num>[123])\.?\s*)?"
    r"(?P<book>%s)(?![A-Za-z])\.?\s*"
    r"(?P<roman>[ivxlc]+)(?![A-Za-z])\s*[.·]?\s*"
    r"(?P<verses>\d+(?:\s*[,.]\s*\d+)*)"
    % _ALT_PROSE, re.I)


def prose_citations(text: str):
    """Citations named in an explanatory note. Chapter AND verse are both
    required — a bare book name in prose ("Job's words") is not a citation."""
    out = []
    for m in CITE_PROSE.finditer(text):
        tok = (m.group("num") or "") + m.group("book")
        slug = resolve(tok, True) or LONG_FORMS.get(tok.strip().lower())
        if not slug:
            continue
        out.append((slug, roman_to_int(m.group("roman")),
                    expand_verses(m.group("verses")), m.group(0).strip()))
    return out


# The editor's supplied brackets and the band's lemma backticks wrap a head
# without being part of it: `[2 Cor. viii. 12]` is a citation.
def _clean_head(h: str) -> str:
    return h.strip().strip("`").strip().strip("[]").strip()

# Phrases in which the notes pass recorded WHICH Psalter a figure belongs to.
# Matched to surface the note, never to convert a number.
NUMBERING = re.compile(
    r"Vulgate|Prayer Book|Coverdale|Authorised|\bAV\b|LXX|Septuagint"
    r"|numbering|versification|Hebrew psalm",
    re.I,
)
# The notes pass's own formula for "as printed, and here is what it wants".
PLATE_FIGURE = re.compile(r"plate's figure|kept as printed", re.I)


def expand_verses(raw):
    """'15, 16' -> [15, 16]; '8–12' -> [8..12]. A range is expanded so a reader
    looking for Ps. ciii. 10 finds the note that took five verses together."""
    out = []
    for part in re.split(r"[,.]", raw or ""):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^(\d+)\s*[–—-]\s*(\d+)$", part)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            out.extend(range(a, b + 1) if a <= b <= a + 50 else [a])
        elif part.isdigit():
            out.append(int(part))
    return out


def parse_citations(text: str):
    """EVERY complete citation in `text`, in order. A note head may name two
    ("Is. xlii. 3, and Matt. xii. 20 quoting it" — prophecy and fulfilment)."""
    out = []
    for m in CITE.finditer(text):
        if not (m.group("roman") or m.group("verses")):
            continue
        slug = resolve((m.group("num") or "") + m.group("book"), bool(m.group("roman")))
        if not slug:
            continue
        ch = roman_to_int(m.group("roman")) if m.group("roman") else None
        verses = expand_verses(m.group("verses"))
        if ch is None and verses:
            ch = 1
        out.append((slug, ch, verses, m.group(0).strip()))
    return out


def parse_citation(text: str):
    """A citation string -> (slug, chapter, [verses], ok) or None.

    Returns the FIRST citation in `text`. `chapter` is None for a chapterless
    book cited by verse alone (Jude 23), whose verse then stands as the verse.
    """
    m = CITE.search(text)
    if not m:
        return None
    token = (m.group("num") or "") + m.group("book")
    roman = m.group("roman")
    slug = resolve(token, chapter_is_roman=bool(roman))
    if not slug:
        return None
    chapter = roman_to_int(roman) if roman else None
    verses = expand_verses(m.group("verses"))
    if chapter is None and verses:
        # a chapterless book: the bare numeral is the verse, chapter 1
        chapter = 1
    return slug, chapter, verses, m.group(0).strip()


def triple(slug, chapter, verses):
    """The identity a marked and an identified reference are matched on.

    ⚠ The WHOLE triple, never the numerals alone. Printed 319 line 3 carries a
    marked `1 Tim. i. 14` and an identified `Eph. i. 14` — same chapter, same
    verse, different books, both genuinely on that line.
    """
    return (slug, chapter, verses[0] if verses else None)


def units_by_page():
    """printed page -> the UNIT page its notes are filed under.

    In Part I the plate prints its references on the LATIN recto while the
    `S:` note goes on the English recto of the same opening, and
    `print-notes.md` is keyed by the opening's even Greek page. So a reference
    on printed 35 must be compared against notes filed at 34.
    """
    pages = transcript2tex.volume_pages([1, 2, 3])
    unit_of = {}
    skip = set()
    for n in sorted(pages):
        if n in skip:
            continue
        slot = pages[n]
        nxt = pages.get(n + 1)
        paired = (
            slot["part"] == 1
            and slot["layer"] == "gr"
            and n % 2 == 0
            and nxt
            and nxt["layer"] == "la"
            and nxt["part"] == 1
            and not nxt["en"]
        )
        unit_of[n] = n
        if paired:
            unit_of[n + 1] = n
            skip.add(n + 1)
    return unit_of


# A candidate `<head> — <situation>` split, at the entry head or after "; ".
_CAND = re.compile(r"(?:^|;\s*)([^;—]+?)\s+—\s+")
# The plate's own continuation form, quoted as a lemma: `Vers. 24`, `Ibid. 5`.
_CONT_HEAD = re.compile(r"^`?\s*(?:Vers|Ibid)\b", re.I)
# A second chapter of the book just named, cited bare — ref_index.py's SEMI
# class, here on the notes side: "John viii. 59 — …; and x. 31, 33 — …".
_BARE_CH = re.compile(
    r"^(?:and\s+)?(?P<roman>[ivxlc]+)\s*[.·]?\s*(?P<verses>\d+(?:\s*[,.]\s*\d+)*)\s*$",
    re.I)
# What the note's prose offers when its head is a continuation form.
_IE = re.compile(r"i\.\s*e\.\s*(?P<cite>[^,;:*]+)", re.I)


def head_kind(head: str):
    """Is this candidate head a REFERENCE, or is it prose?

    ⚠ THIS GUARD IS THE POINT. The band's separator is ` — `, and a situation
    may contain one of its own ("Job vii. 20 — *I have sinned; what shall I do
    unto thee?* — Job's words made the petition"). Splitting on the shape alone
    tore five situations in half and offered their second halves up as
    references. Nothing false entered the index, because prose does not parse
    as a citation — but the truncation was silent, and the rule this repo has
    paid for twice is that a widened or narrowed pattern is checked item by
    item, never on its count.
    """
    h = head.strip()
    if _CONT_HEAD.match(h):
        return "cont"
    bare = _clean_head(h)
    if _BARE_CH.match(bare):
        return "bare"
    m = CITE.search(bare)
    # The head must OPEN with a citation carrying a chapter or a verse. The
    # chapter/verse requirement is what does the work: "Job's words made the
    # petition for pardon" opens with a book name and nothing else, and is
    # prose — the tail of a situation torn in half at its own em-dash.
    if m and m.start() == 0 and (m.group("roman") or m.group("verses")):
        if resolve((m.group("num") or "") + m.group("book"), bool(m.group("roman"))):
            return "cite"
    return None


def parse_s_entry(entry: str):
    """An `S:` band entry -> (line, [(kind, head, situation), ...]).

    The band's shape is regular — `<line> <ref> — <situation>`, and a line
    carrying several references sets them `; `-separated in the same entry.
    Anchored on that shape rather than scanned as free prose: a scan would
    read the italicised quotation itself for book names.
    """
    m = re.match(r"^(\d+)(?:\s*[–-]\s*\d+)?\s+(.*)$", entry, re.S)
    if not m:
        return None, []
    line, rest = int(m.group(1)), m.group(2)
    accepted = []
    for cand in _CAND.finditer(rest):
        kind = head_kind(cand.group(1))
        if kind:
            accepted.append((kind, cand.group(1).strip(), cand.start(1), cand.end()))
    segs = []
    for i, (kind, head, _, end) in enumerate(accepted):
        stop = accepted[i + 1][2] if i + 1 < len(accepted) else len(rest)
        situation = rest[end:stop].strip().rstrip(";").strip()
        segs.append((kind, head, situation))
    return line, segs


def build():
    """-> (books, entries, report)"""
    idx = ref_index.index()
    notes = transcript2tex.load_notes()
    unit_of = units_by_page()

    # --- the plate's marks ------------------------------------------------
    marked = []            # every reference the 1853 printed
    by_unit_line = defaultdict(set)   # (unit, line) -> {triple}
    unparsed_plate = []
    for page, rows in sorted(idx.items()):
        unit = unit_of.get(page, page)
        for line, ref in rows:
            p = parse_citation(ref)
            if not p:
                unparsed_plate.append((page, line, ref))
                continue
            slug, ch, verses, _ = p
            # a per-instance identity, where the abbreviation is two books
            slug = INSTANCE_OVERRIDES.get((page, ref), slug)
            marked.append({
                "book": slug, "chapter": ch, "verses": verses,
                "printed": ref, "page": page, "line": line, "source": "marked",
            })
            by_unit_line[(unit, line)].add(triple(slug, ch, verses))

    # every triple the plate marks anywhere in an opening, for the fallback
    by_unit = defaultdict(set)
    for (unit, _line), triples in by_unit_line.items():
        by_unit[unit] |= triples

    # --- the notes pass's identifications ---------------------------------
    identified = []
    situations = {}        # (unit, line, triple) -> situation, for marked refs
    empty_entries = []
    unparsed_notes = []
    offset_matches = []    # matched on the opening, not the line — see below
    for unit_page, bands in sorted(notes.items()):
        for entry in bands.get("S", []):
            line, segs = parse_s_entry(entry)
            if line is None:
                continue
            if not segs:
                empty_entries.append((unit_page, entry))
                continue
            last_book = None
            for kind, head, situation in segs:
                if kind == "cont":
                    # The head is the plate's own `Vers.`/`Ibid.` form, which
                    # ref_index has already resolved on the plate side. Take
                    # the verse from the note's own gloss ("i.e. Luke vii. 38")
                    # and fall back to the single reference the plate marks on
                    # that line — never to a guess.
                    ie = _IE.search(situation)
                    p = parse_citation(ie.group("cite")) if ie else None
                    if not p:
                        here = by_unit_line[(unit_page, line)]
                        if len(here) == 1:
                            slug, ch, v = next(iter(here))
                            p = (slug, ch, [v] if v else [], head)
                    if not p:
                        unparsed_notes.append((unit_page, line, head))
                        continue
                    cites = [p]
                elif kind == "bare":
                    # a second chapter of the book just named in this entry
                    bm = _BARE_CH.match(_clean_head(head))
                    if not last_book:
                        unparsed_notes.append((unit_page, line, head))
                        continue
                    ch = roman_to_int(bm.group("roman"))
                    verses = [int(v) for v in re.split(r"[,.\s]+", bm.group("verses"))
                              if v.strip()]
                    cites = [(last_book, ch, verses, head)]
                else:
                    cites = parse_citations(_clean_head(head))
                    if not cites:
                        unparsed_notes.append((unit_page, line, head))
                        continue
                for slug, ch, verses, printed in cites:
                    last_book = slug
                    t = triple(slug, ch, verses)
                    rec = {
                        "book": slug, "chapter": ch, "verses": verses,
                        "printed": printed, "page": unit_page, "line": line,
                        "situation": situation,
                    }
                    if NUMBERING.search(situation):
                        rec["numbering"] = True
                    if PLATE_FIGURE.search(situation):
                        rec["plateFigure"] = True
                    if t in by_unit_line[(unit_page, line)]:
                        # the plate marked it; the note says what it is doing
                        situations[(unit_page, line, t)] = rec
                    elif t in by_unit[unit_page]:
                        # ⚠ Marked on this OPENING but not on this line. The
                        # `S:` band anchors to the English line and ref_index
                        # to the Latin one, and they can sit a line apart
                        # (printed 238's note is at 18, the plate's
                        # `Luc. vii. 38` at 19). Calling this an
                        # identification would enter the same verse twice,
                        # once as each kind — so it is a mark, and the offset
                        # is REPORTED rather than smoothed away.
                        offset_matches.append((unit_page, line, printed))
                        situations[(unit_page, line, t)] = rec
                    else:
                        rec["source"] = "identified"
                        identified.append(rec)

    # --- the explanatory band ---------------------------------------------
    # ⚠⚠ §37 (printed 374--379) IS ONLY REACHABLE HERE. Those six leaves carry
    # no plate reference and no `S:` entry at all — printed 374's own note says
    # "The scripture band is empty from here to the end of §37 ... because the
    # plate cites nothing" — and the identifications were written into the
    # EXPLANATORY band instead ("Romans vii. 18 stands here word for word and
    # unmarked"). An index that reads only `S:` joins none of §37, which is the
    # very failure WEB-PLAN §9 names.
    for unit_page, bands in sorted(notes.items()):
        for entry in bands.get("R", []):
            m = re.match(r"^(\d+)(?:\s*[–-]\s*\d+)?\s+(.*)$", entry, re.S)
            line = int(m.group(1)) if m else None
            prose = m.group(2) if m else entry
            for slug, ch, verses, printed in prose_citations(prose):
                t = triple(slug, ch, verses)
                if line is not None and t in by_unit_line[(unit_page, line)]:
                    continue          # the plate marks it; `S:` already has it
                if t in by_unit[unit_page]:
                    continue          # marked elsewhere in the opening
                if any(r["book"] == slug and r["chapter"] == ch
                       and r["verses"][:1] == verses[:1]
                       and r["page"] == unit_page for r in identified):
                    continue          # already identified from the `S:` band
                rec = {
                    "book": slug, "chapter": ch, "verses": verses,
                    "printed": printed, "page": unit_page,
                    "line": line if line is not None else 0,
                    "situation": prose.strip(), "source": "identified",
                    "band": "R",
                }
                if NUMBERING.search(prose):
                    rec["numbering"] = True
                if PLATE_FIGURE.search(prose):
                    rec["plateFigure"] = True
                identified.append(rec)

    # marry each marked reference to its note, where the notes pass wrote one
    for rec in marked:
        unit = unit_of.get(rec["page"], rec["page"])
        t = triple(rec["book"], rec["chapter"], rec["verses"])
        note = situations.get((unit, rec["line"], t))
        if note:
            rec["situation"] = note["situation"]
            for k in ("numbering", "plateFigure"):
                if k in note:
                    rec[k] = note[k]

    entries = defaultdict(list)
    for rec in marked + identified:
        entries[rec["book"]].append(rec)
    for slug in entries:
        entries[slug].sort(key=lambda r: (r["chapter"] or 0,
                                          r["verses"][0] if r["verses"] else 0,
                                          r["page"], r["line"]))

    books = []
    for slug in BOOK_ORDER:
        rows = entries.get(slug)
        if not rows:
            continue
        name, chapters, testament = BOOKS[slug]
        books.append({
            "slug": slug, "name": name, "testament": testament,
            "marked": sum(1 for r in rows if r["source"] == "marked"),
            "identified": sum(1 for r in rows if r["source"] == "identified"),
            "total": len(rows),
        })

    # --- the checks, reported and never silently applied -------------------
    out_of_range = [
        r for rows in entries.values() for r in rows
        if r["chapter"] and r["chapter"] > BOOKS[r["book"]][1]
    ]
    report = {
        "marked": len(marked),
        "identified": len(identified),
        "unparsed_plate": unparsed_plate,
        "unparsed_notes": unparsed_notes,
        "empty_entries": empty_entries,
        "out_of_range": out_of_range,
        "offset_matches": offset_matches,
        "unknown_books": sorted({
            r[2] for r in unparsed_plate} | {r[2] for r in unparsed_notes}),
    }
    return books, dict(entries), report
