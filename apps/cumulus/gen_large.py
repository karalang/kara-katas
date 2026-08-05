#!/usr/bin/env python3
"""
gen_large.py — realistically-sized synthetic subs, for SCALE testing only.

gen_frames.py is deterministic by construction (a hand-rolled LCG, no library
RNG) because the correctness oracles assert EXACT equality. That determinism
costs a pure-Python loop per pixel, which is fine at 96x64 and hopeless at
12 megapixels — 187 million pixels across a 16-frame stack.

This generator uses numpy instead. It is explicitly NOT for the exact oracles:
it does not reproduce gen_frames.py's byte stream, and nothing here should ever
be compared against `oracle.py`. Correctness is already pinned at small scale by
the deterministic path; what this file exists to answer is different — how the
pipeline behaves on real-sized frames, in time and in memory.

The scene matches gen_frames.py in kind (sensor-fixed gradient, Gaussian stars
scaled to the frame, read noise, cosmic rays, per-frame dither) so the measured
work is representative rather than degenerate: a frame of flat noise would give
the star detector nothing to find and the timings would mean nothing.

Usage:
    python3 gen_large.py out.cstack --width 4144 --height 2822 --frames 16
"""

import argparse
import struct

import numpy as np

MAGIC = b"CSTK"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=4144)
    ap.add_argument("--height", type=int, default=2822)
    ap.add_argument("--frames", type=int, default=16)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--noise", type=float, default=60.0)
    ap.add_argument("--dither", type=float, default=3.0)
    ap.add_argument("--stars", type=int, default=400)
    ap.add_argument("--rays", type=int, default=200)
    args = ap.parse_args()

    w, h, n = args.width, args.height, args.frames
    rng = np.random.default_rng(args.seed)

    # Star field: positions in fractional coordinates so density is independent
    # of frame size, brightness spanning ~30x as in the small generator.
    sx = rng.uniform(0.02, 0.98, args.stars) * w
    sy = rng.uniform(0.02, 0.98, args.stars) * h
    amp = rng.uniform(2000, 30000, args.stars)
    sig = rng.uniform(1.2, 2.8, args.stars)

    ys, xs = np.arange(h)[:, None], np.arange(w)[None, :]
    gradient = (1200.0 + 6.0 * xs / w * 96 + 3.0 * ys / h * 64).astype(np.float32)

    with open(args.out, "wb") as fh:
        fh.write(MAGIC)
        fh.write(struct.pack("<III", w, h, n))
        for fi in range(n):
            dx = 0.0 if fi == 0 else rng.uniform(-args.dither, args.dither)
            dy = 0.0 if fi == 0 else rng.uniform(-args.dither, args.dither)

            frame = np.broadcast_to(gradient, (h, w)).astype(np.float32).copy()
            # Stamp each star into a local box — a full-frame Gaussian per star
            # would be 400 x 11.7M element-ops and dominate generation time.
            for k in range(args.stars):
                cx, cy, a, s = sx[k] + dx, sy[k] + dy, amp[k], sig[k]
                r = int(np.ceil(4 * s))
                x0, x1 = max(0, int(cx) - r), min(w, int(cx) + r + 1)
                y0, y1 = max(0, int(cy) - r), min(h, int(cy) + r + 1)
                if x1 <= x0 or y1 <= y0:
                    continue
                gx = np.arange(x0, x1)[None, :] - cx
                gy = np.arange(y0, y1)[:, None] - cy
                frame[y0:y1, x0:x1] += a * np.exp(-(gx * gx + gy * gy) / (2 * s * s))

            frame += rng.normal(0, args.noise, (h, w)).astype(np.float32)

            ri = rng.integers(0, w * h, args.rays)
            flat = frame.reshape(-1)
            flat[ri] = 60000 + rng.integers(0, 5000, args.rays)

            np.clip(frame, 0, 65535, out=frame)
            fh.write(frame.astype("<u2").tobytes())
            print(f"  frame {fi + 1}/{n}", end="\r", flush=True)

    mb = (16 + w * h * n * 2) / 1e6
    print(f"wrote {args.out}: {w}x{h} x{n} = {w * h / 1e6:.1f} Mpx/frame, {mb:.0f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
