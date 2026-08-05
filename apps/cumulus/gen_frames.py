#!/usr/bin/env python3
"""
gen_frames.py — synthetic sub-frame generator for Cumulus.

Writes a deterministic stack of 16-bit mono frames in the `.cstack` container
(see FORMAT below). Content is shaped to make the two integration modes
DISAGREE where it matters:

  * a smooth sky gradient + a few Gaussian stars  — the signal
  * per-frame Gaussian read noise                 — what averaging removes
  * per-frame cosmic-ray hits (single hot pixels) — what sigma clipping removes
                                                    and a plain mean does NOT

Without the cosmic rays, mean and sigma-clip agree everywhere and the oracle
proves nothing about rejection. With them, any pixel carrying a hit differs
between the two modes by a large, obvious margin — so a broken clip shows up as
a value difference, not as a subtle rounding wobble.

Deterministic by construction: a fixed-seed LCG, no numpy RNG, no platform
float formatting. The same seed produces byte-identical files anywhere, which is
what lets the oracle assert EXACT equality rather than a tolerance.

FORMAT (`.cstack`, little-endian):
    magic   4 bytes  "CSTK"
    width   u32
    height  u32
    frames  u32
    pixels  frames * height * width * u16, frame-major then row-major

Usage:
    python3 gen_frames.py out.cstack [--width 96] [--height 64] [--frames 16]
                                     [--seed 7] [--rays 12]
"""

import argparse
import math
import struct

MAGIC = b"CSTK"


class LCG:
    """Numerical Recipes LCG — small, exactly reproducible, no library RNG."""

    def __init__(self, seed: int):
        self.s = seed & 0xFFFFFFFF

    def next_u32(self) -> int:
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s

    def uniform(self) -> float:
        return self.next_u32() / 4294967296.0

    def gauss(self, sigma: float) -> float:
        # Box-Muller, one value per call (the discarded twin costs nothing here
        # and keeps the stream position trivially predictable).
        u1 = max(self.uniform(), 1e-12)
        u2 = self.uniform()
        return sigma * math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def base_sky(width: int, height: int) -> list[float]:
    """Static scene: linear gradient + three Gaussian stars."""
    stars = [
        (width * 0.25, height * 0.35, 9000.0, 1.8),
        (width * 0.60, height * 0.55, 5000.0, 1.2),
        (width * 0.80, height * 0.25, 15000.0, 2.6),
    ]
    sky = []
    for y in range(height):
        for x in range(width):
            v = 1200.0 + 6.0 * x + 3.0 * y  # gradient
            for sx, sy, amp, sig in stars:
                d2 = (x - sx) ** 2 + (y - sy) ** 2
                v += amp * math.exp(-d2 / (2.0 * sig * sig))
            sky.append(v)
    return sky


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=96)
    ap.add_argument("--height", type=int, default=64)
    ap.add_argument("--frames", type=int, default=16)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--rays", type=int, default=12,
                    help="cosmic-ray hits per frame (0 disables rejection testing)")
    ap.add_argument("--noise", type=float, default=60.0)
    args = ap.parse_args()

    w, h, n = args.width, args.height, args.frames
    sky = base_sky(w, h)
    rng = LCG(args.seed)

    with open(args.out, "wb") as fh:
        fh.write(MAGIC)
        fh.write(struct.pack("<III", w, h, n))
        for _ in range(n):
            px = [0] * (w * h)
            for i in range(w * h):
                v = sky[i] + rng.gauss(args.noise)
                px[i] = min(65535, max(0, int(v + 0.5)))
            # Cosmic rays: a handful of pixels slammed near saturation. They
            # land in DIFFERENT places each frame, which is exactly the property
            # sigma clipping exploits and a mean cannot.
            for _ in range(args.rays):
                idx = rng.next_u32() % (w * h)
                px[idx] = 60000 + (rng.next_u32() % 5000)
            fh.write(struct.pack(f"<{w * h}H", *px))

    print(f"wrote {args.out}: {w}x{h} x {n} frames, {args.rays} rays/frame, seed {args.seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
