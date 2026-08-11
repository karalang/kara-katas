#!/usr/bin/env python3
"""
check_cal.py — the calibration oracle.

Calibration is unusual in this corpus: its correctness cannot be checked by
comparing two implementations, because both would be applying the same formula
to the same masters. What makes it checkable is that gen_cal.py knows the CLEAN
scene — the one the sensor defects were added to — so there is a ground truth
that neither implementation authored.

Three checks:

  1. against TRUTH   a calibrated stack must land close to the clean scene, and
                     an uncalibrated one must not — the second half matters as
                     much as the first, since a calibrator that did nothing
                     would pass a one-sided check on quiet data
  2. hot pixels      the dark's stuck-bright photosites must be GONE, not merely
                     reduced; they are the sharpest single indicator that the
                     subtraction happened and had the right sign
  3. vignetting      the corner-to-centre response ratio must match truth's,
                     which is what the flat division is for

Comparison is on frames NORMALISED to mean 1. Flat normalisation deliberately
preserves the flat's own mean, so a calibrated frame is the scene times a
constant; comparing raw levels would fail a correct calibrator for a reason that
has nothing to do with correctness.

Usage:
    python3 check_cal.py <cumulus-binary> <session-dir>
"""

import subprocess
import sys
from pathlib import Path

import numpy as np

# Calibrated must be at least this many times closer to truth than raw.
MIN_IMPROVEMENT = 5.0
# ...and raw must be at least this far off, or the data cannot show anything.
MIN_RAW_ERROR = 0.02
MAX_CAL_ERROR = 0.05
# Corner/centre response, against truth's own ratio.
MAX_VIGNETTE_ERR = 0.05


def read(path):
    b = Path(path).read_bytes()
    assert b[:4] == b"CSTK", f"{path}: bad magic"
    w, h, n = np.frombuffer(b[4:16], dtype="<u4")
    px = np.frombuffer(b[16:16 + int(w) * int(h) * int(n) * 2], dtype="<u2")
    return px.astype(float).reshape(int(n), int(h), int(w))[0]


def run(binary, *args):
    r = subprocess.run([binary, *[str(a) for a in args]], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"cumulus failed: {r.stdout}{r.stderr}")
    return r.stdout


def main() -> int:
    binary = sys.argv[1] if len(sys.argv) > 1 else "./cumulus"
    d = Path(sys.argv[2] if len(sys.argv) > 2 else "cal")
    fails = 0

    # Masters are ordinary Cumulus outputs — the same integration modes that
    # stack lights, applied to calibration subs. Nothing bespoke.
    for name, sub in (("dark", "darks"), ("flat", "flats"), ("bias", "bias")):
        run(binary, d / f"{name}.cstack", "sigmaclip", *sorted((d / sub).glob("*.fits")))

    lights = sorted((d / "lights").glob("*.fits"))
    run(binary, d / "raw.cstack", "sigmaclip", *lights)
    run(binary, d / "cal.cstack", "sigmaclip",
        "--dark", d / "dark.cstack", "--flat", d / "flat.cstack",
        "--bias", d / "bias.cstack", *lights)
    run(binary, d / "truth_stack.cstack", "sigmaclip", d / "truth.cstack")

    truth = read(d / "truth_stack.cstack")
    raw = read(d / "raw.cstack")
    cal = read(d / "cal.cstack")
    dark = read(d / "dark.cstack")

    def norm(a):
        return a / a.mean()

    tn, rn, cn = norm(truth), norm(raw), norm(cal)
    e_raw = float(np.abs(rn - tn).mean())
    e_cal = float(np.abs(cn - tn).mean())

    # NON-VACUITY, first: if the uncalibrated stack were already close to truth
    # the comparison would prove nothing about calibration.
    if e_raw < MIN_RAW_ERROR:
        print(f"  FAIL uncalibrated error {e_raw:.4f} is below {MIN_RAW_ERROR} — "
              f"the session carries no defects to remove, so this check is vacuous")
        fails += 1
    ratio = e_raw / e_cal if e_cal > 0 else float("inf")
    ok = ratio >= MIN_IMPROVEMENT and e_cal <= MAX_CAL_ERROR
    print(f"  vs truth: uncalibrated {e_raw:.4f}, calibrated {e_cal:.4f} "
          f"-> {ratio:.1f}x closer{'' if ok else '   FAIL'}")
    if not ok:
        fails += 1

    # Hot pixels: present in the dark by construction, and gone afterwards.
    hot = dark > 40000
    n_hot = int(hot.sum())
    left = int((cal[hot] > 40000).sum())
    before = int((raw[hot] > 40000).sum())
    if n_hot == 0:
        print("  FAIL the master dark has no hot pixels — nothing to test")
        fails += 1
    elif before == 0:
        print("  FAIL the uncalibrated stack has no hot pixels either — vacuous")
        fails += 1
    elif left != 0:
        print(f"  FAIL {left} of {n_hot} hot pixels survive calibration")
        fails += 1
    else:
        print(f"  hot pixels: {before} of {n_hot} in the raw stack, 0 after calibration")

    # Vignetting: corner response relative to centre.
    h, w = truth.shape
    cy, cx = h // 2, w // 2
    def ratio_cc(a):
        return float(a[4, 4] / a[cy, cx])
    t_r, r_r, c_r = ratio_cc(truth), ratio_cc(raw), ratio_cc(cal)
    err = abs(c_r - t_r)
    if abs(r_r - t_r) < MAX_VIGNETTE_ERR:
        print(f"  FAIL raw corner/centre {r_r:.3f} already matches truth {t_r:.3f} — vacuous")
        fails += 1
    elif err > MAX_VIGNETTE_ERR:
        print(f"  FAIL corner/centre {c_r:.3f} vs truth {t_r:.3f} (raw {r_r:.3f})")
        fails += 1
    else:
        print(f"  vignetting: corner/centre {c_r:.3f} vs truth {t_r:.3f} (raw was {r_r:.3f})")

    print("PASS" if fails == 0 else "FAIL")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
