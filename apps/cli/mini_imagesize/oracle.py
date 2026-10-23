"""Run every job in data/jobs.txt against the vendored imagesize 1.4.1 and
print the results: expected.out.

Run: python3 -I -B oracle.py > expected.out
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import imagesize  # noqa: E402

assert imagesize.__version__ == "1.4.1"
os.chdir(os.path.join(HERE, "data"))


def err(e):
    return "error %s: %s" % (type(e).__name__, e)


def call(fn, path):
    try:
        return True, fn(path)
    except Exception as e:  # the library's own errors, and struct's
        return False, err(e)


def show(r):
    ok, v = r
    return repr(v) if ok else v


def py_round(x):
    return round(x)


def gallery(path):
    with open(path, encoding="utf-8") as f:
        for line in f.read().splitlines():
            name, scale, alt = line.split("\t")
            ok, v = call(imagesize.get, "images/" + name)
            if not ok:
                print("  <!-- %s: %s -->" % (name, v))
                continue
            w, h = v
            if w == -1 or h == -1:
                print("  <!-- %s: unknown size -->" % name)
                continue
            s = int(scale)
            print('  <img src="images/%s" width="%d" height="%d" alt="%s">'
                  % (name, int(w * s / 100), int(h * s / 100), alt))


def thumbs(path):
    with open(path, encoding="utf-8") as f:
        for name in f.read().splitlines():
            ok, v = call(imagesize.get, "images/" + name)
            if not ok:
                print("  %s: %s" % (name, v))
                continue
            w, h = v
            if w <= 0 or h <= 0:
                print("  %s: no size %r" % (name, v))
                continue
            s = min(320 / w, 240 / h, 1.0)
            tw = max(1, py_round(w * s))
            th = max(1, py_round(h * s))
            print("  %s: %rx%r -> %dx%d" % (name, w, h, tw, th))
            ok, d = call(imagesize.getDPI, "images/" + name)
            if not ok:
                print("    dpi: %s" % d)
            elif d[0] > 0 and d[1] > 0 and isinstance(w, int):
                pw = w * 254 // d[0]
                ph = h * 254 // d[1]
                print("    print: %d.%02d x %d.%02d cm at %dx%d dpi"
                      % (pw // 100, pw % 100, ph // 100, ph % 100, d[0], d[1]))
            else:
                print("    dpi: %r" % (d,))


def audit(path):
    with open(path, encoding="utf-8") as f:
        page = f.read()
    for m in re.finditer(r"<img\b([^>]*)>", page):
        attrs = {}
        for k, v in re.findall(r"""(\w+)=("[^"]*"|'[^']*')""", m.group(1)):
            attrs[k] = v[1:-1]
        src = attrs.get("src", "")
        ok, v = call(imagesize.get, src)
        if not ok:
            print("  %s: %s" % (src, v))
            continue
        w, h = v
        if w == -1 or h == -1:
            print("  %s: not an image imagesize knows" % src)
            continue
        aw, ah = py_round(w), py_round(h)
        if "width" not in attrs or "height" not in attrs:
            print("  %s: no width/height attributes, actual %dx%d" % (src, aw, ah))
            continue
        dw, dh = int(attrs["width"]), int(attrs["height"])
        if (dw, dh) == (aw, ah):
            print("  %s: ok %dx%d" % (src, aw, ah))
        else:
            print("  %s: mismatch, declared %dx%d, actual %dx%d" % (src, dw, dh, aw, ah))


def main():
    with open("jobs.txt", encoding="utf-8") as f:
        lines = f.read().splitlines()
    for line in lines:
        if line.startswith("#") or not line:
            print(line)
        elif line.startswith("!"):
            prog, arg = line[1:].split(" ")
            print("> " + line)
            {"gallery": gallery, "thumbs": thumbs, "audit": audit}[prog](arg)
        else:
            print("> " + line)
            print("  get: " + show(call(imagesize.get, line)))
            print("  getDPI: " + show(call(imagesize.getDPI, line)))


main()
