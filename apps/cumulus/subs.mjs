// subs.mjs — "what is this file, and where are row R's pixels" for the browser.
//
// The native side answers that with `read_sub_header` / `read_sub_rows` in
// cumulus.kara; this is the same dispatcher on the JS side, and it exists for
// the same reason: everything above it — the page, the worker, the inline
// fallback — wants ONE question answered and should not branch on the container
// twice, once on which kind it is and once on what to do about it.
//
// Format comes from the file's first two bytes, never from its name.
// Extensions lie: `.fit`, `.fts`, `.tif`, and files with none at all.

import * as fits from "./fits.mjs";
import * as tiff from "./tiff.mjs";

/// Parse whichever header this turns out to be.
///
/// The returned shape is common to both: `{ kind, w, h, spp, bayer }` plus
/// whatever that decoder needs to find rows again. Nothing above this reads the
/// format-specific half.
export async function readSubHeader(blob) {
  const head = new Uint8Array(await blob.slice(0, 2).arrayBuffer());
  if ((head[0] === 0x49 && head[1] === 0x49) || (head[0] === 0x4d && head[1] === 0x4d)) {
    return await tiff.readHeader(blob);
  }
  const m = await fits.readHeader(blob);
  return { kind: "fits", spp: 1, ...m };
}

/// The byte ranges holding rows `[row0, row0+nrows)`.
///
/// A list rather than one range because a multi-strip TIFF stores them in
/// pieces. FITS is always one piece, and a whole-image-strip TIFF — what most
/// encoders write — is also one, so the common case costs one read either way.
export function rowRanges(meta, row0, nrows) {
  if (meta.kind === "tiff") return tiff.rowRuns(meta, row0, nrows);
  return [{
    row: 0,
    rows: nrows,
    start: meta.dataOff + row0 * meta.w * 2,
    length: nrows * meta.w * 2,
  }];
}

/// Decode one range into `out` at `outOff`, taking sample `plane`.
///
/// `plane` is 0..spp, or -1 for the median luminance registration runs on.
/// FITS has one sample, so it ignores the argument entirely.
export function decodeInto(src, out, outOff, meta, plane, rows) {
  if (meta.kind === "tiff") {
    tiff.decodeRows(src, out, outOff, meta, plane, rows);
    return;
  }
  fits.decodeRows(src, out.subarray(outOff, outOff + rows * meta.w), meta.bzero, meta.bscale);
}

/// Is this sequence one stack, or several sessions concatenated?
///
/// Returns null if it is fine, or the reason it is not. The page refuses rather
/// than stacking whatever happens to line up, which is what the CLI does too.
export function mismatch(metas) {
  const a = metas[0];
  for (let i = 1; i < metas.length; i++) {
    const m = metas[i];
    if (m.w !== a.w || m.h !== a.h) return `frame ${i} is ${m.w}×${m.h}, not ${a.w}×${a.h}`;
    if (m.spp !== a.spp) return `frame ${i} has ${m.spp} channel(s), not ${a.spp}`;
    if ((m.bayer || "") !== (a.bayer || "")) return `frame ${i} disagrees about BAYERPAT`;
    if (m.kind !== a.kind) return `frame ${i} is ${m.kind}, not ${a.kind}`;
  }
  return null;
}
