#!/usr/bin/env python3
"""Writes data/: the files a small backup tool encrypts (data/plain/), and
data/jobs.tsv, the script oracle.py and mini_pyaes.kara both replay.

Each line of jobs.tsv is one step, its fields separated by tabs:

    job      <title>
    mode     <name> <ecb|cbc|cfb|ofb|ctr> <key> [<iv>|<counter>] [<segment size>]
    counter  <name> <initial value, decimal>
    value    <counter>
    aes      <key> <encrypt|decrypt> <block>
    encrypt  <mode> <data>            (and decrypt)
    feeder   <name> <mode> <encrypter|decrypter> [<padding>]
    feed     <feeder> [<data>]        (no data: the final call, feed())
    pipe     <encrypter> <decrypter> <data>   (feed, then feed(), through both)
    roundtrip <mode> <mode> <data>    (encrypt with one, decrypt with the other)
    stream   <encrypt|decrypt> <mode> <in> <out> <block size> [<padding>]
    cut      <in> <out> <length>      (copy the first bytes of a file)
    compare  <a> <b>
    size     <path>

Keys, IVs and data are hex, "-" is None, and paths are under data/. The
keys are made up for the run: SHA-256 of a label, or the published test
vectors of FIPS-197 and NIST SP 800-38A.

Run: python3 -s -P -B mk.py"""
import hashlib
import os

KEYS = {}


def key(label, n=16):
    k = hashlib.sha256(label.encode()).digest()[:n].hex()
    KEYS[label] = k
    return k


def hexof(text):
    return text.encode().hex()


def rand_bytes(n, seed):
    x = seed
    out = bytearray()
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        out.append((x >> 16) & 0xFF)
    return bytes(out)


os.makedirs("data/plain", exist_ok=True)

NOTES = """Backup notes, week 42
======================

- Rotate the offsite drive on Friday.
- The build server's disk is 81% full; prune old artifacts.
- Ask Priya about the printer queue on floor 3.
- Café order: two flat whites, one tea (no sugar).

Restore drill: pick three random files from last month's archive, restore
them to /tmp/restore-drill and compare checksums against the catalogue.
"""

SETTINGS = """[backup]
schedule = 02:30
retain_days = 30
compress = zstd
exclude = *.tmp, node_modules/, .cache/

[target]
host = archive.example.internal
path = /srv/backups/{hostname}
"""


def csv_report():
    rows = ["date,host,files,bytes,seconds,status"]
    hosts = ["web-1", "web-2", "db-1", "cache-1", "mail"]
    for d in range(1, 29):
        for i, h in enumerate(hosts):
            files = (d * 37 + i * 101) % 900 + 50
            size = files * ((d + i) % 7 + 3) * 1013
            secs = size // 250000 + i + 1
            status = "ok" if (d + i) % 11 else "retry"
            rows.append("2026-02-%02d,%s,%d,%d,%d,%s" % (d, h, files, size, secs, status))
    return "\n".join(rows) + "\n"


FILES = {
    "notes.txt": NOTES.encode(),
    "settings.ini": SETTINGS.encode(),
    "report.csv": csv_report().encode(),
    "thumbnail.bin": rand_bytes(3000, 7),
    "aligned.bin": rand_bytes(1024, 99),
    "empty.txt": b"",
    "one.txt": b"x",
    "block.bin": rand_bytes(16, 3),
}
for name, body in FILES.items():
    with open(os.path.join("data/plain", name), "wb") as f:
        f.write(body)

FIPS_PT = "00112233445566778899aabbccddeeff"
FIPS_KEYS = [
    "000102030405060708090a0b0c0d0e0f",
    "000102030405060708090a0b0c0d0e0f1011121314151617",
    "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
]
SP_KEYS = [
    "2b7e151628aed2a6abf7158809cf4f3c",
    "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b",
    "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4",
]
SP_IV = "000102030405060708090a0b0c0d0e0f"
SP_CTR = str(int("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff", 16))
SP_PT = ["6bc1bee22e409f96e93d7e117393172a", "ae2d8a571e03ac9c9eb76fac45af8e51",
         "30c81c46a35ce411e5fbc1191a0a52ef", "f69f2445df4f9b17ad2b417be66c3710"]

L = []


def step(*fields):
    L.append("\t".join(str(f) for f in fields))


step("job", "known answers (FIPS-197 and SP 800-38A)")
for k in FIPS_KEYS:
    step("aes", k, "encrypt", FIPS_PT)
for k, ct in zip(FIPS_KEYS, ["69c4e0d86a7b0430d8cdb78070b4c55a",
                              "dda97ca4864cdfe06eaf70a0ec0d7191",
                              "8ea2b7ca516745bfeafc49904b496089"]):
    step("aes", k, "decrypt", ct)
for n, k in enumerate(SP_KEYS):
    for kind, extra in [("ecb", []), ("cbc", [SP_IV]), ("cfb", [SP_IV, 16]),
                        ("cfb", [SP_IV, 1]), ("ofb", [SP_IV]), ("ctr", ["c%d" % n])]:
        if kind == "ctr":
            step("counter", "c%d" % n, SP_CTR)
        step("mode", "m", kind, k, *extra)
        for p in SP_PT:
            step("encrypt", "m", p)

step("job", "one message per mode")
msg = hexof("Invoice 2026-0117 paid in full. Thank you!")
for kind in ["ecb", "cbc", "cfb", "ofb", "ctr"]:
    k = key("message " + kind, {"ecb": 16, "cbc": 24, "cfb": 32, "ofb": 16, "ctr": 32}[kind])
    extra = []
    if kind in ("cbc", "cfb", "ofb"):
        extra = [hashlib.sha256(("iv " + kind).encode()).digest()[:16].hex()]
    if kind == "cfb":
        extra.append(8)
    if kind == "ctr":
        step("counter", "n", "1000")
        extra = ["n"]
    if kind in ("ecb", "cbc"):
        blocks = [msg[0:32], msg[32:64], (msg[64:] + "20" * 16)[:32]]
    elif kind == "cfb":
        blocks = [msg[0:16], msg[16:48], (msg[48:] + "20" * 8)[:16 * ((len(msg) - 48 + 15) // 16)]]
    else:
        blocks = [msg[0:10], msg[10:50], msg[50:]]
    step("mode", "send", kind, k, *extra)
    for b in blocks:
        step("encrypt", "send", b)

step("job", "a message round trip")
for kind in ["ecb", "cbc", "cfb", "ofb", "ctr"]:
    k = key("round trip " + kind)
    iv = hashlib.sha256(("round trip iv " + kind).encode()).digest()[:16].hex()
    extra = {"ecb": [], "cbc": [iv], "cfb": [iv, 4], "ofb": [iv], "ctr": ["rt"]}[kind]
    data = hexof("Meet at the north entrance at 09:15 sharp!!!!!!")[:96]
    if kind == "ctr":
        step("counter", "rt", "7")
    step("mode", "a", kind, k, *extra)
    if kind == "ctr":
        step("counter", "rt", "7")
    step("mode", "b", kind, k, *extra)
    step("roundtrip", "a", "b", data)

step("job", "reusing a mode")
k = key("reuse")
iv = "ab" * 16
step("mode", "cbc", "cbc", k, iv)
step("encrypt", "cbc", hexof("first block here"))
step("decrypt", "cbc", "00" * 16)
step("encrypt", "cbc", hexof("first block here"))
step("mode", "ofb", "ofb", k, iv)
step("encrypt", "ofb", hexof("abc"))
step("encrypt", "ofb", hexof("defghijklmnopqrstuvwxyz"))
step("decrypt", "ofb", hexof("abc"))
step("mode", "ofb", "ofb", k, iv)
step("encrypt", "ofb", hexof("abcdefghijklmnopqrstuvwxyz"))
step("encrypt", "ofb", "")
step("counter", "shared", "0")
step("mode", "c1", "ctr", k, "shared")
step("mode", "c2", "ctr", k, "shared")
step("encrypt", "c1", hexof("seventeen bytes!!"))
step("value", "shared")
step("encrypt", "c2", hexof("seventeen bytes!!"))
step("value", "shared")
step("encrypt", "c1", hexof("more"))
step("value", "shared")
step("mode", "c3", "ctr", k)
step("encrypt", "c3", "00" * 40)
step("mode", "ecb", "ecb", k)
step("encrypt", "ecb", "00" * 16)
step("encrypt", "ecb", "00" * 16)

step("job", "counters")
for v in ["0", "1", "255", "256", "65535", str(2 ** 64), str(2 ** 128 - 1), str(2 ** 128),
          str(2 ** 130 + 5), "-1", "-256", str(-(2 ** 127)), str(3 ** 90)]:
    step("counter", "c", v)
    step("value", "c")
    step("mode", "m", "ctr", key("counters"), "c")
    step("encrypt", "m", "00" * 33)
    step("value", "c")

step("job", "feeders")
k = key("feeders")
iv = "5a" * 16
sizes = [[], [5], [16], [17], [31], [32], [33], [1] * 40, [7, 9, 16, 1, 15], [100], [0, 0, 3]]
for kind in ["ecb", "cbc", "cfb", "ofb", "ctr"]:
    extra = {"ecb": [], "cbc": [iv], "cfb": [iv, 3], "ofb": [iv], "ctr": []}[kind]
    for sz in sizes:
        step("mode", "m", kind, k, *extra)
        step("feeder", "f", "m", "encrypter")
        base = 0
        for s in sz:
            step("feed", "f", rand_bytes(s, 1000 + base).hex())
            base += s
        step("feed", "f")
for kind in ["ecb", "cbc", "cfb", "ofb", "ctr"]:
    extra = {"ecb": [], "cbc": [iv], "cfb": [iv, 3], "ofb": [iv], "ctr": []}[kind]
    for total in [0, 1, 16, 21, 48]:
        step("mode", "e", kind, k, *extra)
        step("mode", "d", kind, k, *extra)
        step("feeder", "fe", "e", "encrypter")
        step("feeder", "fd", "d", "decrypter")
        step("pipe", "fe", "fd", rand_bytes(total, 77 + total).hex())

step("job", "padding")
for kind in ["ecb", "cbc", "cfb", "ofb", "ctr"]:
    extra = {"ecb": [], "cbc": [iv], "cfb": [iv, 2], "ofb": [iv], "ctr": []}[kind]
    for pad in ["none", "default", "pkcs7", ""]:
        for data in ["", "41" * 16, "41" * 20]:
            step("mode", "m", kind, k, *extra)
            step("feeder", "f", "m", "encrypter", pad)
            step("feed", "f", data)
            step("feed", "f")
            step("feed", "f")
            step("feed", "f", "42")
    for pad in ["none", "default", "bogus"]:
        step("mode", "m", kind, k, *extra)
        step("feeder", "f", "m", "decrypter", pad)
        step("feed", "f", "41" * 32)
        step("feed", "f")
# Decrypting with PKCS#7 checks only the last byte.
step("mode", "m", "ecb", k)
step("encrypt", "m", "41" * 15 + "00")
step("encrypt", "m", "41" * 15 + "05")
step("encrypt", "m", "41" * 15 + "10")
step("encrypt", "m", "41" * 15 + "11")
step("encrypt", "m", "41" * 15 + "ff")
for last in ["00", "05", "10", "11", "ff"]:
    step("mode", "e", "ecb", k)
    step("mode", "d", "ecb", k)
    step("feeder", "fe", "e", "encrypter", "none")
    step("feeder", "fd", "d", "decrypter")
    step("pipe", "fe", "fd", "41" * 15 + last)
step("mode", "d", "cbc", key("wrong key"), iv)
step("feeder", "f", "d", "decrypter")
step("feed", "f", rand_bytes(48, 5).hex())
step("feed", "f")

step("job", "bad arguments")
for n in [0, 1, 8, 15, 17, 20, 23, 25, 31, 33, 64]:
    step("mode", "m", "ecb", "00" * n)
step("mode", "m", "ecb", "-")
step("mode", "m", "ctr", "-")
step("mode", "m", "cbc", "00" * 15, "00" * 16)
step("mode", "m", "cbc", "00" * 15, "00" * 15)
step("mode", "m", "cbc", "00" * 16, "00" * 17)
step("mode", "m", "cfb", "00" * 16, "00" * 8, 1)
step("mode", "m", "cfb", "00" * 15, "00" * 8, 1)
step("mode", "m", "ofb", "00" * 16, "")
step("mode", "m", "ofb", "00" * 7, "00" * 16)
step("mode", "m", "ctr", "00" * 7)
step("aes", "00" * 16, "encrypt", "00" * 15)
step("aes", "00" * 16, "decrypt", "00" * 17)
step("aes", "00" * 12, "encrypt", "00" * 16)
step("mode", "m", "ecb", k)
step("encrypt", "m", "00" * 15)
step("encrypt", "m", "00" * 32)
step("decrypt", "m", "")
step("mode", "m", "cbc", k, iv)
step("encrypt", "m", "00" * 17)
step("decrypt", "m", "00" * 8)
step("encrypt", "m", "00" * 16)
step("mode", "m", "cfb", k, iv, 4)
step("encrypt", "m", "00" * 6)
step("decrypt", "m", "00" * 10)
step("encrypt", "m", "00" * 12)
step("mode", "m", "cfb", k, "-", 4)
step("encrypt", "m", "")
step("encrypt", "m", "00" * 8)
step("decrypt", "m", "00" * 4)
step("mode", "m", "cfb", k, "-", 16)
step("feeder", "f", "m", "encrypter")
step("feed", "f", "00" * 40)
step("feed", "f")
for seg in [0, 2, 5, 16, 20, -4, -3]:
    step("mode", "m", "cfb", k, iv, seg)
    step("encrypt", "m", "11" * 40)
    step("encrypt", "m", "22" * 20)
step("mode", "m", "cfb", k, iv, 20)
step("feeder", "f", "m", "encrypter")
step("feed", "f", "33" * 50)
step("feed", "f")
step("feeder", "f", "m", "encrypter")
step("feed", "f")
step("feed", "f")

step("job", "files")
plain = sorted(FILES)
modes = [("ecb", [], 16), ("cbc", ["iv"], 24), ("cfb", ["iv", 1], 32), ("cfb", ["iv", 16], 16),
         ("ofb", ["iv"], 32), ("ctr", ["ctr"], 16)]
for kind, extra, n in modes:
    k = key("files %s %d" % (kind, n), n)
    iv = hashlib.sha256(("files iv %s %d" % (kind, n)).encode()).digest()[:16].hex()
    tag = kind + str(extra[1] if len(extra) > 1 else "")
    for name in plain:
        args = [iv if e == "iv" else e for e in extra]
        for direction in ["encrypt", "decrypt"]:
            if kind == "ctr":
                step("counter", "ctr", "4242")
            step("mode", "m", kind, k, *args)
            src = "plain/%s" % name if direction == "encrypt" else "out/%s.%s" % (name, tag)
            dst = "out/%s.%s" % (name, tag) if direction == "encrypt" else "out/%s.%s.txt" % (name, tag)
            block = 8192 if name != "report.csv" else 1000
            step("stream", direction, "m", src, dst, block)
        step("compare", "plain/%s" % name, "out/%s.%s.txt" % (name, tag))

step("job", "stream options")
k = key("stream options")
iv = "c3" * 16
for block in [8192, 4096, 100, 17, 16, 15, 1, 0, -1]:
    step("mode", "m", "cbc", k, iv)
    step("stream", "encrypt", "m", "plain/notes.txt", "out/notes.cbc.%d" % block, block)
    step("mode", "m", "cbc", k, iv)
    step("stream", "decrypt", "m", "out/notes.cbc.%d" % block, "out/notes.cbc.%d.txt" % block, block)
    step("compare", "plain/notes.txt", "out/notes.cbc.%d.txt" % block)
for pad in ["none", "default", "pkcs7"]:
    for name in ["aligned.bin", "notes.txt", "empty.txt"]:
        step("mode", "m", "cbc", k, iv)
        step("stream", "encrypt", "m", "plain/" + name, "out/%s.%s" % (name, pad), 256, pad)
        step("size", "out/%s.%s" % (name, pad))
        step("mode", "m", "cbc", k, iv)
        step("stream", "decrypt", "m", "out/%s.%s" % (name, pad), "out/%s.%s.txt" % (name, pad), 256, pad)
        step("size", "out/%s.%s.txt" % (name, pad))
for pad in ["none", "default", "pkcs7"]:
    step("mode", "m", "ofb", k, iv)
    step("stream", "encrypt", "m", "plain/notes.txt", "out/notes.ofb." + pad, 64, pad)
    step("size", "out/notes.ofb." + pad)
    step("mode", "m", "cfb", k, iv, 3)
    step("stream", "encrypt", "m", "plain/notes.txt", "out/notes.cfb3." + pad, 64, pad)
    step("size", "out/notes.cfb3." + pad)

step("job", "damaged files")
k = key("damaged")
iv = "7e" * 16
step("mode", "m", "cbc", k, iv)
step("stream", "encrypt", "m", "plain/settings.ini", "out/settings.cbc", 8192)
for cut in [0, 15, 16, 100, 255, 256, 271]:
    step("cut", "out/settings.cbc", "out/settings.cbc.cut%d" % cut, cut)
    step("mode", "m", "cbc", k, iv)
    step("stream", "decrypt", "m", "out/settings.cbc.cut%d" % cut, "out/settings.cut%d.txt" % cut, 8192)
    step("size", "out/settings.cut%d.txt" % cut)
for wrong in ["damaged 2", "damaged 3", "damaged 4", "damaged 5"]:
    step("mode", "m", "cbc", key(wrong), iv)
    step("stream", "decrypt", "m", "out/settings.cbc", "out/settings.wrong.txt", 8192)
    step("size", "out/settings.wrong.txt")
step("mode", "m", "cbc", k, "00" * 16)
step("stream", "decrypt", "m", "out/settings.cbc", "out/settings.wrongiv.txt", 8192)
step("size", "out/settings.wrongiv.txt")
step("compare", "plain/settings.ini", "out/settings.wrongiv.txt")
step("mode", "m", "ctr", k)
step("stream", "encrypt", "m", "plain/thumbnail.bin", "out/thumbnail.ctr", 512)
step("cut", "out/thumbnail.ctr", "out/thumbnail.ctr.cut", 1234)
step("mode", "m", "ctr", k)
step("stream", "decrypt", "m", "out/thumbnail.ctr.cut", "out/thumbnail.cut.bin", 512)
step("compare", "plain/thumbnail.bin", "out/thumbnail.cut.bin")
step("mode", "m", "ctr", k)
step("stream", "decrypt", "m", "plain/missing.bin", "out/missing.bin", 512)
step("compare", "plain/notes.txt", "plain/missing.bin")

with open("data/jobs.tsv", "w") as f:
    f.write("\n".join(L) + "\n")
