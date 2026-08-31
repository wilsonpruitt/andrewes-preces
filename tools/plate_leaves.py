#!/usr/bin/env python3
"""The printed page -> plate image map (WEB-PLAN.md §10.2).

    python3.11 tools/plate_leaves.py            # write site/src/data/plate.json
    python3.11 tools/plate_leaves.py --verify N # fetch the image for printed N

⚠⚠⚠ THREE MAPPINGS LOOK PLAUSIBLE HERE AND TWO OF THEM ARE WRONG.

1. `STRUCTURE.md`'s offset table is the **GOOGLE** scan
   (`precesprivataeq00andrgoog`), whose offset runs +19 -> +45 and whose "PDF"
   numbers are that file's pages. It says nothing about Toronto. This is why
   WEB-PLAN says never to port it, and it is not ported here.

2. The Toronto item's own `_scandata.xml` gives a complete per-leaf
   `pageNumber` (436 printed pages, one leaf each, offset +12 -> +42). It is
   ACCURATE about leaves and USELESS as an image index: `leafCount` is 522 but
   the derivative carries 480 images, because archive.org drops the duplicate
   and insert leaves. Tested and failed by eye — scandata puts printed 30 at
   leaf 46, but image n45 is printed 34 and n46 is not printed 30.

3. The djvu OCR carries the running-head numeral only sometimes: it reads on
   printed 34 and is simply absent on printed 77, where the numeral sits far
   right and the OCR dropped it. It cannot complete a table on its own.

✅ WHAT IS TRUE, AND IT IS SIMPLER THAN ANY OF THEM: because the derivative
excludes exactly the duplicate leaves that make the LEAF offset drift, the
IMAGE index is a constant offset from the printed page.

        image n = printed page + 11

VERIFIED BY EYE at eight pages spanning the whole volume, chosen to include the
tail that memory flags as duplicate-riddled:

    printed   2 -> n13    (no numeral on a section opening; verified on CONTENT
                           against our own notes for page 2 — Daniel kneeling
                           three times, *seven times a day do I praise thee*,
                           *in all places where I record my name*)
    printed  30 -> n41     running head "30", ΤΗΣ ΠΡΩΤΗΣ ΗΜΕΡΑΣ — chosen as a
                           page that was NOT used to fit the rule, to test it
    printed  34 -> n45     running head "34"
    printed  77 -> n88     running head "77"
    printed 277 -> n288    running head "277"
    printed 381 -> n392    running head "381"   ⚠ inside the hazard zone: the
                           380/381 spread is scanned THREE times in the Google
                           copy, and Toronto's derivative still holds at +11
    printed 414 -> n425    running head "414"
    printed 436 -> n447    running head "436", the volume's last page

⚠ Pages between the anchors are DERIVED from the rule and were not each opened.
That is a weaker claim than "every leaf verified", so the reader is told what it
is being shown: the plate viewer prints the page it believes it is showing, and
the plate carries its own number in the running head. A wrong mapping is
therefore visible to the reader at a glance rather than silent — which is the
point of WEB-PLAN's "treat an unverified entry as absent".
"""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "src" / "data"

ITEM = "precesprivataequ00andruoft"
OFFSET = 11
FIRST, LAST = 1, 436
VERIFIED = [2, 30, 34, 77, 277, 381, 414, 436]


def image_n(printed: int) -> int:
    return printed + OFFSET


def url(printed: int) -> str:
    return f"https://archive.org/download/{ITEM}/page/n{image_n(printed)}.jpg"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", type=int, help="download the plate for a printed page")
    args = ap.parse_args()

    if args.verify:
        out = f"/tmp/plate-{args.verify}.jpg"
        subprocess.run(["curl", "-sSL", "--max-time", "120", "-o", out, url(args.verify)],
                       check=True)
        print(f"printed {args.verify} -> {url(args.verify)}\nsaved {out}\n"
              f"⚠ OPEN IT AND READ THE RUNNING HEAD before trusting it.")
        return

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "plate.json").write_text(json.dumps({
        "item": ITEM,
        "offset": OFFSET,
        "first": FIRST,
        "last": LAST,
        "verified": VERIFIED,
        "source": "University of Toronto 1853, archive.org, greyscale",
    }, indent=1))
    print(f"wrote plate.json — n = printed + {OFFSET}, "
          f"printed {FIRST}-{LAST}, {len(VERIFIED)} pages verified by eye")


if __name__ == "__main__":
    main()
