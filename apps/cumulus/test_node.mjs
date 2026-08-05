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

const host = {
  read_frames(dst, len, ctx) {
    const n = Number(len);
    if (n !== src.px.length) throw new Error(`read_frames wants ${n}, have ${src.px.length}`);
    new Uint8Array(ctx.memory.buffer, dst, n).set(src.px);
  },
  put_result(ptr, len, w, h, ctx) {
    // Copy out immediately — the pointer is only valid until wasm reclaims it.
    result = {
      w: Number(w),
      h: Number(h),
      px: new Uint8Array(ctx.memory.buffer, ptr, Number(len)).slice(),
    };
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
}

console.log(failures === 0 ? "PASS" : "FAIL");
process.exit(failures === 0 ? 0 : 1);
