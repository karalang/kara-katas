"""Replay data/jobs.tsv against the vendored s2sphere 0.2.5.

Each job is a tab-separated command: cell ids and tokens, navigation,
lat/lng and point math, caps, rects, cells, region coverings, cell
unions, metrics, and a small place index (data/places.tsv) queried by
radius and by zone. A job that raises prints `error <class>: <message>`.
"""
import math
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# s2sphere 0.2.5 imports int and range from the `future` package, which on
# Python 3 are the builtins; this stands in for it.
_future = types.ModuleType("future")
_future_builtins = types.ModuleType("future.builtins")
_future_builtins.int = int
_future_builtins.range = range
_future.builtins = _future_builtins
sys.modules["future"] = _future
sys.modules["future.builtins"] = _future_builtins
sys.path.insert(0, os.path.join(HERE, "vendor"))

import s2sphere as s2  # noqa: E402
from s2sphere.sphere import drem  # noqa: E402


def r(x):
    return repr(float(x))


def ll(p):
    return "%s, %s" % (r(p.lat().degrees), r(p.lng().degrees))


def pt(p):
    return "(%s, %s, %s)" % (r(p[0]), r(p[1]), r(p[2]))


def out(s):
    print("  " + s)


def tf(b):
    return "True" if b else "False"


def tok(c):
    return c.to_token()


def toks(cs):
    return " ".join(c.to_token() for c in cs) if cs else "-"


def latlng(a, b):
    return s2.LatLng.from_degrees(float(a), float(b))


def cell_id(t):
    return s2.CellId.from_token(t)


def interval(name, i):
    return "%s [%s, %s]" % (name, r(i.lo()), r(i.hi()))


def rect_str(x):
    if x.is_empty():
        return "empty"
    return "lat [%s, %s] lng [%s, %s]" % (
        r(math.degrees(x.lat().lo())), r(math.degrees(x.lat().hi())),
        r(math.degrees(x.lng().lo())), r(math.degrees(x.lng().hi())))


def cap_str(c):
    if c.is_empty():
        return "empty"
    return "axis %s height %s" % (pt(c.axis()), r(c.height()))


# ------------------------------------------------------------- regions

def region(f):
    """`cap LAT LNG DEG`, `rect LAT LNG LAT LNG` or `cell TOKEN`; returns
    the region and the number of fields it used."""
    kind = f[0]
    if kind == "cap":
        axis = latlng(f[1], f[2]).to_point()
        angle = s2.Angle.from_degrees(float(f[3]))
        return s2.Cap.from_axis_angle(axis, angle), 4
    if kind == "rect":
        return s2.LatLngRect.from_point_pair(latlng(f[1], f[2]),
                                            latlng(f[3], f[4])), 5
    if kind == "cell":
        return s2.Cell(cell_id(f[1])), 2
    raise ValueError("unknown region kind: %s" % kind)


def load_places():
    places = []
    with open("data/places.tsv", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            name, lat, lng = line.split("\t")
            places.append((name, float(lat), float(lng)))
    return places


def load_zones():
    zones = {}
    with open("data/zones.tsv", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            name, rest = line.split("\t", 1)
            zones[name] = rest.split("\t")
    return zones


EARTH_KM = 6371.0088


# ------------------------------------------------------------- commands

def cmd_cell(f):
    c = s2.CellId.from_lat_lng(latlng(f[0], f[1]))
    if len(f) > 2:
        c = c.parent(int(f[2]))
    out("%r" % c)
    out("token %s face %d level %d leaf %s" % (tok(c), c.face(), c.level(),
                                             tf(c.is_leaf())))
    out("center %s" % ll(c.to_lat_lng()))
    cell = s2.Cell(c)
    out("orientation %d" % cell.orientation())
    for k in range(4):
        out("vertex %d %s" % (k, ll(s2.LatLng.from_point(cell.get_vertex(k)))))
    out("rect %s" % rect_str(cell.get_rect_bound()))
    out("cap %s" % cap_str(cell.get_cap_bound()))
    out("area exact %s approx %s average %s" % (
        r(cell.exact_area()), r(cell.approx_area()), r(cell.average_area())))


def cmd_token(f):
    c = cell_id(f[0])
    out("%r" % c)
    out("valid %s" % tf(c.is_valid()))
    out("face %d level %d leaf %s" % (c.face(), c.level(), tf(c.is_leaf())))
    out("token %s" % tok(c))
    chain = []
    p = c
    while not p.is_face():
        p = p.parent()
        chain.append(tok(p))
    out("parents %s" % (" ".join(chain) if chain else "-"))
    face, i, j, orient = c.to_face_ij_orientation()
    out("ij %d %d orientation %d" % (i, j, orient))
    out("center %s" % ll(c.to_lat_lng()))


def cmd_id(f):
    c = s2.CellId(int(f[0], 0))
    out("%r" % c)
    out("valid %s" % tf(c.is_valid()))


def cmd_nav(f):
    c = cell_id(f[0])
    op = f[1]
    a = f[2:]
    if op == "parent":
        out(tok(c.parent(*[int(x) for x in a])))
    elif op == "child":
        out(tok(c.child(int(a[0]))))
    elif op == "children":
        out(toks(list(c.children(*[int(x) for x in a]))))
    elif op == "child_range":
        lv = [int(x) for x in a]
        out("%r %r" % (c.child_begin(*lv), c.child_end(*lv)))
    elif op == "next":
        out("%r" % c.next())
    elif op == "prev":
        out("%r" % c.prev())
    elif op == "next_wrap":
        out("%r" % c.next_wrap())
    elif op == "prev_wrap":
        out("%r" % c.prev_wrap())
    elif op == "advance":
        out("%r" % c.advance(int(a[0])))
    elif op == "advance_wrap":
        out("%r" % c.advance_wrap(int(a[0])))
    elif op == "range":
        out("%r %r" % (c.range_min(), c.range_max()))
    elif op == "edge":
        out(toks(c.get_edge_neighbors()))
    elif op == "vertex":
        out(toks(c.get_vertex_neighbors(int(a[0]))))
    elif op == "all":
        out(toks(list(c.get_all_neighbors(int(a[0])))))
    elif op == "contains":
        out(tf(c.contains(cell_id(a[0]))))
    elif op == "intersects":
        out(tf(c.intersects(cell_id(a[0]))))
    elif op == "lt":
        d = cell_id(a[0])
        out("%s %s %s" % (tf(c < d), tf(c == d), tf(c > d)))
    else:
        raise ValueError("unknown op: %s" % op)


def cmd_walk(f):
    level = int(f[0])
    cells = [c.to_token() for c in s2.CellId.walk(level)]
    out("%d cells" % len(cells))
    out("first %s" % " ".join(cells[:6]))
    out("last %s" % " ".join(cells[-6:]))
    begin = s2.CellId.begin(level)
    end = s2.CellId.end(level)
    out("begin %r end %r" % (begin, end))


def cmd_latlng(f):
    p = latlng(f[0], f[1])
    out("valid %s" % tf(p.is_valid()))
    n = p.normalized()
    out("normalized %s valid %s" % (ll(n), tf(n.is_valid())))
    q = p.to_point()
    out("point %s" % pt(q))
    back = s2.LatLng.from_point(q)
    out("back %s" % ll(back))
    out("approx %s" % tf(back.approx_equals(p)))
    if len(f) > 2:
        o = latlng(f[2], f[3])
        d = p.get_distance(o)
        out("distance %s rad %s deg %s km" % (r(d.radians), r(d.degrees),
                                             r(d.radians * EARTH_KM)))
        out("angle %s" % r(q.angle(o.to_point())))
        out("sum %s diff %s" % (ll(p + o), ll(p - o)))


def cmd_point(f):
    a = s2.Point(float(f[0]), float(f[1]), float(f[2]))
    out("norm %s norm2 %s" % (r(a.norm()), r(a.norm2())))
    u = a.normalize()
    out("normalized %s" % pt(u))
    out("largest %d" % a.largest_abs_component())
    face, uu, vv = s2.sphere.xyz_to_face_uv(a)
    out("face %d uv %s %s" % (face, r(uu), r(vv)))
    out("ortho %s" % pt(s2.sphere.ortho(u)))
    out("latlng %s" % ll(s2.LatLng.from_point(a)))
    out("cell %s" % s2.CellId.from_point(a).to_token())


def cmd_cap(f):
    c, n = region(["cap"] + f[:3])
    out("height %s area %s angle %s" % (r(c.height()), r(c.area()),
                                       r(c.angle().degrees)))
    out("valid %s empty %s full %s" % (tf(c.is_valid()), tf(c.is_empty()),
                                      tf(c.is_full())))
    out("rect %s" % rect_str(c.get_rect_bound()))
    comp = c.complement()
    out("complement %s" % cap_str(comp))
    rest = f[3:]
    i = 0
    while i < len(rest):
        p = latlng(rest[i], rest[i + 1])
        out("contains %s %s interior %s" % (
            ll(p), tf(c.contains(p.to_point())),
            tf(c.interior_contains(p.to_point()))))
        i += 2


def cmd_capop(f):
    a, n = region(["cap"] + f[:3])
    op = f[3]
    b, m = region(["cap"] + f[4:7])
    if op == "contains":
        out(tf(a.contains(b)))
    elif op == "intersects":
        out(tf(a.intersects(b)))
    elif op == "interior_intersects":
        out(tf(a.interior_intersects(b)))
    elif op == "approx":
        out(tf(a.approx_equals(b)))
    else:
        raise ValueError("unknown op: %s" % op)


def cmd_capmisc(f):
    op = f[0]
    if op == "empty":
        c = s2.Cap.empty()
    elif op == "full":
        c = s2.Cap.full()
    elif op == "height":
        c = s2.Cap.from_axis_height(latlng(f[1], f[2]).to_point(), float(f[3]))
    elif op == "area":
        c = s2.Cap.from_axis_area(latlng(f[1], f[2]).to_point(), float(f[3]))
    elif op == "grow":
        c = s2.Cap.from_axis_height(latlng(f[1], f[2]).to_point(), 0)
        i = 3
        while i < len(f):
            c.add_point(latlng(f[i], f[i + 1]).to_point())
            i += 2
    elif op == "expanded":
        c = s2.Cap.from_axis_angle(latlng(f[1], f[2]).to_point(),
                                   s2.Angle.from_degrees(float(f[3])))
        c = c.expanded(s2.Angle.from_degrees(float(f[4])))
    else:
        raise ValueError("unknown op: %s" % op)
    out("cap %s" % cap_str(c))
    out("area %s angle %s" % (r(c.area()), r(c.angle().degrees)))
    out("rect %s" % rect_str(c.get_rect_bound()))


def cmd_rect(f):
    x, n = region(["rect"] + f[:4])
    out("rect %s" % rect_str(x))
    out("valid %s empty %s full %s point %s" % (
        tf(x.is_valid()), tf(x.is_empty()), tf(x.is_full()),
        tf(x.is_point())))
    out("center %s size %s" % (ll(x.get_center()), ll(x.get_size())))
    out("area %s" % r(x.area()))
    for k in range(4):
        out("vertex %d %s" % (k, ll(x.get_vertex(k))))
    out("cap %s" % cap_str(x.get_cap_bound()))
    rest = f[4:]
    i = 0
    while i < len(rest):
        p = latlng(rest[i], rest[i + 1])
        out("contains %s %s interior %s" % (
            ll(p), tf(x.contains(p)), tf(x.interior_contains(p))))
        i += 2


def cmd_rectop(f):
    a, n = region(["rect"] + f[:4])
    op = f[4]
    if op == "expanded":
        out(rect_str(a.expanded(latlng(f[5], f[6]))))
        return
    if op == "convolve":
        out(rect_str(a.convolve_with_cap(s2.Angle.from_degrees(float(f[5])))))
        return
    if op == "cell":
        cell = s2.Cell(cell_id(f[5]))
        out("contains %s intersects %s may %s" % (
            tf(a.contains(cell)), tf(a.intersects(cell)),
            tf(a.may_intersect(cell))))
        return
    b, m = region(["rect"] + f[5:9])
    if op == "union":
        out(rect_str(a.union(b)))
    elif op == "intersection":
        out(rect_str(a.intersection(b)))
    elif op == "contains":
        out(tf(a.contains(b)))
    elif op == "intersects":
        out(tf(a.intersects(b)))
    elif op == "interior":
        out("%s %s" % (tf(a.interior_contains(b)),
                       tf(a.interior_intersects(b))))
    elif op == "approx":
        out(tf(a.approx_equals(b)))
    elif op == "eq":
        out(tf(a == b))
    else:
        raise ValueError("unknown op: %s" % op)


def cmd_sint(f):
    a = s2.SphereInterval(float(f[0]), float(f[1]))
    out("%s length %s center %s" % (interval("sint", a), r(a.get_length()),
                                    r(a.get_center())))
    out("full %s empty %s inverted %s" % (tf(a.is_full()), tf(a.is_empty()),
                                          tf(a.is_inverted())))
    out("%s" % interval("complement", a.complement()))
    out("complement center %s" % r(a.get_complement_center()))
    if len(f) > 2:
        b = s2.SphereInterval(float(f[2]), float(f[3]))
        out("%s" % interval("union", a.union(b)))
        out("%s" % interval("intersection", a.intersection(b)))
        out("contains %s intersects %s interior %s %s" % (
            tf(a.contains(b)), tf(a.intersects(b)),
            tf(a.interior_contains(b)), tf(a.interior_intersects(b))))
        out("hausdorff %s" % r(a.get_directed_hausdorff_distance(b)))
    if len(f) > 4:
        out("%s" % interval("expanded", a.expanded(float(f[4]))))


def cmd_lint(f):
    a = s2.LineInterval(float(f[0]), float(f[1]))
    b = s2.LineInterval(float(f[2]), float(f[3]))
    out("%s length %s center %s empty %s" % (
        interval("lint", a), r(a.get_length()), r(a.get_center()),
        tf(a.is_empty())))
    out("%s" % interval("union", a.union(b)))
    out("%s" % interval("intersection", a.intersection(b)))
    out("contains %s intersects %s interior %s %s eq %s" % (
        tf(a.contains(b)), tf(a.intersects(b)), tf(a.interior_contains(b)),
        tf(a.interior_intersects(b)), tf(a == b)))
    out("%s" % interval("expanded", a.expanded(float(f[4]))))


def cmd_cover(f, interior):
    rc = s2.RegionCoverer()
    rc.min_level = int(f[0])
    rc.max_level = int(f[1])
    rc.max_cells = int(f[2])
    rc.level_mod = int(f[3])
    reg, n = region(f[4:])
    if interior:
        cells = rc.get_interior_covering(reg)
    else:
        cells = rc.get_covering(reg)
    out("%d cells" % len(cells))
    out(toks(cells))
    if cells:
        u = s2.CellUnion(cells)
        out("normalized %d" % u.num_cells())


def cmd_simple(f):
    reg, n = region(f[2:])
    start = latlng(f[0], f[1]).to_point()
    level = int(f[-1])
    cells = list(s2.RegionCoverer.get_simple_covering(reg, start, level))
    out("%d cells" % len(cells))
    out(toks(sorted(cells)))


def union_of(field):
    if field == "-":
        return s2.CellUnion([])
    return s2.CellUnion([cell_id(t) for t in field.split(",")])


def cmd_union(f):
    u = union_of(f[0])
    out("%d cells %s" % (u.num_cells(), toks(u.cell_ids())))
    if len(f) > 1:
        op = f[1]
        if op == "denormalize":
            out(toks(u.denormalize(int(f[2]), int(f[3]))))
        elif op == "expand":
            u.expand(int(f[2]))
            out(toks(u.cell_ids()))
        elif op == "expand_angle":
            u.expand(s2.Angle.from_degrees(float(f[2])), int(f[3]))
            out(toks(u.cell_ids()))
        elif op == "rect":
            out(rect_str(u.get_rect_bound()))
        elif op == "has":
            out(tf(u.contains(cell_id(f[2]))))
        elif op == "hits":
            out(tf(u.intersects(cell_id(f[2]))))
        elif op == "point":
            out(tf(u.contains(latlng(f[2], f[3]).to_point())))
        else:
            v = union_of(f[2])
            if op == "union":
                w = s2.CellUnion.get_union(u, v)
            elif op == "intersection":
                w = s2.CellUnion.get_intersection(u, v)
            elif op == "difference":
                w = s2.CellUnion.get_difference(u, v)
            elif op == "contains":
                out(tf(u.contains(v)))
                return
            elif op == "intersects":
                out(tf(u.intersects(v)))
                return
            elif op == "eq":
                out(tf(u == v))
                return
            elif op == "clip":
                w = s2.CellUnion.get_intersection(u, cell_id(f[2]))
            else:
                raise ValueError("unknown op: %s" % op)
            out("%d cells %s" % (w.num_cells(), toks(w.cell_ids())))


METRICS = {
    "min_angle_span": s2.sphere.MIN_ANGLE_SPAN,
    "max_angle_span": s2.sphere.MAX_ANGLE_SPAN,
    "avg_edge": s2.sphere.AVG_EDGE,
    "min_width": s2.sphere.MIN_WIDTH,
    "max_diag": s2.sphere.MAX_DIAG,
    "avg_area": s2.sphere.AVG_AREA,
    "min_area": s2.sphere.MIN_AREA,
    "max_area": s2.sphere.MAX_AREA,
}


def cmd_metric(f):
    m = METRICS[f[0]]
    v = float(f[1])
    out("deriv %s" % r(m.deriv()))
    out("min %d max %d closest %d" % (m.get_min_level(v), m.get_max_level(v),
                                      m.get_closest_level(v)))
    for level in (0, 1, 10, 30):
        out("value %d %s" % (level, r(m.get_value(level))))


def cmd_drem(f):
    out(r(drem(float(f[0]), float(f[1]))))


def cmd_area(f):
    a = latlng(f[0], f[1]).to_point()
    b = latlng(f[2], f[3]).to_point()
    c = latlng(f[4], f[5]).to_point()
    out("area %s girard %s" % (r(s2.sphere.area(a, b, c)),
                               r(s2.sphere.girard_area(a, b, c))))
    out("ccw %s" % tf(s2.sphere.simple_ccw(a, b, c)))
    out("cross %s" % pt(s2.sphere.robust_cross_prod(a, b)))


def cmd_crossing(f):
    p = [latlng(f[i], f[i + 1]).to_point() for i in range(0, 8, 2)]
    out(tf(s2.sphere.simple_crossing(*p)))


def cmd_subdivide(f):
    cell = s2.Cell(cell_id(f[0]))
    for child in cell.subdivide():
        out("%s orientation %d center %s" % (
            child.id().to_token(), child.orientation(),
            ll(s2.LatLng.from_point(child.get_center()))))
        out("  rect %s" % rect_str(child.get_rect_bound()))


def cmd_cellop(f):
    a = s2.Cell(cell_id(f[0]))
    op = f[1]
    if op == "contains":
        out(tf(a.contains(s2.Cell(cell_id(f[2])))))
    elif op == "point":
        out(tf(a.contains(latlng(f[2], f[3]).to_point())))
    elif op == "may":
        out(tf(a.may_intersect(s2.Cell(cell_id(f[2])))))
    elif op == "edges":
        for k in range(4):
            out("edge %d %s" % (k, pt(a.get_edge(k))))
    elif op == "cap":
        c, n = region(["cap"] + f[2:5])
        out("contains %s may %s" % (tf(c.contains(a)), tf(c.may_intersect(a))))
    else:
        raise ValueError("unknown op: %s" % op)


# ------------------------------------------------------------- the place index

PLACES = None
ZONES = None


def place_index(level):
    idx = {}
    for name, lat, lng in PLACES:
        t = s2.CellId.from_lat_lng(latlng(lat, lng)).parent(level).to_token()
        idx.setdefault(t, []).append(name)
    return idx


def cmd_index(f):
    idx = place_index(int(f[0]))
    for t in sorted(idx):
        out("%s %s" % (t, ",".join(idx[t])))


def cmd_near(f):
    center = latlng(f[0], f[1])
    km = float(f[2])
    rc = s2.RegionCoverer()
    rc.max_cells = int(f[3])
    rc.max_level = int(f[4])
    cap = s2.Cap.from_axis_angle(center.to_point(),
                                 s2.Angle.from_radians(km / EARTH_KM))
    cover = s2.CellUnion(rc.get_covering(cap))
    out("covering %d cells" % cover.num_cells())
    hits = []
    candidates = 0
    for name, lat, lng in PLACES:
        p = latlng(lat, lng)
        if not cover.contains(s2.CellId.from_lat_lng(p)):
            continue
        candidates += 1
        d = center.get_distance(p).radians * EARTH_KM
        if d <= km:
            hits.append((d, name))
    out("candidates %d" % candidates)
    for d, name in sorted(hits):
        out("%s %s" % (name, "%.1f km" % d))


def cmd_zone(f):
    z = ZONES[f[0]]
    reg, n = region(z)
    rc = s2.RegionCoverer()
    rc.max_cells = int(f[1])
    rc.max_level = int(f[2])
    inner = s2.CellUnion(rc.get_interior_covering(reg))
    outer = s2.CellUnion(rc.get_covering(reg))
    out("outer %d inner %d" % (outer.num_cells(), inner.num_cells()))
    inside = []
    for name, lat, lng in PLACES:
        c = s2.CellId.from_lat_lng(latlng(lat, lng))
        if inner.contains(c):
            inside.append(name)
        elif outer.contains(c) and reg.contains(latlng(lat, lng).to_point()):
            inside.append(name + "*")
    out("inside %s" % (" ".join(inside) if inside else "-"))


COMMANDS = {
    "cell": cmd_cell, "token": cmd_token, "id": cmd_id, "nav": cmd_nav,
    "walk": cmd_walk, "latlng": cmd_latlng, "point": cmd_point,
    "cap": cmd_cap, "capop": cmd_capop, "capmisc": cmd_capmisc,
    "rect": cmd_rect, "rectop": cmd_rectop, "sint": cmd_sint,
    "lint": cmd_lint, "cover": lambda f: cmd_cover(f, False),
    "interior": lambda f: cmd_cover(f, True), "simple": cmd_simple,
    "union": cmd_union, "metric": cmd_metric, "drem": cmd_drem,
    "area": cmd_area, "crossing": cmd_crossing, "subdivide": cmd_subdivide,
    "cellop": cmd_cellop, "index": cmd_index, "near": cmd_near,
    "zone": cmd_zone,
}


def main():
    global PLACES, ZONES
    PLACES = load_places()
    ZONES = load_zones()
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
