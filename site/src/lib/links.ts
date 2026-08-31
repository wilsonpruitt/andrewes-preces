import linksData from "@/data/links.json";

// Every note that names another printed page — the volume pointing at itself
// (WEB-PLAN §10.1 and §10.3). This, not an alignment algorithm, is the basis
// of the synopsis: see RECENSION_PAIRS below for why.

export interface PageLink {
  from: number;
  line: number;
  to: number[];
  band: "R" | "S";
  note: string;
}

export function loadLinks(): PageLink[] {
  return linksData as unknown as PageLink[];
}

export interface RecensionPair {
  id: string;
  title: string;
  a: { label: string; pages: [number, number] };
  b: { label: string; pages: [number, number] };
  warrant: string;
}

// ⚠⚠ THESE ARE THE EDITION'S OWN STATEMENT OF THE RELATIONSHIP, taken from
// STRUCTURE.md, not computed. Part III is the Harley recension of Part II's
// penitential matter, and the correspondences it records are §1 to §23 (and
// §38's close), §2 to §17, and §4's Quod brace to §24's estate-catalogue.
export const RECENSION_PAIRS: RecensionPair[] = [
  {
    id: "fides",
    title: "The Creed — thanksgiving turned into belief",
    a: { label: "Part II §23 In magnum pietatis sacramentum", pages: [340, 345] },
    b: { label: "Part III §1 Confessio Fidei", pages: [398, 406] },
    warrant:
      "STRUCTURE.md: a second recension of §23 (and of §38's close), plural where §23 is singular. The note at printed 340 puts it exactly: the same six titles, in this order and in these mysteries, stand again at printed 402–403, turned from thanksgiving into belief — and there they carry not one reference.",
  },
  {
    id: "peccata",
    title: "The confession of sins — the schema and the prayer",
    a: { label: "Part II §17 Peccatorum Confessio", pages: [324, 324] },
    b: { label: "Part III §2 Confessio Peccatorum", pages: [407, 416] },
    warrant:
      "STRUCTURE.md: a second recension of §17. ⚠ The two are not verbally parallel and no alignment could make them so — §17 is a SCHEMA of numbered heads and brace catalogues (Aggravatio · Peccati Species · Quoties? Quamdiu?), and Part III §2 is that schema written out as prayer (Peccavi, Domine, Tibi, Domine, Tibi). One page against ten.",
  },
  {
    id: "gratiarum",
    title: "The estate-catalogue — with the antitheses stripped out",
    a: { label: "Part II §24 Confessio Laudis", pages: [346, 348] },
    b: { label: "Part III §4 Gratiarum Actio", pages: [426, 431] },
    warrant:
      "STRUCTURE.md: the thirteen-line Quod brace at printed 428 is §24's estate-catalogue stripped of its antitheses. The note at printed 346 adds that the schools' division — bona gratiae, naturae, fortunae — stands again at printed 429 as Pro bonis.",
  },
];
