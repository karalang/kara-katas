#!/usr/bin/env python3
"""
gen_cal.py — a synthetic session WITH the sensor defects calibration removes.

Every frame this corpus generated until now was optically perfect: no readout
offset, no thermal signal, no vignetting, no dust. That is why nothing needed
calibration, and it is also why calibration could not be TESTED — subtracting a
zero dark and dividing by a flat that is uniformly 1 is indistinguishable from
doing nothing.

So this writes four sets, and the defects are FIXED patterns rather than noise —
identical in every frame, which is exactly why stacking cannot remove them and
more integration time makes them cleaner rather than smaller:

  lights/  the scene through the optics, with dark signal and bias added after
  darks/   the dark signal alone (thermal + bias), same exposure as the lights
  flats/   the vignetting profile alone (plus its own, shorter-exposure bias)
  bias/    the readout offset alone

and `truth.cstack`, the same scene with NO defects at all. That last one is what
makes the check meaningful: a calibrated stack should converge on it, and an
uncalibrated one must not.

The defect model, in the order a sensor applies it:

    light = scene * vignette + thermal + bias      <- what lands
    dark  =                    thermal + bias      <- shutter closed
    flat  = uniform * vignette         + bias      <- even illumination

The vignette multiplies the SCENE ONLY. Dark current and readout bias are
generated in the silicon, downstream of the optics — light never passed through
a lens to become them, so they are not attenuated by one. The first version of
this generator wrote `(scene + thermal) * vignette + bias`, and calibrating it
made the result 1.4x WORSE than doing nothing, with hot pixels rising from 8 to
24: subtracting an unvignetted dark from a vignetted one leaves a residue
shaped like the vignette, and the hot pixels came back as holes-turned-spikes.
The generator was wrong, not the calibrator — but the failure looked exactly
like a broken calibrator, which is the argument for deriving the model from the
physics rather than from whatever makes the numbers move.

Usage:
    python3 gen_cal.py outdir [--frames 12] [--width 96] [--height 64]
"""

import argparse
import math
import os
import struct

from gen_frames import LCG, base_sky
from gen_fits import write_fits

MAGIC = b"CSTK"

BIAS_LEVEL = 500.0        # readout offset, flat across the sensor
BIAS_TILT = 40.0          # ...with a slight gradient, as real ones have
DARK_BASE = 300.0         # thermal signal at the lights' exposure
HOT_PIXELS = 24           # stuck-bright photosites, identical every frame
HOT_LEVEL = 45000.0
DUST_MOTES = 6            # dark blobs in the flat
VIGNETTE = 0.42           # corner falloff: response drops to 1-VIGNETTE


def vignette_map(w: int, h: int) -> list[float]:
    """Multiplicative response: 1.0 at the centre, falling off radially."""
    cx, cy = (w - 1) / 2.0, (h - 1) / 2.0
    rmax = math.hypot(cx, cy)
    m = []
    for y in range(h):
        for x in range(w):
            r = math.hypot(x - cx, y - cy) / rmax
            m.append(1.0 - VIGNETTE * r * r)
    return m


def add_dust(m: list[float], w: int, h: int, rng: LCG) -> None:
    """Dust motes: small, soft, DARK circles on the flat."""
    for _ in range(DUST_MOTES):
        cx = rng.uniform() * w
        cy = rng.uniform() * h
        rad = 2.0 + rng.uniform() * 3.0
        depth = 0.25 + rng.uniform() * 0.35
        for y in range(max(0, int(cy - rad * 2)), min(h, int(cy + rad * 2) + 1)):
            for x in range(max(0, int(cx - rad * 2)), min(w, int(cx + rad * 2) + 1)):
                d2 = (x - cx) ** 2 + (y - cy) ** 2
                m[y * w + x] *= 1.0 - depth * math.exp(-d2 / (2 * rad * rad))


def dark_map(w: int, h: int, rng: LCG) -> list[float]:
    """Thermal signal: a smooth amp-glow ramp plus fixed hot pixels."""
    d = []
    for y in range(h):
        for x in range(w):
            # Amp glow: brightest in one corner, as a real sensor's is.
            d.append(DARK_BASE * (1.0 + 1.6 * ((w - x) / w) * ((h - y) / h)))
    for _ in range(HOT_PIXELS):
        d[rng.next_u32() % (w * h)] = HOT_LEVEL
    return d


def bias_map(w: int, h: int) -> list[float]:
    return [BIAS_LEVEL + BIAS_TILT * (x / w) for y in range(h) for x in range(w)]


def write_cstack(path, frames, w, h):
    with open(path, "wb") as fh:
        fh.write(MAGIC)
        fh.write(struct.pack("<III", w, h, len(frames)))
        for f in frames:
            fh.write(struct.pack(f"<{len(f)}H", *f))


def clamp(v):
    return min(65535, max(0, int(v + 0.5)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--width", type=int, default=96)
    ap.add_argument("--height", type=int, default=64)
    ap.add_argument("--frames", type=int, default=12)
    ap.add_argument("--cal-frames", type=int, default=8)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--noise", type=float, default=25.0)
    args = ap.parse_args()

    w, h, n = args.width, args.height, args.frames
    os.makedirs(args.outdir, exist_ok=True)
    for sub in ("lights", "darks", "flats", "bias"):
        os.makedirs(os.path.join(args.outdir, sub), exist_ok=True)

    # The defect maps are drawn ONCE and reused by every frame — that is what
    # makes them calibratable rather than noise.
    fixed = LCG(args.seed)
    vign = vignette_map(w, h)
    add_dust(vign, w, h, fixed)
    dark = dark_map(w, h, fixed)
    bias = bias_map(w, h)

    rng = LCG(args.seed + 1)
    scene = base_sky(w, h, 0.0, 0.0)
    truth = []

    for i in range(n):
        clean, dirty = [0] * (w * h), [0] * (w * h)
        for j in range(w * h):
            noise = rng.gauss(args.noise)
            clean[j] = clamp(scene[j] + noise)
            # Optics attenuate the SCENE; thermal signal and bias are added
            # afterwards, in the silicon, untouched by the lens.
            dirty[j] = clamp((scene[j] + noise) * vign[j] + dark[j] + bias[j])
        truth.append(clean)
        write_fits(os.path.join(args.outdir, "lights", f"sub_{i:03d}.fits"), dirty, w, h)

    for i in range(args.cal_frames):
        # A dark frame is thermal + bias: the shutter is closed, so the only
        # things present are the two the optics never touched.
        d = [clamp(dark[j] + bias[j] + rng.gauss(args.noise)) for j in range(w * h)]
        write_fits(os.path.join(args.outdir, "darks", f"d_{i:03d}.fits"), d, w, h)
        # Flats are a uniform illumination through the same optics, at their own
        # (shorter) exposure — so they carry bias but not the lights' thermal
        # signal. That is the whole reason --bias exists.
        f = [clamp(30000.0 * vign[j] + bias[j] + rng.gauss(args.noise)) for j in range(w * h)]
        write_fits(os.path.join(args.outdir, "flats", f"f_{i:03d}.fits"), f, w, h)
        b = [clamp(bias[j] + rng.gauss(args.noise)) for j in range(w * h)]
        write_fits(os.path.join(args.outdir, "bias", f"b_{i:03d}.fits"), b, w, h)

    write_cstack(os.path.join(args.outdir, "truth.cstack"), truth, w, h)
    print(f"wrote {n} lights + {args.cal_frames} each of darks/flats/bias to "
          f"{args.outdir}: {w}x{h}, vignette {VIGNETTE:.0%}, {HOT_PIXELS} hot px, "
          f"{DUST_MOTES} dust motes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
