import Link from "next/link";
import { APPARATUS_PAGES } from "@/lib/apparatus-pages";

export default function ApparatusIndex() {
  return (
    <div>
      <h2 className="section-title">The apparatus</h2>
      <p style={{ maxWidth: "640px", marginBottom: "2rem", fontSize: "15px", opacity: 0.85 }}>
        1,676 entries anchor the text itself — click a small roman numeral beside any
        line in the reader. The prose behind them is reference material in its own
        right, kept here unabridged.
      </p>
      <ul style={{ listStyle: "none", display: "grid", gap: "1.25rem" }}>
        {APPARATUS_PAGES.map((p) => (
          <li key={p.slug}>
            <Link href={`/apparatus/${p.slug}`} className="reader-h3" style={{ margin: 0 }}>
              {p.title}
            </Link>
            <p style={{ fontSize: "14px", opacity: 0.8, marginTop: "0.25rem", maxWidth: "600px" }}>
              {p.blurb}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
