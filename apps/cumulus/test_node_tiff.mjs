// test_node_tiff.mjs — the browser TIFF path against native, byte for byte.
//
// tiff.mjs is a SECOND implementation of the TIFF spec, racing the Kāra one in
// cumulus.kara. Two independent decoders of the same container is exactly the
// arrangement where a subtle disagreement — a strip offset, a sample stride, a
// byte order — hides for months, because each one is self-consistent and the
// page still paints something.
//
// So this feeds real TIFF files through the JS reader into the wasm module and
// demands the result equal what the native binary produced from the SAME files.
// It covers the RGB path specifically, where the two readers have the most room
// to disagree: three interleaved samples, a plane argument, and a median
// luminance computed on the JS side.
//
// Usage: node test_node_tiff.mjs <tiffdir> <native_stack.cstack> [planes]

import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { instantiate } from "./cumulus.js";
import { decodeInto, mismatch, readSubHeader, rowRanges } from "./subs.mjs";

const [dir, wantPath, planesArg] = process.argv.slice(2);
if (!dir || !wantPath) {
  console.error("usage: node test_node_tiff.mjs <tiffdir> <native_stack.cstack> [planes]");
  process.exit(2);
}

const files = readdirSync(dir).filter((f) => /\.tiff?$/i.test(f)).sort();
if (!files.length) { console.error(`no TIFF files in ${dir}`); process.exit(2); }

// Resident here because node has no FileReaderSync — the worker reads these
// ranges off a Blob instead. What the two hosts share is the request pattern
// and the decoder, which is what this file is checking; the mechanism differs
// and is checked by verify_browser.mjs in a real browser.
const raw = files.map((f) => new Uint8Array(readFileSync(join(dir, f))));
const metas = [];
for (const bytes of raw) metas.push(await readSubHeader(new Blob([bytes])));
const why = mismatch(metas);
if (why) { console.error(`fixture is not one stack: ${why}`); process.exit(2); }

const { w, h, spp } = metas[0];
const n = files.length;
const planes = planesArg ? Number(planesArg) : spp;

const want = (() => {
  const buf = readFileSync(wantPath);
  if (buf.subarray(0, 4).toString("latin1") !== "CSTK") throw new Error(`${wantPath}: bad magic`);
  const dv = new DataView(buf.buffer, buf.byteOffset);
  const W = dv.getUint32(4, true), H = dv.getUint32(8, true), P = dv.getUint32(12, true);
  return { w: W, h: H, planes: P, px: buf.subarray(16, 16 + W * H * P * 2) };
})();

let result = null;
const planesSeen = new Set();
const host = {
  read_rows(frame, plane, row0, nrows, dst, dstOff, ctx) {
    const i = Number(frame), m = metas[i], src = raw[i];
    const r0 = Number(row0), nr = Number(nrows), pl = Number(plane);
    planesSeen.add(pl);
    const out = new Uint16Array(ctx.memory.buffer, dst + Number(dstOff) * 2, nr * m.w);
    for (const run of rowRanges(m, r0, nr)) {
      if (run.start + run.length > src.length) {
        throw new Error(`frame ${i}: rows ${r0}..${r0 + nr} run past the end of the file`);
      }
      decodeInto(src.subarray(run.start, run.start + run.length), out, run.row * m.w, m, pl, run.rows);
    }
  },
  put_rows(ptr, len, plane, row0, nrows, rw, rh, ctx) {
    const W = Number(rw), H = Number(rh), r0 = Number(row0), nr = Number(nrows);
    const pl = Number(plane);
    if (!result) result = { w: W, h: H, planes, px: new Uint8Array(W * H * planes * 2) };
    result.px.set(new Uint8Array(ctx.memory.buffer, ptr, Number(len)),
                  (pl * W * H + r0 * W) * 2);
  },
  progress() {},
};

const { exports } = await instantiate(host);
const kept = Number(exports.stack_frames(
  BigInt(w), BigInt(h), BigInt(n), BigInt(planes), 2n, 0n, 0n));

let failures = 0;
const label = `${planes === 3 ? "RGB" : "mono"} ${metas[0].bits}-bit ${metas[0].big ? "MM" : "II"}`;
if (!result) {
  console.log(`  ${label}: FAIL — no rows emitted`);
  failures++;
} else if (result.w !== want.w || result.h !== want.h || result.planes !== want.planes) {
  console.log(`  ${label}: FAIL — got ${result.w}x${result.h}x${result.planes}, ` +
              `want ${want.w}x${want.h}x${want.planes}`);
  failures++;
} else {
  let diff = 0, firstAt = -1;
  for (let i = 0; i < want.px.length; i++) {
    if (result.px[i] !== want.px[i]) { if (firstAt < 0) firstAt = i >> 1; diff++; }
  }
  if (diff === 0) {
    console.log(`  ${label}: byte-identical to native over ${want.px.length / 2} samples ` +
                `(${kept}/${n} registered)`);
  } else {
    console.log(`  ${label}: FAIL — ${diff} bytes differ, first at sample ${firstAt}`);
    failures++;
  }
}

// The plane argument must actually be USED. A module that ignored it, or a host
// that answered every request from plane 0, would produce a grey image in three
// identical planes — which is a valid stack of the right size, and which the
// comparison above would catch only because native disagrees. Asserting the
// request shape catches it directly, and catches the reverse too: a mono run
// that started asking for planes it does not have.
const wantPlanes = planes === 3 ? [-1, 0, 1, 2] : [-1, 0];
const missing = wantPlanes.filter((p) => !planesSeen.has(p));
if (missing.length) {
  console.log(`  ${label}: FAIL — never requested plane(s) ${missing.join(", ")}`);
  failures++;
}
const extra = [...planesSeen].filter((p) => !wantPlanes.includes(p));
if (extra.length) {
  console.log(`  ${label}: FAIL — requested plane(s) ${extra.join(", ")} that do not exist`);
  failures++;
}

console.log(failures === 0 ? "PASS" : "FAIL");
process.exit(failures === 0 ? 0 : 1);
