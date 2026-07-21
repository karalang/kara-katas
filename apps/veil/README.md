# Veil — a privacy-first, fully-local image redactor in Kāra

Redact screenshots and photos **entirely in the browser** — the sensitive file
is never uploaded. Draw a box over what should disappear; the redaction kernel
(Kāra compiled to WebAssembly) runs on your machine. Downloading re-encodes the
image, which also strips EXIF/GPS metadata.

The pitch is the inversion of every "redact online" tool: *nobody should have
to upload the thing they are trying to hide.* Veil is the second app on the
Prism spine (`../prism`) — same host-FFI legs (`read_src` / `put_pixels`),
same request-driven export model, same working-image chaining.

Roster entry: `kara/docs/dogfooding.md` § Veil.

## Redaction styles

| Style | Kernel | Safety |
|---|---|---|
| **Solid bar** (default) | fill rect black/white, opaque | **Destroys** the pixels — the safe choice for text (keys, names, numbers) |
| **Pixelate** | per-tile RGB mean (block size 2–40) | Degrades only — weak mosaics are attackable |
| **Blur** | 3× box blur (radius 2–40), sampling clamped to the rect (no bleed in or out) | Degrades only |

The UI states this honestly: blur/pixelate *degrade*, the bar *destroys*.

## Build & run

```bash
./build.sh                # build veil.wasm + veil.js, run the node oracles
./build.sh --serve        # …then serve on http://localhost:8000
./build.sh --verify       # …then drive the real page in headless Chrome
```

Sequential `wasm_browser` build — main thread, no COOP/COEP, any static host
serves it (`index.html + veil.js + veil.wasm` is the whole deploy).

## Verification

- `test_node.mjs` — exact oracles through the real wasm: pixelate tile-average
  (hand-computed), bar fills (black/white, alpha forced opaque, outside
  untouched), blur solid-region invariance + a hand-traced 3-pass integer box
  blur (`[90,0,0] → [31,25,20]` at radius 1).
- `verify_browser.mjs` — headless Chrome over CDP drives the *real page*
  (style/shade/strength controls + the Redact button): bar redaction lands
  exactly, the outside pixel is untouched, undo restores, pixelate's tile
  average appears on the canvas.

## Next slices

- Multiple pending boxes before a single "redact all" (today: one box per apply,
  redactions accumulate via the working image).
- Regex-driven PII auto-suggest (emails/phones/keys) once a text-region source
  exists (OCR is out of scope; DOM-side text selection for screenshots of pages
  is a possibility).
- EXIF viewer panel ("what your file was carrying") before/after.
