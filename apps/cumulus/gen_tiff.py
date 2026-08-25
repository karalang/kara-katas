#!/usr/bin/env python3
"""
gen_tiff.py — synthetic subs as baseline TIFF, mono or RGB.

TIFF is the format a nightscape photographer actually HAS. The workflow is
RAW -> Lightroom/ACR/darktable -> 16-bit TIFF, and that TIFF is what Starry
Landscape Stacker and Sequator ingest. FITS is what a telescope writes; TIFF is
what a camera-and-tripod session becomes.

Two fixtures come out of here, and they check different things:

  --from-cstack  transcribes an EXISTING `.cstack` into one mono TIFF per
                 frame, value for value. The stack of those TIFFs must then be
                 byte-identical to the stack of the container — a zero-tolerance
                 equality that a reader with an off-by-one strip offset, a
                 byte-order slip, or a stride error cannot pass.

  (default)      renders a COLOUR scene from the same star table gen_cfa.py
                 uses, with deliberate per-star R:G:B ratios. If the RGB path
                 transposes channels or mis-strides the interleave, a red star
                 comes out blue.

It also writes the files the reader must REFUSE — Deflate-compressed, tiled,
planar-configuration 2, 32-bit float — and those are written as genuinely valid
TIFFs (real zlib strips, real tiles) so that a refusal is a statement about
Cumulus rather than about a malformed fixture.

Usage:
    python3 gen_tiff.py outdir [--width 96] [--height 64] [--frames 8]
                               [--dither 3.0] [--bits 16] [--endian big]
                               [--rows-per-strip 8] [--truth t.txt]
    python3 gen_tiff.py outdir --from-cstack in.cstack [--endian big]
"""

import argparse
import math
import os
import struct
import zlib

from gen_frames import LCG
from gen_cfa import STARS, SKY

# TIFF field types, by their numeric code.
SHORT = 3
LONG = 4


def _pack(endian: str, fmt: str, *vals) -> bytes:
    return struct.pack(endian + fmt, *vals)


def write_tiff(path, planes, w, h, bits=16, endian="<", rows_per_strip=None,
               compression=1, planar=1, photometric=None, tiled=0,
               sample_format=1):
    """Write a baseline TIFF.

    `planes` is a list of 1 or 3 flat sample lists, each w*h. Chunky
    (`planar=1`) interleaves them per pixel, which is what every ordinary
    encoder emits; `planar=2` writes each plane's strips consecutively.
    """
    spp = len(planes)
    if photometric is None:
        photometric = 2 if spp == 3 else 1
    bpsamp = bits // 8
    if rows_per_strip is None:
        rows_per_strip = h

    def sample_bytes(v):
        if bits == 8:
            return bytes([max(0, min(255, v))])
        if bits == 16:
            return _pack(endian, "H", max(0, min(65535, v)))
        # 32-bit float, only used for the refusal fixture.
        return _pack(endian, "f", float(v))

    # ── payload ────────────────────────────────────────────────────────────
    chunks = []          # one entry per strip/tile, already compressed
    if tiled:
        tw, th = tiled, tiled
        ntx = (w + tw - 1) // tw
        nty = (h + th - 1) // th
        for ty in range(nty):
            for tx in range(ntx):
                buf = bytearray()
                for y in range(ty * th, ty * th + th):
                    for x in range(tx * tw, tx * tw + tw):
                        # Tiles are PADDED to full size; the pad is zero.
                        inside = y < h and x < w
                        for p in planes:
                            buf += sample_bytes(p[y * w + x] if inside else 0)
                chunks.append(bytes(buf))
    elif planar == 2:
        for p in planes:
            for s in range(0, h, rows_per_strip):
                buf = bytearray()
                for y in range(s, min(s + rows_per_strip, h)):
                    for x in range(w):
                        buf += sample_bytes(p[y * w + x])
                chunks.append(bytes(buf))
    else:
        for s in range(0, h, rows_per_strip):
            buf = bytearray()
            for y in range(s, min(s + rows_per_strip, h)):
                for x in range(w):
                    for p in planes:
                        buf += sample_bytes(p[y * w + x])
            chunks.append(bytes(buf))

    if compression == 8:
        chunks = [zlib.compress(c, 6) for c in chunks]
    elif compression != 1:
        raise SystemExit(f"gen_tiff: cannot emit compression {compression}")

    # ── directory ──────────────────────────────────────────────────────────
    # Entries must be in ascending tag order. Values wider than four bytes live
    # in an overflow area after the IFD, and the entry holds their offset.
    n = len(chunks)
    entries = [
        (256, LONG, 1, [w]),
        (257, LONG, 1, [h]),
        (258, SHORT, spp, [bits] * spp),
        (259, SHORT, 1, [compression]),
        (262, SHORT, 1, [photometric]),
    ]
    if not tiled:
        entries += [(273, LONG, n, None)]           # StripOffsets, patched below
    entries += [(277, SHORT, 1, [spp])]
    if not tiled:
        entries += [(278, LONG, 1, [rows_per_strip]),
                    (279, LONG, n, [len(c) for c in chunks])]
    entries += [(284, SHORT, 1, [planar])]
    if tiled:
        entries += [(322, LONG, 1, [tiled]), (323, LONG, 1, [tiled]),
                    (324, LONG, n, None),            # TileOffsets, patched below
                    (325, LONG, n, [len(c) for c in chunks])]
    entries += [(339, SHORT, spp, [sample_format] * spp)]
    entries.sort(key=lambda e: e[0])

    ifd_off = 8
    ifd_len = 2 + 12 * len(entries) + 4
    over_off = ifd_off + ifd_len
    # Lay the overflow area out first so data offsets are known before packing.
    over = bytearray()
    slots = {}
    for tag, typ, cnt, vals in entries:
        width = (2 if typ == SHORT else 4) * cnt
        if width > 4:
            slots[tag] = over_off + len(over)
            if vals is None:
                over += b"\0" * width           # patched once offsets are known
            else:
                over += b"".join(_pack(endian, "H" if typ == SHORT else "I", v)
                                 for v in vals)
    data_off = over_off + len(over)

    offs, cur = [], data_off
    for c in chunks:
        offs.append(cur)
        cur += len(c)
    for tag in (273, 324):
        if tag in slots:
            pos = slots[tag] - over_off
            over[pos:pos + 4 * n] = b"".join(_pack(endian, "I", o) for o in offs)
        elif any(t == tag for t, _, _, _ in entries):
            # n == 1, so the offset fits inline; handled in the entry loop.
            pass

    out = bytearray()
    out += (b"II" if endian == "<" else b"MM") + _pack(endian, "HI", 42, ifd_off)
    out += _pack(endian, "H", len(entries))
    for tag, typ, cnt, vals in entries:
        width = (2 if typ == SHORT else 4) * cnt
        out += _pack(endian, "HHI", tag, typ, cnt)
        if width > 4:
            out += _pack(endian, "I", slots[tag])
        else:
            v = offs if (vals is None) else vals
            raw = b"".join(_pack(endian, "H" if typ == SHORT else "I", x) for x in v)
            # A value shorter than four bytes is LEFT-justified in the field.
            out += raw + b"\0" * (4 - len(raw))
    out += _pack(endian, "I", 0)                  # no second IFD
    out += bytes(over)
    for c in chunks:
        out += c
    with open(path, "wb") as f:
        f.write(bytes(out))


def render_rgb(w, h, dx, dy):
    """The colour scene at a given dither, before noise — three full-res planes."""
    out = [[0.0] * (w * h) for _ in range(3)]
    stars = [(fx * w, fy * h, amp, sig, col) for fx, fy, amp, sig, col in STARS]
    for k, ch in enumerate("RGB"):
        ped, gx, gy = SKY[ch]
        p = out[k]
        for y in range(h):
            for x in range(w):
                v = ped + gx * (x / w) * 96.0 + gy * (y / h) * 64.0
                for sx, sy, amp, sig, col in stars:
                    d2 = (x - (sx + dx)) ** 2 + (y - (sy + dy)) ** 2
                    if d2 < (5.0 * sig) ** 2:
                        v += amp * col[k] * math.exp(-d2 / (2.0 * sig * sig))
                p[y * w + x] = v
    return out


def read_cstack(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:4] != b"CSTK":
        raise SystemExit(f"gen_tiff: {path} is not a .cstack")
    w, h, n = struct.unpack("<III", data[4:16])
    px = struct.unpack(f"<{w * h * n}H", data[16:16 + w * h * n * 2])
    return list(px), w, h, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--from-cstack", help="transcribe this container to mono TIFFs")
    ap.add_argument("--width", type=int, default=96)
    ap.add_argument("--height", type=int, default=64)
    ap.add_argument("--frames", type=int, default=8)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--rays", type=int, default=12)
    ap.add_argument("--noise", type=float, default=60.0)
    ap.add_argument("--dither", type=float, default=0.0)
    ap.add_argument("--bits", type=int, default=16, choices=[8, 16])
    ap.add_argument("--endian", default="little", choices=["little", "big"])
    ap.add_argument("--rows-per-strip", type=int, default=0,
                    help="0 = one strip for the whole image")
    ap.add_argument("--mono", action="store_true", help="1 sample per pixel")
    ap.add_argument("--refuse", choices=["deflate", "tiled", "planar", "float"],
                    help="emit a file the reader must refuse")
    ap.add_argument("--expect", help="with --from-cstack: write the container the "
                                     "reader should decode these TIFFs to")
    ap.add_argument("--truth", help="write the injected per-frame offsets here")
    args = ap.parse_args()

    endian = "<" if args.endian == "little" else ">"
    rps = args.rows_per_strip or None
    os.makedirs(args.outdir, exist_ok=True)

    kw = dict(bits=args.bits, endian=endian, rows_per_strip=rps)
    if args.refuse == "deflate":
        kw["compression"] = 8
    elif args.refuse == "tiled":
        kw["tiled"] = 16
    elif args.refuse == "planar":
        kw["planar"] = 2
    elif args.refuse == "float":
        kw["bits"] = 32
        kw["sample_format"] = 3

    if args.from_cstack:
        px, w, h, n = read_cstack(args.from_cstack)
        # An 8-bit TIFF cannot carry 16-bit values, so the transcription is
        # lossy BY CONSTRUCTION: take the high byte, and the reader expands it
        # again by bit replication (x257). `--expect` writes the container that
        # round trip should land on, which is what makes the 8-bit case a
        # byte-identity test rather than a tolerance one.
        if args.bits == 8:
            px = [v >> 8 for v in px]
        for i in range(n):
            write_tiff(os.path.join(args.outdir, f"sub_{i:03d}.tif"),
                       [px[i * w * h:(i + 1) * w * h]], w, h, **kw)
        if args.expect:
            exp = [v * 257 for v in px] if args.bits == 8 else px
            with open(args.expect, "wb") as ef:
                ef.write(b"CSTK" + struct.pack("<III", w, h, n))
                ef.write(struct.pack(f"<{len(exp)}H", *exp))
        print(f"wrote {n} mono TIFF frames to {args.outdir}: {w}x{h}, "
              f"{args.bits}-bit, {args.endian}-endian, "
              f"rows/strip {rps or h}, from {args.from_cstack}")
        return 0

    w, h, n = args.width, args.height, args.frames
    rng = LCG(args.seed)
    truth = []
    for i in range(n):
        # Frame 0 is the reference and never moves, as in every other generator
        # here, so recovered offsets are directly comparable across paths.
        if i == 0 or args.dither == 0.0:
            dx = dy = 0.0
        else:
            dx = (rng.uniform() * 2.0 - 1.0) * args.dither
            dy = (rng.uniform() * 2.0 - 1.0) * args.dither
        truth.append((dx, dy))

        scene = render_rgb(w, h, dx, dy)
        top = 255 if args.bits == 8 else 65535
        scale = 1.0 if args.bits == 16 else 255.0 / 65535.0
        planes = []
        for k in range(3):
            p = [0] * (w * h)
            for j in range(w * h):
                v = (scene[k][j] + rng.gauss(args.noise)) * scale
                p[j] = min(top, max(0, int(v + 0.5)))
            planes.append(p)
        for _ in range(args.rays):
            j = rng.next_u32() % (w * h)
            k = rng.next_u32() % 3
            planes[k][j] = int(top * 0.92) + (rng.next_u32() % max(1, top // 20))
        if args.mono:
            planes = [[(planes[0][j] + 2 * planes[1][j] + planes[2][j]) // 4
                       for j in range(w * h)]]

        write_tiff(os.path.join(args.outdir, f"sub_{i:03d}.tif"),
                   planes, w, h, **kw)

    if args.truth:
        with open(args.truth, "w") as th:
            for dx, dy in truth:
                th.write(f"{dx:.9f} {dy:.9f}\n")

    kind = "mono" if args.mono else "RGB"
    print(f"wrote {n} {kind} TIFF frames to {args.outdir}: {w}x{h}, "
          f"{kw.get('bits', args.bits)}-bit, {args.endian}-endian, "
          f"rows/strip {rps or h}, dither +/-{args.dither}px"
          + (f", REFUSAL fixture ({args.refuse})" if args.refuse else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
