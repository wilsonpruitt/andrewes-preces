# Andrewes Preces Privatae — trilingual edition (Greek · Latin · English)

Wroot Press edition of the 1853 Parker printing (1675 Sheldonian text). This repo holds transcription, translation, and print prototypes. **Print layout is DECIDED: the 1675 mirror** (Greek verso / Latin recto page-for-page, English register at the spread foot) — so transcription must stay strictly page-faithful; never merge or re-split printed pages.

## Session protocol

1. Read `next-session-resume.md` FIRST — it names the current front and next action.
2. Then `M3-HANDOFF.md` (the volume-run recipe) and `CONVENTIONS.md` (transcription + translation rules). Follow them exactly; do not re-derive or drift. `STRUCTURE.md` has the volume map and page-offset anchors.
3. Day 1 files (`part1/day1-transcript.md`, `part1/day1-english.md`) are the format reference — match them precisely.

## Hard rules

- **Vision transcription only.** The PDF has no usable text layer; all OCR of the Greek is garbage. Read the 200-dpi images (`pdftoppm -jpeg -r 200`), one spread (2 leaves) per pass, verbatim; `[?]` for unreadable; never infer Greek from context.
- **Verify printed page numbers by eye** at the start/end of every extraction batch — the Google scan has duplicate leaves (42/43 scanned twice; offset is +18 before printed 44, +20 after). Record new anomalies in STRUCTURE.md's anchor table.
- **Translate the Greek** (Part I); Latin is the construal witness; English line-keyed, thou-form AV/BCP register per CONVENTIONS §8–10.
- **Brightman 1903 / Newman / Neale are cribs only** — consult after drafting, never copy, never import Brightman's ordering.
- **No git push, no deploy** — protected actions, per-action OK from Wilson. ⚠ **The repo HAS a remote** (`origin` → github.com/wilsonpruitt/andrewes-preces); older notes said it never had one and were wrong. Verify with `git remote -v`, never from prose. Commit locally: content commit + (if needed) notes commit, then update `next-session-resume.md` as the last commit of the session.
- Translation prose sessions run on **Opus** (Wilson's opus-for-authored-prose rule). If this session's task is a volume day and the model isn't Opus: ⚠️ Wilson — check your model. (Say it once, then proceed as he decides.)

## Build (prototypes / future edition)

`python3.11 tools/proof2tex.py` builds the **whole-volume proofing copy** (`prototypes/volume-proof.tex`; `--part 1|2|3` for one part) — continuous flow, both layers, not the mirror. `python3.11 tools/transcript2tex.py` regenerates the mirror's `prototypes/fragments/`; `cd prototypes && xelatex proto-b-mirror.tex`. TeX packages paracol/bidi/zref/auxhook are user-installed from the frozen TL2025 repo (system tlmgr can't cross-install from 2026 CTAN). Cardo covers polytonic Greek + Hebrew; Hebrew needs `\RL{}` (bidi).
