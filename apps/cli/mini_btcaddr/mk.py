# Writes data/: what a wallet or an exchange is handed to check (a CSV of
# withdrawal requests for BTC, testnet, Litecoin and XRP; extended keys;
# WIF private keys; witness scripts), the files the `python -m base58`
# command reads, and jobs.tsv, the jobs oracle.py and mini_btcaddr.kara
# run. Addresses and keys are made with the packages themselves
# (vendor/), from hashes of fixed strings, next to well-known published
# ones (the genesis address, the BIP-173 and BIP-32 examples).
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HERE, "vendor"))
sys.dont_write_bytecode = True

import base58  # noqa: E402
import bech32  # noqa: E402


def h(seed, n=32):
    return hashlib.sha256(seed.encode()).digest()[:n]


def esc(s):
    # Job text: \xNN and \uNNNN for anything outside printable ASCII.
    out = []
    for c in s:
        o = ord(c)
        if c == "\\":
            out.append("\\x5c")
        elif 0x20 <= o < 0x7f:
            out.append(c)
        elif o < 0x100:
            out.append("\\x%02x" % o)
        else:
            out.append("\\u%04x" % o)
    return "".join(out)


def write(rel, data):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode, **({} if mode == "wb" else {"encoding": "utf-8", "newline": "\n"})) as f:
        f.write(data)


def addr(version, seed, n=20, alphabet=base58.BITCOIN_ALPHABET):
    return base58.b58encode_check(bytes([version]) + h(seed, n), alphabet=alphabet).decode()


def seg(hrp, ver, seed, n=20):
    # Encoded without encode()'s round-trip check, so a program the
    # decoder refuses can still be written down.
    return bech32.bech32_encode(hrp, [ver] + bech32.convertbits(h(seed, n), 8, 5))


def swap_case_at(s, i):
    return s[:i] + s[i].swapcase() + s[i + 1:]


def withdrawals():
    rows = [("id", "coin", "address", "amount")]
    genesis = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    p2wpkh = "BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4"
    rows += [
        ("w001", "btc", genesis, "0.5"),
        ("w002", "btc", "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", "1.25"),
        ("w003", "btc", p2wpkh, "0.01"),
        ("w004", "btc", p2wpkh.lower(), "0.02"),
        ("w005", "btc", seg("bc", 0, "vault", 32), "12"),
        ("w006", "btc", "bc1p5d7rjq7g6rdk2yhzks9smlaqtedr4dekq08ge8ztwac72sfr9rusxg3297", "0.3"),
        ("w007", "btc", seg("bc", 1, "taproot-old", 32), "0.3"),
        ("w008", "btc", genesis.replace("1z", "lz"), "0.5"),
        ("w009", "btc", genesis[:-1] + "b", "0.5"),
        ("w010", "btc", genesis[:20], "0.5"),
        ("w011", "btc", " " + genesis, "0.5"),
        ("w012", "btc", genesis + " ", "0.5"),
        ("w013", "btc", genesis + "​", "0.5"),
        ("w014", "btc", addr(0x6f, "alice-test"), "0.1"),
        ("w015", "btc", seg("tb", 0, "alice-test"), "0.1"),
        ("w016", "btc", swap_case_at(p2wpkh, 10), "0.01"),
        ("w017", "btc", seg("bc", 0, "short", 16), "0.01"),
        ("w018", "btc", seg("bc", 16, "future", 40), "0.01"),
        ("w019", "btc", addr(0x05, "multisig"), "3"),
        ("w020", "btc", addr(0x00, "long", 21), "1"),
        ("w021", "btc", addr(0x30, "litecoin"), "1"),
        ("w022", "btc", "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t5", "0.01"),
        ("w023", "btc", "", "1"),
        ("w101", "tbtc", addr(0x6f, "bob-test"), "2"),
        ("w102", "tbtc", addr(0xc4, "bob-multisig"), "2"),
        ("w103", "tbtc", seg("tb", 0, "bob-wsh", 32), "2"),
        ("w104", "tbtc", "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7", "2"),
        ("w105", "tbtc", genesis, "2"),
        ("w201", "ltc", addr(0x30, "carol"), "10"),
        ("w202", "ltc", addr(0x32, "carol-ms"), "10"),
        ("w203", "ltc", addr(0x05, "carol-old"), "10"),
        ("w204", "ltc", seg("ltc", 0, "carol-sw"), "10"),
        ("w205", "ltc", seg("bc", 0, "carol-sw"), "10"),
        ("w301", "xrp", "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh", "25"),
        ("w302", "xrp", addr(0x00, "dave", alphabet=base58.XRP_ALPHABET), "25"),
        ("w303", "xrp", genesis, "25"),
        ("w304", "xrp", addr(0x00, "dave", alphabet=base58.XRP_ALPHABET).replace("r", "R", 1), "25"),
        ("w305", "doge", genesis, "25"),
    ]
    return "".join(",".join(r) + "\n" for r in rows)


def xkeys():
    v1 = "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8"
    lines = ["# BIP-32 test vector 1, master key", v1]

    def ext(version, depth, fp, child, chain, key):
        return base58.b58encode_check(bytes.fromhex(version) + bytes([depth]) + fp + child.to_bytes(4, "big")
                                      + chain + key).decode()

    pub = b"\x02" + h("account-key")
    lines.append("# an account xpub, m/84'/0'/0'")
    lines.append(ext("0488b21e", 3, h("parent", 4), 0x80000000, h("chain"), pub))
    lines.append("# the same key as a zpub and a ypub")
    lines.append(ext("04b24746", 3, h("parent", 4), 0x80000000, h("chain"), pub))
    lines.append(ext("049d7cb2", 3, h("parent", 4), 0x80000000, h("chain"), pub))
    lines.append("# testnet, and a private key")
    lines.append(ext("043587cf", 1, h("p2", 4), 7, h("chain2"), b"\x03" + h("k2")))
    lines.append(ext("0488ade4", 0, b"\0\0\0\0", 0, h("chain3"), b"\x00" + h("k3")))
    lines.append("# broken ones")
    lines.append(ext("0488b21e", 0, h("x", 4), 0, h("chain4"), b"\x02" + h("k4")))
    lines.append(ext("0488ade4", 2, h("x", 4), 5, h("chain5"), b"\x01" + h("k5")))
    lines.append(ext("0488b21e", 2, h("x", 4), 5, h("chain6"), b"\x05" + h("k6")))
    lines.append(ext("deadbeef", 2, h("x", 4), 5, h("chain7"), b"\x02" + h("k7")))
    lines.append(base58.b58encode_check(b"\x04\x88\xb2\x1e" + h("short", 20)).decode())
    lines.append(v1[:-1] + "9")
    lines.append(v1.replace("1", "l", 1))
    return "\n".join(lines) + "\n"


def wifs():
    lines = ["5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"]
    for net, seed, comp in [(0x80, "w1", True), (0x80, "w2", False), (0xef, "w3", True), (0xef, "w4", False)]:
        lines.append(base58.b58encode_check(bytes([net]) + h(seed) + (b"\x01" if comp else b"")).decode())
    lines.append(base58.b58encode_check(b"\x80" + h("w5") + b"\x02").decode())
    lines.append(base58.b58encode_check(b"\x80" + h("w6", 31)).decode())
    lines.append(base58.b58encode_check(b"\x05" + h("w7")).decode())
    lines.append("5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTj")
    return "\n".join(lines) + "\n"


def scripts():
    def push(b):
        return bytes([len(b)]) + b
    keys = [b"\x02" + h("signer%d" % i) for i in range(3)]
    ms = b"\x52" + b"".join(push(k) for k in keys) + b"\x53\xae"
    lines = ["# label,network,kind,hex"]
    lines.append("2-of-3 treasury,bc,wsh," + ms.hex())
    lines.append("2-of-3 treasury,tb,wsh," + ms.hex())
    lines.append("hot wallet,bc,wpkh," + h("hot", 20).hex())
    lines.append("hot wallet,ltc,wpkh," + h("hot", 20).hex())
    lines.append("timelock,bc,wsh," + (b"\x03\x40\x0d\x03\xb1\x75" + push(keys[0]) + b"\xac").hex())
    lines.append("bad hash,bc,wpkh," + h("hot", 19).hex())
    lines.append("empty script,bc,wsh,")
    return "\n".join(lines) + "\n"


def jobs():
    out = []
    for alph, hx in [("bitcoin", b"hello world".hex()), ("bitcoin", "0000" + b"hello world".hex()), ("bitcoin", ""),
                     ("bitcoin", "00"), ("bitcoin", "000000"), ("bitcoin", "ff" * 16), ("ripple", b"hello world".hex()),
                     ("ripple", "0000ff"), ("base45", b"hello world".hex()), ("base45", "00ff"), ("xl", "0001020304")]:
        out.append(["enc", alph, hx])
    for alph, s in [("bitcoin", "hello world"), ("bitcoin", ""), ("bitcoin", "café"), ("bitcoin", "€€ and é")]:
        out.append(["enc_str", alph, esc(s)])
    for alph, s, fix in [("bitcoin", "StV1DL6CwTryKyV", ""), ("bitcoin", "11StV1DL6CwTryKyV", ""), ("bitcoin", "1", ""),
                         ("bitcoin", "", ""), ("bitcoin", "111", ""), ("bitcoin", "StVlDL6CwTryKyV", "autofix"),
                         ("bitcoin", "StVlDL6CwTryKyV", ""), ("bitcoin", "xyz\b", ""), ("bitcoin", "StV1DL6CwTryKyV  \n", ""),
                         ("bitcoin", "  StV1DL6CwTryKyV", ""), ("bitcoin", "StV1DL6CwTryKyV　", ""),
                         ("bitcoin", "StéV", ""), ("bitcoin", "éèV", ""), ("bitcoin", "0OoIl1", "autofix"),
                         ("bitcoin", "0", ""), ("ripple", "rrr", ""), ("ripple", "pzz", "autofix"), ("base45", "00 A ", ""),
                         ("base45", "Zz", ""), ("xl", "0Oo", "autofix"), ("xl", "Il1", "autofix")]:
        out.append(["dec", alph, esc(s), fix])
    for alph, hx in [("bitcoin", b"hello world".hex()), ("bitcoin", ""), ("bitcoin", "00" * 3), ("ripple", "00" + "ab" * 20)]:
        out.append(["enc_check", alph, hx])
    for alph, s, fix in [("bitcoin", "3vQB7B6MrGQZaxCuFg4oh", ""), ("bitcoin", "3vQB7B6MrGQZaxCuFg4Oh", "autofix"),
                         ("bitcoin", "3vQB7B6MrGQZaxCuFg4oH", ""), ("bitcoin", "3vQB7B6MrGQZaxCuFg4Oh", ""),
                         ("bitcoin", "", ""), ("bitcoin", "1", ""), ("bitcoin", "3QJmnh", ""), ("bitcoin", "1111", "")]:
        out.append(["dec_check", alph, esc(s), fix])
    big = "0x111d38e5fc9071ffcd20b4a763cc9ae4f252bb4e48fd66a835e252ada93ff480d6dd43dc62a641155a5"
    for alph, n, one in [("bitcoin", "0", "1"), ("bitcoin", "0", "0"), ("bitcoin", "57", "1"), ("bitcoin", "58", "1"),
                         ("bitcoin", str(2 ** 64), "1"), ("bitcoin", str(int(big, 16)), "1"), ("ripple", "1000000", "1"),
                         ("base45", "123456789", "1")]:
        out.append(["enc_int", alph, n, one])
    for alph, s in [("bitcoin", base58.BITCOIN_ALPHABET.decode()), ("bitcoin", "2"), ("bitcoin", "1111z"), ("bitcoin", "z "),
                    ("base45", "Z "), ("bitcoin", "zl"), ("ripple", "r"), ("bitcoin", "")]:
        out.append(["dec_int", alph, esc(s)])
    for flags, name in [("", "cli/hello.txt"), ("-d", "cli/encoded.txt"), ("-c", "cli/hello.txt"), ("-dc", "cli/checked.txt"),
                        ("-dc", "cli/tampered.txt"), ("-d", "cli/bad-char.txt"), ("-d", "cli/empty.txt"), ("", "cli/binary.bin"),
                        ("-d", "cli/crlf.txt")]:
        out.append(["cli", flags, name])
    for s in ["A12UEL5L", "a12uel5l", "an83characterlonghumanreadablepartthatcontainsthenumber1andtheexcludedcharactersbio1tt5tgs",
              "abcdef1qpzry9x8gf2tvdw0s3jn54khce6mua7lmqqqxw",
              "11qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqc8247j",
              "split1checkupstagehandshakeupstreamerranterredcaperred2y9e3w", "?1ezyfcl", "\x201nwldj5", "\x7f1axkwrx",
              "an84characterslonghumanreadablepartthatcontainsthenumber1andtheexcludedcharactersbio1569pvx",
              "pzry9x0s0muk", "1pzry9x0s0muk", "x1b4n0q5v", "li1dgmt3", "de1lg7wtÿ", "A1G7SGD8", "10a06t8", "1qzzfhee",
              "A12uEL5L", "a1qqqqqq", "a12uel5m", ""]:
        out.append(["b32_decode", esc(s)])
    for hrp, vals in [("a", ""), ("abcdef", ",".join(str(i) for i in range(32))), ("bc", "0,1,2,31"), ("BC", "0,1"),
                      ("x", "32"), ("x", "-1")]:
        out.append(["b32_encode", hrp, vals])
    for hrp, a in [("bc", "BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4"),
                   ("tb", "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7"),
                   ("bc", "bc1pw508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7k7grplx"),
                   ("bc", "BC1SW50QA3JX3S"), ("bc", "bc1zw508d6qejxtdg4y5r3zarvaryvg6kdaj"),
                   ("tb", "tb1qqqqqp399et2xygdj5xreqhjjvcmzhxw4aywxecjdzew6hylgvsesrxh6hy"),
                   ("bc", "bc1p0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9hcz7vqzk5jj0"),
                   ("tc", "tc1qw508d6qejxtdg4y5r3zarvary0c5xw7kg3g4ty"), ("bc", "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t5"),
                   ("bc", "BC13W508D6QEJXTDG4Y5R3ZARVARY0C5XW7KN40WF2"), ("bc", "bc1rw5uspcuh"),
                   ("bc", "bc10w508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7kw5rljs90"),
                   ("bc", "BC1QR508D6QEJXTDG4Y5R3ZARVARYV98GJ9P"),
                   ("tb", "tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sL5k7"),
                   ("bc", "bc1zw508d6qejxtdg4y5r3zarvaryvqyzf3du"), ("bc", "bc1gmk9yu"),
                   ("tb", "tb1pqqqqp399et2xygdj5xreqhjjvcmzhxw4aywxecjdzew6hylgvsesf3hn0c")]:
        out.append(["seg_decode", hrp, a])
    for hrp, ver, hx in [("bc", "0", "751e76e8199196d454941c45d1b3a323f1433bd6"), ("bc", "1", "751e76e8199196d454941c45d1b3a323f1433bd6"),
                         ("bc", "0", "751e76e8199196d454941c45d1b3a323f1433b"), ("bc", "17", "751e"), ("bc", "16", "751e"),
                         ("bc", "2", "75"), ("bc", "2", "00" * 40), ("bc", "2", "00" * 41), ("tb", "0", "00" * 32),
                         ("an83characterlonghumanreadablepartthatcontainsthenumber1andtheexcludedcharactersbio", "0", "00" * 20)]:
        out.append(["seg_encode", hrp, ver, hx])
    for vals, fb, tb, pad in [("255", "8", "5", "1"), ("255", "8", "5", "0"), ("1,2,3", "5", "8", "0"), ("0,0,0,0,0,0,0,0", "5", "8", "0"),
                              ("31,31,31,31,31,31,31,24", "5", "8", "0"), ("31,31,31,31,31,31,31,31", "5", "8", "0"),
                              ("256", "8", "5", "1"), ("-1", "8", "5", "1"), ("", "8", "5", "1"), ("1,2", "8", "16", "1")]:
        out.append(["convert", vals, fb, tb, pad])
    out.append(["withdrawals", "withdrawals.csv"])
    out.append(["xkeys", "xkeys.txt"])
    out.append(["wif", "wif.txt"])
    out.append(["scripts", "scripts.csv"])
    return out


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    write("withdrawals.csv", withdrawals())
    write("xkeys.txt", xkeys())
    write("wif.txt", wifs())
    write("scripts.csv", scripts())
    write("cli/hello.txt", "hello world\n")
    write("cli/encoded.txt", base58.b58encode(b"hello world\n").decode() + "\n")
    write("cli/checked.txt", base58.b58encode_check(b"backup-2024").decode() + "\n")
    t = base58.b58encode_check(b"backup-2024").decode()
    write("cli/tampered.txt", t[:-2] + ("a" if t[-2] != "a" else "b") + t[-1] + "\n")
    write("cli/bad-char.txt", "StV1DL6Cw0TryKyV\n")
    write("cli/empty.txt", "")
    write("cli/binary.bin", bytes(range(0, 256, 15)) + b"\x00\x00")
    write("cli/crlf.txt", "StV1DL6CwTryKyV\r\n")
    write("jobs.tsv", "".join("\t".join(j) + "\n" for j in jobs()))


main()
