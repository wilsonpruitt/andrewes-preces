# KDP upload sheet — *Preces Privatae*

**Written 2026-08-26, at the close of the cover build, for the session that does the upload.**
Every number here was verified against the built files, not carried from prose. Nothing in the
book is open: the introduction is approved, cream is ruled, the interior is final.

⚠ **This sheet does not need an Opus session.** It is execution. What needed judgment is done.

---

## The files

| | path | verified |
|---|---|---|
| interior | `prototypes/volume-loeb.pdf` | `pdfinfo` — **625 pages, 432 × 648pt = 6 × 9in** |
| cover (upload this) | `covers/out/wrap.pdf` | `pdfinfo` — **994.5 × 666pt = 13.812 × 9.25in** |
| front panel (listing art only, NOT the upload) | `covers/out/front.pdf` | 432 × 648pt |
| keep-out proof (human look only) | `covers/out/wrap-guides.pdf` | box drawn in red |

Fonts in the cover are **Cardo + Cardo-Italic, embedded and subset**. The artwork is type only —
there is no raster in it, so there is no 300dpi image requirement to satisfy.

## Print options — ⚠ THE ONE TRAP ON THIS TITLE

KDP's Content tab pre-fills **"Black and white interior with white paper"** and trim **6 × 9in**,
and it resets on every newly created title ([[feedback_kdp-print-option-defaults]]).

⚠⚠ **On this book the trim default is RIGHT and the paper default is WRONG, which is the dangerous
combination.** 6 × 9 is what we want, so the Print Options block looks correct at a glance — and
the paper underneath it is white when the book is cream. Set it explicitly:

- **Ink and paper: Black and white interior with CREAM paper** ← the override
- **Trim: 6 × 9 in** (matches the default; confirm anyway)
- **Bleed: No bleed** (the interior has none; the *cover* carries its own 0.125in bleed already)
- **Cover finish: Matte**

**Then re-read the page after setting them** to confirm they took. Cream is not a preference here:
the spine was computed at `PPI = 0.0025` (cream). White is 0.002252 and would make the correct
spine **0.14in narrower than the cover we are uploading** — the wrap would be wrong and KDP would
not necessarily reject it.

## What to expect in the previewer

- **Spine 1.562in** at 625pp cream. Spine text is set and there is ample width for it.
- **The barcode area is clear.** Verified mechanically, not by eye: a 300dpi crop of the 2 × 1.2in
  box, 0.25in in from the back panel's spine-side and bottom trim edges, is **one flat colour
  across all 216,000 pixels**. If the previewer shows the barcode landing on ink, something has
  changed in the cover — do not "nudge" it, re-run `python3.11 covers/cover.py guides` and look.
- The interior is **0 TeX errors, 0 `Missing character`, 0 of 595 units too tall.**

## Still to decide at upload (not book decisions)

ISBN (KDP-assigned vs. own), price, categories, keywords, and description. The back-cover blurb in
`covers/cover.py` (`bl[0]`–`bl[3]`) is the tested copy and is a reasonable base for the listing
description — it is the text Wilson approved on the cover.

## Do not

- ⚠ **Do not change the paper stock** without rebuilding the cover. See above.
- ⚠ **Do not regenerate the interior** to "fix" anything. It is final at 625pp and the cover's
  spine depends on that exact count.
- ⚠ **Do not put the portrait on the cover.** It is the frontispiece, whole, with its verse tablet,
  and the type-led front is Wilson's ruling. Reasons in the `covers/cover.py` docstring.
- ⚠ Use **Playwright**, not the Chrome extension, if driving KDP by automation
  ([[feedback_kdp-upload-pacing]]).
