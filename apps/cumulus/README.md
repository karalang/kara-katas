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
  stack ran off the main thread (worker)
  page stack byte-identical to native over 6144 pixels
  canvas painted, luminance range 0..255
  status line: Done in 97 ms · all 16 frames registered
  Worker denied -> inline fallback ran, still byte-identical to native
  iPhone 13 390x664: no overflow, canvas 308px, stacked and painted
  Pixel 5 393x727: no overflow, canvas 311px, stacked and painted
```

The one thing the page reimplements is the **FITS header parse**, in JS, because
the wasm entry point takes decoded pixels rather than files. That is a real
duplication of the `BZERO` trap, so the browser check pins the two decoders to
each other: same files, same stack, or the run fails.

## Will it run on a phone?

Yes — and the interesting part is that the answer has nothing to do with
WebAssembly support.

**Compatibility is a non-issue, and that is checkable from the module rather
than assumed.** `cumulus.wasm` declares a single memory with `shared = false`,
imports nothing but the three `kara_host` functions and the WASI shims
`cumulus.js` polyfills, and uses no atomics. So there is **no
`SharedArrayBuffer`, and therefore no COOP/COEP headers and no cross-origin
isolation** — it serves from any static host and instantiates in any browser
that runs wasm at all. The sequential scheduler that `--target=wasm_browser`
links is what buys that; the threaded archive would have cost the whole setup.

`verify_browser.mjs` runs the page at iPhone 13 and Pixel 5 viewports: zero
horizontal overflow, a canvas that fits the screen, a file-picker target big
enough to tap, and a stack that completes and paints. Emulation exercises
layout, touch and the DOM — **not** WebKit's engine and not a device's memory
ceiling — so it can show the page is broken on mobile and never that it is good.
What it does cover is the failure class that is invisible at desktop width.

### The ceiling is memory

Worth measuring rather than guessing. `mem_probe.mjs` instantiates the module
outside the browser and reports peak `memory.buffer.byteLength`; the wasm heap
is the same size whatever engine hosts it, so the figure is exact without a
device.

| frame | frames in | peak wasm, before | after |
|---|---|---|---|
| 512×512 ×16 | 8 MB | 27.6 MB | **19.6 MB** |
| 1024×768 ×16 | 24 MB | 63.6 MB | **39.6 MB** |
| 2048×1536 ×16 | 96 MB | 225.6 MB | **129.6 MB** |

Before, peak fit `w·h·(4n+8)` bytes to within 4% at every size. The `4n` should
have been `2n`: `stack_frames` allocated a `Vec[u8]` for the raw blob and
decoded it into a separate `Vec[u16]`, both alive to the end of the function.
Half the peak was a copy of the input held in the format we had just finished
converting away from.

The fix is not to free the first buffer sooner. **wasm32 is little-endian by
spec and the blob is already little-endian u16, so the bytes JS holds _are_ the
pixel array** — `read_frames` now takes `*const u16` and the host copy lands
directly in its final home. That deletes the second allocation and the
`w·h·nframes`-iteration decode loop along with it. Peak is now `w·h·(2n+8)`;
extrapolated to the 11.7 Mpx ×16 stack the CLI benchmark uses, ~850 MB becomes
~470 MB.

Declaring the parameter `*const u16` rather than `*const u8` is what keeps this
*safe* code: the `u8` form needs `px.as_ptr() as *const u8`, and Kāra requires
`unsafe` for a cast that reinterprets the pointee. The pointer value is
identical either way, so the honest declaration is also the one that compiles
without an escape hatch.

Wall time barely moved — 40.1 s against 41.8 s at 3 Mpx. The decode loop was
never the bottleneck (registration and integration are), so this is a memory win
that happens to remove a loop, not the speed-up it looks like.

### The freeze

The second phone-hostile property had nothing to do with size. `stack_frames` is
**one synchronous wasm call** that runs for the whole stack — tens of seconds at
real frame sizes. On the page's own thread it blocks every repaint for its full
duration, so the progress ticks it emits updated the DOM but never reached the
screen, and a mobile browser eventually offers to kill the "unresponsive" page.
The progress bar was, on a phone, decorative.

It runs in a worker now (`stack_worker.mjs`), created fresh per run and
terminated when it ends, so the entire wasm heap goes back after every stack
instead of staying at the high-water mark between runs. The inline path survives
as a fallback for a page opened over `file://`, where a module worker cannot
load.

Both halves are checked, because neither was self-evident:

```
  stack ran off the main thread (worker)
  page stack byte-identical to native over 6144 pixels
  Worker denied -> inline fallback ran, still byte-identical to native
```

The first line matters because **the fallback produces identical pixels**, so
every other assertion in `verify_browser.mjs` passes whether or not the worker
ran — a regression that permanently broke it would have shipped green. The last
line matters for the mirror-image reason: the fallback is code the harness never
otherwise reaches, which is exactly the shape of a path that rots quietly and
then fails the one time it is needed. Denying the page a `Worker` constructor
reproduces the failure it exists for, and holds it to the same byte-identity
bar — degraded should mean slower, not different.

One thing here is **not** verified: `index.html` sets `accept=".fits,.fit"`, and
iOS resolves `accept` extensions through UTIs. FITS has no registered UTI, so
the Files picker may grey out exactly the files the user is trying to choose.
Chromium emulation does not reproduce that; it needs a real device.

## Colour: the CFA path

This is what "supports RAW" actually means for the astronomy. Siril, and every
other stacker, runs LibRaw over CR3/NEF/ARW and writes a **FITS sequence**
before doing anything else; what lands is a 16-bit plane per sub with a
`BAYERPAT` card describing the colour filter array. Cumulus reads that directly,
which is the whole of RAW support minus the vendor-format archaeology — a
decoder is a TIFF-variant parser plus per-vendor decompression that changes with
firmware, and it exercises byte-fiddling the FITS reader already covers.

```
cumulus out.cstack stackcfa sub_*.fits    # register + sigma clip, in colour
cumulus out.cstack meancfa  sub_*.fits    # no registration — the exact-oracle mode
```

### Split first, demosaic never

The mosaic is separated into **four half-resolution planes**, one per position
in the 2×2 tile, and every existing kernel then applies unchanged —
`detect_stars`, `estimate_offset`, `resample_tile` and `stack_tiled` all run on
each plane as if it were an ordinary monochrome image. That is the point of the
ordering. Interpolating to full-resolution RGB first would blend neighbouring
filters into every sample **before** alignment is known, baking an interpolation
error into the very data the registration then measures.

The cost is resolution: this is superpixel demosaic, so the output is w/2 × h/2.
Recovering full resolution from the dithers is drizzle, and it is a later slice,
not a different architecture.

Registration runs on a half-resolution **luminance** image, never on the mosaic.
Centroiding a star directly on a mosaic is biased: adjacent photosites sit under
different filters, so the sampled PSF carries a checkerboard modulation and the
measured centre is pulled toward whichever channel the star is brightest in.
That is a colour-dependent astrometric error — red and blue stars in the same
frame disagree about where the frame is, the consensus vote splits, and the
result is a slightly soft stack with nothing in the output to say why.

### What the CFA path found in the monochrome one

The luminance combiner is the **median** of the four photosites rather than the
mean, and the detector now drops any source within 2 px of a brighter one. Both
came out of a measurement, not a design review, and the second is a genuine bug
that had been sitting in the monochrome path all along.

On a **zero-dither** set — every frame the same scene, so the true offset is
exactly zero and any recovered offset is pure error — the CFA path read
**0.078 px**. Removing the cosmic rays from the generator dropped it to 0.005.
So the rays were the cause, but the sharpness cut that rejects them in the
monochrome path was clearly not doing its job.

The reference frame turned out to be finding **13 sources for 12 stars**:

```
ref(23.77, 22.21) flux 48418
ref(23.63, 23.11) flux 31855      <- same star, 0.9 px away
```

A cosmic ray landing *beside* a star creates a second local maximum that the
sharpness cut cannot reject, because the ray **inherits the star's neighbours**
and so looks perfectly resolved. The monochrome path escapes this by luck rather
than design: at 60000 ADU a ray swallows the star's own peak, the pair collapses
into one detection, and the cut throws it away. Combining four photosites scales
a ray down to roughly stellar brightness, the star keeps its maximum, and both
survive.

The damage is out of proportion to the artefact, because a spurious twin
corrupts the **matching** rather than one star's position — the offset search
pairs a real star in one frame against the twin in another and proposes a
displacement wrong by their separation. Deduplication took the zero-dither error
from 0.078 px back to the 0.005 the ray-free set already achieved, and costs the
monochrome path nothing: its gate reads exactly what it read before,
`mean |err| (0.0214, 0.0206)`, worst `0.0707`.

**One thing measured and then deliberately NOT fixed.** A second, smaller effect
survives: a bright star's centroid is bistable, reading 52.32 or 52.74 depending
on which pixel wins the local maximum. The ±3 centroid window cuts a σ=2.2 star
at 1.4σ and discards about a third of its flux, and the truncation flips sides
when the peak pixel moves. Widening the window to ±5 and letting it re-centre
fixed the CFA case — and **regressed the monochrome path below its gate**
(mean |err| 0.021 → 0.050, one frame falling to 6 votes of 11) because an 11×11
window blends neighbouring stars at this field density. So it was reverted. The
honest fix is an adaptive window sized to the measured PSF, with deblending,
which is its own piece of work and not something to smuggle into a colour slice.

### Three oracles, because exact equality is not enough here

Exact equality against a numpy reference cannot catch a channel transposition:
the reference and the implementation share an author, so the same mistake
written into both agrees perfectly. `check_cfa.py` adds two checks that do not
depend on the implementation at all.

```
  RGGB: meancfa EXACT MATCH over 18432 values
  RGGB: colour within 0.0012 of the injected scene over 3 clean stars (all 12: 0.070)
  reference found exactly the 12 injected stars
  offsets: mean |err| (0.0600, 0.0193) px, worst 0.1063 px
```

- **Exact equality**, for all four Bayer patterns, on `meancfa`. Registration is
  off in that mode for a reason: with it on the recovered offsets are near zero
  but not zero, the resample stops being an identity sample, and only a
  tolerance comparison would be possible — which is exactly where a real defect
  in new code hides.
- **Colour**, against the R:G:B ratios `gen_cfa.py` injected. Those are
  constants of the scene, not of either implementation.
- **Star count**, which is what catches the spurious-twin class. The offset
  tolerance alone does not: a phantom pair still lands inside it more often than
  not.

Getting the colour check right took three wrong turns, all of them mine and all
worth recording, because each produced a confident failure that looked exactly
like a pipeline bug:

1. A single aperture at the same coordinates in all three planes. But the planes
   do not share a coordinate system — R and B sample lattices half a superpixel
   apart — so a fixed aperture captures different fractions of the same PSF,
   worst on the sharpest star. That artefact alone read as a 0.18 colour error
   with a pattern-dependent sign.
2. A **global** median background. Each channel carries its own sky gradient,
   several hundred ADU corner to corner, so one global level leaves a
   position-dependent residual which, over ~170 aperture pixels, exceeded the
   faintest star's flux in its weakest channel.
3. A tolerance tighter than the noise. Measuring the *noiseless injected scene*
   through the same aperture settled it: the scene reproduces the injected
   ratios to 0.005, and the pipeline reproduces the scene to 0.0012 on bright
   stars and 0.07 on faint ones — error scaling inversely with brightness, i.e.
   noise, with no systematic term. The check now asserts tightly where a
   transposition would be the only possible explanation (bright, isolated) and
   loosely everywhere else.

The check is **proven non-vacuous**: transposing R and B in `stack_cfa` fails it
on every pattern, at 12288 of 18432 values and a colour error of 0.523 against a
0.25 bound.

### Refusing the mistake that produces a picture

A mosaic stacked as monochrome does not fail. It produces a plausible grey image
with checkerboard texture and colour-biased star positions — no error, no
warning, just a slightly wrong answer. So the mismatch is refused in both
directions, and both refusals are asserted in `verify.sh`:

```
  mosaic into `stack`: refused — input is a Bayer mosaic (BAYERPAT=RGGB) — use `stackcfa`
  mono into `stackcfa`: refused — `stackcfa` needs a BAYERPAT card; this input is monochrome
```

`ROWORDER` is refused the same way when it is not `TOP-DOWN`. That card exists
because FITS inherited bottom-up row order from its tape era while cameras write
top-down, and reading a mosaic at the wrong anchor is a colour **transposition**,
not a flip — every red pixel comes out green.

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
   themselves (`frames × pixels × 2`) — 374 MB at 11.7 Mpx × 16, which is ~80%
   of the browser tab's whole ~470 MB peak. Fine on a desktop; still the thing
   that decides whether a phone survives a full-size stack. Holding only a
   window of frames resident, or memory-mapping the subs, is the next lever, and
   it is now the *only* remaining one — everything above the frames themselves
   has been squeezed out.
3. **Calibration** — darks, flats and bias. Synthetic frames have no amp glow,
   no hot columns, no vignetting and no dust motes, so nothing here has ever
   needed it; real subs from a real sensor do. This is the next thing that
   matters for actual RAW-derived data, now that the mosaic is handled.
4. **Drizzle.** The CFA path is superpixel demosaic, so colour output is half
   resolution. The dithers carry the information needed to recover full
   resolution, and using it is the natural follow-on — the plane-separated
   architecture is already the right shape for it.
5. **Deblending, and an adaptive centroid window.** The fixed ±3 window
   truncates bright stars asymmetrically and makes their centroids bistable by
   ~0.4 px; widening it naively blends close pairs instead. Both want the same
   fix, and it needs its own slice — see the CFA section for the measurement.
6. **Better interpolation** — bilinear softens slightly; Lanczos-3, which Prism
   already implements, is the upgrade once the pipeline is trusted.
7. **Wider FITS** — float and 8-bit `BITPIX`, 3-D colour cubes, compressed
   HDUs, and `ROWORDER = 'BOTTOM-UP'`. Vendor RAW decoding stays out of scope:
   `rawpy`, `dcraw` or `siril -s` convert to FITS in a few lines, which is
   exactly what Siril itself does internally before any astronomy happens.
