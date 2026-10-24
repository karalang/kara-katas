"""Run data/jobs.txt against the vendored pyStrich 0.20 and print the
results: expected.out.

pyStrich's matrix renderers import its SVG and EPS writers, which import
the Courier Prime glyph outlines (pystrich/_courier_glyphs.py, under the
SIL Open Font License). The jobs never draw text, so the glyph module is
not vendored and an empty stand-in is installed before the import.

Run: python3 -I -B oracle.py > expected.out
"""
import os
import sys
import types
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

_glyphs = types.ModuleType("pystrich._courier_glyphs")
_glyphs.ADVANCE = 0
_glyphs.GLYPHS = {}
_glyphs.ASCENT = 0
_glyphs.DESCENT = 0
_glyphs.EM_SIZE = 1
sys.modules["pystrich._courier_glyphs"] = _glyphs

from pystrich.aztec import AztecData, AztecEncoder  # noqa: E402
from pystrich.aztec.dpencoder import encode_high_level as az_high_level  # noqa: E402
from pystrich.aztec.modemessage import build_mode_message  # noqa: E402
from pystrich.aztec.symbol import codeword_bits, module_count  # noqa: E402
from pystrich.aztec.textencoder import TextEncoder as AzTextEncoder  # noqa: E402
from pystrich.aztec.textencoder import _ECI_BY_CHARSET as AZ_ECI  # noqa: E402
from pystrich.datamatrix import DataMatrixData, DataMatrixEncoder  # noqa: E402
from pystrich.datamatrix.textencoder import TextEncoder as DmTextEncoder  # noqa: E402
from pystrich.gs1 import GS1Fixed, GS1Variable  # noqa: E402

DATA = os.path.join(HERE, "data")


def read(rel):
    with open(os.path.join(DATA, rel), encoding="utf-8", newline="") as f:
        return f.read()


def fnv(text):
    h = 0x811C9DC5
    for b in text.encode("utf-8"):
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return "%08x" % h


def hexwords(words, digits):
    return "".join("%0*x" % (digits, w) for w in words)


def options(words):
    opts = {}
    for w in words:
        key, _, value = w.partition("=")
        opts[key] = value
    return opts


def show_matrix(art):
    lines = art.split("\n")[:-1]
    width = len(lines[0]) if lines else 0
    print("  ascii %dx%d fnv %s" % (width, len(lines), fnv(art)))


def show_art(art):
    for line in art.split("\n")[:-1]:
        print("    |" + line + "|")


def print_warnings(caught):
    for w in caught:
        print("  warning: %s: %s" % (w.category.__name__, w.message))


def describe(e):
    return "%s: %s" % (type(e).__name__, e)


# ------------------------------------------------------------ Data Matrix

def dm_input(text, enc):
    if enc == "str":
        return text
    if enc == "auto":
        return DataMatrixData(text, auto_encoding=True)
    return DataMatrixData(text, encoding=enc)


def dm_report(data, shape, force, qz, art):
    enc = DataMatrixEncoder(data, quiet_zone=qz, force_byte_mode=force, symbol_shape=shape)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        te = DmTextEncoder()
        words = te.encode(data, force_byte_mode=force, symbol_shape=shape)
    s = te.spec
    rows = (s.region_rows + 2) * s.v_regions
    cols = (s.region_cols + 2) * s.h_regions
    return enc, te, words, rows, cols


def job_dm(rel, words):
    o = options(words)
    shape = o.get("shape", "square")
    qz = int(o.get("qz", "2"))
    force = "bytes" in o
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            data = dm_input(read(rel), o.get("enc", "str"))
            enc, te, cw, rows, cols = dm_report(data, shape, force, qz, "art" in o)
            err = None
        except Exception as e:
            err = e
    print_warnings(caught)
    if err is not None:
        print("  error " + describe(err))
        return
    s = te.spec
    print("  symbol %dx%d %s, regions %dx%d, %d data + %d error codewords, %d block%s"
          % (rows, cols, s.shape, s.h_regions, s.v_regions, s.data_words, s.error_words,
             s.rs_blocks, "" if s.rs_blocks == 1 else "s"))
    print("  data " + hexwords(cw[:s.data_words], 2))
    print("  ec " + hexwords(cw[s.data_words:], 2))
    art = enc.get_ascii()
    show_matrix(art)
    if "art" in o:
        show_art(art)


# ------------------------------------------------------------ Aztec

def az_input(text, enc):
    if enc == "str":
        return text
    if enc == "auto":
        return AztecData(text, auto_encoding=True)
    return AztecData(text, encoding=enc)


def az_layout(data, ecc, kind, layers):
    if not isinstance(data, AztecData):
        data = AztecData(data, auto_encoding=True)
    text, charset = data.as_plain_text()
    bits = az_high_level(text.encode(charset), eci=AZ_ECI[charset])
    k, n, cws, num_ec = AzTextEncoder()._choose_size(bits, ecc, kind, layers)
    return bits, k, n, cws, num_ec


def job_az(rel, words):
    o = options(words)
    ecc = int(o.get("ecc", "23"))
    kind = o.get("kind", "auto")
    layers = int(o["layers"]) if "layers" in o else None
    qz = int(o.get("qz", "2"))
    try:
        data = az_input(read(rel), o.get("enc", "str"))
        enc = AztecEncoder(data, ecc=ecc, symbol_kind=kind, layers=layers, quiet_zone=qz)
        bits, k, n, cws, num_ec = az_layout(data, ecc, kind, layers)
    except Exception as e:
        print("  error " + describe(e))
        return
    size = module_count(k, n)
    width = codeword_bits(k, n)
    print("  %d bits, %s L%d, %dx%d, %d-bit codewords, %d data + %d check"
          % (len(bits), k, n, size, size, width, len(cws), num_ec))
    mode = build_mode_message(k, layers=n, data_codewords=len(cws))
    print("  mode " + "".join(str(b) for b in mode))
    print("  data " + hexwords(cws, (width + 3) // 4))
    art = enc.get_ascii()
    show_matrix(art)
    if "art" in o:
        show_art(art)


# ------------------------------------------------------------ !labels

def gtin_check(digits):
    total = 0
    for i, ch in enumerate(reversed(digits[:-1])):
        total += int(ch) * (3 if i % 2 == 0 else 1)
    return (10 - total % 10) % 10


def prog_labels(rel):
    lines = [ln for ln in read(rel).split("\n") if ln]
    ok = bad = 0
    first = True
    for line in lines[1:]:
        sku, gtin, expiry, batch, serial = line.split(",")
        if len(gtin) != 14 or not (gtin.isascii() and gtin.isdigit()):
            print("  %s: GTIN %s is not 14 digits" % (sku, gtin))
            bad += 1
            continue
        want = gtin_check(gtin)
        if int(gtin[-1]) != want:
            print("  %s: GTIN %s has check digit %s, expected %d" % (sku, gtin, gtin[-1], want))
            bad += 1
            continue
        human = "(01)" + gtin
        try:
            fields = [GS1Fixed("01", gtin)]
            if expiry:
                fields.append(GS1Fixed("17", expiry))
                human += "(17)" + expiry
            fields.append(GS1Variable("10", batch))
            human += "(10)" + batch
            if serial:
                fields.append(GS1Variable("21", serial))
                human += "(21)" + serial
            data = DataMatrixData.gs1(*fields)
            enc = DataMatrixEncoder(data, quiet_zone=1)
            te = DmTextEncoder()
            te.encode(data)
        except Exception as e:
            print("  %s: error %s" % (sku, describe(e)))
            bad += 1
            continue
        s = te.spec
        art = enc.get_ascii()
        print("  %s: %s -> %dx%d, %d data codewords, fnv %s"
              % (sku, human, s.region_rows + 2, s.region_cols + 2, s.data_words, fnv(art)))
        if first:
            show_art(art)
            first = False
        ok += 1
    print("  %d labels, %d rejected" % (ok, bad))


# ------------------------------------------------------------ !tickets

def prog_tickets(rel):
    for line in read(rel).split("\n"):
        if not line:
            continue
        kind = line.split("|")[0]
        enc = AztecEncoder(line, quiet_zone=1)
        bits, k, n, cws, num_ec = az_layout(line, 23, "auto", None)
        size = module_count(k, n)
        dm = DmTextEncoder()
        dm.encode(line)
        s = dm.spec
        art = enc.get_ascii()
        print("  %s: %d characters -> aztec %s L%d %dx%d (%d+%d), data matrix %dx%d, fnv %s"
              % (kind, len(line), k, n, size, size, len(cws), num_ec,
                 (s.region_rows + 2) * s.v_regions, (s.region_cols + 2) * s.h_regions, fnv(art)))
        if kind == "transit":
            show_art(art)


# ------------------------------------------------------------ !capacity

CLASSES = [
    ("digits", lambda i: str(i % 10)),
    ("upper", lambda i: chr(65 + i % 26)),
    ("lower", lambda i: chr(97 + i % 26)),
    ("words", lambda i: "lorem ipsum dolor sit amet, "[i % 28]),
    ("latin1", lambda i: "äöüß"[i % 4]),
    ("binary", lambda i: chr((i * 37) % 256)),
]


def dm_size(text, shape):
    te = DmTextEncoder()
    try:
        te.encode(text, symbol_shape=shape)
    except Exception:
        return "-"
    s = te.spec
    return "%dx%d" % ((s.region_rows + 2) * s.v_regions, (s.region_cols + 2) * s.h_regions)


def prog_capacity():
    print("  %-7s %5s  %-9s %-9s %s" % ("class", "chars", "square", "rect", "aztec"))
    for name, gen in CLASSES:
        for n in (1, 10, 50, 200):
            text = "".join(gen(i) for i in range(n))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                sq = dm_size(text, "square")
                rect = dm_size(text, "rectangular")
            _, k, layers, cws, num_ec = az_layout(text, 23, "auto", None)
            size = module_count(k, layers)
            az = "%s L%d %dx%d" % (k, layers, size, size)
            print(("  %-7s %5d  %-9s %-9s %s" % (name, n, sq, rect, az)).rstrip())


def main():
    for line in read("jobs.txt").split("\n"):
        if not line:
            continue
        if line.startswith("#"):
            print(line)
            continue
        print("> " + line)
        parts = line.split(" ")
        cmd, args = parts[0], parts[1:]
        if cmd == "dm":
            job_dm(args[0], args[1:])
        elif cmd == "az":
            job_az(args[0], args[1:])
        elif cmd == "!labels":
            prog_labels(args[0])
        elif cmd == "!tickets":
            prog_tickets(args[0])
        elif cmd == "!capacity":
            prog_capacity()
        else:
            raise SystemExit("unknown job " + line)


main()
