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

# Rotation gates, in DEGREES. Looser-looking than the translation ones but
# tighter in effect: on the 96x64 frames this runs at, 0.15 deg is 0.15 px of
# corner error, well inside the sub-pixel bar the translation gate sets. The
# error is a centroid measurement like any other, so it shrinks on the larger
# frames a real session produces — a rotation fit gets MORE precise with a
# longer lever arm, not less.
MAX_ROT_ERR = 0.15
MAX_ROT_MEAN = 0.06


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
            # `frame N dx D dy D rot R votes V stars S`. Rotation reporting was
            # added with the rotation slice; tolerate its absence so an older
            # register output still parses rather than silently mis-indexing
            # `votes` — which is exactly what a positional parser does when a
            # field is inserted ahead of it.
            if "rot" in f:
                k = f.index("rot")
                got[int(f[1])] = (float(f[3]), float(f[5]), float(f[k + 1]),
                                  int(f[f.index("votes") + 1]))
            else:
                got[int(f[1])] = (float(f[3]), float(f[5]), 0.0, int(f[7]))

    if ref_stars is None or not got:
        print("FAIL: no registration output parsed")
        return 1

    ok = True
    sx = sy = sr = 0.0
    worst = worst_rot = 0.0
    for i, t in enumerate(truth):
        tdx, tdy = t[0], t[1]
        trot = t[2] if len(t) > 2 else 0.0
        if i not in got:
            print(f"  frame {i}: MISSING from register output")
            ok = False
            continue
        dx, dy, rot, votes = got[i]
        er = abs(rot - trot)
        sr += er
        worst_rot = max(worst_rot, er)
        if er > MAX_ROT_ERR:
            print(f"  frame {i}: rotation err {er:.4f} deg exceeds {MAX_ROT_ERR}")
            ok = False
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
    mx, my, mr = sx / n, sy / n, sr / n
    print(f"  frames {n}, ref stars {ref_stars}")
    print(f"  mean |err| ({mx:.4f}, {my:.4f}) px, worst {worst:.4f} px")
    print(f"  rotation  mean |err| {mr:.4f} deg, worst {worst_rot:.4f} deg")
    if mx > MAX_MEAN or my > MAX_MEAN:
        print(f"  FAIL: mean error exceeds {MAX_MEAN} px")
        ok = False
    if mr > MAX_ROT_MEAN:
        print(f"  FAIL: mean rotation error exceeds {MAX_ROT_MEAN} deg")
        ok = False

    # Non-vacuity: if the injected dithers were all ~zero the comparison proves
    # nothing, because a register step that always answered (0, 0) would pass.
    spread = max(max(abs(t[0]), abs(t[1])) for t in truth)
    rot_spread = max((abs(t[2]) for t in truth if len(t) > 2), default=0.0)
    if spread < 0.5 and rot_spread < 0.5:
        print("  FAIL: truth dithers AND rotations are ~zero — this would pass "
              "a no-op register")
        ok = False
    # If rotation was injected, the recovered values must actually track it. A
    # build that always answered 0 would otherwise sail through on the
    # translation numbers alone.
    if rot_spread >= 0.5:
        got_rot_spread = max(abs(v[2]) for v in got.values())
        if got_rot_spread < 0.5 * rot_spread:
            print(f"  FAIL: injected up to {rot_spread:.2f} deg of rotation but "
                  f"recovered at most {got_rot_spread:.2f} — not tracking it")
            ok = False

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
