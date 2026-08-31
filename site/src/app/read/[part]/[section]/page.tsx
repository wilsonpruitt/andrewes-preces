import Link from "next/link";
import { notFound } from "next/navigation";
import {
  loadSections, findSection, sectionStem, adjacentSections, PART_TITLES,
} from "@/lib/content";
import { TextReader } from "./text-reader";

export function generateStaticParams() {
  return loadSections().map((s) => {
    const [part, section] = s.id.split("/");
    return { part: part.replace("part", ""), section };
  });
}

export default async function ReadPage({
  params,
}: {
  params: Promise<{ part: string; section: string }>;
}) {
  const { part, section } = await params;
  const partNum = Number(part);
  const found = findSection(partNum, section);
  if (!found) notFound();

  const { prev, next } = adjacentSections(found);

  return (
    <div>
      <p className="section-title" style={{ marginBottom: "0.25rem" }}>
        {PART_TITLES[partNum]}
      </p>
      <h2 className="reader-h3" style={{ fontSize: "20px", marginTop: 0 }}>
        {found.label}
      </h2>

      <TextReader section={found} />

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginTop: "3rem",
          paddingTop: "1.5rem",
          borderTop: "1px solid rgba(139,105,20,0.2)",
        }}
      >
        {prev ? (
          <Link href={`/read/${prev.part}/${sectionStem(prev.id)}`} className="reader-h4">
            &larr; {prev.label}
          </Link>
        ) : (
          <span />
        )}
        {next ? (
          <Link href={`/read/${next.part}/${sectionStem(next.id)}`} className="reader-h4">
            {next.label} &rarr;
          </Link>
        ) : (
          <span />
        )}
      </div>
    </div>
  );
}
