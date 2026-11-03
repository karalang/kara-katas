"""The oracle for mini_lsm: the same store, written plainly in Python.

It follows the formats and rules the README states (the write-ahead log,
the table layout, the bloom filter, the MANIFEST, recovery and
compaction), so the Kāra port's files and output must match it byte for
byte.

Run from this directory, after mk.py: python3 -I -B oracle.py > expected.out
"""
import os
import shutil
import struct
import zlib

MEM_LIMIT = 2048
BLOCK_SIZE = 256
RESTART = 4
TABLE_BYTES = 2048
L0_TRIGGER = 4
BITS_PER_KEY = 10
PROBES = 6
MAGIC = 0x4B4152414C534D31
FOOTER = 40
DEL, VAL = 0, 1
M32 = 0xFFFFFFFF


class Fail(Exception):
    pass


# ------------------------------------------------------------ encoding

def varint(n):
    out = bytearray()
    while n >= 0x80:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    out.append(n)
    return bytes(out)


def get_varint(b, pos):
    n = 0
    shift = 0
    while True:
        if pos >= len(b) or shift > 28:
            raise Fail("bad varint")
        c = b[pos]
        pos += 1
        n |= (c & 0x7F) << shift
        if c < 0x80:
            return n, pos
        shift += 7


def ikey(user, seq, kind):
    return user.encode() + struct.pack("<Q", (seq << 8) | kind)


def split_ikey(k):
    t = struct.unpack("<Q", k[-8:])[0]
    return k[:-8].decode(), t >> 8, t & 0xFF


def ikey_lt(a, b):
    ua, ub = a[:-8], b[:-8]
    if ua != ub:
        return ua < ub
    return struct.unpack("<Q", a[-8:])[0] > struct.unpack("<Q", b[-8:])[0]


def bloom_hash(data):
    m = 0xC6A4A793
    h = (0xBC9F1D34 ^ (len(data) * m)) & M32
    i = 0
    while i + 4 <= len(data):
        w = struct.unpack("<I", data[i:i + 4])[0]
        h = (h + w) & M32
        h = (h * m) & M32
        h ^= h >> 16
        i += 4
    rest = len(data) - i
    if rest == 3:
        h = (h + (data[i + 2] << 16)) & M32
    if rest >= 2:
        h = (h + (data[i + 1] << 8)) & M32
    if rest >= 1:
        h = (h + data[i]) & M32
        h = (h * m) & M32
        h ^= h >> 24
    return h


def bloom_build(keys):
    bits = max(64, len(keys) * BITS_PER_KEY)
    nbytes = (bits + 7) // 8
    bits = nbytes * 8
    arr = bytearray(nbytes)
    for k in keys:
        h = bloom_hash(k.encode())
        delta = ((h >> 17) | (h << 15)) & M32
        for _ in range(PROBES):
            pos = h % bits
            arr[pos // 8] |= 1 << (pos % 8)
            h = (h + delta) & M32
    return bytes(arr) + bytes([PROBES])


def bloom_may_contain(f, key):
    if len(f) < 2:
        return True
    bits = (len(f) - 1) * 8
    k = f[-1]
    h = bloom_hash(key.encode())
    delta = ((h >> 17) | (h << 15)) & M32
    for _ in range(k):
        pos = h % bits
        if not f[pos // 8] & (1 << (pos % 8)):
            return False
        h = (h + delta) & M32
    return True


def crc(b):
    return zlib.crc32(b) & M32


def fname(n):
    return f"{n:06d}"


# ------------------------------------------------------------ tables

def build_block(entries):
    out = bytearray()
    restarts = []
    prev = b""
    for i, (k, v) in enumerate(entries):
        if i % RESTART == 0:
            restarts.append(len(out))
            shared = 0
        else:
            shared = 0
            while shared < min(len(prev), len(k)) and prev[shared] == k[shared]:
                shared += 1
        out += varint(shared) + varint(len(k) - shared) + varint(len(v))
        out += k[shared:] + v
        prev = k
    for r in restarts:
        out += struct.pack("<I", r)
    out += struct.pack("<I", len(restarts))
    return bytes(out)


def write_table(path, entries):
    """entries: sorted (ikey, value) pairs. Returns (bytes, blocks)."""
    out = bytearray()
    index = bytearray()
    blocks = 0
    cur = []
    size = 0
    users = []
    for i, (k, v) in enumerate(entries):
        cur.append((k, v))
        size += len(k) + len(v) + 3
        u = k[:-8].decode()
        if not users or users[-1] != u:
            users.append(u)
        if size >= BLOCK_SIZE or i == len(entries) - 1:
            blk = build_block(cur)
            index += varint(len(cur[-1][0])) + cur[-1][0] + varint(len(out)) + varint(len(blk))
            out += blk + struct.pack("<I", crc(blk))
            blocks += 1
            cur = []
            size = 0
    filt = bloom_build(users)
    foff = len(out)
    out += filt
    ioff = len(out)
    out += index
    out += struct.pack("<QQQQQ", ioff, len(index), foff, len(filt), MAGIC)
    with open(path, "wb") as fh:
        fh.write(out)
    return len(out), blocks


class Table:
    def __init__(self, path, num):
        self.num = num
        self.name = fname(num) + ".sst"
        self.path = path
        try:
            with open(path, "rb") as fh:
                self.data = fh.read()
        except OSError:
            raise Fail(f"{self.name}: cannot read")
        d = self.data
        if len(d) < FOOTER:
            raise Fail(f"{self.name}: too short for a footer")
        ioff, ilen, foff, flen, magic = struct.unpack("<QQQQQ", d[-FOOTER:])
        if magic != MAGIC:
            raise Fail(f"{self.name}: bad magic")
        if ioff + ilen > len(d) - FOOTER or foff + flen > ioff:
            raise Fail(f"{self.name}: footer points past the end")
        self.filter = d[foff:foff + flen]
        self.index = []
        idx = d[ioff:ioff + ilen]
        p = 0
        while p < len(idx):
            kl, p = get_varint(idx, p)
            k = idx[p:p + kl]
            p += kl
            off, p = get_varint(idx, p)
            size, p = get_varint(idx, p)
            self.index.append((k, off, size))

    def block(self, i):
        k, off, size = self.index[i]
        d = self.data
        if off + size + 4 > len(d):
            raise Fail(f"{self.name}: block {i} runs past the end")
        blk = d[off:off + size]
        want = struct.unpack("<I", d[off + size:off + size + 4])[0]
        if crc(blk) != want:
            raise Fail(f"{self.name}: block {i}: bad checksum")
        return blk


def block_restarts(blk):
    n = struct.unpack("<I", blk[-4:])[0]
    start = len(blk) - 4 - 4 * n
    return [struct.unpack("<I", blk[start + 4 * i:start + 4 * i + 4])[0] for i in range(n)], start


def block_entries(blk):
    restarts, end = block_restarts(blk)
    out = []
    p = 0
    prev = b""
    while p < end:
        shared, p = get_varint(blk, p)
        unshared, p = get_varint(blk, p)
        vlen, p = get_varint(blk, p)
        k = prev[:shared] + blk[p:p + unshared]
        p += unshared
        v = blk[p:p + vlen]
        p += vlen
        out.append((k, v))
        prev = k
    return out


def block_seek(blk, target):
    """The first entry >= target, found by a binary search over the
    restart points and a scan from the last restart below target."""
    restarts, end = block_restarts(blk)
    lo, hi = 0, len(restarts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        p = restarts[mid]
        _, p = get_varint(blk, p)
        unshared, p = get_varint(blk, p)
        _, p = get_varint(blk, p)
        k = blk[p:p + unshared]
        if ikey_lt(k, target):
            lo = mid
        else:
            hi = mid - 1
    p = restarts[lo]
    prev = b""
    while p < end:
        shared, p = get_varint(blk, p)
        unshared, p = get_varint(blk, p)
        vlen, p = get_varint(blk, p)
        k = prev[:shared] + blk[p:p + unshared]
        p += unshared
        v = blk[p:p + vlen]
        p += vlen
        if not ikey_lt(k, target):
            return k, v
        prev = k
    return None


# ------------------------------------------------------------ the store

class Meta:
    def __init__(self, level, num, entries, size, smallest, largest):
        self.level, self.num, self.entries, self.size = level, num, entries, size
        self.smallest, self.largest = smallest, largest


class Store:
    def __init__(self, name):
        self.name = name
        self.dir = os.path.join("data", name)
        self.next = 1
        self.seq = 0
        self.log = 0
        self.tables = []
        self.mem = {}
        self.mem_bytes = 0
        self.mem_entries = 0
        self.snaps = {}

    def path(self, n, ext):
        return os.path.join(self.dir, fname(n) + ext)

    def log_path(self):
        return self.path(self.log, ".log")

    def save_manifest(self):
        lines = ["kara-lsm 1", f"next {self.next}", f"seq {self.seq}", f"log {self.log}"]
        for t in sorted(self.tables, key=lambda t: (t.level, t.num)):
            lines.append(f"table {t.level} {t.num} {t.entries} {t.size} {t.smallest} {t.largest}")
        tmp = os.path.join(self.dir, "MANIFEST.tmp")
        with open(tmp, "w", encoding="utf-8", newline="") as fh:
            fh.write("\n".join(lines) + "\n")
        os.replace(tmp, os.path.join(self.dir, "MANIFEST"))

    def load_manifest(self):
        try:
            with open(os.path.join(self.dir, "MANIFEST"), encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            raise Fail(f"{self.name}: cannot read MANIFEST")
        lines = text.split("\n")
        if lines[0] != "kara-lsm 1":
            raise Fail(f"{self.name}: MANIFEST: bad header")
        for ln in lines[1:]:
            if not ln:
                continue
            f = ln.split(" ")
            if f[0] == "next" and len(f) == 2:
                self.next = int(f[1])
            elif f[0] == "seq" and len(f) == 2:
                self.seq = int(f[1])
            elif f[0] == "log" and len(f) == 2:
                self.log = int(f[1])
            elif f[0] == "table" and len(f) == 7:
                self.tables.append(Meta(int(f[1]), int(f[2]), int(f[3]), int(f[4]), f[5], f[6]))
            else:
                raise Fail(f"{self.name}: MANIFEST: bad line: {ln}")

    def new_log(self):
        self.log = self.next
        self.next += 1
        open(self.log_path(), "wb").close()

    # -------------------------------------------------------- writes

    def apply(self, seq, kind, key, value):
        self.mem.setdefault(key, []).insert(0, (seq, kind, value))
        self.mem_bytes += len(key) + len(value) + 16
        self.mem_entries += 1

    def write(self, ops, out):
        """ops: (kind, key, value). One log record, then the memtable."""
        first = self.seq + 1
        payload = bytearray(struct.pack("<QI", first, len(ops)))
        for kind, k, v in ops:
            payload.append(kind)
            payload += varint(len(k)) + k.encode()
            if kind == VAL:
                payload += varint(len(v)) + v.encode()
        rec = struct.pack("<II", crc(bytes(payload)), len(payload)) + payload
        with open(self.log_path(), "ab") as fh:
            fh.write(rec)
        for i, (kind, k, v) in enumerate(ops):
            self.apply(first + i, kind, k, v)
        self.seq = first + len(ops) - 1
        if self.mem_bytes >= MEM_LIMIT:
            self.flush(out, "  ")
        return first

    def flush(self, out, pad):
        if not self.mem:
            out.append(f"{pad}memtable empty")
            return
        entries = []
        for k in sorted(self.mem):
            for seq, kind, v in self.mem[k]:
                entries.append((ikey(k, seq, kind), v.encode()))
        num = self.next
        self.next += 1
        size, blocks = write_table(self.path(num, ".sst"), entries)
        keys = sorted(self.mem)
        self.tables.append(Meta(0, num, len(entries), size, keys[0], keys[-1]))
        old = self.log_path()
        self.new_log()
        self.save_manifest()
        os.remove(old)
        out.append(f"{pad}flush -> L0 {fname(num)}.sst: {len(entries)} entries, {blocks} blocks, {size} bytes")
        self.mem = {}
        self.mem_bytes = 0
        self.mem_entries = 0
        if sum(1 for t in self.tables if t.level == 0) >= L0_TRIGGER:
            self.compact(out, pad)

    def compact(self, out, pad):
        inputs = [t for t in self.tables if t.level in (0, 1)]
        if not inputs:
            out.append(f"{pad}nothing to compact")
            return
        versions = {}
        total = 0
        for t in inputs:
            tab = Table(self.path(t.num, ".sst"), t.num)
            for i in range(len(tab.index)):
                for k, v in block_entries(tab.block(i)):
                    u, seq, kind = split_ikey(k)
                    versions.setdefault(u, []).append((seq, kind, v))
                    total += 1
        bounds = sorted(self.snaps.values()) + [self.seq]
        kept_entries = []
        for u in sorted(versions):
            vs = sorted(versions[u], key=lambda x: -x[0])
            keep = []
            for b in bounds:
                for seq, kind, v in vs:
                    if seq <= b:
                        if (seq, kind, v) not in keep:
                            keep.append((seq, kind, v))
                        break
            keep.sort(key=lambda x: -x[0])
            while keep and keep[-1][1] == DEL:
                keep.pop()
            for seq, kind, v in keep:
                kept_entries.append((u, ikey(u, seq, kind), v))
        new = []
        cur = []
        size = 0
        groups = []
        for j, (u, k, v) in enumerate(kept_entries):
            if cur and size >= TABLE_BYTES and cur[-1][0] != u:
                groups.append(cur)
                cur = []
                size = 0
            cur.append((u, k, v))
            size += len(k) + len(v)
        if cur:
            groups.append(cur)
        for g in groups:
            num = self.next
            self.next += 1
            sz, _ = write_table(self.path(num, ".sst"), [(k, v) for _, k, v in g])
            new.append(Meta(1, num, len(g), sz, g[0][0], g[-1][0]))
        self.tables = [t for t in self.tables if t.level not in (0, 1)] + new
        self.save_manifest()
        for t in inputs:
            os.remove(self.path(t.num, ".sst"))
        n0 = sum(1 for t in inputs if t.level == 0)
        n1 = len(inputs) - n0
        out.append(
            f"{pad}compact {n0} L0 + {n1} L1 tables ({total} entries) -> {len(new)} L1 tables, "
            f"{len(kept_entries)} entries kept, {total - len(kept_entries)} dropped"
        )

    # -------------------------------------------------------- reads

    def get(self, key, snap):
        read = 0
        skipped = 0
        if key in self.mem:
            for seq, kind, v in self.mem[key]:
                if seq <= snap:
                    return (kind, v, seq, "memtable", read, skipped)
        l0 = sorted((t for t in self.tables if t.level == 0), key=lambda t: -t.num)
        l1 = sorted((t for t in self.tables if t.level == 1), key=lambda t: t.smallest)
        target = ikey(key, snap, VAL)
        for t in l0 + l1:
            if key < t.smallest or key > t.largest:
                continue
            tab = Table(self.path(t.num, ".sst"), t.num)
            if not bloom_may_contain(tab.filter, key):
                skipped += 1
                continue
            read += 1
            lo, hi = 0, len(tab.index)
            while lo < hi:
                mid = (lo + hi) // 2
                if ikey_lt(tab.index[mid][0], target):
                    lo = mid + 1
                else:
                    hi = mid
            if lo == len(tab.index):
                continue
            hit = block_seek(tab.block(lo), target)
            if hit is None:
                continue
            u, seq, kind = split_ikey(hit[0])
            if u == key:
                return (kind, hit[1].decode(), seq, f"L{t.level} {fname(t.num)}", read, skipped)
        return None, None, None, None, read, skipped

    def scan(self, lo, hi, snap):
        versions = {}
        for k, vs in self.mem.items():
            if lo <= k < hi:
                versions.setdefault(k, []).extend(vs)
        for t in self.tables:
            if t.largest < lo or t.smallest >= hi:
                continue
            tab = Table(self.path(t.num, ".sst"), t.num)
            for i in range(len(tab.index)):
                for k, v in block_entries(tab.block(i)):
                    u, seq, kind = split_ikey(k)
                    if lo <= u < hi:
                        versions.setdefault(u, []).append((seq, kind, v.decode()))
        rows = []
        for u in sorted(versions):
            best = None
            for seq, kind, v in versions[u]:
                if seq <= snap and (best is None or seq > best[0]):
                    best = (seq, kind, v)
            if best and best[1] == VAL:
                rows.append((u, best[2]))
        return rows

    # -------------------------------------------------------- recovery

    def replay(self):
        path = self.log_path()
        try:
            with open(path, "rb") as fh:
                data = fh.read()
        except OSError:
            raise Fail(f"{self.name}: cannot read {fname(self.log)}.log")
        p = 0
        records = 0
        ops = 0
        why = None
        while p < len(data):
            if p + 8 > len(data):
                why = "torn header"
                break
            want, n = struct.unpack("<II", data[p:p + 8])
            if p + 8 + n > len(data):
                why = "torn record"
                break
            payload = data[p + 8:p + 8 + n]
            if crc(payload) != want:
                why = "bad checksum"
                break
            try:
                seq, count = struct.unpack("<QI", payload[:12])
                q = 12
                batch = []
                for _ in range(count):
                    kind = payload[q]
                    q += 1
                    kl, q = get_varint(payload, q)
                    k = payload[q:q + kl].decode()
                    q += kl
                    v = ""
                    if kind == VAL:
                        vl, q = get_varint(payload, q)
                        v = payload[q:q + vl].decode()
                        q += vl
                    batch.append((kind, k, v))
            except (Fail, IndexError, struct.error):
                why = "bad record"
                break
            for i, (kind, k, v) in enumerate(batch):
                self.apply(seq + i, kind, k, v)
            self.seq = max(self.seq, seq + count - 1)
            records += 1
            ops += count
            p += 8 + n
        msg = f"{fname(self.log)}.log: {records} records ({ops} ops) replayed"
        if why:
            msg += f", stopped at record {records + 1}: {why}, {len(data) - p} bytes dropped"
            with open(path, "r+b") as fh:
                fh.truncate(p)
        return msg


# ------------------------------------------------------------ session

def clip(v):
    return v if len(v) <= 24 else v[:24] + "..."


def fnv(s):
    h = 0x811C9DC5
    for c in s.encode():
        h ^= c
        h = (h * 0x01000193) & M32
    return h


def gen_value(key, size):
    unit = f"{fnv(key):08x}"
    return (unit * (size // 8 + 1))[:size]


def is_token(s):
    return len(s) > 0 and all(33 <= ord(c) <= 126 for c in s)


def parse_int(s):
    if not s.isdigit() or len(s) > 9:
        raise Fail(f"bad number: {s}")
    return int(s)


class Session:
    def __init__(self):
        self.stores = {}

    def store(self, name):
        if name not in self.stores:
            raise Fail(f"no open store named {name}")
        return self.stores[name]

    def snap_of(self, st, args):
        if args and args[-1].startswith("@"):
            s = args[-1][1:]
            if s not in st.snaps:
                raise Fail(f"no snapshot named {s}")
            return st.snaps[s], args[:-1]
        return st.seq, args

    def job(self, line, out):
        a = line.split()
        cmd, args = a[0], a[1:]
        need = {"create": 1, "open": 1, "crash": 1, "stats": 1, "ls": 1, "check": 1,
                "flush": 1, "compact": 1, "put": 3, "del": 2, "get": 2, "snap": 2,
                "release": 2, "sst": 2, "tear": 2, "flip": 3, "putn": 4, "load": 2}
        if cmd == "scan":
            if len(args) < 3:
                raise Fail("scan: needs a store and a range")
        elif cmd == "batch":
            if len(args) < 2:
                raise Fail("batch: needs a store and operations")
        elif cmd in need:
            n = need[cmd]
            ok = len(args) == n or (cmd == "get" and len(args) == 3)
            if not ok:
                raise Fail(f"{cmd}: needs {n} arguments")
        else:
            raise Fail(f"unknown command: {cmd}")

        if cmd == "create":
            name = args[0]
            if name in self.stores:
                raise Fail(f"{name} is already open")
            d = os.path.join("data", name)
            if os.path.isdir(d):
                shutil.rmtree(d)
            os.makedirs(d)
            st = Store(name)
            st.new_log()
            st.save_manifest()
            self.stores[name] = st
            out.append(f"created {name}: log {fname(st.log)}.log")
            return
        if cmd == "open":
            name = args[0]
            if name in self.stores:
                raise Fail(f"{name} is already open")
            st = Store(name)
            st.load_manifest()
            msg = st.replay()
            self.stores[name] = st
            n = len(st.tables)
            out.append(f"opened {name}: seq {st.seq}, {n} tables, {msg}")
            return
        if cmd in ("tear", "flip") and args[0] not in self.stores:
            # Disk tools: they work on a closed store through its MANIFEST.
            st = Store(args[0])
            st.load_manifest()
        else:
            st = self.store(args[0])
        if cmd == "crash":
            size = os.path.getsize(st.log_path())
            del self.stores[args[0]]
            out.append(f"crashed {st.name}: {st.mem_entries} memtable entries lost, "
                       f"{fname(st.log)}.log holds {size} bytes")
        elif cmd == "put":
            k, v = args[1], args[2]
            seq = st.write([(VAL, k, v)], sub := [])
            out.append(f"put {k} (seq {seq})")
            out.extend(sub)
        elif cmd == "del":
            seq = st.write([(DEL, args[1], "")], sub := [])
            out.append(f"del {args[1]} (seq {seq})")
            out.extend(sub)
        elif cmd == "batch":
            ops = []
            for tok in args[1:]:
                if tok.startswith("-") and len(tok) > 1:
                    ops.append((DEL, tok[1:], ""))
                elif "=" in tok and tok.index("=") > 0:
                    i = tok.index("=")
                    ops.append((VAL, tok[:i], tok[i + 1:]))
                else:
                    raise Fail(f"batch: bad operation: {tok}")
            first = st.write(ops, sub := [])
            out.append(f"batch of {len(ops)} (seq {first}..{first + len(ops) - 1})")
            out.extend(sub)
        elif cmd == "putn":
            prefix = args[1]
            n = parse_int(args[2])
            size = parse_int(args[3])
            sub = []
            first = st.seq + 1
            for i in range(n):
                k = f"{prefix}{i:05d}"
                st.write([(VAL, k, gen_value(k, size))], sub)
            out.append(f"put {n} keys {prefix}00000..{prefix}{n - 1:05d} (seq {first}..{st.seq})")
            out.extend(sub)
        elif cmd == "load":
            try:
                with open(os.path.join("data", args[1]), encoding="utf-8") as fh:
                    text = fh.read()
            except OSError:
                raise Fail(f"{args[1]}: cannot read")
            sub = []
            first = st.seq + 1
            rows = 0
            skipped = 0
            for i, ln in enumerate(text.split("\n")):
                if i == 0 or not ln:
                    continue
                f = ln.split(",")
                if len(f) != 4 or not all(is_token(x) for x in f):
                    skipped += 1
                    continue
                st.write([(VAL, f"sku:{f[0]}", f"{f[1]}|{f[2]}|{f[3]}")], sub)
                rows += 1
            out.append(f"loaded {rows} rows from {args[1]} (seq {first}..{st.seq}), {skipped} skipped")
            out.extend(sub)
        elif cmd == "get":
            snap, rest = self.snap_of(st, args)
            if len(rest) != 2:
                raise Fail("get: needs 2 arguments")
            k = rest[1]
            kind, v, seq, src, r, s = st.get(k, snap)
            tail = f"read {r}, skipped {s}"
            if kind is None:
                out.append(f"{k}: not found ({tail})")
            elif kind == DEL:
                out.append(f"{k}: deleted at seq {seq} ({src}, {tail})")
            else:
                out.append(f"{k} = {v} ({src}, {tail})")
        elif cmd == "scan":
            snap, rest = self.snap_of(st, args)
            if len(rest) not in (3, 4):
                raise Fail("scan: needs a store and a range")
            lo, hi = rest[1], rest[2]
            if not lo < hi:
                raise Fail(f"scan: empty range [{lo}, {hi})")
            limit = parse_int(rest[3]) if len(rest) == 4 else 10
            rows = st.scan(lo, hi, snap)
            out.append(f"scan [{lo}, {hi}): {len(rows)} keys")
            for k, v in rows[:limit]:
                out.append(f"  {k} = {clip(v)}")
            if len(rows) > limit:
                out.append(f"  ... {len(rows) - limit} more")
        elif cmd == "snap":
            st.snaps[args[1]] = st.seq
            out.append(f"snapshot {args[1]} at seq {st.seq}")
        elif cmd == "release":
            if args[1] not in st.snaps:
                raise Fail(f"no snapshot named {args[1]}")
            del st.snaps[args[1]]
            out.append(f"released {args[1]}")
        elif cmd == "flush":
            st.flush(out, "")
        elif cmd == "compact":
            st.compact(out, "")
        elif cmd == "stats":
            out.append(f"{st.name}: seq {st.seq}, memtable {st.mem_entries} entries "
                       f"({st.mem_bytes} bytes), log {fname(st.log)}.log "
                       f"{os.path.getsize(st.log_path())} bytes")
            for lvl in (0, 1):
                ts = [t for t in st.tables if t.level == lvl]
                names = " ".join(fname(t.num) for t in sorted(ts, key=lambda t: t.num))
                out.append(f"  L{lvl}: {len(ts)} tables, {sum(t.entries for t in ts)} entries, "
                           f"{sum(t.size for t in ts)} bytes" + (f" [{names}]" if ts else ""))
            if st.snaps:
                out.append("  snapshots: " + " ".join(f"{k}@{v}" for k, v in sorted(st.snaps.items())))
        elif cmd == "ls":
            out.append(f"{st.name}/:")
            for n in sorted(os.listdir(st.dir)):
                out.append(f"  {n} {os.path.getsize(os.path.join(st.dir, n))}")
        elif cmd == "sst":
            num = parse_int(args[1])
            meta = [t for t in st.tables if t.num == num]
            if not meta:
                raise Fail(f"no table {fname(num)} in {st.name}")
            t = meta[0]
            tab = Table(st.path(num, ".sst"), num)
            out.append(f"{tab.name}: L{t.level}, {t.entries} entries, {len(tab.index)} blocks, "
                       f"{len(tab.data)} bytes, keys {t.smallest} .. {t.largest}")
            out.append(f"  bloom: {(len(tab.filter) - 1) * 8} bits, {tab.filter[-1]} probes")
            for i, (k, off, size) in enumerate(tab.index):
                blk = tab.block(i)
                rs, _ = block_restarts(blk)
                n = len(block_entries(blk))
                u, seq, kind = split_ikey(k)
                out.append(f"  block {i}: offset {off}, {size} bytes, {n} entries, "
                           f"{len(rs)} restarts, last {u}@{seq}")
        elif cmd == "check":
            out.append(f"check {st.name}: {len(st.tables)} tables")
            for t in sorted(st.tables, key=lambda t: t.num):
                out.append("  " + check_table(st, t))
        elif cmd == "tear":
            n = parse_int(args[1])
            p = st.log_path()
            size = os.path.getsize(p)
            if n > size:
                raise Fail(f"tear: {fname(st.log)}.log holds only {size} bytes")
            with open(p, "r+b") as fh:
                fh.truncate(size - n)
            out.append(f"tore {n} bytes off {fname(st.log)}.log, {size - n} left")
        elif cmd == "flip":
            if args[1] == "log":
                p = st.log_path()
                shown = f"{fname(st.log)}.log"
            else:
                num = parse_int(args[1])
                p = st.path(num, ".sst")
                shown = f"{fname(num)}.sst"
                if not os.path.exists(p):
                    raise Fail(f"no file {shown} in {st.name}")
            off = parse_int(args[2])
            size = os.path.getsize(p)
            if off >= size:
                raise Fail(f"flip: {shown} holds only {size} bytes")
            with open(p, "r+b") as fh:
                fh.seek(off)
                b = fh.read(1)
                fh.seek(off)
                fh.write(bytes([b[0] ^ 0xFF]))
            out.append(f"flipped byte {off} of {shown}")


def check_table(st, t):
    try:
        tab = Table(st.path(t.num, ".sst"), t.num)
        n = 0
        prev = None
        for i in range(len(tab.index)):
            ents = block_entries(tab.block(i))
            for k, _ in ents:
                if prev is not None and not ikey_lt(prev, k):
                    return f"{tab.name}: block {i}: keys out of order"
                prev = k
            if ents and ents[-1][0] != tab.index[i][0]:
                return f"{tab.name}: block {i}: index key does not match"
            n += len(ents)
        if n != t.entries:
            return f"{tab.name}: {n} entries, MANIFEST says {t.entries}"
        return f"{tab.name}: ok, {n} entries in {len(tab.index)} blocks"
    except Fail as e:
        return str(e)


def main():
    with open("data/jobs.txt", encoding="utf-8") as fh:
        jobs = fh.read()
    s = Session()
    out = []
    for line in jobs.split("\n"):
        t = line.strip()
        if not t or t.startswith("#"):
            continue
        out.append(f"> {t}")
        sub = []
        try:
            s.job(t, sub)
            out.extend(sub)
        except Fail as e:
            out.extend(sub)
            out.append(f"! {e}")
    print("\n".join(out))


main()
