#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py) through the vendored parsedatetime
and prints what each step gives. The clock is the job's: time.localtime()
returns the time the last "now" step set, in UTC. A struct_time prints
as its tuple, everything else as repr() shows it, and an exception as
"error <class>: <message>". The reminders tool writes its files under
data/out/ and prints each one back after "  |".

Run: python3 -I -B oracle.py > expected.out"""
import datetime
import os
import sys
import time
import warnings

os.environ["TZ"] = "UTC"
time.tzset()
warnings.simplefilter("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))
import parsedatetime as pdt  # noqa: E402

DATA = os.path.join(HERE, "data")
CLOCK = [time.struct_time((2026, 1, 1, 0, 0, 0, 3, 1, 0))]
time.localtime = lambda *a: CLOCK[0]


def unesc(t):
    out = []
    k = 0
    while k < len(t):
        c = t[k]
        if c == "\\" and k + 1 < len(t):
            n = t[k + 1]
            out.append({"\\": "\\", "t": "\t", "n": "\n"}.get(n, "\\" + n))
            k += 2
        else:
            out.append(c)
            k += 1
    return "".join(out)


def st(t):
    return repr(tuple(t))


def num(f):
    if f == "-":
        return None
    try:
        return int(f)
    except ValueError:
        try:
            return float(f)
        except ValueError:
            return f


def show_nlp(w, res):
    if res is None:
        w("  -> None\n")
        return
    for dt, flag, a, b, text in res:
        w("  - %r %r %d %d %r\n" % (dt, flag, a, b, text))


def agenda(cal, src, dst):
    with open(os.path.join(DATA, "inbox", src), encoding="utf-8") as f:
        lines = f.read().split("\n")
    out = []
    for no, line in enumerate(lines, 1):
        if not line.strip():
            continue
        res = cal.nlp(line)
        if res is None:
            out.append("%d\t-\t%s\n" % (no, line))
            continue
        for dt, flag, a, b, text in res:
            out.append("%d\t%d-%d\t%s\t%s\t%r\n" % (no, a, b, text, dt.isoformat(" "), flag))
    return out


def todo(cal):
    with open(os.path.join(DATA, "todo.txt"), encoding="utf-8") as f:
        lines = f.read().split("\n")
    due, later = [], []
    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        task, when = [x.strip() for x in line.split("|", 1)]
        t, ctx = cal.parse(when, version=pdt.VERSION_CONTEXT_STYLE)
        if ctx.hasDateOrTime:
            due.append((datetime.datetime(*t[:6]), task, when, ctx))
        else:
            later.append((task, when))
    due.sort(key=lambda e: e[0])
    out = ["%s\t%s\t%s\t%r\n" % (d.isoformat(" "), task, when, ctx) for d, task, when, ctx in due]
    out += ["someday\t%s\t%s\n" % e for e in later]
    return out


def write_out(w, name, lines):
    os.makedirs(os.path.join(DATA, "out"), exist_ok=True)
    path = os.path.join(DATA, "out", name)
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    with open(path, encoding="utf-8") as f:
        text = f.read()
    w("  wrote out/%s (%d lines)\n" % (name, len(lines)))
    for line in text.split("\n")[:-1]:
        w("  | %s\n" % line)


def run(w, cal, f):
    op = f[0]
    if op == "parse":
        text = unesc(f[1])
        if len(f) > 2:
            w("> parse %r version=%s\n" % (text, f[2]))
            t, r = cal.parse(text, version=int(f[2]))
        else:
            w("> parse %r\n" % text)
            t, r = cal.parse(text)
        w("  -> %s %r\n" % (st(t), r))
    elif op == "src":
        text = unesc(f[1])
        src = tuple(int(x) for x in f[2:11])
        w("> parse %r sourceTime=%r\n" % (text, src))
        t, r = cal.parse(text, src)
        w("  -> %s %r\n" % (st(t), r))
    elif op == "dt":
        text = unesc(f[1])
        w("> parseDT %r\n" % text)
        dt, r = cal.parseDT(text)
        w("  -> %r %r\n" % (dt, r))
    elif op == "nlp":
        text = unesc(f[1])
        w("> nlp %r\n" % text)
        show_nlp(w, cal.nlp(text))
    elif op == "range":
        text = unesc(f[1])
        w("> evalRanges %r\n" % text)
        a, b, flag = cal.evalRanges(text)
        w("  -> %s %s %d\n" % (st(a), st(b), flag))
    elif op == "inc":
        args = [int(x) for x in f[1:7]]
        month, year = num(f[7]), num(f[8])
        w("> inc %r month=%r year=%r\n" % (datetime.datetime(*args), month, year))
        w("  -> %r\n" % cal.inc(datetime.datetime(*args), month=month, year=year))
    elif op == "words":
        text = unesc(f[1])
        w("> _convertUnitAsWords %r\n" % text)
        w("  -> %r\n" % cal._convertUnitAsWords(text))
    elif op == "qty":
        text = unesc(f[1])
        w("> _quantityToReal %r\n" % text)
        w("  -> %r\n" % cal._quantityToReal(text))
    elif op == "dow":
        a = [int(x) for x in f[1:6]]
        w("> _CalculateDOWDelta%r\n" % (tuple(a),))
        w("  -> %r\n" % cal._CalculateDOWDelta(*a))
    elif op == "pdate":
        text = unesc(f[1])
        w("> parseDate %r\n" % text)
        w("  -> %s\n" % st(cal.parseDate(text)))
    elif op == "pdtext":
        text = unesc(f[1])
        w("> parseDateText %r\n" % text)
        w("  -> %s\n" % st(cal.parseDateText(text)))
    elif op == "agenda":
        w("> agenda inbox/%s\n" % f[1])
        write_out(w, f[2], agenda(cal, f[1], f[2]))
    elif op == "todo":
        w("> todo todo.txt\n")
        write_out(w, f[1], todo(cal))


def main():
    w = sys.stdout.write
    with open(os.path.join(DATA, "jobs.tsv"), encoding="utf-8") as fh:
        steps = fh.read().split("\n")
    cal = None
    for line in steps:
        if not line:
            continue
        f = line.split("\t")
        op = f[0]
        if op == "job":
            w("== %s\n" % f[1])
        elif op == "now":
            v = [int(x) for x in f[1:7]]
            d = datetime.datetime(*v)
            CLOCK[0] = time.struct_time(tuple(v) + (d.weekday(), d.timetuple().tm_yday, 0))
            w("> now %s\n" % st(CLOCK[0]))
        elif op == "cal":
            locale = None if f[1] == "-" else f[1]
            cal = pdt.Calendar(pdt.Constants(locale), version=int(f[2]))
            w("> Calendar(Constants(%r), version=%s)\n" % (locale, f[2]))
        elif op == "set":
            value = {"True": True, "False": False}.get(f[2])
            if value is None:
                value = int(f[2])
            setattr(cal.ptc, f[1], value)
            w("> ptc.%s = %r\n" % (f[1], value))
        else:
            try:
                run(w, cal, f)
            except Exception as e:
                w("  error %s: %s\n" % (type(e).__name__, e))


main()
