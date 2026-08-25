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
// `[STRIP*w*8, max(w*h*2, strip) + STRIP*w*10 + SLACK]`.
//
// Read the model term by term, because its SHAPE is the claim being made:
//
//   STRIP*w*8   the i64 accumulator — ONE STRIP tall, not one frame
//   STRIP*w*2   the 16-bit rows handed to the host, likewise one strip
//   max(...)    EITHER pass 1's resident frame (`w*h*2`) OR the pass-2 strip
//               window plus per-tile gather, whichever is LARGER — never both
//
// OUTPUT STREAMING removed the two `w*h` terms that used to dominate. The
// accumulator was `w*h*8` and the result `w*h*2`; both are now `STRIP` rows.
// `put_rows` hands each strip to the host as it completes, so the finished
// image is assembled in the JS heap instead of inside wasm — which is the whole
// point, because wasm32's 4 GiB address space is the scarce one and the JS heap
// is not. Measured, at 16 frames:
//
//     1024x768     12.8 ->   6.8 MB
//     2048x1536    33.1 ->   9.1 MB
//     3000x2000    58.3 ->  12.8 MB
//     6016x4016   275.7 ->  47.4 MB     <- 24 MP, 5.8x less
//
// What REMAINS proportional to `w*h` is pass 1's resident frame, `w*h*2`, and
// at 24 MP that is 46 of the 47 MB. Star detection needs global background
// statistics before it can scan, so the frame is read whole; splitting
// `detect_stars` into a statistics pass and a scan pass would strip that too,
// at the cost of reading each sub twice in pass 1. That is the next lever, and
// after this slice it is the ONLY `w*h` term left.
//
// The `max` is a wasm property, not a program one: linear memory is a
// HIGH-WATER MARK and never returns pages, so pass 1's freed frame leaves a
// hole that pass 2's window either fits inside (costing nothing) or does not.
// They never add.
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
  put_rows(ptr, len, row0, nrows, rw, rh, ctx) {
    // One call per strip now. The probe does not assemble the image — it only
    // measures the WASM heap, and assembling here would add a JS-side buffer
    // that has nothing to do with the number being measured.
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
  const model = `max(w*h*2, n*w*${WIN}*2 + n*${TILE}*${STRIP}*8) + ${STRIP}*w*10`;
  const bound =
    Math.max(w * h * 2, n * w * WIN * 2 + n * TILE * STRIP * 8) + STRIP * w * 10 + SLACK;
  const floor = STRIP * w * 8;
  if (peakWasm > bound) {
    console.log(`  FAIL: peak ${MB(peakWasm)} MB exceeds the ${model} model ` +
                `+ slack (${MB(bound)} MB) — a buffer beyond the four the model ` +
                `names is live at peak`);
    process.exit(1);
  }
  if (peakWasm < floor) {
    console.log(`  FAIL: peak ${MB(peakWasm)} MB is below STRIP*w*8 (${MB(floor)} MB), ` +
                `the strip accumulator alone — the run cannot have stacked anything`);
    process.exit(1);
  }
  console.log(`  peak within the memory model, ${model} ` +
              `(${MB(peakWasm)} of ${MB(bound)} MB)`);
}
if (!result) process.exit(1);
