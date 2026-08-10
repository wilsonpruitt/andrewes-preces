# BRIEF — finishing the notes pass (printed 340 → 436)

**Written 2026-08-10 to be picked up cold.** Read this, then `NOTES-CONVENTIONS.md`. You do not need to read `next-session-resume.md` to start; it is the long history.

**Model: Opus.** NOTES-CONVENTIONS §10. The failure mode here is factual, not stylistic — a wrong speaker or a wrong verse is a printed error that looks perfectly plausible.

---

## 1. Where the work stands

**Done: printed 2–339**, every unit, no gaps. (A tag may carry more than one reference, so the tag count is not the reference count.)

**Remaining: 118 pages.** Part II, printed **340–395**; Part III, printed 398–436. **NEXT IS PRINTED 340.**

⚠ The reference counts the old version of this table gave are now understated — the index was blind to 76 references (§1b), so every per-page count taken before 2026-08-10 was low. Re-run `ref_index.py --all` rather than trusting a number written down earlier.

**Many of the remaining leaves carry no references at all**, and from §18 onward whole runs are brace catalogue. **An empty band is a correct outcome** — see §3 below.

The build is whole and stays whole: **617 pages, 0 TeX errors, 0 of 594 units too tall.** Keep it that way; `--fit` is not optional.

---

## 1b. ⚠⚠ Three tool defects found 2026-08-10 opening printed 324 — all fixed, backfill closed

None was visible in the built PDF, and two of the three corrupted **committed** work. They are the fifth, sixth and seventh of their kind, and the pattern is always the same: a tool quietly reports less, or reports wrong, and every downstream check agrees with it.

1. **`ref_index` could not see nineteen book abbreviations** — `*Thren.*` `*Joan.*` `*Ezech.*` `*Mich.*` `*Es.*` `*Ez.*` `*Syr.*` and twelve more, **71 references invisible**, 52 of them on pages already written. Fixed; the sweep is now `tools/audit_missing_books.py` and **NOTES-CONVENTIONS §11 — run it before opening any new stretch.**
2. **`ref_index` and `note_sheet` counted the transcripts' inline `<!-- ... -->` comments as sense-lines**, which the builder drops. On the **58 pages** that carry one, the index ran ahead of the printed page, so the marker printed *below* the line it describes. **51 tags and 3 notes on 15 pages re-anchored**, each verified against the English. `check_lineparity` was never affected — it counts `\pl` in the built fragments, so it measures the real page, and it is what proved the renumbering right.

⚠ **The lesson for the rest of the pass:** these tools agree with each other by construction, so agreement between them is not evidence. **The English text of the line is the evidence.** The `--stub` tell in §4 is the same lesson in a different dress.

✅ **THE BACKFILL IS DONE — 48 tagged or accounted for across 22 pages, 4 deliberate skips** (printed 155 ×2 and 243, where the band is at budget and the English line gives the situation outright; 321, a brace catalogue whose cells print their own references). The audit that reports them is — `python3.11 tools/audit_missing_books.py --tags` — untagged is not automatically wrong (§3, §8), so each was read before anything was written.

⚠⚠ **THREE `R:` NOTES WERE WRONG IN SUBSTANCE, not merely short a tag** — they had *enumerated* their pages out of the defective index. Printed 4 listed six places of prayer where the plate has seven (the garden); printed 14 listed the postures without the bowed head; **printed 154 claimed the Passion catalogue was drawn from five books, 'not one of them a Gospel narrative of it', when John xix is exactly that.** All three rewritten. **Where a note counts something, it counted what the tool showed it — so a tool fix means re-reading the prose, not just the tags.**

⚠ **A SEVENTH gap, found at printed 326:** a one-chapter book is cited by verse alone and `REF` demanded a roman chapter, so five Jude references were invisible. **`*Jud.*` is two books here** — Judges with a roman chapter, Jude with a bare verse.

⚠ **`*Ez.*` is a trap.** At printed 15 it is **Ezra** ix. 6 — *I am ashamed and blush to lift up my face* — not Ezekiel: the volume prints the same verse as `*Ezr.* ix. 6, 7` at printed 171, and Brightman tags the sentence *Of Ezra*. At printed 78 and 84 the same contraction **is** Ezekiel. Expand it from the sense every time, never from the letter.

## 2. The working loop, in order

```
python3.11 tools/check_lineparity.py            # is this page safe to key by line?
python3.11 tools/note_sheet.py 324              # refs by PLATE line + English NUMBERED
#   ... write S:/R: entries into apparatus/print-notes.md ...
python3.11 tools/check_notes.py 324 330         # order (ERROR) · numbering · coverage
python3.11 tools/transcript2tex.py
cd prototypes && xelatex volume-loeb.tex && xelatex volume-loeb.tex   # TWICE
python3.11 tools/transcript2tex.py --fit
```

⚠⚠ **`--fit` reads a file only XELATEX writes.** Running it straight after `transcript2tex.py` reports the *previous* run — it will show a page you just trimmed as still too tall, and, far worse, a page you just filled as still fitting. **Always xelatex between the build and the measurement.**

⚠ **A page over its leaf is trimmed before the commit, never left.** Only one page has ever needed it (printed 312); tighten the `R:` prose, never drop a finding.

**Commit shape:** content commit, then update `next-session-resume.md` as the last commit of the session. **No push** — protected, needs Wilson's per-action OK.

---

## 3. The four rules that actually decide what you write

**a. The brace catalogue takes `R:` notes and NO scripture band.** (NOTES-CONVENTIONS §3.) Where the plate sets `{ a, [ref] / b, [ref] }` it prints its own reference inside each cell and our English keeps it there, so a tag repeats the page on the same line. Printed 306 carries twelve references on four sense-lines. **Write notes, leave the band empty, and say so in the section's first note so the empty foot reads as a decision.** What those leaves need is the technical vocabulary opened — *exinanitio* = κένωσις, *apprehensio seminis Abraham*, *œconomia*, *Therapeutæ* (Philo's Egyptian contemplatives, not physicians), *propitiatorium* = the mercy seat.

**b. On a dense page, SELECT.** (§8.) Printed 320 has 25 references — the most in the book — and took **seven** tags. 323 has 20 and took ten. §3's *don't tag what the line above already gives* does most of the work: these catalogues name their own people and print their own references. **The band is not obliged to fill the leaf.**

**c. An `S:` tag prints the PLATE's chapter-and-verse, always.** (§6, ruled by Wilson 2026-08-10.) Differences go in the tag's clause, never its figure — plate right on another numbering → name the system; plate misprinted → name the true verse; the editor's bracketed slip → keep his brackets and let the `R:` note say whose it is; **not certain which → give the substance and claim nothing.** That last row is the one to reach for.

**d. Never write back to a transcript.** Ever. Separate, argued, Wilson-level decision.

---

## 4. Per-page hazards in what remains — check these lists before keying

**⚠ Parity-mismatched, so `check_notes` CANNOT compare them and `--stub`'s figures are wrong:**
`365 · 370 · 380 · 381 · 386 · 388 · 406 · 425 · 431`

Use `tools/note_sheet.py` and hand-map. **The tell, which found three broken pages in the audited twenty: on a parity-mismatched page, a tag line that EQUALS the plate's line was probably keyed off `--stub` and never hand-mapped.** Not proof — read the English. `tools/audit_unsafe_pages.py <page>` prints tag line, plate line, and the English at both.

**⚠ Marked in more than one section (the builder concatenates both blocks into one fragment):**
`324 · 326 · 327 · 331 · 339 · 345 · 348 · 350 · 354 · 356 · 357 · 359 · 360 · 363 · 364 · 365 · 369 · 370 · 372 · 379 · 380 · 381 · 384 · 387 · 391 · 395 · 406 · 416 · 425 · 431`

`ref_index` and `note_sheet` are both fixed to number continuously across the page. **Nothing to do — but if a page's English looks short, suspect this first.**

**⚠ Over the 14-reference budget — select:**
`330:21 · 327:21 · 406:20 · 357:20 · 331:18 · 367:16 · 328:16 · 408:15 · 342:15 · 338:15`

**⚠ Prose pages, which cannot take line-keyed notes at all** (370, 380, 381): write page-level `R:` notes with no leading figure. Printed 370 is 26 lines of Latin against 3 of English.

---

## 5. What to watch for — the patterns this pass has established

These recur, and each is a thing a careless pass destroys.

1. **Second registers.** The 1853 runs extra columns that are not part of the line beside them: *Shame · Pain* at 313, *Shadow · Dove · Breath · Fiery tongues* at 316–317, Latin-glossing-Latin at 318, order-against-gift at 304, the cross-column asterisks at 389/390. **They are structural and must survive into both layers.**

2. **A text used twice and never for the same thing.** Four instances so far — Mark iv. 38 (286 vs 294), the insults (307 vs 309), Paul's four dimensions (315 measures the wound, 319 measures mercy), Ps. lxxxix. 47 (34, 295, 322). **Never conform or cross-refer the two places in the text.**

3. **Recension parallels.** Part III is the Harley recension of Part II's penitential matter (§1↔§23+§38, §2↔§17, §4↔§24) — **and printed 312 is a recension of printed 154**, the first Part I ↔ Part II case, identical Latin under a different grammar. **Identical Latin gets identical English; divergences stand and are flagged.**

4. **The volume corroborating its own misprints.** Four cases: `Job xiv. 4` at 323 against 406's `xiv. 14`; `Psal. cxxx. 3` at 297 against 40's `cxxx. 30`; `Is. xxxviii. 15` in §37 against Part III's `xxxiii. 15`; printed 25 confirming the reading at 409. **The corroborating witness is the book, which beats any conjecture — expect more of these in Part III, which is where several of the errors live.**

5. ⚠⚠ **THE INDICATIVE TURNED IMPERATIVE — the method, established 2026-08-10 and now the single most useful thing to read a leaf with.** Andrewes builds petitions by taking the record of what God **has done** and asking it back as a command. Nathan's *the LORD hath put away thy sin* prayed as *Transfer*; Hezekiah's *thou hast cast all my sins behind thy back* as *Dissipa*; the psalm's *thou hast covered all their sin* as *Tege*; the Baptist's participle **ὁ αἴρων** as the bare imperative **αἶρε**.
   - **The volume proves it on one verse**: Isaiah xliv. 22 stands at printed 22 as *Dele … blot thou out MINE* and at printed 332 in God's own indicative, *I blot out … thine iniquities*. Same verse, both ways, neither place noting the other.
   - **And once in the Greek itself**: Matthew's *οὐ κατεάξει*, he shall not break, is printed at 334 as *μὴ κατεάξῃς*, break thou not.
   - The relatives of it are everywhere — a text spoken **outward** taken **inward** (Stephen's prayer for other men at 327; Paul's oath about his kinsmen at 335), a promise **borrowed** rather than argued from (321, 22). **When a leaf quotes a promise, always check the mood and the person before writing the tag.**

6. **Greek that cannot be flattened.** 319's ladder of ὑπερ- compounds is the clearest case in Part II for the whole edition. Also Ἐπίκλησις/Παράκλησις at 317, Χρηστός at 302, ῥαπίσματι at 311, ἄλλος at 290, and ⚠ **Ἄγνωστοι βάσανοι at 314 — the one item in a forty-item catalogue with no proof-text, and the blank is the point.**

7. **The Psalter is not one Psalter.** Proved twice from inside single texts: `xxii. 17`/`xxii. 16` (154 vs 312) and `xxxix. 14`/`xxxix. 12` (261 vs 322), plus `cxvii. 25` (Vulgate, 274) against `cxvii. 2` (AV, 300) and 295's AV-numbered `lxxviii. 39`. **An introduction claiming a single Psalter throughout is answerable for these pages.**

---

## 6. After the notes pass

The pre-print list is an **images** problem, not a collation one — printed 210 · 239 · 386's garbled Hebrew · 414's cento · `p. 207` · 370/371's missing heading, four of six blocked on a non-Google 600-dpi digitization. Brightman by text is near exhausted.

**Owed by Wilson:** a push (`git push origin main`, protected); a non-Google digitization; and the preface (`prototypes/front/preface.tex`), which is still a draft in my words and is blocked on his voice, not on research.

Related: `NOTES-CONVENTIONS.md` · `CONVENTIONS.md` · `EDITION-SHAPE.md` · `apparatus/print-notes.md` · `next-session-resume.md`
