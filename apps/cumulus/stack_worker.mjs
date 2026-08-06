// stack_worker.mjs — run the wasm stack off the main thread.
//
// `stack_frames` is a single synchronous wasm call that runs for as long as the
// stack takes: ~40 s for a 3 Mpx x16 set, and longer on a phone. Called from the
// page's own thread it blocks every repaint, so the progress ticks it emits
// update the DOM but never reach the screen, and the browser eventually offers
// to kill the "unresponsive" page. The bar was, on mobile, decorative.
//
// A worker fixes both halves: the main thread stays free to repaint, so the bar
// actually animates, and the long call is no longer a main-thread stall.
//
// Nothing about the numerics lives here. The worker owns the host FFI and the
// message plumbing only — the same three host fns the CLI-equivalent path uses,
// with `progress` forwarded as a message instead of touching the DOM directly
// (a worker has no DOM).

import { instantiate } from "./cumulus.js";

let blob = null;   // the concatenated LE-u16 frame bytes, staged for read_frames
let result = null; // set by put_result before stack_frames returns

const host = {
  read_frames(dst, len, ctx) {
    new Uint8Array(ctx.memory.buffer, dst, Number(len)).set(blob);
  },
  put_result(ptr, len, w, h, ctx) {
    // Copy out immediately — the pointer is only valid until wasm reclaims it.
    const raw = new Uint8Array(ctx.memory.buffer, ptr, Number(len)).slice();
    result = { w: Number(w), h: Number(h), px: new Uint16Array(raw.buffer) };
  },
  progress(stage, done, total) {
    postMessage({ t: "progress", stage: Number(stage), done: Number(done), total: Number(total) });
  },
};

self.onmessage = async (e) => {
  const { blob: buf, w, h, n, mode } = e.data;
  blob = new Uint8Array(buf);
  result = null;
  try {
    const { exports } = await instantiate(host);
    const kept = Number(exports.stack_frames(BigInt(w), BigInt(h), BigInt(n), BigInt(mode)));
    // Drop the staged input before shipping the result back: on a large stack
    // this copy is the single biggest allocation in the worker, and holding it
    // through the postMessage would keep the peak high for no reason.
    blob = null;
    if (!result) throw new Error("stack_frames returned without calling put_result");
    postMessage({ t: "done", kept, w: result.w, h: result.h, px: result.px }, [result.px.buffer]);
    result = null;
  } catch (err) {
    blob = null;
    postMessage({ t: "error", message: String((err && err.message) || err) });
  }
};
