# Runs data/jobs.txt through the copy of pyshp 2.3.1 in shapefile.py and
# prints what it does; expected.out is this program's output.
#
# The Writer stamps each .dbf header with time.localtime(), so the
# oracle gives shapefile a clock that always reads 2026-10-21;
# mini_shapefile.kara writes the same date.
import json
import math
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import shapefile  # noqa: E402


class _Time:
    @staticmethod
    def localtime():
        return (2026, 10, 21, 8, 0, 0, 2, 294, 0)


shapefile.time = _Time


def err(e):
    return "! %s: %r" % (type(e).__name__, str(e))


def path(name):
    return os.path.join("data", name)


# ------------------------------------------------------------ layer scripts

TYPES = {name: code for code, name in shapefile.SHAPETYPE_LOOKUP.items()}


def num(v):
    return None if v == "-" else float(v)


def point(text):
    return [num(v) for v in text.split(",")]


def part(text):
    return [point(p) for p in text.split()]


def parts(text):
    return [part(p) for p in text.split("|")] if text.strip() else []


def value(text):
    text = text.strip()
    if text == "n":
        return None
    if text == "e":
        return ""
    kind, _, v = text.partition(":")
    if kind == "i":
        return int(v)
    if kind == "f":
        return float(v)
    if kind == "s":
        return v
    if kind == "b":
        return v == "T"
    if kind == "d":
        y, m, d = v.split("-")
        return shapefile.date(int(y), int(m), int(d))
    if kind == "l":
        return [int(x) for x in v.split(",")]
    raise ValueError("bad value " + text)


def geo(rest):
    kind, _, coords = rest.partition(" ")
    if kind == "Point":
        c = point(coords)
    elif kind in ("MultiPoint", "LineString"):
        c = part(coords)
    elif kind in ("MultiLineString", "Polygon"):
        c = parts(coords)
    else:
        c = [parts(p) for p in coords.split(";")]
    return {"type": kind, "coordinates": c}


def step(w, name, cmd, rest):
    if cmd == "writer":
        words = rest.split()
        st = None if words[0] == "-" else TYPES[words[0]]
        return shapefile.Writer(path("out/" + name), shapeType=st, autoBalance="autobalance" in words)
    if cmd == "autobalance":
        w.autoBalance = True
    elif cmd == "field":
        n, t, size, deci = rest.split()
        w.field(n, t, int(size), int(deci))
    elif cmd == "point":
        x, y = rest.split()
        w.point(float(x), float(y))
    elif cmd == "pointm":
        x, y, m = rest.split()
        w.pointm(float(x), float(y), num(m))
    elif cmd == "pointz":
        x, y, z, m = rest.split()
        w.pointz(float(x), float(y), float(z), num(m))
    elif cmd in ("multipoint", "multipointm", "multipointz"):
        getattr(w, cmd)(part(rest))
    elif cmd in ("line", "linem", "linez", "poly", "polym", "polyz"):
        getattr(w, cmd)(parts(rest))
    elif cmd == "multipatch":
        types, _, ps = rest.partition(" ")
        w.multipatch(parts(ps), partTypes=[int(t) for t in types.split(",")])
    elif cmd == "null":
        w.null()
    elif cmd == "geo":
        w.shape(geo(rest))
    elif cmd == "record":
        if rest.strip():
            w.record(*[value(v) for v in rest.split(";")])
        else:
            w.record()
    elif cmd == "recordkw":
        kw = {}
        for item in rest.split(";"):
            k, _, v = item.strip().partition("=")
            kw[k] = value(v)
        w.record(**kw)
    elif cmd == "balance":
        w.balance()
    elif cmd == "close":
        w.close()
        print("  closed")
    return w


def job_write(name):
    with open(path(name + ".layer"), encoding="utf-8") as f:
        lines = f.read().split("\n")
    w = None
    for ln, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cmd, _, rest = line.partition(" ")
        try:
            w = step(w, name, cmd, rest)
        except Exception as e:
            print("  line %d %s %s" % (ln, cmd, err(e)))
    if w is None:
        return
    for f in (w.shp, w.shx, w.dbf):
        if f and not f.closed:
            f.flush()
    print("  len %d shapeType %r bbox %r zbox %r mbox %r" % (len(w), w.shapeType, w.bbox(), w.zbox(), w.mbox()))
    for ext in ("shp", "shx", "dbf"):
        with open(path("out/%s.%s" % (name, ext)), "rb") as f:
            data = f.read()
        print("  %s %d bytes adler32 %08x" % (ext, len(data), zlib.adler32(data)))


# ------------------------------------------------------------ reading


def reader(name, mode):
    if mode == "replace":
        return shapefile.Reader(path(name), encodingErrors="replace")
    return shapefile.Reader(path(name))


def show(s):
    print("  %r" % s)
    for attr in ("bbox", "parts", "partTypes", "points", "z", "m"):
        if hasattr(s, attr):
            print("    %s %r" % (attr, getattr(s, attr)))


def job_info(r):
    for line in str(r).split("\n"):
        print("  " + line)
    if r.shp:
        print("  type %s (%d) bbox %r zbox %r mbox %r" % (r.shapeTypeName, r.shapeType, r.bbox, r.zbox, r.mbox))
    print("  len %d numRecords %r numShapes %r" % (len(r), r.numRecords, r.numShapes))
    if r.dbf:
        print("  fields %r" % r.fields)


def job_shapes(r):
    for s in r.iterShapes():
        show(s)


def job_records(r, fields=None):
    for rec in r.records(fields=fields):
        print("  %r" % rec)


def job_get(r, i, keys):
    rec = r.record(i)
    print("  %r" % rec)
    for k in keys:
        try:
            if k.startswith("."):
                v = getattr(rec, k[1:])
            elif k.lstrip("-").isdigit():
                v = rec[int(k)]
            else:
                v = rec[k]
            print("  %s = %r" % (k, v))
        except Exception as e:
            print("  %s %s" % (k, err(e)))


def bbox_arg(text):
    return [float(v) for v in text.split(",")]


def job_bbox(r, bb):
    print("  shapes %r" % [s.oid for s in r.shapes(bbox=bb)])
    for sr in r.shapeRecords(bbox=bb):
        print("  %r %r" % (sr.shape, sr.record))


def job_iter(r):
    for sr in r:
        print("  %r | %r" % (sr.shape, sr.record))


def job_geojson(r):
    g = r.__geo_interface__
    print("  %s bbox %s" % (g["type"], json.dumps(g["bbox"])))
    for feat in g["features"]:
        print("  " + json.dumps(feat))


def job_extract(src, dst, bb):
    r = shapefile.Reader(path(src))
    w = shapefile.Writer(path(dst), shapeType=r.shapeType)
    for f in r.fields[1:]:
        w.field(*f)
    n = 0
    for sr in r.iterShapeRecords(bbox=bb):
        w.shape(sr.shape)
        w.record(*sr.record)
        n += 1
    w.close()
    print("  extracted %d of %d" % (n, len(r)))


# ------------------------------------------------------------ the county report


def rings_of(shape):
    g = shape.__geo_interface__
    if g["type"] == "Polygon":
        return [g["coordinates"]]
    return g["coordinates"]


def poly_area(poly):
    a = abs(shapefile.signed_area(poly[0]))
    for hole in poly[1:]:
        a -= abs(shapefile.signed_area(hole))
    return a


def inside(polys, p):
    for poly in polys:
        if shapefile.ring_contains_point(poly[0], p) and not any(
            shapefile.ring_contains_point(h, p) for h in poly[1:]
        ):
            return True
    return False


def seg_length(pts):
    total = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        total += math.sqrt((x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0))
    return total


def job_report():
    parcels = shapefile.Reader(path("out/parcels"))
    wells = shapefile.Reader(path("out/wells"))
    roads = shapefile.Reader(path("out/roads"))
    sensors = shapefile.Reader(path("out/sensors"))
    print("parcels")
    plots = []
    total = 0.0
    for sr in parcels.iterShapeRecords():
        polys = rings_of(sr.shape)
        area = sum(poly_area(p) for p in polys)
        total += area
        holes = sum(len(p) - 1 for p in polys)
        rec = sr.record
        stated = rec.AREA_HA
        if stated is None:
            check = "no stated area"
        elif abs(stated - area / 10000.0) > 0.05:
            check = "MISMATCH stated %.3f" % stated
        else:
            check = "ok"
        print("  %-8s %-24s polys=%d holes=%d area=%.1f m2 (%.3f ha) %s" % (
            rec.PARCEL_ID, rec.OWNER, len(polys), holes, area, area / 10000.0, check))
        plots.append((rec.PARCEL_ID, polys, sr.shape.bbox))
    print("  total %.1f m2" % total)
    print("wells")
    for sr in wells.iterShapeRecords():
        x, y = sr.shape.points[0]
        where = [pid for pid, polys, _ in plots if inside(polys, (x, y))]
        rec = sr.record
        print("  %s at (%s, %s) z=%r depth=%r drilled=%r in %s" % (
            rec.WELL, x, y, sr.shape.z[0], rec.DEPTH_M, rec.DRILLED, ",".join(where) or "no parcel"))
    print("roads")
    for sr in roads.iterShapeRecords():
        s = sr.shape
        bounds = list(s.parts) + [len(s.points)]
        length = sum(seg_length(s.points[a:b]) for a, b in zip(bounds, bounds[1:]))
        ms = [m for m in s.m if m is not None]
        mr = "%r..%r" % (min(ms), max(ms)) if ms else "-"
        print("  %-6s %-20s lanes=%r parts=%d length=%.2f m=%s" % (
            sr.record.ROAD, sr.record.NAME, sr.record.LANES, len(s.parts), length, mr))
    print("sensors")
    for pid, polys, bb in plots:
        near = sensors.shapes(bbox=list(bb))
        probes = 0
        for s in near:
            probes += sum(1 for p in s.points if inside(polys, p))
        print("  %s clusters %r probes inside %d" % (pid, [s.oid for s in near], probes))


# ------------------------------------------------------------ main


def run_job(w):
    k = w[0]
    if k == "write":
        job_write(w[1])
    elif k == "report":
        job_report()
    elif k == "extract":
        job_extract(w[1], w[2], bbox_arg(w[3]))
    else:
        r = reader(w[1], "replace" if "replace" in w[2:] else None)
        if k == "info":
            job_info(r)
        elif k == "shapes":
            job_shapes(r)
        elif k == "records":
            job_records(r)
        elif k == "fields":
            job_records(r, w[2].split(","))
        elif k == "get":
            job_get(r, int(w[2]), w[3:])
        elif k == "shape":
            show(r.shape(int(w[2])))
        elif k == "bbox":
            job_bbox(r, bbox_arg(w[2]))
        elif k == "iter":
            job_iter(r)
        elif k == "geojson":
            job_geojson(r)


def main():
    os.makedirs(path("out"), exist_ok=True)
    with open(path("jobs.txt")) as f:
        jobs = f.read().split("\n")[:-1]
    for line in jobs:
        print("== " + line)
        try:
            run_job(line.split(" "))
        except Exception as e:
            print(err(e))


main()
