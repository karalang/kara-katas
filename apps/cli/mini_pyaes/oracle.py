#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py) through the vendored pyaes and prints
what each step returns. Bytes print as hex with their length, or as their
length and FNV-1a hash past 64 bytes; a step that raises prints
"error <Class>: <message>".

Run: python3 -I -B oracle.py > expected.out"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import pyaes  # noqa: E402

DATA = os.path.join(HERE, "data")


def fnv(b):
    h = 0x811C9DC5
    for x in b:
        h = ((h ^ x) * 0x01000193) & 0xFFFFFFFF
    return h


def show(b):
    if isinstance(b, list):
        return repr(b)
    if len(b) > 64:
        return "%d bytes, fnv1a %08x" % (len(b), fnv(b))
    return "%s (%d bytes)" % (b.hex(), len(b))


def val(f):
    return None if f == "-" else bytes.fromhex(f)


def path(p):
    return os.path.join(DATA, p)


modes = {}
counters = {}
feeders = {}


def make_mode(f):
    kind = f[2]
    key = val(f[3])
    if kind == "ecb":
        return pyaes.AESModeOfOperationECB(key)
    if kind == "cbc":
        return pyaes.AESModeOfOperationCBC(key, iv=val(f[4]) if len(f) > 4 else None)
    if kind == "ofb":
        return pyaes.AESModeOfOperationOFB(key, iv=val(f[4]) if len(f) > 4 else None)
    if kind == "cfb":
        return pyaes.AESModeOfOperationCFB(key, val(f[4]), segment_size=int(f[5]))
    if len(f) > 4:
        return pyaes.AESModeOfOperationCTR(key, counter=counters[f[4]])
    return pyaes.AESModeOfOperationCTR(key)


def stream(f):
    mode = modes[f[2]]
    block = int(f[5])
    kw = {"padding": f[6]} if len(f) > 6 else {}
    run = pyaes.encrypt_stream if f[1] == "encrypt" else pyaes.decrypt_stream
    with open(path(f[3]), "rb") as src, open(path(f[4]), "wb") as dst:
        run(mode, src, dst, block_size=block, **kw)
    with open(path(f[4]), "rb") as got:
        return show(got.read())


def compare(a, b):
    with open(path(a), "rb") as fa, open(path(b), "rb") as fb:
        x, y = fa.read(), fb.read()
    if x == y:
        return "same (%d bytes)" % len(x)
    n = 0
    while n < len(x) and n < len(y) and x[n] == y[n]:
        n += 1
    return "differ at byte %d (%d and %d bytes)" % (n, len(x), len(y))


def step(f, out):
    op = f[0]
    if op == "mode":
        modes[f[1]] = make_mode(f)
        out.append("ok")
    elif op == "counter":
        counters[f[1]] = pyaes.Counter(initial_value=int(f[2]))
        out.append("ok")
    elif op == "value":
        out.append(repr(counters[f[1]].value))
    elif op == "aes":
        aes = pyaes.AES(val(f[1]))
        b = val(f[3])
        out.append(show(aes.encrypt(b) if f[2] == "encrypt" else aes.decrypt(b)))
    elif op == "encrypt":
        out.append(show(modes[f[1]].encrypt(val(f[2]))))
    elif op == "decrypt":
        out.append(show(modes[f[1]].decrypt(val(f[2]))))
    elif op == "feeder":
        cls = pyaes.Encrypter if f[3] == "encrypter" else pyaes.Decrypter
        if len(f) > 4:
            feeders[f[1]] = cls(modes[f[2]], padding=f[4])
        else:
            feeders[f[1]] = cls(modes[f[2]])
        out.append("ok")
    elif op == "feed":
        if len(f) > 2:
            out.append(show(feeders[f[1]].feed(val(f[2]))))
        else:
            out.append(show(feeders[f[1]].feed()))
    elif op == "pipe":
        fe, fd = feeders[f[1]], feeders[f[2]]
        c = fe.feed(val(f[3]))
        c += fe.feed()
        out.append("ciphertext " + show(c))
        p = fd.feed(c)
        p += fd.feed()
        out.append("plaintext " + show(p))
        out.append("same" if p == val(f[3]) else "differs")
    elif op == "roundtrip":
        c = modes[f[1]].encrypt(val(f[3]))
        out.append("ciphertext " + show(c))
        p = modes[f[2]].decrypt(c)
        out.append("plaintext " + show(p))
        out.append("same" if p == val(f[3]) else "differs")
    elif op == "stream":
        out.append(stream(f))
    elif op == "cut":
        with open(path(f[1]), "rb") as src:
            b = src.read()[:int(f[3])]
        with open(path(f[2]), "wb") as dst:
            dst.write(b)
        out.append(show(b))
    elif op == "compare":
        out.append(compare(f[1], f[2]))
    elif op == "size":
        with open(path(f[1]), "rb") as src:
            out.append(show(src.read()))


def main():
    os.makedirs(path("out"), exist_ok=True)
    with open(path("jobs.tsv")) as fh:
        lines = fh.read().split("\n")
    w = sys.stdout.write
    for line in lines:
        if not line:
            continue
        f = line.split("\t")
        if f[0] == "job":
            w("== %s\n" % f[1])
            continue
        w("> %s\n" % " ".join(x if x else "''" for x in f))
        out = []
        try:
            step(f, out)
        except Exception as e:  # noqa: BLE001
            for x in out:
                w("  -> %s\n" % x)
            msg = str(e)
            if isinstance(e, OSError) and e.filename:
                msg = "[Errno %d] %s: %r" % (e.errno, e.strerror, os.path.relpath(e.filename, HERE))
            w("  error %s: %s\n" % (type(e).__name__, msg))
            continue
        for x in out:
            w("  -> %s\n" % x)


main()
