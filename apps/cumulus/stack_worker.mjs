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
// Streaming gave the worker a SECOND, independent reason to exist. `read_rows`
// is synchronous — it has to be, since it is called from inside a wasm frame —
// and a Blob is normally readable only asynchronously. `FileReaderSync` is the
// one API that reads a Blob synchronously, and it exists ONLY in workers. So the
// page can hold file handles instead of decoded pixels precisely because the
// stack runs here; on the main thread the same design is impossible, which is
// why the inline fallback has to pre-read the files.
//
// Nothing about the numerics lives here. The worker owns the host FFI and the
// message plumbing only — with `progress` forwarded as a message instead of
// touching the DOM directly (a worker has no DOM), and the FITS decoding
// delegated to fits.mjs, which the page shares.

import { instantiateThreaded } from "./cumulus.js";
import { decodeInto, rowRanges } from "./subs.mjs";

const frs = new FileReaderSync();

let subs = [];     // [{ blob, ...meta }] — file handles and headers, not pixels
let result = null; // filled a strip at a time by put_rows

const host = {
  read_rows(frame, plane, row0, nrows, dst, dstOff, ctx) {
    const s = subs[Number(frame)];
    const r0 = Number(row0), nr = Number(nrows), pl = Number(plane);
    // `ctx.memory.buffer` is re-read on every call: a wasm heap growth detaches
    // the old ArrayBuffer, so a cached view would silently be writing to nothing.
    const out = new Uint16Array(ctx.memory.buffer, dst + Number(dstOff) * 2, nr * s.w);
    // Read exactly the rows asked for, straight off the Blob. This is the whole
    // streaming design: nothing before or after this range is ever resident, in
    // this worker or in the page. A multi-strip TIFF needs one read per strip
    // the range touches, which is why this is a loop and not a line.
    for (const run of rowRanges(s, r0, nr)) {
      const buf = frs.readAsArrayBuffer(s.blob.slice(run.start, run.start + run.length));
      if (buf.byteLength !== run.length) {
        throw new Error(
          `frame ${Number(frame)}: rows ${r0}..${r0 + nr} read ${buf.byteLength} bytes, wanted ${run.length}`,
        );
      }
      decodeInto(new Uint8Array(buf), out, run.row * s.w, s, pl, run.rows);
    }
  },
  put_rows(ptr, len, plane, row0, nrows, w, h, ctx) {
    // Streamed: one call per strip, per plane. Allocate on the first, then fill
    // — the assembled image lives HERE, in the JS heap, which is exactly where
    // the output-streaming slice moved it to get it off wasm32's 4 GiB budget.
    const W = Number(w), H = Number(h), r0 = Number(row0), n = Number(nrows);
    const pl = Number(plane);
    if (!result) result = { w: W, h: H, planes: nplanes, px: new Uint16Array(W * H * nplanes) };
    const strip = new Uint16Array(
      new Uint8Array(ctx.memory.buffer, ptr, Number(len)).slice().buffer);
    result.px.set(strip.subarray(0, n * W), pl * W * H + r0 * W);
  },
  progress(stage, done, total) {
    postMessage({ t: "progress", stage: Number(stage), done: Number(done), total: Number(total) });
  },
};

let nplanes = 1;

self.onmessage = async (e) => {
  const { subs: incoming, w, h, n, planes, mode, horizon, feather } = e.data;
  nplanes = planes || 1;
  // Blobs cross a postMessage by reference, not by copy — the bytes stay
  // wherever the browser is keeping them (usually on disk, for a picked File).
  subs = incoming;
  result = null;
  let handle = null;
  try {
    // THREADED when the page is cross-origin isolated (COOP/COEP), sequential
    // otherwise — `instantiateThreaded` makes that choice itself and falls back
    // without throwing. Measured on an 18-core M5 Pro: 8.3x faster threaded,
    // which lands the browser within 1.63x of fully-parallel native.
    //
    // Called from INSIDE this worker rather than from the page, and that is
    // load-bearing for the fallback: when threads are unavailable the fallback
    // runs the module on the CALLING thread, so calling it from the page would
    // freeze the tab — the exact failure this worker exists to prevent. Here,
    // the degraded path is simply today's behaviour.
    //
    // When threads ARE available the glue runs the program in its own primary
    // worker (every blocking primitive bottoms out in `memory.atomic.wait32`,
    // which traps on the main thread), so this worker just waits on it.
    handle = await instantiateThreaded(host);
    // Threaded exports are async — the call is a message round-trip to the
    // primary worker, not a direct wasm call.
    const kept = Number(await handle.exports.stack_frames(
      BigInt(w), BigInt(h), BigInt(n), BigInt(nplanes), BigInt(mode),
      BigInt(horizon || 0), BigInt(feather || 0)));
    subs = [];
    if (!result) throw new Error("stack_frames returned without emitting any rows");
    postMessage({ t: "done", kept, threaded: !!handle.threaded,
                  w: result.w, h: result.h, planes: result.planes, px: result.px },
                [result.px.buffer]);
    result = null;
  } catch (err) {
    // A `read_rows` that could not serve its range throws, and the exception
    // unwinds out of wasm to here. The run is abandoned rather than completed
    // with stale rows; the page terminates this worker either way, so the
    // abandoned wasm heap costs nothing.
    subs = [];
    postMessage({ t: "error", message: String((err && err.message) || err) });
  } finally {
    // Threaded runs hold a pool of worker threads; without this they outlive
    // the stack and the page leaks an agent per run.
    await handle?.terminate?.();
  }
};
