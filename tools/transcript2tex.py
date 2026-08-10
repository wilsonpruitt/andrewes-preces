#!/usr/bin/env python3
"""Build the EDITION LAYOUT — originals verso, English recto (prototype C, "Loeb").

Ruled by Wilson 2026-08-05 over the 1675 mirror, on measurement: see
EDITION-SHAPE.md 6b. This emits one TeX fragment per printed page into
prototypes/fragments/, then a driver that lays them out:

    python3.11 tools/transcript2tex.py                # whole volume -> volume-loeb.tex
    python3.11 tools/transcript2tex.py --part 1       # Part I only  -> part1-loeb.tex
    python3.11 tools/transcript2tex.py --fit          # read back the last build
    python3.11 tools/transcript2tex.py --layout mirror  # prototype B, for comparison

Build with:  cd prototypes && xelatex <name>.tex

THE UNIT IS THE 1853 OPENING, not the 1853 page. In Part I the Greek verso and its
Latin recto share one leaf in two columns and the English takes the whole facing
page; in Parts II--III, which are one language to a page, the verso takes the full
measure and the English still faces it. One structure serves all three parts,
where the mirror needed two.

Why this layout cannot desynchronise: nothing depends on a page facing its own
translation. Originals are always verso and English always recto, so a unit that
runs long takes two spreads and the alternation is untouched. Across the whole
volume nothing is too tall for its leaf. ⚠ The instrument that proves it is NOT
the mirror's page marks — a minipage overruns in silence instead of breaking, so
marks would report no overflow however bad it got. Each unit is boxed, its height
written out, and compared against \textheight by `--fit`.

The edition carries ITS OWN continuous folios, with the 1853 page as a
shoulder-note in the inner head of every leaf (EDITION-SHAPE.md 6a; that ruling is
layout-agnostic and survived the change of layout).

What the layout costs, and it is worth knowing before touching the measure: 839 of
Part I's 6,759 sense-lines turn in the two columns, against 23 at full width. The
1853 turns lines itself and CONVENTIONS keeps its turned-line hyphens, so a turned
line is not a broken parallel — but `tools/measure_lines.py` re-runs the whole
comparison before anyone changes a column width on a hunch. The Latin column turns
MORE than the Greek; widening the Greek makes the total worse.

The mirror (`--layout mirror`) is kept because it is the thing this was measured
against, and because Part I's mirror is still the truest picture of the 1853's own
page. It needs \versoalign to hold its register; see EDITION-SHAPE.md 6a.

Parsing and rendering are imported from proof2tex so the two builders cannot
drift: both the apparatus cut-off (a trailing `## Translator's flags` must never
flow into the last printed page) and the twice-marked-page fix (continue the
block, never restart it) live in one place now.
"""
import argparse
import re
from pathlib import Path

from proof2tex import (
    HEBREW, OUT_DIR, PART_TITLES, ROOT, parse_pages, render_block, render_line,
    sections_for, tex_escape, tex_inline,
)

FRAG = OUT_DIR / "fragments"
NOTES_SRC = ROOT / "apparatus" / "print-notes.md"


def load_notes():
    """The two foot-bands, keyed by printed page: `V:` apparatus (verso foot),
    `R:` explanatory note (recto foot). Source is apparatus/print-notes.md.

    ⚠ These bands exist because the Loeb leaves roughly 44%% of every leaf empty
    and a Loeb's foot is where an apparatus belongs — but they are NOT filler.
    Nothing here may be phrased as a repair: the plate stands as printed above,
    an apparatus entry records another witness, a note tells the reader what the
    flags already know. See the head of print-notes.md.
    """
    notes = {}
    if not NOTES_SRC.exists():
        return notes
    page = None
    for raw in NOTES_SRC.read_text().splitlines():
        line = raw.strip()
        m = re.match(r"^## (\d+)$", line)
        if m:
            page = int(m.group(1))
            continue
        m = re.match(r"^([VRS]): (.+)$", line)
        if m and page is not None:
            notes.setdefault(page, {"V": [], "R": [], "S": []})[
                m.group(1)].append(m.group(2))
    return notes


def note_tex(entries):
    r"""One band's worth of entries. Backticks mark a lemma and are set upright —
    `tex_inline` handles *em* and **bold** but knows nothing of them."""
    out = []
    for e in entries:
        t = tex_inline(e)
        t = re.sub(r"`([^`]+)`", r"\\textup{\1}", t)
        # Hebrew is right-to-left and needs bidi's \RL, exactly as in the page
        # fragments — an apparatus entry is the likeliest place in the book to
        # carry a bare Hebrew word, since class A is where the dropped Hebrew is.
        t = HEBREW.sub(lambda m: r"\RL{%s}" % m.group(0), t)
        out.append(t)
    return r"\\[1pt]".join(out)


def recto_band(page_notes):
    r"""The recto foot: scripture context first, then explanatory notes.

    ⚠ The two are set DIFFERENTLY on purpose. `S:` entries run in, separated by
    ·, because there can be fourteen of them on one page and a stack of fourteen
    stanzas would swamp the English above; `R:` entries are paragraphs, because
    there is rarely more than one and it has something to say.

    ⚠ Scripture context lives on the RECTO though the 1853 prints its references
    on the LATIN side. The reference belongs to the original; the *situation* it
    came from belongs to the reader, and the reader is on the recto.
    """
    s = page_notes.get("S", [])
    r = page_notes.get("R", [])
    blocks = []
    if s:
        blocks.append(r"{\scriptsize " + r" \textperiodcentered\ ".join(
            note_tex([e]) for e in s) + r"\par}")
    if r:
        blocks.append(note_tex(r))
    return r"\\[3pt]".join(blocks)

# The M2 sample split three pages at a unit boundary so prototype B could show a
# mid-page break. proto-{a,b,c}.tex still \input those a/b fragments by name, so
# they are still emitted; the volume driver does not use them.
SPLITS = {
    ("gr", 32): "ΟΙΚΤΙΡΜΟΝ", ("la", 33): "MISERICORS", ("en", 32): "MERCIFUL",
    ("gr", 40): "ΑΙΡΩ", ("la", 41): "Attollo", ("en", 40): "I LIFT UP",
    ("gr", 42): "סיג", ("la", 43): "SEPES", ("en", 42): "סיג",
}

# Leaves the 1853 sets as DISPLAY, not as running text. Both are named in the
# transcripts' own page markers ("bilingual half-title", "the epigraph page facing
# the section-opener"); grep the markers before adding to this list, rather than
# guessing from a page's length.
DISPLAY = {1: "title", 398: "epigraph"}

FIT = re.compile(r"^([SEB])\s+(\d+)(?:\s+(\d+))?\s*$")
HGT = re.compile(r"^H\s+([OE])\s+(\d+)\s+([\d.]+)pt\s*$")
TEXTHEIGHT = re.compile(r"^T\s+([\d.]+)pt\s*$")


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


def loeb_unit(n: int, gr: str | None, la: str | None, en: str | None,
              single=False, toc: str | None = None, vnotes="", rnotes=""):
    """One Loeb unit: originals on the verso, the full English on the recto.

    The unit is the 1853 OPENING in Part I — Greek and Latin side by side on one
    leaf, which is why the layout costs no more extent than the mirror despite
    giving English a whole page. In Parts II--III there is one language, so the
    verso is a single full-width column and the same structure serves all three
    parts, where the mirror needed two.

    Originals are boxed before they are set, and the box's height is written out,
    because a minipage does not break across leaves — it silently overruns, and
    \\fitstart/\\fitend would both land on the same page and report no overflow.
    Measuring the box is the only honest instrument here.
    """
    out = [r"\versoalign", r"\markright{%d}" % n]
    if toc:
        # After the page break, so the entry records the leaf the section opens on.
        out.append(r"\addcontentsline{toc}{section}{%s}" % toc)
    mode = DISPLAY.get(n)
    if mode == "title":
        out.append(r"\titleleaf{%d}{\input{fragments/%s}%s}" % (
            n, gr, r"\parasep\input{fragments/%s}" % la if la else ""))
    elif single:
        # A display leaf is composed, not flowed, so it never takes a band.
        if vnotes and not mode:
            out.append(r"\originalsonen{%d}{\input{fragments/%s}}{}{%s}"
                       % (n, gr or la, vnotes))
        else:
            out.append(r"\originalsone{%d}{\input{fragments/%s}}{%s}"
                       % (n, gr or la, mode or ""))
    else:
        gr_in = r"\input{fragments/%s}" % gr if gr else ""
        la_in = r"\input{fragments/%s}" % la if la else ""
        if vnotes:
            out.append(r"\originalsn{%d}{%s}{%s}{%s}" % (n, gr_in, la_in, vnotes))
        else:
            out.append(r"\originals{%d}{%s}{%s}" % (n, gr_in, la_in))
    out.append(r"\clearpage")
    if en:
        out.append(r"\markright{%d}" % n)
        if mode == "title":
            out.append(r"\titleleaf{%d}{\input{fragments/%s}}" % (n, en))
        elif rnotes and not mode:
            out.append(r"\enleafn{%d}{\input{fragments/%s}}{}{%s}"
                       % (n, en, rnotes))
        else:
            out.append(r"\enleaf{%d}{\input{fragments/%s}}{%s}"
                       % (n, en, mode or ""))
        out.append(r"\clearpage")
    return out


def build_loeb(parts, pages, have):
    body, part_seen, label_seen = [], None, None
    notes = load_notes()
    skip = set()
    for n in sorted(pages):
        if n in skip:
            continue
        slot = pages[n]
        if slot["part"] != part_seen:
            part_seen = slot["part"]
            label_seen = None
            body.append(r"\parthead{%s}" % PART_TITLES[part_seen])
        toc = None
        if slot["label"] != label_seen:
            label_seen = slot["label"]
            body.append(r"\sethead{%s}" % tex_inline(short_label(label_seen)))
            # The head has one line; the contents page has a whole measure, so it
            # gets the section's real title rather than the truncated one.
            toc = tex_inline(label_seen)

        def frag(name):
            return name if name in have else None

        recto = pages.get(n + 1)
        paired = (
            slot["part"] == 1 and slot["layer"] == "gr" and n % 2 == 0
            and recto and recto["layer"] == "la" and recto["part"] == 1
        )
        if paired:
            # The verso holds BOTH printed pages of the opening, so it carries
            # the apparatus of both. The recto holds one English page and its
            # notes are the notes of the Greek page it translates.
            v = (notes.get(n, {}).get("V", [])
                 + notes.get(n + 1, {}).get("V", []))
            body += [r"%% ---------- opening %d | %d ----------" % (n, n + 1)]
            body += loeb_unit(n, frag(f"gr{n:03d}"), frag(f"la{n + 1:03d}"),
                              frag(f"en{n:03d}"), toc=toc,
                              vnotes=note_tex(v),
                              rnotes=recto_band(notes.get(n, {})))
            skip.add(n + 1)
        else:
            body += [r"%% ---------- printed %d ----------" % n]
            body += loeb_unit(n, frag(f"{slot['layer']}{n:03d}"), None,
                              frag(f"en{n:03d}"), single=True, toc=toc,
                              vnotes=note_tex(notes.get(n, {}).get("V", [])),
                              rnotes=recto_band(notes.get(n, {})))
    return "\n".join(body)


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


def report_loeb(name: str):
    """A minipage overruns silently, so the Loeb is judged on measured heights:
    how many units are too tall for a leaf, and by how much."""
    path = OUT_DIR / f"{name}.fit"
    if not path.exists():
        raise SystemExit(f"no fit record at {path} — build {name}.tex first")
    avail, heights, blanks = None, {"O": {}, "E": {}}, 0
    for line in path.read_text().splitlines():
        line = line.strip()
        m = TEXTHEIGHT.match(line)
        if m:
            avail = float(m.group(1))
            continue
        m = HGT.match(line)
        if m:
            heights[m.group(1)][int(m.group(2))] = float(m.group(3))
            continue
        if line.startswith("B "):
            blanks += 1
    if avail is None:
        raise SystemExit("no \\textheight recorded — rebuild")

    print(f"leaf holds {avail:.0f}pt")
    for key, what in [("O", "originals (verso)"), ("E", "English (recto)")]:
        hs = heights[key]
        over = sorted((n for n, h in hs.items() if h > avail),
                      key=lambda n: -hs[n])
        worst = f", worst printed {over[0]} at {hs[over[0]]:.0f}pt" if over else ""
        print(f"  {len(hs):>3} {what}: {len(over)} too tall for their leaf{worst}")
        if over:
            print("      " + ", ".join(str(n) for n in sorted(over)[:24])
                  + (" …" if len(over) > 24 else ""))
    print(f"  {blanks} blank leaves spent keeping originals on the verso")
    return heights


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", default="all", choices=["1", "2", "3", "all"])
    ap.add_argument("--layout", default="loeb", choices=["loeb", "mirror"],
                    help="loeb = the edition layout, ruled 2026-08-05 (default); "
                         "mirror = prototype B, kept for comparison")
    ap.add_argument("--fit", nargs="?", const=True, default=False,
                    help="report the last build's page fitting instead of building")
    args = ap.parse_args()

    parts = [1, 2, 3] if args.part == "all" else [int(args.part)]
    stem = "volume" if args.part == "all" else f"part{args.part}"
    name = f"{stem}-{args.layout}"
    if args.fit:
        if args.fit is not True:
            name = f"part{args.fit}-{args.layout}"
        (report_loeb if args.layout == "loeb" else report_fit)(name)
        return

    pages = volume_pages(parts)
    have = emit_fragments(pages)
    scope = "The whole volume" if len(parts) > 1 else PART_TITLES[parts[0]]
    template = LOEB_TEMPLATE if args.layout == "loeb" else TEMPLATE
    driver = build_loeb if args.layout == "loeb" else build_driver
    scope_line = ("" if len(parts) > 1 else
                  r"\\[3em]{\small\scshape %s}"
                  % scope.replace("---", "\\textemdash{}"))
    doc = (template
           .replace("%%SCOPE%%", scope.replace("---", "\\textemdash{}"))
           .replace("%%SCOPELINE%%", scope_line)
           .replace("%%BODY%%", driver(parts, pages, have)))
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

\backmatter
% Plain style: the fancy heads carry the 1853 shoulder-note in \rightmark, which
% the back matter has no use for and would otherwise fight with its own \markboth.
\pagestyle{plain}
\input{back/sources}

\clearpage
\immediate\closeout\fitfile
\end{document}
"""



LOEB_TEMPLATE = r"""% Prototype C at volume scale — originals verso, English recto.
% Auto-generated by tools/transcript2tex.py --layout loeb.
\documentclass[10pt,twoside]{book}
\input{preamble}
\usepackage{fancyhdr}
\usepackage{ifthen}
\setlength{\headheight}{14pt}

\newcommand{\headL}{ΕΥΧΑΙ ΚΑΘΗΜΕΡΙΝΑΙ.\ $\cdot$\ PRECES QUOTIDIANÆ.}
\newcommand{\headR}{THE DAILY PRAYERS.}
\newcommand{\sethead}[1]{\renewcommand{\headL}{#1}\renewcommand{\headR}{#1}}
\pagestyle{fancy}\fancyhf{}
\fancyhead[CE]{\small\headL}
\fancyhead[CO]{\small\headR}
\fancyhead[LE,RO]{\small\thepage}
\fancyhead[RE,LO]{\footnotesize\color{rulegray}[\,\rightmark\,]}
\renewcommand{\headrulewidth}{0pt}

\newcommand{\parthead}[1]{\clearpage\thispagestyle{empty}\vspace*{2.2in}%
  \addcontentsline{toc}{part}{#1}%
  {\centering\Huge\scshape #1\par}\clearpage}

\newwrite\fitfile
\immediate\openout\fitfile=\jobname.fit
\newcommand{\versoalign}{\clearpage
  \ifodd\value{page}
    \null\thispagestyle{empty}\write\fitfile{B \thepage}\clearpage
  \fi}

% A minipage cannot break across leaves: it overruns in silence. So every unit is
% boxed, its height written out, and only then set — python compares the height
% against \textheight. This is the measurement the mirror got from page marks.
\newcommand{\originals}[3]{%
  \setbox0=\vbox{\noindent
    \begin{minipage}[t]{0.485\textwidth}
      \footnotesize\setlength{\plhang}{1.5em}#2
    \end{minipage}\hfill
    \begin{minipage}[t]{0.485\textwidth}
      \footnotesize\setlength{\plhang}{1.5em}#3
    \end{minipage}\par}%
  % ⚠ \ht0 ALONE IS WRONG HERE and silently reported ~5.7pt for every Part I
  % verso until 2026-08-09. This vbox's content is ONE LINE of two tall boxes, so
  % its height is just that line's height above the baseline and the whole column
  % sits in the DEPTH. Measure ht+dp. (\originalsone and \enleaf are multi-line
  % vboxes and were never affected.)
  \immediate\write\fitfile{H O #1 \the\dimexpr\ht0+\dp0\relax}\box0}

\newcommand{\originalsone}[3]{%
  \setbox0=\vbox{\hsize=\textwidth\footnotesize\setlength{\plhang}{1.5em}#2}%
  \immediate\write\fitfile{H O #1 \the\ht0}%
  \ifthenelse{\equal{#3}{epigraph}}{\dropto{0.16}\box0}{\box0}}

\newcommand{\enleaf}[3]{%
  \setbox0=\vbox{\hsize=\textwidth\small#2}%
  \immediate\write\fitfile{H E #1 \the\ht0}%
  \ifthenelse{\equal{#3}{epigraph}}{\dropto{0.16}\box0}{\box0}}

% ---- the two foot-bands -------------------------------------------------
% The Loeb leaves roughly 44% of every leaf empty, and a Loeb's foot is where an
% apparatus belongs. The verso band carries the apparatus criticus against the
% originals; the recto band carries explanatory notes against the English.
%
% ⚠ The band is set at the FOOT, which means the leaf must be composed as a box
% of exactly \textheight with \vfill between body and band. \vfil alone will not
% do it: the preamble sets \raggedbottom, whose own bottom glue competes with it
% and lands the band a third of the way up. Same trap as the display leaves.
%
% ⚠ The band is measured INTO the fit record (\dimexpr body + band), not beside
% it. A band that overruns is exactly as silent as a minipage that overruns, and
% the point of the instrument is that nothing is unmeasured — which is how Part
% I's verso went 131 leaves without ever being tested.
% ⚠ The \par after the rule is load-bearing: without it the rule is just an inline
% box and the band's first word sets on the same line as the rule.
\newcommand{\bandrule}{\par\vspace{5pt}%
  {\noindent\color{rulegray}\rule{0.28\textwidth}{0.4pt}\par}\vspace{3.5pt}}

\newcommand{\apparatusband}[1]{%
  \bandrule{\scriptsize\setlength{\parindent}{0pt}\setlength{\parskip}{1pt}%
    \raggedright #1\par}}

\newcommand{\notesband}[1]{%
  \bandrule{\footnotesize\setlength{\parindent}{0pt}\setlength{\parskip}{2pt}%
    #1\par}}

% Compose a leaf whose body sits at the top and whose band sits at the foot.
\newcommand{\bandleaf}[2]{\vbox to \textheight{#1\vfill#2}}

\newcommand{\originalsn}[4]{%
  \setbox0=\vbox{\noindent
    \begin{minipage}[t]{0.485\textwidth}
      \footnotesize\setlength{\plhang}{1.5em}#2
    \end{minipage}\hfill
    \begin{minipage}[t]{0.485\textwidth}
      \footnotesize\setlength{\plhang}{1.5em}#3
    \end{minipage}\par}%
  \setbox2=\vbox{\hsize=\textwidth\apparatusband{#4}}%
  \immediate\write\fitfile{H O #1 \the\dimexpr\ht0+\dp0+\ht2+\dp2\relax}%
  \bandleaf{\box0}{\box2}}

\newcommand{\originalsonen}[4]{%
  \setbox0=\vbox{\hsize=\textwidth\footnotesize\setlength{\plhang}{1.5em}#2}%
  \setbox2=\vbox{\hsize=\textwidth\apparatusband{#4}}%
  \immediate\write\fitfile{H O #1 \the\dimexpr\ht0+\ht2+\dp2\relax}%
  \bandleaf{\box0}{\box2}}

\newcommand{\enleafn}[4]{%
  \setbox0=\vbox{\hsize=\textwidth\small#2}%
  \setbox2=\vbox{\hsize=\textwidth\notesband{#4}}%
  \immediate\write\fitfile{H E #1 \the\dimexpr\ht0+\ht2+\dp2\relax}%
  \bandleaf{\box0}{\box2}}

% Place a display block a fixed way down the leaf. NOT \vfil: the preamble sets
% \raggedbottom, whose own bottom glue competes with any \vfil pair and lands the
% block about a third of the way down by accident. A title page sits where it is
% put, so put it.
\newcommand{\dropto}[1]{\vspace*{#1\textheight}}

% A leaf composed as one box of exactly the text height, so \vfill inside it
% divides the leaf instead of competing with \raggedbottom's bottom glue.
\newcommand{\fullleaf}[1]{\thispagestyle{empty}%
  \vbox to \textheight{#1}\clearpage}

% A display leaf: the 1853's own title and half-title pages, which are not running
% text and must not be set as though they were. \pl is redefined to drop its
% indent and centre, so the fragment renders as the page it is.
\newcommand{\titleleaf}[2]{\thispagestyle{empty}%
  \dropto{0.28}%
  \begingroup\centering
    \renewcommand{\parasep}{\par\vspace{2.4\baselineskip}}%
    \renewcommand{\pl}[2]{\par{\Large\scshape ##2}}%
    #2\par
  \endgroup}

\begin{document}
\frontmatter
\pagestyle{plain}
\immediate\write\fitfile{T \the\textheight}

% half-title
\fullleaf{\vspace*{0.30\textheight}
  {\centering{\LARGE\scshape Preces Privatae}\par}\vfill}
\fullleaf{}

% title page
\fullleaf{\vspace*{0.14\textheight}
  {\centering
  {\Huge\scshape Preces Privatae}\\[0.35em]
  {\large\itshape Private Prayers}\\[2.4em]
  {\Large Lancelot Andrewes}\\[0.6em]
  {\small\itshape Bishop of Winchester, 1555--1626}\\[3em]
  {\small Greek, Latin and Hebrew as printed in the}\\
  {\small edition of J.\,H. Parker, Oxford, 1853,}\\
  {\small reprinting the Sheldonian text of 1675,}\\[0.5em]
  {\small with a new English translation}%%SCOPELINE%%\par}
  \vfill
  {\centering\small\scshape Wroot Press\par}}

% colophon
\fullleaf{\vfill
  {\raggedright\footnotesize
  The Greek, Latin and Hebrew are transcribed from the 1853 Parker
  edition, which is in the public domain.\par\medskip
  The English translation, the apparatus and the editorial matter are
  \copyright{} Wroot Press, and are issued under a Creative Commons
  Attribution\,--\,NonCommercial 4.0 licence.\par\medskip
  Set in Cardo.\par}}

\tableofcontents
\clearpage

\input{front/preface}

\mainmatter
\pagestyle{fancy}

%%BODY%%

\backmatter
% Plain style: the fancy heads carry the 1853 shoulder-note in \rightmark, which
% the back matter has no use for and would otherwise fight with its own \markboth.
\pagestyle{plain}
\input{back/sources}

\clearpage
\immediate\closeout\fitfile
\end{document}
"""


if __name__ == "__main__":
    main()
