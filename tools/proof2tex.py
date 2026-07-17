#!/usr/bin/env python3
"""Build a continuous PROOFING PDF of all of Part I (printed 1-263).

NOT the final 1675 mirror (that is the deferred M-print job). This flows every
Part I page in printed order — for each printed page: the Greek or Latin as
printed, and (on Greek pages) the English translation beneath it — full width,
so the ` | ` columns and `{ }` brace catalogues render legibly as literal
characters. Overflow is harmless here: continuous flow, no verso/recto mirror
to desync.

Emits prototypes/part1-proof.tex ; build with:
    cd prototypes && xelatex part1-proof.tex
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PART1 = ROOT / "part1"
OUT = ROOT / "prototypes" / "part1-proof.tex"

# (transcript, english, section label) in reading order
SECTIONS = [
    ("front-transcript.md", "front-english.md", "Front Matter"),
    ("day1-transcript.md", "day1-english.md", "The First Day"),
    ("day2-transcript.md", "day2-english.md", "The Second Day"),
    ("day3-transcript.md", "day3-english.md", "The Third Day"),
    ("day4-transcript.md", "day4-english.md", "The Fourth Day"),
    ("day5-transcript.md", "day5-english.md", "The Fifth Day"),
    ("day6-transcript.md", "day6-english.md", "The Sixth Day"),
    ("day7-transcript.md", "day7-english.md", "The Seventh Day"),
    ("deprecation-transcript.md", "deprecation-english.md", "Deprecation and Hosannas"),
    ("evening-transcript.md", "evening-english.md", "The Evening Office"),
    ("meditations-transcript.md", "meditations-english.md", "The Meditations"),
]

HEBREW = re.compile(r"[֐-׿][֐-׿\s]*[֐-׿]|[֐-׿]")
COMMENT = re.compile(r"<!--.*?-->")
MARKER = re.compile(r"<!--\s*printed\s+(\d+)")


def tex_escape(s: str) -> str:
    s = s.replace("\\", r"\textbackslash{}")
    for c, r in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\~{}"),
                 ("^", r"\^{}")]:
        s = s.replace(c, r)
    return s


def render_line(raw: str):
    """Return a rendered \\pl line, or None if the line is empty/comment-only."""
    line = COMMENT.sub("", raw).rstrip()
    if not line.strip():
        return None
    indent = (len(line) - len(line.lstrip(" "))) // 4
    text = tex_escape(line.strip())
    text = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", text)
    text = HEBREW.sub(lambda m: r"\RL{%s}" % m.group(0), text)
    return r"\pl{%.2f}{%s}" % (indent * 1.2, text)


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


def parse_pages(path: Path):
    """page number -> (layer, lines). layer in {gr, la, en}."""
    blocks, cur, layer = {}, None, None
    for raw in path.read_text().splitlines():
        m = MARKER.match(raw.strip())
        if m:
            cur = int(m.group(1))
            low = raw.lower()
            layer = "en" if "english" in low else "la" if "latin" in low else "gr"
            blocks[cur] = (layer, [])
            continue
        if cur is not None:
            blocks[cur][1].append(raw)
    return blocks


def main():
    pages = {}            # N -> {"gr":lines, "la":lines, "en":lines}
    section_start = {}    # N -> label (first printed page of each section)
    for tr, en, label in SECTIONS:
        tr_blocks = parse_pages(PART1 / tr)
        en_blocks = parse_pages(PART1 / en)
        all_ns = sorted(set(tr_blocks) | set(en_blocks))
        if all_ns:
            section_start[all_ns[0]] = label
        for n in all_ns:
            slot = pages.setdefault(n, {})
            if n in tr_blocks:
                lay, ls = tr_blocks[n]
                slot[lay] = ls
            if n in en_blocks:
                slot["en"] = en_blocks[n][1]

    body = []
    for n in sorted(pages):
        if n in section_start:
            body.append(r"\sectionhead{%s}" % section_start[n])
        slot = pages[n]
        for lay, name in [("gr", "Greek"), ("la", "Latin")]:
            if lay in slot:
                rendered = render_block(slot[lay])
                if rendered:
                    body.append(r"\pglabel{printed %d}{%s}" % (n, name))
                    body.append(rendered)
        if "en" in slot:
            rendered = render_block(slot["en"])
            if rendered:
                body.append(r"\pglabel{printed %d}{English}" % n)
                body.append(r"{\itshape" + "\n" + rendered + "\n}")

    doc = TEMPLATE.replace("%%BODY%%", "\n\n".join(body))
    OUT.write_text(doc)
    print(f"wrote {OUT.name}  ({len(pages)} printed pages, "
          f"{sum('en' in p for p in pages.values())} with English)")


TEMPLATE = r"""% Part I proofing copy — continuous flow, printed order 1-263.
% Auto-generated by tools/proof2tex.py. NOT the final 1675 mirror.
\documentclass[11pt]{book}
\input{preamble}
\usepackage{fancyhdr}
\setlength{\headheight}{14pt}
\pagestyle{fancy}\fancyhf{}
\fancyhead[C]{\small\itshape Preces Privatae --- Part I (proof)}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0pt}

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

\begin{document}
\thispagestyle{empty}
\vspace*{2in}
{\centering
{\Huge Preces Privatae}\\[0.6em]
{\large Lancelot Andrewes}\\[2em]
{\itshape Part I --- proofing copy}\\[0.5em]
{\small Greek and Latin as printed in the 1853 Parker edition,}\\
{\small with the Wroot Press English beneath each Greek page.}\\[0.5em]
{\small Printed pp.\ 1--263 \textperiodcentered\ continuous flow, not the final mirror.}\par}
\clearpage
\setcounter{page}{1}

%%BODY%%

\end{document}
"""


if __name__ == "__main__":
    main()
