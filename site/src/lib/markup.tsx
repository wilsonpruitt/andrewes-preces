import React from "react";

// The bands are written in light markdown: *em*, **bold**, `lemma` (set
// upright), and bare Hebrew. Rendered the same way wherever a band is shown —
// the apparatus in the reader and the situations in the scripture index — so
// the two cannot drift, the same reason the print builders share one parser.
const TOKEN =
  /`([^`]+)`|\*\*([^*]+)\*\*|\*([^*]+)\*|([֐-׿][֐-׿\s]*[֐-׿]|[֐-׿])/g;

export function renderMarkup(text: string): React.ReactNode[] {
  const nodes: React.ReactNode[] = [];
  let last = 0;
  let key = 0;
  let m: RegExpExecArray | null;
  TOKEN.lastIndex = 0;
  while ((m = TOKEN.exec(text))) {
    if (m.index > last) nodes.push(text.slice(last, m.index));
    if (m[1] !== undefined) {
      nodes.push(
        <span key={key++} className="pv-lemma">
          {m[1]}
        </span>
      );
    } else if (m[2] !== undefined) {
      nodes.push(<strong key={key++}>{m[2]}</strong>);
    } else if (m[3] !== undefined) {
      nodes.push(<em key={key++}>{m[3]}</em>);
    } else if (m[4] !== undefined) {
      nodes.push(
        <span
          key={key++}
          className="pv-hebrew"
          dir="rtl"
          style={{ unicodeBidi: "isolate" }}
        >
          {m[4]}
        </span>
      );
    }
    last = TOKEN.lastIndex;
  }
  if (last < text.length) nodes.push(text.slice(last));
  return nodes;
}
