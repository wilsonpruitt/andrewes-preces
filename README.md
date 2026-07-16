# Andrewes: Preces Privatae — trilingual edition (Greek · Latin · English)

Wroot Press edition of Lancelot Andrewes' *Preces Privatae*: Greek original, historic Latin parallel, fresh English translation. First trilingual title in the catalog.

- **Text source:** 1853 J.H. Parker reprint of the 1675 Sheldonian first edition ([archive.org](https://archive.org/details/precesprivataeq00andrgoog)), `raw/preces1853.pdf` (gitignored). Public domain.
- **English cribs (reference only, never copied):** Brightman 1903 ([archive.org](https://archive.org/details/theprecesprivata00andruoft) — re-arranged, does NOT follow 1853 order), Newman 1840 (Greek part), Neale 1844 (Latin part).
- **Deliverables:** static parallel-text site at andrewes.wrootpress.com (modeled on bonaventure.wrootpress.com) + print volume via `~/wroot-press/_pipeline`.

## Layout

- `part1/` — one markdown file per prayer unit (`## Greek` / `## Latin` / `## English` / `## Apparatus` / `## Notes` blocks)
- `raw/` — source PDF and extracted page images (gitignored)
- `tools/` — pipeline scripts
- `STRUCTURE.md` — map of the 1853 volume (part boundaries, PDF↔printed page offsets, day structure)
- `CONVENTIONS.md` — translation + transcription conventions (the score cheaper sessions play from)

## Plan

Full project plan: `~/.claude/plans/i-want-to-think-quiet-rabbit.md` (M1 pilot = Day 1; M2 = three print-layout prototypes; M3 = Part I volume run; M4 = site; M5 = Parts II–III).
