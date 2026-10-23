"""Replay data/jobs.tsv against the vendored geopy 2.4.1.

`point` parses a coordinate string with Point and prints it every way
geopy formats a point; `make`, `seq` and `lonlat` build points from
numbers, strings and sequences; `degrees`, `parse_degrees`, `altitude`
and `units` call the formatting and unit helpers; `dist` and `dest`
measure distances and destinations with geodesic, great_circle or the
Distance base class; `arith` exercises Distance arithmetic and
comparisons. `route`, `nearest` and `fence` are small programs over the
input files: a route's legs and total, the closest cities to a place,
and which delivery stops fall inside a radius. A job that raises prints
`error <class>: <message>`.

geodesic runs on geographiclib 2.1, vendored beside geopy.
"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "vendor"))
warnings.simplefilter("ignore")

from geopy import distance, format as gformat, units  # noqa: E402
from geopy.distance import Distance, great_circle, geodesic, lonlat  # noqa: E402
from geopy.point import Point  # noqa: E402


def out(s):
    print("  " + s)


def unescape(s):
    """Job text uses \\t, \\n, \\\\ and \\uXXXX escapes."""
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


def value(spec):
    """`-` is None, `i:` an int, `f:` a float, `s:` a str."""
    if spec == "-":
        return None
    kind, _, rest = spec.partition(":")
    if kind == "i":
        return int(rest)
    if kind == "f":
        return float(rest)
    return unescape(rest)


def show_point(p):
    out("repr %r" % (p,))
    out("str %s" % p)
    out("unicode %s" % p.format_unicode())
    out("decimal %s" % p.format_decimal())
    out("with altitude %s" % p.format(altitude=True))
    out("altitude " + " ".join(p.format_altitude(u)
                               for u in ["km", "m", "mi", "ft", "nm", "nmi"]))
    out("items %r %r %r" % (p[0], p[1], p[2]))


def point_arg(spec):
    """A job's point: `s:<text>` is a string, else comma-separated floats
    (a tuple)."""
    if spec.startswith("s:"):
        return unescape(spec[2:])
    return tuple(float(x) for x in spec.split(","))


def ellipsoid_arg(text):
    if "," in text:
        return tuple(float(x) for x in text.split(","))
    return text


CLASSES = {"distance": distance.distance, "geodesic": geodesic,
           "great_circle": great_circle, "Distance": Distance}


def build(algo, fields):
    """algo(*points, **kwargs) from a job's fields."""
    args, kwargs = [], {}
    for f in fields:
        if "=" in f and not f.startswith("s:"):
            key, _, v = f.partition("=")
            if key == "ellipsoid":
                kwargs[key] = ellipsoid_arg(v)
            elif key == "override":
                continue
            else:
                kwargs[key] = float(v)
        elif f.startswith("n:"):
            args.append(float(f[2:]))
        else:
            args.append(point_arg(f))
    return CLASSES[algo](*args, **kwargs)


def show_distance(d):
    out("repr %r" % (d,))
    out("str %s" % d)
    out("km %r m %r mi %r ft %r nm %r" % (d.km, d.m, d.mi, d.ft, d.nm))


# ------------------------------------------------------------- commands

def cmd_point(f):
    show_point(Point(unescape(f[0])))


def cmd_make(f):
    p = Point(value(f[0]), value(f[1]), value(f[2]))
    out("repr %r" % (p,))
    out("str %s" % p)
    out("decimal %s" % p.format_decimal())


def cmd_seq(f):
    p = Point([value(x) for x in f])
    out("repr %r" % (p,))


def cmd_lonlat(f):
    p = lonlat(*[float(x) for x in f])
    out("repr %r" % (p,))


SYMBOLS = {"ascii": gformat.ASCII_SYMBOLS, "unicode": gformat.UNICODE_SYMBOLS,
           "latin1": gformat.LATIN1_SYMBOLS, "html": gformat.HTML_SYMBOLS,
           "xml": gformat.XML_SYMBOLS, "abbr": gformat.ABBR_SYMBOLS,
           "default": None}


def cmd_degrees(f):
    out(gformat.format_degrees(float(f[0]), symbols=SYMBOLS[f[1]]))


def cmd_parse_degrees(f):
    direction = None if f[3] == "-" else f[3]
    out("%r" % Point.parse_degrees(f[0], f[1], f[2], direction))


def cmd_altitude(f):
    dist = None if f[0] == "-" else f[0]
    out("%r" % Point.parse_altitude(dist, f[1]))


def cmd_units(f):
    kwargs = {}
    for kv in f[1:]:
        key, _, v = kv.partition("=")
        kwargs[key] = float(v)
    out("%r" % getattr(units, f[0])(**kwargs))


def cmd_dist(f):
    show_distance(build(f[0], f[1:]))


def cmd_dest(f):
    algo, point, bearing = f[0], point_arg(f[1]), float(f[2])
    d = build(algo, f[3:])
    override = [x for x in f[3:] if x.startswith("override=")]
    if override:
        p = d.destination(point, bearing,
                          distance=Distance(float(override[0][9:])))
    else:
        p = d.destination(point, bearing)
    out("repr %r" % (p,))
    out("str %s" % p)


def operand(spec):
    if spec == "-":
        return None
    kind, _, rest = spec.partition(":")
    if kind == "n":
        return float(rest)
    kwargs = {}
    for kv in rest.split(","):
        key, _, v = kv.partition("=")
        if key == "ellipsoid":
            kwargs[key] = v
        else:
            kwargs[key] = float(v)
    return {"d": Distance, "gc": great_circle, "geo": geodesic}[kind](**kwargs)


def shown(x):
    if isinstance(x, Distance):
        return "%s %r" % (type(x).__name__, x)
    return repr(x)


def cmd_arith(f):
    op, a, b = f[0], operand(f[1]), operand(f[2])
    if op == "add":
        r = a + b
    elif op == "sub":
        r = a - b
    elif op == "neg":
        r = -a
    elif op == "mul":
        r = a * b
    elif op == "rmul":
        r = b * a
    elif op == "div":
        r = a / b
    elif op == "floordiv":
        r = a // b
    elif op == "abs":
        r = abs(a)
    elif op == "bool":
        r = bool(a)
    elif op == "eq":
        r = a == b
    elif op == "ne":
        r = a != b
    elif op == "lt":
        r = a < b
    elif op == "le":
        r = a <= b
    elif op == "gt":
        r = a > b
    elif op == "ge":
        r = a >= b
    else:
        show_distance(a)
        return
    out(shown(r))
    if isinstance(r, (great_circle, geodesic)):
        # the result is built afresh, with the class's default model
        out("model %r" % (r.RADIUS if isinstance(r, great_circle)
                           else r.ELLIPSOID,))


def read_lines(name):
    path = os.path.join("data", name)
    if not os.path.exists(path):
        raise OSError("cannot read %s" % name)
    with open(path, encoding="utf-8") as fh:
        return fh.read().split("\n")


def cmd_route(f):
    points = []
    for line in read_lines(f[0]):
        if not line.strip():
            continue
        points.append(Point(line))
    for n, p in enumerate(points):
        out("%d %s" % (n, p.format_decimal()))
    for n in range(len(points) - 1):
        a, b = points[n], points[n + 1]
        out("leg %d-%d geodesic %r great_circle %r" % (
            n, n + 1, geodesic(a, b).km, great_circle(a, b).km))
    total = distance.distance(*points)
    out("total %s (%r mi, %r nm)" % (total, total.miles, total.nautical))
    out("great circle %s" % great_circle(*points))


def cmd_nearest(f):
    query = Point(f[1])
    k = int(f[2])
    found = []
    for line in read_lines(f[0]):
        if not line:
            continue
        name, _, text = line.partition("|")
        try:
            p = Point(text)
        except ValueError as e:
            out("skip %s: %s" % (name, e))
            continue
        found.append((geodesic(query, p).km, name, p))
    found.sort(key=lambda t: t[0])
    out("from %s" % query.format_unicode())
    for km, name, p in found[:k]:
        out("%s %s %r km %r mi" % (name, p.format_decimal(), km,
                                   units.miles(kilometers=km)))


def cmd_fence(f):
    center = Point(f[1])
    radius = float(f[2])
    inside = 0
    for line in read_lines(f[0]):
        if not line:
            continue
        p = Point(line)
        try:
            d = great_circle(center, p)
        except ValueError as e:
            out("%s error ValueError: %s" % (line, e))
            continue
        where = "in" if d <= radius else "out"
        if where == "in":
            inside += 1
        out("%s %s %r m" % (where, p.format_decimal(), d.m))
    out("%d inside %r km of %s" % (inside, radius, center))


COMMANDS = {
    "point": cmd_point, "make": cmd_make, "seq": cmd_seq, "lonlat": cmd_lonlat,
    "degrees": cmd_degrees, "parse_degrees": cmd_parse_degrees,
    "altitude": cmd_altitude, "units": cmd_units, "dist": cmd_dist,
    "dest": cmd_dest, "arith": cmd_arith, "route": cmd_route,
    "nearest": cmd_nearest, "fence": cmd_fence,
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
