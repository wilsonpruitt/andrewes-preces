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

## Unit model (for the eventual chunk files)

13. Unit boundaries follow the 1853 typographic breaks (large blank + caps opener), cross-checked against the *Variae Lectiones* section B spacing record. Day 1 units: Commemoration (ΔΙΑ/Δόξα/Θεὸς Κύριος…), Confession (ΟΙΚΤΙΡΜΟΝ…), Prayer for Grace (ΑΙΡΩ…), Profession of Faith (ΠΙΣΤΕΥΩ…), Hedge of the Law (סיג התורה/ΤΗΝ κεφαλὴν…), Intercession (Ὦ ἡ ἐλπὶς…, through the trades/family/enemies sequence), Remembrance litany (Μνήσθητι, Κύριε…), Blessing + Commendation (ΣΥΝΙΣΤΩ…), Sursum corda + Sanctus + closing doxology.
14. Chunk file shape (bonaventure-style): frontmatter (`id, part, day, section, type, printed_pages, title_gr, title_la, title_en`) + `## Greek`, `## Latin`, `## English`, `## Apparatus` (`[^N]: **Gr.** … **La.** … **En.** …`, Variae Lectiones entries incl. Hebrew verbatim), `## Notes` (scripture refs normalized to OSIS dual-key per `reference_data-repository-standard.md`; ref errors flagged; genuine Gr/La divergences).

## Fonts / rendering (downstream)

15. Print: Cardo (polytonic Greek + Hebrew coverage in one face). Site: verify chosen webfont renders polytonic + Hebrew IN THE BROWSER before shipping (rendered check, not build check).
