// mem_probe.mjs — measure the wasm module's PEAK linear memory for a stack run.
//
// The question this answers is "will this page survive on a phone". Mobile
// browsers do not fail a wasm build for lack of features — every phone shipped
// in the last five years runs this module — they fail it by killing the tab
// when linear memory gets large. So the number that decides mobile viability is
// peak `memory.buffer.byteLength`, and it is measurable here, exactly, without a
// phone: the wasm heap is the same size whatever engine hosts it.
//
// Usage: node mem_probe.mjs <in.cstack> [mode]
//
// Reports peak wasm memory and peak node RSS. RSS is the looser bound here
// because this harness holds the whole `.cstack` resident to serve row ranges
// out of it; the page does NOT — it answers the same calls from Blobs the
// browser keeps on disk — so on a phone the wasm figure is the one that
// decides, and RSS overstates the real page by the size of the session.

import { readFileSync } from "node:fs";
import { instantiate } from "./cumulus.js";

const args = process.argv.slice(2);
const assertModel = args.includes("--assert-model");
const [inPath, modeArg] = args.filter((a) => !a.startsWith("--"));
if (!inPath) {
  console.error("usage: node mem_probe.mjs <in.cstack> [mode] [--assert-model]");
  process.exit(2);
}
const mode = Number(modeArg ?? 2);

// With `--assert-model`, fail if peak falls outside
// `[w*h*8, w*h*10 + max(w*h*2, strip) + SLACK]`.
//
// Read the model term by term, because its SHAPE is the claim being made:
//
//   w*h*8    the i64 accumulator the stack integrates into — one per output
//            pixel, and the largest single allocation
//   w*h*2    the 16-bit result handed to the page
//   max(...) EITHER pass 1's resident frame (`w*h*2`) OR the pass-2 strip
//            window plus per-tile gather (`n*w*WIN*2 + n*TILE*STRIP*8`),
//            whichever is LARGER — never their sum
//
// The `max` is the whole subtlety, and it is a property of wasm rather than of
// this program: **linear memory is a HIGH-WATER MARK and never returns pages**.
// Pass 1's frame is freed before pass 2 allocates, but freeing does not shrink
// `memory.buffer.byteLength`; it only leaves a hole. Pass 2's strip window then
// either fits in that hole — costing nothing — or does not, and extends memory
// by its own size. So the two never add, and which one is visible flips at
// roughly `h = 112 * n`:
//
//   TALL frames / few subs  -> the hole wins, peak is `w*h*12`, and `n` DOES
//                              NOT APPEAR. Measured at 6000x4000: byte-identical
//                              275.7 MB at n = 2, 4, 8 and 16. Adding subs is
//                              free, which is the prize the streaming slices won.
//   SHORT frames / many subs -> the window wins and peak grows with `n`.
//                              Measured at 1024x768: 10.1 MB at n = 2 and 4,
//                              12.8 at 16, 16.9 at 32.
//
// THE MODEL HERE WAS WRONG UNTIL 2026-08-15, and wrong in BOTH directions at
// once. It read `w*h*10 + n*w*WIN*2 + n*TILE*STRIP*8 + slack`: it always
// charged the strip window even when the hole absorbed it, and it never charged
// pass 1's frame at all, on the stated grounds that the frame "is freed before
// pass 2 allocates". Those two errors are close in size at n=16 — and every
// measurement ever taken here was at n >= 16, so they cancelled and the bound
// passed. Lower n to 2 and it fails at 2048x1536, the size this file called
// good; raise the area to 24MP and it fails the other way, at n=16.
//
// The correction is not "the old model broke at scale". It was never right; a
// single untested axis hid it. The comment it replaced already knew this failure
// mode by name — "a model that happens to hold because two errors point opposite
// ways is not a model" — which is worth more than the model it was attached to.
//
// Measured against the corrected model, all mode 2:
//
//    1024x768   x2     10.1 /   9.0 MB     6000x4000  x2    275.7 / 274.7 MB
//    1024x768   x4     10.1 /   9.0 MB     6000x4000  x16   275.7 / 274.7 MB
//    1024x768   x16    12.8 /  13.0 MB     8256x5504  x2    521.1 / 520.0 MB
//    1024x768   x32    16.9 /  18.5 MB     9504x6336  x2    690.2 / 689.1 MB
//    2048x1536  x2     37.1 /  36.0 MB
//    2048x1536  x16    37.1 /  39.0 MB
//    3000x2000  x2     69.7 /  68.7 MB
//    4000x3000  x2    138.4 / 137.3 MB
//    5000x3334  x2    191.8 / 190.8 MB
//
// Thirteen points spanning 0.79 to 60.22 Mpx and n from 2 to 32, every one
// within 1.9 MB. The model runs ~1.1 MB UNDER in the tall-frame regime (fixed
// overhead) and up to 1.9 MB OVER in the short-frame one (the real halo is a
// few rows, not the worst-case 24), so SLACK has to cover the under-shoot.
//
// The browser consequence is a straight read off the tall-frame column, since
// any real camera frame is far taller than 112*n: 24MP costs 276 MB and 60MP
// costs 690 MB, WHATEVER the sub count. Desktop tabs carry the first; mobile
// tabs are killed well below the last. Halving each dimension quarters it (a
// 24MP sensor's CFA planes are 3000x2000 -> 70 MB), which is why the colour
// path's superpixel output is the memory-viable browser shape and full-
// resolution mono is not — though the CFA path is CLI-only today, and loads the
// stack whole rather than streaming.
const STRIP = 64, MAX_HALO = 24, TILE = 256, WIN = STRIP + 2 * MAX_HALO;
const SLACK = 4 * 1048576;

const buf = readFileSync(inPath);
if (buf.subarray(0, 4).toString("latin1") !== "CSTK") throw new Error("bad magic");
const dv = new DataView(buf.buffer, buf.byteOffset);
const w = dv.getUint32(4, true), h = dv.getUint32(8, true), n = dv.getUint32(12, true);
const px = buf.subarray(16, 16 + w * h * n * 2);

let peakWasm = 0, peakRss = 0, result = null;
let memRef = null;
const sample = () => {
  if (memRef) peakWasm = Math.max(peakWasm, memRef.buffer.byteLength);
  peakRss = Math.max(peakRss, process.memoryUsage().rss);
};

const host = {
  read_rows(frame, row0, nrows, dst, dstOff, ctx) {
    memRef = ctx.memory;
    const f = Number(frame), r0 = Number(row0), nr = Number(nrows);
    const off = (f * w * h + r0 * w) * 2, len = nr * w * 2;
    new Uint8Array(ctx.memory.buffer, dst + Number(dstOff) * 2, len)
      .set(px.subarray(off, off + len));
    sample();
  },
  put_result(ptr, len, rw, rh, ctx) {
    memRef = ctx.memory;
    result = { w: Number(rw), h: Number(rh), bytes: Number(len) };
    sample();
  },
  progress() { sample(); },
};

const t0 = process.hrtime.bigint();
const { exports } = await instantiate(host);
const kept = Number(exports.stack_frames(BigInt(w), BigInt(h), BigInt(n), BigInt(mode)));
sample();
const secs = Number(process.hrtime.bigint() - t0) / 1e9;

const MB = (x) => (x / 1048576).toFixed(1);
const mpx = (w * h) / 1e6;
console.log(
  `${String(w).padStart(5)}x${String(h).padEnd(5)} x${n}  ${mpx.toFixed(2).padStart(5)} Mpx/frame  ` +
  `mode ${mode}  kept ${kept}/${n}  ` +
  `frames-in ${MB(w * h * n * 2).padStart(6)} MB  ` +
  `peak-wasm ${MB(peakWasm).padStart(6)} MB  ` +
  `peak-rss ${MB(peakRss).padStart(6)} MB  ` +
  `${secs.toFixed(1)}s` + (result ? "" : "  (NO RESULT)"),
);

if (assertModel) {
  const model = `w*h*10 + max(w*h*2, n*w*${WIN}*2 + n*${TILE}*${STRIP}*8)`;
  const bound =
    w * h * 10 + Math.max(w * h * 2, n * w * WIN * 2 + n * TILE * STRIP * 8) + SLACK;
  // Lower bound too, because an upper bound alone passes vacuously when a run
  // does nothing: the i64 accumulator ALONE is w*h*8, so any real stack must
  // clear that. This is the same discipline oracle.py applies when it fails a
  // clip that changed no pixels.
  //
  // Honest status: this is a FORWARD guard and no current input makes it fire —
  // every run that reaches here allocates the accumulator, so peak is ~w*h*12
  // and clears w*h*8 by half again. It is here to catch a future change that
  // makes the probe measure nothing (an early return, a mode that skips pass 2)
  // and report success, which the upper bound alone would wave through.
  const floor = w * h * 8;
  if (peakWasm > bound) {
    console.log(`  FAIL: peak ${MB(peakWasm)} MB exceeds the ${model} model ` +
                `+ slack (${MB(bound)} MB) — a buffer beyond the four the model ` +
                `names is live at peak`);
    process.exit(1);
  }
  if (peakWasm < floor) {
    console.log(`  FAIL: peak ${MB(peakWasm)} MB is below w*h*8 (${MB(floor)} MB), ` +
                `the accumulator alone — the run cannot have stacked anything`);
    process.exit(1);
  }
  console.log(`  peak within the memory model, ${model} ` +
              `(${MB(peakWasm)} of ${MB(bound)} MB)`);
}
if (!result) process.exit(1);
