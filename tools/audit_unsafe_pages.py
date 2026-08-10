#!/usr/bin/env python3.11
"""Hand-audit aid for the pages `check_notes.py` CANNOT compare.

    python3.11 tools/audit_unsafe_pages.py 14 18 192

⚠ WHY. On a page whose Latin recto and English run different line counts, the
tag's line number and the plate's line number are DIFFERENT COUNTS, so nothing
mechanical can check them and check_notes reports the page as UNCHECKED. This
prints, per tag: the line the tag claims, the line the plate prints that exact
reference on, and the English at both — enough to hand-map.

⚠ THE TELL, and it is what found the three broken pages: on a parity-mismatched
page, a tag whose line number EQUALS the plate's Latin line was probably keyed
straight off `ref_index --stub` and never hand-mapped. Where the numbers differ,
someone did the work. Printed 14, 18 and 192 all showed tag == plate and all
three were wrong; 40, 48, 62, 64, 86, 214 and 262 showed tag != plate and all
seven were right.

⚠ Equal numbers are NOT proof of an error — 6, 8, 68, 82, 128 and 258 are equal
and correct, because their columns diverge after the last tagged line. Read the
English before changing anything.
"""
import re, sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
import ref_index, check_notes as C
idx=ref_index.index(); notes=C.load_notes(); FRAG=C.ROOT/"prototypes"/"fragments"
def lines(pre,n):
    f=FRAG/f"{pre}{n:03d}.tex"
    if not f.exists(): return []
    out=[]
    for m in re.finditer(r"\\pl\{(?:\[[^\]]*\])?\s*(.*)", f.read_text()):
        s=re.sub(r"\\[a-zA-Z]+\*?\s*","",m.group(1)); s=re.sub(r"[{}]","",s)
        out.append(re.sub(r"\s+"," ",s).strip()[:64])
    return out
for p in [int(x) for x in sys.argv[1:]]:
    en=lines("en",p); refpage=p+1 if p<=263 and p%2==0 else p
    pl={}
    for ln,r in idx.get(refpage,[]):
        c=C.citation(r)
        if c: pl.setdefault(c,[]).append(ln)
    la=lines("la",refpage); gr=lines("gr",p)
    print(f"\n{'='*74}\nprinted {p}: Greek {len(gr)} | Latin {len(la)} | English {len(en)}")
    for s,ln,body in notes.get(p,[]):
        if s!="S" or not ln: continue
        for m in C.CITE.finditer(re.sub(r"^\d+\s+","",body)):
            c=C.citation(m.group(0))
            if not c or c not in pl: continue
            for L in pl[c]:
                flag = "  <<< tag line != plate line" if L!=ln else ""
                print(f"  {m.group(0).strip():<20} tagL{ln:<3} plateL{L:<3}{flag}")
                print(f"      EN@{ln}: {en[ln-1] if 0<ln<=len(en) else '!! none'}")
                if L!=ln:
                    print(f"      EN@{L}: {en[L-1] if 0<L<=len(en) else '!! none'}")
