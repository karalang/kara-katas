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
// Reports peak wasm memory and peak node RSS. RSS is the looser bound (it also
// carries the host-side copy of the frames), so a phone must fit the wasm figure
// and a phone loading files through the page must fit something closer to RSS.

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

// With `--assert-model`, fail if peak exceeds `w*h*(2n+8) + SLACK`: one u16 copy
// of the frames plus the i64 output, and nothing else that scales with the
// input. SLACK covers the module, the shadow stack and allocator rounding —
// costs that do not grow with the frames.
//
// The bound is set from both sides at the 1024x768 x16 size `build_web.sh` runs
// it at, and both sides were MEASURED, not estimated: this code peaks at
// 39.6 MB, and the predecessor that kept a second full copy of the frames
// (`w*h*(4n+8)`) peaks at 63.6 MB — rebuilt from git and run against this check
// to confirm it does fail. The resulting 48.0 MB bound leaves 17% headroom above
// the real figure while rejecting the duplicate by 33%. Tighter would flake on
// allocator noise; looser would let the regression back through.
const SLACK = 18 * 1048576;

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
  read_frames(dst, len, ctx) {
    memRef = ctx.memory;
    new Uint8Array(ctx.memory.buffer, dst, Number(len)).set(px);
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
  const bound = w * h * (2 * n + 8) + SLACK;
  if (peakWasm > bound) {
    console.log(`  FAIL: peak ${MB(peakWasm)} MB exceeds the w*h*(2n+8) model ` +
                `+ slack (${MB(bound)} MB) — something now scales with the input twice`);
    process.exit(1);
  }
  console.log(`  peak within the w*h*(2n+8) memory model (${MB(peakWasm)} of ${MB(bound)} MB)`);
}
if (!result) process.exit(1);
