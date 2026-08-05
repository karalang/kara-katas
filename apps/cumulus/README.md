# Cumulus — deep-sky sub-frame integration

A browser-side deep-sky stacker written in Kāra. **So far: the integration
engine, its differential oracle, FITS input, and star-based registration.** No registration, no
calibration, no browser shell yet — those are later slices, and the ordering is
deliberate (see *Why the oracle came first*).

```
python3 gen_frames.py in.cstack               # synthetic 16-frame stack
python3 gen_fits.py subs/                     # ...or the same scene as FITS
karac build cumulus.kara -o cumulus
./cumulus out.cstack sigmaclip in.cstack      # or: mean
./cumulus out.cstack sigmaclip subs/*.fits    # one sub per file
python3 oracle.py in.cstack mean.cstack clip.cstack
```

Or all of it, both backends, checked against the reference:

```
KARAC=/path/to/karac ./verify.sh
```

## What it does

Two integration modes over a stack of 16-bit mono frames:

| mode | what it computes |
|---|---|
| `mean` | arithmetic mean across all frames |
| `sigmaclip` | iterative 3σ clipping (max 5 passes), then the mean of the survivors |

The synthetic frames carry a sky gradient, three Gaussian stars, per-frame read
noise, and **cosmic-ray hits in different places on each frame**. The rays are
the point: a plain mean smears them across the result, sigma clipping removes
them. Without them the two modes agree everywhere and the oracle would happily
pass a clip that did nothing — which is why `oracle.py` fails if clipping
changed no pixels.

## Why the oracle came first

Every other artifact in this corpus asserts hand-written expected values, so a
wrong expectation and a wrong implementation agree with each other. Numerical
image processing has an escape from that: an independent implementation in
another language on another runtime. `oracle.py` reimplements both modes in
numpy and compares pixel for pixel.

The bar is **exact equality, not a tolerance**, and that is a property of the
design rather than optimism:

- inputs are u16 and accumulators are f64, so partial sums stay well under
  2<sup>53</sup> and are exact — no representation error to absorb;
- the single division and single `sqrt` per pass are correctly rounded by
  IEEE 754, so both sides land on the same double;
- the output rounding is `floor(x + 0.5)` on both sides.

A tolerance would hide precisely the class of bug this harness exists to find.

`verify.sh` also runs the same program under the interpreter and requires the
output to be **byte-identical** to the AOT build, so a run-vs-build divergence
fails the harness rather than waiting to surprise someone.

## Parallelism: there isn't any, on purpose

There is no `TaskGroup`, no `spawn`, and no `par {}` anywhere in
`cumulus.kara`. Every kernel is an ordinary sequential `for` loop, and the
compiler fans them across the worker pool by itself:

```
$ karac build cumulus.kara --concurrency-report
  parallel_reduction { op: +, accumulator: sum, line: 74 }
  disjoint_writes { loop_var: p, targets: out[1 per iteration], line: 72 }
  disjoint_writes { loop_var: p, targets: out[1 per iteration], line: 92 }
```

This follows Prism, which deleted its hand-rolled band fan-out and got **23%
faster** with byte-identical output — the compiler writes straight into the
output buffer where the manual version paid a per-band allocation and a concat
copy.

One consequence shapes the clipping kernel: it tracks the surviving **interval**
`[lo, hi]` rather than a per-pixel keep-mask. For a symmetric threshold the kept
set is always an interval, so the two formulations are equivalent — but the
interval form allocates nothing inside the pixel loop, which is what keeps the
loop body disjoint and lets it parallelize.

## Registration

Translation-only, sub-pixel, star-based. Three stages, each independently
checkable: detect 3×3 local maxima above a background-derived threshold →
centroid them (intensity-weighted, background-subtracted) → recover the
translation by a consensus vote over candidate offsets, refined on the pairs
that agree.

```
$ ./cumulus out.cstack register subs.cstack
ref_stars 11
frame 1 dx -1.4584 dy 1.1022 votes 11 stars 11
```

**Checked against ground truth, not against a reimplementation.** The generator
injects known per-frame dithers and `check_register.py` compares what was
recovered against what was injected. That distinction earned itself twice in one
sitting — a differential would have missed both:

- **Cosmic rays raised the detection threshold above the stars.** A raw mean/sd
  background is wrecked by the very things detection is meant to find: twelve
  rays at 60000 in a field whose sky sits near 1500 pushed `mean + 6σ` above
  most real stars. The reference frame found 8 of 12 sources, the others 11 —
  the difference being rays, not stars. Fixed with a sigma-clipped background
  and a **sharpness cut**: a Gaussian star puts ~2.8× its peak into the four
  neighbours, a single-pixel ray puts ~zero.
- **The recovered sign was inverted.** Magnitudes matched to 0.03 px, so the
  numbers looked right; only comparison with the injected truth showed they
  were negated. `register` now reports the *measured dither* (frame −
  reference), so a sign error fails the check rather than waiting to surface as
  a mysteriously blurry stack.

This check uses a **tolerance**, unlike the integration oracle, and that is
correct rather than a concession — centroiding a noisy PSF is a measurement, so
the question is whether the error is small enough to stack with. Gates: 0.25 px
worst case per axis, 0.10 px mean. Currently **0.025 / 0.035 px mean, 0.224 px
worst** over 16 frames. It also fails if the consensus rests on fewer than 60%
of the reference stars, since a two-star agreement is luck rather than a match.

## FITS input

`cumulus` reads the subset a smart telescope actually emits: `BITPIX = 16`,
`NAXIS = 2`, with `BZERO` / `BSCALE`, big-endian, 2880-byte blocks.

**BZERO is the trap.** Unsigned 16-bit data rides in FITS's *signed* 16-bit
format with `BZERO = 32768`, so a reader that ignores it turns every value above
32767 into a large negative number — stars come out as holes. `verify.sh` pins
this by generating the same scene twice, once as `.cstack` and once as FITS, and
requiring both to integrate to a byte-identical image.

Anything outside the supported subset is **refused by name** rather than
misread, because a reader that quietly mishandles `BITPIX` produces a plausible
image, which is worse than no image:

```
cumulus: sub.fits: unsupported BITPIX (only 16 is implemented)
cumulus: sub.fits: unsupported NAXIS (only 2-D mono is implemented)
cumulus: sub.fits: no END card in header
```

`gen_fits.py` writes its headers by hand rather than via astropy — the reader
has to be checked against the spec, not against whatever a library happens to
emit, and hand-writing keeps every byte the reader must handle visible: card
padding, the `END` card, block padding, the `BZERO` round trip.

## The `.cstack` container

A deliberately boring container, so the first slice could be about numerics
rather than format parsing. It remains the output format and a convenient way to
carry a whole stack in one file. Little-endian throughout:

```
magic   4 bytes  "CSTK"
width   u32
height  u32
frames  u32
pixels  frames * height * width * u16   (frame-major, then row-major)
```

FITS is read directly (see above); this container is not required for input.

## Scope and what is missing

Deliberately absent, in the order they matter:

1. **Resampling** — `register` reports offsets but integration does not yet
   apply them, so a dithered stack still integrates unshifted. Sub-pixel
   resampling and registration-aware stacking are the next slice.
2. **Rotation** — translation only. Fine for a tracked mount over a short
   session; an alt-az mount accumulates field rotation that this will not
   correct.
3. **Tiled / streaming integration.** The whole stack is decoded up front, which
   is fine at 96×64 and impossible at 12 MP. Measured: 16 frames of 12 MP held
   resident is ~368 MB peak RSS, against ~11 MB for a 512×512 tiled pass — and
   the decoded-frame store, not the working set, is what sets the ceiling under
   the browser's 1 GiB default. Frames stay 16-bit mono with debayering late for
   that reason.
4. **Calibration** (darks / flats / bias) and the browser shell.
5. **Wider FITS** — float and 8-bit `BITPIX`, 3-D colour cubes, compressed
   HDUs. Vendor RAW stays out of scope.
