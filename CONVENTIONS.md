# Conventions — Andrewes *Preces Privatae* trilingual edition

Frozen from the Day 1 pilot (2026-07-16). Later sessions follow this file; propose changes here rather than drifting silently.

## Transcription (Greek + Latin from the 1853 Parker ed.)

1. **Verbatim 1853** — accents, breathings, punctuation, ligatures (æ/œ), capitalization as printed. Do not normalize to modern orthography, do not correct to LXX/Vulgate readings. Genuinely unclear glyph → transcribe best reading + `<!-- print unclear: x/y -->`; wholly unreadable → `[?]`.
2. **Layout encoding:** 4 spaces per indent level; page boundaries as `<!-- printed N (PDF M) — Greek|Latin -->`; running heads/catchwords/signatures omitted; printed brace groups as `{ a / b / c }` (inline) or leading `{ ` on stacked lines; multi-column rows transcribed row-wise with ` | ` between columns, a row continuing only in the right column starts ` | `. Square brackets = the 1853 editor's supplied refs — keep them.
3. **Scripture refs** stay inline where printed (Latin side), book abbreviation italicized exactly as printed (*Psal.*, *Es.*, *Jud. vers.*, *Chrysost. Liturg.*). Do not correct wrong refs (e.g. *Psal.* cxxx. 30) — flag in unit Notes instead.
4. **Hebrew in main text** (e.g. סיג התורה, printed p. 42) transcribed in Hebrew script, RTL, on its own line.
5. **Always verify the printed page number in the image header** — the Google scan has duplicate leaves (42/43 twice). Never trust page arithmetic alone.

## English layer (fresh Wroot Press translation)

6. **Translate the Greek** in Part I (it is Andrewes' primary text there); consult the Latin as the first witness to construal. Where they genuinely diverge, follow the Greek and record the Latin's reading in the unit's Notes. (Latin-only sections in Part II: translate the Latin.)
7. **Line-keyed:** one English line per source line, same indent level, same brace/column structures. The reader must be able to run a finger across three columns and stay in step.
8. **Register: hieratic English of the AV/BCP stream** — *thou/thee* to God, *O Lord*, "Blessed art thou." Rationale: the text is a cento of Scripture that English readers know in AV cadence, and the edition is for praying, not just study. BUT: syntax stays plain and modern-lucid; archaism is confined to pronouns/verb inflections of address (-est/-eth only for address to God, never for narration); no faux-Jacobean inversions the Greek doesn't force.
9. **Scripture echoes:** where a line quotes Scripture verbatim, echo AV wording as the default *unless* Andrewes' Greek visibly departs from the text the AV renders — then follow Andrewes and let the Notes say so. Andrewes' variations are the point of the work.
   - **Psalter crib = the Coverdale/BCP Psalter, ahead of the AV.** Andrewes did not quote an English Bible; his psalm-lines come from the **LXX** (Greek) and **Vulgate** (Latin), never from the AV (1611, from the Hebrew). The **BCP Psalter is Coverdale's**, made *through* the Latin/German — so it carries Vulgate/LXX-flavored readings and repeatedly agrees with Andrewes' Greek in exactly the places the AV (from the Hebrew) diverges. For psalm citations, therefore, **reach first for the Coverdale/BCP Psalter** (1559/1662 — identical for the Psalter; the book Andrewes himself prayed was the 1559 Elizabethan / 1604 Jacobean, *not* the 1662): where BCP-Psalter and Andrewes' Greek agree against the AV, follow that reading and note it. Use the AV cadence as the general model for non-Psalter Scripture and where BCP, AV, and Andrewes all coincide.
10. **Divine titles in caps** (ΙΗΣΟΥ ΧΡΙΣΤΟΥ, Ὁ ΘΕΟΣ) keep their emphasis: JESUS CHRIST, O GOD. Caps openers (ΔΙΑ / PER) → caps first word in English (THROUGH …).
11. **Hebrew headings:** keep the Hebrew, add translation: `סיג התורה — The Fence of the Law`. The English layer never silently drops a script.
12. **Cribs:** Brightman 1903 and Newman 1840 may be consulted as reference AFTER drafting a line, to catch construal errors — never copied. Brightman follows a different arrangement; do not import his ordering.
    - ⚠ **Brightman prints NO Greek and NO Latin** (his preface §4; verified — zero Greek and zero Hebrew runs across all 472 pp of OCR). He can therefore settle a **reference, an attribution, a construal or a sense — never a lost WORD.** Do not send anyone to him to repair a defective plate. He also marks Hebrew by *italics*, which do not survive OCR: Hebrew questions need his page images.
    - ⚠ **His headings are his own** — *"For titles, etc., which are printed in thick type… I am responsible."* Never import a Brightman heading as recovered text.
12a. **⚠ LOST WORDS — the dagger convention** (added 2026-08-04, Wilson's call: *"let's footnote or asterisk lost words for the time being"*). `*` is unavailable — it is markdown italic and the files are full of `*Psal.*`. So:
    - Where the **source** has lost words (plate defect, scan damage, a garbled sort), the English layer marks the loss **once per page block** with a **`†`** appended to the point of loss — normally to the first `[?]` in that block.
    - ⚠ **The `†` is appended INLINE to an existing line. It never adds a line**, because English parity is line-exact per §7 and a new line silently breaks the mirror.
    - Each `†` is keyed to a numbered entry in a **`## Lost words`** section at the foot of the English file, which states: the printed page, what is lost, what secures the construal meanwhile, and **what would be needed to recover it**.
    - The **transcript is untouched** — it keeps `[?]` per §1. `†` never appears in a transcript.
    - **A loss that has been RECOVERED from a witness stops being a lost word.** It graduates to the ordinary bracket convention `[ ]` with the witnesses named in the flags. The dagger is for what is still gone.
    - ⚠ Where a lost word falls on a **Latin recto in Part I**, there is **no English block to mark** (English keys to the Greek versos, §7). Record it in the flags; do not invent a phantom English line for it.

## Unit model (for the eventual chunk files)

13. Unit boundaries follow the 1853 typographic breaks (large blank + caps opener), cross-checked against the *Variae Lectiones* section B spacing record. Day 1 units: Commemoration (ΔΙΑ/Δόξα/Θεὸς Κύριος…), Confession (ΟΙΚΤΙΡΜΟΝ…), Prayer for Grace (ΑΙΡΩ…), Profession of Faith (ΠΙΣΤΕΥΩ…), Hedge of the Law (סיג התורה/ΤΗΝ κεφαλὴν…), Intercession (Ὦ ἡ ἐλπὶς…, through the trades/family/enemies sequence), Remembrance litany (Μνήσθητι, Κύριε…), Blessing + Commendation (ΣΥΝΙΣΤΩ…), Sursum corda + Sanctus + closing doxology.
14. Chunk file shape (bonaventure-style): frontmatter (`id, part, day, section, type, printed_pages, title_gr, title_la, title_en`) + `## Greek`, `## Latin`, `## English`, `## Apparatus` (`[^N]: **Gr.** … **La.** … **En.** …`, Variae Lectiones entries incl. Hebrew verbatim), `## Notes` (scripture refs normalized to OSIS dual-key per `reference_data-repository-standard.md`; ref errors flagged; genuine Gr/La divergences).

## Fonts / rendering (downstream)

15. Print: Cardo (polytonic Greek + Hebrew coverage in one face). Site: verify chosen webfont renders polytonic + Hebrew IN THE BROWSER before shipping (rendered check, not build check).

## Print layout by language-count (Part II+ — PROVISIONAL, pending prototype)

> Decided provisionally by Wilson 2026-07-17. **Not frozen** — build sample spreads at M-print time (as Prototype B was chosen for Part I) before committing. Affects typesetting only; transcription/translation are layout-agnostic and proceed regardless.

16. **The number of source languages on a given opening decides its layout.** Part I is uniformly Greek-verso / Latin-recto parallel, so it is uniformly the trilingual mirror (Prototype B: Gr verso / La recto, English as the italic register across the spread foot). Part II is mixed, so the layout follows the opening:
    - **One source language stands alone on the opening** (Latin-only — most of printed 267–360; or Greek-only — e.g. 367–369) → **that language verso / English recto**, a two-language facing mirror. English is promoted from foot-register to a full facing page here, because it carries the whole translation load.
    - **Greek + Latin run in parallel** (the eucharistic/hymns/poems finale, ~361–397) → revert to the Part I **trilingual mirror** (Gr verso / La recto, English foot-register).
17. **Inline Greek glosses do NOT trigger the trilingual switch.** Most of Part II's "La+Gk" main body is Latin with a few inline Greek words (Ὑπεύθυνον, Κηλίς, Χρηστός, imperatives). Those ride *inside* the Latin verso exactly as the 1853 sets them; only a **sustained Greek parallel column** flips the layout. Net effect: essentially ONE structural boundary (bilingual La/En for ~267–360, trilingual for the ~361–397 finale), not constant flipping. The Latin-only pages are single-column in the 1853 (no source parallel to preserve), so putting English on the facing verso breaks no mirror.
18. **Known cost + the alternative.** English's typographic status shifts (foot-register in trilingual passages, full facing page in bilingual ones) — a reader feels it. Accepted rationale: English steps up precisely where it is the only translation. The consistency-first alternative, if the wobble reads badly in prototype, is to keep **English as the foot-register everywhere** and run Latin-only sections as a single full-width body with English beneath (invariant English role, but loses the facing-parallel look and gives a long Latin measure). Resolve at prototype time. See `STRUCTURE.md` §PARS SECUNDA for which sections carry which layer.
