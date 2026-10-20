# Writes data/: CRC definitions to build (crcmod's catalogue, custom ones
# and broken ones), byte streams to feed them in pieces, the C code jobs
# of crcmod's own examples, the files of seven programs that check real
# formats' CRCs (PNG chunks, gzip trailers, Modbus RTU frames, XMODEM
# blocks, OpenPGP ASCII armor, 1-Wire ROM codes and Redis-style dumps
# with a CRC-64 footer), and data/jobs.tsv, the jobs mini_crcmod.kara
# and oracle.py run.
#
# Bytes in text files are written with \r, \n, \t, \\ and \xNN escapes.
import base64
import gzip
import os
import random
import shutil
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, HERE)

import crcmod  # noqa: E402
import crcmod.predefined  # noqa: E402


def write(rel, data):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, str):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(data)
    else:
        with open(path, "wb") as f:
            f.write(data)


def esc(b):
    out = []
    for x in b:
        c = chr(x)
        if c == "\\":
            out.append("\\\\")
        elif c == "\r":
            out.append("\\r")
        elif c == "\n":
            out.append("\\n")
        elif c == "\t":
            out.append("\\t")
        elif x < 0x20 or x >= 0x7f or c == "|":
            out.append("\\x%02x" % x)
        else:
            out.append(c)
    return "".join(out)


def poly_bits(bits):
    p = 0
    for n in bits:
        p |= 1 << n
    return p


G64 = poly_bits([64, 62, 57, 55, 54, 53, 52, 47, 46, 45, 40, 39, 38, 37, 35, 33, 32, 31, 29, 27, 24, 23, 22, 21,
                 19, 17, 13, 12, 10, 9, 7, 4, 1, 0])

# poly init rev xor_out: crcmod's examples, real-world CRCs not in its
# table, and parameters it refuses.
CUSTOM = [
    ("0x185", "~0", "0", "0"), ("0x185", "~0", "1", "0"), ("0x11021", "~0", "0", "0"), ("0x11021", "~0", "1", "0"),
    ("0x15D6DCB", "~0", "0", "0"), ("0x15D6DCB", "~0", "1", "0"), ("0x104C11DB7", "~0", "0", "0"),
    ("0x104C11DB7", "~0", "1", "0"), ("0x%X" % G64, "~0", "0", "0"), ("0x%X" % G64, "~0", "1", "0"),
    ("0x11021", "0", "1", "~0"), ("0x15D6DCB", "0", "1", "~0"), ("0x104C11DB7", "0", "1", "~0"),
    ("0x%X" % G64, "0", "1", "~0"),
    ("0x142F0E1EBA9EA3693", "~0", "1", "~0"),      # CRC-64/XZ
    ("0x11EDC6F41", "~0", "1", "~0"),              # CRC-32C again, as Castagnoli wrote it
    ("0x1814141AB", "0", "0", "0"),                # CRC-32/AIXM
    ("0x18005", "0x1234", "0", "-2"),
    ("0x107", "-1", "0", "0x1FF"),
    ("0x8005", "0", "1", "0"), ("0x1", "0", "1", "0"), ("0x200000000000000000", "0", "1", "0"),
    ("0x2000000", "0", "0", "0"), ("0", "0", "1", "0"),
]

STREAMS = [
    ("crc-32", b"The quick brown fox jumps over the lazy dog", "1,3,9,0,100"),
    ("crc-32c", b"\x00" * 32, "32"), ("crc-32c", b"\xff" * 32, "7,25"), ("crc-32c", bytes(range(32)), "5,5,5,17"),
    ("crc-32c", bytes(range(31, -1, -1)), "1"),
    ("crc-16-usb", b"", ""), ("modbus", b"\x01\x03\x00\x00\x00\x0a", "2,2,2"),
    ("xmodem", b"123456789", "4,5"), ("crc-64-jones", b"123456789", "9"),
    ("crc-64-we", b"Kara compiles this", "3,3,3,3"), ("crc-24", b"\x14\xfb\x9c\x03\xd9\x7e", "6"),
    ("posix", b"hello world\n", "12"), ("crc-8-maxim", bytes.fromhex("02 1c b8 01 00 00 00"), "1,1,1,1,1,1,1"),
    ("Crc16Mcrf4xx", b"RFID tag 0001", "13"), ("CRC-16 DNP", b"\x05\x64\x05\xc0\x01\x00\x00\x04", "8"),
    ("crc-99", b"x", "1"), ("crc32", b"spellings", "9"), ("CRC-32", b"spellings", "9"), ("Crc32", b"spellings", "9"),
    ("crc_32", b"spellings", "9"),
]

CODE = [
    ("custom", "0x185", "~0", "0", "0", "crc8", "-", "-"),
    ("custom", "0x185", "~0", "1", "0", "crc8r", "-", "-"),
    ("custom", "0x11021", "~0", "0", "0", "crc16", "-", "-"),
    ("custom", "0x15D6DCB", "~0", "1", "0", "crc24r", "-", "-"),
    ("custom", "0x15D6DCB", "0", "1", "~0", "crc24x", "-", "-"),
    ("custom", "0x104C11DB7", "0", "1", "~0", "crc32x", "-", "-"),
    ("custom", "0x%X" % G64, "~0", "0", "0", "crc64", "-", "-"),
    ("named", "crc-16-t10-dif", "t10dif_crc", "uint8_t", "uint16_t"),
    ("named", "crc-32c", "crc32c_sw", "-", "-"),
    ("named", "crc-24-flexray-a", "flexray_a", "-", "-"),
    ("named", "crc-64-jones", "redis_crc64", "unsigned char", "-"),
]


# ------------------------------------------------------------ formats

def png_chunk(kind, body):
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))


def png(r, w, h, broken=None):
    raw = b"".join(b"\x00" + bytes(r.randrange(256) for _ in range(w * 3)) for _ in range(h))
    chunks = [png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)),
              png_chunk(b"tEXt", b"Software\x00mk.py"),
              png_chunk(b"IDAT", zlib.compress(raw, 9)),
              png_chunk(b"IEND", b"")]
    if broken == "crc":
        c = bytearray(chunks[2])
        c[-1] ^= 0x40
        chunks[2] = bytes(c)
    if broken == "data":
        c = bytearray(chunks[1])
        c[10] ^= 0x01
        chunks[1] = bytes(c)
    if broken == "truncated":
        chunks = chunks[:2] + [chunks[2][:20]]
    return b"\x89PNG\r\n\x1a\n" + b"".join(chunks)


def modbus_frame(addr, func, payload):
    body = bytes([addr, func]) + payload
    crc = crcmod.predefined.mkCrcFun("modbus")(body)
    return body + struct.pack("<H", crc)


def xmodem_blocks(r, data, bad=()):
    out = b""
    n = 1
    for i in range(0, len(data), 128):
        block = data[i:i + 128].ljust(128, b"\x1a")
        crc = crcmod.predefined.mkCrcFun("xmodem")(block)
        if n in bad:
            block = block[:5] + bytes([block[5] ^ 0x20]) + block[6:]
        out += b"\x01" + bytes([n & 255, 255 - (n & 255)]) + block + struct.pack(">H", crc)
        n += 1
    return out + b"\x04"


def armor(kind, data, bad=False):
    crc = crcmod.predefined.mkCrcFun("crc-24")(data)
    if bad:
        crc ^= 1
    b64 = base64.b64encode(data).decode()
    lines = ["-----BEGIN PGP %s-----" % kind, "Version: mk.py", ""]
    lines += [b64[i:i + 64] for i in range(0, len(b64), 64)]
    lines.append("=" + base64.b64encode(struct.pack(">I", crc)[1:]).decode())
    lines.append("-----END PGP %s-----" % kind)
    return "\n".join(lines) + "\n"


def rom_code(r, family, bad=False):
    serial = bytes(r.randrange(256) for _ in range(6))
    body = bytes([family]) + serial
    crc = crcmod.predefined.mkCrcFun("crc-8-maxim")(body)
    if bad:
        crc ^= 0x10
    return (body + bytes([crc])).hex().upper()


def dump(r, n, bad=False):
    out = b"REDIS0011"
    for i in range(n):
        k = ("user:%d" % r.randrange(10000)).encode()
        v = ("%d" % r.randrange(10 ** 9)).encode()
        out += b"\x00" + bytes([len(k)]) + k + bytes([len(v)]) + v
    out += b"\xff"
    crc = crcmod.predefined.mkCrcFun("crc-64-jones")(out)
    if bad:
        out = out[:12] + b"X" + out[13:]
    return out + struct.pack("<Q", crc)


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    jobs = [["catalog"]]
    write("custom.txt", "".join(" ".join(c) + "\n" for c in CUSTOM))
    jobs.append(["custom", "custom.txt"])
    write("streams.txt", "".join("%s|%s|%s\n" % (n, esc(d), c) for n, d, c in STREAMS))
    jobs.append(["streams", "streams.txt"])
    for c in CODE:
        jobs.append(["code"] + list(c[1:]) if c[0] == "named" else ["code_custom"] + list(c[1:]))
    r = random.Random(152)
    pngs = []
    for k, broken in enumerate([None, None, "crc", "data", "truncated"]):
        name = "png/%d.png" % k
        write(name, png(r, r.randint(1, 6), r.randint(1, 4), broken))
        pngs.append(name)
    jobs.append(["png"] + pngs)
    payload = "".join("%d,%s\n" % (i, r.choice(["ok", "warn", "fail"])) for i in range(30)).encode()
    write("gz/log.csv.gz", gzip.compress(payload, compresslevel=0, mtime=1700000000))
    bad = bytearray(gzip.compress(payload[:100], compresslevel=0, mtime=1700000000))
    bad[-6] ^= 0xFF
    write("gz/bad_crc.gz", bytes(bad))
    write("gz/empty.gz", gzip.compress(b"", compresslevel=0, mtime=0))
    jobs.append(["gzip", "gz/log.csv.gz", "gz/bad_crc.gz", "gz/empty.gz"])
    frames = [modbus_frame(1, 3, b"\x00\x00\x00\x0a"), modbus_frame(1, 3, b"\x14" + bytes(range(20))),
              modbus_frame(17, 6, b"\x00\x01\x00\x03"), modbus_frame(2, 0x83, b"\x02")]
    broken = bytearray(modbus_frame(5, 16, b"\x00\x10\x00\x02\x04\x00\x0a\x01\x02"))
    broken[3] ^= 1
    frames.append(bytes(broken))
    frames.append(b"\x01\x03")
    write("modbus.txt", "".join(f.hex(" ") + "\n" for f in frames))
    jobs.append(["modbus", "modbus.txt"])
    firmware = bytes(r.randrange(256) for _ in range(300))
    write("xmodem/fw.bin.xmodem", xmodem_blocks(r, firmware))
    write("xmodem/noisy.xmodem", xmodem_blocks(r, firmware, bad=(2,)))
    jobs.append(["xmodem", "xmodem/fw.bin.xmodem", "xmodem/noisy.xmodem"])
    for k, (kind, n, bad) in enumerate([("PUBLIC KEY BLOCK", 140, False), ("MESSAGE", 61, False),
                                        ("SIGNATURE", 119, True), ("MESSAGE", 1, False)]):
        write("armor/%d.asc" % k, armor(kind, bytes(r.randrange(256) for _ in range(n)), bad))
    jobs.append(["armor"] + ["armor/%d.asc" % k for k in range(4)])
    roms = [rom_code(r, 0x28), rom_code(r, 0x10), rom_code(r, 0x01), rom_code(r, 0x28, bad=True), "2800000000000000",
            "0000000000000000"]
    write("onewire.txt", "\n".join(roms) + "\n")
    jobs.append(["onewire", "onewire.txt"])
    write("dumps/a.rdb", dump(r, 5))
    write("dumps/b.rdb", dump(r, 12, bad=True))
    write("dumps/c.rdb", dump(r, 0))
    jobs.append(["rdb", "dumps/a.rdb", "dumps/b.rdb", "dumps/c.rdb"])
    write("jobs.tsv", "".join("\t".join(j) + "\n" for j in jobs))


main()
