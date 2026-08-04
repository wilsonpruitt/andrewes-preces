# M3 handoff — Part I volume run (transcribe + translate Days 2–7 and the rest of Part I)

**Read this file, `CONVENTIONS.md`, and `STRUCTURE.md` before touching anything. Follow them exactly; do not re-derive conventions.** Day 1 (`part1/day1-transcript.md` + `part1/day1-english.md`) is the worked example — match its format precisely.

## Scope, in order

**PART I IS COMPLETE — both layers AND English (printed 1–263).** The Scope list below is the historical Part I plan, kept for reference; all of it is done. The live front is Part II — see the next subsection.

1. ~~**Days 2–7** (the core): printed pp. 70–~220.~~ Done.
2. ~~Officium Vespertinum + evening prayers, the two Meditations, and the FRONT of Part I.~~ Done.
3. Variae Lectiones entries for covered pages come LAST, as a separate pass (still outstanding, Part I + II together).

### Part II — the live front (printed 264→)

Read `next-session-resume.md` for the exact verified entry point. In brief:
- **Text opens at printed 267 = PDF 288** (*Duo in me cognosco, Domine*), offset **+21** (VERIFIED by eye); printed 264–266 = the PARS SECUNDA divisional title + blanks (title scanned twice, PDF 284/286).
- **Part II opens LATIN-ONLY** — single column, no facing Greek. So **translate the Latin** (CONVENTIONS §6), and the Part-I Greek-verso/Latin-recto even/odd rule does NOT apply. Check every page for which layer(s) it carries; later stretches may return to parallel. Heavy nested `{ }` brace catalogues throughout.
- **Files:** new `part2/` dir, `part2/NN-<slug>-transcript.md` + `-english.md`, first = `part2/01-duo-in-me-cognosco-transcript.md`. Segment sections at the 1853 typographic breaks (large blank + caps incipit).
- **Offset keeps drifting** (+21 → +23 by printed 297 → +37 by the poems at 393). Re-verify the printed number by eye every batch; record new anchors in STRUCTURE.md.
- Known Part II shape (STRUCTURE.md §PARS SECUNDA): penitential/eucharistic material, a Latin-only Praefatio (pp. 372–387, from Stokes' *Verus Christianus* 1668), ending with the hymns + *In Christum Crucifixum Monostrophica* poems (printed 393 ff.) and a Greek counterpart.

## Per-day recipe (one day per session; commit per day)

1. Extract page images: `pdftoppm -jpeg -r 200 -f <pdffirst> -l <pdflast> raw/preces1853.pdf raw/dayN/p`. PDF page = printed + 20 **from printed 44 onward** (18 before) — but the scan HAS DUPLICATE LEAVES (42/43 twice already found), so **verify the printed page number in the header of the first and last image before transcribing, and at every anomaly**. Record any new offset shifts in STRUCTURE.md's anchor table.
2. Transcribe one spread (2 leaves) per pass into `part1/dayN-transcript.md`, page-marker format exactly as Day 1 (`<!-- printed N (PDF M) — Greek|Latin -->`). Verbatim 1853; `[?]` unreadable; `<!-- print unclear: x/y -->` for ambiguous glyphs; braces/columns/Hebrew per CONVENTIONS §2–4. NEVER infer Greek from context — transcribe what is printed.
3. Translate into `part1/dayN-english.md`, line-keyed to the GREEK, register per CONVENTIONS §8–10 (thou-form AV/BCP; echo AV wording only where Andrewes' Greek matches it). End the file with a `## Translator's flags` section like Day 1's.
4. Self-check before commit: (a) page-marker sets identical between transcript Greek pages and English blocks; (b) line counts per page within ±2 between Greek and English; (c) every `*Ref.*` italic ref sits on the Latin layer only; (d) grep the transcript for `[?]` and unclear-comments — carry them into the flags list.
5. Two commits per session max: content, then any STRUCTURE.md/notes updates. **No push — protected.** (The remote `origin` already exists; see CLAUDE.md.)

## Print layout (already decided — affects nothing in M3 except discipline)

Wilson chose **the 1675 mirror** (prototype B). Transcription must therefore stay strictly page-faithful: never merge or re-split printed pages, because printed pages become typeset pages one-for-one. `tools/transcript2tex.py` converts transcript pages to TeX fragments; extend its page lists when new days land (that's M-print work, not required in M3 sessions).

## Models & budget

Translation prose = **Opus** (per Wilson's opus-for-authored-prose rule). Transcription-only sessions may run cheaper if split out, but the simplest shape is one Opus session per day (transcribe + translate). Estimated ~11–22 spreads per day-section, ≈100–150k tokens per session, ~8–10 sessions for all of Part I.

## Known hazards (learned in Day 1 — do not relearn)

- Duplicate scan leaves shift the page arithmetic silently. Verify printed page numbers by eye.
- The archive.org IIIF endpoint rate-limits hard; always work from the local PDF.
- The PDF has no usable text layer; `raw/preces1853_djvu.txt` is a Latin-side finding aid ONLY.
- Greek OCR of any kind is unusable — vision transcription from the 200-dpi images only.
- Hebrew occurs in main text (fence-of-the-Law headings); transcribe in Hebrew script on its own line.
- Brightman 1903 re-arranged the work; never import his ordering or wording. Cribs are for catching construal errors after drafting, per CONVENTIONS §12.
