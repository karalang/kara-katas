# Python mirror of mini_bzip2: runs data/jobs.txt with a port of bzip2 1.0.8
# (compressor, decompressor and test mode) and sha256sum.
import hashlib, os, shutil, sys

out = []
def w(s):
    out.append(s)

# ---- CRC32, big-endian, as bzip2 uses it ----
CRC = []
for i in range(256):
    c = i << 24
    for _ in range(8):
        c = ((c << 1) ^ 0x04c11db7) & 0xffffffff if c & 0x80000000 else (c << 1) & 0xffffffff
    CRC.append(c)

def crc_update(c, b):
    return ((c << 8) & 0xffffffff) ^ CRC[(c >> 24) ^ b]

# ---- bit writer ----
class BW:
    def __init__(self):
        self.buf = bytearray(); self.acc = 0; self.n = 0
    def bits(self, n, v):
        self.acc = (self.acc << n) | v; self.n += n
        while self.n >= 8:
            self.n -= 8
            self.buf.append((self.acc >> self.n) & 0xff)
        self.acc &= (1 << self.n) - 1
    def finish(self):
        if self.n:
            self.buf.append((self.acc << (8 - self.n)) & 0xff)
            self.acc = 0; self.n = 0

# ---- compressor ----
def rle1_blocks(data, level):
    # splits the input into blocks after run-length stage one; each block
    # carries its bytes and the CRC of the input it covers
    nmax = 100000 * level - 19
    blocks = []
    blk = bytearray(); crc = 0xffffffff
    i = 0
    while i < len(data):
        ch = data[i]; ln = 1
        while i + ln < len(data) and data[i + ln] == ch and ln < 255:
            ln += 1
        if len(blk) >= nmax:
            blocks.append((blk, crc ^ 0xffffffff)); blk = bytearray(); crc = 0xffffffff
        for _ in range(ln):
            crc = crc_update(crc, ch)
        if ln < 4:
            blk.extend([ch] * ln)
        else:
            blk.extend([ch] * 4); blk.append(ln - 4)
        i += ln
    if blk:
        blocks.append((blk, crc ^ 0xffffffff))
    return blocks

def bwt_sort(blk):
    # cyclic rotations sorted by prefix doubling
    n = len(blk)
    rank = list(blk)
    ptr = list(range(n))
    k = 1
    while True:
        key = [rank[i] * (n + 256) + rank[(i + k) % n] for i in range(n)]
        ptr.sort(key=lambda i: key[i])
        nr = [0] * n
        r = 0
        for j in range(1, n):
            if key[ptr[j]] != key[ptr[j - 1]]:
                r += 1
            nr[ptr[j]] = r
        rank = nr
        if r == n - 1 or k >= n:
            break
        k *= 2
    return ptr

def make_code_lengths(freq, alpha, maxlen):
    weight = [0] * (alpha * 2 + 2)
    parent = [0] * (alpha * 2 + 2)
    heap = [0] * (alpha + 4)
    for i in range(alpha):
        weight[i + 1] = (1 if freq[i] == 0 else freq[i]) << 8
    while True:
        nnodes = alpha; nheap = 0
        heap[0] = 0; weight[0] = 0; parent[0] = -2
        def up(z):
            tmp = heap[z]
            while weight[tmp] < weight[heap[z >> 1]]:
                heap[z] = heap[z >> 1]; z >>= 1
            heap[z] = tmp
        def down(z):
            tmp = heap[z]
            while True:
                y = z << 1
                if y > nheap:
                    break
                if y < nheap and weight[heap[y + 1]] < weight[heap[y]]:
                    y += 1
                if weight[tmp] < weight[heap[y]]:
                    break
                heap[z] = heap[y]; z = y
            heap[z] = tmp
        for i in range(1, alpha + 1):
            parent[i] = -1; nheap += 1; heap[nheap] = i; up(nheap)
        while nheap > 1:
            n1 = heap[1]; heap[1] = heap[nheap]; nheap -= 1; down(1)
            n2 = heap[1]; heap[1] = heap[nheap]; nheap -= 1; down(1)
            nnodes += 1
            parent[n1] = nnodes; parent[n2] = nnodes
            w1 = weight[n1]; w2 = weight[n2]
            weight[nnodes] = ((w1 & 0xffffff00) + (w2 & 0xffffff00)) | (1 + max(w1 & 0xff, w2 & 0xff))
            parent[nnodes] = -1
            nheap += 1; heap[nheap] = nnodes; up(nheap)
        lens = [0] * alpha
        too_long = False
        for i in range(1, alpha + 1):
            j = 0; k = i
            while parent[k] >= 0:
                k = parent[k]; j += 1
            lens[i - 1] = j
            if j > maxlen:
                too_long = True
        if not too_long:
            return lens
        for i in range(1, alpha + 1):
            j = weight[i] >> 8
            weight[i] = (1 + j // 2) << 8

def compress_block(bw, blk, bcrc):
    n = len(blk)
    ptr = bwt_sort(blk)
    orig = ptr.index(0)
    for b in (0x31, 0x41, 0x59, 0x26, 0x53, 0x59):
        bw.bits(8, b)
    bw.bits(32, bcrc)
    bw.bits(1, 0)
    bw.bits(24, orig)
    # MTF and RUNA/RUNB
    in_use = [False] * 256
    for b in blk:
        in_use[b] = True
    seq = [0] * 256; ninuse = 0
    for i in range(256):
        if in_use[i]:
            seq[i] = ninuse; ninuse += 1
    eob = ninuse + 1
    alpha = ninuse + 2
    freq = [0] * alpha
    mtfv = []
    yy = list(range(ninuse))
    zp = 0
    def flush(zp):
        zp -= 1
        while True:
            s = 1 if zp & 1 else 0
            mtfv.append(s); freq[s] += 1
            if zp < 2:
                break
            zp = (zp - 2) // 2
    for i in range(n):
        j = ptr[i] - 1
        if j < 0:
            j += n
        ll = seq[blk[j]]
        if yy[0] == ll:
            zp += 1
        else:
            if zp > 0:
                flush(zp); zp = 0
            k = yy.index(ll)
            del yy[k]; yy.insert(0, ll)
            mtfv.append(k + 1); freq[k + 1] += 1
    if zp > 0:
        flush(zp)
    mtfv.append(eob); freq[eob] += 1
    nmtf = len(mtfv)
    # coding tables
    ng = 2 if nmtf < 200 else 3 if nmtf < 600 else 4 if nmtf < 1200 else 5 if nmtf < 2400 else 6
    lens = [[15] * alpha for _ in range(ng)]
    npart = ng; remf = nmtf; gs = 0
    while npart > 0:
        tf = remf // npart
        ge = gs - 1; af = 0
        while af < tf and ge < alpha - 1:
            ge += 1; af += freq[ge]
        if ge > gs and npart != ng and npart != 1 and (ng - npart) % 2 == 1:
            af -= freq[ge]; ge -= 1
        for v in range(alpha):
            lens[npart - 1][v] = 0 if gs <= v <= ge else 15
        npart -= 1; gs = ge + 1; remf -= af
    for _ in range(4):
        rfreq = [[0] * alpha for _ in range(ng)]
        sels = []
        gs = 0
        while gs < nmtf:
            ge = min(gs + 49, nmtf - 1)
            bt = -1; bc = 999999999
            for t in range(ng):
                c = 0
                for i in range(gs, ge + 1):
                    c += lens[t][mtfv[i]]
                if c < bc:
                    bc = c; bt = t
            sels.append(bt)
            for i in range(gs, ge + 1):
                rfreq[bt][mtfv[i]] += 1
            gs = ge + 1
        for t in range(ng):
            lens[t] = make_code_lengths(rfreq[t], alpha, 17)
    pos = list(range(ng))
    selmtf = []
    for s in sels:
        j = pos.index(s)
        del pos[j]; pos.insert(0, s)
        selmtf.append(j)
    codes = []
    for t in range(ng):
        c = [0] * alpha
        vec = 0
        for ln in range(min(lens[t]), max(lens[t]) + 1):
            for i in range(alpha):
                if lens[t][i] == ln:
                    c[i] = vec; vec += 1
            vec <<= 1
        codes.append(c)
    in16 = [any(in_use[i * 16 + j] for j in range(16)) for i in range(16)]
    for i in range(16):
        bw.bits(1, 1 if in16[i] else 0)
    for i in range(16):
        if in16[i]:
            for j in range(16):
                bw.bits(1, 1 if in_use[i * 16 + j] else 0)
    bw.bits(3, ng)
    bw.bits(15, len(sels))
    for j in selmtf:
        for _ in range(j):
            bw.bits(1, 1)
        bw.bits(1, 0)
    for t in range(ng):
        cur = lens[t][0]
        bw.bits(5, cur)
        for i in range(alpha):
            while cur < lens[t][i]:
                bw.bits(2, 2); cur += 1
            while cur > lens[t][i]:
                bw.bits(2, 3); cur -= 1
            bw.bits(1, 0)
    gs = 0; sc = 0
    while gs < nmtf:
        ge = min(gs + 49, nmtf - 1)
        t = sels[sc]
        for i in range(gs, ge + 1):
            bw.bits(lens[t][mtfv[i]], codes[t][mtfv[i]])
        gs = ge + 1; sc += 1

def compress(data, level):
    bw = BW()
    for b in b"BZh":
        bw.bits(8, b)
    bw.bits(8, 0x30 + level)
    comb = 0
    for blk, bcrc in rle1_blocks(data, level):
        comb = (((comb << 1) | (comb >> 31)) & 0xffffffff) ^ bcrc
        compress_block(bw, blk, bcrc)
    for b in (0x17, 0x72, 0x45, 0x38, 0x50, 0x90):
        bw.bits(8, b)
    bw.bits(32, comb)
    bw.finish()
    return bytes(bw.buf)

# ---- decompressor ----
class Fail(Exception):
    pass  # args[0]: "eof", "data" or "magic"

class BR:
    def __init__(self, data):
        self.d = data; self.p = 0; self.acc = 0; self.n = 0
    def bits(self, k):
        while self.n < k:
            if self.p >= len(self.d):
                raise Fail("eof")
            self.acc = (self.acc << 8) | self.d[self.p]; self.p += 1; self.n += 8
        self.n -= k
        v = (self.acc >> self.n) & ((1 << k) - 1)
        self.acc &= (1 << self.n) - 1
        return v
    def drop_partial(self):
        self.acc = 0; self.n = 0

def decode_tables(lens, alpha):
    mn = min(lens); mx = max(lens)
    perm = []
    for i in range(mn, mx + 1):
        for j in range(alpha):
            if lens[j] == i:
                perm.append(j)
    base = [0] * 23
    for i in range(alpha):
        base[lens[i] + 1] += 1
    for i in range(1, 23):
        base[i] += base[i - 1]
    limit = [0] * 23
    vec = 0
    for i in range(mn, mx + 1):
        vec += base[i + 1] - base[i]
        limit[i] = vec - 1
        vec <<= 1
    for i in range(mn + 1, mx + 1):
        base[i] = ((limit[i - 1] + 1) << 1) - base[i]
    return (mn, limit, base, perm)

def decode_stream(br, verbose, sink):
    # one stream from br; returns False at a clean end of input before a
    # stream starts
    for want in b"BZh":
        if br.bits(8) != want:
            raise Fail("magic")
    level = br.bits(8) - 0x30
    if level < 1 or level > 9:
        raise Fail("magic")
    comb = 0; blockno = 0
    while True:
        magic = [br.bits(8) for _ in range(6)]
        if magic == [0x17, 0x72, 0x45, 0x38, 0x50, 0x90]:
            stored = br.bits(32)
            if stored != comb:
                raise Fail("data")
            br.drop_partial()
            return
        if magic != [0x31, 0x41, 0x59, 0x26, 0x53, 0x59]:
            raise Fail("data")
        blockno += 1
        if verbose >= 2:
            w(f"\n    [{blockno}: huff+mtf ")
        bcrc = br.bits(32)
        br.bits(1)
        orig = br.bits(24)
        if orig > 10 + 100000 * level:
            raise Fail("data")
        in16 = [br.bits(1) for _ in range(16)]
        in_use = [False] * 256
        for i in range(16):
            if in16[i]:
                for j in range(16):
                    if br.bits(1):
                        in_use[i * 16 + j] = True
        unseq = [i for i in range(256) if in_use[i]]
        ninuse = len(unseq)
        if ninuse == 0:
            raise Fail("data")
        alpha = ninuse + 2
        ng = br.bits(3)
        if ng < 2 or ng > 6:
            raise Fail("data")
        nsel = br.bits(15)
        if nsel < 1:
            raise Fail("data")
        selmtf = []
        for i in range(nsel):
            j = 0
            while br.bits(1):
                j += 1
                if j >= ng:
                    raise Fail("data")
            if i < 18002:
                selmtf.append(j)
        pos = list(range(ng))
        sels = []
        for j in selmtf:
            v = pos[j]; del pos[j]; pos.insert(0, v)
            sels.append(v)
        tables = []
        for t in range(ng):
            cur = br.bits(5)
            lens = []
            for i in range(alpha):
                while True:
                    if cur < 1 or cur > 20:
                        raise Fail("data")
                    if br.bits(1) == 0:
                        break
                    cur += 1 if br.bits(1) == 0 else -1
                lens.append(cur)
            tables.append(decode_tables(lens, alpha))
        eob = ninuse + 1
        nmax = 100000 * level
        state = [-1, 0]  # group number, symbols left in the group
        def sym():
            if state[1] == 0:
                state[0] += 1
                if state[0] >= len(sels):
                    raise Fail("data")
                state[1] = 50
            state[1] -= 1
            mn, limit, base, perm = tables[sels[state[0]]]
            zn = mn
            zv = br.bits(zn)
            while True:
                if zn > 20:
                    raise Fail("data")
                if zv <= limit[zn]:
                    break
                zn += 1
                zv = (zv << 1) | br.bits(1)
            k = zv - base[zn]
            if k < 0 or k >= 258 or k >= len(perm):
                raise Fail("data")
            return perm[k]
        yy = list(range(ninuse))
        tt = []
        s = sym()
        while s != eob:
            if s <= 1:
                es = -1; nn = 1
                while s <= 1:
                    if nn >= 2 * 1024 * 1024:
                        raise Fail("data")
                    es += nn if s == 0 else 2 * nn
                    nn *= 2
                    s = sym()
                es += 1
                uc = unseq[yy[0]]
                if len(tt) + es > nmax:
                    raise Fail("data")
                tt.extend([uc] * es)
            else:
                if len(tt) >= nmax:
                    raise Fail("data")
                v = yy[s - 1]; del yy[s - 1]; yy.insert(0, v)
                tt.append(unseq[v])
                s = sym()
        n = len(tt)
        if orig >= n:
            raise Fail("data")
        # inverse BWT
        cnt = [0] * 256
        for b in tt:
            cnt[b] += 1
        start = [0] * 256
        acc = 0
        for i in range(256):
            start[i] = acc; acc += cnt[i]
        nxt = [0] * n
        for i in range(n):
            b = tt[i]; nxt[start[b]] = i; start[b] += 1
        p = nxt[orig]
        rle = bytearray()
        for _ in range(n):
            rle.append(tt[p]); p = nxt[p]
        if verbose >= 2:
            w("rt+rld")
        # undo run-length stage one
        res = bytearray()
        i = 0; run = 0; last = -1
        while i < len(rle):
            b = rle[i]
            if run == 4:
                res.extend([last] * b); run = 0; last = -1
            else:
                res.append(b)
                run = run + 1 if b == last else 1
                last = b
            i += 1
        c = 0xffffffff
        for b in res:
            c = crc_update(c, b)
        c ^= 0xffffffff
        if c != bcrc:
            raise Fail("data")
        comb = (((comb << 1) | (comb >> 31)) & 0xffffffff) ^ c
        if verbose >= 2:
            w("]")
        sink.extend(res)

def decode_file(data, verbose, sink):
    # returns None, or the error, or "trailing" when trailing garbage
    br = BR(data)
    sno = 0
    while True:
        sno += 1
        try:
            decode_stream(br, verbose, sink)
        except Fail as e:
            if e.args[0] == "magic" and sno > 1:
                return "trailing"
            return e.args[0]
        if br.p >= len(data):
            return None

# ---- the bzip2 command ----
MSG = {"eof": "file ends unexpectedly", "data": "data integrity (CRC) error in data",
       "magic": "bad magic number (file not created by bzip2)"}

def bzip2(args, cwd, stdout):
    mode = "z"; keep = False; force = False; tostd = False; verbose = 0; level = 9
    files = []
    for a in args:
        if a.startswith("-") and len(a) > 1:
            for ch in a[1:]:
                if ch == "d": mode = "d"
                elif ch == "z": mode = "z"
                elif ch == "t": mode = "t"
                elif ch == "k": keep = True
                elif ch == "c": tostd = True
                elif ch == "f": force = True
                elif ch == "v": verbose += 1
                elif ch.isdigit(): level = int(ch)
        else:
            files.append(a)
    longest = max(len(f) for f in files)
    rc = 0
    test_fail = False
    def head(f):
        w(f"  {f}: " + " " * (longest - len(f)))
    for f in files:
        path = os.path.join(cwd, f)
        if not os.path.isfile(path):
            w(f"bzip2: Can't open input {f}: No such file or directory.\n")
            rc = max(rc, 1)
            continue
        data = open(path, "rb").read()
        if mode == "t":
            if verbose:
                head(f)
            r = decode_file(data, verbose, bytearray())
            if r is None or r == "trailing":
                if r == "trailing":
                    w("trailing garbage after EOF ignored\n")
                if verbose >= 2:
                    w("\n    ")
                if verbose:
                    w("ok\n")
            else:
                if verbose == 0:
                    w(f"bzip2: {f}: ")
                w(MSG[r] + "\n")
                test_fail = True
            continue
        if mode == "d":
            outn = f[:-4] if f.endswith(".bz2") else f + ".out"
            if not tostd and not force and os.path.exists(os.path.join(cwd, outn)):
                w(f"bzip2: Output file {outn} already exists.\n")
                rc = max(rc, 1)
                continue
            if verbose:
                head(f)
            sink = bytearray()
            r = decode_file(data, verbose, sink)
            if r not in (None, "trailing"):
                w(f"\nbzip2: {f}: {MSG[r]}\n")
                rc = max(rc, 2)
                continue
            if r == "trailing":
                w("trailing garbage after EOF ignored\n")
            if tostd:
                stdout.extend(sink)
            else:
                open(os.path.join(cwd, outn), "wb").write(sink)
                if not keep:
                    os.remove(path)
            if verbose:
                w("done\n")
            continue
        outn = f + ".bz2"
        if not tostd and not force and os.path.exists(os.path.join(cwd, outn)):
            w(f"bzip2: Output file {outn} already exists.\n")
            rc = max(rc, 1)
            continue
        if verbose:
            head(f)
        z = compress(data, level)
        if tostd:
            stdout.extend(z)
        else:
            open(os.path.join(cwd, outn), "wb").write(z)
            if not keep:
                os.remove(path)
        if verbose:
            if not data:
                w(" no data compressed.\n")
            else:
                i, o = len(data), len(z)
                w(f"{i / o:6.3f}:1, {8 * o / i:6.3f} bits/byte, {100 * (1 - o / i):5.2f}% saved, {i} in, {o} out.\n")
    if test_fail:
        w("\nYou can use the `bzip2recover' program to attempt to recover\ndata from undamaged sections of corrupted files.\n\n")
        rc = max(rc, 2)
    return rc

def sha256sum(args, cwd):
    rc = 0
    for f in args:
        p = os.path.join(cwd, f)
        if not os.path.isfile(p):
            w(f"sha256sum: {f}: No such file or directory\n")
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
        if parts[0] == "bzip2":
            rc = bzip2(parts[1:], work, stdout)
        else:
            rc = sha256sum(parts[1:], work)
        # stdout goes before stderr; sha256sum writes only stdout
        if stdout:
            out.insert(mark, stdout.decode("utf-8", "replace"))
        if rc:
            w(f"[exit status {rc}]\n")
        w("\n")
    shutil.rmtree(work)
    sys.stdout.write("".join(out))

main()
