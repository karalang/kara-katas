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

## Sample screenshot

The chip under the drop zone paints a fabricated account page — name, email,
address, a live-looking API key, a card number — with canvas 2D, so a visitor
can see what the tool does without handing it the sensitive file first. That
catch-22 is the whole reason it exists: the pitch is "never upload the thing
you are hiding", and until you have watched it work, taking that on trust is
exactly what the tool asks you not to do.

The API key uses a prefix no provider issues. In a real vendor's format it
trips GitHub push protection on the way into this repo — and every secret
scanner the page passes through after that.

**Start over** (next to Undo/Original) empties the canvas and returns to the
drop zone, so you can move between the sample and your own screenshot. It
drops the canvas bitmap, not just the references — a redactor should stop
displaying the sensitive image the moment you ask it to.

It is **drawn, not fetched**: no request, no bundled asset, nothing to
license, no EXIF — the Network tab stays empty on the sample too. Every value
in it is invented (example.com, 555 numbers, the well-known Stripe test card)
and the image carries a SAMPLE stamp, so a redacted export can never be
mistaken for a real leak.

## Build & run

```bash
./build.sh                # build veil.wasm + veil.js, run the node oracles
./build.sh --serve        # …then serve on http://localhost:8000
./build.sh --verify       # …then drive the real page in headless Chrome
```

Sequential `wasm_browser` build — main thread, no COOP/COEP, any static host
serves it (`index.html + veil.js + veil.wasm` is the whole deploy).
**Deploying:** the live copy is `karac.dev/veil`, served from the
`karalang/website` repo's `public/veil/` — sync fresh artifacts there with
`../sync-website.sh` (see `../DEPLOY.md`).

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
