"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { checkFold, fold, type FoldTest } from "@/lib/fold";
import { LAYER_LABEL, type LayerKey } from "@/lib/content";

// [page, line, lang, display text, folded text]
type Row = [number, number, string, string, string];

interface Index {
  foldTests: FoldTest[];
  lines: Row[];
}

const MAX_RESULTS = 200;

export function SearchClient({ hrefs }: { hrefs: Record<string, string> }) {
  const [index, setIndex] = useState<Index | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [drift, setDrift] = useState<FoldTest[]>([]);
  const [q, setQ] = useState("");
  const [lang, setLang] = useState<string>("all");

  // Fetched, not imported: at 1.6MB this must not be bundled into the page.
  useEffect(() => {
    let live = true;
    fetch("/search-index.json")
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((data: Index) => {
        if (!live) return;
        setIndex(data);
        setDrift(checkFold(data.foldTests));
      })
      .catch((e) => live && setError(String(e)));
    return () => {
      live = false;
    };
  }, []);

  const folded = useMemo(() => fold(q), [q]);

  const results = useMemo(() => {
    if (!index || folded.length < 2) return [];
    const out: Row[] = [];
    for (const row of index.lines) {
      if (lang !== "all" && row[2] !== lang) continue;
      if (row[4].includes(folded)) {
        out.push(row);
        if (out.length >= MAX_RESULTS) break;
      }
    }
    return out;
  }, [index, folded, lang]);

  return (
    <div>
      <input
        className="search-input"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search the Greek, the Latin, the English…"
        autoFocus
      />
      <p className="search-hint">
        Accents and breathings are folded, so <code>αγαπη</code> finds ἀγάπην;{" "}
        <code>coelum</code> finds <em>cœlum</em> and <code>iesum</code> finds{" "}
        <em>Jesum</em>; Hebrew is matched without its points.
      </p>

      <div className="view-toggle" style={{ marginBottom: "1.25rem" }}>
        {(["all", "gr", "la", "en"] as const).map((k) => (
          <button
            key={k}
            className={`view-btn ${lang === k ? "active" : ""}`}
            onClick={() => setLang(k)}
          >
            {k === "all" ? "All" : LAYER_LABEL[k as LayerKey]}
          </button>
        ))}
      </div>

      {drift.length > 0 && (
        <p className="search-drift">
          ⚠ The browser&rsquo;s folding disagrees with the index on{" "}
          {drift.length} case{drift.length > 1 ? "s" : ""} (e.g.{" "}
          <code>{drift[0].in}</code> &rarr; <code>{fold(drift[0].in, !!drift[0].hebrew)}</code>,
          index expects <code>{drift[0].out}</code>). Results may be incomplete —
          <code> tools/search_fold.py</code> and <code>src/lib/fold.ts</code> have drifted.
        </p>
      )}
      {error && <p className="search-drift">Could not load the index: {error}</p>}
      {!index && !error && <p style={{ opacity: 0.7 }}>Loading the index…</p>}

      {index && folded.length >= 2 && (
        <p className="search-count">
          {results.length === MAX_RESULTS ? `first ${MAX_RESULTS}` : results.length}{" "}
          {results.length === 1 ? "line" : "lines"}
        </p>
      )}

      <ul className="search-results">
        {results.map(([page, line, l, text], i) => {
          const href = hrefs[page];
          return (
            <li key={i} className="search-result">
              <span className="search-where">
                {href ? (
                  <Link href={`${href}#p${page}.${line}`}>
                    printed {page}. {line}
                  </Link>
                ) : (
                  <>
                    printed {page}. {line}
                  </>
                )}
                <span className="scripture-flag">{LAYER_LABEL[l as LayerKey] ?? l}</span>
              </span>
              <p className={`search-text lang-${l}`} data-lang={l}>
                {text}
              </p>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
