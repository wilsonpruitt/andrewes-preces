# M2 print-layout prototypes

Same sample in all three: Day 1, printed pp. 30–43 of the 1853 ed. (Commemoration, Confession, Prayer for Grace, and the Hebrew-headed Fence of the Law). 6×9 trim, Cardo throughout.

| PDF | Layout | Trade-offs seen on the page |
|---|---|---|
| `proto-a-stacked.pdf` | Greek block → Latin block → English block, per prayer unit | Bulletproof to typeset; reads well for praying one language at a time; BUT in long units (Confession = 5 pages of Greek) the languages drift far apart — you cannot compare a line across languages without flipping. |
| `proto-b-mirror.pdf` | Greek verso / Latin recto exactly as 1853, English register across the spread foot | The collector's edition; the 1853 page IS the page; three languages visible on one spread. English is subordinate (italic, small). Requires page-fitting discipline every spread (one overflow broke the mirror until fixed). |
| `proto-c-loeb.pdf` | Greek \| Latin two columns on verso, English full recto | Best line-for-line comparability — the 1853's own parallelism keeps the two columns in step; English gets full-page dignity. Originals at smaller size; longest Greek lines wrap in the narrow column. |

## Beyond the sample

Two whole-volume builds now exist, from the same parser and the same renderer:

| PDF | Built by | What it is |
|---|---|---|
| `volume-proof.pdf` | `tools/proof2tex.py` | 608pp **proofing copy** — continuous flow, printed order, every page's original with its English beneath. Not the edition. |
| `volume-loeb.pdf` | `tools/transcript2tex.py` | 604pp — **THE EDITION LAYOUT**, ruled 2026-08-05. Originals verso, English recto; Part I's Greek and Latin share a leaf in two columns. The edition's own folios, 1853 page as a shoulder-note. |
| `volume-mirror.pdf` | `… --layout mirror` | 566pp — prototype B, the 1675 mirror. **Not the edition**; kept because it is what the Loeb was measured against, and because Part I's mirror is still the truest picture of the 1853's own page. |

**Why the Loeb cannot desynchronise:** nothing depends on a page facing its own translation. Originals are always verso, English always recto, so a unit that runs long takes two spreads and the alternation is untouched — 0 of 596 units are too tall for their leaf. The mirror, by contrast, stakes verso/recto on every page fitting: `\versoalign` holds its register at a cost of one blank leaf, and printed 256 and 257 stay spoilt.

⚠ **`--fit` measures BOX HEIGHTS for the Loeb, not page marks.** A minipage overruns in silence rather than breaking, so the marks that instrument the mirror would report no overflow here however bad it got.

⚠ **Before touching a column width, run `python3.11 tools/measure_lines.py`.** 839 of Part I's 6,759 sense-lines already turn in the two columns (against 23 at full width), and the **Latin** column turns more than the Greek — so widening the Greek for its longer lines makes the total worse, not better. The full trade is at `EDITION-SHAPE.md` §6b.

## Build

```
python3.11 tools/transcript2tex.py                  # the edition + prototypes/fragments/
python3.11 tools/transcript2tex.py --part 1         # Part I only
python3.11 tools/transcript2tex.py --fit            # fit report for the last build
python3.11 tools/transcript2tex.py --layout mirror  # prototype B, for comparison
python3.11 tools/measure_lines.py                   # turned lines, both layouts
cd prototypes && xelatex volume-loeb.tex            # likewise proto-a-stacked, -b-, -c-
```

Requires: TeX Live + user-mode packages `paracol bidi zref auxhook` (installed 2026-07-16 into `~/Library/texmf` from the frozen TL2025 repo — system tlmgr can't cross-install from the 2026 CTAN), Cardo font. Hebrew via `bidi`'s `\RL{}` (xelatex does not auto-bidi).

Known prototype simplifications (fix in the real edition): brace groups render as literal `{ a / b }` text, not typeset stacked braces; prototype B's English register splits mechanically near the spread's midpoint; no drop caps / ornaments.
