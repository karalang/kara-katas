# Runs the jobs in data/jobs.txt through qrcode 8.0 (the copy in qrcode/,
# unchanged) and wrote expected.out. A job reads its payload file as
# bytes, as the `qr` command reads stdin, adds it to a QRCode with the
# job's options and prints what was asked for: the chunks and the version
# and mask chosen (with the penalty of every mask), the ASCII art of
# print_ascii, the matrix of get_matrix, or one of the SVG images.
import io, os, sys, zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.modules["lxml"] = None  # the SVG images use lxml when it is there; the port follows ElementTree
sys.modules["PIL"] = None

import qrcode  # noqa: E402
from qrcode import util  # noqa: E402
import qrcode.image.svg as svg  # noqa: E402
from qrcode.image.styles.moduledrawers import svg as drawers  # noqa: E402

EC = {"L": qrcode.ERROR_CORRECT_L, "M": qrcode.ERROR_CORRECT_M,
      "Q": qrcode.ERROR_CORRECT_Q, "H": qrcode.ERROR_CORRECT_H}
EC_NAME = {v: k for k, v in EC.items()}
MODE_NAME = {util.MODE_NUMBER: "numeric", util.MODE_ALPHA_NUM: "alphanumeric", util.MODE_8BIT_BYTE: "byte"}
SVG_LINES = 12
SVG_WIDTH = 160

FACTORIES = {
    "svg": (svg.SvgImage, None),
    "svg-fragment": (svg.SvgFragmentImage, None),
    "svg-fill": (svg.SvgFillImage, None),
    "svg-circle": (svg.SvgImage, "circle"),
    "svg-path": (svg.SvgPathImage, None),
    "svg-path-fill": (svg.SvgPathFillImage, None),
    "svg-path-circle": (svg.SvgPathImage, "circle"),
}


def crc(data):
    return f"{zlib.crc32(data):08x}"


def info(qr):
    chunks = ", ".join(f"{MODE_NAME[d.mode]} {len(d)}" for d in qr.data_list)
    print(f"  chunks: {chunks or 'none'}")
    n = qr.modules_count
    print(f"  version {qr.version}, error correction {EC_NAME[qr.error_correction]}, {n}x{n}")
    codewords = bytes(qr.data_cache)
    print(f"  codewords: {len(codewords)}, crc32 {crc(codewords)}")
    print(f"  first codewords: {' '.join(f'{b:02x}' for b in codewords[:12])}")
    if qr.mask_pattern is None:
        chosen = qr.best_mask_pattern()
        points = []
        for i in range(8):
            qr.makeImpl(True, i)
            points.append(util.lost_point(qr.modules))
        qr.makeImpl(False, chosen)
        print(f"  mask {chosen}, penalties {' '.join(str(p) for p in points)}")
    else:
        print(f"  mask {qr.mask_pattern} (given)")
    dark = sum(1 for row in qr.modules for m in row if m)
    print(f"  dark modules: {dark} of {n * n}")


def show_svg(label, text):
    data = text.encode("utf-8")
    lines = text.replace("><", ">\n<").split("\n")
    print(f"  -- {label}: {len(data)} bytes, {len(lines)} lines, crc32 {crc(data)}")
    if len(lines) > SVG_LINES:
        lines = lines[:SVG_LINES - 2] + [f"... {len(lines) - SVG_LINES + 1} lines ..."] + lines[-1:]
    for line in lines:
        if len(line) > SVG_WIDTH:
            line = f"{line[:SVG_WIDTH]}... ({len(line)} characters)"
        print(f"   |{line}")


def run_job(name, payload, opts):
    with open(os.path.join("payloads", payload), "rb") as f:
        data = f.read()
    print(f"== {name}: {payload}, {len(data)} bytes")
    kw = {}
    if "ec" in opts:
        kw["error_correction"] = EC[opts["ec"]]
    for key in ("version", "mask", "border", "box"):
        if key in opts:
            kw[{"mask": "mask_pattern", "box": "box_size"}.get(key, key)] = int(opts[key])
    try:
        qr = qrcode.QRCode(**kw)
        if "optimize" in opts:
            qr.add_data(data, optimize=int(opts["optimize"]))
        else:
            qr.add_data(data)
        qr.make(fit=opts.get("fit", "1") == "1")
    except (ValueError, qrcode.exceptions.DataOverflowError) as e:
        print(f"  ! {type(e).__name__}: {e}")
        return
    for out in opts["out"].split("+"):
        if out == "info":
            info(qr)
        elif out in ("ascii", "ascii-invert"):
            buf = io.StringIO()
            qr.print_ascii(out=buf, invert=out == "ascii-invert")
            print(f"  -- {out}")
            for line in buf.getvalue().split("\n")[:-1]:
                print(f"   |{line}")
        elif out == "matrix":
            print("  -- matrix")
            for row in qr.get_matrix():
                print("   |" + "".join("#" if m else "." for m in row))
        else:
            factory, drawer = FACTORIES[out]
            img = qr.make_image(image_factory=factory, module_drawer=drawer)
            buf = io.BytesIO()
            img.save(buf)
            show_svg(out, buf.getvalue().decode("utf-8"))


def main():
    os.chdir(os.path.join(HERE, "data"))
    with open("jobs.txt", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            name, payload, options = (p.strip() for p in line.split("|"))
            opts = dict(w.split("=", 1) for w in options.split())
            run_job(name, payload, opts)


main()
