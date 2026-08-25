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
import { decodeRows } from "./fits.mjs";

const frs = new FileReaderSync();

let subs = [];     // [{ blob, w, h, bzero, bscale, dataOff }] — handles, not pixels
let result = null; // set by put_result before stack_frames returns

const host = {
  read_rows(frame, row0, nrows, dst, dstOff, ctx) {
    const s = subs[Number(frame)];
    const r0 = Number(row0), nr = Number(nrows), count = nr * s.w;
    const start = s.dataOff + r0 * s.w * 2;
    // Read exactly the rows asked for, straight off the Blob. This is the whole
    // streaming design in one line: nothing before or after this range is ever
    // resident, in this worker or in the page.
    const buf = frs.readAsArrayBuffer(s.blob.slice(start, start + count * 2));
    if (buf.byteLength !== count * 2) {
      throw new Error(
        `frame ${Number(frame)}: rows ${r0}..${r0 + nr} read ${buf.byteLength} bytes, wanted ${count * 2}`,
      );
    }
    // `ctx.memory.buffer` is re-read on every call: a wasm heap growth detaches
    // the old ArrayBuffer, so a cached view would silently be writing to nothing.
    decodeRows(
      new Uint8Array(buf),
      new Uint16Array(ctx.memory.buffer, dst + Number(dstOff) * 2, count),
      s.bzero, s.bscale,
    );
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
  const { subs: incoming, w, h, n, mode } = e.data;
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
      BigInt(w), BigInt(h), BigInt(n), BigInt(mode)));
    subs = [];
    if (!result) throw new Error("stack_frames returned without calling put_result");
    postMessage({ t: "done", kept, threaded: !!handle.threaded,
                  w: result.w, h: result.h, px: result.px }, [result.px.buffer]);
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
