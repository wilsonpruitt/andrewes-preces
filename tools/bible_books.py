#!/usr/bin/env python3
"""Canonical book identities for the scripture index (WEB-PLAN.md §9).

⚠⚠ WHY THIS FILE EXISTS AS ITS OWN MODULE. The index merges TWO vocabularies
that do not overlap: the 1853 plate cites in VULGATE forms (`Psal.`, `Luc.`,
`Jo.`, `Apoc.`, `Jac.`, `Thren.`, `Sap.`, `Abac.`, `Reg.`) and the `S:` band —
authored, in English — cites the same verses as `Ps.`, `Luke`, `John`, `Rev`,
`Jas`, `Lam`, `Wisd`, `Hab`, `Kings`. A string match between the two calls
almost every MARKED reference "identified", which is precisely the distinction
§9 exists to draw. Both sides must reduce to one canonical identity first.

⚠⚠⚠ THE TABLE BELOW WAS DERIVED FROM EVIDENCE, NOT FROM LATIN. For each plate
form, every `S:` note standing on the SAME page and line with the same chapter
and verse was collected, and the book it names was counted as a vote. Those
notes were written with the page in view, so they are a witness, not a guess.
`CONFIRMED` marks a mapping carried by that vote; `inferred` marks one no vote
reached (all of them low-count and unambiguous — `Cant.` is the Song, `Bar.` is
Baruch), left visible so a later session can see which rest on evidence.

⚠ `1/2 Reg.` IS THE ONE THAT WOULD HAVE GONE WRONG ON LATIN ALONE. In the
Vulgate 1--2 Regum ARE 1--2 Samuel and Kings is 3--4 Regum, so the natural
reading files fourteen references under Samuel. It is wrong here: this plate
prints `Sam.` for Samuel in its own right, and all fourteen `Reg.` notes name
KINGS — `1 Reg. viii. 28/39/47` against "Solomon at the dedication", which is
1 Kings 8 on its content and not merely on its numerals. Verified 2026-08-31.

⚠ `Jud.` IS TWO BOOKS AND NO VOTE CAN SETTLE IT — the split is by the shape of
the numeral, exactly as `ref_index.py` records: with a roman chapter it is
JUDGES (`Jud. ix. 23`), with a bare verse it is JUDE (`Jud. 23`). The vote came
back {Jude: 4, Judg: 1}, which is that rule showing through, not noise.

⚠ A VOTE CAN ALSO BE SPURIOUS, and one was. `1 Tim.` drew a single `Eph.` vote
from printed 319 line 3, where the plate marks `1 Tim. i. 14` and the note
identifies `Eph. i. 14` — the SAME chapter and verse in a different book, both
genuinely on that line. Numerals agreeing is not the reference agreeing
(`reference_...`: "reading a digit correctly is not reading it rightly"), so
the merge matches on the whole canonical triple and that vote is excluded here.
"""

# canonical slug -> (display name, chapters, testament)
# `chapters` is used ONLY to flag an out-of-range citation for an eye; nothing
# is ever renumbered or "corrected" on the strength of it.
BOOKS = {
    "gen": ("Genesis", 50, "ot"), "exod": ("Exodus", 40, "ot"),
    "lev": ("Leviticus", 27, "ot"), "num": ("Numbers", 36, "ot"),
    "deut": ("Deuteronomy", 34, "ot"), "josh": ("Joshua", 24, "ot"),
    "judg": ("Judges", 21, "ot"), "ruth": ("Ruth", 4, "ot"),
    "1sam": ("1 Samuel", 31, "ot"), "2sam": ("2 Samuel", 24, "ot"),
    "1kgs": ("1 Kings", 22, "ot"), "2kgs": ("2 Kings", 25, "ot"),
    "1chr": ("1 Chronicles", 29, "ot"), "2chr": ("2 Chronicles", 36, "ot"),
    "ezra": ("Ezra", 10, "ot"), "neh": ("Nehemiah", 13, "ot"),
    "esth": ("Esther", 10, "ot"), "job": ("Job", 42, "ot"),
    "ps": ("Psalms", 150, "ot"), "prov": ("Proverbs", 31, "ot"),
    "eccl": ("Ecclesiastes", 12, "ot"), "song": ("Song of Songs", 8, "ot"),
    "isa": ("Isaiah", 66, "ot"), "jer": ("Jeremiah", 52, "ot"),
    "lam": ("Lamentations", 5, "ot"), "ezek": ("Ezekiel", 48, "ot"),
    # ⚠ 14, not 12: the Vulgate carries Susanna and Bel as Dan. xiii--xiv, and
    # this plate cites the Vulgate. Flagging xiii as out of range would be the
    # tool being wrong about the book, not the book being wrong.
    "dan": ("Daniel", 14, "ot"),
    "hos": ("Hosea", 14, "ot"), "joel": ("Joel", 3, "ot"),
    "amos": ("Amos", 9, "ot"), "obad": ("Obadiah", 1, "ot"),
    "jonah": ("Jonah", 4, "ot"), "mic": ("Micah", 7, "ot"),
    "nah": ("Nahum", 3, "ot"), "hab": ("Habakkuk", 3, "ot"),
    "zeph": ("Zephaniah", 3, "ot"), "hag": ("Haggai", 2, "ot"),
    "zech": ("Zechariah", 14, "ot"), "mal": ("Malachi", 4, "ot"),

    # The Apocrypha stand as a group after the Old Testament, which is where a
    # Church of England book sets them — read "for example of life and
    # instruction of manners" (Article VI), and cited freely by this volume.
    "tob": ("Tobit", 14, "ap"), "judith": ("Judith", 16, "ap"),
    "wisd": ("Wisdom", 19, "ap"), "ecclus": ("Ecclesiasticus", 51, "ap"),
    "bar": ("Baruch", 6, "ap"), "esd": ("Esdras", 16, "ap"),
    "1macc": ("1 Maccabees", 16, "ap"), "2macc": ("2 Maccabees", 15, "ap"),

    "matt": ("Matthew", 28, "nt"), "mark": ("Mark", 16, "nt"),
    "luke": ("Luke", 24, "nt"), "john": ("John", 21, "nt"),
    "acts": ("Acts", 28, "nt"), "rom": ("Romans", 16, "nt"),
    "1cor": ("1 Corinthians", 16, "nt"), "2cor": ("2 Corinthians", 13, "nt"),
    "gal": ("Galatians", 6, "nt"), "eph": ("Ephesians", 6, "nt"),
    "phil": ("Philippians", 4, "nt"), "col": ("Colossians", 4, "nt"),
    "1thess": ("1 Thessalonians", 5, "nt"), "2thess": ("2 Thessalonians", 3, "nt"),
    "1tim": ("1 Timothy", 6, "nt"), "2tim": ("2 Timothy", 4, "nt"),
    "titus": ("Titus", 3, "nt"), "philem": ("Philemon", 1, "nt"),
    "heb": ("Hebrews", 13, "nt"), "jas": ("James", 5, "nt"),
    "1pet": ("1 Peter", 5, "nt"), "2pet": ("2 Peter", 3, "nt"),
    "1john": ("1 John", 5, "nt"), "2john": ("2 John", 1, "nt"),
    "3john": ("3 John", 1, "nt"), "jude": ("Jude", 1, "nt"),
    "rev": ("Revelation", 22, "nt"),
}

BOOK_ORDER = list(BOOKS)

# Every abbreviation either source actually uses, lowercased, with the numeral
# prefix normalised to a bare digit ("1. Tim" and "1 Tim" both arrive as "1tim").
# ⚠ Long forms and short forms are BOTH listed in their own right; a form that
# is absent maps to nothing and the reference silently leaves the index, which
# is how nineteen books once went missing from the plate index
# (`ref_index.py` §11). Extend by ADDING, never by loosening a pattern.
ALIASES = {
    # --- Old Testament -------------------------------------------------
    "gen": "gen",
    "exod": "exod", "ex": "exod",
    "lev": "lev",
    "num": "num",
    "deut": "deut",
    "josh": "josh", "jos": "josh",
    "judg": "judg", "judic": "judg",          # Judic. CONFIRMED
    "ruth": "ruth",
    "1sam": "1sam", "2sam": "2sam",
    # ⚠ CONFIRMED against fourteen notes — Kings, NOT the Vulgate's Samuel.
    "1reg": "1kgs", "2reg": "2kgs",
    "1kings": "1kgs", "2kings": "2kgs", "1kgs": "1kgs", "2kgs": "2kgs",
    "1chron": "1chr", "2chron": "2chr", "1chr": "1chr", "2chr": "2chr",
    "1paralip": "1chr", "2paralip": "2chr",   # 2 Paralip. CONFIRMED
    "1paral": "1chr", "2paral": "2chr",
    "ezra": "ezra", "ezr": "ezra",
    "neh": "neh", "nehem": "neh",
    "esth": "esth",
    "job": "job",
    "psal": "ps", "ps": "ps",
    "prov": "prov", "pro": "prov",
    "eccl": "eccl", "eccles": "eccl",
    "cant": "song", "song": "song",           # inferred (Canticum)
    # ⚠ `Es.` is ESAIAS, not Esther and not Esdras — CONFIRMED six times, and
    # independently verified against all six occurrences in ref_index.py §11.
    "isa": "isa", "is": "isa", "es": "isa", "isai": "isa",
    "jer": "jer", "jerem": "jer",
    "lam": "lam", "thren": "lam",             # Threni CONFIRMED
    "ezek": "ezek", "ezech": "ezek", "ez": "ezek",   # Ez. CONFIRMED = Ezekiel
    "dan": "dan",
    "hos": "hos", "os": "hos",                # Osee CONFIRMED
    "joel": "joel",
    "amos": "amos", "am": "amos",
    "obad": "obad", "abd": "obad",
    "jonah": "jonah", "jon": "jonah",
    "mic": "mic", "mich": "mic",              # Mich. CONFIRMED
    "nah": "nah",
    "hab": "hab", "abac": "hab",              # Abacuc CONFIRMED
    "zeph": "zeph", "soph": "zeph",
    "hag": "hag", "agg": "hag",
    "zech": "zech", "zach": "zech",
    "mal": "mal",
    # --- Apocrypha ------------------------------------------------------
    "tob": "tob",
    "judith": "judith",
    "wisd": "wisd", "sap": "wisd",            # Sapientia CONFIRMED
    # ⚠ `Syr.` (Sirach) is Ecclesiasticus and the 1853 GLOSSES IT ITSELF,
    # `[i. e. Ecclus.]` — not the same book as Eccl. (Ecclesiastes) above.
    "ecclus": "ecclus", "syr": "ecclus",
    "bar": "bar",                             # inferred
    "esd": "esd",
    "1mac": "1macc", "2mac": "2macc", "mac": "1macc",
    # --- New Testament ---------------------------------------------------
    "matt": "matt", "mat": "matt", "matth": "matt",
    "mark": "mark", "marc": "mark", "mar": "mark",
    "luke": "luke", "luc": "luke", "luk": "luke",
    "john": "john", "joh": "john", "jo": "john", "joan": "john",
    "1john": "1john", "1joh": "1john", "1jo": "1john", "1joan": "1john",
    "2john": "2john", "2joh": "2john", "2jo": "2john",
    "3john": "3john", "3joh": "3john", "3jo": "3john",
    "acts": "acts", "act": "acts",
    "rom": "rom",
    "1cor": "1cor", "2cor": "2cor",
    "gal": "gal", "galat": "gal",
    "eph": "eph", "ephes": "eph",
    "phil": "phil",
    "col": "col", "coloss": "col",
    "1thess": "1thess", "2thess": "2thess",
    "1tim": "1tim", "2tim": "2tim",
    "titus": "titus", "tit": "titus",
    "philem": "philem",
    "heb": "heb",
    "jas": "jas", "jac": "jas",               # Jacobus CONFIRMED
    "1pet": "1pet", "2pet": "2pet",
    "jude": "jude",
    "rev": "rev", "apoc": "rev",              # Apocalypsis CONFIRMED
}

# ⚠ The `R:` band is PROSE, and it names its books in full — "Romans vii. 18
# stands here word for word and unmarked". Those long forms appear nowhere in
# the plate or the `S:` band, so they live here, apart, and are added to the
# alternation only for the explanatory band. Kept separate so the plate index
# is never widened by them (a widened pattern is this project's most expensive
# recurring mistake).
LONG_FORMS = {
    "genesis": "gen", "exodus": "exod", "leviticus": "lev", "numbers": "num",
    "deuteronomy": "deut", "joshua": "josh", "judges": "judg",
    "samuel": "1sam", "kings": "1kgs", "chronicles": "1chr",
    "nehemiah": "neh", "esther": "esth", "psalm": "ps", "psalms": "ps",
    "proverbs": "prov", "ecclesiastes": "eccl", "isaiah": "isa",
    "jeremiah": "jer", "lamentations": "lam", "ezekiel": "ezek",
    "daniel": "dan", "hosea": "hos", "obadiah": "obad", "jonah": "jonah",
    "micah": "mic", "nahum": "nah", "habakkuk": "hab", "zephaniah": "zeph",
    "haggai": "hag", "zechariah": "zech", "malachi": "mal",
    "wisdom": "wisd", "ecclesiasticus": "ecclus",
    "matthew": "matt", "romans": "rom", "corinthians": "1cor",
    "galatians": "gal", "ephesians": "eph", "philippians": "phil",
    "colossians": "col", "thessalonians": "1thess", "timothy": "1tim",
    "philemon": "philem", "hebrews": "heb", "james": "jas",
    "peter": "1pet", "revelation": "rev",
}

# ⚠ `Jud.` alone is deliberately ABSENT from ALIASES: it is Judges with a roman
# chapter and Jude with a bare verse, and only the citation's own shape decides.
# `resolve()` handles it; anything that bypasses resolve() must too.
AMBIGUOUS_JUD = {"jud"}

# ⚠⚠ `Ez.` IS ALSO TWO BOOKS, and unlike `Jud.` NOTHING IN THE CITATION'S SHAPE
# SEPARATES THEM — both Ezra and Ezekiel have a chapter ix. The default above
# is Ezekiel, which is right five times out of six; the exception is recorded
# here per instance, because a rule that cannot be checked is worse than a list
# that can.
#
# ⚠ `ref_index.py`'s own docstring is WRONG on this point: it lists "`Ez`
# (= Ezekiel — ix. 6, xviii. 23, xxxiii. 11)", but printed 15's `Ez. ix. 6` is
# EZRA. The `S:` note reads it *I am ashamed and blush to lift up my face to
# thee, my God*, which is Ezra ix. 6 word for word; Ezekiel ix. 6 is *slay
# utterly old and young, both maids, and little children*. The notes pass had
# the line in view and the docstring did not. Found 2026-08-31 — and only
# because a column line-count offset hid it from the first pass of the same
# check, which is this project's recurring failure class exactly.
#
# Keyed (printed page, the reference as ref_index reports it).
INSTANCE_OVERRIDES = {
    (15, "Ez. ix. 6"): "ezra",
}

ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}


def roman_to_int(s: str):
    """Lowercase roman -> int, or None if it is not a clean roman numeral."""
    s = s.strip().lower().rstrip(".")
    if not s or any(ch not in ROMAN for ch in s):
        return None
    total, prev = 0, 0
    for ch in reversed(s):
        v = ROMAN[ch]
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total or None


def normalise_token(book_token: str) -> str:
    """'1. Tim' / '1 Tim' / 'Tim' -> '1tim' / 'tim'."""
    t = book_token.strip().lower().replace(".", "").replace(" ", "")
    return t


def resolve(book_token: str, chapter_is_roman: bool):
    """Canonical slug for a book abbreviation, or None if unknown.

    `chapter_is_roman` decides `Jud.` and nothing else: a roman chapter makes
    it Judges, a bare arabic verse makes it Jude (ref_index.py's rule).
    """
    t = normalise_token(book_token)
    if t in AMBIGUOUS_JUD:
        return "judg" if chapter_is_roman else "jude"
    return ALIASES.get(t)
