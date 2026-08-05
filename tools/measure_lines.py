#!/usr/bin/env python3
"""How many sense-lines TURN in a given measure? — the layout question numerically.

    python3.11 tools/measure_lines.py

The volume's discipline is the sense-line: one line of the 1853, one line of ours,
one line of the English. A line too long for its measure does not break that
discipline — the 1853 turns lines itself, and CONVENTIONS keeps its printer's
turned-line hyphens — but a layout that turns one line in eight is a different
book from one that turns one in three hundred. That is the whole difference
between the mirror and the Loeb, and it is measurable rather than arguable.

The trick: \\pl is the macro every fragment is built from, so redefining it to
MEASURE its argument instead of setting it turns the whole corpus into data. It
boxes each line, compares the box's natural width against the measure minus that
line's indent, and counts. Nothing is typeset.
"""
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from proof2tex import OUT_DIR  # noqa: E402
from transcript2tex import FRAG, volume_pages  # noqa: E402

# (label, measure, size) per layout. The Loeb pairs Part I's originals into two
# columns on one leaf and gives Parts II-III the full measure; the mirror gives
# every page the full measure at \small.
LAYOUTS = {
    "mirror": lambda part: (r"\textwidth", r"\small", "5em"),
    "loeb": lambda part: ((r"0.485\textwidth", r"\footnotesize", "1.5em")
                          if part == 1 else
                          (r"\textwidth", r"\footnotesize", "1.5em")),
}

DOC = r"""\documentclass[10pt,twoside]{book}
\input{preamble}
\newwrite\m \immediate\openout\m=lines.dat
\newcount\nl \newcount\nw
% Measure a sense-line instead of setting it: does its natural width exceed the
% width available to it here (the measure, less its own indent)?
\newcommand{\measure}[5]{\begingroup
  \nl=0 \nw=0
  \renewcommand{\parasep}{}%
  \renewcommand{\pl}[2]{\setbox0=\hbox{##2}\global\advance\nl by1
    \dimen0=\hsize \advance\dimen0 by -##1em
    \ifdim\wd0>\dimen0 \global\advance\nw by1 \fi}%
  \setbox9=\vbox{#4 #5}%
  \immediate\write\m{#1 #2 #3 \the\nl\space \the\nw}%
\endgroup}
\begin{document}
%%BODY%%
\immediate\closeout\m
\end{document}
"""

ROW = re.compile(r"^(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$")


def main():
    pages = volume_pages([1, 2, 3])
    body = []
    for n, slot in sorted(pages.items()):
        if not slot["body"] or slot["layer"] is None:
            continue
        frag = f"{slot['layer']}{n:03d}"
        if not (FRAG / f"{frag}.tex").exists():
            continue
        for name, spec in LAYOUTS.items():
            measure, size, hang = spec(slot["part"])
            setup = r"\hsize=%s%s\setlength{\plhang}{%s}" % (measure, size, hang)
            body.append(r"\measure{%s}{%d}{%d}{%s}{\input{fragments/%s}}"
                        % (name, slot["part"], n, setup, frag))

    tex = OUT_DIR / "measure-lines.tex"
    tex.write_text(DOC.replace("%%BODY%%", "\n".join(body)))
    subprocess.run(["xelatex", "-interaction=nonstopmode", tex.name],
                   cwd=OUT_DIR, stdout=subprocess.DEVNULL, check=True)

    tally = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for line in (OUT_DIR / "lines.dat").read_text().splitlines():
        m = ROW.match(line.strip())
        if m:
            cell = tally[m.group(1)][int(m.group(2))]
            cell[0] += int(m.group(4))
            cell[1] += int(m.group(5))

    print(f"{'layout':<8}{'part':<6}{'lines':>8}{'turned':>9}{'':>8}")
    for name in LAYOUTS:
        tot = [0, 0]
        for part in (1, 2, 3):
            nl, nw = tally[name][part]
            tot[0] += nl
            tot[1] += nw
            print(f"{name:<8}{part:<6}{nl:>8}{nw:>9}{100 * nw / nl:>7.1f}%")
        print(f"{name:<8}{'ALL':<6}{tot[0]:>8}{tot[1]:>9}"
              f"{100 * tot[1] / tot[0]:>7.1f}%")


if __name__ == "__main__":
    main()
