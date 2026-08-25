// tiff.mjs — the browser-side TIFF reader, shared by the page and the worker.
//
// Same two-function shape as fits.mjs, and for the same reason: the page parses
// HEADERS to learn geometry and reject a mismatched sequence, and the worker
// decodes ROW RANGES on demand. Neither does the other's half.
//
// And the same warning applies twice over. This is a second implementation of
// the TIFF spec racing the Kāra one in cumulus.kara, so the two are checked
// against each other for byte-identity (test_node.mjs) — a third copy inside
// the worker would be a second place for it to drift.
//
// Scope is deliberately identical to the Kāra reader's: uncompressed, strip
// organised, 8 or 16 bits, 1 or 3 samples, either byte order. Anything else is
// refused by name here too, because a page that half-reads a file paints a
// plausible wrong picture rather than an error.

const SHORT = 3, LONG = 4;

function val(dv, off, width, big) {
  if (width === 1) return dv.getUint8(off);
  if (width === 2) return dv.getUint16(off, !big);
  return dv.getUint32(off, !big);
}

/// Every value of one IFD entry.
///
/// A value of four bytes or fewer sits INSIDE the twelve-byte entry, left
/// justified; a longer one sits elsewhere in the file. `fetch` resolves that
/// second case — it is a synchronous slice of an already-read buffer here,
/// because the header read below grows until the whole directory is covered.
function entryValues(dv, eo, big, fetch) {
  const typ = dv.getUint16(eo + 2, !big);
  const cnt = dv.getUint32(eo + 4, !big);
  const width = typ === 1 ? 1 : typ === SHORT ? 2 : typ === LONG ? 4 : 0;
  if (!width || cnt <= 0 || cnt > 16777216) return null;
  const total = cnt * width;
  const out = new Array(cnt);
  if (total <= 4) {
    for (let i = 0; i < cnt; i++) out[i] = val(dv, eo + 8 + i * width, width, big);
    return out;
  }
  const at = dv.getUint32(eo + 8, !big);
  const far = fetch(at, total);
  if (!far) return null;
  const fdv = new DataView(far.buffer, far.byteOffset, far.byteLength);
  for (let i = 0; i < cnt; i++) out[i] = val(fdv, i * width, width, big);
  return out;
}

/// Parse IFD0 out of `bytes`, which must already cover the directory and any
/// out-of-line values it points at.
///
/// Returns `{ incomplete: true, need }` when it does not, which is a request
/// for more bytes rather than an error — libtiff writes the directory AFTER the
/// pixels, so a first read of the front of the file usually misses it entirely.
export function parseHeader(bytes, fileSize) {
  if (bytes.length < 8) return { incomplete: true, need: 8 };
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const b0 = bytes[0], b1 = bytes[1];
  const big = b0 === 0x4d && b1 === 0x4d;
  if (!big && !(b0 === 0x49 && b1 === 0x49)) throw new Error("not a TIFF (no II/MM byte-order mark)");
  const magic = dv.getUint16(2, !big);
  if (magic === 43) throw new Error("BigTIFF is not implemented (only the classic 42 magic)");
  if (magic !== 42) throw new Error("not a TIFF (bad magic number)");

  const ifdOff = dv.getUint32(4, !big);
  if (ifdOff + 2 > bytes.length) return { incomplete: true, need: ifdOff + 2 };
  const nent = dv.getUint16(ifdOff, !big);
  if (nent <= 0 || nent > 512) throw new Error("implausible IFD entry count");
  const end = ifdOff + 2 + nent * 12;
  if (end > bytes.length) return { incomplete: true, need: end };

  let short = 0;
  const fetch = (at, n) => {
    if (at + n > bytes.length) { short = Math.max(short, at + n); return null; }
    return bytes.subarray(at, at + n);
  };

  const tags = {};
  for (let e = 0; e < nent; e++) {
    const eo = ifdOff + 2 + e * 12;
    const tag = dv.getUint16(eo, !big);
    if ([256, 257, 258, 259, 262, 273, 277, 278, 279, 284, 322, 339].includes(tag)) {
      tags[tag] = entryValues(dv, eo, big, fetch);
    }
  }
  if (short) return { incomplete: true, need: short };

  const w = tags[256]?.[0] ?? 0, h = tags[257]?.[0] ?? 0;
  const spp = tags[277]?.[0] ?? 1;
  const comp = tags[259]?.[0] ?? 1;
  const photo = tags[262]?.[0] ?? -1;
  const planar = tags[284]?.[0] ?? 1;
  const fmt = tags[339]?.[0] ?? 1;
  const bitsArr = tags[258] ?? [1];

  if (w <= 0 || h <= 0) throw new Error("TIFF carries no image dimensions");
  if (tags[322]) throw new Error("tiled TIFF is not implemented (only strip-organised files)");
  if (comp !== 1) {
    throw new Error(`unsupported TIFF compression ${comp} — only uncompressed is implemented ` +
                    "(re-export with compression off)");
  }
  if (planar !== 1) throw new Error("unsupported PlanarConfiguration (only chunky, 1, is implemented)");
  if (fmt !== 1) throw new Error("unsupported SampleFormat (only unsigned integer is implemented)");
  if (spp !== 1 && spp !== 3) {
    throw new Error(`unsupported SamplesPerPixel ${spp} — only 1 (mono) and 3 (RGB) are implemented`);
  }
  if (bitsArr.length !== spp) throw new Error("BitsPerSample count disagrees with SamplesPerPixel");
  const bits = bitsArr[0];
  if (bitsArr.some((b) => b !== bits)) throw new Error("channels of differing bit depth are not implemented");
  if (bits !== 8 && bits !== 16) {
    throw new Error(`unsupported BitsPerSample ${bits} — only 8 and 16 are implemented`);
  }
  if (spp === 1 && photo !== 1 && photo !== -1) {
    throw new Error(`unsupported PhotometricInterpretation ${photo} for a 1-sample TIFF — only 1 (BlackIsZero)`);
  }
  if (spp === 3 && photo !== 2) {
    throw new Error(`unsupported PhotometricInterpretation ${photo} for a 3-sample TIFF — only 2 (RGB)`);
  }

  let rowsPerStrip = tags[278]?.[0] ?? h;
  if (rowsPerStrip <= 0 || rowsPerStrip > h) rowsPerStrip = h;
  const stripOffs = tags[273] ?? [];
  const nstrips = Math.ceil(h / rowsPerStrip);
  if (stripOffs.length !== nstrips) throw new Error("StripOffsets count disagrees with the image height");

  // The one check that catches a file whose compression TAG says 1 but whose
  // payload does not — and, equally, a reader whose row stride is wrong.
  const rowBytes = w * spp * (bits / 8);
  const counts = tags[279];
  if (counts && counts.length === nstrips) {
    const rows0 = Math.min(rowsPerStrip, h);
    if (counts[0] !== rows0 * rowBytes) {
      throw new Error("StripByteCounts does not match an uncompressed strip of this geometry");
    }
  }

  return { kind: "tiff", w, h, spp, bits, big, rowsPerStrip, stripOffs, rowBytes, bayer: "" };
}

/// Read enough of `blob` to parse its directory, growing until it is covered.
///
/// The growth pattern is not the FITS one. A FITS header is a PREFIX, so 11 KB
/// always suffices; a TIFF directory is commonly at the END of the file, and
/// `parseHeader` reports how far it needed to reach, so the second attempt is
/// exact rather than a guess. The tail read is what makes the usual libtiff
/// layout cost two small reads instead of one whole-file read.
export async function readHeader(blob) {
  let bytes = new Uint8Array(await blob.slice(0, Math.min(blob.size, 64 * 1024)).arrayBuffer());
  let meta = parseHeader(bytes, blob.size);
  if (!meta.incomplete) return meta;
  // Read from 0 up to what it asked for. Directories are small; what is large
  // is the pixel data sitting between the header and them, and there is no way
  // to skip it with one contiguous slice.
  const need = Math.min(blob.size, meta.need + 4096);
  bytes = new Uint8Array(await blob.slice(0, need).arrayBuffer());
  meta = parseHeader(bytes, blob.size);
  if (meta.incomplete) throw new Error("TIFF directory extends past the end of the file");
  return meta;
}

/// Byte range of rows `[row0, row0+nrows)` — the slice the caller must read.
///
/// Rows can only be fetched in runs that stay inside ONE strip, so this returns
/// a list of runs. A whole-image strip, which is what most encoders write,
/// makes that list one entry.
export function rowRuns(meta, row0, nrows) {
  const runs = [];
  let r = row0;
  while (r < row0 + nrows) {
    const si = Math.floor(r / meta.rowsPerStrip);
    const within = r - si * meta.rowsPerStrip;
    const run = Math.min(meta.rowsPerStrip - within, row0 + nrows - r);
    runs.push({
      row: r - row0,
      rows: run,
      start: meta.stripOffs[si] + within * meta.rowBytes,
      length: run * meta.rowBytes,
    });
    r += run;
  }
  return runs;
}

/// Decode one run into `out`, taking sample `plane` of each pixel.
///
/// `plane` is 0..spp, or -1 for the MEDIAN of the three — which is what
/// registration runs on, because a hot pixel or a ray lands in one channel and
/// a median drops it outright where a mean divides it by three and lets it drag
/// the star's measured centre.
export function decodeRows(src, out, outOff, meta, plane, rows) {
  const dv = new DataView(src.buffer, src.byteOffset, src.byteLength);
  const { w, spp, bits, big } = meta;
  const bp = bits / 8;
  // 8-bit expands by bit REPLICATION (x257): 255 goes to exactly 65535. A bare
  // shift caps at 65280 and darkens the whole sequence — invisible in a
  // picture, fatal to a byte-identity oracle.
  const sample = bits === 8
    ? (o) => dv.getUint8(o) * 257
    : (o) => dv.getUint16(o, !big);
  for (let y = 0; y < rows; y++) {
    const ro = y * meta.rowBytes;
    const po = outOff + y * w;
    for (let x = 0; x < w; x++) {
      const so = ro + x * spp * bp;
      if (plane >= 0) {
        out[po + x] = sample(so + plane * bp);
      } else if (spp === 1) {
        out[po + x] = sample(so);
      } else {
        const a = sample(so), b = sample(so + bp), c = sample(so + 2 * bp);
        out[po + x] = a + b + c - Math.min(a, b, c) - Math.max(a, b, c);
      }
    }
  }
}
