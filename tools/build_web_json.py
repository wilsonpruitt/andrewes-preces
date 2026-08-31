#!/usr/bin/env python3
"""Build the JSON the web reader consumes (WEB-PLAN.md §4-§5).

⚠⚠ ADDITIVE ONLY (WEB-PLAN §0). This imports from proof2tex / transcript2tex /
ref_index and never edits them — those three files are also what the printed
cover's page count depends on, and the print book is already submitted to KDP.

    python3.11 tools/build_web_json.py               # write site/src/data/*.json
    python3.11 tools/build_web_json.py --check-lines # gate only, writes nothing

Emits:
    site/src/data/content.json    — sections, in reading order (§5)
    site/src/data/scripture.json  — ref_index.index(), raw (marked references only;
                                     the S:-band merge in WEB-PLAN §9 is W4 work)
    site/src/data/apparatus.json  — transcript2tex.load_notes(), raw (W3 renders it)
"""
import argparse
import json
import re
from pathlib import Path

from proof2tex import COMMENT, GAP, HEBREW, SUPERS, parse_pages, sections_for
import ref_index
import transcript2tex

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "src" / "data"

# ⚠ Same test proof2tex.render_line uses to decide a line renders to nothing —
# kept byte-identical on purpose (§4.2): the sense-line count this script hands
# out must agree with ref_index.index(), and both must agree with what actually
# prints.
BLANK_AFTER_COMMENT = lambda line: not COMMENT.sub("", line).strip()

BOLD = re.compile(r"\*\*((?:[^*]|\*(?!\*))+?)\*\*")
ITAL = re.compile(r"\*([^*]+?)\*")
SUP_CH = re.compile("[" + "".join(SUPERS) + "]")
UNCLEAR = re.compile(r"\[\?\]")
SUPPLIED = re.compile(r"\[[^\[\]]*\]")


def _emphasis_spans(text: str):
    """Bold first (it may enclose italic), then italic — mirrors proof2tex.md_emph."""
    spans, pos = [], 0
    for m in BOLD.finditer(text):
        if m.start() > pos:
            spans += _italic_spans(text[pos:m.start()])
        spans.append({"kind": "strong", "children": _italic_spans(m.group(1))})
        pos = m.end()
    if pos < len(text):
        spans += _italic_spans(text[pos:])
    return spans


def _italic_spans(text: str):
    spans, pos = [], 0
    for m in ITAL.finditer(text):
        if m.start() > pos:
            spans.append({"kind": "text", "text": text[pos:m.start()]})
        spans.append({"kind": "em", "text": m.group(1)})
        pos = m.end()
    if pos < len(text) or not spans:
        spans.append({"kind": "text", "text": text[pos:]})
    return spans


def _mark_spans(text: str, pattern, kind):
    """Split `text` on `pattern`, tagging matches as `kind` and recursing on the
    rest through `_emphasis_spans`. Non-overlapping, applied before emphasis."""
    spans, pos = [], 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            spans += _emphasis_spans(text[pos:m.start()])
        spans.append({"kind": kind, "text": m.group(0)})
        pos = m.end()
    if pos < len(text):
        spans += _emphasis_spans(text[pos:])
    return spans if spans else _emphasis_spans(text)


def web_line(raw: str):
    """Sibling to proof2tex.render_line (§4.1): same regexes, structure instead
    of TeX. Returns None for a blank/comment-only line — NOT a sense-line, and
    that exclusion must match ref_index.index() exactly (§4.2)."""
    line = COMMENT.sub("", raw).rstrip()
    if not line.strip():
        return None
    indent = len(line) - len(line.lstrip(" "))
    body = line.strip()

    gaps = []

    def stash(m):
        gaps.append(len(m.group(1)))
        return "\x00%d\x00" % (len(gaps) - 1)

    body = GAP.sub(stash, body)

    # unclear marks before supplied brackets ([?] is a special case of [...]),
    # then Hebrew, then the printed-279 superscript letters, then emphasis.
    spans = []
    for chunk, is_special in _split(body, UNCLEAR):
        if is_special:
            spans.append({"kind": "unclear", "text": chunk})
            continue
        for chunk2, is_supplied in _split(chunk, SUPPLIED):
            if is_supplied:
                spans.append({"kind": "supplied", "text": chunk2})
                continue
            for chunk3, is_heb in _split(chunk2, HEBREW):
                if is_heb:
                    spans.append({"kind": "hebrew", "text": chunk3})
                    continue
                spans += _mark_spans(chunk3, SUP_CH, "sup")

    # resolve the stashed gap placeholders, wherever they landed (inside a plain
    # "text" span only — a gap never falls inside markdown emphasis in practice,
    # but guard it rather than assume)
    def resolve(span):
        if "text" not in span:
            if "children" in span:
                span["children"] = [resolve(c) for c in span["children"]]
            return span
        parts = re.split(r"\x00(\d+)\x00", span["text"])
        if len(parts) == 1:
            return span
        out = []
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    out.append({"kind": "text", "text": part})
            else:
                out.append({"kind": "gap", "width": gaps[int(part)]})
        return out

    resolved = []
    for s in spans:
        r = resolve(s)
        resolved.extend(r) if isinstance(r, list) else resolved.append(r)

    return {"indent": indent, "spans": resolved}


def _split(text: str, pattern):
    """[(chunk, matched_bool), ...] splitting `text` on `pattern`, in order."""
    out, pos = [], 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], False))
        out.append((m.group(0), True))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False))
    if not out:
        out.append((text, False))
    return out


def render_page_lines(lines):
    """A page's raw source lines -> [{"n", "indent", "spans"} | {"break": true}],
    numbering sense-lines 1..N exactly as ref_index.index() does: comment-only
    and blank lines take no number, and a leading/trailing/duplicated blank
    collapses to a single paragraph break (mirrors proof2tex.render_block)."""
    out, n, prev_blank = [], 0, True
    for raw in lines:
        w = web_line(raw)
        if w is None:
            if not prev_blank:
                out.append({"break": True})
                prev_blank = True
            continue
        n += 1
        out.append({"n": n, **w})
        prev_blank = False
    while out and out[-1] == {"break": True}:
        out.pop()
    return out


def build_content():
    """[{id, part, label, pages:[{n, layers:{lay: [line...]}}]}]"""
    pages = transcript2tex.volume_pages([1, 2, 3])
    used = set()
    sections = []
    for part in (1, 2, 3):
        for tr, en, label in sections_for(part):
            stem = tr.name[: -len("-transcript.md")]
            tr_blocks = parse_pages(tr)
            en_blocks = parse_pages(en) if en else {}
            own = sorted(set(tr_blocks) | set(en_blocks))
            section_pages = []
            for n in own:
                if n in used:
                    continue
                used.add(n)
                slot = pages[n]
                layers = {}
                if slot["body"]:
                    layers[slot["layer"]] = render_page_lines(slot["body"])
                if slot["en"]:
                    layers["en"] = render_page_lines(slot["en"])
                if layers:
                    section_pages.append({"n": n, "layers": layers})
            if section_pages:
                sections.append({
                    "id": f"part{part}/{stem}",
                    "part": part,
                    "label": label,
                    "pages": section_pages,
                })
    return sections


def build_scripture():
    idx = ref_index.index()
    return {str(p): [{"line": ln, "ref": ref} for ln, ref in rows]
            for p, rows in sorted(idx.items()) if rows}


def build_apparatus():
    notes = transcript2tex.load_notes()
    return {str(p): bands for p, bands in sorted(notes.items())}


def check_lines(content):
    """§4.2's gate: the last sense-line number this script assigns on a page
    must not exceed the highest line any scripture reference cites there —
    a reference can only be numbered inside the text that carries it. Also
    pins the two ground-truths ref_index.py's own docstring gives by eye:
    printed 34 line 27, and printed 115's `Cruce` at line 9 (not 11)."""
    idx = ref_index.index()
    counts = {}
    for sec in content:
        for pg in sec["pages"]:
            n = max((ln["n"] for layer in pg["layers"].values()
                     for ln in layer if "n" in ln), default=0)
            counts[pg["n"]] = n

    failures = []
    for page, rows in idx.items():
        if not rows:
            continue
        hi = max(ln for ln, _ in rows)
        mine = counts.get(page, 0)
        if hi > mine:
            failures.append(f"printed {page}: ref_index cites line {hi}, "
                             f"but this build only numbered {mine} lines")

    def find_line_text(page, line_no):
        for sec in content:
            for pg in sec["pages"]:
                if pg["n"] != page:
                    continue
                for layer in pg["layers"].values():
                    for ln in layer:
                        if ln.get("n") == line_no:
                            return "".join(
                                s.get("text", "") for s in ln["spans"]
                                if s["kind"] not in ("gap",))
        return None

    checks = [(34, 27, "Τὰ ἔργα"), (115, 9, "Cruce")]
    for page, line, needle in checks:
        text = find_line_text(page, line)
        if text is None or needle not in text:
            failures.append(f"printed {page} line {line}: expected to find "
                             f"{needle!r}, got {text!r}")

    if failures:
        print(f"✗ {len(failures)} line-numbering disagreement(s):")
        for f in failures:
            print(f"   {f}")
        return False
    print(f"✓ line numbering agrees with ref_index.index() on all "
          f"{sum(1 for r in idx.values() if r)} pages carrying a reference, "
          f"and both ground-truth spot checks hold")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-lines", action="store_true",
                     help="run the gate only; write nothing")
    args = ap.parse_args()

    content = build_content()
    ok = check_lines(content)
    if args.check_lines:
        raise SystemExit(0 if ok else 1)
    if not ok:
        raise SystemExit("refusing to write JSON: line-numbering gate failed")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "content.json").write_text(json.dumps(content, ensure_ascii=False, indent=1))
    (OUT / "scripture.json").write_text(
        json.dumps(build_scripture(), ensure_ascii=False, indent=1))
    (OUT / "apparatus.json").write_text(
        json.dumps(build_apparatus(), ensure_ascii=False, indent=1))
    npages = sum(len(s["pages"]) for s in content)
    print(f"wrote content.json ({len(content)} sections, {npages} pages), "
          f"scripture.json, apparatus.json -> {OUT}")


if __name__ == "__main__":
    main()
