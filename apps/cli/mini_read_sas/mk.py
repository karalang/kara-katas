"""Writes data/: the .sas7bdat and .xpt files the jobs read, each shaped
like a file SAS wrote, and data/jobs.txt, one job per line. oracle.py
runs each job on pandas' read_sas, mini_read_sas.kara on its own port.

pandas writes neither format, so both writers are here, byte by byte:

- sas7bdat: 32-bit and 64-bit layouts in either byte order, metadata on
  a meta page or a mix page, rows on data pages, mix pages or (when the
  data set is compressed) in meta-page subheaders, with SAS's two row
  compressions, RLE ("SASYZCRL") and RDC ("SASYZCR2"), each written by
  the compressors below.
- xport: SAS transport version 5, as `libname x xport` and
  `proc copy` write it for FDA submissions, with IBM-370 floats.

Every timestamp is fixed, so the bytes are the same on every run.

Run: python3 -s -P -B mk.py"""
import gzip
import math
import os
import shutil
import struct
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)


def put(name, data):
    with open(os.path.join(DATA, name), "wb") as f:
        f.write(data)


# Seconds from 1960-01-01, SAS's epoch.
def sas_seconds(y, mo, d, h=0, mi=0, s=0.0):
    days = (date_ordinal(y, mo, d) - date_ordinal(1960, 1, 1))
    return days * 86400 + h * 3600 + mi * 60 + s


def sas_days(y, mo, d):
    return date_ordinal(y, mo, d) - date_ordinal(1960, 1, 1)


def date_ordinal(y, mo, d):
    import datetime
    return datetime.date(y, mo, d).toordinal()


# ------------------------------------------------------------ compressors
# RLE, as SAS's COMPRESS=CHAR writes it. The control byte's high nibble
# says what follows; the low nibble (and for the long forms the next
# byte) is a count.


def rle_compress(row):
    out = bytearray()
    lit = bytearray()

    def flush():
        i = 0
        while i < len(lit):
            n = min(len(lit) - i, 64 + 4095) if len(lit) - i > 64 else len(lit) - i
            chunk = lit[i:i + n]
            if n > 64:
                k = n - 64
                out.append(0x00 | (k >> 8))
                out.append(k & 0xFF)
            elif n > 48:
                out.append(0xB0 | (n - 49))
            elif n > 32:
                out.append(0xA0 | (n - 33))
            elif n > 16:
                out.append(0x90 | (n - 17))
            else:
                out.append(0x80 | (n - 1))
            out.extend(chunk)
            i += n
        lit.clear()

    i = 0
    while i < len(row):
        b = row[i]
        j = i
        while j < len(row) and row[j] == b and j - i < 4095 + 18:
            j += 1
        run = j - i
        if b in (0x20, 0x00) and run >= 17:
            flush()
            k = run - 17
            out.append((0x60 if b == 0x20 else 0x70) | (k >> 8))
            out.append(k & 0xFF)
        elif b in (0x20, 0x00, 0x40) and run >= 2:
            run = min(run, 17)
            j = i + run
            flush()
            out.append({0x20: 0xE0, 0x00: 0xF0, 0x40: 0xD0}[b] | (run - 2))
        elif run >= 19:
            flush()
            k = run - 18
            out.append(0x40 | (k >> 8))
            out.append(k & 0xFF)
            out.append(b)
        elif run >= 3:
            flush()
            out.append(0xC0 | (run - 3))
            out.append(b)
        else:
            lit += row[i:j]
        i = j
    flush()
    return bytes(out)


# RDC (Ross Data Compression, COMPRESS=BINARY): a 16-bit control word
# before every 16 items says which are literal bytes and which commands.


def rdc_compress(row):
    out = bytearray()
    items = []
    i = 0
    n = len(row)
    while i < n:
        b = row[i]
        run = 1
        while i + run < n and row[i + run] == b and run < 4095 + 19:
            run += 1
        best_len, best_ofs = 0, 0
        lo = max(0, i - 4098)
        for start in range(lo, i):
            ofs = i - start
            if ofs < 3:
                continue
            k = 0
            while i + k < n and k < 271 and row[start + k] == row[i + k]:
                k += 1
            if k > best_len:
                best_len, best_ofs = k, ofs
        if run >= 19:
            cnt = run - 19
            items.append(bytes([0x10 | (cnt & 0x0F), cnt >> 4, b]))
            i += run
        elif best_len >= 16:
            o = best_ofs - 3
            items.append(bytes([0x20 | (o & 0x0F), o >> 4, best_len - 16]))
            i += best_len
        elif run >= 3:
            items.append(bytes([0x00 | (run - 3), b]))
            i += run
        elif best_len >= 3:
            o = best_ofs - 3
            k = min(best_len, 15)
            items.append(bytes([(k << 4) | (o & 0x0F), o >> 4]))
            i += k
        else:
            items.append(b)
            i += 1
    for g in range(0, len(items), 16):
        group = items[g:g + 16]
        ctrl = 0
        for k, it in enumerate(group):
            if isinstance(it, bytes):
                ctrl |= 0x8000 >> k
        out += bytes([ctrl >> 8, ctrl & 0xFF])
        for it in group:
            if isinstance(it, bytes):
                out += it
            else:
                out.append(it)
    return bytes(out)


# ------------------------------------------------------- sas7bdat writer

MAGIC = (b"\x00" * 12 + b"\xc2\xea\x81\x60\xb3\x14\x11\xcf\xbd\x92\x08\x00"
         b"\x09\xc7\x31\x8c\x18\x1f\x10\x11")


class Col:
    def __init__(self, name, kind, length, fmt="", label="", values=()):
        self.name, self.kind, self.length = name, kind, length
        self.fmt, self.label, self.values = fmt, label, list(values)


# A SAS missing numeric: "." is a NaN whose high bytes are FE FF FF ..
SAS_MISSING = struct.unpack("<d", b"\x00\x00\x00\x00\x00\xfe\xff\xff")[0]


class Sas7:
    """One data set. `layout` is "meta" (metadata alone on the first
    page, rows on data pages), "mix" (metadata and the first rows on a
    mix page) or, for a compressed data set, rows as subheaders on meta
    pages."""

    def __init__(self, cols, u64=True, big=False, page=4096, header=1024,
                 enc=20, compress=None, layout="meta", windows=False,
                 name="DATA", created=0.0, modified=0.0, proc=b"DATASTEP",
                 pad_page=None, raw_rows=(), truncated_ptr=False,
                 counts=None, rows_claim=None, extra_meta=None,
                 mix_rows=None, release=b"9.0401M7", mangle=None):
        self.cols = cols
        self.u64, self.big = u64, big
        self.il = 8 if u64 else 4
        self.bo = ">" if big else "<"
        self.page, self.header = page, header
        self.enc, self.compress, self.layout = enc, compress, layout
        self.windows, self.name = windows, name
        self.created, self.modified, self.proc = created, modified, proc
        self.pad_page = pad_page
        self.raw_rows = set(raw_rows)
        self.truncated_ptr = truncated_ptr
        self.counts = counts
        self.rows_claim = rows_claim
        self.extra_meta = extra_meta
        self.mix_rows = mix_rows
        self.release = release
        self.mangle = mangle or {}
        self.nrows = max((len(c.values) for c in cols), default=0)
        off = 0
        # numerics first, as SAS lays a row out, then the strings
        for c in sorted(cols, key=lambda c: c.kind != "num"):
            c.offset = off
            off += c.length
        self.row_length = off

    # -- primitives
    def u(self, v, n):
        return v.to_bytes(n, "big" if self.big else "little")

    def sig(self, v):
        if self.u64:
            if v >= 0xF0000000 and v not in (0xF7F7F7F7, 0xF6F6F6F6):
                v |= 0xFFFFFFFF00000000
            return self.u(v, 8)
        return self.u(v, 4)

    def num(self, v, n):
        b = struct.pack(self.bo + "d", v)
        return b[:n] if self.big else b[8 - n:]

    def row(self, i):
        out = bytearray(self.row_length)
        for c in self.cols:
            v = c.values[i] if i < len(c.values) else None
            if c.kind == "num":
                b = self.num(SAS_MISSING if v is None else (
                    struct.unpack("<d", v)[0] if isinstance(v, bytes) else v),
                    c.length)
            else:
                t = b"" if v is None else (v if isinstance(v, bytes)
                                           else v.encode(self.codec()))
                b = t[:c.length].ljust(c.length, b" ")
            out[c.offset:c.offset + c.length] = b
        return bytes(out)

    def codec(self):
        return {20: "utf-8", 29: "latin-1", 62: "cp1252", 61: "cp1251"}[self.enc]

    # -- the text blocks: names, formats, labels
    def texts(self):
        il = self.il
        # the first block opens with the compression literal and the
        # creator proc at fixed places
        lit = {None: b"\x00" * 8, "rle": b"SASYZCRL", "rdc": b"SASYZCR2"}
        # the literal sits 16 bytes into the subheader (20 in 64-bit)
        first = bytearray(16 - il + (4 if self.u64 else 0))
        first += lit[self.compress]
        if self.compress == "rle":
            first += b"\x00" * 16 + self.proc
        else:
            first += b"\x00" * 8 + self.proc
        first += b"\x00" * ((-len(first)) % 4)
        blocks = [first]
        refs = {}

        def add(key, text):
            t = text.encode(self.codec()) if isinstance(text, str) else text
            if not t:
                refs[key] = (0, 0, 0)
                return
            b = blocks[-1]
            if len(b) + len(t) > 300:
                blocks.append(bytearray(4))
                b = blocks[-1]
            refs[key] = (len(blocks) - 1, len(b), len(t))
            b += t
            b += b"\x00" * ((-len(b)) % 4)

        for c in self.cols:
            add(("name", c.name), c.name)
        for c in self.cols:
            add(("fmt", c.name), c.fmt)
        for c in self.cols:
            add(("label", c.name), c.label)
        out = []
        for b in blocks:
            b[0:2] = self.u(len(b), 2)
            out.append(self.sig(0xFFFFFFFD) + bytes(b) + b"\x00" * 12)
        return out, refs

    def meta_subheaders(self):
        il = self.il
        n = len(self.cols)
        subs = []
        # row size
        rs = bytearray(808 if self.u64 else 480)
        rs[0:il] = self.sig(0xF7F7F7F7)
        nrows = self.nrows if self.rows_claim is None else self.rows_claim
        p1, p2 = (n, 0) if self.counts is None else self.counts
        for k, v in ((5, self.row_length), (6, nrows), (9, p1), (10, p2),
                     (15, self.mix_capacity())):
            rs[k * il:(k + 1) * il] = self.u(v, il)
        lcs, lcp = (682, 706) if self.u64 else (354, 378)
        rs[lcs:lcs + 2] = self.u(8, 2)
        rs[lcp:lcp + 2] = self.u(len(self.proc), 2)
        subs.append(bytes(rs))
        # column size
        cs = bytearray(3 * il)
        cs[0:il] = self.sig(0xF6F6F6F6)
        cs[il:2 * il] = self.u(n, il)
        subs.append(bytes(cs))
        # subheader counts (pandas skips it)
        sc = bytearray(600 if self.u64 else 304)
        sc[0:il] = self.sig(0xFFFFFC00)
        subs.append(bytes(sc))
        texts, refs = self.texts()
        subs += texts
        # column names
        cn = bytearray(il + 8)
        cn[0:il] = self.sig(0xFFFFFFFF)
        for c in self.cols:
            t, o, ln = refs[("name", c.name)]
            cn += self.u(t, 2) + self.u(o, 2) + self.u(ln, 2) + b"\x00\x00"
        cn += b"\x00" * (il + 4)
        subs.append(bytes(cn))
        # column attributes
        ca = bytearray(il + 8)
        ca[0:il] = self.sig(0xFFFFFFFC)
        for c in self.cols:
            ca += self.u(c.offset, il) + self.u(c.length, 4) + self.u(0, 2)
            ca += bytes([1 if c.kind == "num" else 2, 0])
        ca += b"\x00" * (il + 4)
        subs.append(bytes(ca))
        # formats and labels, one per column
        for c in self.cols:
            f = bytearray(64 if self.u64 else 52)
            f[0:il] = self.sig(0xFFFFFBFE)
            b = 3 * il
            t, o, ln = refs[("fmt", c.name)]
            f[b + 22:b + 28] = self.u(t, 2) + self.u(o, 2) + self.u(ln, 2)
            t, o, ln = refs[("label", c.name)]
            f[b + 28:b + 34] = self.u(t, 2) + self.u(o, 2) + self.u(ln, 2)
            subs.append(bytes(f))
        # column list (pandas skips it)
        cl = bytearray(il + 8 + 2 * n + 8)
        cl[0:il] = self.sig(0xFFFFFFFE)
        subs.append(bytes(cl))
        if self.extra_meta:
            subs.append(self.extra_meta(self))
        return subs

    def mix_capacity(self):
        if self.mix_rows is not None:
            return self.mix_rows
        return self._mix_cap if hasattr(self, "_mix_cap") else 0

    # -- pages
    def page_bytes(self, ptype, subs, rows=(), extra_ptrs=()):
        """subs: list of (bytes, compression, type) placed from the end of
        the page backwards; rows: raw row bytes after the pointers."""
        bo_ = 32 if self.u64 else 16
        pl = 24 if self.u64 else 12
        page = bytearray(self.page)
        nsub = len(subs) + len(extra_ptrs)
        start = bo_ + 8 + nsub * pl
        if ptype == 0x0200:
            start += start % 8
        for k, r in enumerate(rows):
            page[start + k * len(r):start + (k + 1) * len(r)] = r
        end = self.page
        ptrs = []
        for data, comp, typ in subs:
            end -= len(data)
            end -= end % 8
            page[end:end + len(data)] = data
            ptrs.append((end, len(data), comp, typ))
        ptrs += list(extra_ptrs)
        low = start + len(rows) * self.row_length
        if end < low:
            raise ValueError("page overflow")
        for k, (o, ln, comp, typ) in enumerate(ptrs):
            p = bo_ + 8 + k * pl
            il = self.il
            page[p:p + il] = self.u(o, il)
            page[p + il:p + 2 * il] = self.u(ln, il)
            page[p + 2 * il] = comp
            page[p + 2 * il + 1] = typ
        page[bo_:bo_ + 2] = self.u(ptype, 2)
        blocks = len(rows) + nsub if ptype != 0x0100 else len(rows)
        page[bo_ + 2:bo_ + 4] = self.u(blocks, 2)
        page[bo_ + 4:bo_ + 6] = self.u(nsub, 2)
        return bytes(page)

    def free(self, nsub, subs_len, ptype):
        bo_ = 32 if self.u64 else 16
        pl = 24 if self.u64 else 12
        start = bo_ + 8 + nsub * pl
        if ptype == 0x0200:
            start += start % 8
        return self.page - subs_len - 8 * nsub - start

    def pages(self):
        meta = [(s, 0, 0) for s in self.meta_subheaders()]
        rows = [self.row(i) for i in range(self.nrows)]
        out = []
        bo_ = 32 if self.u64 else 16
        if self.compress:
            data = []
            for i, r in enumerate(rows):
                if i in self.raw_rows:
                    data.append((r, 0, 1))
                else:
                    c = rle_compress(r) if self.compress == "rle" else rdc_compress(r)
                    if i in self.mangle:
                        c = self.mangle[i](c)
                    if len(c) >= len(r):
                        data.append((r, 0, 1))
                    else:
                        data.append((c, 4, 1))
            # fill page 0 after the metadata, then more meta pages
            cur = list(meta)
            extra = []
            if self.truncated_ptr:
                extra = [(0, 0, 1, 0)]
            for d in data:
                trial = cur + [d]
                used = sum(len(s) + 8 for s, _, _ in trial)
                if self.free(len(trial) + len(extra), used, 0) < 0:
                    out.append(self.page_bytes(0x0000, cur, extra_ptrs=extra))
                    cur = [d]
                    extra = []
                else:
                    cur = trial
            out.append(self.page_bytes(0x0000, cur, extra_ptrs=extra))
        else:
            per_data = (self.page - bo_ - 8) // max(1, self.row_length)
            i = 0
            if self.layout == "mix":
                used = sum(len(s) + 8 for s, _, _ in meta)
                cap = max(0, self.free(len(meta), used, 0x0200) // self.row_length)
                if self.mix_rows is None:
                    self._mix_cap = cap
                    meta = [(s, 0, 0) for s in self.meta_subheaders()]
                k = min(cap, self.nrows)
                out.append(self.page_bytes(0x0200, meta, rows[:k]))
                i = k
            else:
                out.append(self.page_bytes(0x0000, meta))
            while i < self.nrows:
                k = min(per_data, self.nrows - i)
                out.append(self.page_bytes(0x0100, [], rows[i:i + k]))
                i += k
        if self.pad_page is not None:
            at, ptype = self.pad_page
            out.insert(at, self.page_bytes(ptype, []))
        return out

    def header_bytes(self, npages):
        h = bytearray(self.header)
        h[0:32] = MAGIC
        a = 4 if self.u64 else 0
        h[32] = 0x33 if self.u64 else 0x22
        h[35] = 0x33 if self.u64 else 0x22
        h[37] = 0x00 if self.big else 0x01
        h[39] = ord("2") if self.windows else ord("1")
        h[70] = self.enc
        h[84:92] = b"SAS FILE"
        h[92:156] = self.name.encode("latin-1").ljust(64)
        h[156:164] = b"DATA    "
        h[164 + a:172 + a] = struct.pack(self.bo + "d", self.created)
        h[172 + a:180 + a] = struct.pack(self.bo + "d", self.modified)
        h[196 + a:200 + a] = self.u(self.header, 4)
        h[200 + a:204 + a] = self.u(self.page, 4)
        h[204 + a:204 + a + (8 if self.u64 else 4)] = self.u(npages, 8 if self.u64 else 4)
        b = 216 + a + (4 if self.u64 else 0)
        h[b:b + 8] = self.release.ljust(8)
        h[b + 8:b + 24] = (b"X64_SR12R2" if self.windows else b"Linux").ljust(16)
        return bytes(h)

    def bytes(self):
        pages = self.pages()
        return self.header_bytes(len(pages)) + b"".join(pages)


# ---------------------------------------------------------- xport writer


def ibm(x):
    """An IEEE double as an IBM-370 double: sign, a base-16 exponent in
    excess 64, 56 bits of fraction. Every double fits exactly."""
    if isinstance(x, bytes):
        return x.ljust(8, b"\x00")
    if x == 0:
        return bytes(8)
    sign = 0x80 if x < 0 else 0
    m, e = math.frexp(abs(x))
    E = -((-e) // 4)
    mant = int(math.ldexp(m, e - 4 * E + 56))
    return bytes([sign | (E + 64)]) + mant.to_bytes(7, "big")


def xmiss(code="."):
    return code.encode() + bytes(7)


def card(s):
    b = s.encode("latin-1") if isinstance(s, str) else s
    assert len(b) <= 80, (len(b), b)
    return b.ljust(80)


LIB = "HEADER RECORD*******LIBRARY HEADER RECORD!!!!!!!000000000000000000000000000000  "


class XCol:
    def __init__(self, name, kind, length, label="", fmt="", flen=0, fdec=0,
                 values=()):
        self.name, self.kind, self.length = name, kind, length
        self.label, self.fmt, self.flen, self.fdec = label, fmt, flen, fdec
        self.values = list(values)


def xport_member(cols, name, label="", created="16FEB11:10:07:55",
                 modified="16FEB11:10:07:55", namelen=140, os_="X64_7PRO",
                 obs_header=True, nrows=None):
    out = bytearray()
    out += card("HEADER RECORD*******MEMBER  HEADER RECORD!!!!!!!"
                f"000000000000000001600000000{namelen:03d}  ")
    out += card("HEADER RECORD*******DSCRPTR HEADER RECORD!!!!!!!"
                "000000000000000000000000000000  ")
    out += card("SAS     " + name.ljust(8) + "SASDATA " + "9.4".ljust(8)
                + os_.ljust(8) + " " * 24 + created)
    out += card(modified + " " * 16 + label.ljust(40) + "DATA".ljust(8))
    out += card("HEADER RECORD*******NAMESTR HEADER RECORD!!!!!!!"
                f"000000{len(cols):04d}00000000000000000000  ")
    ns = bytearray()
    pos = 0
    for k, c in enumerate(cols):
        rec = struct.pack(
            ">hhhh8s40s8shhh2s8shhl",
            1 if c.kind == "num" else 2, 0, c.length, k + 1,
            c.name.encode("latin-1").ljust(8), c.label.encode("latin-1").ljust(40),
            c.fmt.encode("latin-1").ljust(8), c.flen, c.fdec, 0, b"\x00\x00",
            b"".ljust(8), 0, 0, pos)
        rec = rec.ljust(140, b"\x00")[:namelen]
        ns += rec
        pos += c.length
    ns += b" " * ((-len(ns)) % 80)
    out += ns
    if obs_header:
        out += card("HEADER RECORD*******OBS     HEADER RECORD!!!!!!!"
                    "000000000000000000000000000000  ")
    n = max(len(c.values) for c in cols) if nrows is None else nrows
    data = bytearray()
    for i in range(n):
        for c in cols:
            v = c.values[i]
            if c.kind == "num":
                b = (xmiss() if v is None else ibm(v))[:c.length]
            else:
                b = (v.encode("latin-1") if isinstance(v, str) else v)
                b = b.ljust(c.length)[:c.length]
            data += b
    data += b" " * ((-len(data)) % 80)
    out += data
    return bytes(out)


def xport(members, created="16FEB11:10:07:55", modified="16FEB11:10:07:55",
          line1=LIB, prefix="SAS     SAS     SASLIB  ", os_="X64_7PRO"):
    out = bytearray()
    out += card(line1)
    out += card(prefix + "9.4".ljust(8) + os_.ljust(8) + " " * 24 + created)
    out += card(modified + " " * 64)
    for m in members:
        out += m
    return bytes(out)


# ------------------------------------------------------------- the files
import random

rnd = random.Random(20241029)
FIRST = ["Nguyễn Thị Lan", "José Álvarez", "Zoë Müller", "Aoife Ní Bhriain",
         "Søren Kierkegård", "Mei-Ling Chen", "Oluwaseun Adeyemi", "Ana-María Oyarzún",
         "Łukasz Wiśniewski", "Priya Raman", "Jean-Luc Bérubé", "Fatma Yılmaz"]
DX = ["E11.9", "I10", "J45.909", "M54.5", "Z00.00", "K21.9", "F41.1", "N39.0"]

# 1. Health-insurance claims, 64-bit little-endian UTF-8, as SAS 9.4 on
#    Linux writes an uncompressed data set: metadata on page 0, rows on
#    data pages.
n = 70
claims = [
    Col("CLAIM_ID", "char", 10, label="Claim identifier",
        values=[f"CLM{4100 + 37 * i:07d}" for i in range(n)]),
    Col("MEMBER_NM", "char", 32, label="Member name",
        values=[("" if i % 17 == 5 else FIRST[(i * 5) % len(FIRST)]) for i in range(n)]),
    Col("SVC_DT", "num", 8, fmt="YYMMDD", label="Date of service",
        values=[float(sas_days(2023, 1, 1) + (i * 11) % 365) if i % 23 != 7 else None
                for i in range(n)]),
    Col("RECV_TS", "num", 8, fmt="DATETIME", label="Received at",
        values=[sas_seconds(2023, 1, 3) + i * 86400 * 5 + (i * 7919) % 86400
                + (0.25 if i % 9 == 4 else 0.0) for i in range(n)]),
    Col("PAID_AMT", "num", 8, fmt="DOLLAR", label="Paid amount ($)",
        values=[round(rnd.uniform(15, 4800), 2) if i % 13 != 3 else None for i in range(n)]),
    Col("UNITS", "num", 3, label="Service units",
        values=[float(1 + (i * 7) % 12) for i in range(n)]),
    Col("DX_CODE", "char", 8, label="Primary diagnosis",
        values=[DX[(i * 3) % len(DX)] for i in range(n)]),
    Col("STATUS", "char", 1, label="P=paid D=denied",
        values=[("P" if i % 5 else ("D" if i % 10 else " ")) for i in range(n)]),
    Col("LOS_TIME", "num", 8, fmt="TIME", label="Visit length",
        values=[float(900 * (1 + i % 8)) for i in range(n)]),
]
put("claims_2023.sas7bdat", Sas7(
    claims, header=8192, page=4096, name="CLAIMS_2023",
    created=sas_seconds(2024, 1, 15, 7, 45, 12.5),
    modified=sas_seconds(2024, 1, 15, 7, 45, 13.0)).bytes())

# 2. Branch sales, 32-bit little-endian WLATIN1 (cp1252), from SAS on
#    Windows: metadata and the first rows share a mix page.
REG = ["Île-de-France", "Bretagne", "Rhône-Alpes", "Andalucía", "Bayern", "Zürich"]
BR = ["Café Señor", "Gare du Nord", "Ñuñoa Centro", "Marché Saint-Cœur",
      "Straße 12", "Plaza Mayor", "Œuvre Rive", "Porto Antigo"]
n = 46
sales = [
    Col("REGION", "char", 16, label="Sales region",
        values=[REG[i % len(REG)] for i in range(n)]),
    Col("BRANCH", "char", 24, label="Branch",
        values=[BR[(i * 3) % len(BR)] for i in range(n)]),
    Col("WEEK", "num", 8, fmt="WEEKDATE", label="Week starting",
        values=[float(sas_days(2024, 1, 1) + 7 * (i // 6)) for i in range(n)]),
    Col("SALES", "num", 8, fmt="COMMA", label="Net sales (€)",
        values=[round(1000 + rnd.random() * 25000, 2) for i in range(n)]),
    Col("RETURNS", "num", 6, label="Returns (€)",
        values=[(round(rnd.random() * 900, 1) if i % 7 != 2 else None) for i in range(n)]),
    Col("CUR", "char", 3, values=["€" if i % 4 else "EUR" for i in range(n)]),
]
put("branch_sales.sas7bdat", Sas7(
    sales, u64=False, enc=62, layout="mix", windows=True, page=4096,
    name="BRANCH_SALES", created=sas_seconds(2024, 3, 2, 18, 0, 1.0),
    modified=sas_seconds(2024, 3, 2, 18, 0, 1.0),
    release=b"9.0401M6").bytes())

# 3. Smart-meter readings, 64-bit big-endian latin-1 (SAS on AIX),
#    COMPRESS=CHAR: every row is an RLE subheader on a meta page. Two rows
#    are stored as they are (they did not get smaller), and one pointer is
#    a truncated subheader SAS left behind.
SITES = ["Substation 4 / Feeder B", "Rue de l'Église 7", "Industriepark Süd",
         "Harbour Rd pumping station", ""]
n = 160
meters = [
    Col("METER_ID", "char", 16, values=[f"MTR-{(i % 40):04d}" for i in range(n)]),
    Col("SITE", "char", 40, values=[SITES[i % len(SITES)] for i in range(n)]),
    Col("READ_TS", "num", 8, fmt="DATETIME",
        values=[sas_seconds(2024, 6, 1) + 900 * i for i in range(n)]),
    Col("KWH", "num", 8, values=[round(0.5 + (i * 37 % 100) / 7.0, 3) for i in range(n)]),
    Col("TEMP_C", "num", 4, values=[float(18 + i % 9) if i % 31 != 0 else None
                                    for i in range(n)]),
    Col("FLAGS", "char", 24, values=[("ESTIMATED" if i % 19 == 0 else "") for i in range(n)]),
    Col("NOTE", "char", 96, values=[("Seal replaced; reading confirmed on site." if i % 41 == 0
                                     else "") for i in range(n)]),
]
put("meter_readings.sas7bdat", Sas7(
    meters, big=True, enc=29, compress="rle", page=8192, name="METER_READINGS",
    raw_rows=(3, 90), truncated_ptr=True,
    created=sas_seconds(2024, 7, 1, 2, 0, 0.0),
    modified=sas_seconds(2024, 7, 1, 2, 5, 0.0), proc=b"SORT").bytes())

# 4. A survey wave, 64-bit little-endian UTF-8, COMPRESS=BINARY (RDC),
#    numeric-heavy; one page of a type pandas skips sits between them.
n = 150
qs = []
for q in range(1, 9):
    qs.append(Col(f"Q{q}", "num", 8, label=f"Question {q} (1-5)",
                  values=[(float(1 + (i * q + i // 3) % 5) if (i + q) % 29 else None)
                          for i in range(n)]))
survey = [
    Col("RESP_ID", "char", 8, values=[f"R{i + 1:05d}" for i in range(n)]),
    Col("INT_DT", "num", 8, fmt="DATE", label="Interview date",
        values=[float(sas_days(2024, 4, 1) + i // 10) for i in range(n)]),
] + qs + [
    Col("REGION", "char", 12, values=[["North", "South", "East", "West", "Centre"][i % 5]
                                      for i in range(n)]),
    Col("COMMENT", "char", 64, values=[("" if i % 6 else ["Fine.", "Too long; skipped Q4.",
                                                          "«Très bien»", "No comment"][i % 4])
                                       for i in range(n)]),
]
put("survey_wave2.sas7bdat", Sas7(
    survey, compress="rdc", page=4096, name="SURVEY_WAVE2", pad_page=(2, 0x9000),
    created=sas_seconds(2024, 5, 20, 12, 0, 0.0),
    modified=sas_seconds(2024, 5, 21, 9, 30, 0.0)).bytes())

# 5. Warehouse inventory, 32-bit big-endian (SAS 8 on Solaris): a mix
#    page holding the first rows behind an odd number of subheaders.
ITEMS = ["Hex bolt M8x40", "Washer, zinc 8mm", "Cable tie 200mm", "Drill bit 6.5mm",
         "Gloves (L)", "Tape, 50m", "Fuse 10A"]
n = 30
inv = [
    Col("SKU", "char", 8, values=[f"SK{1000 + 13 * i}" for i in range(n)]),
    Col("DESCR", "char", 24, label="Description", values=[ITEMS[i % len(ITEMS)] for i in range(n)]),
    Col("QTY", "num", 4, values=[float((i * 53) % 400) for i in range(n)]),
    Col("PRICE", "num", 8, fmt="DOLLAR", values=[round(0.05 + (i * 13 % 50) * 0.37, 2)
                                                 for i in range(n)]),
    Col("LAST_CNT", "num", 8, fmt="MMDDYY", label="Last counted",
        values=[float(sas_days(2003, 11, 1) + i * 3) for i in range(n)]),
    Col("BIN", "char", 6, values=[f"A{i % 7}-{i % 3}" for i in range(n)]),
]
put("inventory_sol.sas7bdat", Sas7(
    inv, u64=False, big=True, enc=29, layout="mix", page=2048, mix_rows=None,
    name="INVENTORY", created=sas_seconds(2003, 12, 5, 16, 20, 0.0),
    modified=sas_seconds(2003, 12, 5, 16, 20, 0.0), release=b"8.0202M0").bytes())

# 6. An extract with no rows.
put("empty_extract.sas7bdat", Sas7(
    [Col("ACCT", "char", 12, values=[]), Col("OPENED", "num", 8, fmt="DATE", values=[]),
     Col("LIMIT", "num", 8, values=[]), Col("SEGMENT", "char", 4, values=[])],
    name="EMPTY", created=sas_seconds(2024, 8, 1)).bytes())

# 7. The error cases people meet with sas7bdat files.
put("notes.sas7bdat", b"claim_id,amount\nCLM0004100,1672.73\n")
claims_bytes = Sas7(claims, header=8192, page=4096, name="CLAIMS_2023",
                    created=sas_seconds(2024, 1, 15, 7, 45, 12.5),
                    modified=sas_seconds(2024, 1, 15, 7, 45, 13.0)).bytes()
put("claims_cut.sas7bdat", claims_bytes[:600])               # in the header
put("claims_copying.sas7bdat", claims_bytes[:8192 + 4096 * 2])  # last page not yet written
put("claims_partial.sas7bdat", claims_bytes[:8192 + 4096 * 2 + 1500])  # mid-page
put("readings.dat", open(os.path.join(DATA, "meter_readings.sas7bdat"), "rb").read())
small = [Col("ACCT", "char", 8, values=["A-1", "A-2", "A-3", "A-4"]),
         Col("BAL", "num", 8, values=[10.0, -2.5, 0.0, 7.25]),
         Col("MEMO", "char", 60, values=["", "overdraft fee waived", "", ""])]
put("ledger_mismatch.sas7bdat", Sas7(small, counts=(3, 1), name="LEDGER").bytes())
put("ledger_newsub.sas7bdat", Sas7(
    small, name="LEDGER", extra_meta=lambda s: s.sig(0x11223344) + bytes(24)).bytes())
put("ledger_badrle.sas7bdat", Sas7(
    small, compress="rle", name="LEDGER",
    mangle={2: lambda c: bytes([0x20 | (c[0] & 0x0F)]) + c[1:]}).bytes())
put("ledger_shortrle.sas7bdat", Sas7(
    small, compress="rle", name="LEDGER", mangle={1: lambda c: c[:-2]}).bytes())
put("ledger_longrle.sas7bdat", Sas7(
    small, compress="rle", name="LEDGER", mangle={1: lambda c: c + b"\xe5"}).bytes())
put("ledger_badrdc.sas7bdat", Sas7(
    small, compress="rdc", name="LEDGER",
    mangle={3: lambda c: b"\x80\x00" + bytes([0x30, 0x05]) + c[2:]}).bytes())
put("novars.sas7bdat", Sas7([], name="NOVARS").bytes())

# ---------------------------------------------------------- xport files

# 8. SDTM lab results (LB), as a submission ships them: transport v5,
#    rows wider than a card, 0.0 results, and the missing values ".",
#    ".A" (not done) and "._".
TESTS = [("ALB", "Albumin", "g/L", 35, 50), ("BASO", "Basophils", "10^9/L", 0, 0.2),
         ("CREAT", "Creatinine", "umol/L", 62, 106), ("GLUC", "Glucose", "mmol/L", 3.9, 5.6),
         ("HGB", "Hemoglobin", "g/L", 130, 175), ("K", "Potassium", "mmol/L", 3.5, 5.1)]
n = 48
lb_vals = {k: [] for k in ["STUDYID", "DOMAIN", "USUBJID", "LBSEQ", "LBTESTCD", "LBTEST",
                           "LBORRES", "LBORRESU", "LBSTRESN", "LBSTNRLO", "LBSTNRHI",
                           "LBNRIND", "VISITNUM", "LBDTC", "LBDY"]}
for i in range(n):
    code, name, unit, lo, hi = TESTS[i % len(TESTS)]
    subj = i // 12
    if code == "BASO":
        val = [0.0, 0.1, 0.0, 0.02][subj % 4]
    else:
        val = round(lo + (hi - lo) * (((i * 37) % 23) / 17.0), 1)
    missing = (i == 17) or (i == 40)
    lb_vals["STUDYID"].append("ACME-301")
    lb_vals["DOMAIN"].append("LB")
    lb_vals["USUBJID"].append(f"ACME-301-{101 + subj:04d}")
    lb_vals["LBSEQ"].append(float(1 + i % 12))
    lb_vals["LBTESTCD"].append(code)
    lb_vals["LBTEST"].append(name)
    lb_vals["LBORRES"].append("" if missing else (f"{val:g}"))
    lb_vals["LBORRESU"].append(unit)
    lb_vals["LBSTRESN"].append(b"A" if i == 17 else (None if i == 40 else val))
    lb_vals["LBSTNRLO"].append(float(lo))
    lb_vals["LBSTNRHI"].append(float(hi))
    lb_vals["LBNRIND"].append("" if missing else ("HIGH" if val > hi else ("LOW" if val < lo else "NORMAL")))
    lb_vals["VISITNUM"].append(float(1 + (i % 12) // 6) if i != 33 else b"_")
    day = 1 + 14 * ((i % 12) // 6) - (1 if i % 12 == 0 else 0)
    lb_vals["LBDTC"].append(f"2024-0{3 + subj}-{10 + (day % 15):02d}T08:{(i * 7) % 60:02d}")
    lb_vals["LBDY"].append(float(day - 1))
lb_cols = [
    XCol("STUDYID", "char", 8, "Study Identifier"), XCol("DOMAIN", "char", 2, "Domain Abbreviation"),
    XCol("USUBJID", "char", 16, "Unique Subject Identifier"),
    XCol("LBSEQ", "num", 8, "Sequence Number", "BEST", 8),
    XCol("LBTESTCD", "char", 8, "Lab Test or Examination Short Name"),
    XCol("LBTEST", "char", 40, "Lab Test or Examination Name"),
    XCol("LBORRES", "char", 12, "Result or Finding in Original Units"),
    XCol("LBORRESU", "char", 8, "Original Units"),
    XCol("LBSTRESN", "num", 8, "Numeric Result/Finding in Standard Units", "BEST", 12),
    XCol("LBSTNRLO", "num", 8, "Normal Range Lower Limit-Std Units"),
    XCol("LBSTNRHI", "num", 8, "Normal Range Upper Limit-Std Units"),
    XCol("LBNRIND", "char", 8, "Reference Range Indicator"),
    XCol("VISITNUM", "num", 8, "Visit Number", "BEST", 4),
    XCol("LBDTC", "char", 16, "Date/Time of Specimen Collection"),
    XCol("LBDY", "num", 8, "Study Day of Specimen Collection", "BEST", 4),
]
for c in lb_cols:
    c.values = lb_vals[c.name]
lb = xport([xport_member(lb_cols, "LB", "Laboratory Test Results",
                         created="05MAR24:14:22:09", modified="05MAR24:14:22:09")],
           created="05MAR24:14:22:09", modified="05MAR24:14:22:09")
put("lb_2024.xpt", lb)
put("lb_2024.xpt.gz", gzip.compress(lb, mtime=0))
with zipfile.ZipFile(os.path.join(DATA, "lb_2024.xpt.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    zi = zipfile.ZipInfo("lb_2024.xpt", date_time=(2024, 3, 5, 14, 22, 8))
    zi.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(zi, lb)

# 9. Demographics with records shorter than a card. pandas counts the
#    rows by subtracting every all-blank 8-byte word in the last card,
#    so a blank ARMCD there costs it the last subject.
dm = [XCol("SUBJID", "char", 8, "Subject Identifier for the Study",
           values=[f"{1001 + i}" for i in range(13)]),
      XCol("ARMCD", "char", 8, "Planned Arm Code",
           values=["PBO", "DRUG10", "DRUG20", "PBO", "", "DRUG10", "DRUG20", "PBO", "DRUG10",
                   "DRUG20", "PBO", "DRUG10", ""]),
      XCol("AGE", "num", 8, "Age", values=[float(a) for a in
                                           [34, 51, 47, 62, 29, 58, 44, 39, 70, 55, 41, 66, 23]])]
put("dm_screen.xpt", xport([xport_member(dm, "DM", "Demographics",
                                          created="12JAN24:09:00:00", modified="12JAN24:09:00:00")],
                           created="12JAN24:09:00:00", modified="12JAN24:09:00:00"))
dm2 = [XCol(c.name, c.kind, c.length, c.label, values=c.values[:12]) for c in dm]
put("dm_enrolled.xpt", xport([xport_member(dm2, "DM", "Demographics",
                                            created="12JAN24:09:00:00", modified="12JAN24:09:00:00")],
                             created="12JAN24:09:00:00", modified="12JAN24:09:00:00"))

# 10. From SAS 6 on VMS: 135-byte NAMESTR records, 2-, 4- and 6-byte
#     numerics, a header date pandas cannot parse.
vms = [XCol("PLANT", "char", 6, values=["OSLO", "BERGEN", "OSLO", "TROMSO", "BERGEN"]),
       XCol("UNITS", "num", 4, values=[120.0, 75.5, 0.0, 1 / 3, 99999.0]),
       XCol("SHIFT", "num", 2, values=[1.0, 2.0, 3.0, 1.0, 2.0]),
       XCol("RATE", "num", 6, values=[0.1, 2.718281828, -45.125, None, 1e-5])]
put("plant_vms.xpt", xport([xport_member(vms, "PLANT", "Plant output 1994",
                                          namelen=135, os_="VAX/VMS", created="03OCT94:23:59:01",
                                          modified=" " * 16)],
                           os_="VAX/VMS", created="03OCT94:23:59:01", modified=""))

# 11. Two members in one transport file. pandas reads only the first,
#     and counts the second member's headers as rows of it.
ae = [XCol("USUBJID", "char", 16, values=["ACME-301-0101", "ACME-301-0103"]),
      XCol("AETERM", "char", 24, values=["HEADACHE", "NAUSEA"]),
      XCol("AESEV", "char", 8, values=["MILD", "MODERATE"]),
      XCol("AESTDY", "num", 8, values=[3.0, 15.0])]
ds = [XCol("USUBJID", "char", 16, values=["ACME-301-0101", "ACME-301-0102", "ACME-301-0103"]),
      XCol("DSDECOD", "char", 24, values=["COMPLETED", "ADVERSE EVENT", "COMPLETED"]),
      XCol("DSSTDY", "num", 8, values=[85.0, 22.0, 85.0])]
put("ae_ds.xpt", xport([xport_member(ae, "AE", "Adverse Events"),
                        xport_member(ds, "DS", "Disposition")]))

# 12. The error cases.
put("lb_cport.xpt", b"**COMPRESSED** **COMPRESSED** **COMPRESSED** **COMPRESSED** **COMPRESSED********"
    + b"\x00" * 400)
put("lb_v8.xpt", xport([], line1="HEADER RECORD*******LIBV8   HEADER RECORD!!!!!!!"
                                 "000000000000000000000000000000  "))
put("lb_prefix.xpt", xport([xport_member(vms, "PLANT")], prefix="SPSS    SPSS    SPSSLIB "))
wide = [XCol("ID", "char", 8, values=["a"]), XCol("BIG", "num", 9, values=[1.0])]
put("lb_wide.xpt", xport([xport_member(wide, "WIDE")]))
put("lb_noobs.xpt", xport([xport_member(dm[:2], "DM", obs_header=False)]))

# ------------------------------------------------------------- the jobs
JOBS = """
meta claims_2023.sas7bdat
read claims_2023.sas7bdat
read claims_2023.sas7bdat encoding=infer
read claims_2023.sas7bdat encoding=infer index=CLAIM_ID
chunks claims_2023.sas7bdat 32 encoding=utf-8
rows claims_2023.sas7bdat 5,0,3,100,4 encoding=infer
reader claims_2023.sas7bdat convert_dates=False blank_missing=False encoding=infer
reader claims_2023.sas7bdat convert_header_text=False convert_text=False encoding=infer
meta branch_sales.sas7bdat
read branch_sales.sas7bdat encoding=infer
read branch_sales.sas7bdat encoding=latin-1
read branch_sales.sas7bdat index=WEEK
chunks branch_sales.sas7bdat 20 encoding=cp1252
meta meter_readings.sas7bdat
read meter_readings.sas7bdat encoding=infer
chunks meter_readings.sas7bdat 64 encoding=latin-1
read readings.dat encoding=infer
read readings.dat format=sas7bdat encoding=infer
meta survey_wave2.sas7bdat
read survey_wave2.sas7bdat encoding=utf-8 index=RESP_ID
read survey_wave2.sas7bdat encoding=latin-1
chunks survey_wave2.sas7bdat 70 encoding=infer
meta inventory_sol.sas7bdat
read inventory_sol.sas7bdat encoding=infer
chunks inventory_sol.sas7bdat 7 encoding=infer
meta empty_extract.sas7bdat
read empty_extract.sas7bdat encoding=infer
read empty_extract.sas7bdat
chunks empty_extract.sas7bdat 5
read notes.sas7bdat
read claims_cut.sas7bdat
read claims_copying.sas7bdat encoding=infer
read claims_partial.sas7bdat encoding=infer
chunks claims_partial.sas7bdat 30 encoding=infer
read ledger_mismatch.sas7bdat encoding=infer
read ledger_newsub.sas7bdat
read ledger_badrle.sas7bdat
read ledger_shortrle.sas7bdat
read ledger_longrle.sas7bdat
read ledger_badrdc.sas7bdat
read novars.sas7bdat
read survey_wave2.sas7bdat format=xport
meta lb_2024.xpt
read lb_2024.xpt
read lb_2024.xpt encoding=latin-1 index=USUBJID
chunks lb_2024.xpt 20 encoding=utf-8
rows lb_2024.xpt 10,30,8,5 encoding=latin-1
read lb_2024.xpt.gz encoding=latin-1
read lb_2024.xpt.zip encoding=latin-1
read lb_2024.xpt format=sas7bdat
read lb_2024.xpt format=spss
meta dm_screen.xpt
read dm_screen.xpt encoding=latin-1
chunks dm_screen.xpt 5 encoding=latin-1
read dm_enrolled.xpt encoding=latin-1
meta plant_vms.xpt
read plant_vms.xpt encoding=latin-1
meta ae_ds.xpt
read ae_ds.xpt encoding=latin-1
read lb_cport.xpt
read lb_v8.xpt
read lb_prefix.xpt
read lb_wide.xpt
read lb_noobs.xpt
read missing.xpt
"""
put("jobs.txt", JOBS.lstrip("\n").encode())
