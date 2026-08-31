# The digital edition — plan of record

**Written 2026-08-31, after the print book was submitted to KDP.** This is the execution
document for `andrewes.wrootpress.com`: a Greek · Latin · English reader with the Hebrew
where the plate sets it, the whole apparatus, and the scripture index.

> **▶ This file is written to be executed by a later, cheaper session.** The judgment is
> already spent. Read §0 and §4 before touching anything; §15 is the trap list and it is
> not optional.

---

## 0. The ruling that unblocked this, and the one that constrains it

**`EDITION-SHAPE.md` has carried a standing prohibition since 2026-08-04:** *"The web
reader is NOT Andrewes work… Do not build the Andrewes site reader; wait and port."* The
language-array generalisation was deliberately scheduled as **Milton M2** so it would be
done once, on the easier text — two languages, clean prose, no polytonic Greek, no
four-script pages.

✅ **M2 IS DONE AND LIVE.** `~/milton-doctrina/site/src/lib/content.ts` defines an
N-language array (`LangKey = string`, `texts: LangText[]`) with a comment stating in as
many words that it exists so this ports "to a 3-language (Greek/Latin/English) reader for
Andrewes without re-architecting," and
`src/app/browse/[book]/[chapter]/text-reader.tsx` generates its view modes from
`texts.length` rather than a hardcoded pair. Milton is deployed at
`milton.wrootpress.com`. **The prohibition is satisfied. This work is now sanctioned.**

⛔⛔ **THE CONSTRAINT THAT REPLACES IT: THE PRINT BOOK IS SUBMITTED AND FINAL.** Interior
625pp, and `covers/cover.py` hangs the whole wrap on two unvalidated constants,
`PAGES = 625` and `PPI = 0.0025`. **Any change to `tools/proof2tex.py` or
`tools/transcript2tex.py` that alters TeX output re-flows the volume and silently
invalidates the printed cover.** The web build is therefore **ADDITIVE ONLY** — new files
in `tools/` and `site/`, importing from the print tools, never editing them. If a shared
helper genuinely must be touched, rebuild `prototypes/volume-loeb.tex`, confirm **625
pages / 0 units too tall / 0 `Missing character`**, and say so in the commit.

---

## 1. Wilson's rulings, 2026-08-31

1. **The English goes up FULL AND FREE.** Precedent: `milton.wrootpress.com`,
   `migne.app`. This makes the site **the one published home of the Wroot Press English**
   under `reference_one-translation-one-home` — `wrootpress.com` links to it and never
   re-hosts a line of it. The book still sells as the physical Loeb object and as the
   carrier of the introduction.
2. **The introduction and preface stay with the book.** They are authored argument, not
   edited text. The site gets a short `/about` written for the site, which may draw on
   the introduction's material but is not the introduction.
3. **Scholarly reader first.** Home page is the volume's own structure plus the scripture
   index in top nav from day one — Milton's shape. Part I's seven days are simply Part
   I's sections; there is no `/today` route in v1. (A devotional door stays possible
   later and costs nothing now: the reader component is the same.)

**Assumed unless Wilson says otherwise:** domain **`andrewes.wrootpress.com`**, house
pattern (`milton.`, `glossa.`), DNS-only record at Cloudflare pointed at Vercel per
`reference_domains-cloudflare`. Vercel project on the **Labs** team
(`team_sERwO8GidBZdsL7F1I6fcgAW`), same as Milton — **not** the Covenant team.

---

## 2. What the site is, and what it is not

**It is** the 1853 Parker plate — Greek, Latin, and the Hebrew where the plate sets it —
beside the Wroot Press English, line for line, with 1,678 apparatus entries and 2,267
scripture references already keyed to page and sense-line.

**It is not** a facsimile, and it is not the printed book in a browser. The Loeb leaf,
the two foot-bands, the margin line-ruler and the 1853 shoulder-note are *print*
solutions to a print problem — a leaf that must hold a fixed amount. The web has no leaf.
Anything ported for the sake of resemblance rather than use should be cut.

**The three things the book cannot do and the site can** — §10 — are the actual argument
for building it. If the site ends up being the book with worse typography, it failed.

---

## 3. Stack and layout

Fork `~/milton-doctrina/site/` into **`~/andrewes-preces/site/`** — same repo as the
text, same as Milton, so content and reader move together.

- Next.js 16 + React 19, **`output: "export"`** (static). No server, no database.
- `pnpm`; build is `node scripts/build-content.mjs && next build` in Milton — **here the
  content step is Python** (§4), so `package.json`'s build becomes
  `python3.11 ../tools/build_web_json.py && next build`.
- Deploy: `npx vercel --prod` **from `site/`, never from the repo root**
  (`feedback_vercel-deploy-from-subdirectory` — a root deploy 404s the whole site while
  reporting Ready).
- `site/src/data/*.json` is generated. Commit it anyway: the build must not require a
  working Python to produce a preview, and a committed artifact diffs reviewably.

---

## 4. ⚠⚠ THE ARCHITECTURAL DECISION: the web build reuses the PYTHON parser

**Do not re-parse the transcripts in JavaScript.** Milton's `scripts/build-content.mjs`
is the wrong template and copying it is the single most expensive mistake available here.

**Why it does not transfer.** Milton's source is prose chunks with language sections
discovered from `## la` / `## en-sumner` headers, paragraphs separated by blank lines.
Andrewes' source is nothing like it:

- **page-keyed**, by `<!-- printed NNN (PDF nn) — Greek -->` markers, not chapter-keyed;
- **line-faithful** — every line of the transcript is a printed line, and the line is the
  edition's coordinate;
- **indentation is semantic** — 4 spaces per level, as printed; it is the shape of the
  prayer, not decoration;
- **runs of 2+ spaces are measured horizontal space** — Part III's left margin reference
  column, the ` | ` multi-column rows, the brace gutters;
- `{ a / b }` brace catalogues, `[?]` unreadable marks, the editor's `[ ]` supplied
  references, and the 1853's own lettered footnote apparatus at printed 279 (`ᵃᵇᶜᵈ`, four
  raised romans standing *before* the word each marks).

The repo already made this decision once, for exactly this reason:
`transcript2tex.py`'s own docstring — *"Parsing and rendering are imported from proof2tex
so the two builders cannot drift."* **A JS reimplementation would be a third parser, and
the drift would be invisible: both outputs look fine on their own page.**

### 4.1 What to write

**`tools/build_web_json.py`** — new file, imports from `proof2tex`:

```python
from proof2tex import (COMMENT, GAP, GREEK_CH, HEBREW, LATIN_CH, SUPERS,
                       parse_pages, sections_for, PART_TITLES, PART1_LABELS)
```

`parse_pages()` and `sections_for()` are reused **unchanged** — they already handle the
two things that have burned this project: a page marked twice in one file (continue the
block, never restart it) and the trailing `## Translator's flags` apparatus prose that
must never flow into the last printed page.

What is new is the **line serializer**. `proof2tex.render_line` emits TeX; the web needs
structure. Write a *sibling*, not a refactor (§0):

```
web_line(raw) -> None | {"indent": int, "spans": [...], "gaps": [...]}
```

using the same `COMMENT` / `GAP` / `SUPERS` regexes so the two cannot disagree about what
a line is. Span kinds: `text`, `greek`, `hebrew` (RTL), `ref` (a scripture reference as
printed), `sup` (the 279 apparatus letters), `unclear` (`[?]`), `supplied` (editor's
brackets).

### 4.2 ⚠ Sense-line numbering — copy the rules, do not re-derive them

The line number is the whole citation scheme and it has been got wrong twice. Take these
from `tools/ref_index.py:index()` verbatim:

- **A comment-only line is not a sense-line.** `render_line` drops them, so they take no
  place on the page and none on the ruler. Counting them put the index one ahead per
  inline comment — printed 115's *Cruce* indexed as line 11 instead of 9 — **on 58
  pages**, and every tag took its figure from that count.
- **Blank lines are not sense-lines.**
- **The count runs CONTINUOUSLY across a page marked twice.** 49 pages are marked in more
  than one section file. Restarting the count at each marker put printed 299 eighteen
  lines adrift, *pointing at real lines*, so nothing looked wrong.
- The count is per printed page, 1..N, and must **agree exactly with `ref_index.py`**.
  ✅ **Gate: `build_web_json.py --check-lines` compares its own per-page line counts
  against `ref_index.index()` and fails the build on any disagreement.** This is cheap
  and it is the only thing standing between the site and 1,678 misplaced notes.

---

## 5. The JSON shape

```
site/src/data/content.json     — sections, in reading order
site/src/data/scripture.json   — the index, by book
site/src/data/apparatus.json   — the 1,678 entries, by page+line
```

A **section** (60 of them: 11 + 43 + 6) is the reading unit and the URL:

```jsonc
{
  "id": "part1/day1",
  "part": 1,
  "label": "The First Day",
  "titles": { "grc": "ΤΗΣ ΠΡΩΤΗΣ ΗΜΕΡΑΣ", "la": "DIEI PRIMÆ", "en": "Of the First Day" },
  "pages": [
    { "n": 30, "layers": { "grc": [ /* lines */ ], "en": [ /* lines */ ] } },
    { "n": 31, "layers": { "la":  [ /* lines */ ] } }
  ]
}
```

**⚠ The language array is keyed by layer, and a page does not carry all three.** This is
the fact that will break a naive reader:

| | Greek | Latin | English |
|---|---|---|---|
| Part I (263 pp) | 131 pages, **even** | 132 pages, **odd** | 132, keyed to the **Greek** page |
| Part II (129 pp) | 9 pages (§42–43 hymns) | 122 pages | 125 |
| Part III (39 pp) | 3 pages | 39 pages | 39 |

In Part I the Greek verso and the Latin recto are **two printed pages of one opening**:
`gr(n)` + `la(n+1)` + `en(n)`, n even. `transcript2tex.build_loeb()` has the exact
predicate — reuse its logic:

```
part == 1 and layer == "gr" and n % 2 == 0 and pages[n+1].layer == "la"
```

**§42 and §43 in Part II revert to the same paired pattern** (printed 388–397, the
morning and evening hymns). That is why printed 389/391/393/395 have no English file
block — they are Latin rectos, and their English is filed under the Greek page they face.
**English coverage is complete. There are no gaps. Do not "fill" these four.**

**The columns align by SENSE-LINE, not by page.** Verified at printed 34/35 and recorded
in `ref_index.py`'s docstring: the Latin is line-for-line with the Greek and the English
is line-keyed to the Greek, so **line N is the same line in all three**. That is what
makes a three-column parallel view honest rather than approximate.

---

## 6. Coordinates and permalinks

**The citation scheme is the printed page and the sense-line — the 1853's own, and the
print edition's own.** `38. 3` in the apparatus means printed page 38, line 3. Keep it:

```
/read/part1/day1                 a section
/read/part1/day1#p38             a printed page
/read/part1/day1#p38.3           a sense-line  ← every note anchors here
```

**Print and web then cite identically**, which is worth more than any convenience of a
prettier URL. Every line carries an `id`; hovering reveals a link. The printed-page
marker toggle (`off` / `margin` / `inline`) already exists in Milton's `text-reader.tsx`
with `localStorage` persistence — port it and default to `margin`.

⚠ **Line figures print every five in the book because a leaf has a margin.** On the web,
print a figure on every line that carries a note (Milton's `\setnoted` logic, generalised)
— *"a note on line 27 is unfindable if the margin only prints 25 and 30."*

---

## 7. The reader

Port `text-reader.tsx` and generalise it from 2 columns to N. It already builds its modes
from the array; what it has never had to do is lay out three.

- **Modes:** `Parallel` · `Greek` · `Latin` · `English`. Generated, never hardcoded.
- **Parallel on desktop:** three columns. Where a page has no Greek (most of Parts II–III)
  the mode collapses to two — *per page*, not per section, because §42 changes mid-part.
- **Parallel on a phone is a lie** and should not be attempted. Under ~900px, fall back to
  a two-language interleave (originals + English) with a language picker for which
  original. State this in the component; do not let a later session "fix" it with a
  horizontal scroll.
- **Indentation renders as `padding-left`, one level per 4 source spaces.** The measured
  gaps (§4.1) render as inline `<span>` width in `ch`, not as `&nbsp;` runs.
- **Part III's margin reference column** needs its own treatment — it is a left-hand
  column of references in the source's horizontal positions, and flowing it inline
  destroys the page. Set it as a real gutter column.

---

## 8. The apparatus on the web

**1,678 entries already written**, in `apparatus/print-notes.md`, keyed `## <page>` then
`S:` / `R:` / `V:` with a leading line figure. `transcript2tex.load_notes()` parses it —
reuse it.

| band | count | print home | web home |
|---|---|---|---|
| `S:` scripture situation | **1,285** | recto foot | anchored note on the English line; the site's best feature |
| `R:` explanatory | **383** | recto foot | same |
| `V:` apparatus criticus | **10** | verso foot | on the originals column, sigla intact |

The two-band split exists because a leaf has two feet. **The web should keep the
*distinction* and drop the *geometry*:** a marker on the line, opening a note in the
margin on wide screens and inline on narrow. Keep the roman-numeral markers — Wilson's
point that two arabic series in one alphabet would confuse still holds when the line
figures are on screen.

**Also publishable, and cheap** — the `apparatus/` files are already prose:
`CLASS-A-ledger.md` (the Wright apograph), `CLASS-B-unit-boundaries.md`,
`BRIGHTMAN-collation.md`, `variae-lectiones-transcript.md`, `notae-marginales-transcript.md`.
These become `/apparatus/*` reference pages. **The Hebrew that the 1853 dropped from
Andrewes' own text lives in Class A** — printed 38 · 76 · 86–88 · 92 · 96 · 152 · 192 ·
198 · 200 · 202 · 210 · 212, including the rabbinic `יצר טוב` at 76 and a seven-word
Greek–Hebrew lexicon of sin at 96. Publishing Class A is how the site carries Hebrew the
printed plate does not.

⚠ **Nothing in a band may be phrased as a repair.** The plate stands as printed; an
apparatus entry records another witness. `NOTES-CONVENTIONS.md` governs — the site does
not get to relax it.

---

## 9. The scripture index — the product, not the apparatus

**2,267 references on 253 printed pages**, median 8 per page, max 30, already extracted by
`tools/ref_index.py` with page and sense-line. Port Milton's `/scripture` +
`/scripture/[book]` (which Milton in turn ported from Bonaventure) and put **Scripture in
the top-level nav from day one**.

The query it unlocks: *what does Andrewes actually do with Psalm 51 — where, in which of
the seven days, in which language, and does the English follow the Vulgate or the Hebrew
there?* There is no free instrument that answers it.

⚠⚠ **The index built from the plate's marks UNDER-REPORTS, and the notes pass proved it.**
`§37 (printed 374–379) is six unmarked leaves`: the plate cites nothing on any of them and
the confession is built of allusion it never references. Printed 335's brace fastens
*ariditas* to Is. xxiv. 16 and the *fountain of tears* to Jer. ix. 1, and **both return
unreferenced at 376 and 378**. The `S:` notes identified allusions the plate never marked
— so `scripture.json` must merge **two sources**: `ref_index` (marked) and the `S:` band
(identified), tagged distinctly. An index that joins only the marks joins none of §37.

⚠ **The psalm-numbering trap is live here.** The volume is not on one Psalter — plain AV
(300), plain Vulgate (274), BCP (433, 356), and a **hybrid** at 344 and 353 (the Vulgate's
verse-figure under the Hebrew psalm-number). A `/scripture/psalms` page that silently
picks one numbering will be wrong on real pages. Carry the numbering as printed and state
which it is.

⚠ **Reading a digit correctly is not reading it rightly** (Bonaventure lesson, restated in
Milton's PLAN): verify a reference's *target exists*, not merely that the numerals were
transcribed. And the plate's known-wrong references are **kept as printed and flagged**:
`[Jer. l. 24.]` is a roman **fifty** and is not to be "corrected"; likewise `[Eph. i. 8.]`
(wants i. 18), `[Dan. vi. 4.]` (wants vi. 10), `[Psal. cxix. 114.]`.

---

## 10. The three things the site can do that the book cannot

**These are the argument for building it.**

1. ⭐ **The two recensions, side by side.** Part III is the **Harley recension** of Part
   II's penitential matter — §1↔§23+§38, §2↔§17, §4↔§24. The codex order forces them 100
   pages apart and the print edition rightly keeps them there. A `/synopsis` view sets
   them in adjacent columns. ⚠ **Never conform two recensions**: identical Latin gets
   identical English, divergences stand and are shown as divergences. This is the single
   best reason for the site to exist.
2. ⭐ **The plate itself, one URL away.** `SOURCE-IMAGES.md`: the University of Toronto
   1853 (`archive.org/details/precesprivataequ00andruoft`) is free, greyscale, and its
   page images are fetchable directly (`reference_archive-org-page-images`). A "show the
   plate" toggle per printed page turns every editorial decision into something a reader
   can check. ⚠⚠ **The leaf offset runs +18 → +42 and Toronto has duplicate leaves —
   verify every leaf by eye and NEVER port `STRUCTURE.md`'s offsets.** Build a checked
   `page → leaf` table once, commit it, and treat an unverified entry as absent.
3. ⭐ **The volume as its own concordance.** The one-verse-three-dresses habit — Hosea at
   361, Dan. ix. 16 at 363, *Magis deceret* at 345 / 366 / 384 — is invisible in a codex
   and trivial on a page that lists every occurrence.

A fourth, nearly free: **`Divisio` (printed 347–348) is the book explaining its own
shape**, and most of its terms are this volume's actual section headings. It is *a table
of contents for a book that never prints one.* Render it as a live one.

---

## 11. Typography, scripts, and RTL

- **Cardo** via `next/font/google` for `grc` and `he` — it is what the print uses and it
  covers polytonic Greek and pointed Hebrew. Keep **EB Garamond / Cinzel** from Milton for
  `la`, `en` and chrome so the two sites read as one house.
- **Hebrew is RTL and appears inline inside LTR lines** (printed 42, 274, 383, 386, plus
  the apparatus). `dir="rtl"` on the span, `unicode-bidi: isolate`. The print build needs
  `\RL{}` for exactly this; the web equivalent is the isolate, and getting it wrong
  reverses a word silently.
- ⚠ **A character with no glyph has no width, so it passes every check.** This cost the
  print book a real defect at printed 414. The web analogue is tofu, or worse, an invisible
  fallback. **Add a build check that every codepoint in the JSON is covered by the declared
  subset**, and do not trust a visual pass to find it.
- The `ᵃᵇᶜᵈ` at printed 279 are Unicode modifier letters in the source and are mapped at
  render time in `proof2tex.SUPERS` — **do the same on the web; never write back to a
  transcript** (`NOTES-CONVENTIONS §7.2`).

---

## 12. Search

Port Milton's `search-client.tsx` (client-side, over the JSON — no server).

⚠ **Three scripts means three normalisations.** Polytonic Greek must be **accent- and
breathing-folded** or a reader who types `αγαπη` finds nothing; Latin needs `æ/ae`,
`œ/oe`, `v/u`, `j/i` folding against the 1853's orthography; Hebrew needs
vowel-point-stripping. Fold at *build* time into a parallel search field — never at query
time, and never lossily over the display text.

---

## 13. Rights

`wroot-press-licensing`: **CC BY-NC 4.0 on the English and the encoding; the 1853 source is
public domain.** Port Milton's `/rights` page and say exactly that — and say what the
encoding is, since here it is substantial (the line-faithful transcription, the sense-line
numbering, the apparatus, the index).

**`reference_one-translation-one-home` applies from the first deploy:** once this is live,
it is the ONE address of the Wroot Press English. `wrootpress.com` links here. Nothing
re-hosts a line of it. ⚠ Verify the URL resolves with `curl` before writing it into any
other site — a guessed URL is a broken promise on a public page.

---

## 14. Open for Wilson

1. **The Latin question is still unruled — and the site makes it sharper than print did.**
   `andrewes-latin-question` / `apparatus/THE-LATIN-QUESTION.md`: the 1853's *Variæ
   Lectiones* says the Wright apograph carries Greek only *usque ad pag. 250*, "sine
   versione Latina, **quam Editor ipse confecisse videtur**." If the Latin of printed
   1–250 is a 1675 editor's, then a column header reading plainly **"Latin"** makes a
   claim on every screen, on every one of Part I's 132 Latin pages. Print answered this in
   an introduction the site will not carry. **Minimum: the column header links to a
   `/latin` page stating the question.** ⚠ **The decisive test is nearly free and is still
   unrun** — for each Class A Greek divergence in pp. 1–250, check which reading the facing
   Latin supports. It is the same JSON this build produces.
2. **Domain** — `andrewes.wrootpress.com` assumed (§1). Say if not.
3. **Book A / Book B** (`EDITION-SHAPE.md`) remains unruled and **still does not block
   anything.** The site is built from the transcripts, which are invariant under every
   option in that memo.

---

## 15. ⚠⚠ Traps carried over from the print build

Every one of these was paid for once. None is hypothetical.

1. ⛔ **Do not re-flow the print volume.** §0. The cover's `PAGES = 625` is validated by
   nothing.
2. **Do not write back to a transcript.** Ever, from any web work. `part1/`–`part3/` are
   the record of the plate; restoring anything is a separate, Wilson-level act.
3. **Tool blindness is this project's recurring failure class — twelve recorded
   instances.** A tool quietly reports less, and every downstream check agrees with it.
   *A checker's first output is not evidence, including a checker written an hour ago.*
   Run the existing pre-flight before trusting any derived count:
   ```
   python3.11 tools/audit_missing_books.py
   python3.11 tools/ref_index.py --continuations
   python3.11 tools/ref_index.py --turned
   ```
4. **A widened pattern must be DIFFED item by item against the old one — its count proves
   nothing.** Removing one gate added 245 duplicates and left five ghost books, and the
   tally moved the right way throughout.
5. **`Ibid. N` ≠ `Ibid.`** Bare `Ibid.` repeats the antecedent; `Ibid. N` means the same
   chapter at verse N. 227 continuations exist and none was visible until 2026-08-10.
6. **Wrong references and printing defects are kept as printed and flagged, never silently
   mended** — on the web as in print. §9 lists the running ones.
7. **The 1853 capital upsilon is drawn with flat arms and reads as `Τ`.** Handled in the
   transcripts already; relevant only if anything new is read off a plate.
8. **A defect "confirmed against the OCR" is not confirmed** — `_djvu.txt` is generated
   from the same scan. Only a *different* scan settles plate-vs-camera. This was paid for
   three times (printed 239, 210, 353) and **on all three the plate was innocent.**
9. **Read one page past the apparent end before closing a section.** Twice-burned.

---

## 16. Milestones

Sized so each ends with something deployable, and so the judgment-dense work is separated
from the volume work (`reference_model-prudence-rubric`).

| | Milestone | Deliverable | Model |
|---|---|---|---|
| **W1** | Content pipeline | `tools/build_web_json.py`, the three JSON files, `--check-lines` green against `ref_index` | Sonnet — spec is §4/§5 |
| **W2** | Reader | Fork of Milton's site; 3-column parallel; page markers; line anchors; Cardo + RTL | Sonnet, with an Opus pass on the parallel-view CSS |
| **W3** | Apparatus | 1,678 entries anchored and rendering; `/apparatus/*` reference pages | Sonnet |
| **W4** | Scripture index | `/scripture` + `/scripture/[book]`, marked **and** identified references merged (§9) | Opus — the merge and the psalm-numbering are judgment |
| **W5** | Site-only wins | `/synopsis` recension view; verified `page → leaf` table + plate toggle | Opus for the synopsis, Sonnet for the leaf table |
| **W6** | Search, rights, deploy | Folded search fields; `/rights`; `/about`; Cloudflare DNS; `npx vercel --prod` **from `site/`** | Sonnet; ⛔ **the deploy itself is a protected action — surface the command and wait** |

**Ship after W2.** A three-column reader with the whole text and nothing else is already
the only place this book exists online. W3–W6 land on a live site.
