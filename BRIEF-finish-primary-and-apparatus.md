# BRIEF — finish the primary text, then the apparatus pass

**Written 2026-08-03 for a session Wilson starts later.** Two deliverables, in this order. Everything needed to begin is in this file plus `next-session-resume.md`; **read `CLAUDE.md` and `CONVENTIONS.md` first as always**, then this.

**Model:** translation prose runs on **Opus** (`feedback_opus-for-authored-prose`). Deliverable 1 is authored prose and stays Opus. Deliverable 2 is collation, not prose — see its own note.

**Estimated size:** Deliverable 1 ≈ two sections, twelve printed pages — comparable to one of the 2026-08-03 sections. Deliverable 2 ≈ fourteen leaves of apparatus, but the output is a ledger, not a translation, so it is lighter per page. **Both together are a normal working session, not a fleet run** — no big-burn OK is owed unless the scope grows.

---

## DELIVERABLE 1 — §5 and §6, printed 431–436: the last of the primary text

Finish these and **the primary text of the entire volume is complete** (printed 1–263 · 267–395 · 398–436).

### §5 `MATUTINÆ PRECES` — printed 431–432 (PDF 474–475)
All-caps centred heading. The morning office as a psalm-catena in the reference-column manner. Opens *DOMINE, Tuus est dies, et Tua est nox, / Tu fabricatus es auroram et solem* (Ps. lxxiv. 6); runs through *Vespere, mane, et meridie, orabo* · *Benedictus es Tu, Domine, qui convertis in mane tenebras* · *Qui liberasti nos a terrore nocturno* · *Qui illuminasti oculos nostros, ne obdormiant in morte* · *Dele, Domine, ut nubem noctis iniquitates nostras* (Is. xliv. 22) · *Fac nos filios diei, et lucis* · *Da, ut caste ac sobrie ambulemus, sicut in die*; closes on a line tagged **`[Te Deum.]`** — *Dignare, Domine, nos hodie absque peccato custodire.* Printed 432 then gives *Serva nos a sagitta volante* · *Auditam fac mihi misericordiam Tuam* (Ps. cxliii. 8–12 entire) · *Respice in servos Tuos* · *Pone, Domine, custodiam ori meo* · *Sermo meus sit in gratia sale conspersus* · *Complaceant colloquia oris mei*, closing *Dominus custodiat exitum et introitum nostrum ex hoc et in sæculum.  Amen.*

⚠ **`[Te Deum.]` is the first non-scriptural source-tag the reference column has carried.** It is the editor's supplied tag, in brackets like the supplied scripture refs. Keep it as printed and do not expand it to a scripture reference.

### §6 `VESPERTINÆ PRECES` — printed 433–436 (PDF 478–481)
`AND. PRECES. — 3 K` at 433. The evening office. Opens *IN noctibus extollite manus vestras in sanctuario, et benedicite Domino* (Ps. cxxxiv. 3); runs through *Dirigatur oratio mea sicut incensum* · the *Benedictus Tu, Domine, / Qui creasti vices diei, et / noctis, et das lassis requiem* series · *Qui non præcidisti, quasi textor, vitam nostram* (Is. xxxviii. 14) · *Domine, sicut dies super dies, / peccata super peccata adjicimus.* **Ends the volume** at printed 436: *Stramentum vermium, / Operimentum pulveris. / In pace in idipsum dormiam et requiescam … **In manus Tuas, Domine, / Commendo spiritum / meum, quia Tu / redemisti me, / Domine Deus.***

⚠ **Printed 434 and 435 have NOT been read.** Read them before fixing the section's internal shape; everything above 433 and at 436 is eye-verified, the middle two leaves are not.

⚠ **Isaiah xxxviii — Hezekiah's psalm — appears here for the third time in the volume** (§37 at printed 372, Part III §2 at 409, and now *quasi textor* at 433). Worth a cross-reference note in all three; it is evidently a text Andrewes returned to, not a coincidence.

### Offset — it breaks a fifth time inside this stretch
| printed | PDF | offset |
|---|---|---|
| 431–432 | 474–475 | **+43** |
| 431–432 | 476–477 | — (**the spread is scanned TWICE**; both scans complete) |
| 433–436 | 478–481 | **+45** |

Printed 436 = PDF 481 is the last leaf of primary text, verified by eye. **Eye-verify every leaf anyway** — the tail has broken five times now.

### Discipline (unchanged)
Latin-only → translate the Latin (§6). Coverdale/BCP Psalter ahead of the AV (§9) — these two sections are almost entirely Psalter, so the crib does most of the work; flag any place the Latin departs from it. Reference column: **ref at line start = printed in the margin; ref trailing = printed inline.** Parity self-check with the awk one-liner used all session; **line-exact per page** is the standard these files have held to. One transcript + one english file per section in `part3/`, named `05-matutinae-preces-*` and `06-vespertinae-preces-*`. Commit each section separately, then update `next-session-resume.md` and `STRUCTURE.md` as the last commit.

---

## DELIVERABLE 2 — the *Variae Lectiones* apparatus pass

**PDF 482–491** = VARIÆ LECTIONES ET ADDENDA QUÆDAM, *ex apographo Samuelis Wright, apud Coll. Pemb. Cant. conservato*. **PDF 492–495** = *Notæ Marginales ex eodem MS* (the liturgies each prayer derives from — Chrysostom, Basil, St James). PDF 496 = library cover, book ends.

**This is NOT primary translation and must not be treated as it.** It is a collation ledger. The deliverable is a structured record, not a line-keyed English page.

### ⚠⚠ READ THIS BEFORE ANYTHING ELSE — the preface at PDF 482 states four things, and the first is load-bearing for the whole edition

The 1853 sets out its own principles on the apparatus title-page. Verbatim sense:

1. **`Hoc apographum Græca tantum continet usque ad pag. 250 nostræ editionis, sine versione Latina, quam Editor ipse confecisse videtur.`** — *The apograph contains only Greek as far as p. 250 of our edition, without the Latin version, which the Editor himself seems to have made.* **⚠ This says the Latin parallel column for printed 1–250 is not in the manuscript and appears to be an editor's work.** See "The Latin question" below — **do not act on it, surface it.**
2. **No titles in the apograph**, except `Ὡσαννὰ ἐν ὑψίστοις` (p. 208) and `Ὡσαννὰ ἐν ἐπιγείοις` (p. 214); `εἴσοδος` at p. 10 looks like an erratum. ⚠ **So the section titles we have been transcribing as headings are largely the printed edition's, not the MS's.**
3. **Distinct parts are marked in the apograph with GREEK letters** — α΄, β΄, γ΄ — **not Arabic numerals.** Bears directly on our numbered-article encoding.
4. **Each day is distinguished by its own astronomical sign** (planetary day-symbols).

Then the divergences are sorted into **three classes**, and the classes are the whole design of the pass:

- **A — *Variæ Lectiones quæ in textu ipso occurrunt, et idcirco pro veris sunt habendæ.*** Readings in the text itself, **to be held as the true ones.** Begins immediately (`p. 6. lin. 15. dele Μνήσθητι.` · `20. pro τοῦ ἁγίου φροντιστηρίου τούτου lege τῆς ἁγίας μονῆς ταύτης.`). **These are corrections to what we transcribed.**
- **B — *Intervalla sive spatia, quæ mentem auctoris sæpius indicant.*** The spacing record — **Andrewes' own unit grouping**, and exactly what `CONVENTIONS §13` said to cross-check unit boundaries against. **This is the highest-value class for the edition's structure.**
- **C — *Variæ Lectiones quas Ricardus Drake in ora libri exaravit*** — Drake's marginalia, made to bring the scripture citations closer to the received text. **A later hand with a normalising agenda. Class C is evidence about Drake, not about Andrewes** — never apply it to the text.

### What to produce
`part3/` is the wrong home for this. Make **`apparatus/`** with:
- `apparatus/variae-lectiones-transcript.md` — verbatim transcription of PDF 482–491, class by class, keeping the `p. N. lin. N.` addressing exactly as printed.
- `apparatus/notae-marginales-transcript.md` — PDF 492–495.
- **`apparatus/CLASS-A-ledger.md` — the one that matters most.** Every class-A reading resolved against our own files: printed page → our file and line → what we transcribed → what the apograph reads → **applied / not applied / cannot locate**. ⚠ **Do NOT silently edit the Part I/II transcripts.** The transcripts record the 1853 plate; class A records the manuscript behind it. They are two witnesses and the edition needs both. Any change to a transcript is a separate, argued commit — and probably a decision for Wilson, not for the session.
- `apparatus/CLASS-B-unit-boundaries.md` — the spacing record mapped onto our section/unit divisions, flagging every place where Andrewes' own grouping disagrees with the boundaries we chose (especially the ones recorded as *our* judgments: §28's, and Part III's §2/§3 cut).

### Model note for Deliverable 2
Collation is **not** authored prose. The transcription and ledger-building are mechanical enough that the Opus-for-prose rule does not compel Opus here — **but the class-B pass, where the MS's spacing is weighed against boundaries we chose, is judgment-dense and should stay on the strong model.** Split it if the session is long: transcribe A and C cheaply, weigh B carefully.

---

## ⚠ THE LATIN QUESTION — surface it, do not act on it

The apparatus preface says the Greek-only apograph lacks the Latin, *quam Editor ipse confecisse videtur* — "which the Editor himself seems to have made."

**Why this matters more than anything else in the apparatus.** The edition's print layout is **Prototype B, the 1675 mirror** — Greek verso, Latin recto, page for page — chosen by Wilson from three built prototypes, and the whole of Part I was translated on the standing rule that **the Greek is Andrewes' text and the Latin is the construal witness**. If the Latin of printed 1–250 is an editor's Latin rather than Andrewes' own, then for that stretch the mirror sets Andrewes beside his editor, and "construal witness" means something weaker than it has meant all along.

**What is genuinely uncertain, and must not be flattened:**
- **Which Editor?** The 1853 Parker text reprints the 1675 Sheldonian. *Editor* in that sentence most likely means the **1675** editor, not Parker's 1853 editor — but the sentence does not say so, and this file is not going to pretend it does.
- **`videtur`** — "seems." The 1853 is hedging, exactly as it hedged with *forsitan* in the §42 footnote (which we kept for that reason).
- **The scope is *usque ad pag. 250*** — printed 1–250 only. Part I runs to 263, so even on the strongest reading this does not touch printed 251–263, and it says nothing about Parts II and III, whose Latin is the primary text anyway.
- ⚠ **§42 is NOT evidence here, and an earlier draft of this brief wrongly said it was.** The two-recensions finding (the asterisk alignment rows on the Gloria) is at printed **388–391**, well outside the *usque ad pag. 250* scope. It tells us nothing about the Latin under discussion. Do not re-import it as a counter-argument.
- **On "which Editor": the sentence leans toward 1675.** It contrasts *pag. 250 **nostræ editionis*** with ***Editor ipse***. The 1853 says *nostra editio* when it means itself, so the unqualified contrasted *Editor* most naturally means the editor of the book being reprinted — the 1675 Sheldonian. Not proof, but the better reading, and it matters: a 1675 Oxford Latinist shared Andrewes' Vulgate, liturgical vocabulary and Latinity, and his version is the Latin every reader knew from 1675 to Brightman.

### ⚠ THE DECISIVE TEST — run it, it is nearly free
**Class A gives apograph-versus-printed Greek divergences for exactly this stretch (pp. 1–250). For each one, check which reading the facing LATIN supports.**
- If the Latin **consistently follows the printed Greek against the apograph** → it was made from the edited Greek, is downstream, and the question is **settled**: editor's Latin.
- If the Latin **ever supports the apograph against the printed Greek** → it has a source independent of the printed Greek, and the preface's *videtur* is too modest.

This costs almost nothing on top of the class-A ledger you are building anyway, and it can **close** the question rather than leaving it hedged forever. Record the result in `apparatus/THE-LATIN-QUESTION.md` as a table of test cases, not as a verdict paragraph.

**What the session should do:** transcribe the preface exactly, record the question in `apparatus/THE-LATIN-QUESTION.md`, **run the class-A test above**, and **stop there**. Do not revise CONVENTIONS §6, do not re-word any existing English, do not touch the Prototype B decision. **It is Wilson's call and it is an introduction-level question, not a translation-level one.**

**And note how little actually moves even on the strongest reading.** CONVENTIONS §6 already makes the Greek primary and the Latin *the first witness to construal* — a role a 1675 Latinist fills excellently, and one that never claimed independent textual authority. Prototype B reproduces **the 1675 book**, which is what it always claimed to do. The project's own framing already reads "Greek original, **historic Latin parallel**, fresh English translation," which is accurate under either answer. **The only thing that genuinely changes is the introduction** — and there it is an asset: an edition precise about its witnesses reads as more serious, not less. It also belongs on the pre-print verification list beside §39's Fulgentius attribution and the Hebrew at printed 386.

---

## Standing constraints for whoever runs this

- **No git push, no deploy.** ⚠ **CORRECTED 2026-08-03: the repo DOES have a remote** — `origin` → github.com/wilsonpruitt/andrewes-preces, current through `067e326`. This brief and several other files claimed it had "never had a remote," which was stale and wrong; the work is backed up off the machine. **Pushing is still protected** and needs Wilson's per-action OK. Commit locally, that is all. **Check `git remote -v` rather than believing any prose about it, including this line.**
- **Nothing here needs a big-burn OK** at the scope written above. If the scope grows — a full re-collation of Parts I–II against class A, say — stop and ask.
- **Wrong references, defective sorts and bad attributions stay as printed**, flagged in the translator's-flags, never silently mended. Part III alone added ten to the running list, and three times the volume proved its own misprint from its own pages.
- **Read one page past before closing any section.** It has now caught a wrong ending at both ends of this volume — Part II's real end at 395 (not "~397") and Part III's at 436 (not "~430").
- **The pre-print verification list** (needs a non-Google digitization): the garbled Hebrew at printed 386 · `Πᾶς` for `Πῶς` at 392, whose leaf has no duplicate · §39's Fulgentius attribution · `Tuâ` at 421 · `Cantemus Domino Isaac` at 425 · `fœcundi simus` against §23's `fervidus sum` · and now the Latin question above.
