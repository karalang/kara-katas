#!/usr/bin/env python3
"""
check_cfa.py — the CFA path's oracles.

Three independent checks, because exact equality against a numpy reference is
NOT sufficient on its own here. The reference and the implementation share an
author, so a channel transposition written into both would agree perfectly and
prove nothing. The colour check is what closes that: it compares against the
R:G:B ratios gen_cfa.py INJECTED, which are constants of the scene rather than
of either implementation.

  1. exact equality   `meancfa` against a numpy split-and-mean, per plane,
                      for all four Bayer patterns
  2. colour fidelity  each star's recovered R:G:B matches what was injected
  3. registration     recovered offsets match the injected dithers, and the
                      reference frame finds exactly the injected star count

Usage:
    python3 check_cfa.py <cumulus-binary> [--keep]
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from gen_cfa import STARS, render  # noqa: E402

PATTERNS = ["RGGB", "BGGR", "GRBG", "GBRG"]
W, H, N = 192, 128, 8

# Registration: the same bars the monochrome path is held to.
MAX_ERR = 0.25     # px, worst single frame
MAX_MEAN = 0.10    # px, mean over frames
# Colour: aperture ratios, not peak ratios — the R, G and B lattices sit half a
# mosaic pixel apart, so peaks sample the PSF at slightly different points while
# integrated flux does not care. Two bounds; see the measurement note below.
#
# The residual is NOISE-dominated and scales inversely with stellar brightness:
# measured over eight frames it runs 0.0005 on the brightest star and 0.07 on
# the faintest, with no systematic component. A crowded star is contaminated
# too — one of the brightest has a companion 10.7 px away and reads 0.012 on
# that account alone. Neither is what this check is FOR, so it asserts tightly
# on the stars where a transposition would be the only possible explanation
# (bright and isolated), and keeps a loose bound over every star to catch the
# gross case. Swapping R and B moves a coloured star's ratio by ~0.5, so even
# the loose bound has 4x of margin.
MAX_COLOUR_ERR = 0.01     # bright, isolated stars — 50x below a transposition
GROSS_COLOUR_ERR = 0.25   # every star, including faint and crowded ones
MIN_AMP = 8000.0          # "bright": above this the residual is ~0.001
MIN_SEP_PX = 15.0         # "isolated", in superpixel units


def nearest_neighbour(i):
    fx, fy = STARS[i][0], STARS[i][1]
    return min((((fx - g[0]) * W / 2) ** 2 + ((fy - g[1]) * H / 2) ** 2) ** 0.5
               for j, g in enumerate(STARS) if j != i)


def read_fits(path):
    d = path.read_bytes()
    hl = 0
    while True:
        blk = d[hl:hl + 2880].decode("ascii")
        hl += 2880
        if any(blk[i:i + 3] == "END" for i in range(0, 2880, 80)):
            break
    return (np.frombuffer(d[hl:hl + W * H * 2], dtype=">i2").astype(np.int64) + 32768).reshape(H, W)


def read_cstack(path):
    b = path.read_bytes()
    assert b[:4] == b"CSTK", "bad magic"
    w, h, n = np.frombuffer(b[4:16], dtype="<u4")
    px = np.frombuffer(b[16:16 + int(w) * int(h) * int(n) * 2], dtype="<u2").astype(np.int64)
    return int(w), int(h), int(n), px.reshape(int(n), int(h), int(w))


def run(binary, out, mode, indir):
    subs = sorted(Path(indir).glob("*.fits"))
    r = subprocess.run([binary, str(out), mode, *[str(s) for s in subs]],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"cumulus failed: {r.stdout}{r.stderr}")
    return r.stdout


def gen(outdir, pattern, dither, seed=7, truth=None):
    cmd = [sys.executable, "gen_cfa.py", str(outdir), "--frames", str(N),
           "--width", str(W), "--height", str(H), "--pattern", pattern,
           "--dither", str(dither), "--seed", str(seed)]
    if truth:
        cmd += ["--truth", str(truth)]
    subprocess.run(cmd, check=True, capture_output=True, cwd=Path(__file__).parent)


def ref_meancfa(frames, pattern):
    """Split, mean per plane, recombine — the reference for check 1.

    Mirrors the Kāra integer arithmetic exactly: the per-plane mean rounds
    half-up (`+0.5` then truncate, as integrate_mean does) and the two greens
    are combined with integer division.
    """
    planes = {}
    for p in range(4):
        x0, y0 = p % 2, p // 2
        sub = frames[:, y0::2, x0::2].astype(np.float64)
        m = np.floor(sub.mean(axis=0) + 0.5).astype(np.int64)
        planes.setdefault(pattern[p], []).append(m)
    return np.stack([planes["R"][0],
                     sum(planes["G"]) // len(planes["G"]),
                     planes["B"][0]])


def aperture_colour(rgb, sx, sy, pattern, rad=3):
    """Background-subtracted flux around a star, per channel.

    The three planes do NOT share a coordinate system, and getting this wrong
    looks exactly like a colour bug. Plane p samples the photosites at
    (2x + p%2, 2y + p//2), so R and B are half a superpixel apart on both axes
    — a star sits at a different sub-pixel phase in each plane. A single
    aperture at the same (x, y) in all three therefore captures different
    fractions of the same PSF, and the narrower the star the worse it is. On
    the first version of this check that artefact alone produced a 0.18
    "colour error" on the sharpest star, with a pattern-dependent sign, which
    is precisely what a genuine transposition would look like.
    (`sx`, `sy` are MOSAIC coordinates.)

    So: centre each plane's aperture on the star's position in THAT plane, and
    keep the aperture wide enough that the residual sub-pixel phase difference
    is negligible against the total flux.
    """
    # First lattice offset carrying each colour, in the 2x2 tile.
    origin = {}
    for p in range(4):
        origin.setdefault(pattern[p], (p % 2, p // 2))
    out = []
    ann = rad + 3
    for c, letter in enumerate("RGB"):
        x0o, y0o = origin[letter]
        cx, cy = int(round((sx - x0o) / 2.0)), int(round((sy - y0o) / 2.0))
        pl = rgb[c].astype(np.float64)
        if (cx - ann < 0 or cy - ann < 0
                or cx + ann + 1 > pl.shape[1] or cy + ann + 1 > pl.shape[0]):
            return None
        # LOCAL background, from an annulus — not the plane median. Each channel
        # carries its own sky gradient (light pollution is not grey), spanning
        # several hundred ADU corner to corner here. Subtracting a single global
        # level therefore leaves a position-dependent residual, and multiplied
        # by the ~170 pixels of an aperture that residual can exceed the star's
        # own flux in its weakest channel. Using the plane median made the blue
        # star read a 0.15 colour error with nothing wrong in the pipeline.
        outer = pl[cy - ann:cy + ann + 1, cx - ann:cx + ann + 1]
        mask = np.ones(outer.shape, dtype=bool)
        mask[ann - rad:ann + rad + 1, ann - rad:ann + rad + 1] = False
        bgv = float(np.median(outer[mask]))
        ap = pl[cy - rad:cy + rad + 1, cx - rad:cx + rad + 1]
        out.append(float((ap - bgv).sum()))
    return out


def main() -> int:
    binary = sys.argv[1] if len(sys.argv) > 1 else "./cumulus"
    fails = 0
    tmp = Path(tempfile.mkdtemp(prefix="cfa"))

    # ── 1 + 2: exact equality and colour, for every Bayer pattern ────────────
    for pattern in PATTERNS:
        d = tmp / f"in_{pattern}"
        gen(d, pattern, 0.0)
        frames = np.stack([read_fits(p) for p in sorted(d.glob("*.fits"))])

        outp = tmp / f"{pattern}.cstack"
        run(binary, outp, "meancfa", d)
        w, h, n, got = read_cstack(outp)

        want = ref_meancfa(frames, pattern)
        if (w, h, n) != (W // 2, H // 2, 3):
            print(f"  {pattern}: FAIL shape {w}x{h}x{n}, want {W//2}x{H//2}x3")
            fails += 1
            continue
        diff = int((got != want).sum())
        if diff:
            first = np.argwhere(got != want)[0]
            print(f"  {pattern}: FAIL {diff} of {got.size} differ; "
                  f"first at plane {first[0]} ({first[2]},{first[1]}) "
                  f"got {got[tuple(first)]} want {want[tuple(first)]}")
            fails += 1
        else:
            print(f"  {pattern}: meancfa EXACT MATCH over {got.size} values")

        # Colour fidelity. The expectation is the NOISELESS scene measured
        # through the same aperture, not the raw colour weights — though the
        # two agree to 0.005, which is itself the evidence that the aperture
        # method is unbiased.
        scene = np.array(render(W, H, pattern, 0.0, 0.0)).reshape(H, W)
        spl = {}
        for p in range(4):
            spl.setdefault(pattern[p], []).append(scene[p // 2::2, p % 2::2])
        truth = np.stack([spl["R"][0], sum(spl["G"]) / len(spl["G"]), spl["B"][0]])

        # Two bars, because one number cannot do both jobs. The residual is
        # NOISE-dominated and scales inversely with stellar brightness: measured
        # over eight frames it runs 0.0005 on the brightest star and 0.07 on the
        # faintest, with no systematic component. So the faint stars get a loose
        # bound that still catches a transposition by 5x (swapping R and B moves
        # a coloured star's ratio by ~0.5), and the bright ones — where noise
        # cannot hide anything — get a bound 5x tighter than the noise floor.
        rows, gross = [], 0.0
        for i, (fx, fy, amp, sig, col) in enumerate(STARS):
            g = aperture_colour(got, fx * W, fy * H, pattern)
            t = aperture_colour(truth, fx * W, fy * H, pattern)
            if g is None or t is None or sum(g) <= 0 or sum(t) <= 0:
                continue
            e = float(np.abs(np.array(g) / sum(g) - np.array(t) / sum(t)).max())
            gross = max(gross, e)
            if amp >= MIN_AMP and nearest_neighbour(i) >= MIN_SEP_PX:
                rows.append((e, f"({fx:.2f},{fy:.2f}) {col}"))
        worst = max(e for e, _ in rows)
        worst_star = max(rows)[1]
        bad = worst > MAX_COLOUR_ERR or gross > GROSS_COLOUR_ERR
        if bad:
            print(f"  {pattern}: FAIL colour error {worst:.4f} at {worst_star} "
                  f"(max {MAX_COLOUR_ERR}; worst over all stars {gross:.3f}, "
                  f"max {GROSS_COLOUR_ERR}) — channels transposed or phase off")
            fails += 1
        else:
            print(f"  {pattern}: colour within {worst:.4f} of the injected scene "
                  f"over {len(rows)} clean stars (all {len(STARS)}: {gross:.3f})")

    # ── 3: registration against the injected dithers ─────────────────────────
    d = tmp / "dith"
    truth = tmp / "truth.txt"
    gen(d, "RGGB", 3.0, truth=truth)
    out = run(binary, tmp / "dith.cstack", "stackcfa", d)

    tvals = [tuple(float(x) for x in l.split()) for l in truth.read_text().split("\n") if l.strip()]
    got_off, nref = {}, None
    for line in out.splitlines():
        f = line.split()
        if f and f[0] == "ref_stars":
            nref = int(f[1])
        if f and f[0] == "frame":
            got_off[int(f[1])] = (float(f[3]), float(f[5]))

    # The reference must find exactly the injected stars. A spurious twin — a
    # cosmic ray beside a star, which the sharpness cut cannot reject because it
    # inherits the star's neighbours — corrupts the MATCHING, not just one
    # position, and invents offsets close to a pixel. Counting is what catches
    # it; the offset tolerance alone would not.
    if nref != len(STARS):
        print(f"  FAIL reference found {nref} sources, injected {len(STARS)}")
        fails += 1
    else:
        print(f"  reference found exactly the {nref} injected stars")

    errs = []
    for f, (tdx, tdy) in enumerate(tvals):
        if f not in got_off:
            print(f"  FAIL no offset reported for frame {f}")
            fails += 1
            continue
        gdx, gdy = got_off[f]
        # Recovered offsets are the MEASURED dither (frame - reference), so they
        # match the injected values directly, in mosaic pixels.
        errs.append((abs(gdx - tdx), abs(gdy - tdy)))
    if errs:
        ex = sum(e[0] for e in errs) / len(errs)
        ey = sum(e[1] for e in errs) / len(errs)
        worst = max(max(e) for e in errs)
        ok = worst <= MAX_ERR and ex <= MAX_MEAN and ey <= MAX_MEAN
        print(f"  offsets: mean |err| ({ex:.4f}, {ey:.4f}) px, worst {worst:.4f} px"
              f"{'' if ok else '   FAIL'}")
        if not ok:
            fails += 1

    if "--keep" in sys.argv:
        print(f"  kept {tmp}")
    print("PASS" if fails == 0 else "FAIL")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
