import contentData from "@/data/content.json";

// The shape build_web_json.py emits (WEB-PLAN.md §4-5). Andrewes' source is
// page-keyed and line-faithful, not chapter-prose like Milton's — so this is a
// fresh model, not a port of Milton's Chunk/BookMeta shape. What DOES port is
// the underlying idea Milton's content.ts proved: an array, not a fixed pair,
// so the reader never hardcodes a language count.

export type SpanKind =
  | "text" | "strong" | "em" | "hebrew" | "sup" | "unclear" | "supplied" | "gap";

export interface Span {
  kind: SpanKind;
  text?: string;
  width?: number; // "gap" only — measured horizontal space, in source spaces
  children?: Span[]; // "strong" only — bold may enclose italic
}

export interface Line {
  break?: true; // a paragraph separator; no other field is present
  n?: number; // sense-line number, 1..N per page — absent on a break
  indent?: number;
  spans?: Span[];
}

export interface PageData {
  n: number; // printed page number, the 1853's own
  layers: Record<string, Line[]>; // keys among "gr" | "la" | "en"
}

export interface Section {
  id: string; // "part1/day1"
  part: number;
  label: string;
  pages: PageData[];
}

export const PART_TITLES: Record<number, string> = {
  1: "Part I",
  2: "Part II — Preces Quotidianae",
  3: "Part III — Confessio Fidei and after",
};

export const LAYER_ORDER = ["gr", "la", "en"] as const;
export type LayerKey = (typeof LAYER_ORDER)[number];
export const LAYER_LABEL: Record<LayerKey, string> = {
  gr: "Greek",
  la: "Latin",
  en: "English",
};

export function loadSections(): Section[] {
  return contentData as unknown as Section[];
}

export function findSection(part: number, stem: string): Section | undefined {
  return loadSections().find((s) => s.id === `part${part}/${stem}`);
}

export function sectionsForPart(part: number): Section[] {
  return loadSections().filter((s) => s.part === part);
}

export function sectionStem(id: string): string {
  return id.split("/")[1];
}

/** The layers this section carries anywhere in it, in canonical order — the
 * set the view-mode toggle offers. A given PAGE may carry fewer (§7: Part I's
 * Greek/Latin pairing means most pages are 2 of the 3, never all 3 at once). */
export function sectionLayers(section: Section): LayerKey[] {
  const have = new Set<string>();
  for (const p of section.pages) for (const k of Object.keys(p.layers)) have.add(k);
  return LAYER_ORDER.filter((k) => have.has(k));
}

export function adjacentSections(section: Section): { prev?: Section; next?: Section } {
  const all = loadSections();
  const i = all.findIndex((s) => s.id === section.id);
  return { prev: all[i - 1], next: all[i + 1] };
}

/** A reading UNIT: one printed page, or — where the plate pairs a Greek verso
 * with its facing Latin recto (Part I's opening, and Part II's §42/§43 hymns,
 * WEB-PLAN §5) — two. The pairing test is structural, not a part number: a
 * "gr" page immediately followed by a page that is "la" ALONE (no "en" of its
 * own, because its English is filed under the Greek page it faces) is exactly
 * the shape build_loeb's own `paired` predicate exists to catch. */
export interface Unit {
  pages: number[]; // 1 or 2 printed page numbers, in reading order
  layers: Partial<Record<LayerKey, Line[]>>;
  pageOf: Partial<Record<LayerKey, number>>; // which printed page each layer is on
}

export function sectionUnits(section: Section): Unit[] {
  const byN = new Map(section.pages.map((p) => [p.n, p] as const));
  const ordered = [...byN.keys()].sort((a, b) => a - b);
  const skip = new Set<number>();
  const units: Unit[] = [];
  for (const n of ordered) {
    if (skip.has(n)) continue;
    const page = byN.get(n)!;
    const next = byN.get(n + 1);
    const pairable =
      "gr" in page.layers &&
      !!next &&
      "la" in next.layers &&
      !("en" in next.layers) &&
      Object.keys(next.layers).length === 1;
    if (pairable) {
      skip.add(n + 1);
      const layers: Unit["layers"] = { gr: page.layers.gr, la: next!.layers.la };
      const pageOf: Unit["pageOf"] = { gr: n, la: n + 1 };
      if (page.layers.en) {
        layers.en = page.layers.en;
        pageOf.en = n;
      }
      units.push({ pages: [n, n + 1], layers, pageOf });
    } else {
      const layers: Unit["layers"] = {};
      const pageOf: Unit["pageOf"] = {};
      for (const k of LAYER_ORDER) {
        if (page.layers[k]) {
          layers[k] = page.layers[k];
          pageOf[k] = n;
        }
      }
      units.push({ pages: [n], layers, pageOf });
    }
  }
  return units;
}

/** Which section a printed page falls in — the scripture index links back
 * into the reader by page and sense-line. */
export function sectionForPage(n: number): Section | undefined {
  return loadSections().find((s) => s.pages.some((p) => p.n === n));
}

/** The reader anchor for a printed page and line: /read/1/day1#p34.27 */
export function readerHref(page: number, line: number): string | undefined {
  const s = sectionForPage(page);
  if (!s) return undefined;
  const anchor = line > 0 ? `#p${page}.${line}` : "";
  return `/read/${s.part}/${sectionStem(s.id)}${anchor}`;
}
