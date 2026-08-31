// Search folding, in the browser (WEB-PLAN.md §12).
//
// ⚠⚠ THIS MIRRORS tools/search_fold.py AND MUST NOT DRIFT FROM IT. The index
// is folded at build time by Python; the query is folded here, so the two
// implementations have to agree exactly or a reader's query silently fails to
// match text that is really there. This repo's own rule is that a second
// implementation of a parser is a drift waiting to happen — so the drift is
// MEASURED, not trusted: the index ships `foldTests` (input/expected pairs
// produced by the Python), and `checkFold` runs them through this code on
// load. A mismatch is reported in the UI rather than swallowed.

const HEBREW_MARKS = /[֑-ׇ]/g;

export function fold(text: string, hebrew = false): string {
  let t = text;
  if (hebrew) {
    t = t.replace(HEBREW_MARKS, "");
  } else {
    // NFD then drop combining marks — this takes the accents and breathings
    // off polytonic Greek and the diacritics off Latin.
    t = t.normalize("NFD").replace(/\p{M}/gu, "");
    t = t.toLowerCase();
    t = t.replace(/æ/g, "ae").replace(/œ/g, "oe");
    t = t.replace(/ς/g, "σ");
    t = t.replace(/v/g, "u").replace(/j/g, "i");
  }
  // \w is ASCII-only in JS without the u flag; use an explicit class so Greek
  // and Hebrew letters survive.
  t = t.replace(/[^\p{L}\p{N}\s]/gu, " ");
  return t.split(/\s+/).filter(Boolean).join(" ");
}

export interface FoldTest {
  in: string;
  out: string;
  hebrew?: boolean;
}

/** Returns the cases where this code disagrees with the Python that built the
 * index. Empty is the only acceptable answer. */
export function checkFold(tests: FoldTest[]): FoldTest[] {
  return tests.filter((t) => fold(t.in, !!t.hebrew) !== t.out);
}
