import Link from "next/link";
import { readerHref, sectionForPage, PART_TITLES } from "@/lib/content";
import { loadLinks, RECENSION_PAIRS } from "@/lib/links";
import { renderMarkup } from "@/lib/markup";

function PageRange({ from, to }: { from: number; to: number }) {
  const href = readerHref(from, 0);
  const label = from === to ? `printed ${from}` : `printed ${from}–${to}`;
  return href ? (
    <Link href={href} className="synopsis-range">
      {label}
    </Link>
  ) : (
    <span className="synopsis-range">{label}</span>
  );
}

export default function SynopsisPage() {
  const links = loadLinks();
  const partOf = (n: number) => sectionForPage(n)?.part;
  // Links that cross from one part into another — the volume recognising
  // itself across the codex order that separates the twins.
  const cross = links
    .map((l) => ({ ...l, to: l.to.filter((t) => partOf(t) && partOf(t) !== partOf(l.from)) }))
    .filter((l) => l.to.length > 0)
    .sort((a, b) => a.from - b.from);

  return (
    <div>
      <h2 className="section-title">Synopsis</h2>
      <p style={{ maxWidth: "700px", fontSize: "15px", marginBottom: "1rem" }}>
        Part III is the <strong>Harley recension</strong> of Part II&rsquo;s penitential matter.
        The codex order forces the twins a hundred pages apart, and the printed edition rightly
        keeps them there. Here they stand together.
      </p>
      <p className="synopsis-caveat">
        ⚠ <strong>The columns are not aligned line for line, and must not be.</strong> These are
        two recensions, not two printings: measured against each other they share ten identical
        Latin lines out of 157 and 208 between §23 and §1, and <em>none at all</em> between §17
        and §2 — because §17 is a schema of headings and brace catalogues and §2 is that schema
        written out as prayer. Identical Latin keeps identical English; divergences stand as
        divergences and are never conformed.
      </p>

      {RECENSION_PAIRS.map((p) => (
        <section key={p.id} className="synopsis-pair">
          <h3 className="reader-h3">{p.title}</h3>
          <div className="synopsis-cols">
            <div>
              <div className="section-title" style={{ fontSize: "11px" }}>
                {PART_TITLES[2].split("—")[0].trim()}
              </div>
              <p className="synopsis-side">{p.a.label}</p>
              <PageRange from={p.a.pages[0]} to={p.a.pages[1]} />
            </div>
            <div>
              <div className="section-title" style={{ fontSize: "11px" }}>
                {PART_TITLES[3].split("—")[0].trim()}
              </div>
              <p className="synopsis-side">{p.b.label}</p>
              <PageRange from={p.b.pages[0]} to={p.b.pages[1]} />
            </div>
          </div>
          <p className="synopsis-warrant">{p.warrant}</p>
        </section>
      ))}

      <h3 className="reader-h3" style={{ marginTop: "3rem" }}>
        Where the volume names itself
      </h3>
      <p style={{ maxWidth: "700px", fontSize: "14px", opacity: 0.85, marginBottom: "1.5rem" }}>
        {cross.length} places where a note on one page points at another <em>in a different
        part</em> — a phrase returning in a new dress, a verse cited under two different numbers,
        a catalogue standing again with its antitheses stripped out. Invisible in a codex, and
        the reason this edition is worth having on a screen.
      </p>
      <ul className="synopsis-link-list">
        {cross.map((l, i) => (
          <li key={i}>
            <div className="synopsis-link-head">
              <PageRange from={l.from} to={l.from} />
              <span className="synopsis-arrow">↔</span>
              {l.to.map((t) => (
                <span key={t}>
                  <PageRange from={t} to={t} />{" "}
                </span>
              ))}
              {l.band === "R" && <span className="scripture-flag">note</span>}
            </div>
            <p className="synopsis-note">{renderMarkup(l.note)}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
