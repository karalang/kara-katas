"""Runs data/jobs.txt through the vendored XlsxWriter 3.2.0 and prints what
the port must print: every call that returned something other than 0 or
None, raised, or warned, then each book's summary and the parts of the file
it wrote, with their sizes and CRC-32s.

Run: python3 -I -B oracle.py > expected.out"""
import datetime as dt
import io
import os
import sys
import warnings
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

import xlsxwriter  # noqa: E402
from xlsxwriter.format import Format  # noqa: E402
from xlsxwriter.worksheet import Worksheet  # noqa: E402


def unpct(s):
    out = bytearray()
    i = 0
    while i < len(s):
        if s[i] == "%":
            out.append(int(s[i + 1:i + 3], 16))
            i += 3
        else:
            out += s[i].encode()
            i += 1
    return out.decode("utf-8")


def parse(toks, i, fmts, url):
    t = toks[i]
    c, rest = t[0], t[1:]
    if c == "N":
        return None, i + 1
    if c == "T":
        return True, i + 1
    if c == "F":
        return False, i + 1
    if c == "i":
        return int(rest), i + 1
    if c == "f":
        return float(rest), i + 1
    if c == "s":
        return unpct(rest), i + 1
    if c == "R":
        n, ch = rest.split(":", 1)
        return unpct(ch) * int(n), i + 1
    if c == "C":
        parts = []
        i += 1
        for _ in range(int(rest)):
            v, i = parse(toks, i, fmts, url)
            parts.append(v)
        return "".join(parts), i
    if c == "@":
        return (url if rest == "u" else fmts[int(rest)]), i + 1
    if c == "d":
        return dt.datetime.strptime(rest, "%Y-%m-%dT%H:%M:%S.%f"), i + 1
    if c == "D":
        return dt.datetime.strptime(rest, "%Y-%m-%d").date(), i + 1
    if c == "t":
        return dt.datetime.strptime(rest, "%H:%M:%S.%f").time(), i + 1
    if c == "x":
        d, s, u = (int(x) for x in rest.split(","))
        return dt.timedelta(days=d, seconds=s, microseconds=u), i + 1
    if c == "L":
        out = []
        i += 1
        for _ in range(int(rest)):
            v, i = parse(toks, i, fmts, url)
            out.append(v)
        return out, i
    if c == "M":
        out = {}
        i += 1
        for _ in range(int(rest)):
            k, i = parse(toks, i, fmts, url)
            v, i = parse(toks, i, fmts, url)
            out[k] = v
        return out, i
    raise ValueError(t)


def show(v):
    if isinstance(v, (Worksheet, Format)):
        return None
    return repr(v)


def run_book(lines):
    head = lines[0].split(" ")
    name = unpct(head[1])
    options, _ = parse(head, 2, [], None)
    options = dict(options)
    options["in_memory"] = True
    bio = io.BytesIO()
    wb = xlsxwriter.Workbook(bio, options)
    fmts = []
    sheets = []
    print("== %s" % name)
    closed_ok = True
    for n, line in enumerate(lines[1:], 1):
        toks = line.split(" ")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            if toks[0] == "close":
                try:
                    wb.close()
                except Exception as e:
                    closed_ok = False
                    print("  %d close raised %s: %s" % (n, type(e).__name__, e))
                for w in caught:
                    print("  %d close warns: %s" % (n, w.message))
                continue
            target, method = toks[0], toks[1]
            args = []
            i = 2
            while i < len(toks):
                v, i = parse(toks, i, fmts, wb.get_default_url_format())
                args.append(v)
            obj = wb if target == "wb" else sheets[int(target[1:])]
            label = "%s.%s" % (target, method)
            try:
                ret = getattr(obj, method)(*args)
            except Exception as e:
                print("  %d %s raised %s: %s" % (n, label, type(e).__name__, e))
                ret = None
            for w in caught:
                print("  %d %s warns: %s" % (n, label, w.message))
            if method == "add_worksheet" and isinstance(ret, Worksheet):
                sheets.append(ret)
            elif method == "add_format" and isinstance(ret, Format):
                fmts.append(ret)
            elif ret is not None and ret != 0:
                print("  %d %s -> %s" % (n, label, show(ret)))
    if not closed_ok:
        print("  no file written")
        return
    data = bio.getvalue()
    zf = zipfile.ZipFile(io.BytesIO(data))
    infos = zf.infolist()
    tables = sum(len(ws.tables) for ws in wb.worksheets())
    print("  %d parts, %d sheets, %d strings (%d uses), %d cell formats, %d tables, %d names"
          % (len(infos), len(wb.worksheets()), wb.str_table.unique_count, wb.str_table.count,
             len(wb.xf_formats), tables, len(wb.defined_names)))
    for info in infos:
        print("  %-40s %7d %08x" % (info.filename, info.file_size, info.CRC))
    dump = os.environ.get("XLSX_DUMP")
    if dump:
        zf.extractall(os.path.join(dump, name))
    bad = zf.testzip()
    print("  read back: %s" % ("crc ok" if bad is None else "bad crc in " + bad))


def main():
    with open(os.path.join(HERE, "data", "jobs.txt")) as f:
        lines = f.read().split("\n")
    book = []
    for line in lines:
        if not line:
            continue
        book.append(line)
        if line == "close":
            run_book(book)
            book = []


main()
