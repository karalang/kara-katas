# Python mirror of mini_hashsum: runs data/jobs.txt with a port of GNU
# coreutils 9.4's checksum tools (md5sum, sha1sum, sha224sum, sha256sum,
# sha384sum, sha512sum, b2sum, cksum and sum), hashing and checking.
import base64, hashlib, os, shutil, sys

out = []
err = []

ALGOS = ["bsd", "sysv", "crc", "md5", "sha1", "sha224", "sha256", "sha384", "sha512", "blake2b", "sm3"]
TAG = {"md5": "MD5", "sha1": "SHA1", "sha224": "SHA224", "sha256": "SHA256", "sha384": "SHA384",
       "sha512": "SHA512", "blake2b": "BLAKE2b", "sm3": "SM3"}
BITS = {"md5": 128, "sha1": 160, "sha224": 224, "sha256": 256, "sha384": 384, "sha512": 512, "blake2b": 512, "sm3": 256}
PROG_ALGO = {"md5sum": "md5", "sha1sum": "sha1", "sha224sum": "sha224", "sha256sum": "sha256",
             "sha384sum": "sha384", "sha512sum": "sha512", "b2sum": "blake2b"}

def digest(algo, bits, data):
    if algo == "blake2b":
        return hashlib.blake2b(data, digest_size=bits // 8).digest()
    return hashlib.new(algo, data).digest()

def crc_cksum(data):
    c = 0
    def feed(b):
        nonlocal c
        c ^= b << 24
        for _ in range(8):
            c = ((c << 1) ^ 0x04C11DB7) & 0xFFFFFFFF if c & 0x80000000 else (c << 1) & 0xFFFFFFFF
    for b in data:
        feed(b)
    n = len(data)
    while n:
        feed(n & 0xFF); n >>= 8
    return c ^ 0xFFFFFFFF

def bsd_sum(data):
    s = 0
    for b in data:
        s = (s >> 1) + ((s & 1) << 15)
        s = (s + b) & 0xFFFF
    return s

def sysv_sum(data):
    s = sum(data)
    r = (s & 0xFFFF) + ((s & 0xFFFFFFFF) >> 16)
    return (r & 0xFFFF) + (r >> 16)

def needs_escape(name):
    return "\\" in name or "\n" in name or "\r" in name

def escape(name):
    return name.replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r")

def read_file(prog, cwd, f):
    p = os.path.join(cwd, f)
    if os.path.isdir(p):
        err.append(f"{prog}: {f}: Is a directory\n")
        return None
    if not os.path.isfile(p):
        err.append(f"{prog}: {f}: No such file or directory\n")
        return None
    return open(p, "rb").read()

def tag_name(algo, bits):
    if algo == "blake2b" and bits != 512:
        return f"BLAKE2b-{bits}"
    return TAG[algo]

def is_hex(s):
    return len(s) > 0 and all(c in "0123456789abcdefABCDEF" for c in s)

def b64_ok(s, nbytes):
    if len(s) != (nbytes + 2) // 3 * 4:
        return None
    try:
        d = base64.b64decode(s, validate=True)
    except Exception:
        return None
    if len(d) != nbytes or base64.b64encode(d).decode() != s:
        return None
    return d

def unescape(name):
    o = []; i = 0
    while i < len(name):
        c = name[i]
        if c == "\\":
            if i + 1 >= len(name):
                return None
            n = name[i + 1]
            if n == "\\":
                o.append("\\")
            elif n == "n":
                o.append("\n")
            elif n == "r":
                o.append("\r")
            else:
                return None
            i += 2
        else:
            o.append(c); i += 1
    return "".join(o)

def parse_line(line, algo, bits):
    # returns (algo, bits, expected digest bytes, file name, escaped) or None
    i = 0
    while i < len(line) and line[i] in " \t":
        i += 1
    s = line[i:]
    escaped = False
    if s.startswith("\\"):
        escaped = True
        s = s[1:]
    # the tagged (BSD) form: ALGO (name) = digest
    for a in ([algo] if algo else [x for x in ALGOS if x in TAG]):
        t = TAG[a]
        if s.startswith(t):
            rest = s[len(t):]
            b = BITS[a]
            if a == "blake2b" and rest.startswith("-"):
                j = 1
                while j < len(rest) and rest[j].isdigit():
                    j += 1
                if j == 1:
                    continue
                b = int(rest[1:j])
                if b % 8 or b == 0 or b > 512:
                    return None
                rest = rest[j:]
            if rest.startswith(" "):
                rest = rest[1:]
            if not rest.startswith("("):
                continue
            rest = rest[1:]
            k = rest.rfind(") = ")
            if k < 0:
                return None
            name = rest[:k]; dg = rest[k + 4:]
            exp = decode_digest(dg, b)
            if exp is None:
                return None
            if escaped:
                name = unescape(name)
                if name is None:
                    return None
            return (a, b, exp, name)
    if not algo:
        return None
    # the untagged form: digest, a space, a space or '*', the name
    j = 0
    while j < len(s) and s[j] not in " \t":
        j += 1
    dg = s[:j]
    exp = decode_digest(dg, bits)
    if exp is None:
        return None
    rest = s[j:]
    if len(rest) < 2 or rest[0] != " " or rest[1] not in " *":
        return None
    name = rest[2:]
    if name == "":
        return None
    if escaped:
        name = unescape(name)
        if name is None:
            return None
    return (algo, bits, exp, name)

def decode_digest(dg, bits):
    n = bits // 8
    if len(dg) == 2 * n and is_hex(dg):
        return bytes.fromhex(dg)
    return b64_ok(dg, n)

def plural(n, one, many):
    return one if n == 1 else many

def check(prog, algo, bits, files, opts, cwd, outb):
    rc = 0
    for sf in files:
        p = os.path.join(cwd, sf)
        if not os.path.isfile(p):
            err.append(f"{prog}: {sf}: No such file or directory\n")
            rc = 1
            continue
        text = open(p, "rb").read().decode("utf-8", "replace")
        lines = text.split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        bad_format = 0; bad_read = 0; mismatch = 0; good = 0; verified = 0
        for ln, line in enumerate(lines, 1):
            if line == "" or line.startswith("#"):
                continue
            r = parse_line(line, algo, bits)
            if r is None:
                bad_format += 1
                if opts["warn"]:
                    what = f"{TAG[algo]} " if algo else ""
                    err.append(f"{prog}: {sf}: {ln}: improperly formatted {what}checksum line\n")
                continue
            a, b, exp, name = r
            good += 1
            shown = ("\\" + escape(name)) if needs_escape(name) else name
            fp = os.path.join(cwd, name)
            if not os.path.isfile(fp):
                if opts["ignore_missing"]:
                    continue
                err.append(f"{prog}: {name}: No such file or directory\n")
                if not opts["status"]:
                    outb.append(f"{shown}: FAILED open or read\n")
                bad_read += 1
                continue
            verified += 1
            got = digest(a, b, open(fp, "rb").read())
            if got != exp:
                mismatch += 1
                if not opts["status"]:
                    outb.append(f"{shown}: FAILED\n")
            elif not opts["status"] and not opts["quiet"]:
                outb.append(f"{shown}: OK\n")
        if good == 0:
            err.append(f"{prog}: {sf}: no properly formatted checksum lines found\n")
            rc = 1
            continue
        if not opts["status"]:
            if bad_format:
                err.append(f"{prog}: WARNING: {bad_format} {plural(bad_format, 'line is', 'lines are')} improperly formatted\n")
            if bad_read:
                err.append(f"{prog}: WARNING: {bad_read} listed {plural(bad_read, 'file', 'files')} could not be read\n")
            if mismatch:
                err.append(f"{prog}: WARNING: {mismatch} computed {plural(mismatch, 'checksum', 'checksums')} did NOT match\n")
        if opts["ignore_missing"] and verified == 0:
            err.append(f"{prog}: {sf}: no file was verified\n")
            rc = 1
        if bad_read or mismatch or (opts["strict"] and bad_format):
            rc = 1
    return rc

def run_tool(prog, args, cwd, outb):
    algo = PROG_ALGO.get(prog)
    bits = BITS.get(algo, 0)
    opts = {"check": False, "tag": prog == "cksum", "base64": False, "quiet": False, "status": False,
            "warn": False, "strict": False, "ignore_missing": False}
    length = None
    files = []
    i = 0
    if prog == "sum":
        algo = "bsd"
    if prog == "cksum":
        algo = "crc"
    while i < len(args):
        a = args[i]
        if a in ("-c", "--check"):
            opts["check"] = True
        elif a == "--tag":
            opts["tag"] = True
        elif a == "--untagged":
            opts["tag"] = False
        elif a == "--base64":
            opts["base64"] = True
        elif a == "--quiet":
            opts["quiet"] = True
        elif a == "--status":
            opts["status"] = True
        elif a in ("-w", "--warn"):
            opts["warn"] = True
        elif a == "--strict":
            opts["strict"] = True
        elif a == "--ignore-missing":
            opts["ignore_missing"] = True
        elif a == "-s" and prog == "sum":
            algo = "sysv"
        elif a == "-r" and prog == "sum":
            algo = "bsd"
        elif a == "-l":
            i += 1; length = args[i]
        elif a == "-a":
            i += 1
            if args[i] not in ALGOS:
                err.append(f"cksum: invalid argument ‘{args[i]}’ for ‘--algorithm’\nValid arguments are:\n")
                for x in ALGOS:
                    err.append(f"  - ‘{x}’\n")
                err.append("Try 'cksum --help' for more information.\n")
                return 1
            algo = args[i]
            bits = BITS.get(algo, 0)
        else:
            files.append(a)
        i += 1
    if length is not None:
        n = int(length)
        if n % 8 or n == 0 or n > 512:
            err.append(f"{prog}: invalid length: ‘{length}’\n")
            if n % 8:
                err.append(f"{prog}: length is not a multiple of 8\n")
            else:
                err.append(f"{prog}: maximum digest length for ‘BLAKE2b’ is 512 bits\n")
            return 1
        bits = n
    if opts["check"]:
        # cksum -c reads the algorithm from each tagged line
        return check(prog, None if prog == "cksum" else algo, bits, files, opts, cwd, outb)
    rc = 0
    for f in files:
        data = read_file(prog, cwd, f)
        if data is None:
            rc = 1
            continue
        if algo == "crc":
            outb.append(f"{crc_cksum(data)} {len(data)} {f}\n")
        elif algo == "bsd":
            outb.append(f"{bsd_sum(data):05} {(len(data) + 1023) // 1024:5} {f}\n")
        elif algo == "sysv":
            outb.append(f"{sysv_sum(data)} {(len(data) + 511) // 512} {f}\n")
        else:
            d = digest(algo, bits, data)
            ds = base64.b64encode(d).decode() if opts["base64"] else d.hex()
            esc = needs_escape(f)
            name = escape(f) if esc else f
            pre = "\\" if esc else ""
            if opts["tag"]:
                outb.append(f"{pre}{tag_name(algo, bits)} ({name}) = {ds}\n")
            else:
                outb.append(f"{pre}{ds}  {name}\n")
    return rc

def main():
    work = os.path.abspath("oraclework")
    if os.path.isdir(work):
        shutil.rmtree(work)
    shutil.copytree("data", work)
    for line in open("data/jobs.txt").read().splitlines():
        if not line or line.startswith("#"):
            continue
        out.append(f"$ {line}\n")
        parts = line.split(" ")
        outb = []
        del err[:]
        rc = run_tool(parts[0], parts[1:], work, outb)
        out.extend(outb)
        out.extend(err)
        if rc:
            out.append(f"[exit status {rc}]\n")
        out.append("\n")
    shutil.rmtree(work)
    sys.stdout.write("".join(out))

main()
