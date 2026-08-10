#!/usr/bin/env python3.11
"""Adjudication sheet for the continuation backfill.

For each page: the references the index could not see until 2026-08-10, the
English line each one sits on, and the band entry already standing at that
line. ⚠ Untagged is not automatically wrong — §3 and §8 — so this prints the
evidence and decides nothing.
"""
import re, sys, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ref_index, check_notes

ROOT = Path(__file__).resolve().parent.parent

def band():
    out, page = {}, None
    for raw in (ROOT / "apparatus/print-notes.md").read_text().splitlines():
        m = re.match(r"##\s+(\d+)\s*$", raw)
        if m:
            page = int(m.group(1)); out.setdefault(page, [])
            continue
        if page and re.match(r"[SRV]:", raw.strip()):
            out[page].append(raw.strip())
    return out

def main():
    pages = [int(a) for a in sys.argv[1:]]
    idx, bands = ref_index.index(), band()
    cont = {(p, l): (pr, rs) for p, l, pr, rs, *_ in ref_index.CONTINUATIONS}
    eng = check_notes.english_lines() if hasattr(check_notes, "english_lines") else {}
    for pg in pages:
        # ⚠ In Part I the references sit on the LATIN RECTO and the band is keyed
        # to the Greek verso facing it, so an opening must be read as two leaves.
        key = pg if pg % 2 == 0 else pg - 1
        rows = [(src, l, r) for src in (pg, pg + 1)
                for l, r in idx.get(src, []) if (src, l) in cont]
        print(f"\n{'='*72}\nprinted {pg}   (band ## {key})")
        if not rows:
            print("  no continuation references on this page"); continue
        tagged = {}
        for e in bands.get(key, []):
            m = re.match(r"([SRV]):\s*(\d+)", e)
            if m: tagged.setdefault(int(m.group(2)), []).append(e[:100])
        for src, l, r in rows:
            pr, _ = cont[(src, l)]
            here = tagged.get(l)
            mark = "TAGGED" if here else "—"
            print(f"  p{src} line {l:>3}  {pr:<10} -> {r:<20} [{mark}]")
            for e in (here or [])[:2]:
                print(f"           band: {e}")
        print(f"  band lines present: {sorted(tagged)}")

if __name__ == "__main__":
    main()
