# Runs data/jobs.jsonl and the three programs through python-barcode
# 0.16.1 itself (the copy in barcode/, unchanged) and prints what
# mini_barcode.kara must print.
import contextlib
import csv
import io
import json
import os
import shlex
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(write_through=True)
os.chdir(HERE)
# No Pillow, so ImageWriter is None wherever this runs.
sys.modules["PIL"] = None

import barcode  # noqa: E402
from barcode import pybarcode  # noqa: E402
from barcode.ean import EuropeanArticleNumber14  # noqa: E402

assert barcode.__file__.startswith(HERE), barcode.__file__


def err(e):
    return f"{type(e).__name__}: {e}"


def gs1_check(digits):
    """The GS1 check digit, as EAN-14 computes it."""
    return EuropeanArticleNumber14.calculate_checksum(None, digits)


def svg_lines(out):
    text = out.decode("utf-8")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def is_bar(line):
    return line.startswith("        <rect x=")


def print_svg(lines, mode, indent):
    if mode == "full":
        for line in lines:
            print(indent + line)
        return
    bars = [x for x in lines if is_bar(x)]
    done = False
    for line in lines:
        if not is_bar(line):
            print(indent + line)
        elif not done:
            done = True
            print(indent + bars[0])
            if len(bars) > 2:
                print(f"{indent}        ({len(bars) - 2} more bars)")
            if len(bars) > 1:
                print(indent + bars[-1])


def file_size(path):
    return os.path.getsize(path)


def svg_tag(path):
    for line in svg_lines(open(path, "rb").read()):
        if line.startswith("<svg "):
            return line
    return "?"


def attr(tag, name):
    i = tag.find(f' {name}="')
    if i < 0:
        return "?"
    j = tag.find('"', i + len(name) + 3)
    return tag[i + len(name) + 3:j]


# ------------------------------------------------------------- jobs

SHOW = {
    "repr": lambda b: ("repr(b)", repr(b)),
    "str": lambda b: ("str(b)", repr(str(b))),
    "full": lambda b: ("b.get_fullcode()", repr(b.get_fullcode())),
    "build": lambda b: ("b.build()", repr(b.build())),
    "ascii": lambda b: ("b.to_ascii()", repr(b.to_ascii())),
    "encoded": lambda b: ("b.encoded", repr(b.encoded)),
    "checksum": lambda b: ("b.calculate_checksum()", repr(b.calculate_checksum())),
}
LABEL = {
    "repr": "repr(b)", "str": "str(b)", "full": "b.get_fullcode()", "build": "b.build()",
    "ascii": "b.to_ascii()", "encoded": "b.encoded", "checksum": "b.calculate_checksum()",
}


def call_text(args):
    return ", ".join(repr(a) for a in args)


def run_cli(argv):
    print(f"  $ {shlex.join(['python-barcode'] + argv)}")
    sys.argv = ["python-barcode"] + argv
    out, errs = io.StringIO(), io.StringIO()
    code = 0
    raised = None
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(errs):
        try:
            pybarcode.main()
        except SystemExit as e:
            code = e.code
        except Exception as e:
            raised = e
    for stream, mark in ((out, "|"), (errs, "!")):
        text = stream.getvalue().replace(HERE + os.sep, "./")
        for line in text.split("\n")[:-1] if text else []:
            print(f"  {mark} {line}".rstrip())
    if raised is not None:
        print(f"  raised {err(raised)}")
    else:
        print(f"  exit {code}")


def step(st, env):
    op = st[0]
    if op == "new":
        _, var, kind, code, kw = st
        shown = call_text([kind, code]) + (f", options={kw!r}" if kw else "")
        try:
            env[var] = barcode.get(kind, code, options=kw)
            print(f"  {var} = get({shown}) = {env[var]!r}")
        except Exception as e:
            env.pop(var, None)
            print(f"  {var} = get({shown}) raised {err(e)}")
    elif op == "show":
        var = st[1]
        for what in st[2:]:
            label = LABEL[what].replace("b", var, 1) if what != "repr" else f"repr({var})"
            if var not in env:
                print(f"  {label}: {var} was not made")
                continue
            try:
                _, text = SHOW[what](env[var])
                print(f"  {label} = {text}")
            except Exception as e:
                print(f"  {label} raised {err(e)}")
    elif op == "render":
        _, var, opts, text, mode = st
        print(f"  {var}.render({opts!r}, {text!r}):")
        if var not in env:
            print(f"    {var} was not made")
            return
        try:
            out = env[var].render(opts, text)
        except Exception as e:
            print(f"    raised {err(e)}")
            return
        print_svg(svg_lines(out), mode, "    ")
    elif op == "save":
        _, var, name, opts, text = st
        if var not in env:
            print(f"  {var}.save: {var} was not made")
            return
        try:
            path = env[var].save(name, opts, text)
            print(f"  {var}.save({name!r}, {opts!r}, {text!r}) -> {path!r} ({file_size(path)} bytes)")
        except Exception as e:
            print(f"  {var}.save({name!r}, {opts!r}, {text!r}) raised {err(e)}")
    elif op == "generate":
        _, kind, code, output, opts, text = st
        shown = f"generate({kind!r}, {code!r}, output={output!r}, writer_options={opts!r}, text={text!r})"
        try:
            path = barcode.generate(kind, code, output=output, writer_options=opts, text=text)
            print(f"  {shown} -> {path!r} ({file_size(path)} bytes)")
        except Exception as e:
            print(f"  {shown} raised {err(e)}")
    elif op == "cli":
        run_cli(st[1])


def run_jobs():
    os.makedirs("data/out/jobs", exist_ok=True)
    os.makedirs("data/out/cli/sub", exist_ok=True)
    with open("data/jobs.jsonl", encoding="utf-8") as f:
        for line in f:
            j = json.loads(line)
            print(f"== {j['name']}")
            env = {}
            for st in j["steps"]:
                step(st, env)


# ------------------------------------------------------------- programs

LABEL_OPTIONS = {"module_height": 10, "font_size": 8, "text_distance": 3, "quiet_zone": 2}


def labels():
    print("== program: shelf labels")
    os.makedirs("data/out/labels", exist_ok=True)
    rows = []
    rejects = []
    with open("data/products.csv", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            sku = row["sku"]
            digits = row["code"].replace(" ", "").replace("-", "")
            if digits == "":
                kind, code = "code128", sku
                print(f"{sku}: no code, labelled with the SKU")
            else:
                kind = {8: "ean8", 12: "upca", 13: "ean13", 14: "itf"}.get(len(digits))
                code = digits
                if kind is None:
                    print(f"{sku}: rejected, a code of {len(digits)} digits")
                    rejects.append(sku)
                    continue
            try:
                b = barcode.get(kind, code)
                if kind == "itf":
                    full = digits[:13] + str(gs1_check(digits[:13]))
                else:
                    full = b.get_fullcode()
            except Exception as e:
                print(f"{sku}: rejected, {err(e)}")
                rejects.append(sku)
                continue
            if digits and full[-1] != digits[-1]:
                print(f"{sku}: rejected, check digit {digits[-1]} should be {full[-1]}")
                rejects.append(sku)
                continue
            path = b.save(f"data/out/labels/{sku}", LABEL_OPTIONS)
            tag = svg_tag(path)
            print(f"{sku}: {b.name} {full} -> {path}")
            rows.append((sku, path, attr(tag, "width"), attr(tag, "height"), file_size(path)))
    with open("data/out/labels/index.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["sku", "file", "width", "height", "bytes"])
        for r in rows:
            w.writerow(r)
    print("-- data/out/labels/index.csv")
    print(open("data/out/labels/index.csv", encoding="utf-8").read(), end="")
    print(f"{len(rows)} labels, {len(rejects)} rejected: {', '.join(rejects)}")
    print("-- data/out/labels/CHO-100.svg")
    print_svg(svg_lines(open("data/out/labels/CHO-100.svg", "rb").read()), "full", "")


def valid_date(d):
    return len(d) == 6 and d.isdigit() and 1 <= int(d[2:4]) <= 12 and 1 <= int(d[4:6]) <= 31


def shipping():
    print("== program: shipping labels")
    os.makedirs("data/out/shipping", exist_ok=True)
    first = None
    with open("data/shipments.jsonl", encoding="utf-8") as f:
        for line in f:
            s = json.loads(line)
            sid = s["id"]
            problems = []
            fixed = []
            variable = []
            if s["sscc"] is not None:
                if len(s["sscc"]) != 17:
                    problems.append("SSCC must have 17 digits before its check digit")
                else:
                    fixed.append(("00", s["sscc"] + str(gs1_check(s["sscc"]))))
            if len(s["gtin"]) != 13:
                problems.append("GTIN must have 13 digits before its check digit")
            else:
                fixed.append(("01", s["gtin"] + str(gs1_check(s["gtin"]))))
            if s["expiry"] is not None:
                if not valid_date(s["expiry"]):
                    problems.append(f"bad expiry date {s['expiry']}")
                else:
                    fixed.append(("17", s["expiry"]))
            variable.append(("10", s["batch"]))
            if s.get("serial"):
                variable.append(("21", s["serial"]))
            if s["count"] is not None:
                variable.append(("37", str(s["count"])))
            if problems:
                print(f"{sid}: not labelled: {'; '.join(problems)}")
                continue
            elements = fixed + variable
            code = ""
            for i, (ai, val) in enumerate(elements):
                code += ai + val
                if (ai, val) in variable and i + 1 < len(elements):
                    code += "\xf1"
            hri = "".join(f"({ai}){val}" for ai, val in elements)
            b = barcode.get("gs1_128", code)
            values = b.encoded
            print(f"{sid}: {hri}")
            print(f"  symbol values {values}, {len(values)} symbols")
            path = b.save(f"data/out/shipping/{sid}", {"module_height": 12, "font_size": 6}, hri)
            print(f"  {path}: {attr(svg_tag(path), 'width')} wide, {file_size(path)} bytes")
            gtin14 = dict(fixed)["01"]
            itf = barcode.get("itf", gtin14)
            ipath = itf.save(f"data/out/shipping/{sid}-itf", {"module_height": 12})
            print(f"  {ipath}: ITF-14 {itf.get_fullcode()}, {attr(svg_tag(ipath), 'width')} wide, "
                  f"{file_size(ipath)} bytes")
            if first is None:
                first = path
    print(f"-- {first}")
    print_svg(svg_lines(open(first, "rb").read()), "brief", "")


def library():
    print("== program: library catalogue")
    os.makedirs("data/out/spines", exist_ok=True)
    entries = []
    with open("data/books.txt", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            kind, number, title = line.split(None, 2)
            digits = number.replace("-", "").upper()
            try:
                b = barcode.get(kind, number)
            except Exception as e:
                print(f"{title}: {kind} {number} refused: {err(e)}")
                continue
            note = ""
            if str(b) != digits:
                note = f" (check digit should make it {str(b)})"
            ean = b.get_fullcode()
            print(f"{title}: {kind} {number} -> {b.name} {str(b)}, EAN {ean}{note}")
            if len(ean) != 13:
                # ISBN-10 and ISSN keep their own digit count when they
                # build the EAN, so ask EAN-13 for the whole one.
                if kind == "isbn10":
                    ean = barcode.get("isbn13", "978" + str(b)[:9]).get_fullcode()
                else:
                    ean = barcode.get("ean13", b.make_ean()).get_fullcode()
                print(f"  that EAN is cut short; the whole one is {ean}")
            spine = barcode.get("ean13-guard", ean)
            path = spine.save(f"data/out/spines/{ean}", {"module_height": 10, "font_size": 6})
            entries.append((ean, kind, str(b), title, path))
    entries.sort()
    with open("data/out/catalog.tsv", "w", encoding="utf-8") as f:
        for ean, kind, number, title, path in entries:
            f.write(f"{ean}\t{kind}\t{number}\t{title}\t{path}\n")
    print("-- data/out/catalog.tsv")
    print(open("data/out/catalog.tsv", encoding="utf-8").read(), end="")
    for name in sorted(os.listdir("data/out/spines")):
        p = f"data/out/spines/{name}"
        print(f"{p}: {svg_tag(p)}")


shutil.rmtree("data/out", ignore_errors=True)
run_jobs()
labels()
shipping()
library()
