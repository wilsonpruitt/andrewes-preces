import Link from "next/link";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { APPARATUS_PAGES, loadApparatusPage } from "@/lib/apparatus-pages";

export function generateStaticParams() {
  return APPARATUS_PAGES.map((p) => ({ slug: p.slug }));
}

export default async function ApparatusPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const page = loadApparatusPage(slug);
  if (!page) notFound();

  return (
    <div>
      <Link href="/apparatus" className="reader-h4">
        &larr; The apparatus
      </Link>
      <div className="apparatus-prose" style={{ marginTop: "1.5rem" }}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{page.body}</ReactMarkdown>
      </div>
    </div>
  );
}
