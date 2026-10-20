# Runs data/jobs.tsv through base58 2.1.1 and bech32 1.2.0 themselves
# (vendor/, unchanged) and prints what each job gives; expected.out is
# this output.
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True
os.chdir(HERE)

import base58  # noqa: E402
import bech32  # noqa: E402
from base58.__main__ import _fmap  # noqa: E402

DATA = "data"
ALPHABETS = {
    "bitcoin": base58.BITCOIN_ALPHABET,
    "ripple": base58.XRP_ALPHABET,
    "base45": b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:",
    "xl": base58.BITCOIN_ALPHABET.replace(b"x", b"l"),
}


def show(text):
    out = []
    for c in text:
        if c == "\r":
            out.append("<CR>")
        elif (c < " " and c not in "\t\n") or "\x7f" <= c <= "\x9f":
            out.append("<x%02x>" % ord(c))
        else:
            out.append(c)
    return "".join(out)


def print(line):
    sys.stdout.write(show(line) + "\n")


def err(e):
    return "error: %s: %s" % (type(e).__name__, e)


def unesc(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and s[i + 1] == "x":
            out.append(chr(int(s[i + 2:i + 4], 16)))
            i += 4
        elif s[i] == "\\" and s[i + 1] == "u":
            out.append(chr(int(s[i + 2:i + 6], 16)))
            i += 6
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def ints(s):
    return [int(x) for x in s.split(",")] if s else []


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return f.read()


def attempt(f):
    try:
        print(repr(f()))
    except Exception as e:
        print(err(e))


# --- the library

def library_job(job):
    kind, a = job[0], job[1:]
    if kind == "enc":
        attempt(lambda: base58.b58encode(bytes.fromhex(a[1]), alphabet=ALPHABETS[a[0]]))
    elif kind == "enc_str":
        attempt(lambda: base58.b58encode(unesc(a[1]), alphabet=ALPHABETS[a[0]]))
    elif kind == "dec":
        attempt(lambda: base58.b58decode(unesc(a[1]), alphabet=ALPHABETS[a[0]], autofix=a[2] == "autofix"))
    elif kind == "enc_check":
        attempt(lambda: base58.b58encode_check(bytes.fromhex(a[1]), alphabet=ALPHABETS[a[0]]))
    elif kind == "dec_check":
        attempt(lambda: base58.b58decode_check(unesc(a[1]), alphabet=ALPHABETS[a[0]], autofix=a[2] == "autofix"))
    elif kind == "enc_int":
        attempt(lambda: base58.b58encode_int(int(a[1]), default_one=a[2] == "1", alphabet=ALPHABETS[a[0]]))
    elif kind == "dec_int":
        attempt(lambda: base58.b58decode_int(unesc(a[1]), alphabet=ALPHABETS[a[0]]))
    elif kind == "b32_decode":
        attempt(lambda: bech32.bech32_decode(unesc(a[0])))
    elif kind == "b32_encode":
        attempt(lambda: bech32.bech32_encode(a[0], ints(a[1])))
    elif kind == "seg_decode":
        attempt(lambda: bech32.decode(a[0], a[1]))
    elif kind == "seg_encode":
        attempt(lambda: bech32.encode(a[0], int(a[1]), bytes.fromhex(a[2])))
    elif kind == "convert":
        attempt(lambda: bech32.convertbits(ints(a[0]), int(a[1]), int(a[2]), a[3] == "1"))


def cli_job(flags, name):
    # python -m base58 [flags] FILE: the file's bytes in, the result's
    # bytes out, or sys.exit(e) with the error on stderr.
    with open(os.path.join(DATA, name), "rb") as f:
        data = f.read()
    fun = _fmap[("d" in flags, "c" in flags)]
    try:
        print("stdout %r" % fun(data))
    except Exception as e:
        print("exit 1, stderr: %s" % e)


# --- programs

NETS = {
    "btc": ("bc", {0x00: "P2PKH", 0x05: "P2SH"}, "bitcoin"),
    "tbtc": ("tb", {0x6f: "P2PKH", 0xc4: "P2SH"}, "bitcoin"),
    "ltc": ("ltc", {0x30: "P2PKH", 0x32: "P2SH", 0x05: "P2SH (old 3-address)"}, "bitcoin"),
    "xrp": (None, {0x00: "account"}, "ripple"),
}
OWNERS = {0x00: "bitcoin", 0x05: "bitcoin P2SH", 0x6f: "testnet", 0xc4: "testnet P2SH", 0x30: "litecoin",
          0x32: "litecoin P2SH"}
SEGWIT_HRPS = [("bc", "bitcoin"), ("tb", "testnet"), ("ltc", "litecoin")]


def check_address(coin, a):
    if coin not in NETS:
        return "REJECT no such coin"
    hrp, versions, alph_name = NETS[coin]
    alph = ALPHABETS[alph_name]
    if a == "":
        return "REJECT empty address"
    if hrp is not None and a.lower().startswith(hrp + "1"):
        ver, prog = bech32.decode(hrp, a)
        if ver is None:
            got, data = bech32.bech32_decode(a)
            if got is None:
                return "REJECT bech32: bad character, mixed case or checksum"
            prog8 = bech32.convertbits(data[1:], 5, 8, False)
            if prog8 is None:
                return "REJECT bech32: program is not whole bytes"
            return "REJECT bech32: witness version %d with a %d-byte program" % (data[0], len(prog8))
        kind = {(0, 20): "P2WPKH", (0, 32): "P2WSH", (1, 32): "P2TR"}.get((ver, len(prog)), "witness v%d" % ver)
        canon = bech32.encode(hrp, ver, prog)
        return "OK %s %s%s" % (kind, bytes(prog).hex()[:8], "" if canon == a else " (as %s)" % canon)
    for other, name in SEGWIT_HRPS:
        if other != hrp and a.lower().startswith(other + "1") and bech32.decode(other, a)[0] is not None:
            return "REJECT a %s address" % name
    try:
        payload = base58.b58decode_check(a, alphabet=alph)
    except ValueError as e:
        try:
            fixed = base58.b58decode_check(a, alphabet=alph, autofix=True)
        except ValueError:
            return "REJECT base58: %s" % e
        return "REJECT base58: %s; did you mean %s?" % (e, base58.b58encode_check(fixed, alphabet=alph).decode())
    if len(payload) != 21:
        return "REJECT %d-byte payload, want 21" % len(payload)
    v = payload[0]
    if v not in versions:
        return "REJECT version 0x%02x (%s)" % (v, OWNERS.get(v, "unknown"))
    canon = base58.b58encode_check(payload, alphabet=alph).decode()
    return "OK %s %s%s" % (versions[v], payload[1:5].hex(), "" if canon == a else " (as %s)" % canon)


def withdrawals_job(name):
    rows = read(name).split("\n")[1:-1]
    counts = {}
    for row in rows:
        wid, coin, a, amount = row.split(",")
        verdict = check_address(coin, a)
        print("%s %s %s: %s" % (wid, coin, amount, verdict))
        key = (coin, verdict.split(" ")[0])
        counts[key] = counts.get(key, 0) + 1
    for key in sorted(counts):
        print("  %s %s: %d" % (key[0], key[1], counts[key]))


XKEYS = {
    "0488b21e": ("xpub", False, "0488b21e"), "0488ade4": ("xprv", True, "0488ade4"),
    "049d7cb2": ("ypub", False, "0488b21e"), "04b24746": ("zpub", False, "0488b21e"),
    "043587cf": ("tpub", False, "043587cf"), "04358394": ("tprv", True, "04358394"),
}


def xkeys_job(name):
    for line in read(name).split("\n")[:-1]:
        if line.startswith("#"):
            print(line)
            continue
        head = line[:12] + "..."
        try:
            raw = base58.b58decode_check(line)
        except ValueError as e:
            print("%s %s" % (head, e))
            continue
        if len(raw) != 78:
            print("%s %d bytes, want 78" % (head, len(raw)))
            continue
        ver = raw[:4].hex()
        if ver not in XKEYS:
            print("%s unknown version %s" % (head, ver))
            continue
        kind, private, plain = XKEYS[ver]
        depth, fp, child = raw[4], raw[5:9].hex(), int.from_bytes(raw[9:13], "big")
        chain, key = raw[13:45], raw[45:]
        child_s = "%d'" % (child - 2 ** 31) if child >= 2 ** 31 else str(child)
        problems = []
        if depth == 0 and (fp != "00000000" or child != 0):
            problems.append("a master key with a parent")
        if private and key[0] != 0:
            problems.append("private key starts with 0x%02x" % key[0])
        if not private and key[0] not in (2, 3):
            problems.append("public key starts with 0x%02x" % key[0])
        print("%s %s depth %d parent %s child %s chain %s..." % (head, kind, depth, fp, child_s, chain.hex()[:12]))
        if problems:
            print("  invalid: " + "; ".join(problems))
        elif plain != ver:
            print("  as %s: %s" % (XKEYS[plain][0], base58.b58encode_check(bytes.fromhex(plain) + raw[4:]).decode()))


def wif_job(name):
    for line in read(name).split("\n")[:-1]:
        head = line[:10] + "..."
        try:
            raw = base58.b58decode_check(line)
        except ValueError as e:
            print("%s %s" % (head, e))
            continue
        net = {0x80: "mainnet", 0xef: "testnet"}.get(raw[0])
        if net is None:
            print("%s not a private key (version 0x%02x)" % (head, raw[0]))
            continue
        if len(raw) == 33:
            comp = "uncompressed"
        elif len(raw) == 34 and raw[33] == 1:
            comp = "compressed"
        else:
            print("%s %s, %d bytes: not a key" % (head, net, len(raw)))
            continue
        print("%s %s %s key, fingerprint %s" % (head, net, comp, hashlib.sha256(raw[1:33]).hexdigest()[:8]))


def scripts_job(name):
    for line in read(name).split("\n")[1:-1]:
        label, net, kind, hx = line.split(",")
        data = bytes.fromhex(hx)
        prog = hashlib.sha256(data).digest() if kind == "wsh" else data
        a = bech32.encode(net, 0, prog)
        if a is None:
            print("%s: cannot encode a %d-byte program" % (label, len(prog)))
        else:
            print("%s: %s (%d-byte script)" % (label, a, len(data)) if kind == "wsh" else "%s: %s" % (label, a))


def main():
    for line in read("jobs.tsv").split("\n")[:-1]:
        job = line.split("\t")
        print("== " + " ".join(job))
        if job[0] == "cli":
            cli_job(job[1], job[2])
        elif job[0] == "withdrawals":
            withdrawals_job(job[1])
        elif job[0] == "xkeys":
            xkeys_job(job[1])
        elif job[0] == "wif":
            wif_job(job[1])
        elif job[0] == "scripts":
            scripts_job(job[1])
        else:
            library_job(job)


main()
