"""Writes data/: the layer scripts the `write` jobs run through pyshp's
Writer, the legacy and broken shapefiles some other program left behind
(made here byte by byte with struct), and jobs.txt."""
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def put(name, body):
    with open(os.path.join(DATA, name), "wb") as f:
        f.write(body if isinstance(body, bytes) else body.encode("utf-8"))


# ------------------------------------------------------------ layer scripts

PARCELS = """\
# Ashby Vale cadastre: parcels with ponds, an island farm, a mis-wound
# allotment and a ring nobody closed.
writer POLYGON
field PARCEL_ID C 8 0
field OWNER C 24 0
field AREA_HA F 10 3
field VALUE N 9 0
field SURVEYED D 8 0
field ACTIVE L 1 0
field ZONE C 2 0
poly 1000,1000 1000,1200 1250,1200 1250,1000 1000,1000
record s:AV-0001 ; s:Hollins Farm Ltd ; f:5.0 ; i:420000 ; d:2026-03-01 ; b:T ; s:AG
poly 1300,1000 1300,1250.5 1600.25,1250.5 1600.25,1000 1300,1000 | 1350,1050 1450,1050 1450,1150 1350,1150 1350,1050
record s:AV-0002 ; s:Zoë Lefèvre ; f:6.502 ; s:125000.75 ; l:2026,2,30 ; i:0 ; s:R1
poly 2000,1000 2000,1600 2600,1600 2600,1000 2000,1000 | 2100,1100 2500,1100 2500,1500 2100,1500 2100,1100 | 2200,1200 2200,1400 2400,1400 2400,1200 2200,1200 | 2250,1250 2350,1250 2350,1350 2250,1350 2250,1250 | 2700,1000 2700,1300 2900,1300 2900,1000 2700,1000 | 2750,1050 2850,1050 2850,1150 2750,1150 2750,1050
record s:AV-0003 ; s:Marsh Island Trust ; f:28.0 ; f:9990000000.0 ; s:notadate ; s:T ; s:AG
poly 3000,1000 3100,1000 3100,1100 3000,1100 3000,1000
recordkw PARCEL_ID=s:AV-0004 ; OWNER=s:Allotment Society ; ZONE=s:CM ; COLOUR=s:green
poly 3200,1000.1 3200,1100.2 3300.3,1100.2 3300.3,1000.1
record s:AV-0005 ; s:St Wilfrid's Glebe ; n ; i:-875 ; s:2026-3-1 ; n ; s:CH
poly 4000,1000 4000,1100 4100,1100 4100,1000 4000,1000 | 4200,1000 4200,1100 4300,1100 4300,1000 4200,1000 | 4500,1000 4600,1000 4600,1100 4500,1100 4500,1000
record s:AV-0006 ; s:Crown Estate ; f:2.0 ; e ; e ; b:F ; s:AG ; s:extra
close
"""

ROADS = """\
# Road centrelines, measured in chainage metres.
writer POLYLINEM
field ROAD C 6 0
field NAME C 20 0
field LANES N 2 0
linem 1000,990,0 1600,990,600 2600,990,1600
record s:B1290 ; s:Vale Road ; i:2
linem 1625,900,0 1625,1300,400 | 1625,1300,400 2000,1700
record s:C31 ; s:Mill Lane ; s:1
linem 3000,950 3400,950
record s:U12 ; s:Church Walk ; i:123
linem 4000,950,7 4300,950,- 4600,950,12.25
record s:U13 ; s:Glebe Track ; n
close
"""

WELLS = """\
# Boreholes: elevation of the casing top as z, and no measures.
writer POINTZ
field WELL C 6 0
field DEPTH_M F 7 2
field LICENSED L 1 0
field DRILLED D 8 0
pointz 1100 1100 88.5 -
record s:BH-01 ; f:42.125 ; b:T ; d:1998-06-14
pointz 1500 1200 90.25 -
record s:BH-02 ; f:18 ; i:1 ; l:2004,11,2
pointz 2300 1300 72.0 12.5
record s:BH-03 ; s:30.5 ; s:Y ; s:20101301
pointz 2220 1220 70.5 -
record s:BH-04 ; f:9.999 ; b:F ; n
pointz 3500 3500 101 -
record s:BH-05 ; f:-3.5 ; n ; e
close
"""

SENSORS = """\
# Soil moisture probes, deployed in clusters.
writer MULTIPOINT
field CLUSTER C 4 0
field PROBES N 3 0
multipoint 1050,1050 1100,1150 1200,1050
record s:K1 ; i:3
multipoint 2050,1050 2450,1450 2230,1230
record s:K2 ; i:3
multipoint 2800,1100
record s:K3 ; f:1.9
multipoint 5000,5000 5100,5100
record s:K4 ; s:12 extra
close
"""

PATCHES = """\
# A barn roof and its gable, as a multipatch.
writer MULTIPATCH
field PART C 10 0
multipatch 0,2 1000,1000,5 1010,1000,5 1000,1010,9 1010,1010,9 | 990,990,0 990,1020,0 1020,1020,0 1020,990,0 990,990,0
record s:barn
close
"""

GEO = """\
# Features pasted in as GeoJSON, wound the GeoJSON way (counter-clockwise
# exteriors), which pyshp rewinds for the shapefile.
writer -
field SRC C 10 0
null
record s:empty
geo Polygon 0,0 10,0 10,10 0,10 0,0 | 2,2 2,4 4,4 4,2 2,2
record s:ccw-poly
geo MultiPolygon 20,0 30,0 30,10 20,10 20,0 ; 40,0 40,10 50,10 50,0 40,0
record s:multi
close
"""

LINEGEO = """\
writer -
field SRC C 10 0
geo LineString 0,0 5,5 10,0
record s:line
geo MultiLineString 0,0 1,1 | 2,2 3,3,9
record s:multiline
geo Point 7,7
record s:point
balance
close
"""

MISTAKES = """\
# One afternoon's mistakes, and how the Writer takes them.
writer POINT
field ID N 4 0
field NAME C 8 0
field WHEN D 8 0
field OK L 1 0
point 1 1
record i:1 ; s:first ; d:2026-10-21 ; b:T
record s:abc ; s:second ; e ; e
record i:3 ; s:third ; s:2026-10-21 ; e
record d:2026-10-21 ; s:fourth ; e ; e
record f:5.5 ; s:Æthelflæd ; e ; s:yes
point 5 5
multipoint 6,6 7,7
point 8 8
record i:6 ; s:sixth ; e ; e
close
balance
close
"""

OWNERS = """\
# A register exported by a tool that thought in characters, not bytes.
writer POINT
field Propriété1 C 3 0
field NOTE C 12 0
point 0 0
record s:Zoë Lefèvre ; s:ok
point 1 1
record s:Ana ; s:façade nord
close
"""

UNBALANCED = """\
writer POINT
autobalance
field ID N 3 0
point 1 2
point 3 4
record i:9
record i:10
record i:11
close
"""

NOFIELDS = """\
writer POLYLINE
close
"""

EMPTY = """\
writer POLYGON
field ID N 3 0
poly
record i:1
close
"""

# ------------------------------------------------------------ legacy files


def shp_header(shape_type, length_words, bbox, zbox=(0, 0), mbox=(0, 0)):
    h = struct.pack(">6ii", 9994, 0, 0, 0, 0, 0, length_words)
    h += struct.pack("<2i", 1000, shape_type)
    h += struct.pack("<4d", *bbox) + struct.pack("<4d", zbox[0], zbox[1], mbox[0], mbox[1])
    return h


def poly_content(shape_type, rings):
    pts = [p for r in rings for p in r]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    c = struct.pack("<i4d", shape_type, min(xs), min(ys), max(xs), max(ys))
    c += struct.pack("<2i", len(rings), len(pts))
    idx = 0
    for r in rings:
        c += struct.pack("<i", idx)
        idx += len(r)
    for p in pts:
        c += struct.pack("<2d", p[0], p[1])
    return c


def records_file(shape_type, contents, bbox, mbox=(0, 0)):
    body = b""
    offsets = []
    for i, c in enumerate(contents):
        offsets.append((100 + len(body), len(c) // 2))
        body += struct.pack(">2i", i + 1, len(c) // 2) + c
    shp = shp_header(shape_type, (100 + len(body)) // 2, bbox, mbox=mbox) + body
    shx = shp_header(shape_type, (100 + 8 * len(contents)) // 2, bbox, mbox=mbox)
    for off, ln in offsets:
        shx += struct.pack(">2i", off // 2, ln)
    return shp, shx


def dbf(fields, rows, count=None, terminator=b"\r"):
    rec_len = 1 + sum(f[2] for f in fields)
    n = len(rows) if count is None else count
    out = struct.pack("<BBBBLHH20x", 3, 98, 7, 1, n, 33 + 32 * len(fields), rec_len)
    for name, typ, size, deci in fields:
        nb = name.ljust(11, b"\x00")
        out += struct.pack("<11sc4xBB14x", nb, typ, size, deci)
    out += terminator
    for flag, vals in rows:
        out += flag
        for (_, _, size, _), v in zip(fields, vals):
            assert len(v) == size, (v, size)
            out += v
    return out + b"\x1a"


def legacy():
    sq = lambda x, y, s: [(x, y), (x, y + s), (x + s, y + s), (x + s, y), (x, y)]
    shapes = [
        poly_content(5, [sq(0, 0, 10)]),
        poly_content(5, [sq(20, 0, 10)]),
        poly_content(5, [sq(40, 0, 10), [(42, 2), (48, 2), (48, 8), (42, 8), (42, 2)]]),
        struct.pack("<i", 0),
        poly_content(5, [sq(60, 0, 5)]),
    ]
    shp, _ = records_file(5, shapes, (0, 0, 65, 10))
    put("legacy.SHP", shp)
    fields = [
        (b"PLOTNUMBERS", b"C", 6, 0),
        (b"AREA", b"N", 8, 0),
        (b"RATE", b"F", 7, 2),
        (b"LET", b"D", 8, 0),
        (b"FREEHOLD", b"L", 1, 0),
    ]
    rows = [
        (b" ", [b"P-001 ", b"     100", b"  12.50", b"19870401", b"Y"]),
        (b" ", [b"P-002\x00", b"   1_000", b"   ****", b"00000000", b"n"]),
        (b"*", [b"P-003 ", b"     400", b"   3.25", b"20261321", b"?"]),
        (b" ", [b" P-004", b"   12.75", b"abc    ", b"        ", b" "]),
        (b" ", [b"P-005\x00", b"\x00\x00\x00\x00\x00\x00\x00\x00", b"  1e3  ", b"2026-3-1", b"1"]),
    ]
    put("legacy.DBF", dbf(fields, rows))


def broken():
    sq = lambda x, y, s: [(x, y), (x, y + s), (x + s, y + s), (x + s, y), (x, y)]
    shapes = [poly_content(5, [sq(0, 0, 4)]), poly_content(5, [sq(5, 0, 4)]), poly_content(5, [sq(10, 0, 4)])]
    shp, shx = records_file(5, shapes, (0, 0, 14, 4))
    put("truncated.shp", shp[: len(shp) - 40])
    put("truncated.shx", shx)
    # polylineM whose m block was cut off, and pointMs with and without m
    pts = [(0.0, 0.0), (3.0, 4.0), (6.0, 8.0)]
    line = struct.pack("<i4d2ii", 23, 0, 0, 6, 8, 1, 3, 0)
    for p in pts:
        line += struct.pack("<2d", *p)
    line_m = line + struct.pack("<2d", 0, 10) + struct.pack("<3d", 0, 5, -1e39)
    shapes = [line, line_m]
    shp, shx = records_file(23, shapes, (0, 0, 6, 8), mbox=(0, 10))
    put("measures.shp", shp)
    put("measures.shx", shx)
    shapes = [struct.pack("<i2d", 21, 1, 2), struct.pack("<i3d", 21, 3, 4, 7.5), struct.pack("<i3d", 21, 5, 6, -2e39)]
    shp, shx = records_file(21, shapes, (1, 2, 5, 6), mbox=(-2e39, 7.5))
    put("gauges.shp", shp)
    fields = [(b"ID", b"N", 3, 0)]
    put("noterm.dbf", dbf(fields, [(b" ", [b"  1"])], terminator=b"\x00"))
    put("short.dbf", dbf(fields, [(b" ", [b"  1"]), (b" ", [b"  2"])], count=3)[:-1])


# ------------------------------------------------------------ jobs

JOBS = """\
write parcels
write roads
write wells
write sensors
write patches
write geo
write linegeo
write mistakes
write owners
write unbalanced
write nofields
write empty
info out/parcels
shapes out/parcels
records out/parcels
geojson out/parcels
info out/roads
shapes out/roads
records out/roads
geojson out/roads
info out/wells
shapes out/wells
records out/wells
geojson out/wells
info out/sensors
shapes out/sensors
geojson out/sensors
info out/patches
shapes out/patches
geojson out/patches
info out/geo
shapes out/geo
geojson out/geo
info out/linegeo
shapes out/linegeo
geojson out/linegeo
info out/mistakes
shapes out/mistakes
records out/mistakes
info out/owners
info out/owners replace
records out/owners replace
info out/unbalanced
records out/unbalanced
info out/empty
shapes out/empty
records out/empty
fields out/parcels OWNER,VALUE
fields out/parcels ACTIVE,ACTIVE
fields out/parcels DeletionFlag
fields out/parcels HEIGHT
get out/parcels 1 PARCEL_ID .OWNER 0 6 -1 .HEIGHT HEIGHT
get out/parcels -2 ZONE
get out/parcels 6 ZONE
get out/parcels -7 ZONE
get out/parcels -6 ZONE
shape out/parcels -1
shape out/parcels 6
shape out/wells 2
bbox out/parcels 1900,900,2650,1650
bbox out/wells 0,0,10,10
bbox out/roads 2900,800,3500,1000
info legacy
shapes legacy
records legacy
iter legacy
get legacy 0 PLOTNUMBER .FREEHOLD
get legacy 2 AREA
get legacy 4 RATE AREA .LET
shape legacy 3
geojson legacy
info truncated
shapes truncated
shape truncated 1
shape truncated 2
info measures
shapes measures
info gauges
shapes gauges
shape gauges 2
info noterm
info short
records short
info nowhere
extract out/parcels out/clip 1900,900,4150,1650
info out/clip
records out/clip
report
"""


def main():
    os.makedirs(DATA, exist_ok=True)
    layers = {
        "parcels": PARCELS, "roads": ROADS, "wells": WELLS, "sensors": SENSORS,
        "patches": PATCHES, "geo": GEO, "linegeo": LINEGEO, "mistakes": MISTAKES,
        "owners": OWNERS, "unbalanced": UNBALANCED, "nofields": NOFIELDS, "empty": EMPTY,
    }
    for name, text in layers.items():
        put(name + ".layer", text)
    legacy()
    broken()
    put("jobs.txt", JOBS)


main()
