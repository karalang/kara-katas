// Veil regression harness — pure-node, end-to-end through the real wasm.
// `process(op, sw, sh, x, y, w, h, s)`: op 0 pixelate (s=block), 1 blur
// (s=radius), 2 bar (s=0 black / 1 white).
import { instantiate } from "./veil.js";
import { readFileSync } from "node:fs";

const bytes = readFileSync(new URL("./veil.wasm", import.meta.url));

let srcPixels = null, out = null;
const host = {
  read_src(dst, len, ctx) {
    new Uint8Array(ctx.memory.buffer, Number(dst), Number(len))
      .set(srcPixels.subarray(0, Number(len)));
  },
  put_pixels(ptr, len, w, h, ctx) {
    out = new Uint8Array(ctx.memory.buffer, Number(ptr), Number(len)).slice();
  },
};
const handle = await instantiate(host, { bytes });
const run = (op, sw, sh, x, y, w, h, s, src) => {
  srcPixels = src; out = null;
  handle.exports.process(BigInt(op), BigInt(sw), BigInt(sh),
    BigInt(x), BigInt(y), BigInt(w), BigInt(h), BigInt(s));
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

// ── 1. pixelate: 4x2, rect (0,0,2,2), block 2 → tile avg; outside untouched ──
// r-values in the tile: 10, 20, 30, 40 → avg (100/4) = 25.
{
  const px = (r) => [r, r, r, 255];
  const src = new Uint8Array([].concat(
    px(10), px(20), px(200), px(201),
    px(30), px(40), px(202), px(203)));
  const got = run(0, 4, 2, 0, 0, 2, 2, 2, src);
  const e = [].concat(
    px(25), px(25), px(200), px(201),
    px(25), px(25), px(202), px(203));
  check("pixelate 2x2 tile avg, outside untouched", got, e);
}

// ── 2. bar: black + white fills, alpha forced opaque, outside untouched ─────
{
  const src = new Uint8Array([10, 20, 30, 128, 40, 50, 60, 128]);
  check("bar black rect(0,0,1,1)", run(2, 2, 1, 0, 0, 1, 1, 0, src),
    [0, 0, 0, 255, 40, 50, 60, 128]);
  check("bar white rect(1,0,1,1)", run(2, 2, 1, 1, 0, 1, 1, 1, src),
    [10, 20, 30, 128, 255, 255, 255, 255]);
}

// ── 3. blur: solid region is invariant; outside untouched (self-contained) ──
{
  const src = new Uint8Array([
    77, 77, 77, 255, 77, 77, 77, 255, 9, 9, 9, 255,
    77, 77, 77, 255, 77, 77, 77, 255, 9, 9, 9, 255,
  ]); // 3x2: solid 77 in left 2x2, distinct right column
  const got = run(1, 3, 2, 0, 0, 2, 2, 1, src);
  check("blur solid 2x2 rect invariant + outside untouched", got, [...src]);
}

// ── 4. blur: exact 3-pass integer trace on a 3x1 rect, radius 1 ─────────────
// start [90,0,0] → p1 [45,30,0] → p2 [37,25,15] → p3 [31,25,20]
// (each pass: h box (edge-normalized, integer div) then v box (identity, h=1)).
{
  const src = new Uint8Array([90, 90, 90, 255, 0, 0, 0, 255, 0, 0, 0, 255]);
  const got = run(1, 3, 1, 0, 0, 3, 1, 1, src);
  const e = [31, 31, 31, 255, 25, 25, 25, 255, 20, 20, 20, 255];
  check("blur exact 3-pass trace [90,0,0] -> [31,25,20]", got, e);
}

console.log(failures === 0 ? "\nALL PASS ✅" : `\n${failures} FAILURE(S) ❌`);
process.exit(failures === 0 ? 0 : 1);
