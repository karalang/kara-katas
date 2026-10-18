#!/usr/bin/env python3
"""Writes data/: PNG files of every colour type and bit depth, interlaced
and not, with every filter type, compressed by zlib at several levels and
strategies, with text and other ancillary chunks, and broken files; and
data/jobs.tsv, the jobs mini_png runs."""
import os
import struct
import zlib

os.makedirs("data/broken", exist_ok=True)

CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


def chunk(kind, data):
    return (struct.pack(">I", len(data)) + kind + data
            + struct.pack(">I", zlib.crc32(kind + data)))


def pack_row(pixels, depth, ctype):
    ch = CHANNELS[ctype]
    if depth < 8:
        out = bytearray()
        acc = 0
        nbits = 0
        for p in pixels:
            acc = (acc << depth) | p[0]
            nbits += depth
            if nbits == 8:
                out.append(acc)
                acc = 0
                nbits = 0
        if nbits:
            out.append(acc << (8 - nbits))
        return bytes(out)
    out = bytearray()
    for p in pixels:
        for k in range(ch):
            if depth == 8:
                out.append(p[k])
            else:
                out += struct.pack(">H", p[k])
    return bytes(out)


def paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def filter_row(ftype, row, prev, bpp):
    out = bytearray([ftype])
    for i, x in enumerate(row):
        a = row[i - bpp] if i >= bpp else 0
        b = prev[i] if prev else 0
        c = prev[i - bpp] if prev and i >= bpp else 0
        if ftype == 0:
            v = x
        elif ftype == 1:
            v = x - a
        elif ftype == 2:
            v = x - b
        elif ftype == 3:
            v = x - (a + b) // 2
        else:
            v = x - paeth(a, b, c)
        out.append(v & 0xFF)
    return bytes(out)


def raw_image(pix, depth, ctype, filters):
    bpp = max(1, depth * CHANNELS[ctype] // 8)
    out = bytearray()
    prev = None
    for y, row in enumerate(pix):
        packed = pack_row(row, depth, ctype)
        out += filter_row(filters[y % len(filters)], packed, prev, bpp)
        prev = packed
    return bytes(out)


PASSES = [(0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 0, 4, 4),
          (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2)]


def interlaced(pix, depth, ctype, filters):
    h = len(pix)
    w = len(pix[0])
    out = bytearray()
    for (x0, y0, dx, dy) in PASSES:
        sub = [[pix[y][x] for x in range(x0, w, dx)] for y in range(y0, h, dy)]
        sub = [r for r in sub if r]
        if sub:
            out += raw_image(sub, depth, ctype, filters)
    return bytes(out)


def png(name, pix, depth, ctype, filters=(0,), interlace=0, before=(),
        after=(), level=6, strategy=zlib.Z_DEFAULT_STRATEGY, wbits=15,
        split=0, plte=None, trns=None, raw=None, ihdr=None):
    h = len(pix)
    w = len(pix[0]) if h else 0
    if raw is None:
        if interlace:
            raw = interlaced(pix, depth, ctype, filters)
        else:
            raw = raw_image(pix, depth, ctype, filters)
    co = zlib.compressobj(level, zlib.DEFLATED, wbits, 9, strategy)
    z = co.compress(raw) + co.flush()
    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", ihdr or struct.pack(">IIBBBBB", w, h, depth, ctype, 0, 0, interlace))
    for c in before:
        out += c
    if plte is not None:
        out += chunk(b"PLTE", bytes(v for rgb in plte for v in rgb))
    if trns is not None:
        out += chunk(b"tRNS", trns)
    if split:
        for i in range(0, len(z), split):
            out += chunk(b"IDAT", z[i:i + split])
    else:
        out += chunk(b"IDAT", z)
    for c in after:
        out += c
    out += chunk(b"IEND", b"")
    with open("data/" + name, "wb") as f:
        f.write(out)
    return out


def grid(w, h, f):
    return [[f(x, y) for x in range(w)] for y in range(h)]


ALL = (0, 1, 2, 3, 4)
# Colour types and depths.
png("gray1-checker.png", grid(8, 8, lambda x, y: ((x // 2 + y // 2) % 2,)), 1, 0, ALL)
png("gray2.png", grid(10, 3, lambda x, y: ((x + y) % 4,)), 2, 0, ALL)
png("gray4.png", grid(16, 4, lambda x, y: ((x + 3 * y) % 16,)), 4, 0, ALL)
png("gray8-gradient.png", grid(32, 16, lambda x, y: ((x * 8 + y * 4) % 256,)), 8, 0, ALL)
png("gray16.png", grid(16, 8, lambda x, y: ((x * 4096 + y * 257) % 65536,)), 16, 0, ALL)


def circle(x, y, w=32, h=32):
    dx, dy = x - w / 2 + 0.5, y - h / 2 + 0.5
    if dx * dx + dy * dy <= (w / 2 - 2) ** 2:
        return (200 + x % 50, 40 + 6 * y, 30 + 5 * x)
    return (255, 255, 255)


CIRCLE = grid(32, 32, circle)
png("rgb8-circle.png", CIRCLE, 8, 2, ALL)
png("rgb16.png", grid(8, 8, lambda x, y: (x * 8000, y * 9000, (x * y * 1000) % 65536)), 16, 2, ALL)

PAL16 = [(i * 16, 255 - i * 16, (i * 37) % 256) for i in range(16)]
png("pal1.png", grid(12, 5, lambda x, y: ((x + y) % 2,)), 1, 3, ALL, plte=[(0, 0, 0), (255, 200, 0)])
png("pal2.png", grid(9, 5, lambda x, y: ((x * y) % 4,)), 2, 3, ALL, plte=PAL16[:4])
png("pal4.png", grid(20, 6, lambda x, y: ((x + 2 * y) % 16,)), 4, 3, ALL, plte=PAL16)
FAV = [(0, 0, 0), (32, 96, 224), (250, 250, 250), (230, 60, 40)]


def favicon(x, y):
    if x in (0, 15) or y in (0, 15):
        return (0,)
    if 4 <= x <= 11 and 4 <= y <= 11:
        return (3,) if (x + y) % 3 else (2,)
    return (1,)


png("favicon-pal8.png", grid(16, 16, favicon), 8, 3, (4, 1), plte=FAV, trns=bytes([0, 255, 200]))
png("graya8.png", grid(12, 12, lambda x, y: (x * 20, (y * 21) % 256)), 8, 4, ALL)
png("graya16.png", grid(6, 6, lambda x, y: (x * 10000, 65535 - y * 9000)), 16, 4, ALL)
png("rgba8.png", grid(24, 24, lambda x, y: (x * 10, y * 10, 128, (x * y) % 256)), 8, 6, ALL)
png("rgba16.png", grid(5, 5, lambda x, y: (x * 13000, y * 13000, 40000, 65535 - x * y * 2000)), 16, 6, ALL)
# Adam7.
png("rgb8-interlaced.png", grid(13, 11, lambda x, y: (x * 19, y * 23, (x ^ y) * 15)), 8, 2, ALL, interlace=1)
png("gray1-interlaced.png", grid(9, 7, lambda x, y: ((x * y) % 2,)), 1, 0, ALL, interlace=1)
png("pal4-interlaced.png", grid(10, 10, lambda x, y: ((x + y) % 16,)), 4, 3, ALL, interlace=1, plte=PAL16)
png("rgba8-1x1-interlaced.png", [[(10, 20, 30, 40)]], 8, 6, interlace=1)
png("gray8-3x2-interlaced.png", grid(3, 2, lambda x, y: (x * 100 + y,)), 8, 0, ALL, interlace=1)
png("graya16-interlaced.png", grid(7, 5, lambda x, y: (x * 9000, y * 12000)), 16, 4, ALL, interlace=1)
# Transparency keys.
png("gray8-trns.png", grid(6, 4, lambda x, y: ((x * 51) % 256,)), 8, 0, trns=struct.pack(">H", 0))
png("rgb8-trns.png", grid(32, 32, circle), 8, 2, (1,), trns=struct.pack(">HHH", 255, 255, 255))
png("gray4-trns.png", grid(4, 4, lambda x, y: (x * 5,)), 4, 0, trns=struct.pack(">H", 5))
# zlib variants of one image.
png("circle-level0.png", CIRCLE, 8, 2, (0,), level=0)
png("circle-level1.png", CIRCLE, 8, 2, (2,), level=1)
png("circle-level9.png", CIRCLE, 8, 2, (4,), level=9)
png("circle-fixed.png", CIRCLE, 8, 2, (1,), strategy=zlib.Z_FIXED)
png("circle-huffman.png", CIRCLE, 8, 2, (3,), strategy=zlib.Z_HUFFMAN_ONLY)
png("circle-rle.png", CIRCLE, 8, 2, (0,), strategy=zlib.Z_RLE)
png("circle-window512.png", CIRCLE, 8, 2, (2,), wbits=9)
png("circle-idat1.png", CIRCLE, 8, 2, (4,), split=1)
png("circle-idat100.png", CIRCLE, 8, 2, (4,), split=100)


def text_chunks():
    return [
        chunk(b"tEXt", b"Title\x00Caf\xe9 menu"),
        chunk(b"tEXt", b"Author\x00Jos\xe9"),
        chunk(b"zTXt", b"Comment\x00\x00" + zlib.compress(b"Drawn by hand.\nSecond line.")),
        chunk(b"iTXt", b"Description\x00\x00\x00fr\x00Description\x00Un cercle rouge \xe2\x80\x94 tr\xc3\xa8s simple"),
        chunk(b"iTXt", b"Software\x00\x01\x00\x00\x00" + zlib.compress("mini_png ✓".encode())),
        chunk(b"tIME", struct.pack(">HBBBBB", 2024, 3, 9, 17, 42, 5)),
        chunk(b"prVt", b"private data"),
    ]


def info_chunks():
    return [
        chunk(b"gAMA", struct.pack(">I", 45455)),
        chunk(b"cHRM", struct.pack(">8I", 31270, 32900, 64000, 33000, 30000, 60000, 15000, 6000)),
        chunk(b"sRGB", b"\x00"),
        chunk(b"sBIT", b"\x05\x06\x05"),
    ]


png("annotated.png", CIRCLE, 8, 2, ALL, before=info_chunks(),
    after=text_chunks() + [chunk(b"pHYs", struct.pack(">IIB", 2835, 2835, 1))])
png("bkgd-phys.png", grid(4, 4, lambda x, y: (x * 60, y * 60, 90)), 8, 2,
    before=[chunk(b"bKGD", struct.pack(">HHH", 255, 255, 255)),
            chunk(b"pHYs", struct.pack(">IIB", 1, 2, 0))])
png("icc-iccp.png", grid(2, 2, lambda x, y: (x * 255, 0, y * 255)), 8, 2,
    before=[chunk(b"iCCP", b"Built-in sRGB\x00\x00" + zlib.compress(b"\x00" * 128))])


# Broken files.
def write(name, data):
    with open("data/broken/" + name, "wb") as f:
        f.write(data)


good = png("broken-base.png", grid(8, 4, lambda x, y: (x * 30, y * 60, 100)), 8, 2, ALL)
os.remove("data/broken-base.png")
write("bad-signature.png", b"\x89PNG\r\n\x1a\x0a"[:4] + b"\r\r\x1a\n" + good[8:])
write("truncated.png", good[:len(good) - 30])
bad = bytearray(good)
bad[29] ^= 1
write("bad-crc.png", bytes(bad))
write("no-iend.png", good[:-12])
write("data-after-iend.png", good + b"junk")
ihdr = good[8:33]
write("ihdr-not-first.png", good[:8] + chunk(b"gAMA", struct.pack(">I", 45455)) + good[8:])
write("two-ihdr.png", good[:33] + ihdr + good[33:])


def broken_png(name, **kw):
    out = png("tmp.png", **kw)
    os.remove("data/tmp.png")
    write(name, out)


P = grid(4, 3, lambda x, y: (x, y, 7))
broken_png("bad-depth.png", pix=grid(4, 3, lambda x, y: (1,)), depth=8, ctype=0,
           ihdr=struct.pack(">IIBBBBB", 4, 3, 3, 0, 0, 0, 0))
broken_png("bad-combo.png", pix=P, depth=8, ctype=2,
           ihdr=struct.pack(">IIBBBBB", 4, 3, 4, 2, 0, 0, 0))
broken_png("zero-width.png", pix=P, depth=8, ctype=2,
           ihdr=struct.pack(">IIBBBBB", 0, 3, 8, 2, 0, 0, 0))
broken_png("bad-interlace.png", pix=P, depth=8, ctype=2,
           ihdr=struct.pack(">IIBBBBB", 4, 3, 8, 2, 0, 0, 2))
broken_png("bad-filter-method.png", pix=P, depth=8, ctype=2,
           ihdr=struct.pack(">IIBBBBB", 4, 3, 8, 2, 0, 1, 0))
broken_png("no-plte.png", pix=grid(4, 3, lambda x, y: (x % 2,)), depth=8, ctype=3)
broken_png("plte-index.png", pix=grid(4, 3, lambda x, y: (x,)), depth=8, ctype=3,
           plte=[(0, 0, 0), (255, 255, 255)])
broken_png("plte-in-gray.png", pix=grid(4, 3, lambda x, y: (x,)), depth=8, ctype=0,
           plte=[(0, 0, 0)])
broken_png("trns-too-long.png", pix=grid(4, 3, lambda x, y: (x % 2,)), depth=8, ctype=3,
           plte=[(0, 0, 0), (9, 9, 9)], trns=b"\x00\x01\x02")
broken_png("bad-filter-type.png", pix=P, depth=8, ctype=2,
           raw=b"".join(bytes([5 if y == 1 else 0]) + bytes(12) for y in range(3)))
broken_png("short-data.png", pix=P, depth=8, ctype=2, raw=bytes(13 * 2 + 5))
broken_png("extra-data.png", pix=P, depth=8, ctype=2, raw=bytes(13 * 3 + 4))
broken_png("no-idat.png", pix=P, depth=8, ctype=2, raw=b"", split=10000)
# zlib-level damage: the chunk CRCs are right, the stream is not.
IH = struct.pack(">IIBBBBB", 4, 3, 8, 2, 0, 0, 0)
RAW = b"".join(bytes([0]) + bytes(range(y, y + 12)) for y in range(3))


def with_stream(name, z):
    out = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", IH) + chunk(b"IDAT", z) + chunk(b"IEND", b"")
    write(name, out)


Z = zlib.compress(RAW, 9)
with_stream("zlib-header.png", b"\x78\x9d" + Z[2:])
with_stream("zlib-method.png", b"\x79\x9c"[:0] + bytes([0x77, (31 - (0x77 * 256) % 31) % 31]) + Z[2:])
with_stream("zlib-truncated.png", Z[:len(Z) // 2])
with_stream("zlib-adler.png", Z[:-1] + bytes([Z[-1] ^ 0xFF]))


class Bits:
    def __init__(self):
        self.out = bytearray()
        self.acc = 0
        self.n = 0

    def put(self, v, n):
        self.acc |= v << self.n
        self.n += n
        while self.n >= 8:
            self.out.append(self.acc & 0xFF)
            self.acc >>= 8
            self.n -= 8

    def put_rev(self, code, n):
        r = 0
        for i in range(n):
            r = (r << 1) | ((code >> i) & 1)
        self.put(r, n)

    def done(self):
        if self.n:
            self.out.append(self.acc & 0xFF)
        return bytes(self.out)


b = Bits()
b.put(1, 1)
b.put(3, 2)
with_stream("zlib-block-type.png", b"\x78\x9c" + b.done() + b"\x00" * 8)
b = Bits()
b.put(1, 1)
b.put(0, 2)
st = b.done()
with_stream("zlib-stored-length.png", b"\x78\x01" + st + struct.pack("<HH", 39, 39) + RAW)
b = Bits()
b.put(1, 1)
b.put(1, 2)
b.put_rev(0x30 + 0, 8)            # literal 0
b.put_rev(257 - 256, 7)           # length 3
b.put_rev(4, 5)                   # distance code 4: 5..6, one extra bit
b.put(0, 1)
with_stream("zlib-too-far.png", b"\x78\x01" + b.done() + b"\x00" * 6)
write("unknown-critical.png", good[:33] + chunk(b"cRIT", b"x") + good[33:])
write("bad-chunk-name.png", good[:33] + chunk(b"a1b2", b"x") + good[33:])
idat_at = good.index(b"IDAT") - 4
write("idat-split-by-text.png", good[:idat_at] + chunk(b"IDAT", zlib.compress(RAW)[:10])
      + chunk(b"tEXt", b"k\x00v") + chunk(b"IDAT", zlib.compress(RAW)[10:]) + chunk(b"IEND", b""))
write("huge-length.png", good[:33] + struct.pack(">I", 0x7FFFFFF0) + b"tEXt" + b"abc")
write("empty.png", b"")

jobs = []
names = sorted(n for n in os.listdir("data") if n.endswith(".png"))
broken = sorted(os.listdir("data/broken"))
for n in names:
    jobs.append("check\t" + n)
for n in names:
    jobs.append("decode\t" + n)
for n in ["gray1-checker.png", "gray8-gradient.png", "rgb8-circle.png", "pal4.png",
          "favicon-pal8.png", "rgba8.png", "rgb16.png", "rgb8-interlaced.png",
          "graya16-interlaced.png", "circle-huffman.png"]:
    jobs.append("encode\t" + n)
for n in ["gray4.png", "rgb8-trns.png", "rgba8-1x1-interlaced.png"]:
    jobs.append("encode\t" + n + "\tstored")
for n in broken:
    jobs.append("check\tbroken/" + n)
for n in ["bad-filter-type.png", "plte-index.png", "zlib-adler.png"]:
    jobs.append("decode\tbroken/" + n)
with open("data/jobs.tsv", "w") as f:
    f.write("\n".join(jobs) + "\n")
