# Python mirror of mini_xz: runs data/jobs.txt with a port of XZ Utils
# 5.4.5's xz (the .xz and .lzma decoders, -t, -d and -l with -v and -vv)
# and sha256sum.
import hashlib, os, shutil, sys

out = []
err = []
def w(s):
    out.append(s)
def we(s):
    err.append(s)

# ---- checksums ----
def crc32(data):
    c = 0xFFFFFFFF
    for b in data:
        c ^= b
        for _ in range(8):
            c = (c >> 1) ^ 0xEDB88320 if c & 1 else c >> 1
    return c ^ 0xFFFFFFFF

C64 = []
for i in range(256):
    c = i
    for _ in range(8):
        c = (c >> 1) ^ 0xC96C5795D7870F42 if c & 1 else c >> 1
    C64.append(c)

def crc64(data):
    c = 0xFFFFFFFFFFFFFFFF
    for b in data:
        c = C64[(c ^ b) & 0xFF] ^ (c >> 8)
    return c ^ 0xFFFFFFFFFFFFFFFF

CHECK_SIZE = {0: 0, 1: 4, 4: 8, 10: 32}
CHECK_NAME = {0: "None", 1: "CRC32", 4: "CRC64", 10: "SHA-256"}

def check_of(cid, data):
    if cid == 0:
        return b""
    if cid == 1:
        return crc32(data).to_bytes(4, "little")
    if cid == 4:
        return crc64(data).to_bytes(8, "little")
    return hashlib.sha256(data).digest()

class Fail(Exception):
    pass  # "eof", "data", "format", "options"

MSG = {"eof": "Unexpected end of input", "data": "Compressed data is corrupt",
       "format": "File format not recognized", "options": "Unsupported options"}

# ---- the LZMA decoder ----
class RC:
    def __init__(self, data, pos, end, eof_kind):
        # end: where this coder's input stops; reading past it is eof_kind
        self.d = data; self.p = pos; self.end = end; self.kind = eof_kind
        if self.byte() != 0:
            raise Fail("data")
        self.range = 0xFFFFFFFF
        self.code = 0
        for _ in range(4):
            self.code = (self.code << 8) | self.byte()
    def byte(self):
        if self.p >= self.end:
            raise Fail(self.kind)
        b = self.d[self.p]; self.p += 1
        return b
    def norm(self):
        if self.range < 0x1000000:
            self.range = (self.range << 8) & 0xFFFFFFFF
            self.code = ((self.code << 8) | self.byte()) & 0xFFFFFFFF
    def bit(self, probs, i):
        p = probs[i]
        bound = (self.range >> 11) * p
        if self.code < bound:
            self.range = bound
            probs[i] = p + ((2048 - p) >> 5)
            b = 0
        else:
            self.range -= bound
            self.code -= bound
            probs[i] = p - (p >> 5)
            b = 1
        self.norm()
        return b
    def tree(self, probs, base, nbits):
        m = 1
        for _ in range(nbits):
            m = (m << 1) | self.bit(probs, base + m)
        return m - (1 << nbits)
    def rtree(self, probs, base, nbits):
        m = 1; sym = 0
        for i in range(nbits):
            b = self.bit(probs, base + m)
            m = (m << 1) | b
            sym |= b << i
        return sym
    def direct(self, nbits):
        res = 0
        for _ in range(nbits):
            self.range >>= 1
            if self.code >= self.range:
                self.code -= self.range; b = 1
            else:
                b = 0
            res = (res << 1) | b
            self.norm()
        return res

class LenDec:
    def __init__(self):
        self.p = [1024] * (2 + 16 * 8 * 2 + 256)
    # layout: 0 choice, 1 choice2, 2.. low[16][8], 130.. mid[16][8], 258.. high
    def decode(self, rc, ps):
        if rc.bit(self.p, 0) == 0:
            return self.t(rc, 2 + ps * 8, 3)
        if rc.bit(self.p, 1) == 0:
            return 8 + self.t(rc, 130 + ps * 8, 3)
        return 16 + self.t(rc, 258, 8)
    def t(self, rc, base, nbits):
        # a bit tree whose node m is at base + m - 1
        m = 1
        for _ in range(nbits):
            m = (m << 1) | rc.bit(self.p, base + m - 1)
        return m - (1 << nbits)

class LZMA:
    def __init__(self, lc, lp, pb):
        self.lc, self.lp, self.pb = lc, lp, pb
        self.reset()
    def reset(self):
        self.state = 0
        self.reps = [0, 0, 0, 0]
        self.is_match = [1024] * (12 * 16)
        self.is_rep = [1024] * 12
        self.g0 = [1024] * 12
        self.g1 = [1024] * 12
        self.g2 = [1024] * 12
        self.rep0_long = [1024] * (12 * 16)
        self.lit = [1024] * (0x300 << (self.lc + self.lp))
        self.slot = [1024] * (4 * 64)
        self.spec = [1024] * 115
        self.align = [1024] * 16
        self.lens = LenDec()
        self.replens = LenDec()
    # Decodes into dict (a bytearray holding the whole output since the
    # last dictionary reset) until it has `until` bytes, or until the end
    # marker when until is None. Returns True if it stopped at the marker.
    def run(self, rc, dic, until, dict_size):
        pbm = (1 << self.pb) - 1; lpm = (1 << self.lp) - 1
        while until is None or len(dic) < until:
            pos = len(dic)
            ps = pos & pbm
            st = self.state
            if rc.bit(self.is_match, st * 16 + ps) == 0:
                prev = dic[-1] if dic else 0
                base = 0x300 * (((pos & lpm) << self.lc) + (prev >> (8 - self.lc)))
                sym = 1
                if st >= 7:
                    mb = dic[pos - self.reps[0] - 1]
                    while sym < 0x100:
                        mbit = (mb >> 7) & 1; mb <<= 1
                        b = rc.bit(self.lit, base + 0x100 + (mbit << 8) + sym)
                        sym = (sym << 1) | b
                        if mbit != b:
                            break
                while sym < 0x100:
                    sym = (sym << 1) | rc.bit(self.lit, base + sym)
                dic.append(sym - 0x100)
                self.state = 0 if st < 4 else st - 3 if st < 10 else st - 6
                continue
            if rc.bit(self.is_rep, st) == 0:
                ln = self.lens.decode(rc, ps)
                self.state = 7 if st < 7 else 10
                r = self.reps
                r[3] = r[2]; r[2] = r[1]; r[1] = r[0]
                ls = ln if ln < 3 else 3
                slot = rc.tree(self.slot, ls * 64, 6)
                if slot < 4:
                    dist = slot
                else:
                    nd = (slot >> 1) - 1
                    dist = (2 | (slot & 1)) << nd
                    if slot < 14:
                        dist += rc.rtree(self.spec, dist - slot - 1, nd)
                    else:
                        dist += rc.direct(nd - 4) << 4
                        dist += rc.rtree(self.align, -1, 4)
                if dist == 0xFFFFFFFF:
                    return True
                r[0] = dist
            else:
                r = self.reps
                if rc.bit(self.g0, st) == 0:
                    if rc.bit(self.rep0_long, st * 16 + ps) == 0:
                        self.state = 9 if st < 7 else 11
                        if r[0] >= pos:
                            raise Fail("data")
                        dic.append(dic[pos - r[0] - 1])
                        continue
                else:
                    if rc.bit(self.g1, st) == 0:
                        d = r[1]
                    else:
                        if rc.bit(self.g2, st) == 0:
                            d = r[2]
                        else:
                            d = r[3]; r[3] = r[2]
                        r[2] = r[1]
                    r[1] = r[0]; r[0] = d
                ln = self.replens.decode(rc, ps)
                self.state = 8 if st < 7 else 11
            dist = self.reps[0]
            if dist >= pos or dist >= dict_size:
                raise Fail("data")
            n = ln + 2
            if until is not None and pos + n > until:
                raise Fail("data")
            for _ in range(n):
                dic.append(dic[len(dic) - dist - 1])
        return False

def lclppb(b):
    if b > 224:
        raise Fail("options")
    lc = b % 9; b //= 9
    return lc, b % 5, b // 5

def dict_of_prop(b):
    if b > 40:
        raise Fail("options")
    if b == 40:
        return 0xFFFFFFFF
    return (2 | (b & 1)) << (b // 2 + 11)

def lzma2_decode(data, pos, end, dict_size):
    # LZMA2 chunks from data[pos:end]; returns (output, position after the end byte)
    out = bytearray()
    dic = bytearray()
    lz = None
    need_reset = True; need_props = True
    while True:
        if pos >= end:
            raise Fail("eof")
        c = data[pos]; pos += 1
        if c == 0:
            out += dic
            return out, pos
        if c >= 0xE0 or c == 1:
            need_props = True; need_reset = False
            out += dic; dic = bytearray()
        elif need_reset:
            raise Fail("data")
        if c >= 0x80:
            if pos + 4 > end:
                raise Fail("eof")
            usize = ((c & 0x1F) << 16) + (data[pos] << 8) + data[pos + 1] + 1
            csize = (data[pos + 2] << 8) + data[pos + 3] + 1
            pos += 4
            if c >= 0xC0:
                if pos >= end:
                    raise Fail("eof")
                lc, lp, pb = lclppb(data[pos]); pos += 1
                if lc + lp > 4:
                    raise Fail("data")
                need_props = False
                lz = LZMA(lc, lp, pb)
            elif need_props:
                raise Fail("data")
            elif c >= 0xA0:
                lz.reset()
            if pos + csize > end:
                # the chunk runs past the input
                cend = end; kind = "eof"
            else:
                cend = pos + csize; kind = "data"
            rc = RC(data, pos, cend, kind)
            if lz.run(rc, dic, len(dic) + usize, dict_size):
                raise Fail("data")
            if rc.code != 0 or rc.p != pos + csize:
                raise Fail("data")
            pos += csize
        elif c <= 2:
            if pos + 2 > end:
                raise Fail("eof")
            size = (data[pos] << 8) + data[pos + 1] + 1
            pos += 2
            if pos + size > end:
                raise Fail("eof")
            dic += data[pos:pos + size]
            pos += size
        else:
            raise Fail("data")

# ---- BCJ x86 and delta ----
def x86_decode(buf):
    allowed = [True, True, True, False, True, False, False, False]
    bitnum = [0, 1, 2, 2, 3, 3, 3, 3]
    M = 0xFFFFFFFF
    prev_mask = 0; prev_pos = (-5) & M
    size = len(buf)
    if size < 5:
        return
    i = 0
    while i <= size - 5:
        b = buf[i]
        if b != 0xE8 and b != 0xE9:
            i += 1; continue
        off = (i - prev_pos) & M
        prev_pos = i
        if off > 5:
            prev_mask = 0
        else:
            for _ in range(off):
                prev_mask &= 0x77; prev_mask <<= 1
        b = buf[i + 4]
        if (b == 0 or b == 0xFF) and allowed[(prev_mask >> 1) & 7] and (prev_mask >> 1) < 0x10:
            src = (b << 24) | (buf[i + 3] << 16) | (buf[i + 2] << 8) | buf[i + 1]
            while True:
                dest = (src - (i + 5)) & M
                if prev_mask == 0:
                    break
                j = bitnum[prev_mask >> 1]
                b = (dest >> (24 - j * 8)) & 0xFF
                if not (b == 0 or b == 0xFF):
                    break
                src = dest ^ ((1 << (32 - j * 8)) - 1)
            buf[i + 4] = 0xFF if (dest >> 24) & 1 else 0
            buf[i + 3] = (dest >> 16) & 0xFF
            buf[i + 2] = (dest >> 8) & 0xFF
            buf[i + 1] = dest & 0xFF
            i += 5
            prev_mask = 0
        else:
            i += 1
            prev_mask |= 1
            if b == 0 or b == 0xFF:
                prev_mask |= 0x10

def delta_decode(buf, dist):
    for i in range(dist, len(buf)):
        buf[i] = (buf[i] + buf[i - dist]) & 0xFF

# ---- .xz structures ----
def vli(data, pos, end):
    v = 0
    for i in range(9):
        if pos >= end:
            raise Fail("eof")
        b = data[pos]; pos += 1
        v |= (b & 0x7F) << (7 * i)
        if b & 0x80 == 0:
            if b == 0 and i > 0:
                raise Fail("data")
            return v, pos
    raise Fail("data")

MAGIC = b"\xfd7zXZ\x00"

def stream_flags(data, pos, first):
    # a Stream Header at pos; returns the check id
    if data[pos:pos + 6] != MAGIC:
        raise Fail("format" if first else "data")
    fl = data[pos + 6:pos + 8]
    if crc32(fl) != int.from_bytes(data[pos + 8:pos + 12], "little"):
        raise Fail("data")
    if fl[0] != 0 or fl[1] & 0xF0:
        raise Fail("options")
    return fl[1]

def footer(data, pos):
    # a Stream Footer at pos; returns (backward size, check id)
    if data[pos + 10:pos + 12] != b"YZ":
        raise Fail("data")
    if crc32(data[pos + 4:pos + 10]) != int.from_bytes(data[pos:pos + 4], "little"):
        raise Fail("data")
    fl = data[pos + 8:pos + 10]
    if fl[0] != 0 or fl[1] & 0xF0:
        raise Fail("options")
    return (int.from_bytes(data[pos + 4:pos + 8], "little") + 1) * 4, fl[1]

FILTER_NAMES = {0x21: "lzma2", 0x03: "delta", 0x04: "x86"}

def block_header(data, pos, end):
    # returns a dict: size, csize, usize (or None), filters [(id, props)]
    if pos >= end:
        raise Fail("eof")
    hsize = (data[pos] + 1) * 4
    if pos + hsize > end:
        raise Fail("eof")
    h = data[pos:pos + hsize]
    if crc32(h[:-4]) != int.from_bytes(h[-4:], "little"):
        raise Fail("data")
    fl = h[1]
    if fl & 0x3C:
        raise Fail("options")
    p = 2
    hend = hsize - 4
    csize = usize = None
    if fl & 0x40:
        csize, p = vli(h, p, hend)
        if csize == 0:
            raise Fail("data")
    if fl & 0x80:
        usize, p = vli(h, p, hend)
    filters = []
    for _ in range((fl & 3) + 1):
        fid, p = vli(h, p, hend)
        psz, p = vli(h, p, hend)
        if p + psz > hend:
            raise Fail("data")
        filters.append((fid, bytes(h[p:p + psz])))
        p += psz
    for b in h[p:hend]:
        if b != 0:
            raise Fail("options")
    for fid, _ in filters:
        if fid not in FILTER_NAMES:
            raise Fail("options")
    if filters[-1][0] != 0x21 or any(f[0] == 0x21 for f in filters[:-1]):
        raise Fail("options")
    return {"size": hsize, "csize": csize, "usize": usize, "filters": filters}

def decode_xz(data, sink):
    pos = 0
    first = True
    while True:
        if len(data) - pos < 12:
            raise Fail("eof")
        cid = stream_flags(data, pos, first)
        first = False
        pos += 12
        csz = CHECK_SIZE.get(cid, 0)
        records = []
        while True:
            if pos >= len(data):
                raise Fail("eof")
            if data[pos] == 0:
                break
            bh = block_header(data, pos, len(data))
            start = pos
            pos += bh["size"]
            props = bh["filters"][-1][1]
            if len(props) != 1:
                raise Fail("options")
            dsize = dict_of_prop(props[0])
            limit = len(data) if bh["csize"] is None else min(len(data), pos + bh["csize"])
            ud, npos = lzma2_decode(data, pos, limit, dsize)
            if bh["csize"] is not None and npos - pos != bh["csize"]:
                raise Fail("data")
            if bh["usize"] is not None and len(ud) != bh["usize"]:
                raise Fail("data")
            for fid, fp in reversed(bh["filters"][:-1]):
                if fid == 0x04:
                    x86_decode(ud)
                elif fid == 0x03:
                    delta_decode(ud, fp[0] + 1)
            pos = npos
            while (pos - start) % 4:
                if pos >= len(data):
                    raise Fail("eof")
                if data[pos] != 0:
                    raise Fail("data")
                pos += 1
            if pos + csz > len(data):
                raise Fail("eof")
            if cid in CHECK_SIZE and data[pos:pos + csz] != check_of(cid, ud):
                raise Fail("data")
            pos += csz
            records.append((npos - start + csz, len(ud)))
            sink += ud
        # the index must list the blocks
        istart = pos
        pos += 1
        n, pos = vli(data, pos, len(data))
        if n != len(records):
            raise Fail("data")
        for unp, usz in records:
            a, pos = vli(data, pos, len(data))
            b, pos = vli(data, pos, len(data))
            if a != unp or b != usz:
                raise Fail("data")
        while (pos - istart) % 4:
            if pos >= len(data):
                raise Fail("eof")
            if data[pos] != 0:
                raise Fail("data")
            pos += 1
        if pos + 4 > len(data):
            raise Fail("eof")
        if crc32(data[istart:pos]) != int.from_bytes(data[pos:pos + 4], "little"):
            raise Fail("data")
        pos += 4
        if pos + 12 > len(data):
            raise Fail("eof")
        bsize, fcid = footer(data, pos)
        if fcid != cid or bsize != pos - istart:
            raise Fail("data")
        pos += 12
        # stream padding, then maybe another stream
        pad = 0
        while pos < len(data) and data[pos] == 0:
            pos += 1; pad += 1
        if pad % 4:
            raise Fail("data")
        if pos >= len(data):
            return

def is_lzma(data):
    if len(data) < 13 or data[0] > 224:
        return False
    d = int.from_bytes(data[1:5], "little")
    if d != 0xFFFFFFFF:
        x = d - 1
        x |= x >> 2; x |= x >> 3; x |= x >> 4; x |= x >> 8; x |= x >> 16
        x += 1
        if x != d:
            return False
    u = int.from_bytes(data[5:13], "little")
    return u == 0xFFFFFFFFFFFFFFFF or u <= (1 << 38)

def decode_lzma(data, sink):
    lc, lp, pb = lclppb(data[0])
    d = int.from_bytes(data[1:5], "little")
    u = int.from_bytes(data[5:13], "little")
    lz = LZMA(lc, lp, pb)
    rc = RC(data, 13, len(data), "eof")
    dic = bytearray()
    if u == 0xFFFFFFFFFFFFFFFF:
        lz.run(rc, dic, None, max(d, 4096))
    else:
        lz.run(rc, dic, u, max(d, 4096))
    if rc.code != 0:
        raise Fail("data")
    sink += dic

def decode_file(data, sink):
    if data[:6] == MAGIC:
        decode_xz(data, sink)
    elif is_lzma(data):
        decode_lzma(data, sink)
    else:
        raise Fail("format")

# ---- listing, as lzma_file_info_decoder reads a file ----
def file_info(data):
    stream_flags(data, 0, True)
    streams = []
    pos = len(data)
    while pos > 0:
        pad = 0
        while pos >= 4 and data[pos - 4:pos] == b"\0\0\0\0":
            pos -= 4; pad += 4
        if pos < 24:
            raise Fail("data")
        bsize, cid = footer(data, pos - 12)
        istart = pos - 12 - bsize
        if istart < 12:
            raise Fail("data")
        p = istart
        if data[p] != 0:
            raise Fail("data")
        n, p = vli(data, p + 1, pos - 12)
        recs = []
        for _ in range(n):
            a, p = vli(data, p, pos - 12)
            b, p = vli(data, p, pos - 12)
            if a < 5 or a > (1 << 63):
                raise Fail("data")
            recs.append((a, b))
        while (p - istart) % 4:
            if p >= pos - 12 or data[p] != 0:
                raise Fail("data")
            p += 1
        if p + 4 != pos - 12 or crc32(data[istart:p]) != int.from_bytes(data[p:p + 4], "little"):
            raise Fail("data")
        blocks_size = sum((a + 3) // 4 * 4 for a, _ in recs)
        start = istart - blocks_size - 12
        if start < 0:
            raise Fail("data")
        try:
            hcid = stream_flags(data, start, False)
        except Fail as e:
            raise Fail("data" if e.args[0] == "format" else e.args[0])
        if hcid != cid:
            raise Fail("data")
        streams.append({"start": start, "size": pos - start, "check": cid, "pad": pad, "recs": recs})
        pos = start
    streams.reverse()
    uoff = 0
    for s in streams:
        s["uoff"] = uoff
        s["usize"] = sum(b for _, b in s["recs"])
        uoff += s["usize"]
    return streams

def nice(v, also_bytes=False):
    if v < 10000:
        s = f"{v} B"
    else:
        d = float(v); unit = 0
        while True:
            d /= 1024.0; unit += 1
            if not (d > 9999.9 and unit < 4):
                break
        s = f"{d:.1f} {['B', 'KiB', 'MiB', 'GiB', 'TiB'][unit]}"
        if also_bytes:
            s += f" ({v} B)"
    return s

def ratio(c, u):
    if u == 0:
        return "---"
    r = c / u
    return "---" if r > 9.999 else f"{r:.3f}"

def check_names(ids, sep):
    return sep.join(CHECK_NAME.get(i, f"Unknown-{i}") for i in sorted(ids))

def dict_str(d):
    if d % (1 << 20) == 0:
        return f"{d >> 20}MiB"
    if d % 1024 == 0:
        return f"{d >> 10}KiB"
    return str(d)

def filter_str(filters):
    parts = []
    for fid, props in filters:
        if fid == 0x21:
            parts.append(f"--lzma2=dict={dict_str(dict_of_prop(props[0]))}")
        elif fid == 0x03:
            parts.append(f"--delta=dist={props[0] + 1}")
        elif fid == 0x04:
            start = int.from_bytes(props, "little") if props else 0
            parts.append("--x86" + (f"=start={start}" if start else ""))
    return " ".join(parts)

def memusage(filters):
    m = 32768
    for fid, props in filters:
        if fid == 0x21:
            m += dict_of_prop(props[0]) + 30000
        else:
            m += 1024
    return m

def xz_list(files, verbose, cwd, rc):
    totals = {"files": 0, "streams": 0, "blocks": 0, "c": 0, "u": 0, "pad": 0, "checks": set(), "mem": 0, "sizes": True}
    shown = False
    printed = 0
    for k, f in enumerate(files):
        path = os.path.join(cwd, f)
        if not os.path.isfile(path):
            we(f"xz: {f}: No such file or directory\n"); rc[0] = 1
            continue
        data = open(path, "rb").read()
        if len(data) == 0:
            we(f"xz: {f}: File is empty\n"); rc[0] = 1
            continue
        if len(data) < 24:
            we(f"xz: {f}: Too small to be a valid .xz file\n"); rc[0] = 1
            continue
        try:
            streams = file_info(data)
            blocks = []
            if verbose >= 2:
                for s in streams:
                    off = s["start"] + 12
                    for a, b in s["recs"]:
                        bh = block_header(data, off, len(data))
                        blocks.append((off, a, b, bh))
                        off += (a + 3) // 4 * 4
        except Fail as e:
            we(f"xz: {f}: {MSG[e.args[0]]}\n"); rc[0] = 1
            continue
        nstreams = len(streams)
        nblocks = sum(len(s["recs"]) for s in streams)
        usize = sum(s["usize"] for s in streams)
        checks = set(s["check"] for s in streams)
        pad = sum(s["pad"] for s in streams)
        totals["files"] += 1; totals["streams"] += nstreams; totals["blocks"] += nblocks
        totals["c"] += len(data); totals["u"] += usize; totals["pad"] += pad
        totals["checks"] |= checks
        if verbose == 0:
            if not shown:
                w("Strms  Blocks   Compressed Uncompressed  Ratio  Check   Filename\n")
                shown = True
            w(f"{nstreams:5}  {nblocks:6}  {nice(len(data)):>11}  {nice(usize):>11}  {ratio(len(data), usize):>5}  {check_names(checks, ','):<7} {f}\n")
            continue
        if printed:
            w("\n")
        printed += 1
        w(f"{f} ({k + 1}/{len(files)})\n")
        w(f"  {'Streams:':<18} {nstreams}\n")
        w(f"  {'Blocks:':<18} {nblocks}\n")
        w(f"  {'Compressed size:':<18} {nice(len(data), True)}\n")
        w(f"  {'Uncompressed size:':<18} {nice(usize, True)}\n")
        w(f"  {'Ratio:':<18} {ratio(len(data), usize)}\n")
        w(f"  {'Check:':<18} {check_names(checks, ', ')}\n")
        w(f"  {'Stream Padding:':<18} {nice(pad, True)}\n")
        w("  Streams:\n")
        w("    Stream    Blocks      CompOffset    UncompOffset        CompSize      UncompSize  Ratio  Check      Padding\n")
        for i, s in enumerate(streams):
            w(f"    {i + 1:6} {len(s['recs']):9} {s['start']:15} {s['uoff']:15} {s['size']:15} {s['usize']:15}  {ratio(s['size'], s['usize']):>5}  {CHECK_NAME.get(s['check'], '?'):<10} {s['pad']:7}\n")
        if nblocks:
            cw = max(8, 2 * max(CHECK_SIZE.get(s["check"], 0) for s in streams))
            w("  Blocks:\n")
            head = "    Stream     Block      CompOffset    UncompOffset       TotalSize      UncompSize  Ratio  Check"
            if verbose >= 2:
                head += f"      {'CheckVal':<{cw}} {'Header':>7}  Flags        CompSize    MemUsage  Filters"
            w(head + "\n")
            bi = 0
            for i, s in enumerate(streams):
                off = s["start"] + 12
                uoff = s["uoff"]
                csz = CHECK_SIZE.get(s["check"], 0)
                for j, (a, b) in enumerate(s["recs"]):
                    total = (a + 3) // 4 * 4
                    line = f"    {i + 1:6} {j + 1:9} {off:15} {uoff:15} {total:15} {b:15}  {ratio(total, b):>5}  {CHECK_NAME.get(s['check'], '?')}"
                    if verbose >= 2:
                        bh = blocks[bi][3]
                        cv = data[off + total - csz:off + total]
                        cv = (cv if csz == 32 else cv[::-1]).hex() if csz else "---"
                        flags = ("c" if bh["csize"] is not None else "-") + ("u" if bh["usize"] is not None else "-")
                        mem = (memusage(bh["filters"]) + (1 << 20) - 1) >> 20
                        line = line[:-len(CHECK_NAME.get(s['check'], '?'))] + f"{CHECK_NAME.get(s['check'], '?'):<10} {cv:<{cw}} {bh['size']:7}  {flags:<5} {a - bh['size'] - csz:15} {mem:7} MiB  {filter_str(bh['filters'])}"
                    w(line + "\n")
                    off += total; uoff += b; bi += 1
        if verbose >= 2:
            mem = 0; sizes = True
            for _, _, _, bh in blocks:
                mem = max(mem, (memusage(bh["filters"]) + (1 << 20) - 1) >> 20)
                sizes = sizes and bh["csize"] is not None and bh["usize"] is not None
            totals["mem"] = max(totals["mem"], mem)
            totals["sizes"] = totals["sizes"] and sizes
            w(f"  {'Memory needed:':<18} {mem} MiB\n")
            w(f"  {'Sizes in headers:':<18} {'Yes' if sizes else 'No'}\n")
            w("  Minimum XZ Utils version: 5.0.0\n")
    if totals["files"] > 1:
        t = totals
        if verbose == 0:
            w("-" * 79 + "\n")
            w(f"{t['streams']:5}  {t['blocks']:6}  {nice(t['c']):>11}  {nice(t['u']):>11}  {ratio(t['c'], t['u']):>5}  {check_names(t['checks'], ','):<7} {t['files']} files\n")
        else:
            w("\nTotals:\n")
            w(f"  {'Number of files:':<18} {t['files']}\n")
            w(f"  {'Streams:':<18} {t['streams']}\n")
            w(f"  {'Blocks:':<18} {t['blocks']}\n")
            w(f"  {'Compressed size:':<18} {nice(t['c'], True)}\n")
            w(f"  {'Uncompressed size:':<18} {nice(t['u'], True)}\n")
            w(f"  {'Ratio:':<18} {ratio(t['c'], t['u'])}\n")
            w(f"  {'Check:':<18} {check_names(t['checks'], ', ')}\n")
            w(f"  {'Stream Padding:':<18} {nice(t['pad'], True)}\n")
            if verbose >= 2:
                w(f"  {'Memory needed:':<18} {t['mem']} MiB\n")
                w(f"  {'Sizes in headers:':<18} {'Yes' if t['sizes'] else 'No'}\n")
                w("  Minimum XZ Utils version: 5.0.0\n")

def out_name(f):
    for suf, rep in ((".xz", ""), (".txz", ".tar"), (".lzma", ""), (".tlz", ".tar")):
        if f.endswith(suf) and len(f) > len(suf):
            return f[:-len(suf)] + rep
    return None

def xz(args, cwd, stdout):
    mode = "z"; keep = False; tostd = False; verbose = 0; force = False
    files = []
    for a in args:
        if a.startswith("-") and len(a) > 1:
            for ch in a[1:]:
                if ch == "d": mode = "d"
                elif ch == "t": mode = "t"
                elif ch == "l": mode = "l"
                elif ch == "k": keep = True
                elif ch == "c": tostd = True
                elif ch == "f": force = True
                elif ch == "v": verbose += 1
        else:
            files.append(a)
    rc = [0]
    if mode == "l":
        xz_list(files, verbose, cwd, rc)
        return rc[0]
    for f in files:
        path = os.path.join(cwd, f)
        if not os.path.isfile(path):
            we(f"xz: {f}: No such file or directory\n"); rc[0] = 1
            continue
        outp = None
        if mode == "d" and not tostd:
            on = out_name(f)
            if on is None:
                we(f"xz: {f}: Filename has an unknown suffix, skipping\n"); rc[0] = max(rc[0], 2)
                continue
            outp = os.path.join(cwd, on)
            if os.path.exists(outp) and not force:
                we(f"xz: {on}: File exists\n"); rc[0] = 1
                continue
        data = open(path, "rb").read()
        sink = bytearray()
        try:
            decode_file(data, sink)
        except Fail as e:
            we(f"xz: {f}: {MSG[e.args[0]]}\n"); rc[0] = 1
            continue
        if mode == "d":
            if tostd:
                stdout.extend(sink)
            else:
                open(outp, "wb").write(sink)
                if not keep:
                    os.remove(path)
        if verbose:
            r = len(data) / len(sink) if sink else 16.0
            rs = " > 9.999" if r > 9.999 else f" = {r:.3f}"
            we(f"{f}: {nice(len(data))} / {nice(len(sink))}{rs}\n")
    return rc[0]

def sha256sum(args, cwd):
    rc = 0
    for f in args:
        p = os.path.join(cwd, f)
        if not os.path.isfile(p):
            we(f"sha256sum: {f}: No such file or directory\n")
            rc = 1
            continue
        w(hashlib.sha256(open(p, "rb").read()).hexdigest() + "  " + f + "\n")
    return rc

def main():
    work = os.path.abspath("oraclework")
    if os.path.isdir(work):
        shutil.rmtree(work)
    shutil.copytree("data", work)
    for line in open("data/jobs.txt").read().splitlines():
        if not line or line.startswith("#"):
            continue
        w(f"$ {line}\n")
        parts = line.split(" ")
        stdout = bytearray()
        mark = len(out)
        del err[:]
        if parts[0] == "xz":
            rc = xz(parts[1:], work, stdout)
        else:
            rc = sha256sum(parts[1:], work)
        if stdout:
            out.insert(mark, stdout.decode("utf-8", "replace"))
        out.extend(err)
        if rc:
            w(f"[exit status {rc}]\n")
        w("\n")
    shutil.rmtree(work)
    sys.stdout.write("".join(out))

main()
