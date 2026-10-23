#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored geographiclib and writes
expected.out. A single call prints "<op>(<args>) => <repr of result>", or
"<ExceptionType>: <message>" when it raises. A line, poly or acc job prints
"<op>(<args>):" and then one indented line per call it makes on the object.
Run: python3 -I -B oracle.py > expected.out"""
import sys

sys.path.insert(0, "vendor")
from geographiclib.accumulator import Accumulator  # noqa: E402
from geographiclib.geodesic import Geodesic  # noqa: E402


def mask(s):
    m = 0
    for name in s.split("|"):
        m |= getattr(Geodesic, name)
    return m


def flag(s):
    return s == "True"


def geod(s):
    a, f = s.split(",")
    return Geodesic(float(a), float(f))


def attrs(line):
    return repr({"lat1": line.lat1, "lon1": line.lon1, "azi1": line.azi1,
                 "salp1": line.salp1, "calp1": line.calp1,
                 "a13": line.a13, "s13": line.s13, "caps": line.caps})


def run_line(f, out):
    g = geod(f[1])
    kind = f[2]
    p = [float(x) for x in f[3:6]]
    caps = mask(f[7])
    if kind == "Line":
        line = g.Line(p[0], p[1], p[2], caps)
    else:
        p.append(float(f[6]))
        line = getattr(g, kind)(p[0], p[1], p[2], p[3], caps)
    for op in f[8].split(";"):
        a = op.split(":")
        if a[0] == "attrs":
            out.append("  attrs => " + attrs(line))
        elif a[0] == "pos":
            out.append("  Position(%s, %s) => %r" % (a[1], a[2], line.Position(float(a[1]), mask(a[2]))))
        elif a[0] == "half":
            out.append("  Position(0.5 * s13, %s) => %r" % (a[1], line.Position(0.5 * line.s13, mask(a[1]))))
        elif a[0] == "arcpos":
            out.append("  ArcPosition(%s, %s) => %r" % (a[1], a[2], line.ArcPosition(float(a[1]), mask(a[2]))))
        elif a[0] == "setd":
            line.SetDistance(float(a[1]))
            out.append("  SetDistance(%s)" % a[1])
        elif a[0] == "seta":
            line.SetArc(float(a[1]))
            out.append("  SetArc(%s)" % a[1])


def run_poly(f, out):
    p = geod(f[1]).Polygon(flag(f[2]))
    for op in f[3].split(";"):
        a = op.split(":")
        if a[0] == "pt":
            p.AddPoint(float(a[1]), float(a[2]))
            out.append("  AddPoint(%s, %s)" % (a[1], a[2]))
        elif a[0] == "edge":
            p.AddEdge(float(a[1]), float(a[2]))
            out.append("  AddEdge(%s, %s)" % (a[1], a[2]))
        elif a[0] == "compute":
            out.append("  Compute(%s, %s) => %r" % (a[1], a[2], p.Compute(flag(a[1]), flag(a[2]))))
        elif a[0] == "testpt":
            res = p.TestPoint(float(a[1]), float(a[2]), flag(a[3]), flag(a[4]))
            out.append("  TestPoint(%s) => %r" % (", ".join(a[1:]), res))
        elif a[0] == "testedge":
            res = p.TestEdge(float(a[1]), float(a[2]), flag(a[3]), flag(a[4]))
            out.append("  TestEdge(%s) => %r" % (", ".join(a[1:]), res))
        elif a[0] == "clear":
            p.Clear()
            out.append("  Clear()")
        elif a[0] == "num":
            out.append("  num => %r" % ((p.num, p.lat1, p.lon1),))


def run_acc(f, out):
    acc = Accumulator(float(f[1]))
    for op in f[2].split(";"):
        a = op.split(":")
        if a[0] == "add":
            acc.Add(float(a[1]))
            out.append("  Add(%s)" % a[1])
        elif a[0] == "sum":
            out.append("  Sum(%s) => %r" % (a[1], acc.Sum(float(a[1]))))
        elif a[0] == "neg":
            acc.Negate()
            out.append("  Negate()")
        elif a[0] == "rem":
            acc.Remainder(float(a[1]))
            out.append("  Remainder(%s)" % a[1])
        elif a[0] == "set":
            acc.Set(float(a[1]))
            out.append("  Set(%s)" % a[1])


def call(f):
    op = f[0]
    if op == "geod":
        g = Geodesic(float(f[1]), float(f[2]))
        return {"a": g.a, "f": g.f, "area0": g.Polygon().area0}
    g = geod(f[1])
    x = [float(v) for v in f[2:6]]
    if op == "inv":
        return g.Inverse(x[0], x[1], x[2], x[3], mask(f[6]))
    if op == "dir":
        return g.Direct(x[0], x[1], x[2], x[3], mask(f[6]))
    if op == "arc":
        return g.ArcDirect(x[0], x[1], x[2], x[3], mask(f[6]))
    raise SystemExit("unknown op " + op)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if line == "":
        continue
    f = line.split("\t")
    if f[0] in ("line", "poly", "acc"):
        out.append("%s(%s):" % (f[0], ", ".join(f[1:-1])))
        {"line": run_line, "poly": run_poly, "acc": run_acc}[f[0]](f, out)
        continue
    try:
        res = repr(call(f))
    except Exception as e:
        res = "%s: %s" % (type(e).__name__, e)
    out.append("%s(%s) => %s" % (f[0], ", ".join(f[1:]), res))
print("\n".join(out))
