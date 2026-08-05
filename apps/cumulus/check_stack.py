#!/usr/bin/env python3
"""
check_stack.py — did registration actually improve the stack?

`register` proves the offsets are right; this proves they were USED, and used
in the right direction. Both are needed: a pipeline that measures a correct
offset and then resamples by its negation produces a stack that is worse than
doing nothing, and every intermediate check would still pass.

The measurement is star sharpness. A dithered stack integrated WITHOUT
registration smears each star across the dither radius: the peak drops and the
light spreads into the wings. Registering first should raise the peaks and
concentrate the flux. So for the brightest sources:

    peak(registered) > peak(unregistered)          — stars are brighter
    concentration(registered) > concentration(unregistered)

where concentration is peak / (flux in a 7x7 box), i.e. what fraction of a
star's light sits in its core.

Usage: check_stack.py registered.cstack unregistered.cstack
"""

import struct
import sys

import numpy as np

MIN_PEAK_GAIN = 1.05  # registered peaks at least 5% brighter
MIN_CONC_GAIN = 1.02  # and at least 2% more concentrated


def read(path):
    blob = open(path, "rb").read()
    if blob[:4] != b"CSTK":
        raise SystemExit(f"{path}: bad magic")
    w, h, n = struct.unpack("<III", blob[4:16])
    px = np.frombuffer(blob, dtype="<u2", count=w * h * n, offset=16)
    return w, h, px.reshape(n, h, w)[0].astype(np.float64)


def sources(img, k=6.0, n=6):
    """The n brightest 3x3 local maxima, sigma-clipped background."""
    v = img.copy()
    for _ in range(3):
        m, s = v.mean(), v.std()
        v = v[(v >= m - 3 * s) & (v <= m + 3 * s)]
    bg, sd = v.mean(), v.std()
    out = []
    h, w = img.shape
    for y in range(4, h - 4):
        for x in range(4, w - 4):
            c = img[y, x]
            if c > bg + k * sd and c >= img[y - 1:y + 2, x - 1:x + 2].max():
                out.append((c, y, x))
    out.sort(reverse=True)
    return [(y, x) for _, y, x in out[:n]], bg


def measure(img):
    src, bg = sources(img)
    peaks, concs = [], []
    for y, x in src:
        box = img[y - 3:y + 4, x - 3:x + 4] - bg
        flux = float(box[box > 0].sum())
        peak = float(img[y, x] - bg)
        if flux > 0:
            peaks.append(peak)
            concs.append(peak / flux)
    return src, peaks, concs


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_stack.py registered.cstack unregistered.cstack")
        return 2
    _, _, reg = read(sys.argv[1])
    _, _, unreg = read(sys.argv[2])

    rsrc, rpeak, rconc = measure(reg)
    usrc, upeak, uconc = measure(unreg)
    if not rpeak or not upeak:
        print("FAIL: no sources measured")
        return 1

    # Compare on matched counts — the two stacks can detect different numbers.
    k = min(len(rpeak), len(upeak))
    pg = float(np.mean(rpeak[:k]) / np.mean(upeak[:k]))
    cg = float(np.mean(rconc[:k]) / np.mean(uconc[:k]))

    print(f"  sources compared      {k}")
    print(f"  mean peak   reg {np.mean(rpeak[:k]):9.1f}  unreg {np.mean(upeak[:k]):9.1f}  gain {pg:.3f}x")
    print(f"  concentration reg {np.mean(rconc[:k]):7.4f}  unreg {np.mean(uconc[:k]):7.4f}  gain {cg:.3f}x")

    ok = True
    if pg < MIN_PEAK_GAIN:
        print(f"  FAIL: peak gain {pg:.3f} below {MIN_PEAK_GAIN} — offsets not applied, or applied backwards")
        ok = False
    if cg < MIN_CONC_GAIN:
        print(f"  FAIL: concentration gain {cg:.3f} below {MIN_CONC_GAIN}")
        ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
