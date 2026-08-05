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


def base_sky(width: int, height: int, dx: float = 0.0, dy: float = 0.0) -> list[float]:
    """The scene, optionally SHIFTED by (dx, dy) pixels.

    The gradient is a property of the sensor, not the sky, so it does NOT move
    with the dither — only the stars do. That asymmetry is deliberate: a
    registration pass that latches onto the gradient instead of the stars would
    otherwise look correct.
    """
    # A dozen stars spread over the field, spanning ~30x in brightness. Three
    # was enough to look like a star field but not enough for offset recovery
    # to be a real test: a consensus vote over pairs needs sources it can
    # disagree about, and a detector needs faint ones it can miss.
    stars = [
        (0.25, 0.35,  9000.0, 1.8), (0.60, 0.55,  5000.0, 1.2),
        (0.80, 0.25, 15000.0, 2.6), (0.15, 0.70,  7000.0, 1.5),
        (0.45, 0.15, 11000.0, 2.0), (0.70, 0.80,  3000.0, 1.3),
        (0.35, 0.85,  6500.0, 1.6), (0.90, 0.60,  8000.0, 1.9),
        (0.10, 0.20,  4000.0, 1.4), (0.55, 0.40, 12000.0, 2.2),
        (0.85, 0.90,  2500.0, 1.2), (0.30, 0.55,  5500.0, 1.7),
    ]
    stars = [(fx * width, fy * height, amp, sig) for fx, fy, amp, sig in stars]
    sky = []
    for y in range(height):
        for x in range(width):
            v = 1200.0 + 6.0 * x + 3.0 * y  # gradient — fixed to the sensor
            for sx, sy, amp, sig in stars:
                d2 = (x - (sx + dx)) ** 2 + (y - (sy + dy)) ** 2
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
    ap.add_argument("--dither", type=float, default=0.0,
                    help="max per-frame star shift in pixels (0 = aligned)")
    ap.add_argument("--truth", help="write the injected per-frame offsets here")
    args = ap.parse_args()

    w, h, n = args.width, args.height, args.frames
    rng = LCG(args.seed)
    truth = []

    with open(args.out, "wb") as fh:
        fh.write(MAGIC)
        fh.write(struct.pack("<III", w, h, n))
        for fi in range(n):
            # Frame 0 is the reference and never moves; the rest dither by a
            # known sub-pixel amount, which is what the oracle checks recovery
            # against. Ground truth beats a differential here — a registration
            # bug that both implementations share would survive a differential.
            if fi == 0 or args.dither == 0.0:
                dx = dy = 0.0
            else:
                dx = (rng.uniform() * 2.0 - 1.0) * args.dither
                dy = (rng.uniform() * 2.0 - 1.0) * args.dither
            truth.append((dx, dy))
            sky = base_sky(w, h, dx, dy)
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

    if args.truth:
        with open(args.truth, "w") as th:
            for dx, dy in truth:
                th.write(f"{dx:.9f} {dy:.9f}\n")
    print(f"wrote {args.out}: {w}x{h} x {n} frames, {args.rays} rays/frame, "
          f"dither +/-{args.dither}px, seed {args.seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
