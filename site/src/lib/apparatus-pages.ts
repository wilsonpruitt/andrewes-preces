import prose from "@/data/apparatus-prose.json";

// ⚠ Imported, NOT read from ../apparatus/ with fs. A deploy uploads only
// site/, so a path that escapes it resolves locally and is missing in
// production — that is exactly how the first production build failed
// (ENOENT /vercel/apparatus/CLASS-A-ledger.md). tools/build_web_json.py copies
// the prose in; nothing under site/ reaches outside site/.

export interface ApparatusPage {
  slug: string;
  title: string;
  blurb: string;
  body: string;
}

export const APPARATUS_PAGES = prose as ApparatusPage[];

export function loadApparatusPage(slug: string): ApparatusPage | undefined {
  return APPARATUS_PAGES.find((p) => p.slug === slug);
}
