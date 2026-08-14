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

// With `--assert-model`, fail if peak exceeds
// `w*h*10 + n*w*WIN*2 + n*TILE*STRIP*8 + SLACK`.
//
// Read the model term by term, because its SHAPE is the claim being made:
//
//   w*h*8          the i64 accumulator the stack integrates into — one per
//                  output pixel, and the largest single allocation
//   w*h*2          the 16-bit result handed to the page, live at the same time
//   n*w*WIN*2      the strip window: `WIN = STRIP + 2*MAX_HALO` rows of every
//                  frame at once
//   n*TILE*STRIP*8 the per-tile gather inside `integrate_window` — every kept
//                  frame's resampled copy of one tile, as i64. Tiles are 256
//                  wide but a strip caps them at STRIP rows, so this is 128 KiB
//                  per frame however large the frames are.
//
// What is ABSENT is the point: there is no `n*w*h` term at all. Both `n` terms
// are independent of frame HEIGHT — a strip is a strip whether the frame is 768
// rows or 4000 — so the per-sub bound is `w*224 + 128 KiB`: 357 KiB at 1024
// wide, 587 KiB at 2048, ~1.5 MB at 6000. Adding subs is linear in frame WIDTH
// rather than area, which is what turns "the device decides how many subs" into
// "your patience decides". Pass 1's one resident frame (`w*h*2`) is not in the
// bound because it is freed before pass 2 allocates; the model asserts that the
// two peaks do not overlap, and the measurements below confirm it.
//
// The tile term was MISSING from the first version of this model, and the miss
// was nearly invisible: at 1024x768 x16 the bound came out 33% above the real
// peak anyway, because the window term assumes the worst-case halo and the real
// one is a few rows. It only showed up at x64, where the bound landed 0.8%
// above the measurement — a check about to start failing for a correct program.
// A model that happens to hold because two errors point opposite ways is not a
// model; every term here is one the code actually allocates.
//
// SLACK came down from 18 MB to 4 MB with this slice, which is a real tightening
// rather than bookkeeping: fixed overhead measures well under 1 MB, so 18 MB
// used to be a bigger allowance than most of the peaks it guarded. Measured
// peak against the bound, all mode 2:
//
//     512x512  x16    6.6 / 10.3 MB
//    1024x768  x16   12.8 / 17.0 MB
//    1024x768  x64   25.3 / 33.5 MB
//   2048x1536  x16   37.1 / 43.0 MB
//   2048x1536  x32   39.8 / 52.0 MB
//
// — 14-36% below the bound, tightest on the widest frame, and that margin is
// genuine rather than luck: at 2048x1536 x16 the measurement is 1.9 MB under
// the model even BEFORE slack, because the real halo is a few rows rather than
// the worst-case 24 the window term assumes. The resident predecessor's 39.6 MB
// at 1024x768 x16 is rejected by more than 2x.
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
  const model = `w*h*10 + n*w*${WIN}*2 + n*${TILE}*${STRIP}*8`;
  const bound = w * h * 10 + n * w * WIN * 2 + n * TILE * STRIP * 8 + SLACK;
  if (peakWasm > bound) {
    console.log(`  FAIL: peak ${MB(peakWasm)} MB exceeds the ${model} model ` +
                `+ slack (${MB(bound)} MB) — something now scales with frames x area`);
    process.exit(1);
  }
  console.log(`  peak within the streaming memory model, ${model} ` +
              `(${MB(peakWasm)} of ${MB(bound)} MB)`);
}
if (!result) process.exit(1);
