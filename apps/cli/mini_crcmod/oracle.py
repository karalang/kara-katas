# Runs data/jobs.tsv through crcmod 1.7 (the crcmod/ package next to this
# file, unchanged, which falls back to its pure-Python _crcfunpy) and
# prints what it did. mini_crcmod.kara must print the same bytes.
import base64
import io
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import crcmod  # noqa: E402
import crcmod.predefined  # noqa: E402
from crcmod.predefined import _crc_definitions  # noqa: E402

OUT = []


def emit(s):
    OUT.append(s)


def path_of(rel):
    return os.path.join(HERE, "data", rel)


def read(rel):
    with open(path_of(rel), encoding="utf-8") as f:
        return f.read()


def read_bytes(rel):
    with open(path_of(rel), "rb") as f:
        return f.read()


def unesc(s):
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            n = s[i + 1]
            if n == "x":
                out.append(int(s[i + 2:i + 4], 16))
                i += 4
                continue
            out.append({"r": 13, "n": 10, "t": 9, "\\": 92}[n])
            i += 2
            continue
        out += c.encode()
        i += 1
    return bytes(out)


def num(s):
    if s == "~0":
        return ~0
    return int(s, 0)


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


# ------------------------------------------------------------ catalog

def catalog_job():
    for d in _crc_definitions:
        crc = crcmod.predefined.Crc(d["name"])
        crc.update(b"123456789")
        ok = crc.crcValue == d["check"]
        emit("%s (%s): poly=0x%X reverse=%s init=0x%X xor_out=0x%X check=0x%X %s digest=%s" % (
            d["name"], d["identifier"], d["poly"], d["reverse"], d["init"], d["xor_out"], crc.crcValue,
            "ok" if ok else "WRONG", crc.digest().hex()))


def custom_job(rel):
    for line in read(rel).splitlines():
        poly, init, rev, xor = line.split(" ")
        emit("> " + line)
        try:
            crc = crcmod.Crc(num(poly), initCrc=num(init), rev=rev == "1", xorOut=num(xor))
        except Exception as e:
            emit("  " + err(e))
            continue
        fun = crcmod.mkCrcFun(num(poly), initCrc=num(init), rev=rev == "1", xorOut=num(xor))
        for s in str(crc).split("\n"):
            emit("  " + s)
        emit("  digest_size=%d table[1]=0x%X table[255]=0x%X" % (crc.digest_size, crc.table[1], crc.table[255]))
        crc.update(b"123456789")
        emit("  check=0x%X fun=0x%X hexdigest=%s" % (crc.crcValue, fun(b"123456789"), crc.hexdigest()))
        emit("  continued=0x%X empty=0x%X" % (fun(b"56789", fun(b"1234")), fun(b"")))


def streams_job(rel):
    for line in read(rel).splitlines():
        name, data, cuts = line.split("|")
        data = unesc(data)
        emit("> %s %d bytes, pieces %s" % (name, len(data), cuts or "-"))
        try:
            crc = crcmod.predefined.PredefinedCrc(name)
        except Exception as e:
            emit("  " + err(e))
            continue
        one = crcmod.predefined.mkPredefinedCrcFun(name)(data)
        pos = 0
        snaps = []
        for c in (cuts.split(",") if cuts else []):
            crc.update(data[pos:pos + int(c)])
            pos += int(c)
            snaps.append(crc.copy())
        crc.update(data[pos:])
        fresh = crc.new(data)
        emit("  whole=0x%X pieces=0x%X new=0x%X %s" % (one, crc.crcValue, fresh.crcValue,
                                                         "same" if one == crc.crcValue == fresh.crcValue else "DIFFER"))
        emit("  snapshots: " + " ".join(s.hexdigest() for s in snaps))
        emit("  digest=%s" % crc.digest().hex())


def code_job(crc, fn, data_type, crc_type):
    out = io.StringIO()
    crc.generateCode(fn, out, None if data_type == "-" else data_type, None if crc_type == "-" else crc_type)
    for line in out.getvalue().split("\n"):
        emit("| " + line)


# ------------------------------------------------------------ formats

def png_job(names):
    crc32 = crcmod.predefined.mkPredefinedCrcFun("crc-32")
    for name in names:
        data = read_bytes(name)
        emit("%s: %d bytes" % (name, len(data)))
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            emit("  not a PNG")
            continue
        pos = 8
        good = True
        while pos < len(data):
            if pos + 12 > len(data):
                emit("  truncated at %d" % pos)
                good = False
                break
            n = struct.unpack(">I", data[pos:pos + 4])[0]
            kind = data[pos + 4:pos + 8]
            if pos + 12 + n > len(data):
                emit("  %s: %d bytes, truncated" % (kind.decode("latin-1"), n))
                good = False
                break
            stored = struct.unpack(">I", data[pos + 8 + n:pos + 12 + n])[0]
            got = crc32(data[pos + 4:pos + 8 + n])
            emit("  %s: %d bytes, crc %08x %s" % (kind.decode("latin-1"), n, stored,
                                                  "ok" if got == stored else "BAD (computed %08x)" % got))
            good = good and got == stored
            pos += 12 + n
        emit("  %s" % ("ok" if good else "CORRUPT"))


def gzip_job(names):
    crc32 = crcmod.predefined.mkPredefinedCrcFun("crc-32")
    for name in names:
        data = read_bytes(name)
        flags = data[3]
        mtime = struct.unpack("<I", data[4:8])[0]
        pos = 10
        if flags & 8:
            pos = data.index(b"\x00", pos) + 1
        body = b""
        while True:
            hdr = data[pos]
            final = hdr & 1
            if (hdr >> 1) & 3 != 0:
                emit("%s: compressed blocks are not read here" % name)
                body = None
                break
            n = struct.unpack("<H", data[pos + 1:pos + 3])[0]
            body += data[pos + 5:pos + 5 + n]
            pos += 5 + n
            if final:
                break
        if body is None:
            continue
        stored, size = struct.unpack("<II", data[pos:pos + 8])
        got = crc32(body)
        emit("%s: mtime=%d %d bytes, crc32 %08x, stored %08x, size %s: %s" % (
            name, mtime, len(body), got, stored, "ok" if size == len(body) else "WRONG",
            "ok" if got == stored else "CRC MISMATCH"))


def modbus_job(rel):
    fun = crcmod.predefined.mkPredefinedCrcFun("modbus")
    for line in read(rel).splitlines():
        frame = bytes.fromhex(line)
        if len(frame) < 4:
            emit("%s: too short" % line)
            continue
        body, tail = frame[:-2], frame[-2:]
        got = fun(body)
        stored = struct.unpack("<H", tail)[0]
        kind = "exception %d" % body[2] if body[1] & 0x80 else "function %d, %d data bytes" % (body[1], len(body) - 2)
        emit("%s: unit %d %s, crc %04X %s" % (line, body[0], kind, stored,
                                             "ok" if got == stored else "BAD (want %04X)" % got))


def xmodem_job(names):
    fun = crcmod.predefined.mkPredefinedCrcFun("xmodem")
    for name in names:
        data = read_bytes(name)
        pos = 0
        good = 0
        received = b""
        while pos < len(data):
            if data[pos] == 4:
                emit("%s: EOT after %d blocks, %d good, %d bytes" % (name, pos // 133, good, len(received)))
                break
            blk = data[pos + 1]
            comp = data[pos + 2]
            block = data[pos + 3:pos + 131]
            stored = struct.unpack(">H", data[pos + 131:pos + 133])[0]
            got = fun(block)
            if blk + comp != 255:
                emit("  block %d: bad sequence complement" % blk)
            elif got != stored:
                emit("  block %d: crc %04X, computed %04X: NAK" % (blk, stored, got))
            else:
                good += 1
                received += block
                emit("  block %d: ok" % blk)
            pos += 133
        emit("  payload crc-32 %08x, trailing pad %d" % (crcmod.predefined.mkPredefinedCrcFun("crc-32")(
            received.rstrip(b"\x1a")), len(received) - len(received.rstrip(b"\x1a"))))


def armor_job(names):
    fun = crcmod.predefined.mkPredefinedCrcFun("crc-24")
    for name in names:
        lines = read(name).splitlines()
        kind = lines[0][len("-----BEGIN PGP "):-5]
        i = 1
        headers = []
        while lines[i]:
            headers.append(lines[i])
            i += 1
        body = []
        i += 1
        while not lines[i].startswith("="):
            body.append(lines[i])
            i += 1
        data = base64.b64decode("".join(body))
        stored = int.from_bytes(base64.b64decode(lines[i][1:]), "big")
        got = fun(data)
        emit("%s: %s, %s, %d bytes, crc24 %06X %s" % (name, kind, "; ".join(headers), len(data), stored,
                                                     "ok" if got == stored else "BAD (computed %06X)" % got))


def onewire_job(rel):
    fun = crcmod.predefined.mkPredefinedCrcFun("crc-8-maxim")
    families = {0x28: "DS18B20 thermometer", 0x10: "DS18S20 thermometer", 0x01: "DS2401 serial number"}
    for line in read(rel).splitlines():
        b = bytes.fromhex(line)
        got = fun(b[:7])
        serial = b[1:7][::-1].hex().upper()
        emit("%s: family %02X (%s) serial %s crc %02X %s; whole code crc %02X" % (
            line, b[0], families.get(b[0], "unknown"), serial, b[7], "ok" if got == b[7] else "BAD", fun(b)))


def rdb_job(names):
    fun = crcmod.predefined.mkPredefinedCrcFun("crc-64-jones")
    for name in names:
        data = read_bytes(name)
        body, tail = data[:-8], data[-8:]
        stored = struct.unpack("<Q", tail)[0]
        got = fun(body)
        keys = body.count(b"user:")
        emit("%s: %s, %d keys, crc64 %016x %s" % (name, body[:9].decode(), keys, stored,
                                                 "ok" if got == stored else "BAD (computed %016x)" % got))


def main():
    for line in read("jobs.tsv").splitlines():
        job = line.split("\t")
        emit("== " + " ".join(job))
        k = job[0]
        if k == "catalog":
            catalog_job()
        elif k == "custom":
            custom_job(job[1])
        elif k == "streams":
            streams_job(job[1])
        elif k == "code":
            code_job(crcmod.predefined.PredefinedCrc(job[1]), job[2], job[3], job[4])
        elif k == "code_custom":
            crc = crcmod.Crc(num(job[1]), initCrc=num(job[2]), rev=job[3] == "1", xorOut=num(job[4]))
            code_job(crc, job[5], job[6], job[7])
        elif k == "png":
            png_job(job[1:])
        elif k == "gzip":
            gzip_job(job[1:])
        elif k == "modbus":
            modbus_job(job[1])
        elif k == "xmodem":
            xmodem_job(job[1:])
        elif k == "armor":
            armor_job(job[1:])
        elif k == "onewire":
            onewire_job(job[1])
        else:
            rdb_job(job[1:])
    sys.stdout.write("\n".join(OUT) + "\n")


main()
