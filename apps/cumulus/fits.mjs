// fits.mjs — the browser-side FITS reader, shared by the page and the worker.
//
// This used to live inside index.html as one `decodeFits(buffer)` that took a
// whole file and returned a whole decoded image. Streaming split it in two,
// because the page and the worker now want different halves of it: the page
// parses HEADERS (to learn geometry and reject a sequence that does not match)
// and never touches a pixel, while the worker decodes ROW RANGES on demand and
// never re-parses a header.
//
// Both halves live here rather than being copied into each file. The whole
// reason verify_browser.mjs exists is that this decoder is a second
// implementation of the FITS spec racing the Kāra one in cumulus.kara, and a
// third copy inside the worker would be a second place for it to drift.
//
// Scope is deliberately the same as the Kāra reader's: BITPIX=16, NAXIS=2, with
// BZERO/BSCALE — what a smart telescope writes.

export const BLOCK = 2880;
const CARD = 80;

/// Parse the FITS header out of the front of a file.
///
/// Returns `{ incomplete: true }` if `bytes` ran out before the END card, which
/// is a request for more bytes rather than an error — callers slice the file
/// progressively so that a long header costs a second read and a normal one
/// costs nothing.
export function parseHeader(bytes) {
  if (bytes.length < BLOCK) throw new Error("shorter than one FITS block");

  const latin1 = new TextDecoder("latin1");
  let off = 0, done = false;
  const kv = {};
  while (off + CARD <= bytes.length && !done) {
    const card = latin1.decode(bytes.subarray(off, off + CARD));
    const key = card.slice(0, 8).trim();
    if (key === "END") { done = true; off = (Math.floor(off / BLOCK) + 1) * BLOCK; break; }
    const eq = card.indexOf("=");
    if (eq >= 0) {
      let v = card.slice(eq + 1);
      const slash = v.indexOf("/");
      if (slash >= 0) v = v.slice(0, slash);
      kv[key] = v.trim();
    }
    off += CARD;
  }
  if (!done) return { incomplete: true };

  const bitpix = parseInt(kv.BITPIX ?? "0", 10);
  const naxis = parseInt(kv.NAXIS ?? "0", 10);
  const w = parseInt(kv.NAXIS1 ?? "0", 10);
  const h = parseInt(kv.NAXIS2 ?? "0", 10);
  if (bitpix !== 16) throw new Error(`unsupported BITPIX ${bitpix} (only 16 is implemented)`);
  if (naxis !== 2) throw new Error(`unsupported NAXIS ${naxis} (only 2-D mono is implemented)`);

  return {
    w, h,
    bzero: parseFloat(kv.BZERO ?? "0"),
    bscale: parseFloat(kv.BSCALE ?? "1"),
    dataOff: off,
    // A colour mosaic stacked as if it were grey does not fail — it produces a
    // plausible picture with checkerboard texture and colour-biased star
    // positions. The CLI refuses that combination outright; so does the page.
    bayer: (kv.BAYERPAT ?? "").replace(/'/g, "").trim(),
  };
}

/// Read enough of `blob` to parse its header, growing the read if the header is
/// unusually long. Four blocks (11 KB) covers everything a camera writes; the
/// larger steps exist so a hand-annotated file still loads.
export async function readHeader(blob) {
  for (const blocks of [4, 32, 256]) {
    const n = Math.min(blob.size, blocks * BLOCK);
    const meta = parseHeader(new Uint8Array(await blob.slice(0, n).arrayBuffer()));
    if (!meta.incomplete) return meta;
    if (n >= blob.size) break;
  }
  throw new Error("no END card in header");
}

/// Decode `out.length` big-endian 16-bit samples from `src` into `out`.
///
/// The BZERO transform is the part that matters and the part that is easy to get
/// wrong — unsigned 16-bit data rides in FITS's SIGNED 16-bit format, so
/// dropping it turns every value above 32767 negative and stars come out as
/// holes. `out` is normally a view straight into wasm linear memory, so this
/// writes the pixels into their final home with no intermediate buffer.
export function decodeRows(src, out, bzero, bscale) {
  const dv = new DataView(src.buffer, src.byteOffset, src.byteLength);
  for (let i = 0; i < out.length; i++) {
    const v = bzero + bscale * dv.getInt16(i * 2, false); // FITS is big-endian
    out[i] = v < 0 ? 0 : v > 65535 ? 65535 : Math.round(v);
  }
}
