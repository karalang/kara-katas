#!/usr/bin/env python3
"""
gen_cfa.py — synthetic COLOUR subs on a Bayer mosaic, as FITS.

This is the data shape a RAW file becomes. Siril, and every other stacker,
converts CR3/NEF/ARW to a FITS sequence before doing any astronomy; what comes
out is one 16-bit plane per sub with a `BAYERPAT` card saying how the colour
filter array is laid out. So this generator produces the thing the pipeline
actually has to handle, without any of the vendor-format archaeology in
between.

Deterministic by construction (the same fixed-seed LCG as gen_frames.py, no
library RNG), because the CFA oracle asserts EXACT equality.

Two properties are deliberately built in, both of which exist to make a WRONG
answer visible rather than plausible:

  * Stars carry distinct R:G:B ratios — a red one, a blue one, neutral ones.
    If the demosaic phase is off by a pixel, or R and B are transposed, the red
    star comes out blue. A monochrome scene would hide that completely.
  * The sky gradient is stronger in R (light pollution usually is) and, as in
    gen_frames.py, is fixed to the SENSOR — it does not move with the dither.
    A registration pass that latches onto the gradient rather than the stars
    would otherwise look correct.

Usage:
    python3 gen_cfa.py outdir [--frames 16] [--width 96] [--height 64]
                              [--pattern RGGB] [--dither 3.0] [--truth t.txt]
"""

import argparse
import math
import os

from gen_frames import LCG
from gen_fits import write_fits

# Star field, in fractional coordinates: (fx, fy, amp, sigma, (r, g, b)).
# The colour weights multiply `amp` per channel.
#
# Sigma is in SUPERPIXEL units and is doubled when rendered onto the mosaic —
# i.e. the PSF spans about twice as many photosites as it does output pixels.
# That is not a convenience for the test, it is the condition a colour sensor
# has to satisfy to work at all: a PSF narrower than the 2x2 filter tile is
# sampled by only one or two filters, so the star's measured colour depends on
# which photosite it happened to land on. Undersample and you get false-colour
# stars — the CFA equivalent of aliasing. A generator that ignored this would
# produce data no real telescope produces, and would make the pipeline look
# worse than it is.
STARS = [
    (0.25, 0.35,  9000.0, 1.8, (1.00, 0.35, 0.20)),  # red — catches an R/B swap
    (0.60, 0.55,  5000.0, 1.2, (0.25, 0.45, 1.00)),  # blue — the other half
    (0.80, 0.25, 15000.0, 2.6, (1.00, 1.00, 1.00)),
    (0.15, 0.70,  7000.0, 1.5, (0.90, 1.00, 0.70)),
    (0.45, 0.15, 11000.0, 2.0, (1.00, 0.80, 0.55)),
    (0.70, 0.80,  3000.0, 1.3, (1.00, 1.00, 1.00)),
    (0.35, 0.85,  6500.0, 1.6, (0.55, 0.75, 1.00)),
    (0.90, 0.60,  8000.0, 1.9, (1.00, 0.95, 0.85)),
    (0.10, 0.20,  4000.0, 1.4, (1.00, 1.00, 1.00)),
    (0.55, 0.40, 12000.0, 2.2, (0.80, 1.00, 0.90)),
    (0.85, 0.90,  2500.0, 1.2, (1.00, 1.00, 1.00)),
    (0.30, 0.55,  5500.0, 1.7, (1.00, 0.60, 0.40)),
]

# Per-channel sky pedestal and gradient. R carries more, as light pollution
# does; a channel transposition shifts the background too, not just the stars.
SKY = {
    "R": (1400.0, 7.0, 3.5),
    "G": (1200.0, 6.0, 3.0),
    "B": (1050.0, 5.0, 2.5),
}


def channel_at(pattern: str, x: int, y: int) -> str:
    """Which filter sits over photosite (x, y).

    `pattern` names the 2x2 tile anchored at STORED row 0, column 0 — i.e. the
    first row of the data section as written, not the bottom-up row order FITS
    inherited from its tape-era conventions. That ambiguity is real and is why
    the `ROWORDER` card exists; this generator writes ROWORDER='TOP-DOWN' and
    the reader refuses anything else rather than guessing.
    """
    return pattern[(y % 2) * 2 + (x % 2)]


def render(w: int, h: int, pattern: str, dx: float, dy: float) -> list[float]:
    """The mosaicked scene at a given dither, before noise."""
    px = [0.0] * (w * h)
    # sigma is given in superpixel units; the mosaic samples at twice that rate.
    stars = [(fx * w, fy * h, amp, sig * 2.0, col) for fx, fy, amp, sig, col in STARS]
    ci = {"R": 0, "G": 1, "B": 2}
    for y in range(h):
        for x in range(w):
            c = channel_at(pattern, x, y)
            ped, gx, gy = SKY[c]
            # Gradient is normalised to the 96x64 reference field so the scene
            # looks the same at any frame size.
            v = ped + gx * (x / w) * 96.0 + gy * (y / h) * 64.0
            k = ci[c]
            for sx, sy, amp, sig, col in stars:
                d2 = (x - (sx + dx)) ** 2 + (y - (sy + dy)) ** 2
                if d2 < (5.0 * sig) ** 2:  # 5 sigma — beyond it the term is noise
                    v += amp * col[k] * math.exp(-d2 / (2.0 * sig * sig))
            px[y * w + x] = v
    return px


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--width", type=int, default=192)
    ap.add_argument("--height", type=int, default=128)
    ap.add_argument("--frames", type=int, default=16)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--rays", type=int, default=12)
    ap.add_argument("--noise", type=float, default=60.0)
    ap.add_argument("--pattern", default="RGGB", choices=["RGGB", "BGGR", "GRBG", "GBRG"])
    ap.add_argument("--dither", type=float, default=0.0,
                    help="max per-frame star shift, in MOSAIC pixels (0 = aligned)")
    ap.add_argument("--truth", help="write the injected per-frame offsets here")
    args = ap.parse_args()

    if args.width % 2 or args.height % 2:
        print("gen_cfa: width and height must be even — a mosaic tiles in 2x2")
        return 2

    w, h, n = args.width, args.height, args.frames
    rng = LCG(args.seed)
    os.makedirs(args.outdir, exist_ok=True)
    truth = []

    for i in range(n):
        # Frame 0 is the reference and never moves, matching gen_frames.py, so
        # recovered offsets are directly comparable between the two paths.
        if i == 0 or args.dither == 0.0:
            dx = dy = 0.0
        else:
            dx = (rng.uniform() * 2.0 - 1.0) * args.dither
            dy = (rng.uniform() * 2.0 - 1.0) * args.dither
        truth.append((dx, dy))

        scene = render(w, h, args.pattern, dx, dy)
        px = [0] * (w * h)
        for j in range(w * h):
            v = scene[j] + rng.gauss(args.noise)
            px[j] = min(65535, max(0, int(v + 0.5)))
        for _ in range(args.rays):
            px[rng.next_u32() % (w * h)] = 60000 + (rng.next_u32() % 5000)

        write_fits(
            os.path.join(args.outdir, f"sub_{i:03d}.fits"), px, w, h,
            extra=[("BAYERPAT", f"'{args.pattern}'", "colour filter array"),
                   ("ROWORDER", "'TOP-DOWN'", "BAYERPAT anchors at stored row 0")],
        )

    if args.truth:
        with open(args.truth, "w") as th:
            for dx, dy in truth:
                th.write(f"{dx:.9f} {dy:.9f}\n")

    print(f"wrote {n} CFA FITS frames to {args.outdir}: {w}x{h}, "
          f"BAYERPAT={args.pattern}, dither +/-{args.dither} mosaic px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
