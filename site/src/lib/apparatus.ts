import apparatusData from "@/data/apparatus.json";

// apparatus/print-notes.md's two foot-bands (WEB-PLAN §8), reused unchanged
// from transcript2tex.load_notes() via build_web_json.py. The web keeps the
// DISTINCTION between the verso apparatus criticus ("V:") and the recto
// scripture/explanatory notes ("S:"/"R:") and drops the print's two-feet
// GEOMETRY — a marker on the line, opening the note wherever it's clicked.

export interface PageNotes {
  V: string[];
  R: string[];
  S: string[];
}

const DATA = apparatusData as unknown as Record<string, Partial<PageNotes>>;

export function notesForPage(page: number): PageNotes {
  const p = DATA[String(page)];
  return { V: p?.V ?? [], R: p?.R ?? [], S: p?.S ?? [] };
}

const LEAD = /^(\d+)(?:\s*[–-]\s*\d+)?(?:\s|$)/;
const STRIP_LEAD = /^\d+(?:\s*[–-]\s*\d+)?\s*/;

export function stripLead(entry: string): string {
  return entry.replace(STRIP_LEAD, "");
}

/** Group entries by their leading line figure, in FIRST-APPEARANCE order —
 * ports transcript2tex.by_line() exactly (§8). An entry with no leading
 * figure at all (a note about the page, not a line) is dropped here and
 * surfaces separately as an unanchored note. */
export function byLine(entries: string[]): { line: number; entries: string[] }[] {
  const order: number[] = [];
  const groups = new Map<number, string[]>();
  for (const e of entries) {
    const m = e.match(LEAD);
    if (!m) continue;
    const ln = Number(m[1]);
    if (!groups.has(ln)) {
      groups.set(ln, []);
      order.push(ln);
    }
    groups.get(ln)!.push(e);
  }
  return order.map((line) => ({ line, entries: groups.get(line)! }));
}

export function unanchored(entries: string[]): string[] {
  return entries.filter((e) => !LEAD.test(e));
}

const ROMAN_VALUES: [number, string][] = [
  [1000, "m"], [900, "cm"], [500, "d"], [400, "cd"], [100, "c"],
  [90, "xc"], [50, "l"], [40, "xl"], [10, "x"], [9, "ix"],
  [5, "v"], [4, "iv"], [1, "i"],
];

/** Lowercase roman, matching transcript2tex.roman() — Wilson's ruling that a
 * marker series sharing the arabic alphabet with the line-number ruler would
 * confuse still holds on screen (§8). */
export function roman(n: number): string {
  let out = "";
  for (const [v, s] of ROMAN_VALUES) {
    while (n >= v) {
      out += s;
      n -= v;
    }
  }
  return out;
}

export interface VersoMark {
  roman: string;
  entries: string[];
}

/** The verso foot ("V:", apparatus criticus) for ONE opening — numbered
 * continuously gr-then-la so the roman is unique across the leaf, exactly as
 * transcript2tex.apparatus_band(). Keyed "gr:<line>" / "la:<line>". */
export function versoMarks(vGr: string[], vLa: string[]): Map<string, VersoMark> {
  const out = new Map<string, VersoMark>();
  let i = 0;
  for (const [col, list] of [["gr", vGr], ["la", vLa]] as const) {
    for (const { line, entries } of byLine(list)) {
      i += 1;
      out.set(`${col}:${line}`, { roman: roman(i), entries });
    }
  }
  return out;
}

export interface RectoMark {
  roman: string;
  scripture: string[];
  explanatory: string[];
}

/** The recto foot ("S:" scripture + "R:" explanatory), ONE marker series over
 * both streams — transcript2tex.recto_band(). Keyed by line number alone: the
 * recto belongs to whichever page carries "en" in this opening. */
export function rectoMarks(s: string[], r: string[]): Map<number, RectoMark> {
  const sByLine = new Map(byLine(s).map((g) => [g.line, g.entries]));
  const rByLine = new Map(byLine(r).map((g) => [g.line, g.entries]));
  const lines = [...new Set([...sByLine.keys(), ...rByLine.keys()])].sort((a, b) => a - b);
  const out = new Map<number, RectoMark>();
  lines.forEach((line, idx) => {
    out.set(line, {
      roman: roman(idx + 1),
      scripture: sByLine.get(line) ?? [],
      explanatory: rByLine.get(line) ?? [],
    });
  });
  return out;
}
