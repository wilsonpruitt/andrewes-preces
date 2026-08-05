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
| `volume-mirror.pdf` | `tools/transcript2tex.py` | 566pp **edition layout** — the edition's own folios, with the 1853 page as a shoulder-note in the inner head of every leaf. `--part 1` for `part1-mirror.pdf`. |

⚠ **The mirror's discipline belongs to Part I alone** — there, and only there, an overflow desynchronises verso from recto. `\versoalign` forces every Greek page onto a left-hand leaf, so an overflow spoils its own spread and the book realigns at the next one; the whole volume spends **one** blank leaf on that. Parts II–III have no facing page to fall out of, so their 128 second leaves are bulk, not damage.

Every leaf is instrumented: `python3.11 tools/transcript2tex.py --fit` reads the last build's `.fit` record and reports second leaves, blanks spent, and — the one that matters — **any Part I Greek page that landed on a recto**. Currently none. Printed **256 and 257** are the two spreads still wanting hand-fitting. Shape ruled by Wilson 2026-08-05; see `EDITION-SHAPE.md` §6a.

## Build

```
python3.11 tools/transcript2tex.py            # whole-volume mirror + prototypes/fragments/
python3.11 tools/transcript2tex.py --part 1   # Part I only
python3.11 tools/transcript2tex.py --fit      # page-fit report for the last build
cd prototypes && xelatex volume-mirror.tex    # likewise proto-a-stacked, -b-, -c-
```

Requires: TeX Live + user-mode packages `paracol bidi zref auxhook` (installed 2026-07-16 into `~/Library/texmf` from the frozen TL2025 repo — system tlmgr can't cross-install from the 2026 CTAN), Cardo font. Hebrew via `bidi`'s `\RL{}` (xelatex does not auto-bidi).

Known prototype simplifications (fix in the real edition): brace groups render as literal `{ a / b }` text, not typeset stacked braces; prototype B's English register splits mechanically near the spread's midpoint; no drop caps / ornaments.
