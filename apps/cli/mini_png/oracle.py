#!/usr/bin/env python3
"""The mirror: runs data/jobs.tsv as mini_png does, with Python's zlib for
inflating and checksums, and prints expected.out. Run mk.py first."""
import struct
import zlib

SIG = b"\x89PNG\r\n\x1a\n"
CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}
DEPTHS = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8), 4: (8, 16), 6: (8, 16)}
PASSES = [(0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 0, 4, 4),
          (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2)]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
          "Oct", "Nov", "Dec"]
INTENTS = ["perceptual", "relative colorimetric", "saturation",
           "absolute colorimetric"]


class Bad(Exception):
    pass


def describe(depth, ctype):
    if ctype == 0:
        return "%d-bit grayscale" % depth
    if ctype == 2:
        return "%d-bit RGB" % (3 * depth)
    if ctype == 3:
        return "%d-bit palette" % depth
    if ctype == 4:
        return "%d-bit grayscale+alpha" % (2 * depth)
    return "%d-bit RGB+alpha" % (4 * depth)


def inflate(z):
    try:
        return zlib.decompress(z)
    except zlib.error as e:
        msg = str(e)
        raise Bad("zlib: " + msg[msg.index("data: ") + 6:])


def show_text(b, enc):
    s = b.decode(enc)
    return s.replace("\\", "\\\\").replace("\n", "\\n")


def fixed4(v):
    return "%d.%04d" % (v // 100000, (v % 100000) // 10)


def name_of(t):
    out = ""
    for c in t:
        out += chr(c) if 32 < c < 127 else "\\x%02x" % c
    return out


def u16(b, i):
    return struct.unpack(">H", b[i:i + 2])[0]


class Png:
    pass


def walk(data, lines):
    """Checks the chunks and returns the image's header, palette,
    transparency and compressed data."""
    if len(data) < 8 or data[:8] != SIG:
        raise Bad("not a PNG file (bad signature)")
    img = Png()
    img.ihdr = None
    img.plte = None
    img.trns = None
    z = bytearray()
    pos = 8
    seen_idat = False
    prev = b""
    run = 0
    run_bytes = 0

    def end_run():
        nonlocal run, run_bytes
        if run > 1:
            lines.append("  (%d IDAT chunks, %d bytes)" % (run, run_bytes))
        run = 0
        run_bytes = 0

    while True:
        if pos == len(data):
            end_run()
            raise Bad("file doesn't end with an IEND chunk")
        if len(data) - pos < 8:
            end_run()
            raise Bad("truncated chunk header at offset 0x%05x" % pos)
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        t = data[pos + 4:pos + 8]
        name = name_of(t)
        if length > 0x7FFFFFFF:
            end_run()
            raise Bad("chunk %s at offset 0x%05x: invalid length %d" % (name, pos, length))
        if pos + 12 + length > len(data):
            end_run()
            raise Bad("chunk %s at offset 0x%05x: truncated (length %d, %d bytes left)"
                      % (name, pos, length, len(data) - pos - 8))
        if not all(65 <= c <= 90 or 97 <= c <= 122 for c in t):
            end_run()
            raise Bad("invalid chunk name %s at offset 0x%05x" % (name, pos))
        body = data[pos + 8:pos + 8 + length]
        crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        computed = zlib.crc32(t + body)
        if crc != computed:
            end_run()
            raise Bad("CRC error in chunk %s (computed %08x, expected %08x)" % (name, computed, crc))
        if t != b"IDAT" or prev != b"IDAT":
            end_run()
        head = "  chunk %s at offset 0x%05x, length %d" % (name, pos, length)
        detail = None
        if img.ihdr is None and t != b"IHDR":
            raise Bad("first chunk must be IHDR, not %s" % name)
        if t == b"IHDR":
            if img.ihdr is not None:
                raise Bad("multiple IHDR chunks")
            if length != 13:
                raise Bad("IHDR: invalid length %d" % length)
            w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", body)
            if w == 0 or h == 0 or w > 0x7FFFFFFF or h > 0x7FFFFFFF:
                raise Bad("IHDR: invalid image dimensions (%dx%d)" % (w, h))
            if ctype not in DEPTHS:
                raise Bad("IHDR: invalid color type %d" % ctype)
            if depth not in DEPTHS[ctype]:
                raise Bad("IHDR: invalid bit depth %d for color type %d" % (depth, ctype))
            if comp != 0:
                raise Bad("IHDR: invalid compression method %d" % comp)
            if filt != 0:
                raise Bad("IHDR: invalid filter method %d" % filt)
            if inter > 1:
                raise Bad("IHDR: invalid interlace method %d" % inter)
            img.ihdr = (w, h, depth, ctype, inter)
            detail = "%d x %d image, %s, %s" % (w, h, describe(depth, ctype),
                                                "interlaced" if inter else "non-interlaced")
        elif t == b"PLTE":
            ctype = img.ihdr[3]
            if ctype in (0, 4):
                raise Bad("PLTE not allowed in a grayscale image")
            if img.plte is not None:
                raise Bad("multiple PLTE chunks")
            if seen_idat:
                raise Bad("PLTE must come before IDAT")
            if length == 0 or length % 3 or length > 768:
                raise Bad("PLTE: invalid length %d" % length)
            n = length // 3
            if ctype == 3 and n > (1 << img.ihdr[2]):
                raise Bad("PLTE: too many entries (%d) for a %d-bit palette" % (n, img.ihdr[2]))
            img.plte = [tuple(body[3 * i:3 * i + 3]) for i in range(n)]
            detail = "%d palette entries" % n
        elif t == b"tRNS":
            ctype = img.ihdr[3]
            if seen_idat:
                raise Bad("tRNS must come before IDAT")
            if ctype in (4, 6):
                raise Bad("tRNS not allowed with an alpha channel")
            if ctype == 3:
                if img.plte is None:
                    raise Bad("tRNS before PLTE")
                if length > len(img.plte):
                    raise Bad("tRNS: %d entries, more than the %d palette entries" % (length, len(img.plte)))
                detail = "%d transparency entries" % length
            elif ctype == 0:
                if length != 2:
                    raise Bad("tRNS: invalid length %d" % length)
                detail = "gray = %d" % u16(body, 0)
            else:
                if length != 6:
                    raise Bad("tRNS: invalid length %d" % length)
                detail = "red = %d, green = %d, blue = %d" % (u16(body, 0), u16(body, 2), u16(body, 4))
            img.trns = bytes(body)
        elif t == b"IDAT":
            if seen_idat and prev != b"IDAT":
                raise Bad("IDAT chunks are not consecutive")
            if img.ihdr[3] == 3 and img.plte is None:
                raise Bad("palette image has no PLTE before IDAT")
            seen_idat = True
            z += body
            run += 1
            run_bytes += length
            if run > 1:
                head = None
        elif t == b"IEND":
            if length != 0:
                raise Bad("IEND: invalid length %d" % length)
            lines.append(head)
            pos += 12
            if pos < len(data):
                raise Bad("%d bytes of data after IEND" % (len(data) - pos))
            break
        elif t == b"gAMA":
            if length != 4:
                raise Bad("gAMA: invalid length %d" % length)
            g = struct.unpack(">I", body)[0]
            detail = "gamma %d.%05d" % (g // 100000, g % 100000)
        elif t == b"cHRM":
            if length != 32:
                raise Bad("cHRM: invalid length %d" % length)
            v = struct.unpack(">8I", body)
            detail = "white (%s, %s), red (%s, %s), green (%s, %s), blue (%s, %s)" % tuple(fixed4(x) for x in v)
        elif t == b"sRGB":
            if length != 1:
                raise Bad("sRGB: invalid length %d" % length)
            if body[0] > 3:
                raise Bad("sRGB: invalid rendering intent %d" % body[0])
            detail = "rendering intent: " + INTENTS[body[0]]
        elif t == b"sBIT":
            detail = "significant bits " + ", ".join(str(x) for x in body)
        elif t == b"bKGD":
            ctype = img.ihdr[3]
            if ctype == 3:
                detail = "background index %d" % body[0]
            elif ctype in (0, 4):
                detail = "background gray %d" % u16(body, 0)
            else:
                detail = "background red = %d, green = %d, blue = %d" % (u16(body, 0), u16(body, 2), u16(body, 4))
        elif t == b"pHYs":
            if length != 9:
                raise Bad("pHYs: invalid length %d" % length)
            x, y, unit = struct.unpack(">IIB", body)
            if unit == 1:
                detail = "%d x %d pixels/meter" % (x, y)
                if x == y:
                    detail += " (%d dpi)" % ((x * 254 + 5000) // 10000)
            else:
                detail = "%d x %d pixels, aspect ratio only" % (x, y)
        elif t == b"tIME":
            if length != 7:
                raise Bad("tIME: invalid length %d" % length)
            yy, mo, d, hh, mi, ss = struct.unpack(">HBBBBB", body)
            detail = "%d %s %d %02d:%02d:%02d UTC" % (d, MONTHS[mo - 1], yy, hh, mi, ss)
        elif t == b"tEXt":
            if 0 not in body:
                raise Bad("tEXt: missing null separator")
            k, v = body.split(b"\x00", 1)
            detail = "%s: %s" % (show_text(k, "latin-1"), show_text(v, "latin-1"))
        elif t == b"zTXt":
            if 0 not in body:
                raise Bad("zTXt: missing null separator")
            k, rest = body.split(b"\x00", 1)
            text = inflate(rest[1:])
            detail = "%s (compressed): %s" % (show_text(k, "latin-1"), show_text(text, "latin-1"))
        elif t == b"iTXt":
            k, rest = body.split(b"\x00", 1)
            flag, method = rest[0], rest[1]
            lang, rest = rest[2:].split(b"\x00", 1)
            trans, text = rest.split(b"\x00", 1)
            if flag:
                text = inflate(text)
            detail = "%s [%s, %s]%s: %s" % (show_text(k, "latin-1"), lang.decode() or "-",
                                            trans.decode() or "-",
                                            " (compressed)" if flag else "",
                                            show_text(text, "utf-8"))
        elif t == b"iCCP":
            k, rest = body.split(b"\x00", 1)
            detail = "profile %s, %d bytes" % (show_text(k, "latin-1"), len(inflate(rest[1:])))
        else:
            if t[0] & 32 == 0:
                raise Bad("unknown critical chunk %s" % name)
            detail = "unknown ancillary chunk"
        if head is not None:
            lines.append(head + (": " + detail if detail else ""))
        prev = t
        pos += 12 + length
    if not seen_idat:
        raise Bad("no IDAT chunks")
    img.z = bytes(z)
    return img


def paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def unfilter(raw, pos, rows, rowbytes, bpp, rowno):
    out = []
    prev = bytes(rowbytes)
    for y in range(rows):
        if pos + 1 + rowbytes > len(raw):
            raise Bad("image data too short (%d bytes)" % len(raw))
        f = raw[pos]
        if f > 4:
            raise Bad("row %d: invalid filter type %d" % (rowno + y, f))
        cur = bytearray(raw[pos + 1:pos + 1 + rowbytes])
        for i in range(rowbytes):
            a = cur[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1:
                cur[i] = (cur[i] + a) & 255
            elif f == 2:
                cur[i] = (cur[i] + b) & 255
            elif f == 3:
                cur[i] = (cur[i] + (a + b) // 2) & 255
            elif f == 4:
                cur[i] = (cur[i] + paeth(a, b, c)) & 255
        out.append(bytes(cur))
        prev = cur
        pos += 1 + rowbytes
    return out, pos


def samples(row, w, depth, ch):
    px = []
    if depth < 8:
        mask = (1 << depth) - 1
        for x in range(w):
            bit = x * depth
            px.append(((row[bit // 8] >> (8 - depth - bit % 8)) & mask,))
        return px
    step = depth // 8
    for x in range(w):
        p = []
        for k in range(ch):
            i = (x * ch + k) * step
            p.append(row[i] if step == 1 else (row[i] << 8) | row[i + 1])
        px.append(tuple(p))
    return px


def decode(img):
    """The image as rows of pixels (tuples of samples at the file's depth),
    and the size of the inflated data."""
    w, h, depth, ctype, inter = img.ihdr
    ch = CHANNELS[ctype]
    bpp = max(1, depth * ch // 8)
    raw = inflate(img.z)
    pix = [[None] * w for _ in range(h)]
    pos = 0
    rowno = 0
    passes = PASSES if inter else [(0, 0, 1, 1)]
    for (x0, y0, dx, dy) in passes:
        pw = (w - x0 + dx - 1) // dx if w > x0 else 0
        ph = (h - y0 + dy - 1) // dy if h > y0 else 0
        if pw == 0 or ph == 0:
            continue
        rowbytes = (pw * depth * ch + 7) // 8
        rows, pos = unfilter(raw, pos, ph, rowbytes, bpp, rowno)
        rowno += ph
        for j, row in enumerate(rows):
            for i, p in enumerate(samples(row, pw, depth, ch)):
                pix[y0 + j * dy][x0 + i * dx] = p
    if pos != len(raw):
        raise Bad("image data too long (%d bytes, %d used)" % (len(raw), pos))
    if ctype == 3:
        for row in pix:
            for p in row:
                if p[0] >= len(img.plte):
                    raise Bad("palette index %d out of range (%d entries)" % (p[0], len(img.plte)))
    return pix, len(raw)


def rgba(img, p):
    w, h, depth, ctype, inter = img.ihdr
    t = img.trns
    if ctype == 3:
        r, g, b = img.plte[p[0]]
        a = t[p[0]] if t is not None and p[0] < len(t) else 255
        return (r, g, b, a)

    def to8(v):
        if depth == 16:
            return v >> 8
        if depth == 8:
            return v
        return v * 255 // ((1 << depth) - 1)
    if ctype == 0:
        v = to8(p[0])
        a = 0 if t is not None and p[0] == u16(t, 0) else 255
        return (v, v, v, a)
    if ctype == 4:
        v = to8(p[0])
        return (v, v, v, to8(p[1]))
    if ctype == 2:
        a = 0 if t is not None and p == (u16(t, 0), u16(t, 2), u16(t, 4)) else 255
        return (to8(p[0]), to8(p[1]), to8(p[2]), a)
    return tuple(to8(v) for v in p)


def ratio(raw, comp):
    num = 1000 * (raw - comp)
    q = num // raw if num >= 0 else -((-num) // raw)
    sign = "-" if q < 0 else ""
    q = abs(q)
    return "%s%d.%d%%" % (sign, q // 10, q % 10)


def load(path, lines):
    with open("data/" + path, "rb") as f:
        data = f.read()
    img = walk(data, lines)
    pix, rawlen = decode(img)
    return img, pix, rawlen, data


def check(path):
    lines = []
    try:
        img, pix, rawlen, data = load(path, lines)
        w, h, depth, ctype, inter = img.ihdr
        lines.append("  OK: %s (%dx%d, %s, %s, %s)" % (
            path, w, h, describe(depth, ctype),
            "interlaced" if inter else "non-interlaced", ratio(rawlen, len(img.z))))
    except Bad as e:
        lines.append("  ERROR: %s" % e)
    print("\n".join(lines))


RAMP = "@%#*+=-:. "


def show_decode(path):
    lines = []
    try:
        img, pix, rawlen, data = load(path, lines)
    except Bad as e:
        print("  ERROR: %s" % e)
        return
    w, h, depth, ctype, inter = img.ihdr
    buf = bytearray()
    opaque = clear = part = 0
    for row in pix:
        for p in row:
            q = rgba(img, p)
            buf += bytes(q)
            if q[3] == 255:
                opaque += 1
            elif q[3] == 0:
                clear += 1
            else:
                part += 1
    print("  %dx%d %s, %d pixels, RGBA crc32 %08x" % (w, h, describe(depth, ctype), w * h, zlib.crc32(buf)))
    print("  alpha: %d opaque, %d transparent, %d partial" % (opaque, clear, part))
    cols = min(w, 32)
    rows = min(h, 16)
    for r in range(rows):
        y = r * h // rows
        line = ""
        for c in range(cols):
            x = c * w // cols
            red, g, b, a = rgba(img, pix[y][x])
            red = (red * a + 255 * (255 - a)) // 255
            g = (g * a + 255 * (255 - a)) // 255
            b = (b * a + 255 * (255 - a)) // 255
            lum = (299 * red + 587 * g + 114 * b) // 1000
            line += RAMP[lum * 10 // 256]
        print("  |" + line + "|")


# ------------------------------------------------------------- encoder

def pack(row, depth, ch):
    if depth < 8:
        out = bytearray()
        acc = 0
        n = 0
        for p in row:
            acc = (acc << depth) | p[0]
            n += depth
            if n == 8:
                out.append(acc)
                acc = 0
                n = 0
        if n:
            out.append(acc << (8 - n))
        return bytes(out)
    out = bytearray()
    for p in row:
        for v in p:
            if depth == 8:
                out.append(v)
            else:
                out += bytes([v >> 8, v & 255])
    return bytes(out)


def filtered(f, row, prev, bpp):
    out = bytearray()
    for i, x in enumerate(row):
        a = row[i - bpp] if i >= bpp else 0
        b = prev[i]
        c = prev[i - bpp] if i >= bpp else 0
        if f == 0:
            v = x
        elif f == 1:
            v = x - a
        elif f == 2:
            v = x - b
        elif f == 3:
            v = x - (a + b) // 2
        else:
            v = x - paeth(a, b, c)
        out.append(v & 255)
    return bytes(out)


class BitWriter:
    def __init__(self):
        self.out = bytearray()
        self.acc = 0
        self.n = 0

    def put(self, v, n):
        self.acc |= v << self.n
        self.n += n
        while self.n >= 8:
            self.out.append(self.acc & 255)
            self.acc >>= 8
            self.n -= 8

    def code(self, c, n):
        r = 0
        for i in range(n):
            r = (r << 1) | ((c >> i) & 1)
        self.put(r, n)

    def finish(self):
        if self.n:
            self.out.append(self.acc & 255)
            self.acc = 0
            self.n = 0
        return bytes(self.out)


LEN_BASE = [3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27, 31, 35, 43,
            51, 59, 67, 83, 99, 115, 131, 163, 195, 227, 258]
LEN_EXTRA = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4,
             4, 4, 5, 5, 5, 5, 0]
DIST_BASE = [1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257,
             385, 513, 769, 1025, 1537, 2049, 3073, 4097, 6145, 8193, 12289,
             16385, 24577]
DIST_EXTRA = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9,
              9, 10, 10, 11, 11, 12, 12, 13, 13]


def put_lit(bw, v):
    if v < 144:
        bw.code(0x30 + v, 8)
    elif v < 256:
        bw.code(0x190 + v - 144, 9)
    elif v < 280:
        bw.code(v - 256, 7)
    else:
        bw.code(0xC0 + v - 280, 8)


def deflate_fixed(data):
    bw = BitWriter()
    bw.put(1, 1)
    bw.put(1, 2)
    chains = {}
    n = len(data)
    i = 0

    def insert(p):
        if p + 3 <= n:
            chains.setdefault(data[p:p + 3], []).append(p)

    while i < n:
        best = 0
        dist = 0
        if i + 3 <= n:
            cands = chains.get(data[i:i + 3], [])
            tried = 0
            k = len(cands) - 1
            while k >= 0 and tried < 64:
                p = cands[k]
                if i - p > 32768:
                    break
                limit = min(258, n - i)
                m = 0
                while m < limit and data[p + m] == data[i + m]:
                    m += 1
                if m > best:
                    best = m
                    dist = i - p
                    if m == limit:
                        break
                tried += 1
                k -= 1
        if best >= 3:
            c = 0
            while c + 1 < len(LEN_BASE) and LEN_BASE[c + 1] <= best:
                c += 1
            put_lit(bw, 257 + c)
            bw.put(best - LEN_BASE[c], LEN_EXTRA[c])
            d = 0
            while d + 1 < len(DIST_BASE) and DIST_BASE[d + 1] <= dist:
                d += 1
            bw.code(d, 5)
            bw.put(dist - DIST_BASE[d], DIST_EXTRA[d])
            for p in range(i, i + best):
                insert(p)
            i += best
        else:
            put_lit(bw, data[i])
            insert(i)
            i += 1
    put_lit(bw, 256)
    return bw.finish()


def deflate_stored(data):
    out = bytearray()
    i = 0
    while True:
        part = data[i:i + 65535]
        last = i + 65535 >= len(data)
        out.append(1 if last else 0)
        out += struct.pack("<HH", len(part), len(part) ^ 0xFFFF)
        out += part
        i += 65535
        if last:
            return bytes(out)


def zchunk(kind, data):
    return (struct.pack(">I", len(data)) + kind + data
            + struct.pack(">I", zlib.crc32(kind + data)))


def encode(path, stored):
    lines = []
    try:
        img, pix, rawlen, data = load(path, lines)
    except Bad as e:
        print("  ERROR: %s" % e)
        return
    w, h, depth, ctype, inter = img.ihdr
    ch = CHANNELS[ctype]
    bpp = max(1, depth * ch // 8)
    raw = bytearray()
    counts = [0] * 5
    prev = bytes((w * depth * ch + 7) // 8)
    for row in pix:
        cur = pack(row, depth, ch)
        best = None
        for f in range(5):
            fr = filtered(f, cur, prev, bpp)
            score = sum(b if b < 128 else 256 - b for b in fr)
            if best is None or score < best[0]:
                best = (score, f, fr)
        counts[best[1]] += 1
        raw += bytes([best[1]]) + best[2]
        prev = cur
    body = deflate_stored(bytes(raw)) if stored else deflate_fixed(bytes(raw))
    z = b"\x78\x01" + body + struct.pack(">I", zlib.adler32(bytes(raw)))
    assert zlib.decompress(z) == bytes(raw)
    out = SIG + zchunk(b"IHDR", struct.pack(">IIBBBBB", w, h, depth, ctype, 0, 0, 0))
    if img.plte is not None:
        out += zchunk(b"PLTE", bytes(v for rgb in img.plte for v in rgb))
    if img.trns is not None:
        out += zchunk(b"tRNS", img.trns)
    out += zchunk(b"IDAT", z) + zchunk(b"IEND", b"")
    print("  filters: none %d, sub %d, up %d, average %d, paeth %d" % tuple(counts))
    print("  wrote %d bytes (was %d), IDAT %d bytes, crc32 %08x" % (len(out), len(data), len(z), zlib.crc32(out)))
    img2 = walk(out, [])
    pix2, _ = decode(img2)
    same = all(rgba(img, a) == rgba(img2, b) for ra, rb in zip(pix, pix2) for a, b in zip(ra, rb))
    print("  read back: %s" % ("same pixels" if same else "DIFFERENT pixels"))


def main():
    with open("data/jobs.tsv") as f:
        jobs = f.read().split("\n")[:-1]
    for job in jobs:
        f = job.split("\t")
        print("== " + " ".join(f))
        if f[0] == "check":
            check(f[1])
        elif f[0] == "decode":
            show_decode(f[1])
        else:
            encode(f[1], len(f) > 2)


main()
