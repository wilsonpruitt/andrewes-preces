import Link from "next/link";
import { loadBooks, TESTAMENT_LABEL } from "@/lib/scripture";

export default function ScriptureIndex() {
  const books = loadBooks();
  const marked = books.reduce((n, b) => n + b.marked, 0);
  const identified = books.reduce((n, b) => n + b.identified, 0);

  return (
    <div>
      <h2 className="section-title">Scripture</h2>
      <p style={{ maxWidth: "660px", marginBottom: "1rem", fontSize: "15px", opacity: 0.85 }}>
        Every scriptural reference in the volume, by book — <strong>{marked}</strong> that the
        1853 plate prints, and <strong>{identified}</strong> more that it never marks and the
        notes identify.
      </p>
      <p style={{ maxWidth: "660px", marginBottom: "2rem", fontSize: "13.5px", opacity: 0.7 }}>
        The two are kept apart on purpose. A <em>mark</em> is the 1853&rsquo;s own act; an{" "}
        <em>identification</em> is this edition&rsquo;s reading — §37 (printed 374&ndash;379) runs
        six leaves whose confession is built entirely of allusion the plate never references.
        Chapter and verse stand <em>as printed</em> and are never renumbered: the volume is not on
        one Psalter, and where a note says which, it is shown.
      </p>

      {(["ot", "ap", "nt"] as const).map((t) => {
        const rows = books.filter((b) => b.testament === t);
        if (!rows.length) return null;
        return (
          <div key={t} style={{ marginBottom: "2.5rem" }}>
            <h3 className="reader-h3">{TESTAMENT_LABEL[t]}</h3>
            <ul className="scripture-book-list">
              {rows.map((b) => (
                <li key={b.slug}>
                  <Link href={`/scripture/${b.slug}`}>
                    <span className="scripture-book-name">{b.name}</span>
                    <span className="scripture-book-count">
                      {b.marked}
                      {b.identified > 0 && (
                        <span className="scripture-ident"> + {b.identified}</span>
                      )}
                    </span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        );
      })}
    </div>
  );
}
