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

⚠⚠ **THE TORONTO SCAN HAS DUPLICATE LEAVES TOO, and its offset is NOT ours.** This was proved the hard way: leaf `0306` re-photographs printed **272**, already shot at `0304`. Measured anchors — `0060`=42 (+18) · `0064`=46 · `0238`=212 (+26) · `0257`=229 (+28) · `0267`=239 (+28) · `0301`=271 (+30) · `0308`=274 (+34) · `0411`=369 (+42). **The offset climbs from +18 to +42 and jumps 4 in a single spread.** **Verify every leaf by eye against its printed page number, exactly as with the Google PDF.** Do not port `STRUCTURE.md`'s offsets — they belong to a different scan with different duplicates.

⚠ **Apparatus offset is separate and simple: Toronto leaf = Google PDF − 3.** Verified: leaf `0482` = apparatus **iv** = PDF 485. So apparatus [i]=0479, ii=0480, iii=0481, iv=0482, v=0483.

⚠ **There is no text layer** — `_djvu.txt` is empty (0 bytes), so you cannot grep your way to a page. Probe headers instead; stacking several header strips into one image with PIL makes it one look rather than six.

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


---

## What the scan has actually settled (2026-08-10)

Every item below was read on the Toronto scan at native resolution and checked against our transcripts. **Nothing in our transcription of any of it turned out to be wrong.**

| item | leaf | result |
|---|---|---|
| **printed 239**, the cut-off Latin recto | `0267` | ✅ **CLOSED.** Read entire. Restored — and it had hidden a whole line (`DOMINE,`), seven references, `furem`-for-*furen*, and a silent truncation. Closed a Part I parity mismatch. |
| **printed 386**, the garbled Hebrew | `0428` | ✅ **Confirmed a PLATE defect** — `חזתלת` stands exactly so at 400 ppi. ⚠⚠ **And the mechanism is now visible: the very next word is `התועלת`.** The compositor was setting two near-identical words in succession — *tocheleth* and *ha-to'eleth*, which differ by one consonant — **and garbled the first into a mangling of the second.** That is a far better account than random transposition, and it is only visible when both words are legible together. |
| **printed 42** `סיג התורה` · **274** the Hosanna pair · **383** `לך דומיה תהלה` | `0060` · `0308` · `0425` | ✅ All confirmed letter for letter. |
| apparatus **`אדאג`** (38. 3) | `0480` | ✅ Confirmed — **secure on its sorts now, not only on sense.** |
| apparatus **`יצר טוב`** (76. 4) · **`תהום`·`תוהו`·`בוהו`** (92) | `0481` | ✅ Confirmed. |
| apparatus **seven-word column** (96. 25) | `0482` | ✅ All seven confirmed; our transcript of the page, including the second column of seven Greek words, is complete and exact. |
| apparatus **`ואתה תעל משחת חיי`** (152. 8) | `0483` | ✅ Confirmed. |
| ⚠⚠ **THE LATIN QUESTION's one load-bearing word** | `0480` | ✅ **`pro τὰ ἔργα lege τὸ πλάσμα` is unambiguous.** The argument may now go into an introduction. **Off the pre-print list.** |
| ⚠⚠ **the dot-marks**, unresolvable at 200 dpi | `0480` | ✅ **RESOLVED — an ascending count, 1 to 5, that PAIRS ACROSS THE COLUMNS** (μετὰ carries μὴ διαφθείρῃς's 2; διὰ carries Ὡσαννὰ's 3). **Off the pre-print list.** |

**Still open:** printed **210**'s ink smear (expected easy — it is a Google artifact; leaf not yet pinned, the offset drifts near there) and printed **414**'s cento, which needs *Brightman's* page images and not a better 1853. The `אל תשחית`/`הצילני` cluster at 198–202 and `יראתי כסלתי` at 212. 1 are unread only because nothing sets them.
