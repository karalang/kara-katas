# Prism — a local image workbench, in one Kāra source

Drop a photo → it's processed **entirely in your browser** and **never
uploaded**. The pixel math runs in Kāra compiled to WebAssembly; the browser
only decodes and re-encodes the file (JPEG/PNG/WebP via `createImageBitmap` /
`canvas.toBlob`). Open the Network tab and watch it stay empty.

This is the "web convenience + desktop privacy" corner almost no image tool
occupies — the same all-local-in-browser model as Squoosh, but with Kāra owning
the compute. Tracked in the compiler's dogfooding roster
(`kara/docs/dogfooding.md` → **Prism**).

## Status — walking skeleton

- File-drop → decode → **grayscale kernel (Kāra)** → canvas → download PNG.
- Request-driven: JS calls the exported `process(w, h)` on each file-drop; there
  is no render loop.
- Resize/upscale, crop, rotate, adjustments, and more filters are the next
  slices (Kāra owns each kernel; the worker-pool/SIMD parallel pass lands with
  the `--features wasm-threads` build).

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

`test_node.mjs` instantiates `prism.wasm` with mock host fns that feed a known
2×1 RGBA image, calls `process(2, 1)`, and asserts the grayscale output
(`[76,76,76,255, 150,150,150,255]`). This is a pure-node end-to-end check of the
host-FFI-in → kernel → host-FFI-out path — the exact path that surfaced the
wasm `karac_free_buf` ABI bug (compiler ledger **B-2026-07-20-10**).

## How it works

- `prism.kara` — the host-fn declarations (`read_src`, `put_pixels`) and the
  `#[target(wasm_browser)] pub fn process(w, h)` export that pulls the source
  pixels in, runs the kernel, and blits the result. Pure pixel math; no browser
  knowledge.
- `index.html` — the JS glue: decode the dropped file to RGBA, feed it in via
  `read_src`, call `process`, paint the `put_pixels` result to a `<canvas>`,
  and re-encode locally for download.
