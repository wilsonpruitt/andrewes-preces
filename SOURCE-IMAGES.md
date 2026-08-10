# Source images — the non-Google digitizations (found 2026-08-10)

**The pre-print residue was an images problem. Three free, non-Google scans now cover it.** Nothing here is commissioned, nothing is paywalled, and no institution needs to be written to.

⚠ **Read this before spending anything on reprographics, and before recording any leaf as unrecoverable.**

---

## Why the Google scan is bad, stated exactly

`precesprivataeq00andrgoog` is **1-bit bitonal** — 2910×5002 at `bitsPerSample: 1`, ~38 KB a page, no JP2 masters. Bitonal thresholding throws away the faint strokes (vowel points, breathings, worn serifs) **before the file is written**, so no amount of processing recovers them. Every `[?]` in our transcripts traces to that, or to the two-leaves-in-one-frame photography.

**The gain from the new sources is continuous tone and complete margins, not the dpi figure.** Only one of them actually reaches 600 ppi, and it is not the one we mostly need.

---

## 1. THE DEFAULT — University of Toronto 1853 Parker (our exact base text)

**`https://archive.org/details/precesprivataequ00andruoft`**

Verified from the IA metadata API, not from prose: `scanner: scribe11.toronto.archive.org`, `sponsor: University of Toronto`, `ppi: 400`, `imagecount: 484`, publisher *Oxonii : J. H. Parker*, 1853. **Not Google.** 24-bit colour. Free, no wall.

- **Single leaves, not spreads** — which is the whole fix for our worst imaging defect.
- **Complete to printed 436 and through the *Variæ Lectiones*** (apparatus around leaves 479–492).
- IIIF, ungated, full size:

```
https://iiif.archive.org/image/iiif/3/precesprivataequ00andruoft%2fprecesprivataequ00andruoft_jp2.zip%2fprecesprivataequ00andruoft_jp2%2fprecesprivataequ00andruoft_NNNN.jp2/full/max/0/default.jpg
```

`NNNN` is the zero-padded leaf. Swap `full` for `x,y,w,h` to crop. **IIIF 3 wants `max`, not `full`, in the size slot.**

⚠ **The offset is NOT constant and is not ours.** Measured: leaf `0257` = printed **229** (+28), leaf `0238` = printed **212** (+26). **Verify every leaf by eye against its printed page number, exactly as with the Google PDF.** Do not port our `STRUCTURE.md` offsets — they belong to a different scan with different duplicates.

⚠ **Focus varies leaf to leaf** (2008 Canon 5D). Printed 212 is soft; printed 239 and the leaf at `0236` are crisp. **It is uniformly better in *tone*, not uniformly better in *sharpness*.** Check the leaf you actually need before concluding anything from it.

⚠ **Two crop regimes.** Some leaves are uncropped (~2912×4368, cradle and fore-edge visible), others auto-cropped (~1805×3152). **Fixed pixel regions do not map across leaves** — re-find your crop per leaf.

## 2. FOR GREEK ACCENTS — Illinois 1848 Pickering, 650 ppi

**`https://archive.org/details/reverendipatrisl00andr`**

Verified: `scanner: scribe1.il.archive.org`, University of Illinois, **`ppi: 650`**, 406 images, Londini: G. Pickering, 1848 — Greek and Latin. Not Google. The sharpest glyphs available anywhere.

⚠⚠ **It has NO apparatus and NO Hebrew** — the *Variæ Lectiones* is a 1853-Parker feature. ⚠ **Its pagination is not ours**, so it is a collateral witness, never a page-for-page substitute. **Use it only to settle a Greek accent or breathing.**

## 3. FOR THE 1675 — the Sheldonian, free on IA after all

**`https://archive.org/details/bim_early-english-books-1641-1700_rev-patris-lanc-andrew_andrewes-lancelot_1675`**

EEBO-microfilm derived but **grayscale, not bitonal**, `ppi: 800`, IIIF 3233×5160 — the largest pixel dimensions of anything here, with full margins including the outer-margin line-turnovers.

⚠ **Harsh microfilm contrast, blown highlights, halation — do NOT trust it for Hebrew vowel points.** It is the ancestor of our text and it is authoritative for *what a cut or damaged Latin margin says*.

⚠ **Corrects a claim repeated in our own notes:** the 1675 is not undigitized. It is free.

## 4. A SECOND 1853 COPY — Claremont School of Theology

**`https://archive.org/details/precesprivatquot0000andr`** — a *different physical copy*, for when a leaf is damaged in the Toronto one. Masters are 6000×4000 colour inside `_orig_jp2.tar`; **the IIIF derivative is downsampled to 1704×2945, worse than Toronto**, so the derivative is not worth using. ~450 ppi effective on the leaf.

## 5. ⚠⚠ THE LEAD WE DID NOT ASK FOR — Wright's apograph itself is digitized

The 1853 apparatus is headed **EX APOGRAPHO SAMUELIS WRIGHT, APUD COLL. PEMB. CANT.** — and that manuscript, the Greek manual in Wright's hand with **Drake's annotations**, is on Cambridge Digital Library:

**`https://cudl.lib.cam.ac.uk/view/MS-PEMBROKE-LC-00002-00174`**

**This is the source *behind* class A, not another witness beside it.** `apparatus/CLASS-A-ledger.md` currently reasons from the 1853 editor's *report* of that copy; `THE-LATIN-QUESTION.md` rests on his report of one word (`πλάσμα` at printed 34/35); and the unresolved class A/C collision — whether a reading is Drake's or Andrewes' — is a question about **Drake's own marginalia**, which are on these leaves.

⚠ **Unverified: CUDL returned 403 to automated fetch**, so resolution, completeness and licence are unconfirmed. **Needs a browser, not a script.** ⚠ It is *not* the Pembroke MS the critical-text option needs (`EDITION-SHAPE.md` option 3) — it is Wright's transcript. **It does not make a critical text reachable; it makes the apparatus checkable.**

---

## Negative results — recorded so nobody pays to repeat them

**HathiTrust**: no non-Google 1853 worth having; **no record at all** for the 1675 or the 1848. **Digital Bodleian**: nothing, any edition. **Cambridge DL / British Library / Lambeth**: no digitized printed *Preces*. **MDZ, e-rara, Gallica, ÖNB**: negative. **EEBO/ProQuest**: paywalled, and moot — IA serves the same film free and in grayscale.

**Reprographics, if a leaf ever defeats all three scans:** Bodleian £27 first + £7.50 each thereafter, TIFF 600 ppi (they are the 1675's printing institution); Harvard $20 flat for the first 10 but holds only the 1853, which is already free. **Do not commission anything until a specific leaf has beaten all three sources.**

---

## Status of the four blocked watch items

| | item | status |
|---|---|---|
| 1 | **printed 239**, Latin recto cut off by the one-frame spread photograph | ✅ **CLOSED — read entire and legible** on Toronto leaf `0267`, every line complete to the right margin. ⚠ **The transcript still carries the `[?]`s; restoring them is Wilson's call, not the notes pass's.** |
| 2 | **printed 210**, left-margin ink smear | **Open, expected easy.** The smear is a Google-scan artifact, so Toronto should simply not have it. Leaf not yet pinned — the offset drifts, find it by eye near `0236`. |
| 3 | **printed 386**, the garbled Hebrew `חזתלת` | **Open — and a better scan cannot repair it.** Confirmed a *plate* defect (the Google duplicate at PDF 423 reads the same five garbled letters). Toronto buys **certainty about the sorts**, not a reading. The reading stands on Andrewes' own facing Latin *Ecce spes*. |
| 4 | **printed 414**, the `Job. xxv. 3` cento | **Open, and Toronto is the wrong tool** — this needs *Brightman's* page images (he marks Hebrew by italics and italics don't survive OCR), not a better 1853. |

⚠ **So the digitization closes 1 outright, should close 2, confirms 3, and does not touch 4.** The earlier note that "a digitization unblocks the entire remaining pre-print list at once" was **too optimistic** — 414 was never an 1853-imaging problem.

⚠ **`apparatus/print-notes.md` still carries its standing warning that all Hebrew was read at 200 dpi and must be re-read before it is set.** That re-read is now possible and has not been done.
