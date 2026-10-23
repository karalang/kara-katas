"""Write data/jobs.tsv and the input files the jobs read.

geopy is the geocoding toolkit most Python location code imports for its
Point type and its distances: parsing coordinates the way people write
them ("41.5 N 81.0 W", "40°26′46″N 79°58′56″W", "51.5074, -0.1278, 35m"),
formatting them back as degrees, minutes and seconds, converting units,
and measuring great-circle and geodesic distances and destinations. The
inputs are waypoint lists, a city table and a set of delivery stops in
the forms those strings take.

data/point_pattern.txt is geopy's own POINT_PATTERN, written from the
vendored library so the port compiles the same regular expression.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HERE, "vendor"))

from geopy.point import POINT_PATTERN  # noqa: E402

FILES = {
    "point_pattern.txt": POINT_PATTERN.pattern,
    "in/route.txt": "\n".join([
        "51.5074 N, 0.1278 W",
        "51°30′26″N 0°7′39″W",
        "50.8225, -0.1372",
        "49.4944 N 0.1079 E",
        "48 51m 24s N 2 21m 3s E",
        "45.7640;4.8357",
        "43.2965 5.3698",
        "",
        "N 43°42' 0'' / E 7°16' 0''",
    ]) + "\n",
    "in/cities.txt": "\n".join([
        "Tokyo|35.6762, 139.6503",
        "Delhi|28.7041 N, 77.1025 E",
        "Shanghai|31°13′N 121°28′E",
        "Sao Paulo|-23.5505, -46.6333",
        "Mexico City|19.4326 N 99.1332 W",
        "Cairo|30.0444, 31.2357",
        "Mumbai|19 4m 34s N 72 52m 39s E",
        "Beijing|39.9042;116.4074",
        "Dhaka|23.8103 90.4125",
        "Osaka|34.6937 N, 135.5023 E",
        "New York|40.7128, -74.0060",
        "Karachi|24.8607 N 67.0011 E",
        "Buenos Aires|34.6037 S, 58.3816 W",
        "Istanbul|41.0082, 28.9784",
        "Lagos|6.5244 N, 3.3792 E",
        "Manila|14.5995 N 120.9842 E",
        "Rio de Janeiro|22.9068 S 43.1729 W",
        "Los Angeles|34.0522, -118.2437",
        "Moscow|55.7558 37.6173",
        "Paris|48.8566, 2.3522",
        "Lima|12.0464 S, 77.0428 W",
        "London|51.5074 N, 0.1278 W",
        "Sydney|33°52′04″S 151°12′36″E",
        "Auckland|-36.8485, 174.7633",
        "Reykjavik|64.1466 N, 21.9426 W",
        "Honolulu|21.3069 N 157.8583 W",
        "Anchorage|61.2181, -149.9003",
        "Nowhere|somewhere over the rainbow",
        "Suva|18.1248 S, 178.4501 E",
        "Apia|13.8507 S, 171.7514 W",
    ]) + "\n",
    "in/stops.txt": "\n".join([
        "40.7484, -73.9857",
        "40.7580 -73.9855",
        "40.7061, -74.0087",
        "40.6892 N, 74.0445 W",
        "40.7829;-73.9654",
        "40.6413, -73.7781",
        "40.8296 N 73.9262 W",
        "41.0, -74.5",
        "40.7128, -74.0060, 10m",
        "40.75, -73.99, 1.2km",
    ]) + "\n",
}

JOBS = []


def job(*fields):
    JOBS.append("\t".join(str(f) for f in fields))


def section(title):
    JOBS.append("# " + title)


section("points from strings")
for s in ["41.5,-81.0", "41.5;-81.0", "41.5 -81.0", "+41.5 -81.0",
          "41.5 N -81.0 W", "41.5 N, 81.0 W", "-41.5 S, 81.0 E, 2.5km",
          "-41.5 S;81.0 E", "23 26m 22s N 23 27m 30s E", "23 26m 22s N 23 27m 30s E 21.0mi",
          "3 26' 22\" N 23 27' 30\" E", "UT: N 39°20' 0'' / W 74°35' 0''",
          "40°26′46″N 79°58′56″W", "40° 26′ 46″ N, 79° 58′ 56″ W",
          "40.446° N 79.982° W", "40.446D N 79.982D W", "40*26m N 79*58m W",
          "51.5074, -0.1278, 35m", "51.5074 -0.1278 100 ft", "0 0 1.5nmi",
          "0 0 1nm", "0 0 3 KM", "N 40 E 70", "S 33.9 E 18.4", "40.7 N 74 W 10m",
          "Location: 40.7128, -74.0060", "lat=40.7128 lon=-74.0060",
          "  12.5 , 45.5  ", "12.5/45.5", "12.5\\t45.5", "12.5\\u00a045.5",
          "12.5,,45.5", "1.5", "abc", "", "91 0", "-90 0", "0 190", "0 -190",
          "0 540", "0 -180", "0 180", "0 360", "10.5.5 20", "1e5 2", "0.0001 0.00001",
          "89.99999999 179.99999999", "12 59m 59.9999999s N 1 2m 3.5s W",
          "40 26.767m N 79 58.933m W", "45 60m 0s N 0 0m 3600s E"]:
    job("point", s)

section("points from numbers")
for args in [("f:41.5", "f:-81.0", "f:0.0"), ("i:41", "i:-81", "-"),
             ("f:41.5", "f:-81", "f:12.3"), ("i:0", "i:0", "i:0"), ("-", "-", "-"),
             ("f:41.5", "-", "-"), ("-", "f:-81.0", "-"), ("f:90", "f:180", "f:0"),
             ("f:90.0000001", "f:0", "-"), ("f:-91", "f:0", "-"), ("f:0", "f:181", "-"),
             ("f:0", "f:-181", "-"), ("f:0", "f:900", "-"), ("f:0", "f:-540", "-"),
             ("f:0", "f:1e300", "-"), ("f:inf", "f:0", "-"), ("f:0", "f:nan", "-"),
             ("f:0", "f:0", "f:-inf"), ("s:41.5", "s:-81", "-"), ("s:abc", "f:0", "-"),
             ("s: 12.5 ", "s:1_000", "-"), ("f:-0.0", "f:-0.0", "f:-0.0"),
             ("f:12.3456789", "f:-98.7654321", "f:-0.25"), ("f:1e-10", "f:-1e-10", "f:1e-7")]:
    job("make", *args)
for items in [["f:41.5", "f:-81"], ["f:41.5", "f:-81", "f:1"], ["f:1", "f:2", "f:3", "f:4"],
              ["f:1"], [], ["s:41.5", "s:-81.0"], ["i:10", "i:200"]]:
    job("seq", *items)
job("lonlat", "-71.312796", "41.49008")
job("lonlat", "-81.695391", "41.499498", "0.5")
job("lonlat", "190", "10")
job("lonlat", "0", "95")

section("degrees and units")
for x in ["0", "41.5", "81.0", "23.439444", "0.5", "1e-9", "59.999999999",
          "12.999999", "179.9999999999", "123.456789", "0.0002777", "360.25"]:
    for sym in ["ascii", "unicode", "latin1", "html", "xml", "abbr", "default"]:
        job("degrees", x, sym)
for d, m, s, direction in [("41", "30", "0", "N"), ("41", "30", "0", "S"), ("-41", "30", "0", "-"),
                           ("-41", "30", "0", "S"), ("0", "0", "0", "W"), ("12", "0", "36", "E"),
                           ("12", "0.5", "0", "-"), ("12", "61", "61", "N"), ("1", "1", "1", "X"),
                           ("-0", "30", "0", "-"), ("0.5", "0", "0", "W")]:
    job("parse_degrees", d, m, s, direction)
for dist, unit in [("712", "m"), ("712", "km"), ("712", "mi"), ("712", "ft"), ("712", "nm"),
                   ("712", "nmi"), ("0", "m"), ("-3.5", "ft"), ("1", "yd"), ("-", "km")]:
    job("altitude", dist, unit)
for fn, kws in [("kilometers", ["miles=1"]), ("kilometers", ["meters=1500"]),
                ("kilometers", ["feet=5280"]), ("kilometers", ["nautical=1"]),
                ("kilometers", ["meters=1000", "miles=1", "feet=1", "nautical=1"]),
                ("kilometers", []), ("km", ["miles=26.2"]), ("meters", ["kilometers=1.5"]),
                ("meters", ["miles=1"]), ("meters", ["nautical=2", "feet=3"]),
                ("miles", ["kilometers=42.195"]), ("miles", ["feet=5280"]),
                ("miles", ["nautical=1", "meters=1"]), ("mi", ["kilometers=0"]),
                ("feet", ["kilometers=1"]), ("feet", ["miles=1"]), ("feet", ["meters=0.3048"]),
                ("feet", ["nautical=1", "miles=1"]), ("ft", []), ("nautical", ["kilometers=1.852"]),
                ("nautical", ["miles=1"]), ("nautical", ["feet=6076.12"]), ("nm", ["meters=1"]),
                ("degrees", ["radians=3.141592653589793"]), ("degrees", ["arcminutes=90"]),
                ("degrees", ["arcseconds=3600"]), ("degrees", ["radians=1", "arcminutes=1", "arcseconds=1"]),
                ("degrees", []), ("radians", ["degrees=180"]), ("radians", ["degrees=1", "arcminutes=60"]),
                ("rad", ["arcseconds=1"]), ("arcminutes", ["degrees=1.5"]),
                ("arcminutes", ["radians=1"]), ("arcminutes", ["arcseconds=30"]),
                ("arcmin", ["degrees=-0.25"]), ("arcseconds", ["degrees=1"]),
                ("arcseconds", ["arcminutes=1.5"]), ("arcsec", ["radians=0.001"]),
                ("kilometers", ["yards=3"])]:
    job("units", fn, *kws)

section("distances")
NEWPORT, CLEVELAND = "41.49008,-71.312796", "41.499498,-81.695391"
for algo in ["distance", "geodesic", "great_circle"]:
    job("dist", algo, NEWPORT, CLEVELAND)
job("dist", "geodesic", "-41.32,174.81", "40.96,-5.50")
job("dist", "great_circle", "-41.32,174.81", "40.96,-5.50")
job("dist", "geodesic", "40,160", "40.1,160.1")
job("dist", "geodesic", "40,160", "40.1,160.1", "40.2,160.2")
job("dist", "geodesic", "43.668613,40.258916", "43.658852,40.250839")
job("dist", "geodesic", "0,0", "0,180")
job("dist", "geodesic", "0,0", "0.5,179.5")
job("dist", "geodesic", "90,0", "-90,0")
job("dist", "great_circle", "90,0", "-90,0")
job("dist", "geodesic", "10,20", "10,20")
job("dist", "great_circle", "10,20", "10,20")
job("dist", "geodesic", "41.49008,-71.312796,100", "41.499498,-81.695391,100")
job("dist", "geodesic", "41.49008,-71.312796,0", "41.499498,-81.695391,1")
job("dist", "great_circle", "1,2,0.0000001", "3,4,0")
job("dist", "geodesic", "s:41.5 N 81.0 W", "s:40°26′46″N 79°58′56″W")
job("dist", "great_circle", "s:51.5074 N, 0.1278 W", "s:48 51m 24s N 2 21m 3s E")
job("dist", "geodesic", "s:not a point", "1,2")
for ell in ["WGS-84", "GRS-80", "Airy (1830)", "Intl 1924", "Clarke (1880)", "GRS-67",
            "6377.0,6356.0,0.003367003367003367", "6378.137,0,0.0", "Mars"]:
    job("dist", "geodesic", NEWPORT, CLEVELAND, "ellipsoid=" + ell)
job("dist", "great_circle", NEWPORT, CLEVELAND, "radius=6378.137")
job("dist", "great_circle", NEWPORT, CLEVELAND, "radius=1")
job("dist", "geodesic", NEWPORT, CLEVELAND, "miles=10")
job("dist", "great_circle", "miles=10")
job("dist", "distance", "kilometers=2", "meters=500")
job("dist", "distance", "n:1.42")
job("dist", "distance")
job("dist", "distance", "yards=3")
job("dist", "Distance", "miles=2")
job("dist", "Distance", NEWPORT, CLEVELAND)

section("destinations")
for algo in ["distance", "geodesic", "great_circle"]:
    job("dest", algo, "34,148", "90", "miles=10")
    job("dest", algo, "34,148", "90", "miles=10", "override=100")
    job("dest", algo, "0,0", "0", "kilometers=10000")
    job("dest", algo, "0,179.9", "90", "kilometers=50")
    job("dest", algo, "89.9,0", "0", "kilometers=50")
    job("dest", algo, "s:51.5074 N, 0.1278 W", "-45", "kilometers=1000")
    job("dest", algo, "-33.8688,151.2093", "270.5", "nautical=500")
job("dest", "geodesic", "34,148", "90", "miles=10", "ellipsoid=Airy (1830)")
job("dest", "great_circle", "34,148", "90", "miles=10", "radius=3389.5")
job("dest", "Distance", "34,148", "90", "miles=10")

section("distance arithmetic")
for op, a, b in [("add", "d:miles=2", "d:kilometers=1"), ("sub", "d:miles=2", "d:kilometers=1"),
                 ("neg", "d:miles=2", "-"), ("mul", "d:kilometers=6", "n:5"),
                 ("rmul", "d:kilometers=6", "n:2.5"), ("div", "d:kilometers=6", "n:5"),
                 ("div", "d:kilometers=6", "d:kilometers=4"), ("div", "d:kilometers=6", "n:0"),
                 ("floordiv", "d:kilometers=7", "n:2"), ("floordiv", "d:kilometers=-7", "n:2"),
                 ("floordiv", "d:kilometers=7", "d:kilometers=-2"),
                 ("floordiv", "d:kilometers=0.3", "n:0.1"), ("floordiv", "d:kilometers=1", "n:0"),
                 ("abs", "d:kilometers=-3", "-"), ("bool", "d:kilometers=0", "-"),
                 ("bool", "d:meters=1", "-"), ("eq", "d:kilometers=2", "d:meters=2000"),
                 ("gt", "d:kilometers=2", "d:miles=1"), ("lt", "d:kilometers=2", "d:miles=1"),
                 ("ge", "d:kilometers=2", "n:2"), ("le", "d:kilometers=2", "n:1.5"),
                 ("ne", "d:kilometers=1.609344", "d:miles=1"), ("add", "d:kilometers=1", "n:1"),
                 ("sub", "d:kilometers=1", "n:1"), ("mul", "d:kilometers=1", "d:kilometers=1"),
                 ("rmul", "d:kilometers=1", "d:kilometers=1"),
                 ("add", "gc:kilometers=1,radius=10", "d:kilometers=2"),
                 ("mul", "geo:kilometers=1,ellipsoid=Airy (1830)", "n:3"),
                 ("units", "d:kilometers=42.195", "-"), ("units", "d:miles=1", "-"),
                 ("units", "d:nautical=1", "-"), ("units", "d:feet=1", "-")]:
    job("arith", op, a, b)

section("programs")
job("route", "in/route.txt")
job("nearest", "in/cities.txt", "48.8566 N, 2.3522 E", "5")
job("nearest", "in/cities.txt", "-17.7134, 178.065", "4")
job("nearest", "in/cities.txt", "0 0", "3")
job("fence", "in/stops.txt", "40.7484, -73.9857", "5")
job("fence", "in/stops.txt", "40.7484, -73.9857", "0.5")
job("route", "in/missing.txt")


def main():
    for path, body in FILES.items():
        full = os.path.join(DATA, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(body)
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as fh:
        for line in JOBS:
            fh.write(line + "\n")
    with open(os.path.join(DATA, "files.txt"), "w", encoding="utf-8") as fh:
        for path in FILES:
            fh.write(path + "\n")


main()
