# Cumulus — sub-frame integration for deep-sky and nightscape stacking

A browser-side astrophotography stacker written in Kāra. **So far: the
integration engine and its differential oracle; FITS input from a telescope and
TIFF input from a camera, mono or RGB; star-based registration with rotation;
sub-pixel resampling; a sky/foreground mask for tripod nightscapes; colour, both
via the Bayer mosaic a converted RAW becomes and via RGB TIFF; calibration with
darks, flats and bias; and streaming — on the CLI *and* in the page — so peak
memory stops scaling with the size of the session.** No drizzle yet; that is a
later slice, and the ordering is deliberate (see *Why the oracle came first*).

```
python3 gen_frames.py in.cstack               # synthetic 16-frame stack
python3 gen_fits.py subs/                     # ...or the same scene as FITS
python3 gen_tiff.py tsubs/                    # ...or as RGB TIFF, as a camera writes
karac build cumulus.kara -o cumulus
./cumulus out.cstack sigmaclip in.cstack      # or: mean
./cumulus out.cstack stack subs/*.fits        # one sub per file: register + clip
./cumulus out.cstack stack tsubs/*.tif        # TIFF, mono or RGB, sniffed not guessed
./cumulus out.cstack stack --horizon 1400 --feather 40 tsubs/*.tif   # nightscape
python3 oracle.py in.cstack mean.cstack clip.cstack
```

Or all of it, both backends, checked against the reference:

```
KARAC=/path/to/karac ./verify.sh
```

That run is strongest with four optional tools present, and says so when they
are missing rather than quietly doing less: **numpy** (the differential
oracle), **node** (the wasm checks), **playwright** (the real-browser check),
and **`sips` or `tiffcp`** (the third-party TIFF control — `sips` ships with
macOS, `tiffcp` comes from libtiff, `apt install libtiff-tools`).

On a fresh clone, run `./build_web.sh` first: the wasm bundle is generated
output and is gitignored, so `verify.sh` skips every wasm and browser check
until it exists. (The `demo/` fixture is generated too, but `verify.sh` now
makes it on demand rather than treating its absence as a missing tool.)

## What it does

Six modes over a stack of 16-bit frames. The two integrators are the core;
the rest are those two with registration and channel handling around them:

| mode | what it computes |
|---|---|
| `mean` | arithmetic mean across all frames |
| `sigmaclip` | iterative 3σ clipping about the **median**, scaled by the **MAD** (max 5 passes), then the mean of the survivors |
| `register` | report the recovered per-frame transform and stack nothing |
| `stack` | register, then sigma-clip integrate — the one to reach for |
| `meancfa` | separate a Bayer mosaic into R,G,B and take the mean |
| `stackcfa` | register on luminance, then integrate the colour planes |

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

`index.html` is the app: drop FITS or TIFF subs in, pick an integration mode,
set a horizon row if the frame has foreground in it, get a stacked image — in
colour if the subs were RGB. Nothing is uploaded; the pixels never leave the
tab.

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
  page holds 16/16 subs as blob handles, no decoded pixels
  page stack byte-identical to native over 6144 pixels
  canvas painted, luminance range 0..255
  status line: Done in 131 ms · all 16 frames registered
  Bayer mosaic refused by the page, as the CLI refuses it
  Worker denied -> inline fallback ran, still byte-identical to native
  iPhone 13 390x664: no overflow, canvas 308px, stacked and painted
  Pixel 5 393x727: no overflow, canvas 311px, stacked and painted
```

The one thing the page reimplements is the **file readers**, in JS — `fits.mjs`
and `tiff.mjs`, each a header parse plus a row decode, behind the `subs.mjs`
dispatcher that sniffs which is which. They exist because the wasm entry point
takes pixels rather than files, and they are a real duplication: of the `BZERO`
trap on one side and of strip offsets, sample strides and byte order on the
other. So the checks pin the two decoders to each other on pixels — same files,
same stack, or the run fails — rather than leaving them to agree by inspection.

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

### Threads, and the two headers they cost

The page runs the **threaded** wasm module by default. Measured on an 18-core
M5 Pro, same 1024×768 ×16 input:

| leg | time | vs native |
|---|---|---|
| native, auto-par (18 cores) | 0.27 s | 1.0× |
| native, forced sequential | 2.18 s | 8.1× |
| wasm sequential | 3.82 s | 14.1× |
| **wasm threaded** | **0.46 s** | **1.7×** |

Threads are worth **8.3×** here, and the wasm tax that remains is a flat 1.63×
— measured at 0.79, 3.15 and 6.00 Mpx as 1.62×, 1.62×, 1.65×, so it does not
degrade with frame size.

The cost is two response headers:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

They put the page in cross-origin isolation, which browsers require before
handing out `SharedArrayBuffer`. That is a Spectre mitigation, not a Kāra
constraint. Concretely it costs: a host that lets you set headers (GitHub Pages
does not, without a proxy), and a standing rule that the page may never embed a
cross-origin asset without CORP/CORS. This page loads **zero** external
resources, so the second is free — it is the same self-containment that makes
"nothing is uploaded" true.

Memory cost of threading is a **fixed +36 MB**, not a multiplier: measured
+36.0, +36.0, +36.1 MB at 0.79, 3.15 and 6.00 Mpx. It is per-worker tile
buffers — 18 workers × `n·TILE·STRIP·8` — so it scales with worker and frame
count, never with frame area. At 24 MP that is about 4% on top.

Without the headers the glue falls back to the sequential module **silently and
correctly**: same pixels, 8.3× slower. That is precisely the regression that
ships unnoticed, so `verify_browser.mjs` asserts `getThreaded() === true`.
Removing the headers from its server is confirmed to fail that check — while
"byte-identical to native" still passes, which is the whole argument for
asserting it separately.

`verify_browser.mjs` runs the page at iPhone 13 and Pixel 5 viewports: zero
horizontal overflow, a canvas that fits the screen, a file-picker target big
enough to tap, and a stack that completes and paints. Emulation exercises
layout, touch and the DOM — **not** WebKit's engine and not a device's memory
ceiling — so it can show the page is broken on mobile and never that it is good.
What it does cover is the failure class that is invisible at desktop width.

### What resolution, not how many subs

Any real camera frame is far taller than `112·n` for a plausible sub count, so
it sits in the regime where peak is `w·h·12` and the sub count does not enter
(see the model below). The phone question is therefore a question about **sensor
size alone** — a 30-sub session costs what a 2-sub session costs:

| source | peak wasm |
|---|---|
| 3 Mpx (this demo's frames) | 37 MB |
| 24 MP full-frame | 276 MB |
| 45 MP | 521 MB |
| 60 MP | 690 MB |
| 24 MP **after CFA split** (3000×2000 planes) | 70 MB |

Desktop tabs carry the 24 MP figure; a mobile tab is killed well below the
60 MP one. So full-resolution **mono** is a desktop shape, and the memory-viable
mobile shape is the half-resolution plane the colour path already produces —
with the caveat that the CFA path is CLI-only today and loads the stack whole
rather than streaming, so the browser cannot reach it yet. Wiring it up is two
slices (expose it at the wasm entry, thread the row window through plane
extraction), not a new architecture.

### The ceiling is memory

Worth measuring rather than guessing. `mem_probe.mjs` instantiates the module
outside the browser and reports peak `memory.buffer.byteLength`; the wasm heap
is the same size whatever engine hosts it, so the figure is exact without a
device.

Two slices moved this number. The first halved a duplicated copy of the input;
the second removed the input from the peak altogether.

| frame | frames in | one blob, decoded twice | one blob | **streamed** |
|---|---|---|---|---|
| 512×512 ×16 | 8 MB | 27.6 MB | 19.6 MB | **6.6 MB** |
| 1024×768 ×16 | 24 MB | 63.6 MB | 39.6 MB | **12.8 MB** |
| 1024×768 ×64 | 96 MB | — | ~107 MB | **25.3 MB** |
| 2048×1536 ×16 | 96 MB | 225.6 MB | 129.6 MB | **37.1 MB** |
| 2048×1536 ×32 | 192 MB | — | ~226 MB | **39.8 MB** |

(The two `—` rows were never measured under the first version; their `one blob`
figures are that model — `w·h·(2n+8)`, which fit its measurements to within 4% —
evaluated at those shapes, and are marked `~` for that reason.)

**Round one: stop holding the input twice.** Peak used to fit `w·h·(4n+8)` bytes.
The `4n` should have been `2n`: `stack_frames` allocated a `Vec[u8]` for the raw
blob and decoded it into a separate `Vec[u16]`, both alive to the end of the
function. Half the peak was a copy of the input held in the format we had just
finished converting away from.

The fix was not to free the first buffer sooner. **wasm32 is little-endian by
spec and the blob was already little-endian u16, so the bytes JS held _were_ the
pixel array** — the host fn took `*const u16` and the copy landed directly in its
final home, deleting the second allocation and the `w·h·nframes`-iteration decode
loop with it. Declaring the parameter `*const u16` rather than `*const u8` is
also what keeps this *safe* code: the `u8` form needs
`px.as_ptr() as *const u8`, and Kāra requires `unsafe` for a cast that
reinterprets the pointee.

Wall time barely moved — 40.1 s against 41.8 s at 3 Mpx. The decode loop was
never the bottleneck (registration and integration are), so that was a memory win
that happened to remove a loop, not the speed-up it looked like.

**Round two: stop holding the input at all.** `w·h·2n` is still linear in the
whole session, so the ceiling was only pushed back, not removed — 226 MB for a
modest 3 Mpx ×32, on the device with the least memory. The page now streams
(see *Streaming*), and the term is gone:

```
peak ≈ max( pass1 , pass2 )

  pass1 = w·(STRIP+6)·2 + 65536·8          strip + halo, and the histogram
  pass2 = n·w·112·2 + n·256·64·8           strip window + tile gather
        + STRIP·w·10                       strip accumulator + rows out
```

**There is no `w·h` term.** Peak scales with frame **width** and sub count, and
never with frame **height** or area. Measured directly: 1024×4000 peaks at
**6.0 MB — the same as 1024×768**, with 5.2× the rows.

Three slices got here, and each removed a different `w·h` term:

| frame | resident | output streamed | both streamed |
|---|---|---|---|
| 1024×768 | 12.8 MB | 6.8 MB | **6.0 MB** |
| 2048×1536 | 33.1 MB | 9.1 MB | **9.3 MB** |
| 3000×2000 | 58.3 MB | 12.8 MB | **11.8 MB** |
| **6016×4016** (24 MP) | 275.7 MB | 47.4 MB | **20.1 MB** |

Thirty times the area between the first row and the last, and 3.3× the memory.
At 24 MP that is **13.7× less than where the day started**.

**Pass 2 streams its output.** `put_rows` hands each strip to the host as it
completes, so the finished image is assembled in the JS heap — which has no
4 GiB ceiling — instead of inside wasm, which does. The constrained heap holds a
strip; the unconstrained one holds the picture.

**Pass 1 streams its registration**, which needs a trick. Clipped statistics
need the whole frame before the scan can start, since the threshold is
`mean + 6·sd` over all of it. So the sub is walked twice: once to build a
**65536-bin histogram**, once to detect. The histogram is what holds that at two
reads rather than six — the three clipping rounds each need a sum and a
variance, and they now run over bins instead of pixels, which also makes the
statistics about 6× cheaper. A u16 histogram is a *lossless* re-encoding, so
nothing is approximated.

Detection strips carry a 3-row halo — the 3×3 maximum test and the ±3 centroid
window both reach that far — and emit only for their core rows, so no star is
found twice. The strips scan in the same ascending order the whole-frame version
did, so the stitched list is what `deduplicate` would have received anyway.

One thing genuinely changed, and it is worth stating rather than burying.
Summing histogram bins instead of pixels changes the floating-point accumulation
order. The **mean is unaffected** — every partial sum is an integer below 2⁵³, so
it is exact in any order — but the variance is not: the sd shifted in its last
few bits (185.90641024128087 against 185.9064102412528 on a 6 Mpx frame), moving
the detection threshold by 2e-10. Zero pixels fell on a different side of it, but
"no pixel happened to sit in the gap" is a property of one frame, not a
guarantee. So **both backends** compute it the new way: cross-backend
byte-identity, the bar this project actually holds itself to, stays provable
because native and wasm run the same accumulation in the same order.

The `max` between passes is a wasm property, not a program one: linear memory is
a **high-water mark and never returns pages**, so pass 1's freed buffers leave a
hole that pass 2's either fit inside — costing nothing — or do not. They never
add.

`mem_probe.mjs --assert-model` enforces this in `build_web.sh`, validated across
0.79→24.16 Mpx, n from 2 to 64, and the height axis independently.

Two earlier versions of this model were wrong, and how they were wrong is the
part worth keeping. The second read `w·h·10 + n·w·112·2 + …`, which was wrong in
*both* directions at once — it always charged the strip window even when the
hole absorbed it, and never charged pass 1's frame at all. Those two errors are
close in size at n=16, and every measurement ever taken was at n≥16, so they
cancelled and the bound passed. One untested axis was all it took.

> A model that holds because two errors point opposite ways is not a model.

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

The worker later turned out to be load-bearing for a second, unrelated reason:
`FileReaderSync` — the only synchronous way to read a `Blob`, and therefore the
only way to serve a synchronous `read_rows` — exists **only** in workers. See
*Streaming → And in the browser*.

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

## Calibration: darks, flats and bias

Three defects a real sensor puts into every sub, and none of them is noise —
they are **fixed patterns**, identical frame to frame, so stacking does not touch
them. More integration time makes them cleaner, not smaller.

| | what it is | how it enters |
|---|---|---|
| bias | readout offset, present in a zero-length exposure | additive |
| dark | thermal signal over the exposure, plus the bias | additive |
| flat | vignetting, dust motes, filter grime | multiplicative |

```
cumulus master_dark.cstack sigmaclip darks/*.fits     # masters are ordinary output
cumulus master_flat.cstack sigmaclip flats/*.fits
cumulus master_bias.cstack sigmaclip bias/*.fits
cumulus out.cstack stack --dark master_dark.cstack \
                         --flat master_flat.cstack \
                         --bias master_bias.cstack lights/*.fits
```

A master is just a Cumulus **output** — built by the integration modes that
already exist, exactly as Siril does it. Nothing new was needed to make them,
and they inherit the clipping that rejects cosmic rays from a dark as readily as
from a light.

The correction is `calibrated = (light - master_dark) / normalised_flat`.
Subtractive first, then multiplicative, because the flat measures the optical
path's response to **light** and the dark signal never travelled that path —
divide before subtracting and the dark current gets scaled by a vignetting
profile it was never subject to. `--bias` is not needed for the lights (a dark
taken at the light's exposure already contains it) but is needed for the
**flat**, whose exposure differs.

Masters stay resident while the lights stream: at most two frames, so
`2 × w × h × 2` bytes, independent of how many subs the session has.

Measured against a clean-scene truth the generator knows:

| | uncalibrated | calibrated |
|---|---|---|
| mean abs error vs truth | 0.2000 | **0.0051** (39.4× closer) |
| hot pixels surviving | 24 of 24 | **0** |
| corner/centre response | 0.908 | **0.778** (truth: 0.770) |

### It looked like an astronomy bug and it was a compiler bug

The first honest run made calibration **1.4× worse than doing nothing**, with
hot pixels rising from 8 to 24. Two rounds went into the synthetic generator's
physics before the compiler became a suspect, and one of those rounds found a
real error of mine: the generator vignetted the dark current, which the optics
never touch. The corrected model is `scene × vignette + thermal + bias` — the
lens attenuates the scene only; thermal signal and readout offset are added
afterwards, in the silicon.

That fixed the vignetting but not the hot pixels, and then the arithmetic
stopped fitting any correct calibrator. A master dark reading 45517 subtracted
from a light reading 46761 must give 1244. The result was 65535 — which follows
only if the subtrahend is **−20019**, i.e. 45517 − 65536.

A `Vec[u16]` element read through a **struct field** was sign-extending on a
widening cast, AOT only; the interpreter was correct throughout. Compiler ledger
**B-2026-08-11-32**, fixed. Calibration had been right all along.

The lesson worth keeping is not "check the compiler sooner" — the generator
really was wrong too, and doubting your own new code first is correct. It is
that a wrong answer wears the costume of whatever domain it appears in, and the
way out was arithmetic that no correct calibrator could produce, not intuition
about which layer was at fault.

## Streaming: the stack is no longer resident

The single term that made a real session impossible was holding every sub in
memory at once. `main` decoded the lot into one `Vec[u16]` of
`frames × pixels` and kept it for the whole run — 4.8 GB for 24 Mpx × 100
subs, more than most laptops have and more than wasm32's 4 GB address space
permits at any setting.

FITS input now streams. Peak becomes `frames × width × strip` instead of
`frames × width × height` — **independent of frame height**, which is what
unbounds the session:

| frames in | resident | streamed |
|---|---|---|
| 12 MB — 512×512 ×24 | 29.5 MB | **9.9 MB** |
| 50 MB — 512×2048 ×24 | 121.1 MB | **19.6 MB** |

Quadrupling the frame height quadruples the resident figure and roughly doubles
the streamed one — and that residual growth is the *output* (`w·h·8`), not the
frames. The frame term is gone; the output is the next lever.

### Two passes, because the stages want different things

**Pass 1 (registration)** wants one frame at a time — star detection is
per-frame. `compute_offsets` only ever looked at one frame anyway
(`detect_stars(px, f * npix, …)`); streaming just makes that explicit. Read a
sub, detect its stars, drop the pixels, keep the star list. Peak is one frame
regardless of how many subs there are.

**Pass 2 (integration)** wants one horizontal strip from *every* frame at once,
because sigma clipping needs all frames' values at a pixel simultaneously. So
the strip, not the frame, is the unit.

### Strips rather than tiles

The integrator works in 256² tiles internally, but streaming reads **strips**,
and the reason is the file layout. A strip is contiguous in a row-major FITS —
one large sequential read per frame. Square tiles would need a seek per row: at
6000×4000 with 100 subs that is ~10 million small reads instead of ~12 thousand
large ones.

Each strip seeks to the rows it needs, reads them, and integrates. The halo rows
shared with the neighbouring strip are simply read twice, which costs
`2·halo/STRIP` of extra I/O and buys a great deal of simplicity.

That simplicity is recent. `File` had no `seek` when this was written (compiler
ledger B-2026-08-10-3), so reads could only go forward and the strip walk had to
be a **sliding window**: retain the overlap from the previous strip, shift the
tail of every frame's slab to the front, then read only the genuinely new rows.
It worked, and it was where both of the bugs below came from. `File.seek` landed
and the retention became pointless — the shift loop, the cursor bookkeeping, and
the invariant tying each buffer position to its file's read offset all went with
it.

A `.cstack` stays resident, and now that is a *choice* rather than a limit. With
seek it could stream — one file holding every frame back to back is exactly what
seek is for. It does not, because it is the **control**: the oracle below is
"the streamed path agrees with the resident path", and if both paths stream
there is nothing left to check against. One deliberately resident reader is
worth more than a second streaming one. The CFA path stays resident too, since
`stack_cfa` separates planes across the full frame.

### The oracle, and why the obvious version of it was vacuous

`verify.sh` already asserted that the FITS path and the `.cstack` path produce
the same image. Now that FITS streams and `.cstack` does not, that check *is*
the streaming oracle for free: byte-identical is the bar, so streaming may be
slower but never different.

Except at 96×64 it was vacuous for the part that matters. One 64-row strip
covers the whole frame, so the window never advances — the check could not see
the sliding logic at all. There is now a second case at 200 rows (4 strips)
**with a dither**, so the window has to slide, retain its halo across each
boundary, and shrink at the last strip:

```
  mean: streamed over 4 strips == resident
  sigmaclip: streamed over 4 strips == resident
  stack: streamed over 4 strips == resident
```

Both bugs found while building this were invisible at one strip. The frame slab
was indexed by the window's **valid row count** instead of its allocated
**stride**, so every frame after the first was read a few rows into its
neighbour — a clean-looking stack of subtly wrong data. And a zero halo turned
strip edges into NO DATA. Neither crashes; both produce a picture. Forcing the
halo to zero is confirmed to fail the multi-strip check, so it is not vacuous
either.

### What it cost in the language, and what that cost bought

Three gaps in the file API shaped this code more than the astronomy did. All
three are now fixed, and the sequence is the point:

- **No `seek`** — forced the sliding window. Fixed (B-2026-08-10-3); the runtime
  entry point had existed all along and only the Kāra surface was missing.
- **No `mut` sub-slice** — `buf[2..]` is `Slice[u8]`, not `mut Slice[u8]`, so a
  short read could not be topped up in place. That forced a per-frame carry
  queue: read whole fixed chunks, hand back what the caller wanted, keep the
  remainder. About forty lines and a copy per refill. `split_at_mut` turned out
  to be fully specified in design.md and implemented nowhere — the read-only
  `split_at` had shipped and the mutable half had not (B-2026-08-10-4). It is
  now six lines of `read_exact`.
- **A `File` stored in a `Vec` deadlocked under AOT** (B-2026-08-09-17), which
  blocked the design outright: sequential access across many files means many
  concurrently-open handles.

That last one is the interesting one. It was only reachable *because* of the
first: no seek forced the many-handles design, which walked straight into a real
codegen bug that had nothing to do with files being numerous. A missing
primitive pushed the code onto a path where a separate defect was waiting.

### And in the browser, where only a worker can do it

The page had the same problem in the place it hurts most. The old host boundary
was `read_frames(dst, len)` — one call for the entire stack — so `index.html`
had to hold a decoded `Uint16Array` per sub *and* build a second, concatenated
copy of all of them to hand across. Counting the wasm side, a session existed
three times over on the device least able to afford it.

The interface change is the slice:

```kara
host fn read_rows(frame: i64, row0: i64, nrows: i64,
                  dst: *const u16, dst_off: i64) with reads(Input);
```

and `stack_frames` became the same two-pass strip walk the CLI runs, with
`read_rows` where the CLI calls `read_rows_at`. The page now keeps a `File`
handle and the six numbers parsed out of its header — geometry, `BZERO`,
`BSCALE`, the data offset — and never touches a pixel. Loading a hundred
24-megapixel subs costs what loading two costs.

**A `host fn` is synchronous and a `Blob` is not, and that is the whole
problem.** `read_rows` is called from inside a wasm frame, so it cannot await
`file.slice(a, b).arrayBuffer()`; there is no suspension point to await at. The
one API that reads a Blob synchronously is **`FileReaderSync`**, and it exists
**only in workers** — which was checked with a throwaway Playwright probe before
any of this was built, because the entire design rests on it:

```
{"ok":true,"bytes":[4,5,6,7,8,9,10,11]}   // frs.readAsArrayBuffer(blob.slice(4, 12))
```

So the worker — which existed for an unrelated reason, to stop the page freezing
— turns out to be the only place this design can run at all. The inline fallback
cannot: no `FileReaderSync` on the main thread, so it pre-reads every sub before
starting and gives streaming up. That is the honest trade for a path whose job is
to make a page opened over `file://` work at all, and it is still lighter than
the old page, because what it holds is raw FITS bytes decoded a row range at a
time rather than a decoded copy plus a concatenated one.

**What the harness had to learn to check.** None of this is visible to a pixel
comparison. A page that quietly went back to decoding every sub up front would
produce identical pixels, paint an identical canvas, and pass every assertion
that already existed — while being the exact thing this slice removes. Two new
ones close that gap:

- `test_node.mjs` records the **shape** of every `read_rows` call. Pass 2 must
  never ask for more than a strip plus its halo, and only pass 1 may read a
  frame whole. At 96×64 — one strip — it declines to claim anything, because a
  frame that short is read whole no matter what the module does; `verify.sh`
  runs a second stack at 200 rows for the assertion to bite.
- `verify_browser.mjs` asks the page what it is **holding**, per sub, by kind,
  and fails if anything is a typed array rather than a handle.

Both were confirmed by breaking them: re-adding a decoded `Uint16Array` to each
sub trips the second (`sub 0.px=bytes:12288`), and shrinking the strip bound
trips the first.

One thing fell out of rewriting the JS reader as a header parser. It now reads
`BAYERPAT`, so the page **refuses a colour mosaic** — which the CLI has always
done and the page silently did not, stacking it as if it were grey and producing
a plausible picture with checkerboard texture and colour-biased star positions.
`verify_browser.mjs` synthesises a four-pixel mosaic and requires the refusal.

One term is not gone, and should not be claimed away: **pass 1 still reads each
frame whole**, because star detection needs global background statistics before
it can scan. That is `w·h·2` bytes transient in wasm and the same again in the
worker's JS while `FileReaderSync` hands the buffer over — 96 MB together for a
24 Mpx sub, once per frame, freed before the next. It is bounded by one frame
rather than by the session, which is why it is not in the memory model, but it is
the largest single allocation the page makes and the next thing to attack if a
device ever chokes on it. Splitting `detect_stars` into a statistics pass and a
scan pass would remove it, at the cost of reading each sub twice in pass 1.

Worth recording for contrast with the native half above: this one **cost the
language nothing**. No missing primitive, no ledger entry, no workaround — the
Kāra side compiled and produced byte-identical output on the first build. Every
obstacle in this slice was a browser-platform fact (`FileReaderSync` being
worker-only) rather than a compiler gap. Three slices ago that was not the case.

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

## Rotation

Registration recovers a rotation as well as a translation. For a tracked mount
translation is enough; an **untracked** camera is a different problem. The sky
turns about the celestial pole, and inside a small field that is a translation
PLUS a field rotation — and the rotation's error is zero at the frame centre and
largest in the corners, so a translation-only stack looks perfect in the middle
and is mush at the edges.

Measured on a real 20-frame nightscape sequence (Nikon Z5, 24 mm, 13 s, 4 min
45 s total): **0.40° of field rotation**, which is **25 px of corner error** on a
6016×4016 frame. Cross-checked two ways — summing 19 consecutive-pair fits gave
0.4014° against 0.4037° fitting every frame to the reference — and against sky
mechanics: in 285 s the sky turns 1.191°, and the ratio 0.337 puts the field
centre near dec +20°, right for the summer Milky Way.

`estimate_transform` returns `(dx, dy, θ, votes)` in two stages, because neither
works alone. The **vote** finds the translation most star pairs agree on; it is
robust to the two lists having different membership, which they do, but it
cannot see rotation. Then **refinement** iterates: match each reference star to
its nearest neighbour under the current transform and refit rotation and
translation together, tightening the match radius as the fit improves. The refit
is the closed-form 2-D Kabsch solution. Scale is deliberately not fitted — the
sky does not change scale between frames, and a free scale would absorb
residuals and flatter the fit while hiding the rotation.

### Fitting one more parameter always helps, which is the trap

The first working version **invented up to 0.56° on frames that were purely
dithered**. That is not a coding error, it is identifiability: on a 96×64 frame
the corner is 58 px from centre, so half a degree moves it 0.6 px — the same
order as centroid noise. An extra free parameter always reduces the residual,
even against noise, so "the fit improved" proves nothing.

Rotation is therefore accepted only when it explains materially more than
translation alone: sum of squared residuals with the fitted angle against the
same with θ forced to zero. Self-normalising, so there is no pixel threshold to
tune per frame size, and it degrades to exactly the old translation-only answer
when the lever arm is too short to tell. The separation is total rather than
marginal:

| stack | rotation reported |
|---|---|
| dithered, none injected | **0.0000°** |
| rotated 0.5°/frame | recovered to 0.023° mean |

Translation got *better* too (0.025 px mean against 0.031), because it is no
longer absorbing a spurious angle.

This was caught by `check_register.py` precisely because that oracle is **ground
truth, not a differential**: a numpy reimplementation of the same estimator
would have made the identical mistake and agreed with itself.

### Rotation widens the halo

A tilted sample line draws a frame-edge pixel from a source row up to
`sin(θ)·w/2` away — about 21 rows for 0.40° at 6016 wide, on top of the dither.
`MAX_HALO` is 64 rather than the 24 that sufficed when registration was
translation-only, and the halo is still sized from the transform *actually*
recovered, so a tracked session pays nothing for the headroom. Exceeding it
degrades safely: `resample_tile`'s window test fails and those pixels become
NO DATA, which the integrator already excludes. Wrong data would be the
alternative.

### Measured, not merely measured

`verify.sh` checks the angle against injected ground truth, and separately that
the resampler *uses* it — a build that measured rotation perfectly and then
resampled by translation alone passes every other check in the file.
**Concentration** is the discriminating metric there, not peak: rotation error is
zero at the centre where the brightest stars sit, so peak barely moves while the
flux smears outward. On a 640×480 stack with 3.6° total, rotation-aware beats
translation-only by **1.305× concentration** at 0.99× peak — which is exactly the
signature, and exactly why comparing peaks would have called it a regression.

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

## Nightscapes: two subjects in one exposure

Everything above assumes the frame has **one** subject. A nightscape does not.
The camera is on a fixed tripod, the sky turns, the land does not — so a single
transform cannot serve both. Register on the stars and the stars come out sharp
while the ridge line smears into a grey band. Do not register and the land is
sharp and the stars are streaks. This is the whole reason Starry Landscape
Stacker and Sequator exist as separate tools from Siril and DSS.

`--horizon R` splits the frame at row `R`: rows above it are sky and take the
measured transform, rows below are land and are integrated with no transform at
all. `--feather N` ramps the weight linearly across `N` rows so the join reads
as haze rather than a seam.

```kara
fn sky_weight(y: i64, horizon: i64, feather: i64) -> f64 { ... }
```

The decision is per **row**, not per pixel, and that is not a shortcut — a
horizontal cut is constant along a row, so a per-pixel test would recompute the
same number `w` times. Only the tiles straddling the boundary blend at all;
above and below, the weight is exactly 1 or exactly 0 and the resampler takes
the branch it would have taken anyway.

### What it is worth, measured

Three stacks of the same ten frames, with 0.35°/frame of sky rotation and a
static foreground of ridge, town lights and a lake reflection. Sharpness is
summed squared gradient over each region:

| strategy | sky | land |
|---|---|---|
| unregistered | 67144 | 464313 |
| sky-only — *what a deep-sky stacker does* | 68207 | **377507** |
| **masked** | **68207** | **464313** |

The masked stack keeps **100%** of the unregistered land sharpness and beats
sky-only by **1.23×**, giving up nothing in the sky. Both halves get the
treatment they want, which is the entire claim.

### An oracle nothing else in the harness could replace

A smeared foreground is invisible to every other check here. Such a stack is
still byte-identical across backends, still matches the integration oracle to
the bit, still recovers its dithers to a hundredth of a pixel — it is *exactly
correct* at everything the pipeline was asked to do, and still the wrong
picture. So `check_nightscape.py` compares the three stacks above and asserts
the ordering only a working mask produces.

It is proven to fail two ways, because a checker that cannot fail is decoration:

- Feed it the **sky-only** stack in the masked slot and it catches the smear
  (`0.813 < 0.97`) and the missing gain (`1.000 < 1.08`).
- Run it on a fixture with **no foreground** and a non-vacuity guard catches
  that instead — if sky-only registration barely smeared the land (`0.860×`),
  there was nothing to protect and the pass would have meant nothing.

The second guard is the one worth having. Without it the check quietly turns
green the day someone regenerates the fixture without `--foreground`, and it
stays green forever.

### The bug the flags exposed

`--horizon` and `--feather` are the third and fourth flags Cumulus accepts, and
adding them made a latent argument-parsing bug unmissable. The input-shape test
counted `argv.len()`, which includes flags — so two flag pairs made a single
`.cstack` look like a sequence of FITS files, and it died with *"no END card in
header"* on a container it had just written itself.

```kara
let ninputs = argv.len() - first_in;
if ninputs > 1 or inp.ends_with(".fits") { ... }
```

`--dark d.cstack in.cstack` could already trip this with one flag pair; my two
just made it certain. It is now counted from `first_in`, with a regression test
that runs `mean --horizon 40 --feather 4` against a `.cstack` and demands the
same bytes as running it with no flags at all.

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

## TIFF input, and the RGB path

FITS is what a telescope writes. TIFF is what a camera-on-a-tripod session
**becomes**: RAW into Lightroom, ACR or darktable, 16-bit TIFF out, and that
TIFF is what Starry Landscape Stacker and Sequator ingest. Reading it is the
difference between a tool that works on files a photographer already has and
one that works on files they would first have to convert.

Baseline, uncompressed, strip-organised TIFF: both byte orders, 8 or 16 bits,
1 sample (mono) or 3 (RGB), any `RowsPerStrip`. The format is sniffed from the
file's first bytes rather than from its name, so `.tif`, `.fits`, `.fit`, and a
file with no extension at all are all handled by what they actually are.

### Transcription as the oracle

The check is not "does it decode plausibly". `gen_tiff.py --from-cstack`
rewrites an **existing** container as one TIFF per frame, so stacking the TIFFs
must land on exactly the bytes stacking the container lands on:

```
  16-bit little-endian, 64 rows/strip: identical to the container
  16-bit big-endian,    64 rows/strip: identical to the container
  16-bit little-endian,  8 rows/strip: identical to the container
  16-bit big-endian,     7 rows/strip: identical to the container
   8-bit little-endian, 64 rows/strip: identical to the container
   8-bit big-endian,     5 rows/strip: identical to the container
```

Zero tolerance, which is what makes it useful — a stride error, a byte-order
slip or an off-by-one strip offset cannot hide inside an equality. The odd
`RowsPerStrip` values are there because they make the **last strip partial**,
which is where a strip walk goes wrong if it goes wrong. The 8-bit rows are
lossy by construction, so the generator also writes the container that round
trip should land on (8-bit expands by bit replication, ×257, which sends 255 to
exactly 65535 — a bare shift would cap at 65280 and darken the whole sequence);
that keeps even the lossy case an equality rather than a tolerance.

### The control that matters more than any of them

All of the above shares one author's mental model of TIFF between the generator
and the reader. A mistake made in **both** is invisible: every test passes while
real files fail. So `verify.sh` re-encodes the fixtures with something that has
never seen this code, and demands the same stack:

```
  sips re-encode (MM byte order): byte-identical stack       # macOS
  tiffcp re-encode (II byte order): byte-identical stack     # anywhere else
```

Two tools, in preference order, because neither is everywhere. `sips` is macOS
ImageIO, which rewrites the IFD in its own layout and — as it happens — the
opposite byte order. `tiffcp` is libtiff's own copier, so on Linux the control
is the format's **reference implementation**. Agreement with either is worth
more than agreement with six variants of my own.

ImageMagick is deliberately *not* on that list. It is an image processor rather
than a container copier: it may apply colour management, and a Q8 build
silently halves the depth. Either would make the comparison fail while the
reader was perfectly correct — a false alarm pointing at the wrong file.

Which is the hazard the rest of this needs guarding against, since a control
that can be wrong in a way that looks like the thing it is controlling is worse
than no control. So a candidate tool has to earn the job:

- **It must not change the image.** `gen_tiff.py --probe` is a *third* reader —
  four tags, no pixels, separate from both the ones under test — so "did the
  encoder alter this file" is not a question either suspect gets to answer.
  A tool that emits 8-bit where it was given 16 is rejected by name and the
  next one is tried.
- **It must actually re-encode.** A tool that copies the bytes verbatim proves
  nothing, so a byte-identical output disqualifies it too.
- **If none qualifies, the run says so** and stays green, rather than passing
  silently as though the control had run.

Every one of those branches is exercised — including a stand-in that halves the
depth (`changed the image shape (96 64 3 16 -> 96 64 3 8)`) and one that really
does stack differently, which exits 1 as it should.

### RGB: three planes, one transform

Registration runs on the **median** of a pixel's three samples, for the same
reason `cfa_luminance` takes the median of four photosites: a hot pixel or a
cosmic ray usually lands in one channel, and a median drops that outlier
outright where a mean merely divides it by three and lets it drag the star's
measured centre.

The single transform it recovers then drives all three planes. Colour planes of
one exposure came through one lens onto one sensor; registering them
independently could only introduce disagreement between them that the optics
never had.

`check_tiff.py` asserts the injected R:G:B ratios came back, because nothing
else here can see a channel transposition — such a stack is the right size, has
sharp stars, and passes every other oracle in this repo:

```
  star 0 R:G:B  got 1.00:0.35:0.20  want 1.00:0.35:0.20  (max err 0.005)
  star 1 R:G:B  got 0.24:0.45:1.00  want 0.25:0.45:1.00  (max err 0.007)
  star 2 R:G:B  got 1.00:1.00:1.00  want 1.00:1.00:1.00  (max err 0.003)
```

Three ablations, three correct failures: transpose R and B (2 stars off),
shift one plane by a single pixel (1 star off), and neutralise the injected
colours — at which point the non-vacuity guard refuses to certify anything,
because with a grey fixture it could not have caught either of the first two.

That guard reads the **injected** table, not the result, and the distinction is
the whole point. Measuring the result's own discrimination looks equivalent and
is not: a genuine transposition inverts it, so the run fails with *"your fixture
is weak"* when what actually happened is *"your pipeline swapped two
channels"* — the checker blaming its own input for the defect it exists to find.
That is exactly what the first version of it did.

### RGB is what forced the output to stream

Three planes of a 24 MP sub is 144 MB, so a ten-frame nightscape is 1.4 GB
resident — a TIFF sequence has no resident path at all, it always streams. But
the *output* was still frame-sized: an `i64` accumulator of `w·h` per plane
plus the encoded bytes on top, which at 24 MP RGB is 576 MB + 288 MB before a
single byte reached the disk.

So `stack_streaming` became `stack_streaming_to`, writing each strip as it is
finished — the same move the browser slice made with `put_rows`, arriving on
the native side. Peak is now set by `STRIP` and the halo, never by `h`, and the
mono path inherited it for free. Planes are stacked one at a time, which reads
each file three times; at 24 MP that trades about two seconds of warm-cache I/O
for four hundred megabytes of resident accumulator.

### And in the browser, where the app actually lives

A TIFF path that worked only on the CLI would be half a feature for a tool
whose whole identity is *stack in a tab*. `tiff.mjs` is the page-side reader,
`subs.mjs` the dispatcher that sniffs which of the two formats a file is — the
JS twin of `read_sub_header` / `read_sub_rows` in `cumulus.kara`, and it exists
for the same reason: everything above it wants one question answered and should
not branch on the container twice.

The host contract grew a `plane` argument on both sides (`read_rows(frame,
plane, …)`, `put_rows(ptr, len, plane, …)`), and `stack_frames` gained
`nplanes`, `horizon` and `feather` — so the page can now do the nightscape
split too, via a horizon-row control it did not have.

**Two decoders of one format is where disagreements hide**, because each is
self-consistent and the page still paints something. So `test_node_tiff.mjs`
pins them together on pixels — RGB, mono, 8-bit, both byte orders, multi-strip,
and Apple ImageIO's re-encode — each byte-identical to what the native binary
made of the same files. It also asserts the *request shape*: a run must ask for
plane −1 and planes 0/1/2 and nothing else, because a host that answered every
request from plane 0 would return a grey image in three identical planes, which
is a valid stack of the right size.

`verify_browser.mjs` then drives the real page in real Chromium and adds the
one thing only a browser can check — that three planes reach the **canvas** as
colour:

```
  RGB TIFF in the page: byte-identical to native over 18432 samples
  canvas painted in colour (R-B spans -68..122)
```

Ablate `render` to paint plane 0 into all three channels and the byte
comparison still passes — the data is right, only the display is grey — and
only the colour assertion fails. Which is the point of having it.

One stretch spans all three channels rather than one per channel. A per-channel
stretch is an automatic white balance: it maps each channel's own percentiles
onto the same output range, flattening exactly the colour the pipeline just
worked to preserve. Light pollution really is redder than the sky, and showing
that is more honest than hiding it behind three normalisations.

### The stale reference this slice exposed

`build_web.sh` builds a native binary to `/tmp/cumulus_ref` and measures every
"byte-identical to native" claim against it. Its default compiler was a
tree-local **debug** build — and a `karac` compiled without `--features llvm`
makes `build` a no-op: it type-checks every target, prints nothing about
emitting, and **exits 0**. So the previous run's binary stayed in `/tmp` and the
whole suite compared today's wasm against a week-old native.

Green, and measuring nothing. It had been that way since 2026-08-22 and nothing
noticed, because a stale reference still agrees with itself on everything that
did not change. TIFF is what broke the silence: the old binary could not read
one, so the step failed loudly instead of passing vacuously.

The fix is to delete the binary first and require it back, with a message that
names the cause — plus preferring `karac` on PATH, which is what `verify.sh`
already did and is why `verify.sh` never had the bug.

### Refusals

Every fixture behind these is a **valid** TIFF that other decoders open — real
zlib strips, real tiles, a real planar layout — which is what makes a refusal a
statement about Cumulus rather than about a broken fixture:

```
cumulus: sub.tif: unsupported TIFF compression 8 — only uncompressed is
         implemented (re-export with compression off, or
         `magick in.tif -compress none out.tif`)
cumulus: sub.tif: tiled TIFF is not implemented (only strip-organised files)
cumulus: sub.tif: unsupported PlanarConfiguration (only chunky, 1, is implemented)
cumulus: sub.tif: unsupported SampleFormat (only unsigned integer is implemented)
cumulus: sub.tif: unrecognised file — expected FITS (SIMPLE), TIFF (II/MM) or a
         .cstack container (CSTK)
```

The last one is new and replaced a worse message. A JPEG named `.tif` used to
fall through to the FITS reader and be told *"no END card in header"*, which
sends the operator looking for a corrupt FITS file that never existed.

Calibration is refused for RGB rather than approximated: a dark's hot pixels and
a flat's vignetting are both wavelength-dependent, so one mono master applied to
R, G and B alike is three different wrong corrections, not one roughly right
one. Per-channel masters are the fix and are not implemented.

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

1. **Irregular horizon masks.** `--horizon` is a horizontal line, which is the
   crudest mask that works and the mode Sequator ships as its simplest. A tree
   line, a peak, or an arch crossing the boundary is not served by a straight
   cut. The rest of the machinery does not care: the mask enters as a weight
   per sample, so an arbitrary mask changes `sky_weight` and nothing else. What
   it really needs is a way to *author* the mask — a drawing surface in the
   page, or a PNG alpha channel from another tool.
2. **Calibration in the BROWSER.** The CLI takes `--dark`, `--flat` and
   `--bias`; the page has no UI for them and passes none, so a browser stack is
   uncalibrated. The kernels are already shared and target-agnostic
   (`calibrate_rows` is called from the row loop either way), so this is a file
   picker and three more `read_rows`-shaped host calls, not new numerics. It is
   now the *only* CLI capability the page lacks — masking and TIFF both reached
   it with the slices above.
3. **Drizzle.** The CFA path is superpixel demosaic, so colour output is half
   resolution. The dithers carry the information needed to recover full
   resolution, and using it is the natural follow-on — the plane-separated
   architecture is already the right shape for it.
4. **Deblending, and an adaptive centroid window.** The fixed ±3 window
   truncates bright stars asymmetrically and makes their centroids bistable by
   ~0.4 px; widening it naively blends close pairs instead. Both want the same
   fix, and it needs its own slice — see the CFA section for the measurement.
5. **Better interpolation** — bilinear softens slightly; Lanczos-3, which Prism
   already implements, is the upgrade once the pipeline is trusted.
6. **Wider FITS** — float and 8-bit `BITPIX`, 3-D colour cubes, compressed
   HDUs, and `ROWORDER = 'BOTTOM-UP'`. Vendor RAW decoding stays out of scope:
   `rawpy`, `dcraw` or `siril -s` convert to FITS in a few lines, which is
   exactly what Siril itself does internally before any astronomy happens.
7. **Wider TIFF** — LZW/Deflate/PackBits compression, tiled layout, BigTIFF,
   floating-point samples, RGBA. Compression is the one that will actually be
   hit, because several exporters default to it; it wants a `zlib` and an LZW
   decoder in the row reader and changes nothing above that line, since a strip
   is decompressed into exactly the bytes the current reader already expects.
8. **Per-channel calibration masters**, without which an RGB sequence cannot be
   calibrated at all — see the TIFF section for why a mono master is not an
   approximation of the right answer.
