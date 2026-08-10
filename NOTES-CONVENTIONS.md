# Notes conventions — the two foot-bands

**Frozen 2026-08-10. This file governs every note written into `apparatus/print-notes.md`.** It is to the notes what `CONVENTIONS.md` is to the transcription and the English: sessions follow it, they do not re-derive it. If a rule here turns out to be wrong, change it *here first*, in its own commit, and say what changed — do not let one page drift from it.

Read with: `CONVENTIONS.md` (§9 especially) · `apparatus/CLASS-A-ledger.md` · `apparatus/BRIGHTMAN-collation.md` §3b · `EDITION-SHAPE.md`.

---

## 1. The three streams, and what each is for

`apparatus/print-notes.md` is keyed by printed page. Each entry is one line, prefixed by its stream:

| stream | foot | register | what it carries |
|---|---|---|---|
| `V:` | **verso**, under the originals | terse, sigla, Latin conventions | apparatus criticus — class A (the Wright apograph), class B (Andrewes' spacing), class C (Drake), and plate defects |
| `S:` | **recto**, under the English | one clause, run-in | what a scripture reference *is* — whose words, in what situation |
| `R:` | **recto**, under the English | full sentences, paragraph | the explanatory note — what a reader needs that the page cannot show |

⚠ **`V:` can only exist for printed 2–250.** The apograph runs *usque ad pag. 250*, so Parts II–III have no manuscript witness; their verso foot carries plate defects or nothing at all. **An empty band is a correct outcome.** Apparatus is dense where a text is contested and silent where it is not, and a book that carries a note on every leaf is padding.

## 2. The anchoring system — two devices, two alphabets

- **The margin carries ARABIC figures every five sense-lines.** This is the *ruler*, and it is also the 1853's own `PAGE. LINE` coordinate — the form `CLASS-A-ledger.md` is written in, and the form the 1853's apparatus has always cited. **Our sense-line count IS its line count**; verified at printed 34, where `Τὰ ἔργα τῶν χειρῶν σου μὴ παρίδῃς` is line 27 exactly as class A says.
- **The line-end carries a ROMAN superscript.** This is the *anchor*: it says "there is a note on me" at the place the eye already is, and it is repeated at the head of its entry in the band below. Roman against arabic so the two can never be read as one series.

**Every entry begins with its sense-line number.** The builder strips it from the scripture band (the margin already gives the arabic) and keeps it in the apparatus (which must stay checkable against the ledger).

Rules that follow, and they are not negotiable because the reader's trust in the marker is all that makes the band usable:

1. **One marker per LINE, not per entry.** A line with two references gets one roman, and the band gathers what that line carries.
2. **One marker series per leaf, across `S:` and `R:` together.** A line carrying both a tag and a note gets one roman meaning the same thing in both registers. Numbering the streams separately would put two different **i**'s on one page.
3. **Never invent a line number.** Take it from `python3.11 tools/ref_index.py <page>`. A note pointing at the wrong line is worse than no note.
4. **An `R:` note about the PAGE rather than a line is written without a leading figure** and set without a marker. There is no line to send the reader to, and manufacturing one misstates where the comment belongs.
5. ⚠⚠ **THE THREE COLUMNS DO NOT SHARE ONE NUMBERING. Each column is numbered on its own count.** An earlier draft of this file said the opposite, on the strength of one verified page; `tools/check_lineparity.py` disproved it. **The Latin recto is line-for-line with its Greek verso in 111 of Part I's 131 openings and NOT in 20** — the plate turns its own long lines and the Latin is the wordier column, so it can run five or six lines longer (printed 48/49, 62/63, 142/143 all +5 or +6). One set of figures would have named the wrong Latin line on one opening in seven, and **nothing on the page would have shown it.**
   - The **marker series still runs continuously across the leaf** — the Greek's noted lines take i…k, the Latin's take k+1…m — so a roman is unique on a page and the band needs no column label.
   - A `V:` entry is filed under **the printed page it belongs to**: an entry under an odd page is a Latin-recto entry and is numbered on the Latin's own lines.
6. ⚠ **In Part I the references are printed on the LATIN recto and the `S:` note goes on the ENGLISH recto of the same opening.** That is sound where the columns agree, but **run `check_lineparity.py` and consult its list before keying notes on any page in it**. English-vs-original mismatches at printed **1 · 12 · 18 · 62 · 68 · 196 · 238 · 246 · 286 · 288 · 289 · 308 · 370 · 380 · 381 · 386 · 388**.
7. ⚠ **A PROSE page cannot take line-keyed notes at all.** Where the 1853 sets continuous prose the English cannot be line-keyed and is not — printed **370** is 26 lines of Latin against 3 of English (Bradwardine), 380 and 381 likewise. On those pages write **page-level `R:` notes without a leading figure**; they are set without a marker, which is correct.

## 3. `S:` — the scripture tags

**1,954 references on 250 printed pages** (`tools/ref_index.py --all`), median 7 a page.

### What a tag says
**The situation, not the text.** The *Preces* is a cento: its text already *is* scripture, and our English already translates it. Printing the Authorised Version beside it puts two English renderings of the same words on one leaf. What a reader cannot get from the page is *what the verse was doing where Andrewes found it*.

This follows the author's own practice. At printed 425 his catena tags each text with whose blessing it is — *(of Jethro)*, *(of Moses and the Israelites)*.

> `S: 9 Dan. ix. 7 — Daniel in the exile, at the evening sacrifice`
> `S: 13 Neh. ix. 33 — the Levites' confession, while the Law is read`
> `S: 20 Ps. lxxxix. 46 — Ethan: how short a time God has made men for`

### Form
- **One clause. No verb of its own where a phrase will do.** Ten words is comfortable; twenty is over.
- Speaker, then situation: *who is saying this, at what moment*.
- Where the situation is the whole point, quote the few words that make it, in italic: *thou hast destroyed thyself*.
- No "cf.", no "see", no cross-references between tags. A tag is a caption, not an argument. Arguments are `R:`.

### ⚠ The safety rule — this is the one that keeps errors out of a printed book
**If the speaker or the situation is not certain, give the verse's substance instead of a speaker.** A wrong attribution — David for Ethan, Bildad for Elihu — is a printed error in an edition that is otherwise scrupulous about never silently mending anything, and it looks perfectly plausible on the page. A bland true tag costs the reader nothing; a confident wrong one costs the edition its credit.

`S: 21 Ps. cxxxviii. 8 — *despise not the works of thine own hands*` is a perfectly good tag. It says what the verse is and claims nothing it cannot support.

### What NOT to tag
- ⚠⚠ **THE BRACE CATALOGUE — an `S:` band on these leaves is pure duplication.** From §10 (*Confessio Laudum*, printed 305) on, whole pages are single sentences governed by a standing *Pro*, set as `{ a, [ref] / b, [ref] / c, [ref] }` — **the plate prints its own reference inside each cell and our English keeps it there**, so a tag beneath repeats what the reader already has, on the same line. Printed 306 has four sense-lines carrying twelve references this way. **Write `R:` notes and leave the scripture band empty; that is the right outcome, not a gap.** What such a page actually needs is the technical vocabulary opened — *exinanitio* for κένωσις, *apprehensio seminis Abraham*, *œconomia*, *Therapeutæ* — which is `R:` work. Say so once in the first note of the section, so the empty foot reads as a decision.
- **A reference whose situation the line above already gives.** If the English says who is speaking, the tag is noise.
- **A repeat within the same page** — tag it once, at its first line; the second occurrence takes a marker only if something has changed (as at printed 34, where Ps. cxxxviii. 8 returns and the apparatus turns on the second one).
- **Anything requiring a guess about the 1853's numbering.** See §6.

## 4. `R:` — the explanatory notes

Fewer, longer, and they carry the edition's voice. Their material is the **translator's flags already written into the 109 English files** — 363 discrete bullets — plus the collation findings.

A note earns its place when it tells the reader something the facing page cannot:

- **A divergence the English Bible destroys.** The best kind, and the reason this stream exists. Printed 34: Andrewes answers *Substantia mea apud te est* and four lines later *Memorare quæ mea substantia* — both Vulgate, both turning on *substantia*, which is why the two psalms can be stacked. The AV renders one *my hope is in thee* and the other *remember how short my time is*, and the join disappears. **Our English keeps the pun because it translates his Latin.**
- **A reference kept as printed with the true verse named** — there are dozens. The note names what is at the cited place and what was meant. It never mends the plate.
- **A recension parallel** — Part III is the Harley recension of Part II's penitential matter. Say where the twin stands; never conform them.
- **An override of CONVENTIONS §9**, of which four are recorded.
- **A source identification**, with its authority named (§7).

## 5. When the KJV *does* get printed

Selectively, inside an `R:` note, and **only where Andrewes' text departs from the English Bible** — which is the case §9 already governs. Never as a systematic gloss.

⚠ **Brightman's margins mark `heb.` / `sept.` / `vulg.` wherever the original departs from the English Bible.** That is a ready-made index of exactly these places, compiled by someone who had the manuscripts. Use it to *find* the divergences; do not quote his English as ours.

## 6. ⚠ Psalm numbering — three systems, and they do not agree

The Psalter is a trap in this book and every note touching it must say which numbering it means.

- **CONVENTIONS §9 stands: crib against the Coverdale/BCP Psalter ahead of the AV**, because Coverdale worked through the Latin/LXX and so stands with Andrewes where the AV (from the Hebrew) diverges.
- **The BCP Psalter's verse numbers run ahead of the AV's in places.** Brightman numbers *"a wind that passeth away"* as Ps. lxxviii. **40** where the AV has **39** — in two margins and in his own printed psalm text.
- **The Vulgate's psalm numbers run one behind** the AV through most of the Psalter (Vulg. lxxvii = AV lxxviii).
- **Printed 433 gives two references that are right only on the Prayer Book's numbering** (`xlii. 10`, `lxv. 8`) — the first hard evidence that the BCP was the book physically to hand.

**So: name the system whenever it could be read two ways**, and never "correct" a reference into agreement with a numbering the plate was not using.

### ✅✅ RULED BY WILSON 2026-08-10 — **an `S:` tag prints the PLATE's chapter-and-verse, always**

The tag is a **caption on the reference the plate prints**, so it cites what the plate cites. Where the two would differ, the difference goes into the tag's own clause — never into its figure.

| what is true | how the tag reads |
|---|---|
| plate right on another numbering | `Ps. xxxi. 6 — *O LORD God of truth*; Prayer Book numbering` |
| plate genuinely misprinted | `Ps. cxli. 8 — *keep the door of my lips*, which is verse 3` |
| the 1853 editor's bracketed slip | keep his brackets in the tag; the `R:` note says whose slip it is (printed 62) |
| **not certain which** | **give the substance and claim nothing** — `Ps. xxxix. 14 — *I am a stranger with thee, and a sojourner*` |

That last row is §3's safety rule applied to numbering, and it is the one to reach for. A wrong claim about *which Psalter the 1853 was counting from* is exactly the plausible-looking printed error this edition cannot afford.

**Why this way.** The discipline everywhere else in the edition is that wrong references and printing defects are kept as printed, flagged, never silently mended — `[Jer. l. 24.]`, `[Dan. vi. 4.]`, `Job. xiv. 14.`, the *Isaac* crux at 425 all stand. The tags were the one place in the book that quietly emended, and they did it in the register a reader trusts most, because a caption does not look like an argument. And the reader sees both figures on one opening: plate `Psal. xxxi. 6.` on the verso, band `Ps. xxxi. 5` below. Nothing explained the gap, so it read as an error in *our* work — worst of all in that case, where the 1853 is right and we introduced the discrepancy.

⚠ **Applied 2026-08-10 to all 20 surviving cases; `check_notes.py` reports 0.** Nine were the Prayer Book's numbering and the tag had converted it to the AV's. One was the **Vulgate's**, and it is the sharpest: printed 274's Hosanna is `Ps. cxvii. 25`, Vulgate for the AV's cxviii — given §9's whole argument about which Psalter Andrewes had to hand, silently normalising his psalm numbers is the specific thing this edition should least want to do.

⚠ **The checker cannot see a page whose columns are on different line counts** — 20 of them, listed in its own output. Those tags have never been compared with the plate at all.

### (superseded — the question as it stood before the ruling)

`tools/check_notes.py` reports **50 places on 34 pages where a tag's chapter-and-verse disagrees with the reference printed above it**, and a reader of the finished book sees both. Three quite different things are mixed together there and the pass has been treating them alike:

1. **The plate is RIGHT on the Prayer Book's numbering** and the tag silently converted it to the AV's — printed 26 tags `Ps. xxxi. 5` where the plate prints `Psal. xxxi. 6`, and BCP verse 6 *is* `Into thy hands I commend my spirit`. §6 above forbids exactly this.
2. **The plate is genuinely misprinted** — printed 26 also tags `Ps. cxli. 3` against the plate's `cxli. 8`, and *keep the door of my lips* is verse 3 in AV, BCP and Vulgate alike. Here the tag is right, but §7.1 says the note may not be *phrased as a correction of the page*: the true verse gets **named**, in the open.
3. **The reference is the 1853 EDITOR's**, in his brackets, and the slip is his — the `[1 Cor. viii. 12]` → 2 Cor. at printed 62, which is already handled properly, with brackets kept and an `R:` note that says whose slip it is.

**Twelve of the fifty cite a book/chapter that is not on the page at all**, which is a different and larger claim than a verse being off by one.

The question for Wilson is one sentence: **does an `S:` tag print the plate's figure, or the true one?** Whichever way it goes, the other two classes still need their `R:` note, and nothing may be auto-fixed from the checker's output. **Until it is ruled, new tags carry the PLATE's figure and name the system** — which is what printed 286's `Ps. cxxvii. 3` does.

## 7. The never-rules

1. **No note is ever a repair.** The plate stands as printed above, always. An apparatus entry records what another witness reads; a note records what the reader needs. Neither may be phrased as a correction *of the page*.
2. **Nothing here writes back to a transcript.** Ever. That is a separate, argued, Wilson-level decision.
3. **Never import a Brightman heading as recovered text** — preface §3, *"For titles, etc., which are printed in thick type… I am responsible."* They are his.
4. **Name what is owed to a witness.** Identifications from Brightman are named as his, the way `prototypes/back/sources.tex` already does. Three kinds of attribution are not of equal weight and the notes keep them apart: printed in the 1853 plate · supplied by the 1853 editor (his brackets) · owed to Brightman.
5. **An over-reaching attribution is flagged, never trimmed to fit** — the §39 Fulgentius rule.
6. ⚠ **All Hebrew must be re-read at 600 dpi before it is set.** Look-alike sorts (ד/ר, ב/כ, ה/ח) are not separable at 200 dpi, and every Hebrew form we have is a 200-dpi reading.

## 8. The budget, and how to stay inside it

**Measured ceiling: about twelve `S:` tags plus two `R:` notes fills a leaf.** Printed 34 overran twice while this was being built — 538pt, then 540pt, against 531pt available — and both times trimming a handful of tags by a few words fixed it. Treat **twelve** as the working budget, not fourteen.

**34 of the 250 referenced pages carry more than fourteen references** (worst: printed 320 with 24, 309 with 23, 43/321/322 with 22). On those pages **select**; do not squeeze. Order of preference for what gets a tag:

1. a reference the plate gets **wrong** (the note names the true verse);
2. one whose situation is **not** recoverable from the line above;
3. one that carries a **divergence** worth an `R:` note;
4. first occurrences over repeats.

**And 180 pages carry ten or fewer, with room to spare.** The band is not obliged to fill the leaf.

## 9. The working loop

```
python3.11 tools/check_lineparity.py        # ⚠ FIRST: is this page safe to key by line?
python3.11 tools/note_sheet.py 286          # the worksheet: refs BY PLATE LINE + the
                                            #   English NUMBERED. On a page the parity
                                            #   check flagged, this is the hand-map —
                                            #   key to the English figures, not the stub's.
python3.11 tools/ref_index.py --stub 35     # scaffold: line numbers + refs, ready to fill
#   ... write one clause per reference into apparatus/print-notes.md ...
python3.11 tools/check_notes.py 286 290     # ⚠ order (ERROR) · numbering · coverage
python3.11 tools/transcript2tex.py --part 1
cd prototypes && xelatex part1-loeb.tex && xelatex part1-loeb.tex   # twice, for the contents
python3.11 tools/transcript2tex.py --fit 1  # ⚠ --fit alone reads the WHOLE-VOLUME record
```

⚠ **`--fit` is not optional.** The band is measured *into* the fit record, so an overrun is named; it is not visible any other way, because a box that overruns does so in silence. **A page that reports too tall is trimmed before the commit, never left.**

⚠⚠ **`--fit` READS A FILE THAT ONLY XELATEX WRITES.** The Python build regenerates the TeX and the fragments; the `.fit` record is written during the LaTeX run. So `transcript2tex.py` followed straight by `--fit` **reports the PREVIOUS run's measurements** and will show a page you have just trimmed as still too tall — or, far worse, show a page you have just filled as still fitting. **Always xelatex (twice) between the build and the measurement.**

⚠ **`--fit` with no argument reads `volume-loeb.fit`.** After a `--part 1` build you must say `--fit 1` or you are reading a stale file and will believe a page fits when it does not.

## 10. Model and scope

Per [[reference_model-prudence-rubric]]: this file is the **score**; the volume run **plays** it.

- **This conventions file** — governing, compounding, written once.
- **The ~1,954 tags — Opus.** Rule 4: volume editorial passes are Opus-at-best, never Fable; and Sonnet's tier is explicitly *formatting/markup cleanup, NOT content*. The failure mode here is **factual, not stylistic** — a wrong speaker is a printed error that looks plausible — which is what §3's safety rule exists to blunt.
  ⚠ The Christian Library precedent (Scripture-index fleet on Sonnet) does **not** transfer: the mechanical half of that job is the half `tools/ref_index.py` already does in code, with no model at all. What remains is judgment.
- **`R:` notes and divergence findings — Opus**, always.
- **Run a section at a time.** Pilot, measure real cost and a spot-checked error rate, then extrapolate. Per [[feedback_christian-library-iterate-vol1-first]].

## 11. ⚠⚠ The index does not know what it cannot see — sweep before opening a new stretch

`tools/ref_index.py` finds references by matching a **fixed list of book abbreviations**. A form the 1853 uses and the list omits does not raise anything: the reference never enters the index, `--stub` never offers it, `note_sheet.py` never prints it, `check_notes.py` never misses it, and **the finished leaf carries a band that looks complete**. There is no place in the pipeline where the absence shows.

This has now happened **six times**. Printed 290 offered three of the Spirit's four titles because `*Ephes.*` was absent. Printed 324 lost *Et hæc omnia vidisti* — the fourteenth and last term of the confession — because `*Thren.*` was.

**Run `python3.11 tools/audit_missing_books.py` before opening a new part or section.** It reports every italicised token followed by a roman numeral that the current list does not match, and each is a decision: a missing book goes into `BOOK` (**the long form before its short form**), a false positive stays out and is named in the comment there. `*Servitus.*` (a heading at printed 331) and `*sec.* LXX` are false positives and must stay out.

The 2026-08-10 sweep, run at printed 324, found **71 invisible references under nineteen missing forms** — the Vulgate's `Joan` `Thren` `Ezech` `Mich` `Abac` `Judic` `Paralip`/`Paral` `Syr`, the contracted `Es` (Esaias) and `Ez` (Ezekiel), and the plain English `Isa` `Josh` `Amos` `Zech` `Chron` `Nehem` `Eccles` `Ezr`. **Fifty-two of them stood on pages whose notes were already written and committed.**

⚠ **Two of those forms are contractions that look like other books, and both were verified against every occurrence before being added:** `Es.` is **Esaias**, not Esther or Esdras (lxiv. 5 · vi. 3 · xxx. 15 · li. 5 · lvii. 11 · l. 4), and `Ez.` is **Ezekiel**, not Ezra (ix. 6 · xviii. 23 · xxxiii. 11) — the volume writes Ezra `Ezr.` A guess here would have put a wrong book on a printed page.

`--tags` runs the backfill audit: the recovered forms against the bands already written. ⚠ **Untagged is not the same as wrong** — §3 forbids tagging what the line above already gives and §8 requires selection on a dense page, so every hit is read before anything is written.

⚠ **Part I is keyed by the OPENING.** References print on the Latin recto (odd) and the band files under the Greek verso's even number, so an audit that looks up an odd page directly finds an empty band and reports every Latin recto in Part I as untagged. The tool handles this; a hand-written check must too.

Related: `CONVENTIONS.md` · `apparatus/print-notes.md` · `tools/ref_index.py` · `tools/audit_missing_books.py`
