# Prism — a local image workbench, in one Kāra source

Drop a photo → it's processed **entirely in your browser** and **never
uploaded**. The pixel math runs in Kāra compiled to WebAssembly; the browser
only decodes and re-encodes the file (JPEG/PNG/WebP via `createImageBitmap` /
`canvas.toBlob`). Open the Network tab and watch it stay empty.

This is the "web convenience + desktop privacy" corner almost no image tool
occupies — the same all-local-in-browser model as Squoosh, but with Kāra owning
the compute. Tracked in the compiler's dogfooding roster
(`kara/docs/dogfooding.md` → **Prism**).

## Status — usable workbench

- File-drop → decode → **Kāra kernels** → canvas → download (PNG/JPEG/WebP +
  quality slider + encoded-size readout).
- Kernels: **grayscale** (fans out too, 1.32x — see below), **bilinear
  resize**, **Lanczos-3 resize** (separable,
  precomputed normalized tap tables, anti-aliased downscale — 360 ms for a
  12 MP → 3 MP downscale on the worker pool, 97 ms for 3 MP → 0.75 MP; see
  the measured table below), **crop** (drag a selection on the canvas),
  **rotate 90/180/270**, **flip H/V**, and
  **brightness/contrast/saturation** adjust.
- Edits **chain**: the export is `process(op, w, h, a, b, c, d)` over the
  current *working image*; each result becomes the new working image
  (crop → resize → adjust …), with an 8-step Undo and an Original reset.
- **Multicore + SIMD, with no parallel code in the source**: the resamplers
  are ordinary sequential `for` loops. The compiler proves that iteration `dy`
  writes the output only within `[dy * (4 * dw), (dy + 1) * (4 * dw))` — so no
  two rows can touch the same slot — and fans them across the worker pool by
  itself. Ask it: `karac query concurrency prism.kara.resize_bilinear`. The
  Lanczos vertical pass additionally runs `Vector[f64,2]` lane pairs — one v128
  load per pair via the adjacent-lane fusion peephole (kara B-2026-07-21-3).
  This replaced a hand-rolled band fan-out (an arbitrary `let bands = 8`, ceil
  division, tail clamping, a `Vec[TaskHandle[Vec[u8]]]` and an in-order concat
  with offset tracking, plus a `*_band` helper per kernel whose `y0`/`y1`
  parameters existed only to serve the banding). Deleting it made the code
  **faster**: measured natively at 1600×1200 → 800×600, Lanczos runs 37.4 ms
  against the band version's 48.8 ms (**23% faster**, 2.08× vs sequential,
  output byte-identical) — the compiler writes straight into the output buffer,
  where the band version paid a per-band allocation plus a concat copy.
  **Re-benched in the browser** on the converted build (`node
  bench_browser.mjs`, median of 7, headless Chrome, 4-core Linux; both legs
  drive the shipped artifacts through the same span the UI's own ms readout
  reports):

  | lanczos-3 downscale | sequential (`?seq`) | threaded (COOP/COEP) | |
  |---|---|---|---|
  | 12 MP → 3 MP | 802 ms | **360 ms** | 2.23× |
  | 3 MP → 0.75 MP | 152 ms | **97 ms** | 1.57× |

  The figures this README quoted before the conversion came off the band build
  on a different machine, so they are not comparable to these and are not
  reproduced.

  **`grayscale` fans out as well**, once written as `for p in 0..w * h` with
  `i = p * 4`. It had been a strided `while i < n { … i = i + 4 }`, which is not
  a shape the proof accepts — it wants a unit-stride `for v in lo..hi` — so it
  had been running single-threaded without saying so. Restated, it measures
  **1.32x** at 12 MP on 4 cores (22.1 ms/rep against 29.3 ms/rep), output
  identical. That is well under the resize kernels' 1.5–2.2x, and it should be:
  four byte loads and a little integer arithmetic per pixel is close to pure
  memory streaming, so there is not much for extra cores to do. The remaining
  kernels (`crop`, `rotate`, `flip`, `adjust`) are still `while` loops and still
  sequential. Threads come from `instantiateThreaded()`
  (kara B-2026-07-20-13); a sequential build runs the same source. The page
  auto-picks: with COOP/COEP headers (`./build.sh --serve` uses `serve.py`)
  you get threads; without, the vendored **coi-serviceworker** shim (MIT,
  gzuidhof/coi-serviceworker v0.1.7) registers a service worker that injects
  the headers client-side and reloads once — so even a headers-blind host
  like GitHub Pages gets the multicore module. `?seq` in the URL skips the
  shim and pins the single-threaded fallback.
- **Real-browser verified, three legs**: `verify_browser.mjs` drives the
  actual page in headless Chrome over CDP — the sequential-fallback leg
  (`?seq`: fallback pinned + load, grayscale oracle pixels, undo, rotate,
  resize, crop, chained), the threaded leg (real COOP/COEP headers, threaded
  module picked, grayscale oracle, banded Lanczos resize on the pool), AND
  the coi-shim leg (headerless server → SW-injected isolation → threaded +
  oracle — the GitHub Pages simulation). `./build.sh --verify`.
- EXIF awareness and a horizontal-pass SIMD story (u8→f64 gather, not yet peephole-covered) are the next slices.

## Build & run

```bash
./build.sh          # build prism.wasm + prism.js, run the node smoke test
./build.sh --serve  # then open http://localhost:8000
```

`karac` comes from the sibling Kāra compiler checkout by default
(`../../../kara/target/debug/karac`); override with `KARAC=/path/to/karac`.
Any static server works: with COOP/COEP headers (`serve.py`) the threaded
module loads directly; without them the coi-serviceworker shim supplies the
isolation after a one-time reload. **Deploying:** the live copy is
`karac.dev/prism`, served from the `karalang/website` repo's `public/prism/`
— sync fresh artifacts there with `../sync-website.sh` (see `apps/DEPLOY.md`).

## Regression harness

`test_node.mjs` instantiates `prism.wasm` with mock host fns, feeds known
pixels, and asserts exact outputs for every kernel: grayscale (Rec.601 oracle),
bilinear (hand-computed 2×1→4×1 gradient + identity), and Lanczos-3
(constant-image invariance up/down + step-edge symmetry with bounded ringing —
windowed-sinc overshoot at edges is textbook behavior, asserted as such). This
is a pure-node end-to-end check of the host-FFI-in → kernel → host-FFI-out
path — the exact path that surfaced the wasm `karac_free_buf` ABI bug
(compiler ledger **B-2026-07-20-10**).

## How it works

- `prism.kara` — the host-fn declarations (`read_src`, `put_pixels`) and the
  `#[target(wasm_browser)] pub fn process(w, h)` export that pulls the source
  pixels in, runs the kernel, and blits the result. Pure pixel math; no browser
  knowledge.
- `index.html` — the JS glue: decode the dropped file to RGBA, feed it in via
  `read_src`, call `process`, paint the `put_pixels` result to a `<canvas>`,
  and re-encode locally for download.
