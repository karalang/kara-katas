# Cumulus — deep-sky sub-frame integration

A browser-side deep-sky stacker written in Kāra. **So far: the integration
engine, its differential oracle, FITS input, star-based registration, and
sub-pixel resampling, and a browser shell.** No calibration and no rotation
yet — those are later slices, and the ordering is deliberate (see *Why the
oracle came first*).

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
| `sigmaclip` | iterative 3σ clipping about the **median**, scaled by the **MAD** (max 5 passes), then the mean of the survivors |

The synthetic frames carry a sky gradient, three Gaussian stars, per-frame read
noise, and **cosmic-ray hits in different places on each frame**. The rays are
the point: a plain mean smears them across the result, sigma clipping removes
them. Without them the two modes agree everywhere and the oracle would happily
pass a clip that did nothing — which is why `oracle.py` fails if clipping
changed no pixels.

### Why the median and the MAD, not the mean and the sd

The first implementation clipped about the mean using the standard deviation,
and it failed on the case that matters. At a pixel where two cosmic rays landed
after resampling:

```
1675 1750 ... 1813  30590  34796        <- 14 sky values and 2 rays
mean 5644, sd 10000  ->  bounds ±30000  ->  keeps all 16
```

The outliers inflate the very scale meant to exclude them, so the interval
widens to swallow them and the pixel stacks at 5641 instead of ~1780. Two
visible artifacts survived into the browser demo this way.

The MAD does not inflate — it stays near 25 there, giving bounds of about ±111,
and both rays go on the first pass. This is why astropy centres on the median by
default. Rejection is robust; the **estimate is still the mean of the
survivors**, which is what preserves the signal-to-noise that stacking buys.

Two rays colliding is not an exotic case but the expected one: each frame is
resampled by a *different* dither, so rays land on the same **output** pixel even
when no two share an **input** pixel. At ~192 ray hits over 6144 pixels, a
handful of collisions is arithmetic.

Measured, before → after, on the same registered stack:

| | mean/sd | median/MAD |
|---|---|---|
| isolated ray residue | 2 pixels | **0** |
| background noise | 84.00 | 82.91 (**0.987×**) |
| brightest star flux | 511349 | 511320 (0.9999×) |

The tighter scale rejects more — 2591 pixels changed rather than 236 — and it
costs nothing measurable: noise is fractionally *lower* and stellar flux is
preserved to four decimal places. It is removing outliers, not signal.

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

Measured here on 4 cores, `KARAC_NO_AUTOPAR=1` against the default build:

| frame size | sequential | auto-par | speedup |
|---|---|---|---|
| 1024×768 | 5.22 s | 1.80 s | **2.90×** |
| 2048×1536 | 20.53 s | 7.43 s | **2.76×** |

~70% parallel efficiency from loops nobody annotated, and the two builds produce
**byte-identical** output — which is the check that matters, since a race would
show up here first.

Two consequences shape the clipping kernel, both about keeping the loop body
allocation-free so it stays disjoint and parallelizable:

- It tracks the surviving **interval** `[lo, hi]` rather than a per-pixel
  keep-mask. For a symmetric threshold the kept set is always an interval, so
  the formulations are equivalent — but the interval form allocates nothing.
- The median and MAD use **counting selection, not a sort**. A sort needs a
  scratch buffer; one allocated per pixel is ruinous at 12 MP, and one reused
  across pixels is a genuine race that would (correctly) make the compiler
  decline to parallelize. Counting reads the strided source directly and writes
  nothing. It is O(n²) in the frame count, which for the 16–100 subs a real
  session produces is far cheaper than losing the parallelism.

## Memory: u16 storage and tiled integration

The first version decoded pixels to `i64` and, during registration, built a
second full-size aligned copy of the whole stack. That is `frames × pixels ×
8 × 2` — and this README claimed ~368 MB for a 12 MP stack, an estimate that
assumed the pixels stayed `u16` and was **8× wrong**. Measured: **2947 MB**.

Two changes fix it:

- **Frames are stored `u16`**, as they arrive. The integration helpers still use
  `i64` because they carry the `-1` NO-DATA sentinel, but they now operate on a
  single tile rather than the stack.
- **Integration is tiled.** Rather than aligning every frame into a stack-sized
  buffer and then integrating, each 256×256 output tile is gathered from every
  frame and integrated on its own. The working set is `frames × TILE² × 8` —
  8 MB at 16 frames, *independent of frame size*.

Measured on 11.7 Mpx × 16 frames (a Seestar-class stack), full `stack` pipeline:

| | before | after |
|---|---|---|
| peak RSS | 2947 MB | **716 MB** (4.1× less) |
| wall time | 43.5 s | **~28 s** |

Faster as well as smaller, which was not the goal but follows from touching far
less memory — the tiled version fits its working set in cache where the old one
streamed two 1.5 GB buffers. `mean` alone went 10.3 s → 4.3 s.

Tiling also **fixed a latent bug**. The bilinear guard required the `+1`
neighbour to exist unconditionally, so the last row and column were dropped even
at a zero offset — 5953 border pixels of a 12 MP frame, silently NO-DATA. The
`+1` neighbour is only *read* when the fractional part is nonzero, so the guard
now tests the neighbour it will actually use. The oracle caught this the moment
unregistered modes started sharing the resample path.

## The browser shell

`index.html` is the app: drop FITS subs in, pick an integration mode, get a
stacked image. Nothing is uploaded — the pixels never leave the tab.

```
KARAC=/path/to/karac ./build_web.sh          # build + verify
python3 -m http.server                       # then open localhost:8000
```

**One Kāra source, two targets.** `main` is `#[target(native)]`, `stack_frames`
is `#[target(wasm_browser)]`, and both call the *same* kernels. The page is not a
port of the pipeline; it is the pipeline. `test_node.mjs` holds it to that
claim by requiring the WebAssembly result to be **byte-identical to the native
binary's** — the same bar the interpreter and numpy already meet:

```
  mean   byte-identical to native over 6144 pixels
  stack  byte-identical to native over 6144 pixels
```

`verify_browser.mjs` goes further and drives the real page in headless Chromium,
because "the kernels are right" and "the page works" are different claims. It
feeds the demo subs through the same path the file picker uses, compares the
page's pixels against the CLI's, and separately asserts the canvas was actually
painted — a blank canvas would otherwise pass a pixel check that reads the data
rather than the display.

```
  page stack byte-identical to native over 6144 pixels
  canvas painted, luminance range 0..255
  status line: Done in 27 ms · all 16 frames registered
```

The one thing the page reimplements is the **FITS header parse**, in JS, because
the wasm entry point takes decoded pixels rather than files. That is a real
duplication of the `BZERO` trap, so the browser check pins the two decoders to
each other: same files, same stack, or the run fails.

## Registration

Translation-only, sub-pixel, star-based. **O(N²)** in the detected star count —
see the complexity note below; the obvious formulation is O(N⁴) and was
unusable on real frames. Three stages, each independently
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

### The O(N⁴) trap

Every (star in a, star in b) pair proposes an offset, and the proposal with the
most support wins. The obvious way to count that support — for each candidate,
re-scan every other pair — is **O(N⁴)**, and that is what this was first. It is
invisible on a toy frame and ruinous on a real one:

| stars | frame | registration |
|---|---|---|
| 11 | 96×64 | instant |
| 324 | 512×384 | **146.29 s** |

146.29 s of a 146.29 s run, while the entire integration took 0.38 s. Binning
candidates into a vote grid and taking the heaviest bin gets the same answer in
two linear passes over the N² candidates: **146.29 s → 0.10 s**, a 1400×
improvement, and accuracy *improved* (worst error 0.224 px → 0.071 px) because
refining around the bin centre beats refining around an arbitrary pair's offset.

The grid is what forces a **search radius** (`MAX_SHIFT`, 128 px): a full-frame
grid would be 20 million bins at 12 MP. Ordinary practice for registration, but
a real limit — a frame displaced further is reported as no consensus rather than
mismatched.

This check uses a **tolerance**, unlike the integration oracle, and that is
correct rather than a concession — centroiding a noisy PSF is a measurement, so
the question is whether the error is small enough to stack with. Gates: 0.25 px
worst case per axis, 0.10 px mean. Currently **0.025 / 0.035 px mean, 0.224 px
worst** over 16 frames. It also fails if the consensus rests on fewer than 60%
of the reference stars, since a two-star agreement is luck rather than a match.

## Resampling and the full pipeline

`stack` runs the lot: register every frame against the reference, resample it
onto the reference grid with bilinear interpolation, then integrate with sigma
clipping.

Two decisions worth naming:

**Uncovered pixels are NO DATA, not clamped.** After a dithered frame is
shifted, part of its border has no source pixel. Clamping to the edge is the
tempting one-liner and it is wrong here — it smears the border pixel across the
uncovered strip, producing a bright rim that looks like real signal.
Integration counts per-pixel coverage instead, so the divisor at the edges is
the number of frames that actually reached them.

**A frame that cannot be registered is dropped, not guessed.** If the consensus
rests on under 60% of the reference stars, the frame is discarded. One
misaligned frame smears every star in the result; a dropped frame only costs its
share of the signal-to-noise.

### Does registration actually help?

`check_stack.py` measures it rather than assuming it. Against the same dithered
stack integrated without registration:

```
  mean peak   reg    9689.6  unreg    5470.4  gain 1.771x
  concentration reg  0.0485  unreg  0.0334  gain 1.450x
```

This check exists because the offsets being *correct* and the offsets being
*applied correctly* are different claims. A pipeline that measures a right
offset and resamples by its negation passes every other check in this repo.
Verified by doing exactly that: negating the resample scores **0.749×** peak
brightness — worse than not registering — and the check fails.

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

1. **Rotation** — translation only. Fine for a tracked mount over a short
   session; an alt-az mount accumulates field rotation that this will not
   correct.
2. **Streaming from disk.** Memory is now bounded by the decoded frames
   themselves (`frames × pixels × 2`), which is 374 MB at 11.7 Mpx × 16 — fine
   on a desktop, still heavy for a browser tab on a long session. Holding only a
   window of frames resident, or memory-mapping the subs, is the next lever.
3. **Calibration** (darks / flats / bias) and the browser shell.
4. **Better interpolation** — bilinear softens slightly; Lanczos-3, which Prism
   already implements, is the upgrade once the pipeline is trusted.
5. **Wider FITS** — float and 8-bit `BITPIX`, 3-D colour cubes, compressed
   HDUs. Vendor RAW stays out of scope.
