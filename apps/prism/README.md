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
- Kernels: **grayscale**, **bilinear resize**, **Lanczos-3 resize** (separable,
  precomputed normalized tap tables, anti-aliased downscale — ~360 ms for a
  3 MP resize, ~1.2 s for 12 MP, main-thread), **crop** (drag a selection on
  the canvas), **rotate 90/180/270**, **flip H/V**, and
  **brightness/contrast/saturation** adjust.
- Edits **chain**: the export is `process(op, w, h, a, b, c, d)` over the
  current *working image*; each result becomes the new working image
  (crop → resize → adjust …), with an 8-step Undo and an Original reset.
- **Multicore + SIMD**: both resamplers fan across the worker pool in 8 row
  bands via `instantiateThreaded()` (kara B-2026-07-20-13), and the Lanczos
  vertical pass runs `Vector[f64,2]` lane pairs — one v128 load per pair via
  the adjacent-lane fusion peephole (kara B-2026-07-21-3). Measured on node:
  12 MP Lanczos **1058 → 285 ms** (threads 2.4× × SIMD 1.5×; 4.1× vs the
  single-thread scalar baseline), 3 MP **516 → 101 ms**, 12 MP bilinear
  upscale 1575 → 763 ms (2.1×), output **byte-identical** throughout. One
  source: a sequential build runs the same `TaskGroup` code FIFO. The page
  auto-picks: with COOP/COEP headers (`./build.sh --serve` uses `serve.py`)
  you get threads; without, the sequential module — same call shape.
- **Real-browser verified, both legs**: `verify_browser.mjs` drives the actual
  page in headless Chrome over CDP — the sequential-fallback leg (load,
  grayscale oracle pixels, undo, rotate, resize, crop, chained) AND the
  threaded leg (cross-origin isolated, threaded module picked, grayscale
  oracle, banded Lanczos resize on the pool). `./build.sh --verify`.
- EXIF awareness and a horizontal-pass SIMD story (u8→f64 gather, not yet peephole-covered) are the next slices.

## Build & run

```bash
./build.sh          # build prism.wasm + prism.js, run the node smoke test
./build.sh --serve  # then open http://localhost:8000
```

`karac` comes from the sibling Kāra compiler checkout by default
(`../../../kara/target/debug/karac`); override with `KARAC=/path/to/karac`.
A plain static server suffices — this is a sequential (main-thread) wasm_browser
build, so no COOP/COEP headers are needed.

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
