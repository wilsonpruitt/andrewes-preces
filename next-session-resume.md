# Next session — resume note

**Current front: M3 volume run, DAY 4 (ΤΗΣ ΤΕΤΑΡΤΗΣ ΗΜΕΡΑΣ / DIEI QUARTÆ).**

## NEXT ACTION

1. Extract images: `pdftoppm -jpeg -r 200 -f 126 -l 150 raw/preces1853.pdf raw/day4/p` (mkdir `raw/day4` first).
   Expected: printed 106–129 at offset +20 → PDF 126–149 (Day 5 starts printed 130 ≈ PDF 150). **Verify by eye that p-126.jpg shows printed page 106 with the ΤΗΣ ΤΕΤΑΡΤΗΣ ΗΜΕΡΑΣ heading, and that p-149 is printed 129.** If the numbers are off, the scan has more duplicate leaves — hunt the shift, note it in STRUCTURE.md, re-extract before transcribing.
2. Transcribe spread-by-spread into `part1/day4-transcript.md` (12 spreads — this is a LONG day, ~24 pages), then translate into `part1/day4-english.md`. Format = exact match of the Day 1–3 files; rules = CONVENTIONS.md; recipe + self-checks = M3-HANDOFF.md. Day 4 is large — consider splitting transcription and translation across two sessions if context runs tight.
3. Commit content; update this file to point at Day 5 (printed 130–147) as the last commit.

## State (2026-07-16)

- DONE: M1 (Day 1 transcript + English + CONVENTIONS.md), M2 (three print prototypes; **Wilson chose B, the 1675 mirror** — page-faithful transcription is load-bearing), **Day 2 (printed 70–91), Day 3 (printed 92–105)** — both layers, self-checks pass (line-count parity exact on every Greek page).
- Day-start Greek-verso pages (from M3-HANDOFF): 70, 92, 106, 130, 148, 168. Offset held at +20 through printed 105; re-verify entering Day 4.
- Repo is LOCAL ONLY (no GitHub remote — creating one is a protected action, Wilson's call).
- After Days 4–7: evening office (~221–252), Meditations (253–~262), then front matter of Part I (printed 1–29), then Variae Lectiones pass. See M3-HANDOFF.md §Scope.

## Day 3 notes (learned, don't relearn)

- Day 3 is heavy on **catalogue/list units**: two- and three-column tables (the ΚΤΙΣΜΑΤΑ intercession, the 2 Cor. vii. 11 double-brace [εἰς]/[in] table on printed 96–97, the creed catalogue on 98–99). Encoded row-wise with ` | `; center-label double braces got a `<!-- double brace … -->` comment + an `[εἰς]`/`[in]` middle column.
- **Latin prints right-column editorial braces the Greek image doesn't show** (printed 100/101: ψυχὰς/σώματα, τὸ πάλαι/τὸ παρὸν, πανένδεια/τὰ ἔσχατα). Transcribed each side as printed and flagged — watch for the same pattern in Day 4's lists.
- The p.100 intercession is elliptical prayer-shorthand (bare accusative nouns); English preserves the list quality, follows the Greek where the Latin only glosses. Flagged as interpretive.

## Session log

- 2026-07-16 (Fable): M1 pilot + M2 prototypes + layout decision + handoff docs. Day 1 = printed 30–69.
- 2026-07-16 (Opus): Day 2 = printed 70–91, both layers.
- 2026-07-16 (Opus 4.8): Day 3 = printed 92–105, both layers (transcript + line-keyed English). Offset +20 held, no new duplicate leaves. Committed 18b1ad4.
