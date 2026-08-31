"use client";

import { useEffect, useState } from "react";
import type { Line, LayerKey, Section, Span, Unit } from "@/lib/content";
import { LAYER_LABEL, LAYER_ORDER, sectionLayers, sectionUnits } from "@/lib/content";

const MOBILE_QUERY = "(max-width: 900px)";
const ORIGINAL_KEY = "andrewes.originalLang";

// The reader is a language ARRAY, not a fixed pair (Milton's content.ts
// generalization, WEB-PLAN §0/§7) — view modes are generated from whatever
// layers this section actually carries, never hardcoded to two or three.
export function TextReader({ section }: { section: Section }) {
  const layers = sectionLayers(section);
  const units = sectionUnits(section);
  const multi = layers.length > 1;

  const [viewMode, setViewMode] = useState<string>(multi ? "parallel" : layers[0]);
  const [mobile, setMobile] = useState(false);
  // On a phone, "Parallel" is a lie (WEB-PLAN §7): fall back to ONE original +
  // English, with a picker for which original when the section offers more
  // than one (Part I's Greek/Latin). Never a horizontal-scroll 3-up.
  const originals = layers.filter(
    (l): l is Exclude<LayerKey, "en"> => l !== "en"
  );
  const [mobileOriginal, setMobileOriginal] = useState<LayerKey>(originals[0]);

  useEffect(() => {
    const mq = window.matchMedia(MOBILE_QUERY);
    setMobile(mq.matches);
    const onChange = (e: MediaQueryListEvent) => setMobile(e.matches);
    mq.addEventListener("change", onChange);
    try {
      const saved = localStorage.getItem(ORIGINAL_KEY);
      const match = originals.find((o) => o === saved);
      if (match) setMobileOriginal(match);
    } catch {}
    return () => mq.removeEventListener("change", onChange);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(ORIGINAL_KEY, mobileOriginal);
    } catch {}
  }, [mobileOriginal]);

  const modes = [
    ...(multi ? [{ key: "parallel", label: "Parallel" }] : []),
    ...layers.map((l) => ({ key: l, label: LAYER_LABEL[l] })),
  ];

  const showMobileInterleave = mobile && viewMode === "parallel" && originals.length > 0;
  const activeKeys: LayerKey[] = showMobileInterleave
    ? ([mobileOriginal, ...(layers.includes("en") ? (["en"] as LayerKey[]) : [])] as LayerKey[])
    : viewMode === "parallel"
    ? layers
    : [viewMode as LayerKey];

  return (
    <>
      <div className="view-toggle">
        {modes.map((m) => (
          <button
            key={m.key}
            onClick={() => setViewMode(m.key)}
            className={`view-btn ${viewMode === m.key ? "active" : ""}`}
          >
            {m.label}
          </button>
        ))}
        {showMobileInterleave && originals.length > 1 && (
          <select
            value={mobileOriginal}
            onChange={(e) => setMobileOriginal(e.target.value as LayerKey)}
            className="view-btn"
            style={{ marginLeft: "auto" }}
            aria-label="Original language"
          >
            {originals.map((o) => (
              <option key={o} value={o}>
                {LAYER_LABEL[o]}
              </option>
            ))}
          </select>
        )}
      </div>

      {units.map((unit) => (
        <UnitBlock key={unit.pages.join("-")} unit={unit} activeKeys={activeKeys} />
      ))}
    </>
  );
}

function UnitBlock({ unit, activeKeys }: { unit: Unit; activeKeys: LayerKey[] }) {
  // A unit may not carry every active key (§7: the mode collapses PER PAGE,
  // not per section — most of Parts II-III have no Greek at all).
  const present = LAYER_ORDER.filter((k) => activeKeys.includes(k) && unit.layers[k]);
  if (present.length === 0) return null;

  const pageLabel =
    unit.pages.length === 2 ? `Printed ${unit.pages[0]} · ${unit.pages[1]}` : `Printed ${unit.pages[0]}`;

  return (
    <div style={{ marginBottom: "2.5rem" }}>
      <div className="page-marker page-marker-margin" style={{ marginBottom: "0.5rem" }}>
        {pageLabel}
      </div>
      <div className="parallel-grid" style={{ ["--lang-count" as string]: present.length }}>
        {present.map((k) => (
          <div key={k}>
            <div className="section-title" style={{ fontSize: "12px" }}>
              {LAYER_LABEL[k]}
            </div>
            <div className="text-column" data-lang={k}>
              {(unit.layers[k] as Line[]).map((line, i) => (
                <LineRow key={i} line={line} page={unit.pageOf[k]!} lang={k} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function LineRow({ line, page, lang }: { line: Line; page: number; lang: LayerKey }) {
  if (line.break) return <div className="pv-break" aria-hidden />;
  const id = `p${page}.${line.n}`;
  return (
    <div
      id={id}
      className={`pv-line lang-${lang}`}
      style={{ paddingLeft: `${(line.indent ?? 0) * 0.3}em` }}
    >
      <a href={`#${id}`} className="pv-line-num" aria-label={`line ${line.n}`}>
        {line.n}
      </a>
      {(line.spans ?? []).map((s, i) => (
        <SpanNode key={i} span={s} />
      ))}
    </div>
  );
}

function SpanNode({ span }: { span: Span }) {
  switch (span.kind) {
    case "text":
      return <>{span.text}</>;
    case "strong":
      return (
        <strong>
          {(span.children ?? []).map((c, i) => (
            <SpanNode key={i} span={c} />
          ))}
        </strong>
      );
    case "em":
      return <em>{span.text}</em>;
    case "hebrew":
      return (
        <span className="pv-hebrew" dir="rtl" style={{ unicodeBidi: "isolate" }}>
          {span.text}
        </span>
      );
    case "sup":
      return <sup className="pv-sup">{span.text}</sup>;
    case "unclear":
      return (
        <span className="pv-unclear" title="unclear in the plate">
          ?
        </span>
      );
    case "supplied":
      return <span className="pv-supplied">{span.text}</span>;
    case "gap":
      return <span className="pv-gap" style={{ width: `${(span.width ?? 1) * 0.3}em` }} />;
    default:
      return null;
  }
}
