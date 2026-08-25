// test_node_threaded.mjs — the THREADED module must equal native, byte for byte.
//
// test_node.mjs covers the sequential module. It cannot cover this one: it calls
// `instantiate`, which always loads `cumulus.wasm`. The threaded module is a
// different binary with a different scheduler, and it is the one the page runs.
//
// What this exists to catch is a RACE. Eighteen workers write disjoint tiles of
// one output buffer; if the disjointness proof were ever wrong, the damage would
// be a handful of wrong pixels, not a crash — indistinguishable from a correct
// run unless something compares against a known-good reference.
//
// So it runs REPEATEDLY. A race need not show on every execution, and a single
// green run proves much less than a green run repeated: scheduling has to land
// the wrong way before anything is visible.
//
// Usage: node test_node_threaded.mjs <in.cstack> <native_ref.cstack> [mode] [reps]

import { readFileSync } from "node:fs";
import { instantiateThreaded } from "./cumulus.js";
const [inPath, refPath, modeArg, reps] = process.argv.slice(2);
const rd = p => { const b = readFileSync(p); const d = new DataView(b.buffer, b.byteOffset);
  return { w: d.getUint32(4,true), h: d.getUint32(8,true), n: d.getUint32(12,true), px: b.subarray(16) }; };
const src = rd(inPath), want = rd(refPath);
let bad = 0;
for (let r = 0; r < Number(reps ?? 5); r++) {
  let result = null;
  const host = {
    read_rows(frame,row0,nrows,dst,dstOff,ctx){
      const f=Number(frame),r0=Number(row0),nr=Number(nrows);
      const off=(f*src.w*src.h+r0*src.w)*2, len=nr*src.w*2;
      new Uint8Array(ctx.memory.buffer,dst+Number(dstOff)*2,len).set(src.px.subarray(off,off+len));
    },
    put_result(ptr,len,w,h,ctx){ result={w:Number(w),h:Number(h),
      px:new Uint8Array(ctx.memory.buffer,ptr,Number(len)).slice()}; },
    progress(){},
  };
  const hd = await instantiateThreaded(host);
  await hd.exports.stack_frames(BigInt(src.w),BigInt(src.h),BigInt(src.n),BigInt(modeArg??2));
  await hd.terminate?.();
  if (!result) { console.log(`run ${r}: NO RESULT`); bad++; continue; }
  const wantPx = want.px.subarray(0, result.px.length);
  let diff = 0, first = -1;
  for (let i=0;i<wantPx.length;i++) if (result.px[i]!==wantPx[i]) { if(first<0) first=i; diff++; }
  console.log(diff===0 ? `run ${r}: threaded=${hd.threaded} byte-identical (${wantPx.length/2} px)`
                       : `run ${r}: threaded=${hd.threaded} ${diff} BYTES DIFFER, first at ${first}`);
  if (diff) bad++;
}
console.log(bad===0 ? "PASS" : "FAIL");
process.exit(bad===0?0:1);
