#!/usr/bin/env python3.11
"""Find scripture references the index CANNOT SEE, and the tags they never got.

The failure this exists to catch has now happened six times, and it is silent in
every direction: `ref_index.BOOK` is a fixed alternation of book abbreviations, so
a form the 1853 uses but the list omits does not produce an error — the reference
simply never enters the index, `--stub` never offers it, `note_sheet` never prints
it, `check_notes` never misses it, and the finished page shows a foot-band that
looks complete. Printed 290 offered three of the Spirit's four titles that way.
Printed 324 lost the fourteenth and last term of the confession the same way.

Two passes:

  1. **the sweep** — every italicised token followed by a roman numeral, tested
     against the current BOOK list. Anything unmatched is either a missing book or
     a false positive (`*Servitus.*`, `*sec.* LXX`), and a human decides which.
  2. **the backfill audit** (`--tags`) — for the forms named in RECOVERED below,
     every occurrence on a page whose notes are already written, checked against
     the band that page carries. Reports the references a completed page never had
     the chance to tag.

⚠ Part I is keyed by the OPENING, not the leaf: the references print on the Latin
recto (odd) and the band goes under the English recto of the same opening, filed
in `print-notes.md` under the Greek verso's even number. An audit that looks up an
odd page directly finds an empty band and reports every reference on every Latin
recto in the volume as missing. Parts II–III are keyed by the leaf itself.

Usage:
    python3.11 tools/audit_missing_books.py            # the sweep
    python3.11 tools/audit_missing_books.py --tags     # the backfill audit
    python3.11 tools/audit_missing_books.py --tags --through 323
"""
import argparse
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref_index import BOOK  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The nineteen forms recovered 2026-08-10, and the tag spellings each may wear in
# the band. A tag cites the book in the edition's own English, so `*Joan.*` is
# looked for as John, `*Syr.*` as Ecclus/Sir, `*Paralip.*` as Chronicles.
RECOVERED = {
    'Joan': ['John', 'Joh'], 'Thren': ['Lam'], 'Ezech': ['Ezek'], 'Mich': ['Mic'],
    'Es': ['Isa', 'Is'], 'Syr': ['Ecclus', 'Sir'], 'Isa': ['Isa', 'Is'],
    'Chron': ['Chr'], 'Ez': ['Ezek'], 'Abac': ['Hab'], 'Ezr': ['Ezra'],
    'Josh': ['Josh'], 'Zech': ['Zech'], 'Amos': ['Amos', 'Am'], 'Nehem': ['Neh'],
    'Eccles': ['Eccl'], 'Paralip': ['Chr'], 'Paral': ['Chr'], 'Judic': ['Judg'],
}

PAGE_MARK = re.compile(r'<!-- printed (\d+)')
TOKEN = re.compile(r'\*([A-Za-z][A-Za-z]*)\.?\*\s*\[?([ivxlcIVXLC]+)\.')
KNOWN = re.compile(r'^(?:%s)$' % BOOK, re.I)


def transcript_lines():
    """Yield (page, line) for every transcript line, flags sections excluded.

    The `## Translator's flags` prose discusses references in our own words and in
    modern form (`Heb 3:13`), so including it would report our commentary as if it
    were the plate."""
    for path in sorted(glob.glob(os.path.join(ROOT, 'part*', '*transcript.md'))):
        text = open(path).read().split("## Translator's flags")[0]
        page = None
        for line in text.splitlines():
            mark = PAGE_MARK.search(line)
            if mark:
                page = int(mark.group(1))
                continue
            if page:
                yield page, line, os.path.relpath(path, ROOT)


def sweep():
    seen = collections.Counter()
    where = collections.defaultdict(set)
    for page, line, path in transcript_lines():
        for m in TOKEN.finditer(line):
            token = m.group(1)
            if not KNOWN.match(token):
                seen[token] += 1
                where[token].add(path)
    if not seen:
        print('No unrecognised book forms. Every italicised reference is indexed.')
        return 0
    print(f'{len(seen)} unrecognised forms, {sum(seen.values())} occurrences.')
    print('⚠ Decide each: a missing book goes into ref_index.BOOK (long form BEFORE')
    print('  its short form); a false positive stays out and is named in the comment.\n')
    for token, count in seen.most_common():
        print(f'  *{token}.*  x{count:<4} {", ".join(sorted(where[token])[:3])}')
    return 1


def band_by_page():
    """The written notes, keyed by the page heading they stand under."""
    notes = collections.defaultdict(list)
    current = None
    for line in open(os.path.join(ROOT, 'apparatus', 'print-notes.md')):
        heading = re.match(r'##\s+(\d+)\s*$', line.strip())
        if heading:
            current = int(heading.group(1))
            continue
        if current and line.startswith(('S:', 'R:')):
            notes[current].append(line.strip())
    return notes


def band_page(page):
    """Which heading a reference on this printed page files under."""
    return page - 1 if (page <= 263 and page % 2 == 1) else page


def audit_tags(through):
    pattern = re.compile(
        r'\*(%s)\.?\*\s*\[?([ivxlc]+)\.\s*([\d,\s]*)' % '|'.join(RECOVERED), re.I)
    notes = band_by_page()
    total = 0
    missing = []
    for page, line, _ in transcript_lines():
        if page > through:
            continue
        for m in pattern.finditer(line):
            total += 1
            book, chapter, verses = m.group(1), m.group(2), m.group(3).strip()
            band = band_page(page)
            blob = ' '.join(notes[band]) + ' ' + ' '.join(notes.get(page, []))
            tagged = any(re.search(r'\b%s\w*\.?\s*%s\.' % (alt, chapter), blob, re.I)
                         for alt in RECOVERED[book])
            if not tagged:
                missing.append((page, band, book, chapter, verses,
                                line.strip()[:55], len(notes[band])))
    print(f'{len(missing)} of {total} recovered references are untagged '
          f'on pages through {through}.')
    print('⚠ Untagged is not the same as wrong: §3 forbids tagging what the line')
    print('  above already gives, and §8 requires SELECTION on a dense page. Read')
    print('  the page before writing.\n')
    for page, band, book, chapter, verses, context, count in sorted(missing):
        loc = f'p{page}' + (f' → band {band}' if band != page else '')
        print(f'  {loc:<16} *{book}.* {chapter}. {verses:<8} '
              f'({count} notes) | {context}')
    return 1 if missing else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tags', action='store_true',
                    help='audit the recovered forms against the written bands')
    ap.add_argument('--through', type=int, default=323,
                    help='last printed page whose notes are written (default 323)')
    args = ap.parse_args()
    sys.exit(audit_tags(args.through) if args.tags else sweep())


if __name__ == '__main__':
    main()
