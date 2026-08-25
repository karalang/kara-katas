#!/usr/bin/env python3
"""
check_nightscape.py — did the sky/foreground mask do its job?

A tripod nightscape has two subjects moving differently: the sky turns, the land
does not. Registering on stars sharpens the stars and SMEARS the land; not
registering does the reverse. A masked stack has to do both at once, and nothing
else in this harness can tell whether it did — a stack with a smeared foreground
is still byte-identical across backends, still passes the integration oracle,
and still recovers its dithers.

So this compares THREE stacks of the same frames and checks the ordering that
only a working mask produces:

    unregistered   land sharp, sky smeared
    sky-only       sky sharp, LAND SMEARED      <- what a DSO stacker does
    masked         sky sharp AND land sharp     <- the point

The metric is gradient energy — mean squared first difference. Smearing a
high-contrast edge lowers it, and the generator's foreground is built to be
pointy (a ridge line, bright windows, a reflection) precisely so the loss is
measurable rather than a rounding difference.

Usage: check_nightscape.py <unregistered> <sky_only> <masked> <horizon>
"""

import struct
import sys

import numpy as np

# The masked land must keep most of the sharpness the unregistered stack has —
# it is the same pixels stacked the same way, so the only losses are the feather
# band and resampling at the edges.
LAND_KEEP = 0.97
# ...and it must beat the sky-only stack by a clear margin, or the mask did
# nothing. Measured 1.23x; the gate sits well below that but well above noise.
LAND_GAIN = 1.08
# The mask must not COST sky sharpness: registration above the horizon is
# untouched by it.
SKY_KEEP = 0.99


def read(path):
    b = open(path, "rb").read()
    if b[:4] != b"CSTK":
        raise SystemExit(f"{path}: bad magic")
    w, h, n = struct.unpack("<III", b[4:16])
    return np.frombuffer(b, dtype="<u2", count=w * h, offset=16).reshape(h, w).astype(np.float64)


def sharpness(a):
    gx = np.diff(a, axis=1)
    gy = np.diff(a, axis=0)
    return float((gx * gx).mean() + (gy * gy).mean())


def main() -> int:
    if len(sys.argv) != 5:
        print("usage: check_nightscape.py <unregistered> <sky_only> <masked> <horizon>")
        return 2
    unreg, skyonly, masked = (read(p) for p in sys.argv[1:4])
    H = int(sys.argv[4])
    # Skip a band either side of the horizon: the feather deliberately blends
    # there and belongs to neither region, so measuring across it would penalise
    # exactly the thing that makes the join invisible.
    pad = 12
    reg = {
        "sky": (slice(0, max(1, H - pad)),),
        "land": (slice(H + pad, None),),
    }

    ok = True
    s = {k: {n: sharpness(a[reg[k]]) for n, a in
             (("unreg", unreg), ("skyonly", skyonly), ("masked", masked))}
         for k in reg}

    for k in ("sky", "land"):
        v = s[k]
        print(f"  {k:5} unreg {v['unreg']:12.0f}  sky-only {v['skyonly']:12.0f}  "
              f"masked {v['masked']:12.0f}")

    land_keep = s["land"]["masked"] / s["land"]["unreg"]
    land_gain = s["land"]["masked"] / s["land"]["skyonly"]
    sky_keep = s["masked"] if False else s["sky"]["masked"] / s["sky"]["skyonly"]
    print(f"  land keeps {land_keep:.3f} of unregistered, beats sky-only by {land_gain:.3f}x")
    print(f"  sky keeps {sky_keep:.3f} of the sky-only stack")

    if land_keep < LAND_KEEP:
        print(f"  FAIL: masked land lost sharpness ({land_keep:.3f} < {LAND_KEEP}) — "
              f"the foreground is being resampled by the sky's transform")
        ok = False
    if land_gain < LAND_GAIN:
        print(f"  FAIL: masked land no better than sky-only ({land_gain:.3f} < {LAND_GAIN}) — "
              f"the mask is not being applied")
        ok = False
    if sky_keep < SKY_KEEP:
        print(f"  FAIL: masked sky lost sharpness ({sky_keep:.3f} < {SKY_KEEP}) — "
              f"the mask is eating into the registered region")
        ok = False

    # Non-vacuity: if sky-only did not smear the land in the first place, there
    # was nothing for the mask to fix and this proves nothing.
    smear = s["land"]["unreg"] / s["land"]["skyonly"]
    if smear < 1.05:
        print(f"  FAIL: sky-only registration barely smeared the land ({smear:.3f}x) — "
              f"the fixture has no foreground to protect")
        ok = False

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
