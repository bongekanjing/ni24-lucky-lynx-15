#!/usr/bin/env python3
"""Verify the rendered page without looking at it.

Regenerates the page with ImageDraw.text wrapped so that every call's ink
box is recorded, then checks:
  * no ink box leaves the 1024 x 1024 canvas;
  * no two ink boxes overlap (padding-aware, since adjacent type legitimately
    sits close but never on top of another line);
  * no dead panel: every band of the page carries ink;
  * the deck, the footer and the date are present as strings.
Then checks the file itself: PNG magic, exact 1024x1024, <= 1 MiB.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tools.front as front  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

W = H = 1024
MAX = 1048576

THRESH = 0.05        # a box must intrude more than 5% into another to count
calls = []
_orig = ImageDraw.ImageDraw.text


def rec_text(self, xy, text, *a, **kw):
    f = kw.get("font")
    if f is None and len(a) >= 1:
        f = a[0]
    if text and str(text).strip():
        try:
            box = self.textbbox(xy, text, font=f)
        except Exception:
            box = None
        if box is not None:
            calls.append((str(text), box, self))
    return _orig(self, xy, text, *a, **kw)


ImageDraw.ImageDraw.text = rec_text

out = Path(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
front.render(out)
ImageDraw.ImageDraw.text = _orig

fails = []

# 1. every box inside the canvas
out_of_canvas = []
for text, box, _ in calls:
    if box[0] < -0.5 or box[1] < -0.5 or box[2] > W + 0.5 or box[3] > H + 0.5:
        out_of_canvas.append((text, box))
print("text calls            : %d" % len(calls))
print("boxes off canvas      : %d" % len(out_of_canvas))
for t, b in out_of_canvas[:8]:
    print("   OFF %.1f %.1f %.1f %.1f  %r" % (b[0], b[1], b[2], b[3], t[:48]))
if out_of_canvas:
    fails.append("boxes off canvas")


def overlap_area(a, b):
    x = min(a[2], b[2]) - max(a[0], b[0])
    y = min(a[3], b[3]) - max(a[1], b[1])
    return (x * y) if (x > 0 and y > 0) else 0.0


def area(b):
    return max(1e-6, (b[2] - b[0]) * (b[3] - b[1]))


# 2. no two boxes overlap by more than THRESH of the smaller box
overlaps = []
for i in range(len(calls)):
    ti, bi, _ = calls[i]
    for j in range(i + 1, len(calls)):
        tj, bj, _ = calls[j]
        ov = overlap_area(bi, bj)
        if ov <= 0:
            continue
        share = ov / min(area(bi), area(bj))
        if share > THRESH:
            overlaps.append((share, ti, bi, tj, bj))
overlaps.sort(reverse=True, key=lambda r: r[0])
print("overlapping pairs     : %d" % len(overlaps))
for sh, ti, bi, tj, bj in overlaps[:8]:
    print("   %.0f%%  %r %s  vs  %r %s"
          % (sh * 100, ti[:30], tuple(round(v) for v in bi),
             tj[:30], tuple(round(v) for v in bj)))
if overlaps:
    fails.append("overlapping text")

# 3. the date, deck and footer strings are on the sheet
ink = " ".join(t for t, _, _ in calls)
for needle in ("24 NOVEMBER 2026", "TUESDAY", "26 briefs in 8 beats",
               "COP31 ends in collapse", "7.3 million", "New Zealand"):
    if needle not in ink:
        fails.append("missing copy: %s" % needle)
        print("MISSING               : %s" % needle)

# 4. no dead band: scan 32 px rows for ink
img = Image.open(out).convert("RGB")
px = img.load()
bg = front.PAPER
empty_rows = []
for y0 in range(0, H, 32):
    inked = 0
    for y in range(y0, min(y0 + 32, H)):
        for x in range(0, W, 4):
            if px[x, y] != bg:
                inked += 1
                break
        if inked > 2:
            break
    if inked <= 2:
        empty_rows.append(y0)
print("empty 32px bands      : %d %s" % (len(empty_rows), empty_rows[:10]))
if empty_rows:
    fails.append("dead band at %s" % empty_rows[:5])

# 5. file-level checks
size = out.stat().st_size
with out.open("rb") as fh:
    magic = fh.read(8)
print("file                  : %s" % out)
print("bytes                 : %d  (cap %d)" % (size, MAX))
print("png magic             : %s" % (magic == b"\x89PNG\r\n\x1a\n"))
print("pixels                : %dx%d" % img.size)
if magic != b"\x89PNG\r\n\x1a\n":
    fails.append("not a PNG")
if img.size != (W, H):
    fails.append("wrong size")
if size > MAX:
    fails.append("over the cap")

# 6. both runs identical: render again in memory, compare bytes
second = Path(out).with_name("verify_second.png")
front.render(second)
same = out.read_bytes() == second.read_bytes()
print("render twice identical: %s" % same)
if not same:
    fails.append("non-deterministic render")

print()
if fails:
    print("FAIL: " + "; ".join(fails))
    sys.exit(1)
print("PASS: canvas, overlap, copy, dead bands, file limits, determinism")
