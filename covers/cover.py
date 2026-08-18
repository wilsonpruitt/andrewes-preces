#!/usr/bin/env python3.11
"""Cover for *Preces Privatae* (Wroot Press) — the trilingual Andrewes.

Built on the same grammar as the church-in-palestine and wesley-metaphysics covers (xelatex +
tikz, a front panel and a full wrap with a computed spine, Cardo throughout) so the catalog
reads as one shelf.

✅ WILSON'S CALL, 2026-08-18: the front is TYPE-LED and shows THE PARALLEL. Not a portrait.
   The reason is the preface's own claim — *no edition currently in print, and none in the public
   domain, presents the Greek and the Latin at all*. A bishop's portrait on the front sells
   "devotional classic by a famous Anglican", which is the crowded shelf where Brightman and the
   Newman/Neale derivatives already sit and where this book has no advantage. The parallel is the
   thing nobody else has, so the parallel is what the cover shows.
   ⚠ The de Passe portrait is NOT unused — it is the frontispiece, whole, with its verse tablet.
     See prototypes/front/andrewes-frontispiece.png. Don't "restore" it to the cover.

THE SPECIMEN is Ps. xxvi. 8 at printed 356, and it is chosen for a reason worth keeping. Andrewes
says that verse twice on one leaf — in Latin at the door of the temple and again in Greek fourteen
lines later — so the two originals on this cover are THE SAME VERSE. The parallel therefore reads
instantly, with no explanation: a buyer who reads neither language can still see that the two
columns say one thing, and the English beneath says it a third time. Text is copied from the
transcripts, not retyped: part2/27-in-praedicatione-… (Latin l. 64, Greek l. 78, English l. 63).
⚠ If the transcript changes, change it here. The cover must not quote a text the book does not set.

THE PALETTE is MEASURED off the de Passe plate itself (raw/portrait/), by the house rule that a
colour is sampled and not chosen — STONE is the plate's paper, INK its deepest ink, GREY its
hatching. ⚠ DUST IS THE ONE EXCEPTION AND IS CHOSEN, because a monochrome engraving cannot supply
an accent. It is a Venetian red, and the ground for it is historical rather than personal: early
modern title pages were commonly printed in red and black, which is the pair this cover uses.

! THE BARCODE KEEP-OUT IS REAL AND HAS BEEN PAID FOR ONCE ALREADY on wesley-journals. KDP prints
  the barcode in a 2 x 1.2in box at the lower right of the BACK panel. Nothing but ground colour
  goes there. `python3.11 cover.py guides` draws it so it can be checked by eye before upload.

! PAGES drives the spine and NOTHING WARNS YOU WHEN IT IS STALE. It must be the FINAL interior
  count. 625 is the build of 2026-08-18 (introduction + frontispiece in, 0 TeX errors). If Wilson's
  read of the introduction changes its length, rebuild the interior and update this first.

! PPI must match the paper actually chosen at KDP. 0.0025 is CREAM, which is what a 625pp
  classical text wants; white is 0.002252 and would make the spine 0.14in narrower.

Usage:  python3.11 cover.py [front|wrap|guides|all]
"""
import os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

PAGES = 625          # prototypes/volume-loeb.pdf, 2026-08-18 — see the warning above
PPI = 0.0025         # cream paper, inches per page (KDP)

# Measured from raw/portrait/andrewes-depasse-1618-commons.jpg — see the docstring.
STONE = "FEF9DA"     # the plate's paper, brightest large field
INK   = "121110"     # its deepest ink, lifted off pure black so it prints as ink and not as a hole
GREY  = "ACA48B"     # its hatching, a warm mid tone
DUST  = "8A2E22"     # CHOSEN: Venetian red, the second colour of an early modern title page
GOLD  = "9C7A33"     # house gold, used only for the hairline

FONTS = r"\setmainfont{Cardo}[Ligatures=TeX]"

PREAMBLE = rf"""\documentclass{{article}}
\usepackage[xetex]{{geometry}}
\geometry{{paperwidth=__PW__bp,paperheight=__PH__bp,margin=0pt,nohead,nofoot}}
\usepackage{{fontspec}}\usepackage{{tikz}}\usetikzlibrary{{calc}}
\usepackage{{graphicx}}\usepackage{{xcolor}}
\hyphenpenalty=10000 \exhyphenpenalty=10000 \tolerance=2200 \emergencystretch=3.5em
{FONTS}
\definecolor{{stone}}{{HTML}}{{{STONE}}}
\definecolor{{ink}}{{HTML}}{{{INK}}}
\definecolor{{dust}}{{HTML}}{{{DUST}}}
\definecolor{{grey}}{{HTML}}{{{GREY}}}
\definecolor{{gold}}{{HTML}}{{{GOLD}}}
\newcommand{{\sceps}}[1]{{{{\addfontfeature{{LetterSpace=18.0}}\scshape #1}}}}
\newcommand{{\scwide}}[1]{{{{\addfontfeature{{LetterSpace=30.0}}\scshape #1}}}}
\setlength{{\parindent}}{{0pt}}\setlength{{\parskip}}{{0pt}}\pagestyle{{empty}}
\begin{{document}}
\begin{{tikzpicture}}[remember picture,overlay,every node/.style={{inner sep=0pt,outer sep=0pt}}]
\fill[stone] (current page.south west) rectangle (current page.north east);
"""
FOOTER = "\\end{tikzpicture}\n\\end{document}\n"

# The specimen, copied from the transcripts. Ps. xxvi. 8, printed 356 — the separated doublet.
GREEK_1 = r"Κύριε, ἠγάπησα εὐπρέπειαν οἴκου σου,"
GREEK_2 = r"καὶ τόπον σκηνώματος τῆς δόξης σου."
LATIN_1 = r"Domine, dilexi decorem domus Tuæ,"
LATIN_2 = r"et locum habitationis gloriæ Tuæ."
ENGLISH_1 = r"Lord, I have loved the beauty of thy house,"
ENGLISH_2 = r"and the place where thy glory dwelleth."


def front_panel():
    """The front, returned as tikz so the standalone proof and the printed wrap are one artwork.

    ! ONE DESCRIPTION, USED TWICE. A second copy of these coordinates in build_wrap is how a cover
      comes back from the printer not matching the proof — the lesson the church-in-palestine
      cover records, and it is cheaper to obey it than to relearn it.

    The grammar, top to bottom: hairline double frame / title in two lines of wide small caps /
    rule / italic English title / THE SPECIMEN, the two originals side by side above the English /
    rule / the author / the claim / the imprint. The two rules and the frame are the whole ornament.
    """
    # ⚠ THE COLUMN WIDTH AND THE TYPE SIZE ARE SOLVED TOGETHER, and the constraint is that each
    #   original must set in the BOOK'S OWN TWO SENSE-LINES. The first cut was 150bp at 10.5pt:
    #   the Greek wrapped to four lines, the Latin to three, the columns went ragged against each
    #   other and the Greek's last line printed straight through the rule beneath it. Widen and
    #   drop the size until both columns are two lines, and check by eye — nothing warns you.
    #   Second cut, 156bp at 9.4pt: the Latin came right at two lines, THE GREEK STILL WRAPPED TO
    #   FOUR and still ran through the rule. Cardo's Greek is simply wider than its Latin at the
    #   same size — measured off the proof, the Greek sense-line needs ~172bp where the Latin needs
    #   ~148. So THE TWO COLUMNS ARE NOT THE SAME WIDTH. Each is sized to the language in it, which
    #   is what the book does too, and the pair is then centred as a unit.
    GRC, LAC, GAP = 168, 148, 14        # Greek column, Latin column, gutter — 330bp inside 348
    _half = (GRC + LAC + GAP) / 2
    gx = round(-_half + GRC / 2, 2)     # centre of the Greek column
    lx = round(-_half + GRC + GAP + LAC / 2, 2)   # centre of the Latin column
    SIZE, LEAD = 9.0, 12.6
    # Balanced by eye off the proof: the band between the subtitle and the foot rule is 250bp and
    # the specimen is ~112bp of it, so it sits with a little more air above than below.
    ORIG_Y = 312       # top of the originals
    RULE_Y = 360       # the hairline between the originals and the English
    ENG_Y = 374        # top of the English
    return (
        # frame
        r"\draw[gold,line width=0.5pt] ([xshift=-180bp,yshift=-36bp]ftn) rectangle ([xshift=180bp,yshift=36bp]fb);"
        r"\draw[dust,line width=1.2pt] ([xshift=-174bp,yshift=-42bp]ftn) rectangle ([xshift=174bp,yshift=42bp]fb);"
        # title
        r"\node[anchor=north,align=center,text=ink,font=\fontsize{31}{37}\selectfont] at ([yshift=-104bp]ftn) {\scwide{Preces}};"
        r"\node[anchor=north,align=center,text=ink,font=\fontsize{31}{37}\selectfont] at ([yshift=-146bp]ftn) {\scwide{Privatae}};"
        r"\draw[dust,line width=0.7pt] ([xshift=-96bp,yshift=-206bp]ftn) -- ([xshift=96bp,yshift=-206bp]ftn);"
        r"\node[anchor=north,align=center,text=ink,font=\itshape\fontsize{15}{20}\selectfont] at ([yshift=-228bp]ftn) {Private Prayers};"
        # the specimen — the two originals as a parallel, then the English beneath
        rf"\node[anchor=north,align=center,text width={GRC}bp,text=ink,font=\fontsize{{{SIZE}}}{{{LEAD}}}\selectfont] "
        rf"at ([xshift={gx}bp,yshift=-{ORIG_Y}bp]ftn) {{{GREEK_1}\\{GREEK_2}}};"
        rf"\node[anchor=north,align=center,text width={LAC}bp,text=ink,font=\fontsize{{{SIZE}}}{{{LEAD}}}\selectfont] "
        rf"at ([xshift={lx}bp,yshift=-{ORIG_Y}bp]ftn) {{{LATIN_1}\\{LATIN_2}}};"
        rf"\draw[grey,line width=0.4pt] ([xshift=-62bp,yshift=-{RULE_Y}bp]ftn) -- ([xshift=62bp,yshift=-{RULE_Y}bp]ftn);"
        rf"\node[anchor=north,align=center,text width=330bp,text=ink,font=\itshape\fontsize{{11}}{{15}}\selectfont] "
        rf"at ([yshift=-{ENG_Y}bp]ftn) {{{ENGLISH_1}\\{ENGLISH_2}}};"
        # foot
        r"\draw[dust,line width=0.7pt] ([xshift=-96bp,yshift=150bp]fb) -- ([xshift=96bp,yshift=150bp]fb);"
        r"\node[anchor=south,text=ink,font=\fontsize{14}{17}\selectfont] at ([yshift=112bp]fb) {\scwide{Lancelot Andrewes}};"
        r"\node[anchor=south,align=center,text=grey,font=\fontsize{9.5}{12.5}\selectfont] at ([yshift=82bp]fb) "
        r"{\sceps{Greek · Latin · Hebrew}};"
        r"\node[anchor=south,align=center,text=grey,font=\itshape\fontsize{9.5}{12}\selectfont] at ([yshift=66bp]fb) "
        r"{with a new English translation};"
        r"\node[anchor=south,text=dust,font=\fontsize{11}{13}\selectfont] at ([yshift=54bp]fb) {\sceps{Wroot Press}};"
    )


def blurb():
    p1 = (r"Lancelot Andrewes kept a book of prayers in his own hand\,---\,in Greek, in Latin and in "
          r"Hebrew\,---\,and did not publish it. It is among the most private documents the English "
          r"Church has produced, and it has never been generally available in the languages he wrote "
          r"it in. No edition now in print, and none in the public domain, presents the Greek and the "
          r"Latin at all.")
    p2 = (r"This edition sets out one witness whole\,---\,the text printed at Oxford in 1853, "
          r"reprinting the Sheldonian edition of 1675\,---\,and puts a new English translation on the "
          r"facing page, one English line to one line of the original, at the same indentation, so a "
          r"reader can run a finger down the page and stay in step. Where the printed page is wrong "
          r"it is left wrong and the note says so; where Hebrew stands in the text it is kept, and "
          r"translated. An apparatus at the foot of each opening records what other witnesses read.")
    p3 = (r"The prayers are not, for the most part, original composition, and Andrewes does not "
          r"pretend they are. What he kept was closer to a commonplace book of prayer: Scripture, the "
          r"Greek and Latin liturgies, the creeds, the Fathers, and\,---\,without apology or any "
          r"change of voice\,---\,Cicero and Seneca. The work is in what he took, what he left, and "
          r"what he set beside what, and it is everywhere.")
    p4 = (r"Lancelot Andrewes (1555--1626) was Bishop of Chichester, of Ely and of Winchester, and "
          r"one of the translators of the Authorised Version.")
    return [p1, p2, p3, p4]


def render(tex, pw, ph, name):
    tex = PREAMBLE.replace("__PW__", str(pw)).replace("__PH__", str(ph)) + tex + FOOTER
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, "c.tex"), "w").write(tex)
        r = None
        for _ in range(2):
            r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "c.tex"],
                               cwd=td, capture_output=True, text=True)
        if not os.path.exists(os.path.join(td, "c.pdf")):
            sys.stderr.write((r.stdout or "")[-4000:])
            raise SystemExit(f"xelatex failed: {name}")
        dst = os.path.join(OUT, name)
        shutil.copy(os.path.join(td, "c.pdf"), dst)
    return dst


def _png(pdf, dpi):
    png = pdf[:-4] + ".png"
    subprocess.run(["/usr/local/bin/pdftoppm", "-png", "-r", str(dpi), "-singlefile", pdf, png[:-4]],
                   check=True)


def build_front():
    body = (r"\coordinate (ftn) at (current page.north);"
            r"\coordinate (fb) at (current page.south);") + front_panel()
    pdf = render(body, 432, 648, "front.pdf")
    _png(pdf, 220)
    print("front -> out/front.pdf + png")


def build_wrap(guides=False):
    spine = round(PAGES * PPI * 72, 4)
    full_w = round(18 + 432 + spine + 432, 4)
    full_h = 666
    fcx = round(9 + 432 + spine + 216, 4)
    sx = round(-(full_w / 2) + (9 + 432 + spine / 2), 4)
    bl = blurb()
    # KDP barcode keep-out, lower right of the BACK panel: 2 x 1.2in plus a 0.25in margin.
    keep_w, keep_h = 2 * 72, 1.2 * 72
    keep_x = round(9 + 432 - 0.25 * 72 - keep_w, 4)
    keep_y = round(9 + 0.25 * 72, 4)
    guide = ""
    if guides:
        guide = (rf"\draw[red,dashed,line width=1pt] ([xshift={keep_x}bp,yshift={keep_y}bp]current page.south west) "
                 rf"rectangle ([xshift={keep_x + keep_w}bp,yshift={keep_y + keep_h}bp]current page.south west);"
                 rf"\node[red,font=\fontsize{{9}}{{11}}\selectfont,anchor=south west] at "
                 rf"([xshift={keep_x}bp,yshift={keep_y + keep_h + 4}bp]current page.south west) {{KDP barcode keep-out}};")
    body = rf"""
\coordinate (ftn) at ([xshift={fcx}bp,yshift=-9bp]current page.north west);
\coordinate (fb)  at ([xshift={fcx}bp,yshift=9bp]current page.south west);
% ===== BACK PANEL =====
\node[anchor=north west,text width=326bp,align=justify,text=ink]
  at ([xshift=62bp,yshift=-104bp]current page.north west) {{%
  {{\fontsize{{9.6}}{{13.8}}\selectfont {bl[0]}\par}}%
  \vspace{{8pt}}\hbox{{\color{{dust}}\vrule height0.7pt width78bp}}\vspace{{9pt}}\par
  {{\fontsize{{9.6}}{{13.8}}\selectfont {bl[1]}\par}}%
  \vspace{{9pt}}{{\fontsize{{9.6}}{{13.8}}\selectfont {bl[2]}\par}}%
  \vspace{{10pt}}{{\itshape\fontsize{{9}}{{12.5}}\selectfont {bl[3]}\par}}%
}};
\node[anchor=south west,text=dust] at ([xshift=62bp,yshift=150bp]current page.south west)
  {{{{\fontsize{{11}}{{13}}\selectfont \sceps{{Wroot Press}}}}}};
{guide}
% ===== SPINE =====
\node[rotate=-90,anchor=center,text=ink] at ([xshift={sx}bp,yshift=96bp]current page.center)
  {{{{\fontsize{{15}}{{18}}\selectfont \sceps{{Preces Privatae}}}}}};
\node[rotate=-90,anchor=center,text=grey] at ([xshift={sx}bp,yshift=-132bp]current page.center)
  {{{{\fontsize{{12}}{{14}}\selectfont \sceps{{Andrewes}}}}}};
\node[rotate=-90,anchor=center,text=dust] at ([xshift={sx}bp,yshift=92bp]current page.south)
  {{{{\fontsize{{9}}{{11}}\selectfont \sceps{{Wroot Press}}}}}};
% ===== FRONT PANEL =====
""" + front_panel()
    name = "wrap-guides" if guides else "wrap"
    pdf = render(body, full_w, full_h, f"{name}.pdf")
    _png(pdf, 150)
    print(f"{name} -> {round(full_w/72,3)}x{round(full_h/72,3)}in, "
          f"spine {round(spine/72,3)}in at {PAGES}pp on {'cream' if PPI==0.0025 else 'white'}")


if __name__ == "__main__":
    args = sys.argv[1:]
    mode = next((a for a in args if a in ("front", "wrap", "guides", "all")), "all")
    if mode in ("front", "all"):
        build_front()
    if mode in ("wrap", "all"):
        build_wrap()
    if mode == "guides":
        build_wrap(guides=True)
