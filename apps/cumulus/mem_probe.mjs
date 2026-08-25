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

// With `--assert-model`, fail if peak falls outside `[STRIP*w*8, bound]`, where
//
//   pass1 = w*(STRIP+6)*2 + 65536*8      strip buffer (+3-row halo) + histogram
//   pass2 = n*w*WIN*2 + n*TILE*STRIP*8   strip window + per-tile gather
//         + STRIP*w*10                   strip accumulator + strip rows out
//   bound = max(pass1, pass2) + SLACK
//
// THERE IS NO `w*h` TERM. Peak scales with frame WIDTH and sub count, never with
// frame HEIGHT or area — a 4000-row frame costs what a 768-row frame of the same
// width costs. Both passes stream now:
//
//   pass 1  registration reads a strip at a time. Clipped statistics need the
//           whole frame before the scan can begin, so the sub is walked twice —
//           once to build a 65536-bin histogram, once to detect. The histogram
//           is what holds that at TWO reads instead of six: the three clipping
//           rounds each need a sum and a variance, and they run over bins rather
//           than pixels. Detection strips carry a 3-row halo (the 3x3 maximum
//           test and the +/-3 centroid window both reach that far) and emit only
//           for their core rows, so no star is found twice.
//
//   pass 2  integration writes each strip out through `put_rows` as it
//           completes, so the finished image is assembled in the JS heap rather
//           than inside wasm — which is the point, because wasm32's 4 GiB
//           address space is the scarce one and the JS heap is not.
//
// Measured at 16 frames, across the three slices that got here:
//
//                    resident   output-streamed   both streamed
//    1024x768          12.8            6.8              6.0 MB
//    2048x1536         33.1            9.1              9.3 MB
//    3000x2000         58.3           12.8             11.8 MB
//    6016x4016 (24MP) 275.7           47.4             20.1 MB    <- 13.7x
//
// Thirty times the area between the first row and the last, and 3.3x the
// memory. What is left is linear in `w`, which is why the model has no area
// term to state.
//
// The `max` between passes is a wasm property rather than a program one: linear
// memory is a HIGH-WATER MARK and never returns pages, so pass 1's freed
// buffers leave a hole that pass 2's either fit inside — costing nothing — or
// do not. The two never add.
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
  const model = `max(pass1, pass2)`;
  const pass1 = w * (STRIP + 6) * 2 + 65536 * 8;
  const pass2 = n * w * WIN * 2 + n * TILE * STRIP * 8 + STRIP * w * 10;
  const bound = Math.max(pass1, pass2) + SLACK;
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
