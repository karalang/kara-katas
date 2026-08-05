#!/usr/bin/env python3
"""
check_register.py — ground-truth check for Cumulus registration.

Compares the offsets `cumulus register` recovered against the dithers
gen_frames.py actually injected. This is GROUND TRUTH, not a differential: a
registration bug that a numpy reimplementation would share — a sign convention,
a centroid bias, a detector that latches onto cosmic rays — survives a
differential and dies here.

That is not hypothetical. The first working version recovered the offsets with
the SIGN INVERTED and nobody would have noticed from a stack; and before that,
raw mean/sd statistics let cosmic rays raise the detection threshold above most
of the real stars. Both were caught by this comparison.

Unlike the integration oracle, this one uses a TOLERANCE, and that is correct
rather than a concession: centroiding a noisy PSF is a measurement, so the
question is whether the error is small enough to stack with, not whether it is
zero. Sub-pixel registration wants ~0.1 px; the gate is set at 0.25 px per axis
with a mean well under that.

Usage: check_register.py truth.txt register_output.txt
"""

import sys

MAX_ERR = 0.25   # px, per axis — worst single frame
MAX_MEAN = 0.10  # px, per axis — averaged over frames
MIN_VOTE_FRAC = 0.6  # of the reference star count


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_register.py truth.txt register_output.txt")
        return 2
    truth = [tuple(float(v) for v in line.split())
             for line in open(sys.argv[1]) if line.strip()]

    got, ref_stars = {}, None
    for line in open(sys.argv[2]):
        f = line.split()
        if not f:
            continue
        if f[0] == "ref_stars":
            ref_stars = int(f[1])
        elif f[0] == "frame":
            got[int(f[1])] = (float(f[3]), float(f[5]), int(f[7]))

    if ref_stars is None or not got:
        print("FAIL: no registration output parsed")
        return 1

    ok = True
    sx = sy = 0.0
    worst = 0.0
    for i, (tdx, tdy) in enumerate(truth):
        if i not in got:
            print(f"  frame {i}: MISSING from register output")
            ok = False
            continue
        dx, dy, votes = got[i]
        ex, ey = abs(dx - tdx), abs(dy - tdy)
        sx += ex
        sy += ey
        worst = max(worst, ex, ey)
        if ex > MAX_ERR or ey > MAX_ERR:
            print(f"  frame {i}: err ({ex:.4f}, {ey:.4f}) px exceeds {MAX_ERR}")
            ok = False
        # A frame that stacked on a 2-star "consensus" is a frame that got
        # lucky. Requiring most of the reference stars to agree is what makes
        # the offset trustworthy rather than merely close on this seed.
        if votes < MIN_VOTE_FRAC * ref_stars:
            print(f"  frame {i}: only {votes} votes of {ref_stars} reference stars")
            ok = False

    n = len(truth)
    mx, my = sx / n, sy / n
    print(f"  frames {n}, ref stars {ref_stars}")
    print(f"  mean |err| ({mx:.4f}, {my:.4f}) px, worst {worst:.4f} px")
    if mx > MAX_MEAN or my > MAX_MEAN:
        print(f"  FAIL: mean error exceeds {MAX_MEAN} px")
        ok = False

    # Non-vacuity: if the injected dithers were all ~zero the comparison proves
    # nothing, because a register step that always answered (0, 0) would pass.
    spread = max(max(abs(a), abs(b)) for a, b in truth)
    if spread < 0.5:
        print("  FAIL: truth dithers are ~zero — this would pass a no-op register")
        ok = False

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
