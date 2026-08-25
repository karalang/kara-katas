// test_node.mjs — end-to-end check of the wasm boundary.
//
// Instantiates cumulus.wasm with real host fns, feeds it the same stack the CLI
// gets, and requires the result to be BYTE-IDENTICAL to what the native binary
// produced. That is the bar the other backends already meet — AOT, interpreter
// and numpy all agree exactly — and there is no reason wasm should be held to a
// looser one: it is the same kernels, compiled for a different target.
//
// This exercises the host-FFI-in -> kernel -> host-FFI-out path specifically,
// which is where Prism found the wasm `karac_free_buf` ABI bug (compiler ledger
// B-2026-07-20-10). A page that merely "looks right" would not have caught it.
//
// Usage: node test_node.mjs <in.cstack> <native_mean.cstack> <native_stack.cstack>

import { readFileSync } from "node:fs";
import { instantiate } from "./cumulus.js";

const [inPath, meanPath, stackPath] = process.argv.slice(2);
if (!inPath || !meanPath || !stackPath) {
  console.error("usage: node test_node.mjs <in.cstack> <native_mean.cstack> <native_stack.cstack>");
  process.exit(2);
}

function readStack(path) {
  const buf = readFileSync(path);
  if (buf.subarray(0, 4).toString("latin1") !== "CSTK") throw new Error(`${path}: bad magic`);
  const dv = new DataView(buf.buffer, buf.byteOffset);
  const w = dv.getUint32(4, true), h = dv.getUint32(8, true), n = dv.getUint32(12, true);
  return { w, h, n, px: buf.subarray(16, 16 + w * h * n * 2) };
}

const src = readStack(inPath);
const want = { mean: readStack(meanPath), stack: readStack(stackPath) };

let result = null;
const progressCalls = [];

// Rows served straight out of the `.cstack`, which is already frame-major
// little-endian u16 — so this host is a pure address calculation with no decode,
// and any divergence from native is the wasm build's, not the harness's.
//
// Serving ROWS rather than the whole stack is also the only way this file can
// still stand in for the page: the browser's read_rows is answered from a Blob
// by FileReaderSync, which node has no equivalent of, so what the two hosts
// share is the request pattern, not the mechanism.
const rowsRead = [];
const host = {
  read_rows(frame, row0, nrows, dst, dstOff, ctx) {
    const f = Number(frame), r0 = Number(row0), nr = Number(nrows);
    if (f < 0 || f >= src.n) throw new Error(`read_rows: frame ${f} out of range`);
    if (r0 < 0 || r0 + nr > src.h) throw new Error(`read_rows: rows ${r0}..${r0 + nr} out of range`);
    const off = (f * src.w * src.h + r0 * src.w) * 2, len = nr * src.w * 2;
    rowsRead.push(nr);
    new Uint8Array(ctx.memory.buffer, dst + Number(dstOff) * 2, len)
      .set(src.px.subarray(off, off + len));
  },
  put_rows(ptr, len, row0, nrows, w, h, ctx) {
    // Streamed: one call per strip, assembled here as BYTES (this file compares
    // against the native .cstack byte for byte, so it keeps the wire form).
    const W = Number(w), H = Number(h), r0 = Number(row0), n = Number(nrows);
    if (!result) result = { w: W, h: H, px: new Uint8Array(W * H * 2) };
    result.px.set(new Uint8Array(ctx.memory.buffer, ptr, Number(len)), r0 * W * 2);
  },
  progress(stage, done, total) {
    progressCalls.push([Number(stage), Number(done), Number(total)]);
  },
};

const MODES = [
  { name: "mean", mode: 0, want: want.mean, expectKept: src.n },
  { name: "stack", mode: 2, want: want.stack, expectKept: src.n },
];

let failures = 0;
for (const m of MODES) {
  result = null;
  progressCalls.length = 0;
  rowsRead.length = 0;
  const { exports } = await instantiate(host);
  const kept = Number(
    exports.stack_frames(BigInt(src.w), BigInt(src.h), BigInt(src.n), BigInt(m.mode)),
  );

  if (!result) {
    console.log(`  ${m.name.padEnd(6)} FAIL: put_result never called`);
    failures++;
    continue;
  }
  if (result.w !== m.want.w || result.h !== m.want.h) {
    console.log(`  ${m.name.padEnd(6)} FAIL: got ${result.w}x${result.h}, want ${m.want.w}x${m.want.h}`);
    failures++;
    continue;
  }
  if (kept !== m.expectKept) {
    console.log(`  ${m.name.padEnd(6)} FAIL: kept ${kept}, want ${m.expectKept}`);
    failures++;
    continue;
  }

  let diff = 0, firstAt = -1, gotV = 0, wantV = 0;
  for (let i = 0; i < m.want.px.length; i++) {
    if (result.px[i] !== m.want.px[i]) {
      if (firstAt < 0) {
        firstAt = i >> 1;
        gotV = result.px[i & ~1] | (result.px[(i & ~1) + 1] << 8);
        wantV = m.want.px[i & ~1] | (m.want.px[(i & ~1) + 1] << 8);
      }
      diff++;
    }
  }
  if (diff === 0) {
    console.log(`  ${m.name.padEnd(6)} byte-identical to native over ${m.want.px.length / 2} pixels`);
  } else {
    console.log(`  ${m.name.padEnd(6)} FAIL: ${diff} bytes differ; first pixel ${firstAt} wasm ${gotV} vs native ${wantV}`);
    failures++;
  }

  // The page relies on these to drive its progress bar; a silent regression
  // there turns a working stack into one that looks hung.
  const stages = new Set(progressCalls.map((c) => c[0]));
  const wantStages = m.mode === 2 ? [0, 1, 2] : [0, 2];
  for (const st of wantStages) {
    if (!stages.has(st)) {
      console.log(`  ${m.name.padEnd(6)} FAIL: no progress tick for stage ${st}`);
      failures++;
    }
  }

  // The point of the whole slice is that the module asks for STRIPS, not for
  // whole frames — the page can only hold handles instead of pixels because
  // that is true. Byte-identity alone would still pass if a future change went
  // back to pulling every row of every frame in one call, so the request shape
  // is asserted directly: pass 2 must never ask for more than a strip plus its
  // halo, and the only full-height reads allowed are pass 1's, one per frame.
  const maxStrip = 64 + 2 * 24; // STRIP + 2*MAX_HALO, from cumulus.kara
  const biggest = Math.max(...rowsRead);
  if (src.h <= maxStrip) {
    // A frame no taller than one strip is read whole no matter what the module
    // does, so this stack cannot tell streaming from not-streaming. Say so
    // rather than print a pass: verify.sh runs a second, taller stack for the
    // assertion below to mean anything.
    console.log(`  ${m.name.padEnd(6)} ${rowsRead.length} row-range reads ` +
                `(${src.h} rows fits one strip — streaming shape not exercised)`);
  } else {
    // Pass 1 reads each frame whole to find its stars; pass 2 must never ask
    // for more than a strip plus its halo. Byte-identity alone would still pass
    // if a future change went back to pulling everything in one call, so the
    // request shape is asserted directly.
    const whole = rowsRead.filter((r) => r === src.h).length;
    const allowedWhole = m.mode === 2 ? src.n : 0;
    const tooBig = rowsRead.filter((r) => r !== src.h && r > maxStrip).length;
    if (tooBig > 0 || whole > allowedWhole) {
      console.log(`  ${m.name.padEnd(6)} FAIL: ${whole} whole-frame and ${tooBig} oversized reads ` +
                  `(at most ${allowedWhole} whole-frame, none over ${maxStrip} rows)`);
      failures++;
    } else {
      console.log(`  ${m.name.padEnd(6)} streamed: ${rowsRead.length} row-range reads, ` +
                  `largest ${biggest} of ${src.h} rows`);
    }
  }
}

console.log(failures === 0 ? "PASS" : "FAIL");
process.exit(failures === 0 ? 0 : 1);
