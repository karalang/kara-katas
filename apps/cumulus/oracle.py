#!/usr/bin/env python3
"""
oracle.py — differential oracle for Cumulus integration.

Reimplements the two integration modes in numpy and compares, pixel for pixel,
against what `cumulus.kara` produced. This is the reason step 1 exists: every
other artifact we dogfood asserts hand-written expected values, so a wrong
expectation and a wrong implementation agree. Here the reference is an
independent implementation in a different language on a different runtime.

EXACT EQUALITY IS THE BAR, not a tolerance, and that is a deliberate design
property rather than optimism:

  * inputs are u16 and the accumulator is f64, so every partial sum stays
    exact — well under 2^53, no representation error to absorb;
  * the one division and the one sqrt per pass are each correctly rounded by
    IEEE 754, so both sides land on the same double;
  * rounding to the output integer is floor(x + 0.5) on both sides.

So any difference is a real defect — in the kernel, in the compiler, or in the
algorithm spec drifting between the two implementations. A tolerance here would
hide exactly the class of bug this harness exists to find.

The clipping parameters below MUST match the constants in cumulus.kara.

Usage:
    python3 oracle.py in.cstack mean_out.cstack sigmaclip_out.cstack
"""

import struct
import sys

import numpy as np

SIGMA = 3.0
MAXITERS = 5
MAGIC = b"CSTK"


def read_stack(path: str) -> tuple[int, int, int, np.ndarray]:
    with open(path, "rb") as fh:
        blob = fh.read()
    if blob[:4] != MAGIC:
        raise SystemExit(f"{path}: not a .cstack (bad magic {blob[:4]!r})")
    w, h, n = struct.unpack("<III", blob[4:16])
    want = 16 + w * h * n * 2
    if len(blob) != want:
        raise SystemExit(f"{path}: expected {want} bytes for {w}x{h}x{n}, got {len(blob)}")
    px = np.frombuffer(blob, dtype="<u2", count=w * h * n, offset=16)
    return w, h, n, px.reshape(n, h * w).astype(np.float64)


def ref_mean(stack: np.ndarray) -> np.ndarray:
    return np.floor(stack.mean(axis=0) + 0.5).astype(np.int64)


def ref_sigma_clip(stack: np.ndarray) -> np.ndarray:
    """Interval-form iterative clipping — the same formulation as the kernel.

    Tracks the surviving interval rather than a per-pixel mask, and converges on
    the surviving COUNT, exactly as cumulus.kara does. Written as an explicit
    per-pixel loop rather than a vectorised one on purpose: the point is to
    mirror the kernel's control flow so a divergence is attributable to the
    kernel, not to a clever numpy rewrite that clips in a subtly different order.
    """
    nframes, npix = stack.shape
    out = np.zeros(npix, dtype=np.int64)
    for p in range(npix):
        col = stack[:, p]
        lo, hi = -1.0e30, 1.0e30
        prev_count = nframes + 1
        mean = 0.0
        it = 0
        while it < MAXITERS:
            sel = col[(col >= lo) & (col <= hi)]
            count = sel.size
            if count == 0:
                break
            mean = float(sel.sum() / count)
            if count == prev_count:
                break
            d = sel - mean
            sd = float(np.sqrt(float((d * d).sum()) / count))
            prev_count = count
            lo, hi = mean - SIGMA * sd, mean + SIGMA * sd
            it += 1
        out[p] = int(np.floor(mean + 0.5))
    return out


def compare(label: str, got: np.ndarray, want: np.ndarray) -> bool:
    if got.shape != want.shape:
        print(f"  {label:<10} SHAPE MISMATCH got {got.shape} want {want.shape}")
        return False
    diff = got.astype(np.int64) - want.astype(np.int64)
    bad = int(np.count_nonzero(diff))
    if bad == 0:
        print(f"  {label:<10} EXACT MATCH over {got.size} pixels")
        return True
    idx = int(np.argmax(np.abs(diff)))
    print(f"  {label:<10} {bad}/{got.size} pixels differ, max |diff| {int(np.abs(diff).max())}")
    print(f"             first at pixel {idx}: kara {int(got[idx])} vs ref {int(want[idx])}")
    return False


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: oracle.py in.cstack mean_out.cstack sigmaclip_out.cstack")
        return 2
    inp, mean_path, clip_path = sys.argv[1:4]

    w, h, n, stack = read_stack(inp)
    print(f"input {w}x{h} x{n} frames")

    _, _, _, got_mean = read_stack(mean_path)
    _, _, _, got_clip = read_stack(clip_path)
    got_mean = got_mean[0].astype(np.int64)
    got_clip = got_clip[0].astype(np.int64)

    want_mean = ref_mean(stack)
    want_clip = ref_sigma_clip(stack)

    ok = compare("mean", got_mean, want_mean)
    ok = compare("sigmaclip", got_clip, want_clip) and ok

    # Non-vacuity: if the two modes agree everywhere, the cosmic rays did not
    # land or the clip did nothing, and the comparison above proves far less
    # than it appears to. This is the check that keeps a no-op clip from
    # reading as a pass.
    rejected = int(np.count_nonzero(want_mean != want_clip))
    print(f"  {'rejection':<10} {rejected} pixel(s) where clipping changed the result")
    if rejected == 0:
        print("  FAIL: clipping changed nothing — the oracle would pass a no-op kernel")
        ok = False

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
