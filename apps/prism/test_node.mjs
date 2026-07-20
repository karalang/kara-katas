// Prism regression harness — pure-node, end-to-end through the real wasm:
// instantiate prism.wasm with mock host fns, feed known pixels, call the
// `process(op, sw, sh, dw, dh)` export, assert exact output bytes.
//
// Ops: 0 = grayscale, 1 = bilinear resize, 2 = lanczos3 resize.
import { instantiate } from "./prism.js";
import { readFileSync } from "node:fs";

const bytes = readFileSync(new URL("./prism.wasm", import.meta.url));

let srcPixels = null;
let out = null, outW = 0, outH = 0;

const host = {
  read_src(dst, len, ctx) {
    new Uint8Array(ctx.memory.buffer, Number(dst), Number(len))
      .set(srcPixels.subarray(0, Number(len)));
  },
  put_pixels(ptr, len, w, h, ctx) {
    out = new Uint8Array(ctx.memory.buffer, Number(ptr), Number(len)).slice();
    outW = Number(w); outH = Number(h);
  },
};

const handle = await instantiate(host, { bytes });
const run = (op, sw, sh, dw, dh, src) => {
  srcPixels = src; out = null;
  handle.exports.process(BigInt(op), BigInt(sw), BigInt(sh), BigInt(dw), BigInt(dh));
  return out;
};

let failures = 0;
function check(name, got, expected) {
  const ok = got && got.length === expected.length && expected.every((v, i) => v === got[i]);
  console.log(`${ok ? "PASS ✅" : "FAIL ❌"}  ${name}`);
  if (!ok) {
    console.log("  got     :", JSON.stringify(got ? [...got] : null));
    console.log("  expected:", JSON.stringify(expected));
    failures++;
  }
}

// ── 1. grayscale (op 0): red -> 76, green -> 150 (Rec.601 int), alpha kept ──
{
  const src = new Uint8Array([255, 0, 0, 255, 0, 255, 0, 255]);
  const got = run(0, 2, 1, 2, 1, src);
  check("grayscale 2x1", got, [76, 76, 76, 255, 150, 150, 150, 255]);
}

// ── 2. bilinear (op 1) 2x1 -> 4x1 of black|white ────────────────────────────
// Pixel-center alignment, xs = 0.5:
//   dx=0: fx=-0.25 -> clamp x0=0, tx=0        -> 0
//   dx=1: fx= 0.25 -> tx=0.25 -> 63.75 + .5   -> 64
//   dx=2: fx= 0.75 -> tx=0.75 -> 191.25 + .5  -> 191
//   dx=3: fx= 1.25 -> x0=1 clamp x1=1         -> 255
{
  const src = new Uint8Array([0, 0, 0, 255, 255, 255, 255, 255]);
  const got = run(1, 2, 1, 4, 1, src);
  const e = [];
  for (const v of [0, 64, 191, 255]) e.push(v, v, v, 255);
  check("bilinear 2x1 -> 4x1 gradient", got, e);
  if (outW !== 4 || outH !== 1) { console.log("FAIL ❌  bilinear out dims", outW, outH); failures++; }
}

// ── 3. bilinear identity: same-size resize must be exact ────────────────────
{
  const src = new Uint8Array([10, 20, 30, 255, 200, 150, 100, 128]);
  const got = run(1, 2, 1, 2, 1, src);
  check("bilinear identity 2x1 -> 2x1", got, [...src]);
}

// ── 4. lanczos (op 2) constant-image invariance ─────────────────────────────
// Weights are normalized by wsum, so a solid image must resize to exactly
// itself at any scale — up (3x3 -> 6x6) and down (6x6 -> 2x2).
{
  const solid = (w, h, rgba) => {
    const a = new Uint8Array(w * h * 4);
    for (let i = 0; i < w * h; i++) a.set(rgba, i * 4);
    return a;
  };
  const up = run(2, 3, 3, 6, 6, solid(3, 3, [100, 150, 200, 255]));
  check("lanczos solid 3x3 -> 6x6", up, [...solid(6, 6, [100, 150, 200, 255])]);
  const down = run(2, 6, 6, 2, 2, solid(6, 6, [7, 77, 177, 255]));
  check("lanczos solid 6x6 -> 2x2", down, [...solid(2, 2, [7, 77, 177, 255])]);
}

// ── 5. lanczos step-edge behavior ───────────────────────────────────────────
// A left-black / right-white 4x1 upscaled 2x. True Lanczos properties:
//   * symmetry: out[i] + out[7-i] == 255 (the filter is symmetric);
//   * bounded ringing at the ends: windowed-sinc negative lobes cause slight
//     overshoot near a step edge (this is textbook Lanczos, NOT a bug — the
//     ends need not be pinned to 0/255), but it must stay small;
//   * the edge transition happens at the middle: out[3] < 128 <= out[4].
{
  const src = new Uint8Array([0,0,0,255, 0,0,0,255, 255,255,255,255, 255,255,255,255]);
  const got = run(2, 4, 1, 8, 1, src);
  let ok = !!got;
  if (got) {
    for (let i = 0; i < 4; i++) {
      if (got[i * 4] + got[(7 - i) * 4] !== 255) ok = false;   // symmetry
    }
    if (got[0] > 32 || got[7 * 4] < 223) ok = false;           // ringing bounded
    if (!(got[3 * 4] < 128 && got[4 * 4] >= 128)) ok = false;  // edge at middle
  }
  console.log(`${ok ? "PASS ✅" : "FAIL ❌"}  lanczos 4x1 -> 8x1 step edge (symmetry + bounded ringing)`);
  if (!ok) { console.log("  got:", got ? [...got] : null); failures++; }
}

console.log(failures === 0 ? "\nALL PASS ✅" : `\n${failures} FAILURE(S) ❌`);
process.exit(failures === 0 ? 0 : 1);
