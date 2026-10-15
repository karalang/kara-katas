# mini_unzip in Python: Info-ZIP unzip 6.0 and zipinfo, written from
# PKWARE's APPNOTE, RFC 1951 and Info-ZIP's output formats. It runs the
# commands in data/jobs.txt; each job's stdout comes first, then its
# stderr, as real.py captures them.
import os, sys

CRC_TABLE = []
for n in range(256):
    c = n
    for _ in range(8):
        c = (0xEDB88320 ^ (c >> 1)) if c & 1 else c >> 1
    CRC_TABLE.append(c)


def crc_byte(crc, b):
    return CRC_TABLE[(crc ^ b) & 0xFF] ^ (crc >> 8)


def crc32(data):
    c = 0xFFFFFFFF
    for b in data:
        c = crc_byte(c, b)
    return c ^ 0xFFFFFFFF


def u16(b, i):
    return b[i] | b[i + 1] << 8


def u32(b, i):
    return u16(b, i) | u16(b, i + 2) << 16


def u64(b, i):
    return u32(b, i) | u32(b, i + 4) << 32


def ljust(s, n):
    # Info-ZIP pads with printf's %-22s, which counts bytes
    k = len(s.encode())
    return s + " " * (n - k) if k < n else s


# ------------------------------------------------------------ inflate (RFC 1951)

class Bits:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.bit = 0
        self.nbits = 0
        self.bad = False

    def need(self, n):
        while self.nbits < n:
            if self.pos >= len(self.data):
                self.bad = True
                return False
            self.bit |= self.data[self.pos] << self.nbits
            self.pos += 1
            self.nbits += 8
        return True

    def get(self, n):
        if n == 0:
            return 0
        if not self.need(n):
            return 0
        v = self.bit & ((1 << n) - 1)
        self.bit >>= n
        self.nbits -= n
        return v


# A canonical Huffman code as counts per length and symbols in order.
class Huff:
    def __init__(self, lengths):
        self.count = [0] * 16
        for l in lengths:
            self.count[l] += 1
        self.count[0] = 0
        offs = [0] * 16
        for i in range(1, 16):
            offs[i] = offs[i - 1] + self.count[i - 1]
        self.symbol = [0] * len(lengths)
        for s, l in enumerate(lengths):
            if l != 0:
                self.symbol[offs[l]] = s
                offs[l] += 1


def decode(br, h):
    code = 0
    first = 0
    index = 0
    for l in range(1, 16):
        code |= br.get(1)
        if br.bad:
            return -1
        count = h.count[l]
        if code - count < first:
            return h.symbol[index + (code - first)]
        index += count
        first += count
        first <<= 1
        code <<= 1
    return -1


LEN_BASE = [3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27, 31, 35, 43, 51, 59,
            67, 83, 99, 115, 131, 163, 195, 227, 258]
LEN_EXTRA = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 0]
DIST_BASE = [1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257, 385, 513, 769,
             1025, 1537, 2049, 3073, 4097, 6145, 8193, 12289, 16385, 24577]
DIST_EXTRA = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11,
              12, 12, 13, 13]
CL_ORDER = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]


def codes(br, out, lit, dist):
    while True:
        sym = decode(br, lit)
        if sym < 0:
            return False
        if sym < 256:
            out.append(sym)
        elif sym == 256:
            return True
        else:
            sym -= 257
            if sym >= 29:
                return False
            n = LEN_BASE[sym] + br.get(LEN_EXTRA[sym])
            d = decode(br, dist)
            if d < 0 or d >= 30:
                return False
            back = DIST_BASE[d] + br.get(DIST_EXTRA[d])
            if br.bad or back > len(out):
                return False
            for _ in range(n):
                out.append(out[len(out) - back])


# The bytes `data` inflates to, and whether it was a whole stream.
def inflate(data):
    br = Bits(data)
    out = []
    fixed_lit = Huff([8] * 144 + [9] * 112 + [7] * 24 + [8] * 8)
    fixed_dist = Huff([5] * 30)
    while True:
        last = br.get(1)
        kind = br.get(2)
        if br.bad:
            return out, False
        if kind == 0:
            br.bit = 0
            br.nbits = 0
            if br.pos + 4 > len(data):
                return out, False
            n = u16(data, br.pos)
            nn = u16(data, br.pos + 2)
            if n != (~nn & 0xFFFF) or br.pos + 4 + n > len(data):
                return out, False
            out.extend(data[br.pos + 4:br.pos + 4 + n])
            br.pos += 4 + n
        elif kind == 1:
            if not codes(br, out, fixed_lit, fixed_dist):
                return out, False
        elif kind == 2:
            nlen = br.get(5) + 257
            ndist = br.get(5) + 1
            ncode = br.get(4) + 4
            cl = [0] * 19
            for i in range(ncode):
                cl[CL_ORDER[i]] = br.get(3)
            clh = Huff(cl)
            lengths = []
            while len(lengths) < nlen + ndist:
                sym = decode(br, clh)
                if sym < 0:
                    return out, False
                if sym < 16:
                    lengths.append(sym)
                elif sym == 16:
                    if not lengths:
                        return out, False
                    lengths += [lengths[-1]] * (3 + br.get(2))
                elif sym == 17:
                    lengths += [0] * (3 + br.get(3))
                else:
                    lengths += [0] * (11 + br.get(7))
            if len(lengths) > nlen + ndist or br.bad:
                return out, False
            if not codes(br, out, Huff(lengths[:nlen]), Huff(lengths[nlen:])):
                return out, False
        else:
            return out, False
        if last:
            return out, True


# ------------------------------------------------------------ ZipCrypto

class Keys:
    def __init__(self, password):
        self.k0 = 305419896
        self.k1 = 591751049
        self.k2 = 878082192
        for c in password.encode():
            self.update(c)

    def update(self, c):
        self.k0 = crc_byte(self.k0, c)
        self.k1 = ((self.k1 + (self.k0 & 0xFF)) * 134775813 + 1) & 0xFFFFFFFF
        self.k2 = crc_byte(self.k2, self.k1 >> 24)

    def next(self):
        t = (self.k2 | 2) & 0xFFFF
        return ((t * (t ^ 1)) >> 8) & 0xFF

    def decrypt(self, data):
        out = []
        for b in data:
            p = b ^ self.next()
            self.update(p)
            out.append(p)
        return out


# ------------------------------------------------------------ the archive

class Entry:
    pass


class Archive:
    pass


EOCD_TEXT = ("  End-of-central-directory signature not found.  Either this file is not\n"
             "  a zipfile, or it constitutes one disk of a multi-part archive.  In the\n"
             "  latter case the central directory and zipfile comment will be found on\n"
             "  the last disk(s) of this archive.\n")


def open_archive(name, data):
    a = Archive()
    a.name = name
    a.size = len(data)
    a.data = data
    a.error = ""
    a.extra_bytes = 0
    a.entries = []
    # the end record is in the last 22 + 65535 bytes
    at = -1
    i = len(data) - 22
    stop = max(0, len(data) - 22 - 65535)
    while i >= stop:
        if data[i] == 0x50 and data[i + 1] == 0x4B and data[i + 2] == 5 and data[i + 3] == 6:
            at = i
            break
        i -= 1
    if at < 0:
        a.error = "eocd"
        return a
    count = u16(data, at + 10)
    cd_size = u32(data, at + 12)
    cd_off = u32(data, at + 16)
    clen = u16(data, at + 20)
    a.comment = data[at + 22:at + 22 + clen].decode("utf-8", "replace")
    end = at
    # a zip64 end record, through its locator
    if at >= 20 and u32(data, at - 20) == 0x07064B50:
        z = u64(data, at - 12)
        if z + 56 <= len(data) and u32(data, z) == 0x06064B50:
            count = u64(data, z + 32)
            cd_size = u64(data, z + 40)
            cd_off = u64(data, z + 48)
            end = z
    # a self-extractor's stub shifts every offset
    a.extra_bytes = end - cd_size - cd_off
    p = cd_off + a.extra_bytes
    for _ in range(count):
        if p + 46 > len(data) or u32(data, p) != 0x02014B50:
            a.error = "cd"
            return a
        e = Entry()
        e.made_by = u16(data, p + 4)
        e.flags = u16(data, p + 8)
        e.method = u16(data, p + 10)
        e.time = u16(data, p + 12)
        e.date = u16(data, p + 14)
        e.crc = u32(data, p + 16)
        e.csize = u32(data, p + 20)
        e.usize = u32(data, p + 24)
        nlen = u16(data, p + 28)
        xlen = u16(data, p + 30)
        klen = u16(data, p + 32)
        e.internal = u16(data, p + 36)
        e.external = u32(data, p + 38)
        e.offset = u32(data, p + 42)
        e.name = data[p + 46:p + 46 + nlen].decode("utf-8", "replace")
        e.has_extra = xlen > 0
        x = p + 46 + nlen
        xend = x + xlen
        while x + 4 <= xend:
            tag = u16(data, x)
            size = u16(data, x + 2)
            if tag == 1:
                q = x + 4
                if e.usize == 0xFFFFFFFF:
                    e.usize = u64(data, q)
                    q += 8
                if e.csize == 0xFFFFFFFF:
                    e.csize = u64(data, q)
                    q += 8
                if e.offset == 0xFFFFFFFF:
                    e.offset = u64(data, q)
            x += 4 + size
        e.comment = data[xend:xend + klen].decode("utf-8", "replace")
        a.entries.append(e)
        p = xend + klen
    return a


def is_dir(e):
    return e.name.endswith("/")


def is_link(e):
    return e.made_by >> 8 == 3 and (e.external >> 16) & 0o170000 == 0o120000


def encrypted(e):
    return e.flags & 1 != 0


# The entry's compressed bytes, past its local header.
def raw_data(a, e):
    p = e.offset + a.extra_bytes
    d = a.data
    if p + 30 > len(d) or u32(d, p) != 0x04034B50:
        return None
    start = p + 30 + u16(d, p + 26) + u16(d, p + 28)
    return d[start:start + e.csize]


# The entry's contents: (status, bytes), status "ok", "password",
# "crc" or "bad".
def contents(a, e, password):
    raw = raw_data(a, e)
    if raw is None:
        return "bad", []
    if encrypted(e):
        if password is None:
            return "password", []
        k = Keys(password)
        head = k.decrypt(raw[:12])
        check = (e.time >> 8) & 0xFF if e.flags & 8 else e.crc >> 24
        if len(head) < 12 or head[11] != check:
            return "password", []
        raw = k.decrypt(raw[12:])
    if e.method == 0:
        data = list(raw)
    elif e.method == 8:
        data, whole = inflate(raw)
        if not whole:
            return "bad", data
    else:
        return "bad", []
    if crc32(data) != e.crc:
        return "crc", data
    return "ok", data


# ------------------------------------------------------------ dates, modes, ratios

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def ymd(e):
    return 1980 + (e.date >> 9), (e.date >> 5) & 15, e.date & 31


def iso_date(e):
    y, m, d = ymd(e)
    return f"{y:04}-{m:02}-{d:02} {e.time >> 11:02}:{(e.time >> 5) & 63:02}"


def short_date(e):
    y, m, d = ymd(e)
    return f"{y % 100:02}-{MONTHS[m - 1]}-{d:02} {e.time >> 11:02}:{(e.time >> 5) & 63:02}"


def mode_str(e):
    if e.made_by >> 8 != 3:
        # an MS-DOS attribute byte
        attr = e.external & 0xFF
        s = "d" if attr & 0x10 else "-"
        s += "r"
        s += "-" if attr & 1 else "w"
        return s + "x" if attr & 0x10 else s + "-"
    m = e.external >> 16
    kinds = {0o040000: "d", 0o100000: "-", 0o120000: "l", 0o020000: "c", 0o060000: "b",
             0o010000: "p", 0o140000: "s"}
    s = kinds.get(m & 0o170000, "?")
    for sh in (6, 3, 0):
        bits = (m >> sh) & 7
        s += "r" if bits & 4 else "-"
        s += "w" if bits & 2 else "-"
        s += "x" if bits & 1 else "-"
    return s


OS_NAMES = {0: "fat", 3: "unx", 7: "mac", 10: "ntf", 19: "osx"}


# Info-ZIP's ratio(): the space saved, in tenths of a percent, rounded.
def ratio(uc, c):
    if uc == 0:
        return 0
    if uc > 2000000:
        denom = uc // 1000
        return (uc - c + (denom >> 1)) // denom if uc >= c else -((c - uc + (denom >> 1)) // denom)
    denom = uc
    return (1000 * (uc - c) + (denom >> 1)) // denom if uc >= c else -((1000 * (c - uc) + (denom >> 1)) // denom)


def percent(uc, c):
    r = ratio(uc, c)
    if r < 0:
        return "-" + f"{(-r + 5) // 10}".rjust(2)
    return f"{(r + 5) // 10:3}"


def method_name(e, long):
    if e.method == 0:
        return "Stored" if long else "stor"
    if e.method == 8:
        level = "NXFS"[(e.flags >> 1) & 3]
        return "Defl:" + level if long else "def" + level
    return f"Unk:{e.method:03}" if long else f"u{e.method:03}"


# ------------------------------------------------------------ name matching

# Info-ZIP's wildcards: `*` and `?` match `/` too.
def wild(p, s):
    if not p:
        return not s
    if p[0] == "*":
        return any(wild(p[1:], s[i:]) for i in range(len(s) + 1))
    if not s:
        return False
    if p[0] == "[":
        end = p.find("]", 1)
        if end > 0:
            body = p[1:end]
            neg = body.startswith("!") or body.startswith("^")
            if neg:
                body = body[1:]
            hit = False
            i = 0
            while i < len(body):
                if i + 2 < len(body) and body[i + 1] == "-":
                    hit = hit or body[i] <= s[0] <= body[i + 2]
                    i += 3
                else:
                    hit = hit or body[i] == s[0]
                    i += 1
            return hit != neg and wild(p[end + 1:], s[1:])
    if p[0] == "?" or p[0] == s[0]:
        return wild(p[1:], s[1:])
    return False


def selected(a, pats):
    if not pats:
        return list(a.entries), []
    used = [False] * len(pats)
    out = []
    for e in a.entries:
        hit = False
        for i, p in enumerate(pats):
            if wild(p, e.name):
                used[i] = True
                hit = True
        if hit:
            out.append(e)
    return out, [p for i, p in enumerate(pats) if not used[i]]


# ------------------------------------------------------------ the commands

class Job:
    def __init__(self):
        self.out = ""
        self.err = ""
        self.status = 0


def load(job, name, tool):
    path = "data/" + name
    if not os.path.isfile(path):
        job.err += f"{tool}:  cannot find or open {name}, {name}.zip or {name}.ZIP.\n"
        job.status = 9
        return None
    data = open(path, "rb").read()
    a = open_archive(name, data)
    return a


def eocd_error(job, a, tool, to_err):
    text = EOCD_TEXT + (f"{tool}:  cannot find zipfile directory in one of {a.name} or\n"
                        f"        {a.name}.zip, and cannot find {a.name}.ZIP, period.\n")
    if to_err:
        job.err += text
    else:
        job.out += text
    job.status = 9


def sfx_warning(a):
    return (f"warning [{a.name}]:  {a.extra_bytes} extra bytes at beginning or within zipfile\n"
            "  (attempting to process anyway)\n")


def zipinfo(job, args):
    a = load(job, args[0], "zipinfo")
    if a is None:
        return
    job.out += f"Archive:  {a.name}\n"
    if a.error:
        eocd_error(job, a, "zipinfo", False)
        return
    if a.extra_bytes:
        job.out += sfx_warning(a)
        job.status = 1
    job.out += f"Zip file size: {a.size} bytes, number of entries: {len(a.entries)}\n"
    tu = 0
    tc = 0
    for e in a.entries:
        v = e.made_by & 0xFF
        osname = OS_NAMES.get(e.made_by >> 8, "???")
        kind = "t" if e.internal & 1 else "b"
        if encrypted(e):
            kind = kind.upper()
        desc = e.flags & 8 != 0
        x = ("X" if desc else "x") if e.has_extra else ("l" if desc else "-")
        job.out += (f"{mode_str(e)}  {v // 10}.{v % 10} {osname} {e.usize:8} {kind}{x} "
                    f"{method_name(e, False)} {short_date(e)} {e.name}\n")
        tu += e.usize
        # zipinfo leaves out the 12-byte encryption headers
        tc += e.csize - 12 if encrypted(e) else e.csize
    r = ratio(tu, tc)
    sign = "-" if r < 0 else ""
    r = abs(r)
    n = len(a.entries)
    job.out += (f"{n} file{'' if n == 1 else 's'}, {tu} bytes uncompressed, {tc} bytes compressed:  "
                f"{sign}{r // 10}.{r % 10}%\n")


def header(job, a):
    job.out += f"Archive:  {a.name}\n"
    if a.comment:
        job.out += a.comment + "\n"


def list_cmd(job, args, verbose):
    a = load(job, args[0], "unzip")
    if a is None:
        return
    job.out += f"Archive:  {a.name}\n"
    if a.error:
        eocd_error(job, a, "unzip", True)
        return
    if a.comment:
        job.out += a.comment + "\n"
    entries, _ = selected(a, args[1:])
    tu = 0
    tc = 0
    if verbose:
        job.out += " Length   Method    Size  Cmpr    Date    Time   CRC-32   Name\n"
        job.out += "--------  ------  ------- ---- ---------- ----- --------  ----\n"
    else:
        job.out += "  Length      Date    Time    Name\n"
        job.out += "---------  ---------- -----   ----\n"
    for e in entries:
        if verbose:
            job.out += (f"{e.usize:8}  {method_name(e, True):<6} {e.csize:8} {percent(e.usize, e.csize)}% "
                        f"{iso_date(e)} {e.crc:08x}  {e.name}\n")
        else:
            job.out += f"{e.usize:9}  {iso_date(e)}   {e.name}\n"
        if e.comment:
            job.out += e.comment + "\n"
        tu += e.usize
        tc += e.csize
    n = len(entries)
    files = f"{n} file{'' if n == 1 else 's'}"
    if verbose:
        job.out += "--------          -------  ---                            -------\n"
        job.out += f"{tu:8}         {tc:8} {percent(tu, tc)}%                            {files}\n"
    else:
        job.out += "---------                     -------\n"
        job.out += f"{tu:9}                     {files}\n"
    if a.extra_bytes:
        job.err += sfx_warning(a)
        job.status = 1
    if args[1:] and n == 0:
        job.status = 11


def test_cmd(job, args, password):
    a = load(job, args[0], "unzip")
    if a is None:
        return
    job.out += f"Archive:  {a.name}\n"
    if a.error:
        eocd_error(job, a, "unzip", False)
        return
    if a.comment:
        job.out += a.comment + "\n"
    if a.extra_bytes:
        job.out += sfx_warning(a)
        job.status = 1
    entries, unmatched = selected(a, args[1:])
    errors = 0
    tested = 0
    skipped = 0
    for e in entries:
        st, data = contents(a, e, password)
        if st == "password":
            job.out += f"   skipping: {ljust(e.name, 22)}  incorrect password\n"
            skipped += 1
            continue
        tested += 1
        job.out += f"    testing: {ljust(e.name, 22)}   "
        if st == "ok":
            job.out += "OK\n"
        elif st == "crc":
            job.out += f"bad CRC {crc32(data):08x}  (should be {e.crc:08x})\n"
            errors += 1
        else:
            job.out += "error:  invalid compressed data to inflate\n"
            errors += 1
    for p in unmatched:
        job.out += f"caution: filename not matched:  {p}\n"
    if tested == 0 and skipped > 0:
        job.out += f"Caution:  zero files tested in {a.name}.\n"
    elif errors or unmatched:
        job.out += f"At least one error was detected in {a.name}.\n"
    else:
        job.out += f"No errors detected in compressed data of {a.name}.\n"
    if skipped:
        job.out += f"{skipped} file{'' if skipped == 1 else 's'} skipped because of incorrect password.\n"
    if unmatched:
        job.status = 11
    elif errors:
        job.status = 2
    elif skipped:
        job.status = 82


def pipe_cmd(job, args, password):
    a = load(job, args[0], "unzip")
    if a is None:
        return
    if a.error:
        job.out += f"Archive:  {a.name}\n"
        eocd_error(job, a, "unzip", False)
        return
    entries, unmatched = selected(a, args[1:])
    for e in entries:
        st, data = contents(a, e, password)
        if st != "password":
            job.out += bytes(data).decode("utf-8", "replace")
    for p in unmatched:
        job.err += f"caution: filename not matched:  {p}\n"
    if unmatched:
        job.status = 11


# The path an entry extracts to: Info-ZIP drops `..` components and a
# leading `/`, and says so.
def safe_name(job, name):
    parts = name.split("/")
    absolute = name.startswith("/")
    kept = []
    dotdot = False
    for p in parts:
        if p == "..":
            dotdot = True
        elif p == "." or (p == "" and not kept):
            continue
        else:
            kept.append(p)
    if dotdot:
        job.out += f'warning:  skipped "../" path component(s) in {name}\n'
        job.status = max(job.status, 1)
    if absolute:
        job.err += f"warning:  stripped absolute path spec from {name}\n"
        job.status = max(job.status, 1)
    return "/".join(kept)


def make_parents(path):
    parts = path.split("/")
    for i in range(1, len(parts)):
        d = "/".join(parts[:i])
        if not os.path.isdir(d):
            os.mkdir(d)


def extract_cmd(job, args, password, dest):
    a = load(job, args[0], "unzip")
    if a is None:
        return
    job.out += f"Archive:  {a.name}\n"
    if a.error:
        eocd_error(job, a, "unzip", False)
        return
    if a.comment:
        job.out += a.comment + "\n"
    if a.extra_bytes:
        job.out += sfx_warning(a)
        job.status = 1
    root = "data/" + dest
    if not os.path.isdir(root):
        try:
            os.mkdir(root)
        except OSError:
            job.err += (f"checkdir:  cannot create extraction directory: {dest}\n"
                        "           No such file or directory\n")
            job.status = 2
            return
    entries, unmatched = selected(a, args[1:])
    links = []
    for e in entries:
        rel = safe_name(job, e.name)
        shown = f"{dest}/{rel}"
        path = f"{root}/{rel}"
        if is_dir(e):
            d = path.rstrip("/")
            if not os.path.isdir(d):
                make_parents(d)
                os.mkdir(d)
                job.out += f"   creating: {shown}\n"
            continue
        st, data = contents(a, e, password)
        if st == "password":
            job.err += f"   skipping: {ljust(shown, 22)}  incorrect password\n"
            job.status = max(job.status, 1)
            continue
        if is_link(e):
            target = bytes(data).decode("utf-8", "replace")
            job.out += f"    linking: {ljust(shown, 22)}  -> {target} \n"
            links.append((shown, path, target))
            continue
        verb = " extracting: " if e.method == 0 else "  inflating: "
        job.out += f"{verb}{ljust(shown, 22)}  "
        make_parents(path)
        with open(path, "wb") as f:
            f.write(bytes(data))
        if st == "ok":
            job.out += "\n"
        elif st == "crc":
            job.err += f" bad CRC {crc32(data):08x}  (should be {e.crc:08x})\n"
            job.status = 2
        else:
            job.err += "  error:  invalid compressed data to inflate\n"
            job.status = 2
    if links:
        job.out += "finishing deferred symbolic links:\n"
        for shown, path, target in links:
            job.out += f"  {shown} -> {target}\n"
            # no symlinks here: the link is written as a file holding
            # its target, as Info-ZIP does where links are unsupported
            make_parents(path)
            with open(path, "wb") as f:
                f.write(target.encode())
    for p in unmatched:
        job.err += f"caution: filename not matched:  {p}\n"
        job.status = 11


def unzip(job, args):
    mode = "x"
    password = None
    dest = None
    rest = []
    i = 0
    while i < len(args):
        w = args[i]
        if w in ("-l", "-v", "-t", "-p"):
            mode = w[1]
        elif w == "-P":
            password = args[i + 1]
            i += 1
        elif w == "-d":
            dest = args[i + 1]
            i += 1
        else:
            rest.append(w)
        i += 1
    if mode == "l" or mode == "v":
        list_cmd(job, rest, mode == "v")
    elif mode == "t":
        test_cmd(job, rest, password)
    elif mode == "p":
        pipe_cmd(job, rest, password)
    else:
        extract_cmd(job, rest, password, dest)


def tree(job, root):
    base = "data/" + root
    if not os.path.isdir(base):
        job.out += f"tree: {root}: no such directory\n"
        return
    rows = []

    def walk(d, rel):
        for n in sorted(os.listdir(d)):
            p = f"{d}/{n}"
            r = n if rel == "" else f"{rel}/{n}"
            if os.path.isdir(p):
                rows.append((r + "/", f"     dir            {r}/\n"))
                walk(p, r)
            else:
                data = open(p, "rb").read()
                rows.append((r, f"{len(data):8}  {crc32(data):08x}  {r}\n"))
    walk(base, "")
    rows.sort()
    for _, line in rows:
        job.out += line


def main():
    # a fresh start for the extraction jobs
    import shutil
    for line in open("data/jobs.txt").read().splitlines():
        w = line.split(" ")
        if "-d" in w:
            top = "data/" + w[w.index("-d") + 1].split("/")[0]
            if os.path.isdir(top):
                shutil.rmtree(top)
    for line in open("data/jobs.txt").read().splitlines():
        if not line or line.startswith("#"):
            continue
        job = Job()
        w = line.split(" ")
        if w[0] == "zipinfo":
            zipinfo(job, w[1:])
        elif w[0] == "unzip":
            unzip(job, w[1:])
        elif w[0] == "tree":
            tree(job, w[1])
        text = f"$ {line}\n" + job.out + job.err
        if job.status:
            text += f"[exit status {job.status}]\n"
        sys.stdout.write(text + "\n")


main()
