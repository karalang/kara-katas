#!/usr/bin/env python3
"""
check_tiff.py — did the RGB TIFF path keep the colours it was given?

The failure this exists to catch is not a crash. A three-plane pipeline that
transposes R and B, or that mis-strides the chunky interleave by one sample,
produces a perfectly well-formed stack of exactly the right size, sharp stars
included — and every other oracle in this repo passes it. Only the COLOUR is
wrong, and only against a scene whose colours were known in advance.

gen_tiff.py renders that scene from gen_cfa.py's star table, which carries
deliberate ratios: a red star at 1.00:0.35:0.20, a blue one at 0.25:0.45:1.00,
and neutral ones. This reads the stacked result back and compares.

Usage:
    python3 check_tiff.py stacked.cstack
"""

import struct
import sys

from gen_cfa import STARS

# Per-star tolerance on a channel ratio, normalised so the brightest channel is
# 1.0. Wide enough to absorb photon noise and the sub-pixel resample, nowhere
# near wide enough to absorb a channel swap: the red star's R:B is 5:1, so a
# transposition moves that ratio by 400%.
TOL = 0.06

# The stars whose colour is unambiguous enough to assert on: strongly coloured,
# or exactly neutral. The mid-tone ones are left out — a 0.90:1.00:0.70 star is
# a weak discriminator, and asserting on it would only add tolerance.
PICK = [0, 1, 2]

# Local background is the lower OCTILE of the window rather than its minimum:
# the minimum is a single noise sample, and subtracting it biases every star by
# the depth of one noise excursion.
HALF = 3


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_tiff.py stacked.cstack")
        return 2
    data = open(sys.argv[1], "rb").read()
    if data[:4] != b"CSTK":
        print("check_tiff: not a .cstack")
        return 1
    w, h, planes = struct.unpack("<III", data[4:16])
    if planes != 3:
        print(f"check_tiff: expected 3 planes, got {planes}")
        return 1
    px = struct.unpack(f"<{w * h * 3}H", data[16:16 + w * h * 6])
    np = w * h

    worst = 0.0
    bad = 0
    for i in PICK:
        fx, fy, amp, sig, col = STARS[i]
        cx, cy = int(fx * w), int(fy * h)
        if not (HALF <= cx < w - HALF and HALF <= cy < h - HALF):
            print(f"check_tiff: star {i} is too close to the edge to measure")
            return 1
        got = []
        for k in range(3):
            win = [px[k * np + (cy + dy) * w + cx + dx]
                   for dy in range(-HALF, HALF + 1)
                   for dx in range(-HALF, HALF + 1)]
            floor = sorted(win)[len(win) // 8]
            got.append(max(win) - floor)
        gm, em = max(got), max(col)
        if gm <= 0:
            print(f"check_tiff: star {i} has no signal in any channel")
            return 1
        gr = [v / gm for v in got]
        er = [v / em for v in col]
        err = max(abs(a - b) for a, b in zip(gr, er))
        worst = max(worst, err)
        flag = "" if err <= TOL else "   <-- OFF"
        print(f"  star {i} R:G:B  got " + ":".join(f"{v:.2f}" for v in gr)
              + "  want " + ":".join(f"{v:.2f}" for v in er)
              + f"  (max err {err:.3f}){flag}")
        if err > TOL:
            bad += 1

    # Non-vacuity: a scene whose stars were all near-neutral would pass the loop
    # above no matter what the pipeline did with the channels.
    #
    # This is computed from the INJECTED table, not from the result, and the
    # distinction is the whole point. Measuring the result's discrimination
    # instead looks equivalent and is not: a genuine R/B transposition inverts
    # it, so the run fails with "your fixture is weak" when what actually
    # happened is "your pipeline swapped two channels" — the checker blaming
    # its own input for the defect it was built to find.
    want_red = STARS[0][4][0] / STARS[0][4][2]
    want_blue = STARS[1][4][0] / STARS[1][4][2]
    print(f"  fixture discrimination  red star R/B {want_red:.2f}, "
          f"blue star R/B {want_blue:.2f} (injected)")
    if want_red < 2.0 or want_blue > 0.5:
        print("FAIL: the injected stars are not distinctly coloured — this "
              "check could not have caught a channel transposition")
        return 1

    if bad:
        print(f"FAIL: {bad} star(s) outside {TOL:.2f} of the injected colour")
        return 1
    print(f"PASS  (worst channel-ratio error {worst:.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
