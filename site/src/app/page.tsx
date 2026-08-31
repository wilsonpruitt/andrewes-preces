import Link from "next/link";
import { loadSections, sectionStem, PART_TITLES } from "@/lib/content";

export default function HomePage() {
  const sections = loadSections();
  const parts = [1, 2, 3] as const;

  return (
    <div>
      <p style={{ maxWidth: "640px", marginBottom: "2.5rem", fontSize: "15px", opacity: 0.85 }}>
        Lancelot Andrewes&rsquo; <em>Preces Privatae</em> — the Greek, the Latin, and the Hebrew
        where the plate sets it, beside the Wroot Press English, from the 1853 Parker text.
      </p>
      {parts.map((part) => (
        <div key={part} style={{ marginBottom: "2.5rem" }}>
          <h2 className="section-title">{PART_TITLES[part]}</h2>
          <ul style={{ listStyle: "none", display: "grid", gap: "0.4rem" }}>
            {sections
              .filter((s) => s.part === part)
              .map((s) => (
                <li key={s.id}>
                  <Link href={`/read/${part}/${sectionStem(s.id)}`} className="reader-h4">
                    {s.label}
                  </Link>
                </li>
              ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
