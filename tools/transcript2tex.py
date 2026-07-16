#!/usr/bin/env python3
"""Convert day1-transcript.md / day1-english.md page blocks into TeX fragments.

Emits prototypes/fragments/{gr,la,en}NNN[ab].tex — one fragment per printed page
(split into a/b at unit boundaries where configured). Each source line becomes
\\pl{<em-indent>}{<text>}; blank lines become \\parasep; *italics* -> \\emph{};
Hebrew runs -> \\RL{}; HTML comments stripped.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRAG = ROOT / "prototypes" / "fragments"

# pages included in the M2 sample
GR_PAGES = [30, 32, 34, 36, 38, 40, 42]
LA_PAGES = [31, 33, 35, 37, 39, 41, 43]
EN_PAGES = [30, 32, 34, 36, 38, 40, 42]

# unit-boundary splits: (kind, page) -> line-prefix that starts part b
SPLITS = {
    ("gr", 32): "ΟΙΚΤΙΡΜΟΝ",
    ("la", 33): "MISERICORS",
    ("en", 32): "MERCIFUL",
    ("gr", 40): "ΑΙΡΩ",
    ("la", 41): "Attollo",
    ("en", 40): "I LIFT UP",
    ("gr", 42): "סיג",
    ("la", 43): "SEPES",
    ("en", 42): "סיג",
}

HEBREW = re.compile(r"[֐-׿][֐-׿\s]*[֐-׿]|[֐-׿]")
COMMENT = re.compile(r"<!--.*?-->")


def tex_escape(s: str) -> str:
    s = s.replace("\\", r"\textbackslash{}")
    for c, r in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\~{}"),
                 ("^", r"\^{}")]:
        s = s.replace(c, r)
    return s


def render_line(raw: str) -> str:
    line = COMMENT.sub("", raw).rstrip()
    if not line.strip():
        return r"\parasep"
    indent = (len(line) - len(line.lstrip(" "))) // 4
    text = line.strip()
    text = tex_escape(text)
    text = re.sub(r"\*([^*]+)\*", r"\\emph{\1}", text)
    text = HEBREW.sub(lambda m: r"\RL{%s}" % m.group(0), text)
    return r"\pl{%.2f}{%s}" % (indent * 1.4, text)


def parse_pages(path: Path, marker: str):
    """marker: 'printed (N) (PDF' for transcript, 'printed (N) — English' for english"""
    pages, cur = {}, None
    for raw in path.read_text().splitlines():
        m = re.match(r"<!-- printed (\d+)", raw)
        if m:
            cur = int(m.group(1))
            pages[cur] = []
            continue
        if cur is not None:
            pages[cur].append(raw)
    # trim leading/trailing blanks
    for k, v in pages.items():
        while v and not v[0].strip():
            v.pop(0)
        while v and not v[-1].strip():
            v.pop()
    return pages


def emit(kind: str, page: int, lines):
    key = (kind, page)
    parts = {"": lines}
    if key in SPLITS:
        pre = SPLITS[key]
        idx = next(i for i, l in enumerate(lines) if l.strip().startswith(pre))
        a, b = lines[:idx], lines[idx:]
        while a and not a[-1].strip():
            a.pop()
        parts = {"a": a, "b": b}
    for suffix, ls in parts.items():
        out = FRAG / f"{kind}{page:03d}{suffix}.tex"
        body = "\n".join(render_line(l) for l in ls)
        out.write_text(body + "\n")
        print(f"wrote {out.name} ({len(ls)} lines)")


def emit_halves(page: int, lines):
    """Split a full English page block at the blank line nearest its middle
    (fallback: middle line) -> enNNN-h1.tex / enNNN-h2.tex for the B register."""
    mid = len(lines) // 2
    blanks = [i for i, l in enumerate(lines) if not l.strip() and abs(i - mid) <= 4]
    cut = min(blanks, key=lambda i: abs(i - mid)) if blanks else mid
    halves = {"h1": lines[:cut], "h2": lines[cut:]}
    for name, ls in halves.items():
        while ls and not ls[0].strip():
            ls.pop(0)
        while ls and not ls[-1].strip():
            ls.pop()
        out = FRAG / f"en{page:03d}-{name}.tex"
        out.write_text("\n".join(render_line(l) for l in ls) + "\n")
        print(f"wrote {out.name} ({len(ls)} lines)")


def main():
    FRAG.mkdir(parents=True, exist_ok=True)
    tr = parse_pages(ROOT / "part1" / "day1-transcript.md", "transcript")
    en = parse_pages(ROOT / "part1" / "day1-english.md", "english")
    for p in GR_PAGES:
        emit("gr", p, tr[p])
    for p in LA_PAGES:
        emit("la", p, tr[p])
    for p in EN_PAGES:
        emit("en", p, en[p])
        emit_halves(p, en[p])


if __name__ == "__main__":
    main()
