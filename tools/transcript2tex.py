#!/usr/bin/env python3
"""Build the 1675 MIRROR — Greek verso, Latin recto, English register at the foot.

This is the edition layout (prototype B), as against the continuous proofing copy
built by tools/proof2tex.py. It emits one TeX fragment per printed page into
prototypes/fragments/, then a driver that lays those fragments out one edition
page per 1853 page:

    python3.11 tools/transcript2tex.py             # whole volume -> volume-mirror.tex
    python3.11 tools/transcript2tex.py --part 1    # Part I only  -> part1-mirror.tex
    python3.11 tools/transcript2tex.py --fit 1     # read back part1-mirror.fit

Build with:  cd prototypes && xelatex <name>.tex

Two structures, not one. **Part I is a true mirror**: printed 1 stands alone, then
every Greek verso 2N faces its Latin recto 2N+1, and the English of the Greek page
is split across the foot of the spread (h1 under the Greek, h2 under the Latin).
**Parts II and III are not mirrored at all** — each printed page carries a single
language and its own English register beneath it.

The edition carries ITS OWN continuous folios, and the 1853 page runs as a
shoulder-note in the inner head of every leaf (Wilson's ruling, 2026-08-05; the
reasoning is EDITION-SHAPE.md 6a). An earlier draft made the 1853 number the
edition's number, which was elegant until a page ran to two leaves and printed a
duplicate folio.

⚠ THE MIRROR'S DISCIPLINE BELONGS TO PART I ALONE. There a printed page must
occupy exactly one leaf, because overflow desynchronises verso from recto for
everything after it; `\versoalign` forces every Greek page onto a left-hand leaf
so the damage stops at the spoilt spread. Parts II--III have no facing page to
fall out of, so a second leaf there is bulk, not damage. Every leaf is
instrumented and `--fit` reads the record back; the line that matters is whether
a Part I Greek page landed on a recto. Nothing is silently scaled to make a page
fit — that is a typesetting decision, not a scripting one.

Parsing and rendering are imported from proof2tex so the two builders cannot
drift: both the apparatus cut-off (a trailing `## Translator's flags` must never
flow into the last printed page) and the twice-marked-page fix (continue the
block, never restart it) live in one place now.
"""
import argparse
import re
from pathlib import Path

from proof2tex import (
    OUT_DIR, PART_TITLES, ROOT, parse_pages, render_block, render_line,
    sections_for, tex_escape, tex_inline,
)

FRAG = OUT_DIR / "fragments"

# The M2 sample split three pages at a unit boundary so prototype B could show a
# mid-page break. proto-{a,b,c}.tex still \input those a/b fragments by name, so
# they are still emitted; the volume driver does not use them.
SPLITS = {
    ("gr", 32): "ΟΙΚΤΙΡΜΟΝ", ("la", 33): "MISERICORS", ("en", 32): "MERCIFUL",
    ("gr", 40): "ΑΙΡΩ", ("la", 41): "Attollo", ("en", 40): "I LIFT UP",
    ("gr", 42): "סיג", ("la", 43): "SEPES", ("en", 42): "סיג",
}

FIT = re.compile(r"^([SEB])\s+(\d+)(?:\s+(\d+))?\s*$")


def volume_pages(parts):
    """printed page -> {'part', 'layer', 'body', 'en', 'label'}.

    A printed page may be marked in two consecutive sections (a section closing
    and the next opening on the same leaf — printed 275, 364 and some thirty
    others). In the continuous proof those are two labelled blocks; in the mirror
    they are ONE leaf and must be merged in reading order, or the page is set
    twice and every following spread is off by one.
    """
    pages = {}
    for part in parts:
        for tr, en, label in sections_for(part):
            tr_blocks = parse_pages(tr)
            en_blocks = parse_pages(en) if en else {}
            for n in sorted(set(tr_blocks) | set(en_blocks)):
                slot = pages.setdefault(n, {
                    "part": part, "layer": None, "body": [], "en": [],
                    "label": label,
                })
                if n in tr_blocks:
                    layer, lines = tr_blocks[n]
                    if slot["body"]:
                        slot["body"].append("")
                    else:
                        slot["layer"] = layer
                    slot["body"].extend(lines)
                if n in en_blocks:
                    if slot["en"]:
                        slot["en"].append("")
                    slot["en"].extend(en_blocks[n][1])
    return pages


def write_fragment(have: set, name: str, lines) -> bool:
    """Write a fragment and record its name. A fragment that renders to nothing is
    not written, and the driver must not \\input a name that is not in `have` —
    xelatex stops dead on a missing file."""
    body = render_block(lines)
    if not body:
        return False
    (FRAG / f"{name}.tex").write_text(body + "\n")
    have.add(name)
    return True


def split_halves(lines):
    """Cut an English page at the blank line nearest its middle, for the two feet
    of a Part I spread. Mechanical, as the prototype README records — a real
    edition would cut at a sense boundary.

    The page's own leading and trailing blanks are dropped before measuring: they
    sit within reach of the midpoint on a short page and win the nearest-blank
    contest, which hands one foot the whole register and the other nothing
    (printed 90, 206 and 248 all did exactly that). A page too short to divide
    keeps its register whole under the verso."""
    core = list(lines)
    while core and not core[0].strip():
        core.pop(0)
    while core and not core[-1].strip():
        core.pop()
    if len(core) < 4:
        return core, []
    mid = len(core) // 2
    blanks = [i for i, l in enumerate(core)
              if not l.strip() and 0 < i < len(core) - 1 and abs(i - mid) <= 4]
    cut = min(blanks, key=lambda i: abs(i - mid)) if blanks else mid
    return core[:cut], core[cut:]


def emit_fragments(pages):
    FRAG.mkdir(parents=True, exist_ok=True)
    have = set()
    for n, slot in sorted(pages.items()):
        if slot["body"]:
            write_fragment(have, f"{slot['layer']}{n:03d}", slot["body"])
        if slot["en"]:
            write_fragment(have, f"en{n:03d}", slot["en"])
            if slot["part"] == 1 and n % 2 == 0:
                h1, h2 = split_halves(slot["en"])
                write_fragment(have, f"en{n:03d}-h1", h1)
                write_fragment(have, f"en{n:03d}-h2", h2)
    # legacy M2 a/b splits, for the three prototype drivers
    for (kind, page), prefix in SPLITS.items():
        src = pages.get(page, {})
        lines = src.get("en" if kind == "en" else "body", [])
        idx = next((i for i, l in enumerate(lines) if l.strip().startswith(prefix)), None)
        if idx is None:
            continue
        write_fragment(have, f"{kind}{page:03d}a", lines[:idx])
        write_fragment(have, f"{kind}{page:03d}b", lines[idx:])
    return have


def short_label(label: str) -> str:
    """A running head has one line. Part II's own headings run to 200 characters
    (§41 names four works and a cross-reference), so the head keeps the section
    number and its first named work and drops the rest."""
    head = re.split(r"\s+[+·(\u2192]|\s+—\s+", label, maxsplit=1)[0].strip()
    if len(head) > 58:
        head = head[:57].rstrip() + "\u2026"
    head = head.rstrip(" ,;:")
    # Cutting mid-title can strand an opening italic marker, which then sets as a
    # literal asterisk because the emphasis regex needs a pair. Close it.
    return head + "*" if head.count("*") % 2 else head


def leaf(n: int, slot, en_frag: str | None, body_frag: str | None, verso=False):
    """One edition leaf: its 1853 shoulder-note, its text, and an English register.

    `verso=True` forces the leaf onto a left-hand page, inserting a blank if the
    count has drifted. Only Part I's Greek pages ask for it — that is where the
    mirror lives — and it makes an overflow self-healing: the spread that ran over
    is spoilt, but the book realigns at the next Greek page instead of staying
    flipped for two hundred leaves.
    """
    out = [r"\versoalign" if verso else r"\clearpage",
           r"\markright{%d}" % n, r"\fitstart{%d}" % n]
    if body_frag:
        out.append(r"{\small\input{fragments/%s}}" % body_frag)
    if en_frag:
        out.append(r"\registerrule")
        out.append(r"{\footnotesize\itshape\input{fragments/%s}}" % en_frag)
    out.append(r"\fitend{%d}" % n)
    return out


def build_driver(parts, pages, have):
    body, part_seen, label_seen = [], None, None
    ordered = sorted(pages)
    skip = set()
    for n in ordered:
        if n in skip:
            continue
        slot = pages[n]
        if slot["part"] != part_seen:
            part_seen = slot["part"]
            label_seen = None
            body.append(r"\parthead{%s}" % PART_TITLES[part_seen])
        if slot["label"] != label_seen:
            label_seen = slot["label"]
            body.append(r"\sethead{%s}" % tex_inline(short_label(label_seen)))
        recto = pages.get(n + 1)
        mirrored = (
            slot["part"] == 1 and slot["layer"] == "gr" and n % 2 == 0
            and recto and recto["layer"] == "la" and recto["part"] == 1
        )
        def frag(name):
            return name if name in have else None

        if mirrored:
            body += [r"%% ---------- spread %d | %d ----------" % (n, n + 1)]
            body += leaf(n, slot, frag(f"en{n:03d}-h1"), frag(f"gr{n:03d}"), verso=True)
            body += leaf(n + 1, recto, frag(f"en{n:03d}-h2"), frag(f"la{n + 1:03d}"))
            skip.add(n + 1)
        else:
            body += leaf(n, slot, frag(f"en{n:03d}"), frag(f"{slot['layer']}{n:03d}"))
    return "\n".join(body)


def report_fit(name: str):
    path = OUT_DIR / f"{name}.fit"
    if not path.exists():
        raise SystemExit(f"no fit record at {path} — build {name}.tex first")
    start, end, blanks = {}, {}, []
    for line in path.read_text().splitlines():
        m = FIT.match(line.strip())
        if not m:
            continue
        if m.group(1) == "B":
            blanks.append(int(m.group(2)))
        else:
            (start if m.group(1) == "S" else end)[int(m.group(2))] = int(m.group(3))
    over = sorted(n for n in start if end.get(n, start[n]) != start[n])
    # Which printed pages are supposed to be Part I versos — the only leaves whose
    # side carries meaning. Read from the sources, not assumed from parity.
    versos = {n for n, slot in volume_pages([1]).items()
              if slot["layer"] == "gr" and n % 2 == 0}
    flipped = sorted(n for n in start if n in versos and start[n] % 2)

    print(f"{len(start)} printed pages on {max(end.values(), default=0)} leaves")
    print(f"  {len(over)} run to a second leaf: "
          + (", ".join(str(n) for n in over) if over else "none"))
    print(f"  {len(blanks)} blank leaves spent keeping Part I's Greek on a verso"
          + (f" (after leaf {', '.join(str(b) for b in blanks)})" if blanks else ""))
    # The mirror is the only place a second leaf costs more than paper.
    print(f"  {len(flipped)} Part I Greek pages landed on a RECTO — the mirror is "
          "broken there" if flipped else
          "  the mirror holds: every Part I Greek page is on a verso")
    for n in flipped:
        print(f"    printed {n} on leaf {start[n]}")
    return over


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="all", choices=["1", "2", "3", "all"])
    ap.add_argument("--fit", nargs="?", const=True, default=False,
                    help="report the last build's page fitting instead of building")
    args = ap.parse_args()

    parts = [1, 2, 3] if args.part == "all" else [int(args.part)]
    name = "volume-mirror" if args.part == "all" else f"part{args.part}-mirror"
    if args.fit:
        report_fit(name if args.fit is True else f"part{args.fit}-mirror")
        return

    pages = volume_pages(parts)
    have = emit_fragments(pages)
    scope = "The whole volume" if len(parts) > 1 else PART_TITLES[parts[0]]
    doc = (TEMPLATE
           .replace("%%SCOPE%%", scope.replace("---", "\\textemdash{}"))
           .replace("%%BODY%%", build_driver(parts, pages, have)))
    (OUT_DIR / f"{name}.tex").write_text(doc)
    print(f"wrote {name}.tex and {len(have)} fragments "
          f"({len(pages)} printed pages, "
          f"{sum(1 for s in pages.values() if s['en'])} with English)")


TEMPLATE = r"""% The 1675 mirror — Greek verso, Latin recto, English register at the foot.
% Auto-generated by tools/transcript2tex.py. The edition carries its OWN folios;
% the 1853 page runs as a shoulder-note in the inner head of every leaf.
\documentclass[10pt,twoside]{book}
\input{preamble}
\usepackage{fancyhdr}
\setlength{\headheight}{14pt}

% Running heads: Part I keeps the 1853's own, Parts II--III take the section's.
\newcommand{\headL}{ΕΥΧΑΙ ΚΑΘΗΜΕΡΙΝΑΙ.}
\newcommand{\headR}{PRECES QUOTIDIANÆ.}
\newcommand{\sethead}[1]{\renewcommand{\headL}{#1}\renewcommand{\headR}{#1}}
\pagestyle{fancy}\fancyhf{}
\fancyhead[CE]{\small\headL}
\fancyhead[CO]{\small\headR}
% Outer: the edition's own folio. Inner: the 1853 page as a shoulder-note, so the
% original pagination stays recoverable on every leaf without the edition having
% to promise one leaf per 1853 page. \rightmark carries the FIRST mark on the
% leaf, so a page that runs to two leaves keeps its own number on both.
\fancyhead[LE,RO]{\small\thepage}
\fancyhead[RE,LO]{\footnotesize\color{rulegray}[\,\rightmark\,]}
\renewcommand{\headrulewidth}{0pt}

% Force the next leaf to be a verso, and record the blank if one was spent.
% After \clearpage the counter holds the number of the leaf about to be set: even
% is a verso. So an ODD count means a blank must be spent to reach the left-hand
% page.
\newcommand{\versoalign}{\clearpage
  \ifodd\value{page}
    \null\thispagestyle{empty}\write\fitfile{B \thepage}\clearpage
  \fi}

% English register across the foot of the leaf
\newcommand{\registerrule}{\par\vfill
  {\centering\color{rulegray}\rule{0.9\textwidth}{0.4pt}\par}\vspace{0.3\baselineskip}}

% part divider
\newcommand{\parthead}[1]{\clearpage\thispagestyle{empty}\vspace*{2.2in}%
  {\centering\Huge\scshape #1\par}\clearpage}

% Fit instrumentation. \write is deferred to shipout, so \thepage records the
% leaf the mark actually landed on: if a page's start and end differ, its text
% ran to a second leaf. In Parts II--III that is now merely bulk; in Part I it
% spoils a spread, and \versoalign recovers the alignment at the next Greek page.
\newwrite\fitfile
\immediate\openout\fitfile=\jobname.fit
\newcommand{\fitstart}[1]{\write\fitfile{S #1 \thepage}}
\newcommand{\fitend}[1]{\write\fitfile{E #1 \thepage}}

\begin{document}
\thispagestyle{empty}
\vspace*{2in}
{\centering
{\Huge Preces Privatae}\\[0.6em]
{\large Lancelot Andrewes}\\[2em]
{\itshape %%SCOPE%% --- the 1675 mirror}\\[0.5em]
{\small Greek verso, Latin recto, line for line as the 1853 edition;}\\
{\small the English translation runs as a register across the foot.}\\[0.5em]
{\small The edition's own folios, with the 1853 page in the inner margin.}\par}
\clearpage
\setcounter{page}{1}

%%BODY%%

\clearpage
\immediate\closeout\fitfile
\end{document}
"""


if __name__ == "__main__":
    main()
