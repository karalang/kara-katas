"""Replay data/jobs.tsv against the vendored pdf417gen 0.8.1.

Each job is a tab-separated command: encode data to a PDF417 bar code and
print its code words, rows and module grid, render it to an SVG file or a
PPM image under data/out/, or call the library's helpers (compaction,
error correction, base conversion, colours) directly. A job that raises
prints `error <class>: <message>`.

render_image needs Pillow, which pdf417gen depends on; the images are
written as binary PPM, whose bytes are Pillow's pixels after its nearest-
neighbour resize and padding.
"""
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "vendor"))

from pdf417gen import encode, render_image, render_svg  # noqa: E402
from pdf417gen import encoding as enc  # noqa: E402
from pdf417gen import rendering  # noqa: E402
from pdf417gen.compaction import (  # noqa: E402
    _split_to_chunks, compact, optimizations)
from pdf417gen.compaction.byte import compact_bytes  # noqa: E402
from pdf417gen.compaction.numeric import compact_numbers  # noqa: E402
from pdf417gen.compaction.text import (  # noqa: E402
    compact_text, compact_text_interim)
from pdf417gen.error_correction import (  # noqa: E402
    compute_error_correction_code_words)
from pdf417gen.util import switch_base, to_bytes  # noqa: E402


def out(s):
    print("  " + s)


def unescape(s):
    """Job text uses \\t, \\n, \\r, \\\\ and \\uXXXX escapes."""
    res = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            if n == "t":
                res.append("\t")
            elif n == "n":
                res.append("\n")
            elif n == "r":
                res.append("\r")
            elif n == "u":
                res.append(chr(int(s[i + 2:i + 6], 16)))
                i += 4
            else:
                res.append(n)
            i += 2
            continue
        res.append(c)
        i += 1
    return "".join(res)


def data_of(spec):
    """`text:...` is a str, `hex:...` bytes, `file:path` a file's bytes,
    `textfile:path` a file read as UTF-8 text."""
    kind, _, rest = spec.partition(":")
    if kind == "text":
        return unescape(rest)
    if kind == "hex":
        return bytes.fromhex(rest)
    if kind == "file":
        with open(os.path.join("data", rest), "rb") as fh:
            return fh.read()
    if kind == "textfile":
        with open(os.path.join("data", rest), encoding="utf-8") as fh:
            return fh.read()
    if kind == "int":
        return int(rest)
    raise ValueError("unknown data kind: %s" % kind)


def options(fields):
    opts = {}
    for f in fields:
        key, _, value = f.partition("=")
        if key in ("columns", "security_level", "scale", "ratio", "padding"):
            opts[key] = int(value)
        else:
            opts[key] = unescape(value)
    return opts


def fn_name(fn):
    return {compact_text: "text", compact_bytes: "byte",
            compact_numbers: "numeric"}[fn]


def words(ws):
    return " ".join(str(w) for w in ws) if ws else "-"


def grid(codes):
    width, height = rendering.barcode_size(codes)
    rows = [["."] * width for _ in range(height)]
    for x, y in rendering.modules(codes):
        rows[y][x] = "#"
    return ["".join(r) for r in rows]


# ------------------------------------------------------------- commands

def cmd_encode(f):
    data = data_of(f[0])
    opts = options(f[1:])
    codes = encode(data, **opts)
    cols = opts.get("columns", 6)
    level = opts.get("security_level", 2)
    high = enc.encode_high(to_bytes(data, opts.get("encoding", "utf-8")),
                           cols, level)
    out("high %d: %s" % (len(high), words(high)))
    out("rows %d cols %d size %dx%d" % (
        len(codes), len(codes[0]) - 4, *rendering.barcode_size(codes)))
    for row in codes:
        out(" ".join("%05x" % w for w in row))


def cmd_grid(f):
    codes = encode(data_of(f[0]), **options(f[1:]))
    for line in grid(codes):
        out(line)


def cmd_compact(f):
    data = to_bytes(data_of(f[0]))
    chunks = list(_split_to_chunks(data))
    out("split %s" % " ".join(
        "%s:%d" % (fn_name(c.compact_fn), len(c.data)) for c in chunks))
    chunks = list(optimizations.replace_short_numeric_chunks(chunks))
    chunks = list(optimizations.merge_chunks_with_same_compact_fn(chunks))
    out("merged %s" % (" ".join(
        "%s:%d" % (fn_name(c.compact_fn), len(c.data)) for c in chunks)
        or "-"))
    out("words %s" % words(list(compact(data))))


def cmd_text(f):
    data = to_bytes(data_of(f[0]))
    out("interim %s" % words(list(compact_text_interim(data))))
    out("words %s" % words(list(compact_text(data))))


def cmd_numeric(f):
    out("words %s" % words(list(compact_numbers(to_bytes(data_of(f[0]))))))


def cmd_bytes(f):
    out("words %s" % words(list(compact_bytes(to_bytes(data_of(f[0]))))))


def cmd_ec(f):
    data = [int(x) for x in f[0].split(",")] if f[0] != "-" else []
    level = int(f[1])
    out("ec %s" % words(compute_error_correction_code_words(data, level)))


def cmd_base(f):
    digits = [int(x) for x in f[0].split(",")] if f[0] != "-" else []
    out(words(switch_base(digits, int(f[1]), int(f[2]))))


def cmd_rowwords(f):
    rows, cols, level = int(f[0]), int(f[1]), int(f[2])
    for row in range(rows):
        left = enc.get_left_code_word(row, rows, cols, level)
        right = enc.get_right_code_word(row, rows, cols, level)
        out("%d %d %d" % (row, left, right))


def cmd_color(f):
    rgb = rendering.parse_color(unescape(f[0]))
    out("%s %s" % (",".join(str(v) for v in rgb),
                   rendering.rgb_to_hex(rgb)))


def cmd_svg(f):
    name = f[0]
    data = data_of(f[1])
    enc_opts, svg_opts = {}, {}
    for key, value in options(f[2:]).items():
        if key in ("scale", "ratio", "color", "description"):
            svg_opts[key] = value
        else:
            enc_opts[key] = value
    codes = encode(data, **enc_opts)
    tree = render_svg(codes, **svg_opts)
    path = os.path.join("data", "out", name)
    tree.write(path)
    with open(path, "rb") as fh:
        body = fh.read()
    root = tree.getroot()
    rects = len(root.find("g"))
    out("%s %s x %s, %d rects, %d bytes, crc32 %08x" % (
        name, root.get("width"), root.get("height"), rects, len(body),
        zlib.crc32(body)))
    out(body[:body.index(b'<rect')].decode("ascii"))


def cmd_image(f):
    name = f[0]
    data = data_of(f[1])
    enc_opts, img_opts = {}, {}
    for key, value in options(f[2:]).items():
        if key in ("scale", "ratio", "padding", "fg_color", "bg_color"):
            img_opts[key] = value
        else:
            enc_opts[key] = value
    codes = encode(data, **enc_opts)
    image = render_image(codes, **img_opts)
    path = os.path.join("data", "out", name)
    image.save(path, format="PPM")
    with open(path, "rb") as fh:
        body = fh.read()
    w, h = image.size
    px = image.load()
    out("%s %dx%d, %d bytes, crc32 %08x, corner %s, first module %s" % (
        name, w, h, len(body), zlib.crc32(body),
        ",".join(str(v) for v in px[0, 0]),
        ",".join(str(v) for v in px[
            img_opts.get("padding", 20), img_opts.get("padding", 20)])))


COMMANDS = {
    "encode": cmd_encode, "grid": cmd_grid, "compact": cmd_compact,
    "text": cmd_text, "numeric": cmd_numeric, "bytes": cmd_bytes,
    "ec": cmd_ec, "base": cmd_base, "rowwords": cmd_rowwords,
    "color": cmd_color, "svg": cmd_svg, "image": cmd_image,
}


def main():
    with open("data/jobs.tsv", encoding="utf-8") as fh:
        jobs = [ln.rstrip("\n") for ln in fh if ln.strip()]
    for line in jobs:
        if line.startswith("#"):
            print(line)
            continue
        print("> " + line.replace("\t", " "))
        f = line.split("\t")
        try:
            COMMANDS[f[0]](f[1:])
        except Exception as e:  # noqa: BLE001
            print("  error %s: %s" % (type(e).__name__, e))


main()
