# Prism — a local image workbench, in one Kāra source

Drop a photo → it's processed **entirely in your browser** and **never
uploaded**. The pixel math runs in Kāra compiled to WebAssembly; the browser
only decodes and re-encodes the file (JPEG/PNG/WebP via `createImageBitmap` /
`canvas.toBlob`). Open the Network tab and watch it stay empty.

This is the "web convenience + desktop privacy" corner almost no image tool
occupies — the same all-local-in-browser model as Squoosh, but with Kāra owning
the compute. Tracked in the compiler's dogfooding roster
(`kara/docs/dogfooding.md` → **Prism**).

## Status — skeleton + resize

- File-drop → decode → **Kāra kernel** → canvas → download PNG.
- Kernels so far: **grayscale**, **bilinear resize**, **Lanczos-3 resize**
  (separable, precomputed normalized tap tables, anti-aliased downscale —
  ~360 ms for a 3 MP resize, ~1.2 s for 12 MP, main-thread).
- Request-driven: JS calls the exported `process(op, sw, sh, dw, dh)` on each
  action; there is no render loop. UI has target-size inputs with aspect lock,
  a method picker, and ½×/2× shortcuts.
- Crop, rotate, adjustments, more filters, and the worker-pool/SIMD parallel
  pass (`--features wasm-threads`) are the next slices.

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
