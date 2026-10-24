"""Play data/jobs.txt through the vendored pyDes 2.0.1 and print what each
step returned or raised. Its output is expected.out.

Run: python3 -I -B oracle.py > expected.out"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

import pyDes  # noqa: E402


def unesc(text, as_str):
    out = []
    i = 0
    while i < len(text):
        if text[i] == "~":
            out.append(int(text[i + 1:i + 3], 16))
            i += 3
        else:
            out.append(ord(text[i]))
            i += 1
    if as_str:
        return "".join(chr(c) for c in out)
    return bytes(out)


class State:
    def __init__(self):
        self.objs = {}
        self.last = None


def value(st, tok):
    if tok == "n":
        return None
    if tok == "@":
        return st.last
    if tok.startswith("h:"):
        return bytes.fromhex(tok[2:])
    if tok.startswith("b:"):
        return unesc(tok[2:], False)
    if tok.startswith("s:"):
        return unesc(tok[2:], True)
    if tok.startswith("r:"):
        _, n, pat = tok.split(":")
        n = int(n)
        p = bytes.fromhex(pat)
        return (p * (n // len(p) + 1))[:n]
    raise SystemExit("bad value " + tok)


def mode_of(word):
    return pyDes.CBC if word == "CBC" else pyDes.ECB


def show(x):
    if isinstance(x, bytes):
        return "h:" + x.hex()
    return repr(x)


def err(e):
    return "! " + type(e).__name__ + ": " + str(e).replace("\n", "\\n")


def options(st, toks):
    kw = {}
    for t in toks:
        k, _, v = t.partition("=")
        if k in ("mode",):
            kw[k] = mode_of(v)
        elif k == "padmode":
            kw[k] = int(v)
        elif k == "iv":
            kw["IV"] = value(st, v)
        else:
            kw[k] = value(st, v)
    return kw


def fnv(data):
    h = 2166136261
    for c in data:
        h = ((h ^ c) * 16777619) & 0xFFFFFFFF
    return h


def cipher_for(key):
    if len(key) == 8:
        return pyDes.des(key)
    return pyDes.triple_des(key)


def kcv(key):
    c = cipher_for(key)
    return c.encrypt(b"\0" * 8)[:3].hex().upper()


def pin_block(pan, pin):
    field = "0" + "%X" % len(pin) + pin
    field = field + "F" * (16 - len(field))
    acct = "0000" + pan[-13:-1]
    return bytes(a ^ b for a, b in zip(bytes.fromhex(field), bytes.fromhex(acct)))


def pin_from_block(block, pan):
    acct = bytes.fromhex("0000" + pan[-13:-1])
    clear = bytes(a ^ b for a, b in zip(block, acct)).hex().upper()
    n = int(clear[1], 16)
    return clear[0], clear[2:2 + n]


def retail_mac(key, data):
    if len(data) % 8 != 0 or len(data) == 0:
        data = data + b"\0" * (8 - len(data) % 8)
    k1 = key[:8]
    cbc = pyDes.des(k1, pyDes.CBC, b"\0" * 8)
    last = cbc.encrypt(data)[-8:]
    if len(key) == 8:
        return last
    k2 = key[8:16]
    return pyDes.des(k1).encrypt(pyDes.des(k2).decrypt(last))


def run_step(st, line):
    toks = line.split(" ")
    op = toks[0]
    if op == "new":
        name, kind = toks[1], toks[2]
        kw = options(st, toks[3:])
        key = kw.pop("key")
        try:
            if kind == "des":
                st.objs[name] = pyDes.des(key, **kw)
            else:
                st.objs[name] = pyDes.triple_des(key, **kw)
            print("new " + name + " = ok")
        except ValueError as e:
            st.objs.pop(name, None)
            print("new " + name + " " + err(e))
    elif op in ("enc", "dec", "sum"):
        obj = st.objs[toks[1]]
        data = value(st, toks[2])
        kw = options(st, toks[3:])
        try:
            if op == "dec":
                r = obj.decrypt(data, **kw)
            else:
                r = obj.encrypt(data, **kw)
        except ValueError as e:
            print(op + " " + err(e))
            return
        st.last = r
        if op == "dec":
            print("dec = " + repr(r))
        elif op == "enc":
            print("enc = " + show(r))
        else:
            print("sum = %d bytes, fnv %08x, starts %s" % (len(r), fnv(r), r[:8].hex()))
    elif op == "get":
        obj = st.objs[toks[1]]
        what = toks[2]
        if what == "key":
            r = obj.getKey()
        elif what == "iv":
            r = obj.getIV()
        elif what == "mode":
            r = obj.getMode()
        elif what == "pad":
            r = obj.getPadding()
        else:
            r = obj.getPadMode()
        print("get " + what + " = " + repr(r))
    elif op == "set":
        obj = st.objs[toks[1]]
        what = toks[2]
        try:
            if what == "key":
                obj.setKey(value(st, toks[3]))
            elif what == "iv":
                obj.setIV(value(st, toks[3]))
            elif what == "mode":
                obj.setMode(mode_of(toks[3]))
            elif what == "pad":
                obj.setPadding(value(st, toks[3]))
            else:
                obj.setPadMode(int(toks[3]))
            print("set " + what + " = ok")
        except ValueError as e:
            print("set " + what + " " + err(e))
    elif op == "kcv":
        key = value(st, toks[1])
        try:
            print("kcv " + key.hex() + " = " + kcv(key))
        except ValueError as e:
            print("kcv " + err(e))
    elif op == "pin":
        zpk = value(st, toks[1])
        pan, pin = toks[2], toks[3]
        clear = pin_block(pan, pin)
        enc = pyDes.triple_des(zpk).encrypt(clear)
        fmt, back = pin_from_block(pyDes.triple_des(zpk).decrypt(enc), pan)
        print("pin " + pan + " " + pin + ": clear " + clear.hex().upper() + ", under ZPK " + enc.hex().upper()
              + ", format " + fmt + ", recovered " + back)
    elif op == "translate":
        zpk1 = value(st, toks[1])
        zpk2 = value(st, toks[2])
        pan, pin = toks[3], toks[4]
        enc1 = pyDes.triple_des(zpk1).encrypt(pin_block(pan, pin))
        enc2 = pyDes.triple_des(zpk2).encrypt(pyDes.triple_des(zpk1).decrypt(enc1))
        _, back = pin_from_block(pyDes.triple_des(zpk2).decrypt(enc2), pan)
        print("translate " + pan + ": " + enc1.hex().upper() + " -> " + enc2.hex().upper() + ", recovered " + back)
    elif op == "mac":
        key = value(st, toks[1])
        data = value(st, toks[2])
        m = retail_mac(key, data)
        print("mac %d bytes = %s (full %s)" % (len(data), m[:4].hex().upper(), m.hex().upper()))
    elif op == "roundtrip":
        obj = st.objs[toks[1]]
        data = value(st, toks[2])
        e = obj.encrypt(data)
        d = obj.decrypt(e)
        verdict = "ok" if d == data else "MISMATCH " + repr(d)
        print("roundtrip %s %d -> %d bytes %s, %s" % (toks[1], len(data), len(e), e.hex(), verdict))
    else:
        raise SystemExit("bad step " + line)


def main():
    st = State()
    with open(os.path.join(HERE, "data", "jobs.txt")) as f:
        lines = f.read().split("\n")
    for line in lines:
        if line == "":
            continue
        if line.startswith("job "):
            st = State()
            print("== " + line[4:])
            continue
        run_step(st, line)


main()
