import Link from "next/link";
import { notFound } from "next/navigation";
import { readerHref } from "@/lib/content";
import { byChapter, loadBook, loadBooks } from "@/lib/scripture";
import { renderMarkup } from "@/lib/markup";

export function generateStaticParams() {
  return loadBooks().map((b) => ({ book: b.slug }));
}

export default async function ScriptureBookPage({
  params,
}: {
  params: Promise<{ book: string }>;
}) {
  const { book } = await params;
  const meta = loadBooks().find((b) => b.slug === book);
  const entries = loadBook(book);
  if (!meta || !entries) notFound();

  const isPsalms = book === "ps";

  return (
    <div>
      <Link href="/scripture" className="reader-h4">
        &larr; Scripture
      </Link>
      <h2 className="section-title" style={{ marginTop: "1.25rem" }}>
        {meta.name}
      </h2>
      <p style={{ fontSize: "14px", opacity: 0.8, marginBottom: "1.5rem" }}>
        {meta.marked} marked by the plate
        {meta.identified > 0 && <> · {meta.identified} identified in the notes</>}
      </p>

      {isPsalms && (
        <p className="scripture-caveat">
          ⚠ <strong>The volume is not on one Psalter.</strong> It cites plain Authorised
          numbering, plain Vulgate, the Prayer Book&rsquo;s, and at printed 344 and 353 a hybrid
          that sets the Vulgate&rsquo;s verse-figure under the Hebrew psalm-number. Every figure
          below stands <em>exactly as printed</em>; nothing has been converted. Where the notes
          pass recorded which Psalter a figure belongs to, the entry is marked{" "}
          <span className="scripture-flag">numbering</span>.
        </p>
      )}

      {byChapter(entries).map(([chapter, rows]) => (
        <div key={chapter} style={{ marginBottom: "1.75rem" }}>
          <h3 className="reader-h4" style={{ marginBottom: "0.5rem" }}>
            {meta.name} {chapter}
          </h3>
          <ul className="scripture-entry-list">
            {rows.map((e, i) => {
              const href = readerHref(e.page, e.line);
              return (
                <li key={i} className={`scripture-entry src-${e.source}`}>
                  <span className="scripture-printed">{e.printed}</span>
                  <span className="scripture-where">
                    {href ? (
                      <Link href={href}>
                        printed {e.page}
                        {e.line > 0 && <>. {e.line}</>}
                      </Link>
                    ) : (
                      <>printed {e.page}</>
                    )}
                  </span>
                  {e.source === "identified" && (
                    <span
                      className="scripture-flag flag-ident"
                      title={
                        e.band === "R"
                          ? "identified in an explanatory note; the plate does not mark it"
                          : "identified in the notes; the plate does not mark it"
                      }
                    >
                      identified
                    </span>
                  )}
                  {e.numbering && (
                    <span className="scripture-flag" title="the note states which Psalter this figure belongs to">
                      numbering
                    </span>
                  )}
                  {e.plateFigure && (
                    <span className="scripture-flag flag-plate" title="the plate's own figure, kept as printed">
                      as printed
                    </span>
                  )}
                  {e.situation && (
                    <p className="scripture-situation">{renderMarkup(e.situation)}</p>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      ))}
    </div>
  );
}
