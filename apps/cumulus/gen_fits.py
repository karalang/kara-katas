#!/usr/bin/env python3
"""
gen_fits.py — write the synthetic stack as individual FITS frames.

Same scene and same deterministic LCG as gen_frames.py, emitted in the shape a
smart telescope actually produces: one FITS file per sub, `BITPIX = 16` with
`BZERO = 32768` (the standard way unsigned 16-bit data rides in FITS's signed
16-bit format), big-endian, 2880-byte blocks.

Written by hand rather than with astropy on purpose. The Kāra reader has to be
checked against the SPEC, not against whatever a library happens to emit, and
hand-writing the header keeps every byte the reader must handle visible here —
the card padding, the END card, the block padding, the BZERO round trip.

Usage:
    python3 gen_fits.py outdir [--frames 16] [--width 96] [--height 64]
                               [--seed 7] [--rays 12] [--noise 60]
"""

import argparse
import os
import struct

from gen_frames import LCG, base_sky

BLOCK = 2880
CARD = 80


def card(key: str, value, comment: str = "") -> bytes:
    """One 80-byte FITS header card, fixed format."""
    if isinstance(value, bool):
        v = "T" if value else "F"
    elif isinstance(value, int):
        v = str(value)
    else:
        v = str(value)
    body = f"{key:<8}= {v:>20}"
    if comment:
        body = f"{body} / {comment}"
    if len(body) > CARD:
        body = body[:CARD]
    return body.ljust(CARD).encode("ascii")


def write_fits(path: str, px: list[int], w: int, h: int, extra=None) -> None:
    """Write one 16-bit FITS image.

    `extra` is an optional list of (key, value, comment) appended before END —
    used by gen_cfa.py for the BAYERPAT/ROWORDER pair. String values must
    arrive already quoted, since FITS quotes them and the reader strips them.
    """
    cards = [
        card("SIMPLE", True, "conforms to FITS standard"),
        card("BITPIX", 16, "16-bit integers"),
        card("NAXIS", 2),
        card("NAXIS1", w),
        card("NAXIS2", h),
        # Unsigned 16-bit data stored in signed 16-bit space. A reader that
        # ignores BZERO gets everything above 32767 as a large negative number
        # — the single most common way to get FITS wrong.
        card("BZERO", 32768, "unsigned 16-bit offset"),
        card("BSCALE", 1),
    ]
    for key, value, comment in (extra or []):
        cards.append(card(key, value, comment))
    cards.append(b"END".ljust(CARD))
    header = b"".join(cards)
    header += b" " * ((-len(header)) % BLOCK)

    # Physical -> stored: stored = (physical - BZERO) / BSCALE, as int16 BE.
    stored = [v - 32768 for v in px]
    data = struct.pack(f">{len(stored)}h", *stored)
    data += b"\0" * ((-len(data)) % BLOCK)

    with open(path, "wb") as fh:
        fh.write(header)
        fh.write(data)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir")
    ap.add_argument("--width", type=int, default=96)
    ap.add_argument("--height", type=int, default=64)
    ap.add_argument("--frames", type=int, default=16)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--rays", type=int, default=12)
    ap.add_argument("--noise", type=float, default=60.0)
    ap.add_argument("--dither", type=float, default=0.0,
                    help="max per-frame star shift in pixels (0 = aligned)")
    ap.add_argument("--truth", help="write the injected per-frame offsets here")
    args = ap.parse_args()

    w, h, n = args.width, args.height, args.frames
    rng = LCG(args.seed)
    os.makedirs(args.outdir, exist_ok=True)
    truth = []

    for i in range(n):
        # Same convention as gen_frames.py: frame 0 is the reference and never
        # moves, so the recovered offsets are directly comparable between the
        # two containers.
        if i == 0 or args.dither == 0.0:
            dx = dy = 0.0
        else:
            dx = (rng.uniform() * 2.0 - 1.0) * args.dither
            dy = (rng.uniform() * 2.0 - 1.0) * args.dither
        truth.append((dx, dy))
        sky = base_sky(w, h, dx, dy)
        px = [0] * (w * h)
        for j in range(w * h):
            v = sky[j] + rng.gauss(args.noise)
            px[j] = min(65535, max(0, int(v + 0.5)))
        for _ in range(args.rays):
            idx = rng.next_u32() % (w * h)
            px[idx] = 60000 + (rng.next_u32() % 5000)
        write_fits(os.path.join(args.outdir, f"sub_{i:03d}.fits"), px, w, h)

    if args.truth:
        with open(args.truth, "w") as th:
            for dx, dy in truth:
                th.write(f"{dx:.9f} {dy:.9f}\n")
    print(f"wrote {n} FITS frames to {args.outdir}: {w}x{h}, BITPIX=16, BZERO=32768, "
          f"dither +/-{args.dither}px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
