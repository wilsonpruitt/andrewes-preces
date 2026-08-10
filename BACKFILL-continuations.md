# BACKFILL — the references `Vers.` and `Ibid.` hid

**Written 2026-08-10, the moment `ref_index` learned to resolve continuation references.**

⚠⚠ **This is a WORKLIST, not a defect list. Untagged is not automatically wrong** — §3's *don't tag what the
line above already gives* and §8's SELECT rule mean many of these are correct as they stand, especially on the
dense catalogue leaves (313 has eleven, and it is a Passion catalogue whose band deliberately selected seven).
**Read the page before writing anything**, exactly as with the `audit_missing_books` backfill.

⚠ **And where a note COUNTS something, re-read the prose, not just the tags.** That is how three `R:` notes were
found wrong in substance after the missing-books fix: they had enumerated their pages out of a defective index.

**135 newly-visible references on 62 pages already written.**

| page | n | references the index could not see |
|---|---|---|
| **10** | 2 | ps 119:133, ps 119:36 |
| **24** | 2 | ps 143:10, ps 143:9 |
| **26** | 1 | ps 143:11 |
| **28** | 1 | ps 86:17 |
| **42** | 2 | 1 cor 14:26, 1 pet 4:16 |
| **46** | 1 | 1 pet 3:3 |
| **52** | 2 | rev 2:5, rom 14:8 |
| **60** | 1 | mt 5:46 |
| **70** | 1 | gen 1:7 |
| **72** | 2 | mt 15:27, ps 13:2 |
| **92** | 1 | gen 1:11 |
| **104** | 2 | neh 9:30, ps 103:9 |
| **108** | 5 | jer 14:8, jer 14:9, rom 7:16, rom 7:18, rom 7:19 |
| **110** | 3 | rom 7:22, rom 7:23, rom 7:24 |
| **112** | 2 | ps 69:15, ps 69:16 |
| **116** | 1 | ps 65:12 |
| **132** | 5 | dan 9:16, dan 9:17, dan 9:18, dan 9:7, dan 9:8 |
| **134** | 4 | 1 jn 1:9, 1 jn 2:2, dan 9:19, ps 77:10 |
| **136** | 8 | mt 5:10, mt 5:12, mt 5:4, mt 5:5, mt 5:6, mt 5:7, mt 5:8, mt 5:9 |
| **148** | 1 | gen 1:28 |
| **152** | 2 | jon 2:4, jon 2:7 |
| **154** | 3 | lk 23:42, mt 27:30, mt 27:34 |
| **156** | 5 | ps 85:3, ps 85:4, ps 85:5, ps 85:6, ps 85:7 |
| **160** | 1 | ps 119:81 |
| **166** | 3 | rev 5:12, rev 5:13, rev 7:12 |
| **200** | 1 | mt 25:41 |
| **228** | 1 | ps 121:7 |
| **242** | 2 | jn 6:54, ps 116:18 |
| **260** | 1 | job 14:2 |
| **275** | 1 | ps 92:2 |
| **276** | 1 | ps 145:2 |
| **278** | 1 | ps 147:13 |
| **280** | 1 | mt 25:41 |
| **283** | 1 | jn 16:22 |
| **292** | 1 | heb 7:26 |
| **293** | 1 | ecclus 2:12 |
| **294** | 1 | 1 cor 6:19 |
| **295** | 2 | ps 103:15, ps 103:16 |
| **296** | 1 | mk 11:26 |
| **297** | 2 | ps 88:11, ps 88:12 |
| **298** | 1 | ps 79:13 |
| **300** | 1 | ps 139:8 |
| **301** | 1 | neh 9:31 |
| **305** | 6 | gen 1:11, gen 1:14, gen 1:20, gen 1:24, gen 1:28, gen 1:6 |
| **306** | 2 | lk 2:21, phil 2:8 |
| **307** | 1 | mt 4:2 |
| **309** | 1 | jn 19:17 |
| **310** | 7 | mt 26:33, mt 26:49, mt 26:55, mt 26:56, mt 26:70, mt 26:72, mt 26:74 |
| **311** | 4 | jn 19:17, lk 22:64, lk 23:11, mt 26:56 |
| **312** | 3 | lk 23:7, mt 27:30, mt 27:34 |
| **313** | 11 | jn 19:15, jn 19:16, jn 19:17, jn 19:29, mk 15:24, mk 15:29, mk 15:32, mt 27:28, mt 27:30, mt 27:31, mt 27:43 |
| **314** | 1 | jn 19:30 |
| **316** | 4 | 1 cor 15:6, gen 1:20, jn 20:26, lk 24:13 |
| **318** | 1 | eph 1:8 |
| **319** | 1 | ps 103:4 |
| **320** | 1 | lk 15:8 |
| **329** | 2 | 1 pet 4:2, ps 119:20 |
| **331** | 2 | lev 26:41, lev 26:42 |
| **332** | 3 | ps 103:10, ps 119:116, ps 78:39 |
| **335** | 1 | rom 9:2 |
| **342** | 1 | eph 1:14 |
| **344** | 1 | ps 89:17 |

## ⚠ Three that were resolving to the WRONG VERSE, not merely missing

Found 2026-08-10 while working the backfill: **`Ibid.` alone repeats the antecedent entire, but `Ibid. N` does not** —
it means the same book and chapter at verse N, exactly like `Vers.` The first version of the fix read the keyword and threw
the number away, so `Ibid. 5` (printed 53) resolved to Rev. ii. **1**, and `Ibid. 36` / `Ibid. 133` (printed 11) both
resolved to Psal. cxix. **18**. **They looked perfectly resolved.** Multi-verse forms — `*Vers.* 55, 56`, `10, 12`, `7, 8`,
`8, 9` — were also losing their second verse. Both fixed. ⚠ **The lesson is the pass's own: a checker's first output is not
evidence, and that applies to a checker written an hour ago.**

## The ones most likely to be real omissions

- **printed 136 — the BEATITUDES, seven of them** (Matt. v. 4–10), every one invisible. The page sets the
  whole sermon-opening and the band could see only v. 3.
- **printed 132, 134 — Daniel's prayer** (ix. 7, 8, 16, 17, 18, 19) — the volume quotes it at length and the
  index held only ix. 5.
- **printed 305 — the six days of creation** (Gen. i. 6, 11, 14, 20, 24, 28).
- **printed 310 — Peter's denial** (Matt. xxvi. 33, 49, 55, 56, 70, 72, 74).
- **printed 156 — Ps. lxxxv. 3–7**; **printed 108/110 — Rom. vii. 16–24**, the whole *wretched man* passage.
- **printed 342 — Eph. i. 14**, the Earnest. ⚠ **This one was found by hand on 2026-08-10 and written into the
  band before the tool could see it** — which is the argument for the whole fix: the eye caught one, and there
  were a hundred and twenty-nine more.

## Method

```
python3.11 tools/ref_index.py --continuations   # read this FIRST for the page you are on
python3.11 tools/note_sheet.py <page>
python3.11 tools/check_notes.py <page> <page>
```

⚠ `--continuations` flags every resolution whose antecedent is on the previous page or more than six lines back.
**A long quotation walking up one chapter (Dan. ix, Matt. v, Ps. lxxxv) is the innocent case; anything else is not.**

