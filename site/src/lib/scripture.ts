import fs from "fs";
import path from "path";

// The merged index (WEB-PLAN §9), built by tools/scripture_index.py. Read from
// disk per book rather than imported, so a static export does not inline all
// 2,361 entries into every one of the sixty book pages.

export interface ScriptureEntry {
  book: string;
  chapter: number | null;
  verses: number[];
  printed: string; // the reference AS PRINTED — never renumbered
  page: number;
  line: number;
  source: "marked" | "identified";
  band?: "R"; // an identification made in the explanatory band
  situation?: string;
  numbering?: boolean; // the note states which Psalter the figure belongs to
  plateFigure?: boolean; // the plate's own figure, kept as printed and glossed
}

export interface BookMeta {
  slug: string;
  name: string;
  testament: "ot" | "ap" | "nt";
  marked: number;
  identified: number;
  total: number;
}

const DIR = path.join(process.cwd(), "src", "data", "scripture");

export function loadBooks(): BookMeta[] {
  return JSON.parse(fs.readFileSync(path.join(DIR, "index.json"), "utf-8"));
}

export function loadBook(slug: string): ScriptureEntry[] | undefined {
  const f = path.join(DIR, `${slug}.json`);
  if (!fs.existsSync(f)) return undefined;
  return JSON.parse(fs.readFileSync(f, "utf-8"));
}

export const TESTAMENT_LABEL: Record<string, string> = {
  ot: "Old Testament",
  ap: "Apocrypha",
  nt: "New Testament",
};

/** Entries grouped by chapter, in order — the shape a book page reads in. */
export function byChapter(entries: ScriptureEntry[]) {
  const groups = new Map<number, ScriptureEntry[]>();
  for (const e of entries) {
    const ch = e.chapter ?? 0;
    if (!groups.has(ch)) groups.set(ch, []);
    groups.get(ch)!.push(e);
  }
  return [...groups.entries()].sort((a, b) => a[0] - b[0]);
}
