#!/usr/bin/env python3
"""Four small plates for the four leads, drawn from primitives.

Each plate is a flat, high-contrast vignette of its story, sized to sit above
the kicker in a lead column. They are drawn rather than photographed: no
gradients, no halftones, no tiny type that would smear at thumbnail size. The
shapes carry the meaning, so a viewer who reads nothing still sees a stalled
climate chart, a blockaded strait, a sinking ship and an aid pipeline cut.

Build time only; main.py ships the bytes this produces.
"""

PAPER = (252, 250, 245)
INK = (17, 17, 17)
RED = (176, 32, 30)
GREY = (96, 92, 86)
HAIR = (214, 208, 196)
SEA = (48, 72, 96)
SAND = (198, 176, 132)
WHITE = (255, 255, 255)


def _frame(d, box, fill=(240, 236, 227)):
    x, y, w, h = box
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=fill, outline=HAIR, width=1)


def climate(d, box):
    """A rising line that stops dead: the talks, and the curve that outran them."""
    x, y, w, h = box
    _frame(d, box)
    # baseline grid, three hairlines, so the plate reads as a chart even small
    for i in range(1, 4):
        gy = y + 6 + (h - 12) * i / 4
        d.line([x + 6, gy, x + w - 7, gy], fill=HAIR, width=1)
    # the temperature curve: six points climbing, then a flat final step
    pts = [(0.10, 0.80), (0.26, 0.70), (0.42, 0.58), (0.58, 0.44),
           (0.74, 0.30), (0.90, 0.30)]
    poly = [(x + 6 + (w - 13) * px, y + 6 + (h - 12) * py) for px, py in pts]
    # filled area under the curve, so the plate carries ink at thumbnail size
    under = poly + [(poly[-1][0], y + h - 7), (poly[0][0], y + h - 7)]
    d.polygon(under, fill=(232, 214, 206))
    d.line(poly, fill=RED, width=max(2, h // 18), joint="curve")
    for px_, py_ in poly:
        r = max(2, h // 22)
        d.ellipse([px_ - r, py_ - r, px_ + r, py_ + r], fill=RED)
    # the last segment is a dashed "and then no agreement" tail
    lx, ly = poly[-1]
    for i in range(3):
        sx = lx + 3 + i * 5
        if sx + 3 < x + w - 5:
            d.line([sx, ly, sx + 3, ly], fill=GREY, width=1)
    # a struck-through target marker at the top left of the curve's rise
    tx, ty = x + w * 0.20, y + h * 0.24
    d.line([tx - 6, ty, tx + 6, ty], fill=INK, width=2)
    d.line([tx, ty - 6, tx, ty + 6], fill=INK, width=2)


def hormuz(d, box):
    """A strait pinched shut: two headlands, a hull held between them."""
    x, y, w, h = box
    _frame(d, box, fill=(226, 232, 238))
    # sea
    d.rectangle([x + 1, y + h * 0.52, x + w - 2, y + h - 2], fill=SEA)
    # two headlands, narrowing to a gap in the middle
    d.polygon([(x + 1, y + 1), (x + w * 0.34, y + 1),
               (x + w * 0.40, y + h * 0.52), (x + 1, y + h * 0.52)], fill=SAND)
    d.polygon([(x + w - 2, y + 1), (x + w * 0.66, y + 1),
               (x + w * 0.60, y + h * 0.52), (x + w - 2, y + h * 0.52)], fill=SAND)
    # a hull in the gap, low and wide
    cx, cy = x + w * 0.50, y + h * 0.66
    hw, hh = w * 0.14, h * 0.09
    d.polygon([(cx - hw, cy - hh), (cx + hw, cy - hh),
               (cx + hw * 0.7, cy + hh), (cx - hw * 0.7, cy + hh)], fill=INK)
    d.rectangle([cx - hw * 0.45, cy - hh * 2.2, cx + hw * 0.1, cy - hh], fill=GREY)
    # the blockade: a chain of dashes across the gap, above the waterline
    by = y + h * 0.50
    for i in range(7):
        sx = x + w * 0.36 + i * (w * 0.28 / 7)
        d.line([sx, by - 3, sx + 3, by + 3], fill=RED, width=2)
    # movement refused: one hull waits on each side of the chain
    for mx in (x + w * 0.26, x + w * 0.74):
        d.polygon([(mx - 5, by + 6), (mx + 5, by + 6),
                   (mx + 3, by + 11), (mx - 3, by + 11)], fill=WHITE)


def sinking(d, box):
    """A corvette going down by the stern, with the drone that found it."""
    x, y, w, h = box
    _frame(d, box, fill=(226, 232, 238))
    d.rectangle([x + 1, y + h * 0.58, x + w - 2, y + h - 2], fill=SEA)
    # the hull, tilted, stern already under the surface
    cx, cy = x + w * 0.46, y + h * 0.56
    L, T = w * 0.30, h * 0.10
    d.polygon([(cx - L, cy + T * 0.6), (cx + L, cy - T * 0.9),
               (cx + L * 0.86, cy - T * 0.1), (cx - L * 0.90, cy + T * 1.5)], fill=INK)
    # superstructure, small against the hull
    d.polygon([(cx - L * 0.12, cy - T * 0.55), (cx + L * 0.30, cy - T * 0.85),
               (cx + L * 0.30, cy - T * 1.45), (cx - L * 0.12, cy - T * 1.15)], fill=GREY)
    # smoke where it was hit
    for i, r in enumerate((3, 5, 7)):
        d.ellipse([cx - L * 0.55 - r, cy - T * 1.4 - i * 5 - r,
                   cx - L * 0.55 + r, cy - T * 1.4 - i * 5 + r], outline=GREY, width=1)
    # surface line broken over the sinking stern
    d.line([x + 2, y + h * 0.58, cx + L * 0.55, y + h * 0.58], fill=WHITE, width=1)
    d.line([cx + L * 0.75, y + h * 0.58, x + w - 3, y + h * 0.58], fill=WHITE, width=1)
    # the drone: a small delta above and to the right, with its track
    dx, dy = x + w * 0.80, y + h * 0.22
    d.polygon([(dx, dy - 4), (dx + 9, dy), (dx, dy + 4), (dx + 3, dy)], fill=RED)
    d.line([dx - 14, dy + 10, dx - 2, dy + 1], fill=RED, width=1)


def aid(d, box):
    """An aid pipeline cut: grain moving along a path that stops at a chokepoint."""
    x, y, w, h = box
    _frame(d, box, fill=(240, 236, 227))
    # the route, a shallow arc from left to right, drawn heavy so it reads as
    # the subject of the plate rather than a hairline in the furniture
    y0 = y + h * 0.66
    pts = []
    for i in range(33):
        t = i / 32.0
        pts.append((x + 10 + (w - 20) * t, y0 - (h * 0.34) * (1 - (2 * t - 1) ** 2)))
    d.line(pts, fill=(222, 206, 186), width=max(7, h // 7))
    d.line(pts, fill=INK, width=max(3, h // 16))
    # three chokepoints, the middle one closed
    for i, t in enumerate((0.18, 0.50, 0.82)):
        px = x + 10 + (w - 20) * t
        py = y0 - (h * 0.34) * (1 - (2 * t - 1) ** 2)
        r = max(5, h // 11)
        if i == 1:
            d.ellipse([px - r - 3, py - r - 3, px + r + 3, py + r + 3], fill=RED)
            d.line([px - r, py - r, px + r, py + r], fill=WHITE, width=3)
            d.line([px - r, py + r, px + r, py - r], fill=WHITE, width=3)
        else:
            d.ellipse([px - r, py - r, px + r, py + r], fill=WHITE, outline=INK, width=2)
    # grain: a small block of sheaves at the left end of the route
    for i in range(4):
        gx = x + 14 + i * 9
        d.line([gx, y + h * 0.12, gx, y + h * 0.30], fill=INK, width=2)
        d.line([gx - 4, y + h * 0.16, gx, y + h * 0.12], fill=INK, width=2)
        d.line([gx + 4, y + h * 0.16, gx, y + h * 0.12], fill=INK, width=2)
    d.line([x + 10, y + h - 9, x + w - 11, y + h - 9], fill=HAIR, width=1)
