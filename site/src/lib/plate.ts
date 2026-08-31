import plateData from "@/data/plate.json";

// The plate image for a printed page (WEB-PLAN §10.2). See tools/plate_leaves.py
// for why the mapping is a constant offset and what two plausible mappings it
// is NOT — the scan's own leaf numbers are accurate about leaves and useless as
// image indices, because the derivative drops the duplicate leaves.

interface PlateData {
  item: string;
  offset: number;
  first: number;
  last: number;
  verified: number[];
  source: string;
}

export const PLATE = plateData as PlateData;

export function plateUrl(printed: number): string | undefined {
  if (printed < PLATE.first || printed > PLATE.last) return undefined;
  return `https://archive.org/download/${PLATE.item}/page/n${printed + PLATE.offset}.jpg`;
}

/** Eye-verified pages carry a stronger claim than derived ones, and the UI
 * says which it is rather than levelling them. */
export function isVerified(printed: number): boolean {
  return PLATE.verified.includes(printed);
}
