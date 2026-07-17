# Next session — resume note

**Current front: PART II IN PROGRESS. §§1–6 COMPLETE both layers (printed 267–290).** Part I is complete end-to-end (printed 1–263). Part II sections done in `part2/`, each transcript + line-keyed English, self-checked parity:
- **§1 `01-duo-in-me-cognosco`** (267–269) — Latin-only opening penitential prayer, parity 3/3.
- **§2 `02-preces-matutinae`** (270–272) — Latin-only morning-prayer psalm-catena, parity 3/3.
- **§3 `03-intercessio`** (273–275top) — FOUR scripts (Latin body, Hebrew Hosanna הושיעה נא/הצליחה נא Ps 118:25, sustained Greek King-block, inline ortho- Greek pun), parity 3/3.
- **§4 `04-gratiarum-actio`** (275–279) — Latin-only thanksgiving scripture-catena, lettered ᵃᵇᶜᵈ footnote apparatus on 279, parity 5/5.
- **§5 `05-deprecatio`** (280–285) — Latin-only deprecation litany, the most brace/column-heavy yet (nested braces, 2-/3-col antithetical tables, armour-of-God catalogue), parity 6/6.
- **§6 `06-sacrificium-vespertinum-horologium`** (286–290) — Latin-only evening sacrifice + the Hours; canonical-hours litany keyed to Gospel events, *Et serva nos* refrain; Emmaus close + Trinity-works brace + Spirit's four titles (inline Greek ἄλλος), parity 5/5.

**NEXT = §7 Allegatio (pleading — *Ex parte Dei / nostra / consequentis mali & boni*, I–VI), printed 291–298 = PDF 314–321.** Then Confessio Laudis (299–302), Confessio + Confessio Laudum (303–308), etc. — work down STRUCTURE.md §PARS SECUNDA. NB the map marks 299 onward as "La+Gk" — watch for sustained Greek (translate it) vs inline glosses (keep apposed).

## NEXT ACTION

**Offset is stable +23** through the whole main body (verified this session at 274/276/278/280/286). Extract with `pdftoppm -jpeg -r 200 -f 314 -l NNN raw/preces1853.pdf raw/end/p`; **printed 291 = PDF 314**. Re-verify the printed page number by eye every batch (dups resume ~368). Continue the `part2/NN-slug-transcript.md` + `-english.md` file pattern; match the §1–6 files exactly (header para + `<!-- printed N (PDF M) -->` markers + `## Translator's flags`).

### Part II entry (historical note — DONE)

> **printed 267 = PDF 288** — incipit *DUO in me cognosco…* — Latin-only, offset **+21** at entry, drifting to **+23** by printed 272 across the 270–271 duplicate spread (PDF 293–294 re-scan 270–271).

### Phase 0 — section mapping — ✅ DONE (2026-07-17, Opus 4.8 recon pass)

The full Part II + III section map, offset-anchor table, and layer-per-section are now in **`STRUCTURE.md` §PARS SECUNDA & TERTIA** (verified by eye). Read that FIRST — it is the score. Headlines:
- Part II (printed 267–~397) = a second, largely **Latin** daily-office cycle + long penitential cycle, then a **bilingual (Gk+La)** eucharistic/hymns/poems finale. **Layer is not uniform — the map marks La / La+Gk / Greek / Gk-verso-La-recto per section.**
- Offset is **stable +23** through the whole main body (267–367), then climbs erratically (+25→+37→+43) through a **duplicate-riddled tail** (368–429). Verify every leaf by eye from 368 on.
- Part III (PARS TERTIA, PDF 438+) = Confessio Fidei / Creed prose, Latin. Primary text ends ~printed 430 (~PDF 481); **Variae Lectiones apparatus starts PDF 482** (separate final pass, not primary translation).
- Two earlier notes were WRONG and are corrected in STRUCTURE: the "Stokes Praefatio 372–387" and "Part III = Harley poems."

### Then, per-section transcription (start here next session)

1. **Start at printed 267 = PDF 288** (first section: *Duo in me cognosco*, Latin, printed 267–269). Work section-by-section down the STRUCTURE map; one `part2/NN-slug` file pair per section (or per few short sections). Extract with `pdftoppm -jpeg -r 200 -f 288 -l NNN raw/preces1853.pdf raw/end/p`. Skip PDF 283–287 (blank + the twice-scanned PARS SECUNDA title = printed 264–266, no prayer text; capture the divisional title once as a section marker if wanted). See STRUCTURE.md anchor table for the whole boundary.
2. **Part II is LATIN-ONLY at the opening — translate the Latin (CONVENTIONS §6), not the Greek.** There is no facing Greek here; the even/odd Greek-verso/Latin-recto rule of Part I does NOT apply. Later stretches may go parallel again — check every page which layer(s) it carries before translating. Heavy nested `{ }` brace catalogues (both left- and right-joining) start immediately (see PDF 288–289).
3. **File naming for Part II — create a `part2/` dir** (parallels `part1/`); name files by section, `part2/NN-<slug>-transcript.md` + `part2/NN-<slug>-english.md`, starting `part2/01-duo-in-me-cognosco-transcript.md`. Match the Day-1 file format (frontmatter + page-marker comments + `## Translator's flags`). Part II's internal section boundaries aren't mapped yet — segment at the 1853 typographic breaks (large blank + caps incipit) as you go, cross-checking STRUCTURE.md §PARS SECUNDA.
4. **Offset keeps drifting** past +21 later (printed 297 = PDF 320 → +23; printed 393 = PDF 430 → +37, the poems). **Re-verify the printed page number by eye at every batch.**
5. **CONVENTIONS §9 Psalter rule (added this session):** for psalm-lines crib against the **Coverdale/BCP Psalter** ahead of the AV — it stands with Andrewes' LXX where the AV (from the Hebrew) diverges. Worked LXX-vs-AV cases in `evening-english.md` / `meditations-english.md` flags (Ps 19:13, 38:7, 91:6, 4:8, 89:47; Job 5:1, 14:1).

## Watch items (source defects — restore from a non-Google digitization before print)

- **Printed 239 (Latin)** — the Google scan photographed the whole spread 238+239 in one frame (PDF 258); the Latin recto (239) is CUT OFF past the first ~15 chars of each line. Transcribed with `[?]`; needs a clean scan. This is where the offset dropped +20→+19.
- **Printed 210 (Greek)** — left-margin ink damage in the Google scan (`deprecation-transcript.md`); Latin 211 has the construal.
- Minor per-scan accent calls flagged inline in `meditations-transcript.md` (Rom. vii. 24 articles on 252; αὐτοκατάκριτον smudge on 258; "Διοτιοῦν" one-word on 262). Recheck on a cleaner scan.

## State (2026-07-17)

- **PART I COMPLETE — transcription AND English, all self-checks pass.** Days 1–7 (30–197), front (1–29), post-days deprecation+Hosannas (198–219), Evening Office (220–251), Meditations I–II (252–263).
- **English done: ALL of Part I** — Days 1–7, front, deprecation block, Evening Office (parity 16/16), Meditations I–II (parity 6/6). Nothing in Part I outstanding.
- Offset history: +18 (front, ≤43), +20 (44–238), **+19 (240–263, after the photographed spread 238/239)**. See STRUCTURE.md anchor table.
- **Print pipeline still Day-1-only** (`tools/transcript2tex.py` hardcodes pp.30–43). Generalizing it (page-range args, ` | ` table + `{` brace rendering, page-fit for the fragile mirror) is deferred M-print work.
- Repo is LOCAL ONLY (no GitHub remote — protected action, Wilson's call).
- Remaining after Part I English: Part II (~264–400, Latin-only stretches), Part III (~401–460, Harley 6616 poems), appendix + Variae Lectiones pass. See M3-HANDOFF.md §Scope and STRUCTURE.md.

## Session log (recent)

- 2026-07-17 (Opus 4.8, Part II cont.): **Added §6 Sacrificium Vespertinum + Horologium** (printed 286–290), both layers, parity 5/5 — the canonical-hours litany (each hour→Gospel event, *Et serva nos* refrain), Emmaus close, Trinity-works brace, Spirit's four titles. §7 Allegatio opens printed 291 (PDF 314). NEXT = §7.
- 2026-07-17 (Opus 4.8, Part II cont.): **Added §5 Deprecatio** (*Ne perdas*, printed 280–285), both layers, parity 6/6 — the brace/column stress-test (nested braces, 2-/3-col antithetical tables, armour catalogue) all encoded. Verified §6 SACRIFICIUM VESPERTINUM opens printed 286 (PDF 309).
- 2026-07-17 (Opus 4.8, Part II start): **Part II §§1–4 COMPLETE both layers** (printed 267–279), new `part2/` dir. §1 Duo in me cognosco (267–269), §2 Preces Matutinæ (270–272), §3 Intercessio (273–275top, four scripts), §4 Gratiarum Actio (275–279). Verified entry offset +21 (267) → +23 (272) across the 270–271 dup spread (PDF 293–294); +23 stable thereafter (checked 274/276/278). Established Part II conventions in practice: Latin-only sections translate the Latin (§6); psalm-catenae cribbed from Coverdale/BCP (§9); inline Greek glosses kept apposed (§11/§17); sustained Greek/Hebrew blocks are main text and fully translated; lettered ᵃᵇᶜᵈ footnote apparatus preserved. NEXT = §5 Deprecatio (280–285 = PDF 303–308).
- 2026-07-17 (Opus 4.8, later): **Evening Office + both Meditations ENGLISH complete** — `evening-english.md` (parity 16/16) + `meditations-english.md` (parity 6/6). Part I English now finished end-to-end (printed 1–263). Added **CONVENTIONS §9 Psalter rule** (Coverdale/BCP Psalter as the first psalm-crib ahead of the AV; the BCP stands with Andrewes' LXX against the AV — worked cases in both files' flags). Rendered the communion devotions (238–248) in settled Divine-Liturgy English (Πρόσχες Κύριε, the anamnesis, Agnus Dei, Ἤνυσται καὶ τετέλεσται) + the Prayer-of-Humble-Access parallel at 238; Meditation II closes on Dan 9:19 verbatim. Local commit only. NEXT = Part II (printed 264→).
- 2026-07-17 (Opus 4.8, earlier): Evening Office transcript printed 220–251 COMPLETE both layers (parity 16/16). Discovered + flagged the photographed-spread anomaly at PDF 258 (238+239 in one frame; Latin 239 cut off; offset +20→+19). Encoded the big communion catalogues (Εἰς {…} / Ad {…}), the Luke-3 catechism with brace-joined addressees, the Righteousness/Mercies two-column offering. Then started `part1/meditations-transcript.md`: Meditation I (252–259, Day of Judgement) + Meditation II (260–263, Human Frailty) COMPLETE both layers (parity 6/6). Part I transcription now finished end-to-end. NEXT = Evening + Meditations ENGLISH, then Part II.

(Earlier session log preserved in git history; see prior resume notes and M3-HANDOFF.md.)
