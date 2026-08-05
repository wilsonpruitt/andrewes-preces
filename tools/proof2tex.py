#!/usr/bin/env python3
"""Build a continuous PROOFING PDF of the Preces Privatae — any part, or all of it.

NOT the final 1675 mirror (that is the deferred M-print job, tools/transcript2tex.py).
This flows every printed page in printed order — for each page: the Greek or Latin
as printed, and the English translation beneath it — full width, so the ` | ` columns,
the `{ }` brace catalogues and Part III's left-margin reference column render legibly
as literal characters in their printed horizontal positions. Overflow is harmless
here: continuous flow, no verso/recto mirror to desync.

    python3.11 tools/proof2tex.py            # whole volume -> volume-proof.tex
    python3.11 tools/proof2tex.py --part 1   # Part I only  -> part1-proof.tex
    python3.11 tools/proof2tex.py --part 3   # Part III     -> part3-proof.tex

Build with:  cd prototypes && xelatex <name>.tex
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "prototypes"

# Part I is not alphabetical — its reading order is explicit.
PART1_SECTIONS = [
    "front", "day1", "day2", "day3", "day4", "day5", "day6", "day7",
    "deprecation", "evening", "meditations",
]
PART1_LABELS = {
    "front": "Front Matter", "day1": "The First Day", "day2": "The Second Day",
    "day3": "The Third Day", "day4": "The Fourth Day", "day5": "The Fifth Day",
    "day6": "The Sixth Day", "day7": "The Seventh Day",
    "deprecation": "Deprecation and Hosannas", "evening": "The Evening Office",
    "meditations": "The Meditations",
}

PART_TITLES = {
    1: "Part I",
    2: "Part II --- Preces Quotidianae",
    3: "Part III --- Confessio Fidei and after",
}

# One em of leading/internal space per 0.3em keeps Part I's 4-space unit at the
# 1.2em it has always rendered at, and lets Part III's ragged reference column
# keep its printed horizontal position instead of being rounded onto a ladder.
SPACE_EM = 0.3

HEBREW = re.compile(r"[\u0590-\u05ff][\u0590-\u05ff\s]*[\u0590-\u05ff]|[\u0590-\u05ff]")
COMMENT = re.compile(r"<!--.*?-->")
MARKER = re.compile(r"<!--\s*printed\s+(\d+)")
GREEK_CH = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")
LATIN_CH = re.compile(r"[A-Za-z]")
GAP = re.compile(r"(?<=\S)( {2,})(?=\S)")
# Every file ends with an apparatus section ("## Translator's flags", "## Transcription
# notes", ...). It is editorial prose, NOT page text, and must never be flowed into the
# last printed page of the section.
APPARATUS = re.compile(r"^##\s")


def tex_escape(s: str) -> str:
    s = s.replace("\\", r"\textbackslash{}")
    for c, r in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\~{}"),
                 ("^", r"\^{}")]:
        s = s.replace(c, r)
    return s


def tex_inline(s: str) -> str:
    """Escape a scrap of source prose and honour its markdown emphasis. Section
    headings are written like the rest of the files (`§6 *Sacrificium Vespertinum*`),
    so escaping alone sets the asterisks as literal characters — which is what all
    49 Part II--III headings did."""
    t = tex_escape(s)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", t)
    t = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", t)
    return t


def render_line(raw: str):
    """Return a rendered \\pl line, or None if the line is empty/comment-only."""
    line = COMMENT.sub("", raw).rstrip()
    if not line.strip():
        return None
    indent = len(line) - len(line.lstrip(" "))
    body = line.strip()
    # Preserve internal runs of 2+ spaces (the reference column, the ` | ` tables,
    # the brace gutters) as measured horizontal space, not collapsed word-space.
    gaps = []

    def stash(m):
        gaps.append(len(m.group(1)))
        return "\x00%d\x00" % (len(gaps) - 1)

    body = GAP.sub(stash, body)
    text = tex_escape(body)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", text)
    text = HEBREW.sub(lambda m: r"\RL{%s}" % m.group(0), text)
    text = re.sub(r"\x00(\d+)\x00",
                  lambda m: r"\hspace{%.2fem}" % (gaps[int(m.group(1))] * SPACE_EM),
                  text)
    return r"\pl{%.2f}{%s}" % (indent * SPACE_EM, text)


def render_block(lines):
    out, prev_blank = [], True
    for l in lines:
        r = render_line(l)
        if r is None:
            if not prev_blank:
                out.append(r"\parasep")
                prev_blank = True
        else:
            out.append(r)
            prev_blank = False
    while out and out[-1] == r"\parasep":
        out.pop()
    return "\n".join(out)


def layer_of(lines, marker: str) -> str:
    """Which layer a printed page belongs to.

    Decided from the page's own SCRIPT, not from the marker's prose. The marker
    is unreliable in both directions: most of Part II carries no layer word at
    all, and the words that do appear are often descriptive ("Greek, with Latin
    connectives", "one Latin line, then Greek"), so any substring test reads
    them backwards. Counting characters agrees with Part I's verso/recto rule on
    all 263 of its pages, and Greek versos stay Greek despite their Latin
    scripture tags because the tags are a few words against a page of Greek.
    The marker only breaks a tie (an empty block, or a bare title page).
    """
    text = "\n".join(lines)
    gr, la = len(GREEK_CH.findall(text)), len(LATIN_CH.findall(text))
    if gr != la:
        return "gr" if gr > la else "la"
    low = marker.lower()
    return "en" if "english" in low else "la" if "latin" in low else "gr"


def parse_pages(path: Path):
    """printed page number -> (layer, lines). layer in {gr, la, en}."""
    blocks, markers, cur = {}, {}, None
    for raw in path.read_text().splitlines():
        if APPARATUS.match(raw):
            break
        m = MARKER.match(raw.strip())
        if m:
            cur = int(m.group(1))
            # A page can be marked twice in one file (a section opening or closing
            # mid-page). Continue the block; never start it over — overwriting drops
            # the page's real text.
            if cur in blocks:
                blocks[cur].append("")
            else:
                blocks[cur] = []
                markers[cur] = raw
            continue
        if cur is not None:
            blocks[cur].append(raw)
    return {n: (layer_of(ls, markers[n]), ls) for n, ls in blocks.items()}


def section_label(part: int, stem: str, transcript: Path) -> str:
    """Part I labels are named; Parts II-III take the section's own H1."""
    if part == 1:
        return PART1_LABELS.get(stem, stem)
    head = transcript.read_text().splitlines()[0].lstrip("# ").strip()
    head = re.sub(r"\s*—\s*raw transcript\s*$", "", head)
    head = re.sub(r"^Part\s+[IVX]+\s*—\s*[^—]*—\s*", "", head)
    return head.strip()


def sections_for(part: int):
    """[(transcript Path, english Path, label)] in reading order."""
    d = ROOT / f"part{part}"
    if part == 1:
        stems = PART1_SECTIONS
    else:
        stems = sorted(
            {p.name[: -len("-transcript.md")] for p in d.glob("*-transcript.md")},
            key=lambda s: (int(s.split("-", 1)[0]), s),
        )
    out = []
    for stem in stems:
        tr = d / f"{stem}-transcript.md"
        en = d / f"{stem}-english.md"
        if not tr.exists():
            raise SystemExit(f"missing transcript: {tr}")
        out.append((tr, en if en.exists() else None,
                    section_label(part, stem, tr)))
    return out


def build_part(part: int, body: list, stats: dict):
    body.append(r"\parthead{%s}" % PART_TITLES[part])
    for tr, en, label in sections_for(part):
        tr_blocks = parse_pages(tr)
        en_blocks = parse_pages(en) if en else {}
        pages = {}
        for n, (lay, ls) in tr_blocks.items():
            pages.setdefault(n, {})[lay] = ls
        for n, (_, ls) in en_blocks.items():
            pages.setdefault(n, {})["en"] = ls
        if not pages:
            continue
        body.append(r"\sectionhead{%s}" % tex_inline(label))
        for n in sorted(pages):
            slot = pages[n]
            for lay, name in [("gr", "Greek"), ("la", "Latin")]:
                if lay in slot:
                    rendered = render_block(slot[lay])
                    if rendered:
                        body.append(r"\pglabel{printed %d}{%s}" % (n, name))
                        body.append(rendered)
                        stats["pages"] += 1
            if "en" in slot:
                rendered = render_block(slot["en"])
                if rendered:
                    body.append(r"\pglabel{printed %d}{English}" % n)
                    body.append(r"{\itshape" + "\n" + rendered + "\n}")
                    stats["english"] += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="all", choices=["1", "2", "3", "all"])
    args = ap.parse_args()

    parts = [1, 2, 3] if args.part == "all" else [int(args.part)]
    name = "volume-proof" if args.part == "all" else f"part{args.part}-proof"
    out = OUT_DIR / f"{name}.tex"

    body, stats = [], {"pages": 0, "english": 0}
    for p in parts:
        build_part(p, body, stats)

    if len(parts) == 1:
        scope = PART_TITLES[parts[0]]
        blurb = r"Greek and Latin as printed in the 1853 Parker edition,\\ with the Wroot Press English beneath."
    else:
        scope = "The whole volume"
        blurb = (r"Greek, Latin and Hebrew as printed in the 1853 Parker edition,\\ "
                 r"with the Wroot Press English beneath each page.")

    doc = (TEMPLATE
           .replace("%%SCOPE%%", scope)
           .replace("%%BLURB%%", blurb)
           .replace("%%RUNHEAD%%", scope.replace("---", "\\textemdash{}"))
           .replace("%%BODY%%", "\n\n".join(body)))
    out.write_text(doc)
    print(f"wrote {out.name}  ({stats['pages']} printed pages, "
          f"{stats['english']} with English)")


TEMPLATE = r"""% Proofing copy — continuous flow, printed order.
% Auto-generated by tools/proof2tex.py. NOT the final 1675 mirror.
\documentclass[11pt]{book}
\input{preamble}
\usepackage{fancyhdr}
\setlength{\headheight}{14pt}
\pagestyle{fancy}\fancyhf{}
\fancyhead[C]{\small\itshape Preces Privatae --- proof}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0pt}
% Long inline brace catalogues ({ a / b / c }) have few breakpoints; in a proof a
% loose line is better than one running past the trim.
\sloppy

% printed-page / layer label
\newcommand{\pglabel}[2]{\par\vspace{0.7\baselineskip}%
  {\centering\color{rulegray}\footnotesize\scshape #1 \textperiodcentered\ #2\par}%
  \vspace{0.15\baselineskip}%
  {\centering\color{rulegray}\rule{0.22\textwidth}{0.3pt}\par}%
  \vspace{0.25\baselineskip}}

% section divider
\newcommand{\sectionhead}[1]{\clearpage\vspace*{0.5in}%
  {\centering\Large\scshape #1\par}%
  {\centering\color{rulegray}\rule{0.4\textwidth}{0.4pt}\par}%
  \vspace{0.6\baselineskip}}

% part divider
\newcommand{\parthead}[1]{\clearpage\thispagestyle{empty}\vspace*{2.2in}%
  {\centering\Huge\scshape #1\par}\clearpage}

\begin{document}
\thispagestyle{empty}
\vspace*{2in}
{\centering
{\Huge Preces Privatae}\\[0.6em]
{\large Lancelot Andrewes}\\[2em]
{\itshape %%SCOPE%% --- proofing copy}\\[0.5em]
{\small %%BLURB%%}\\[0.5em]
{\small Continuous flow, not the final mirror.}\par}
\clearpage
\setcounter{page}{1}

%%BODY%%

\end{document}
"""


if __name__ == "__main__":
    main()
