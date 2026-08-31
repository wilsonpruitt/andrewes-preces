import fs from "fs";
import path from "path";

// The apparatus/ prose files are already publishable, and cheap (WEB-PLAN
// §8): they're written as reference prose, not generated. Read straight from
// the repo — additive only, nothing here writes back to apparatus/.
const APPARATUS_DIR = path.join(process.cwd(), "..", "apparatus");

export interface ApparatusPage {
  slug: string;
  file: string;
  title: string;
  blurb: string;
}

export const APPARATUS_PAGES: ApparatusPage[] = [
  {
    slug: "class-a",
    file: "CLASS-A-ledger.md",
    title: "Class A — the ledger",
    blurb: "Every reading where the Wright apograph (Pembroke College, Cambridge) diverges from the 1853 plate, resolved against our own transcripts.",
  },
  {
    slug: "class-b",
    file: "CLASS-B-unit-boundaries.md",
    title: "Class B — the spacing record",
    blurb: "The manuscript's own record of where Andrewes left air on the page — the intervals CONVENTIONS §13 calls the highest-value class for the edition's structure.",
  },
  {
    slug: "brightman",
    file: "BRIGHTMAN-collation.md",
    title: "Brightman 1903 as a collation witness",
    blurb: "A pilot collation against Brightman's edition — method, probes, and the anchor table.",
  },
  {
    slug: "variae-lectiones",
    file: "variae-lectiones-transcript.md",
    title: "Variæ Lectiones et Addenda Quædam",
    blurb: "Raw transcript of the 1853's own apparatus, separately foliated in lower-case roman — the source Class A is resolved from.",
  },
  {
    slug: "notae-marginales",
    file: "notae-marginales-transcript.md",
    title: "Notæ Marginales ex eodem MS.",
    blurb: "Raw transcript of the 1853's marginal notes from the same manuscript.",
  },
  {
    slug: "latin-question",
    file: "THE-LATIN-QUESTION.md",
    title: "The Latin Question",
    blurb: "Whether the Latin of printed 1–250 is Andrewes' own or a 1675 editor's — surfaced, not settled; Wilson's call.",
  },
];

export function loadApparatusPage(slug: string): { meta: ApparatusPage; body: string } | undefined {
  const meta = APPARATUS_PAGES.find((p) => p.slug === slug);
  if (!meta) return undefined;
  const body = fs.readFileSync(path.join(APPARATUS_DIR, meta.file), "utf-8");
  return { meta, body };
}
