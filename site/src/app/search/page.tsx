import { loadSections, sectionStem } from "@/lib/content";
import { SearchClient } from "./search-client";

export default function SearchPage() {
  // page -> reader href, resolved at build so the client never carries
  // content.json (4MB) just to turn a page number into a link.
  const hrefs: Record<string, string> = {};
  for (const s of loadSections()) {
    for (const p of s.pages) {
      hrefs[p.n] = `/read/${s.part}/${sectionStem(s.id)}`;
    }
  }
  return (
    <div>
      <h2 className="section-title">Search</h2>
      <SearchClient hrefs={hrefs} />
    </div>
  );
}
