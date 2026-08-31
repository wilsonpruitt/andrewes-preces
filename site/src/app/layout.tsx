import type { Metadata } from "next";
import Link from "next/link";
import { EB_Garamond, Cinzel, Cinzel_Decorative, Cardo } from "next/font/google";
import { Illumination } from "@/components/decorations";
import "./globals.css";

// next/font self-hosts these at build time — zero CLS, no external request.
// Cardo covers polytonic Greek and pointed Hebrew (WEB-PLAN §11); EB Garamond
// and Cinzel are kept from Milton so the two sites read as one house.
const ebGaramond = EB_Garamond({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  style: ["normal", "italic"],
  variable: "--font-eb-garamond",
  display: "swap",
});

const cinzel = Cinzel({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-cinzel",
  display: "swap",
});

const cinzelDecorative = Cinzel_Decorative({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-cinzel-decorative",
  display: "swap",
});

const cardo = Cardo({
  subsets: ["greek", "greek-ext", "hebrew", "latin"],
  weight: ["400", "700"],
  style: ["normal", "italic"],
  variable: "--font-cardo",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Andrewes — Preces Privatae",
  description:
    "A free Greek · Latin · English edition of Lancelot Andrewes' Preces Privatae, from the 1853 Parker text, with the whole apparatus and a scripture index.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const fontVars = `${ebGaramond.variable} ${cinzel.variable} ${cinzelDecorative.variable} ${cardo.variable}`;
  return (
    <html lang="en" className={fontVars}>
      <body>
        <header className="site-header">
          <div className="header-inner">
            <Link href="/" style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
              <Illumination size={54} letter="A" />
              <div>
                <h1 className="header-title">Andrewes</h1>
                <p className="header-subtitle">Preces Privatae</p>
              </div>
            </Link>
          </div>
          <nav className="site-nav">
            <Link href="/">Home</Link>
            <Link href="/scripture">Scripture</Link>
            <Link href="/apparatus">Apparatus</Link>
          </nav>
        </header>

        <main className="main-content">{children}</main>

        <footer className="site-footer">
          <p style={{ marginBottom: "0.25rem" }}>
            Lancelot Andrewes, <em>Preces Privatae</em> &middot; a Wroot Press edition
          </p>
          <p style={{ fontSize: "11px", opacity: 0.7 }}>
            The 1853 Parker text, public domain &middot; translation and encoding CC BY-NC 4.0
            &middot; MMXXVI
          </p>
        </footer>
      </body>
    </html>
  );
}
