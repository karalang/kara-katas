#!/usr/bin/env python3
"""Writes data/jobs.tsv: one pymap3d call per line, "<function>\t<arg>\t...".
A bare argument is a float; "ell=<model>" or "ell=<a>:<b>" is the ellipsoid
keyword, and "deg=False", "method=", "npts=" and "alt=" the other keywords.
Hand-picked places and edge cases come first, then seeded random points.
Run: python3 -s -P -B mk.py"""
import os
import random

R = random.Random(307)

# (lat, lon, alt) in degrees and metres.
PLACES = [
    (-41.2865, 174.7762, 20.0),        # Wellington
    (40.9701, -5.6635, 800.0),         # Salamanca
    (42.3601, -71.0589, 43.0),         # Boston
    (35.6762, 139.6503, 40.0),         # Tokyo
    (-0.1807, -78.4678, 2850.0),       # Quito
    (-77.846, 166.676, 10.0),          # McMurdo
    (78.2232, 15.6267, 0.0),           # Longyearbyen
    (31.5, 35.5, -430.5),              # Dead Sea shore
    (27.9881, 86.925, 8848.86),        # Everest
    (0.0, 0.0, 0.0),                   # Null Island
    (90.0, 0.0, 0.0),                  # North Pole
    (-90.0, 0.0, 2835.0),              # South Pole station
    (10.0, 180.0, 0.0),
    (-10.0, -180.0, 0.0),
    (0.0, -75.2, 35786000.0),          # a geostationary satellite
    (51.6, -30.0, 408000.0),           # the ISS
    (45.0, 45.0, -6000000.0),          # deep inside the planet
]

ELLS = ["wgs84", "grs80", "airy", "bessel", "clarke1866", "wgs72", "pz90.11",
        "gsk2011", "wgs84_mean", "moon", "mars", "jupyter", "saturn", "venus", "io",
        "pluto"]

jobs = []


def f(x):
    return repr(float(x))


def job(name, *args):
    jobs.append("\t".join([name] + [a if isinstance(a, str) else f(a) for a in args]))


def rlat():
    return R.uniform(-90.0, 90.0)


def rlon():
    return R.uniform(-180.0, 180.0)


def ralt():
    return R.choice([R.uniform(-500.0, 9000.0), R.uniform(0.0, 4.0e7)])


def rad(x):
    return x * 3.141592653589793 / 180.0


# ------------------------------------------------------------ ellipsoids
for name in ELLS + ["maupertuis", "everest1830", "international1967", "nosuch"]:
    job("ellipsoid", name)
for ab in ["6378137.0:6356752.0", "1.0:1.0", "2.0:-1.0", "1.0:0.0", "1.0:2.0",
           "0.0:0.0", "1.0:-1.0", "1.0:-5.0", "-1.0:-2.0", "6400000.0:6300000.0"]:
    job("ellipsoid", ab)

# ------------------------------------------------------------ geodetic <-> ECEF
for p in PLACES:
    job("geodetic2ecef", *p)
for e in ELLS[1:]:
    job("geodetic2ecef", 33.3, -111.9, 1500.0, "ell=" + e)
job("geodetic2ecef", 0.5, -1.2, 100.0, "deg=False")
job("geodetic2ecef", 1.5707963267948966, 0.0, 0.0, "deg=False")
job("geodetic2ecef", float("inf"), 0.0, 0.0)
job("geodetic2ecef", 0.0, float("-inf"), 0.0)
job("geodetic2ecef", float("nan"), 10.0, 0.0)
job("geodetic2ecef", 45.0, 45.0, 0.0, "ell=1.0:2.0")
job("geodetic2ecef", 45.0, 45.0, 0.0, "ell=1.0:0.0")

ECEF = [
    (6378137.0, 0.0, 0.0), (0.0, 6378137.0, 0.0), (-6378137.0, 0.0, 0.0),
    (0.0, 0.0, 6356752.31424518), (0.0, 0.0, -6356752.31424518),
    (0.0, 0.0, 7000000.0), (0.0, 0.0, -7000000.0), (0.0, 0.0, 0.0),
    (1000.0, 2000.0, 3000.0), (0.001, 0.0, 0.0), (0.0, 0.0, 0.001),
    (42164000.0, 0.0, 0.0), (1334000.0, -4654000.0, 4138000.0),
    (-4645000.0, 2553000.0, -3536000.0), (3500000.0, 3500000.0, 3500000.0),
    (6378137.0, 0.0, 1e-9), (100000.0, 0.0, 0.0), (5000.0, 0.0, 0.0),
    (float("nan"), 0.0, 0.0), (float("inf"), 0.0, 0.0),
]
for p in ECEF:
    job("ecef2geodetic", *p)
for p in ECEF[:6] + ECEF[12:15]:
    job("ecef2geodetic", *p, "deg=False")
for e in ["moon", "mars", "jupyter", "venus", "io", "1.0:0.0"]:
    job("ecef2geodetic", 1000000.0, 2000000.0, 1500000.0, "ell=" + e)
    job("ecef2geodetic", 0.0, 0.0, 1000.0, "ell=" + e)
for _ in range(40):
    job("ecef2geodetic", R.uniform(-4e7, 4e7), R.uniform(-4e7, 4e7), R.uniform(-4e7, 4e7))
for _ in range(25):
    job("geodetic2ecef", rlat(), rlon(), ralt(), "ell=" + R.choice(ELLS))

# ------------------------------------------------------------ local frames
LOCAL6 = ["ecef2enu", "enu2ecef", "enu2geodetic", "geodetic2enu", "ecef2aer",
          "geodetic2aer", "aer2geodetic", "aer2ecef", "ned2geodetic", "ned2ecef",
          "ecef2ned", "geodetic2ned"]
FIRST = {
    "ecef2enu": [(1345660.0, -4350891.0, 4452314.0), (660930.0, -4701424.0, 4246579.0)],
    "enu2ecef": [(186.277521, 286.842228, 939.692621), (-1000.0, 0.0, 50.0)],
    "enu2geodetic": [(0.0, 0.0, -1.0), (3000.0, -4000.0, 120.5)],
    "geodetic2enu": [(42.002582, -81.997752, 1.1397018e3), (-41.28, 174.9, 0.0)],
    "ecef2aer": [(660930.0, -4701424.0, 4246579.0), (0.0, 0.0, 0.0)],
    "geodetic2aer": [(42.002582, -81.997752, 1.1397018e3), (40.97, -5.66, 800.0)],
    "aer2geodetic": [(33.0, 70.0, 1000.0), (270.0, -5.0, 250000.0)],
    "aer2ecef": [(33.0, 70.0, 1000.0), (0.0, 90.0, 35786000.0)],
    "ned2geodetic": [(286.842228, 186.277521, -939.692621), (10.0, 10.0, 10.0)],
    "ned2ecef": [(286.842228, 186.277521, -939.692621), (0.0, 0.0, 0.0)],
    "ecef2ned": [(1345660.0, -4350891.0, 4452314.0), (660930.0, -4701424.0, 4246579.0)],
    "geodetic2ned": [(42.002582, -81.997752, 1.1397018e3), (89.0, 0.0, 0.0)],
}
ORIGINS = [(42.0, -82.0, 200.0), (0.0, 0.0, 0.0), (-41.2865, 174.7762, 20.0),
           (90.0, 45.0, 0.0)]
for name in LOCAL6:
    for a in FIRST[name]:
        for o in ORIGINS[:3]:
            job(name, *a, *o)
    job(name, *FIRST[name][0], *ORIGINS[3])
    job(name, *FIRST[name][0], *ORIGINS[0], "ell=mars")
    job(name, rad(10.0) if name.startswith("geodetic") else FIRST[name][0][0],
        FIRST[name][0][1] if not name.startswith("geodetic") else rad(20.0),
        FIRST[name][0][2], rad(42.0), rad(-82.0), 200.0, "deg=False")
    for _ in range(4):
        if name.startswith("geodetic"):
            a = (rlat(), rlon(), ralt())
        elif name.startswith("ecef"):
            a = (R.uniform(-1e7, 1e7), R.uniform(-1e7, 1e7), R.uniform(-1e7, 1e7))
        elif name.startswith("aer"):
            a = (R.uniform(0.0, 360.0), R.uniform(-90.0, 90.0), R.uniform(0.0, 1e6))
        else:
            a = (R.uniform(-1e5, 1e5), R.uniform(-1e5, 1e5), R.uniform(-1e5, 1e5))
        job(name, *a, rlat(), rlon(), ralt())
job("aer2geodetic", 33.0, 70.0, -1.0, 42.0, -82.0, 200.0)
job("aer2ecef", 33.0, 70.0, -1000.0, 42.0, -82.0, 200.0)

for name, cases in [
        ("ecef2enuv", [(1.0, 2.0, 3.0, 42.0, -82.0), (100.0, -50.0, 0.0, 0.0, 0.0),
                       (0.5, 0.5, 0.5, 90.0, 180.0)]),
        ("enu2uvw", [(186.277521, 286.842228, 939.692621, 42.0, -82.0),
                     (1.0, 0.0, 0.0, -45.0, 135.0)]),
        ("uvw2enu", [(-1000.0, 2000.0, 300.0, 42.0, -82.0), (0.0, 0.0, 1.0, 0.0, 90.0)]),
        ("enu2ecefv", [(1.0, 2.0, 3.0, 42.0, -82.0), (0.0, 1.0, 0.0, 30.0, 60.0)]),
        ("ecef2nedv", [(1.0, 2.0, 3.0, 42.0, -82.0), (-7.0, 0.0, 7.0, -12.0, 300.0)])]:
    for c in cases:
        job(name, *c)
    job(name, *cases[0][:3], rad(cases[0][3]), rad(cases[0][4]), "deg=False")

for c in [(186.277521, 286.842228, 939.692621), (0.0, 0.0, 0.0), (0.0005, -0.0002, 10.0),
          (-1.0, -1.0, -1.0), (-0.0, 0.0, 0.0), (0.0, -1.0, 0.0), (-5.0, 0.0, 0.0),
          (1e-4, 1e-4, 1e-4), (3.0, 4.0, 0.0), (0.0, 0.0, -100.0)]:
    job("enu2aer", *c)
    job("ned2aer", *c)
job("enu2aer", 3.0, 4.0, 5.0, "deg=False")
for c in [(33.0, 70.0, 1000.0), (0.0, 0.0, 0.0), (360.0, -90.0, 5.0), (90.0, 45.0, 0.0),
          (33.0, 70.0, -1.0), (-30.0, 10.0, 1e7)]:
    job("aer2enu", *c)
    job("aer2ned", *c)
job("aer2enu", 1.0, 0.5, 10.0, "deg=False")
for _ in range(10):
    a = (R.uniform(0.0, 360.0), R.uniform(-90.0, 90.0), R.uniform(0.0, 1e6))
    job("aer2enu", *a)
    e = (R.uniform(-1e4, 1e4), R.uniform(-1e4, 1e4), R.uniform(-1e4, 1e4))
    job("enu2aer", *e)

# ------------------------------------------------------------ DCA
for name in ["enu2dca", "dca2enu", "dca2ned", "ned2dca", "aer2dca", "dca2aer"]:
    for c in [(100.0, 200.0, 30.0, 45.0), (-5.0, 0.0, 1.0, 0.0), (1000.0, -1000.0, 0.0, 270.0)]:
        job(name, *c)
    job(name, 100.0, 200.0, 30.0, 0.7, "deg=False")
job("aer2dca", 10.0, 20.0, -5.0, 0.0)
for name in ["ecef2dca", "dca2ecef", "geodetic2dca", "dca2geodetic"]:
    first = (42.01, -81.99, 300.0) if name.startswith("geodetic") else \
        (660930.0, -4701424.0, 4246579.0) if name.startswith("ecef") else (500.0, -20.0, 10.0)
    job(name, *first, 42.0, -82.0, 200.0, 30.0)
    job(name, *first, 42.0, -82.0, 200.0, 30.0, "ell=airy")
    job(name, *first, -41.2865, 174.7762, 20.0, 315.0)

# ------------------------------------------------------------ utils, nvector, spherical
for c in [(3.0, 4.0), (-1.0, 0.0), (0.0, -0.0), (-0.0, -0.0), (1e300, 1e300)]:
    job("utils.cart2pol", *c)
for c in [(0.0, 1.0), (3.141592653589793, 2.0), (-1.0, 5.0), (1.0, -2.0)]:
    job("utils.pol2cart", *c)
for c in [(1.0, 2.0, 3.0), (0.0, 0.0, -1.0), (-3.0, -4.0, 0.0), (0.0, 0.0, 0.0)]:
    job("utils.cart2sph", *c)
for c in [(0.5, 0.25, 10.0), (0.0, 1.5707963267948966, 1.0), (-2.0, -1.0, 3.0)]:
    job("utils.sph2cart", *c)

for p in PLACES[:12]:
    job("geodetic2nvector", p[0], p[1])
    job("ecef2nvector", 1334000.0 + 100 * p[0], -4654000.0 + 10 * p[1], 4138000.0 + p[2])
job("geodetic2nvector", 0.3, -0.2, "deg=False")
for c in [(0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.5, 0.5, 0.7071067811865476), (0.0, 0.0, 2.0),
          (0.0, 0.0, -1.0), (-0.6, -0.8, 0.0)]:
    job("nvector2geodetic", *c)
    job("nvector2ecef", *c)
job("nvector2geodetic", 0.6, 0.8, 0.0, "deg=False")
job("nvector2ecef", 0.6, 0.8, 0.0, "alt=1000.0")
job("nvector2ecef", 0.6, 0.8, 0.0, "alt=500.0", "ell=moon")
job("ecef2nvector", 0.0, 0.0, 0.0)
job("ecef2nvector", 1700000.0, 0.0, 0.0, "ell=moon", "deg=False")

for p in PLACES[:16]:
    job("spherical.geodetic2spherical", *p)
for c in [(30.0, 40.0, 6370000.0), (0.0, 0.0, 6378137.0), (89.9, 10.0, 6356800.0),
          (-60.0, -120.0, 7000000.0), (45.0, 45.0, 4.2164e7), (90.0, 0.0, 6356752.31424518),
          (-10.0, 50.0, 1000000.0)]:
    job("spherical.spherical2geodetic", *c)
job("spherical.geodetic2spherical", 0.5, 0.5, 0.0, "deg=False")
job("spherical.spherical2geodetic", 0.5, 0.5, 6371000.0, "deg=False")
job("spherical.geodetic2spherical", 20.0, 30.0, 1000.0, "ell=mars")
job("spherical.spherical2geodetic", 20.0, 30.0, 3390000.0, "ell=mars")
for _ in range(12):
    job("spherical.geodetic2spherical", rlat(), rlon(), ralt())
    job("spherical.spherical2geodetic", rlat(), rlon(), R.uniform(2e6, 4e7))

# ------------------------------------------------------------ latitude
LATS = [0.0, 10.0, 45.0, -45.0, 60.0, 89.9, 90.0, -90.0, -33.3, 1e-7]
for name in ["geodetic2isometric", "isometric2geodetic", "conformal2geodetic",
             "geodetic2conformal", "geodetic2rectifying", "rectifying2geodetic",
             "geodetic2authalic", "authalic2geodetic", "geodetic2parametric",
             "parametric2geodetic"]:
    for lat in LATS:
        job("latitude." + name, lat)
    job("latitude." + name, 0.7, "deg=False")
    job("latitude." + name, 30.0, "ell=jupyter")
    job("latitude." + name, 30.0, "ell=venus")
for lat in [200.0, -400.0, 1.5707963267948966]:
    job("latitude.geodetic2isometric", lat)
job("latitude.geodetic2isometric", 1.5707963267948966, "deg=False")
job("latitude.geodetic2isometric", 90.0, "ell=1.0:0.0")
job("latitude.geodetic2isometric", 30.0, "ell=1.0:-5.0")
job("latitude.geodetic2conformal", 90.0, "ell=1.0:0.0")
job("latitude.geodetic2conformal", -90.0, "ell=mars")
job("latitude.isometric2geodetic", float("inf"))
job("latitude.isometric2geodetic", 1000.0)
for name in ["geodetic2geocentric", "geocentric2geodetic"]:
    for c in [(0.0, 0.0), (45.0, 0.0), (45.0, 10000.0), (-60.0, 400000.0), (89.0, -500.0),
              (90.0, 0.0), (30.0, 35786000.0)]:
        job("latitude." + name, *c)
    job("latitude." + name, 0.0, -6378137.0, "deg=False")
    job("latitude." + name, 0.5, 100.0, "deg=False", "ell=moon")
for c in [(0.0, 6378137.0), (45.0, 6378137.0), (-30.0, 7000000.0), (89.0, 6357000.0),
          (10.0, 0.0), (45.0, -1.0)]:
    job("latitude.geoc2geod", *c)
job("latitude.geoc2geod", 0.5, 6371000.0, "deg=False", "ell=grs80")

# ------------------------------------------------------------ rcurve, rsphere
for name in ["geocentric_radius", "parallel", "meridian", "transverse"]:
    for lat in [0.0, 30.0, 45.0, -60.0, 90.0, -90.0]:
        job("rcurve." + name, lat)
    job("rcurve." + name, 1.0, "deg=False")
    job("rcurve." + name, 30.0, "ell=saturn")
    job("rcurve." + name, 30.0, "ell=1.0:0.0")
for e in [None] + ELLS[1:] + ["1.0:0.0", "1.0:-5.0", "2.0:-1.0"]:
    kw = [] if e is None else ["ell=" + e]
    # A negative polar axis makes rectifying() and triaxial("norm") raise a
    # negative number to a fractional power, which Python answers with a
    # complex number; those two calls are left out for it.
    real = e != "2.0:-1.0"
    for name in ["eqavol", "authalic"] + (["rectifying"] if real else []):
        job("rsphere." + name, *kw)
    for m in ["mean", "norm"]:
        if real or m == "mean":
            job("rsphere.triaxial", *kw, "method=" + m)
        job("rsphere.biaxial", *kw, "method=" + m)
job("rsphere.triaxial", "method=median")
job("rsphere.biaxial", "method=max")
for lat in [0.0, 45.0, -80.0, 90.0]:
    for m in ["mean", "norm"]:
        job("rsphere.curve", lat, "method=" + m)
job("rsphere.curve", 45.0, "method=geometric")
job("rsphere.curve", 0.3, "deg=False", "ell=mars", "method=norm")
for c in [(42.0, -82.0, 41.0, -81.0), (0.0, 0.0, 0.0, 90.0), (-41.28, 174.77, 40.96, -5.5),
          (10.0, 10.0, 10.0, 10.0), (80.0, 0.0, -80.0, 180.0), (0.0, 0.0, 0.5, 179.5)]:
    job("rsphere.euler", *c)
job("rsphere.euler", 0.7, -1.4, 0.71, -1.39, "deg=False")
job("rsphere.euler", 42.0, -82.0, 41.0, -81.0, "ell=clarke1866")

# ------------------------------------------------------------ haversine, vincenty
for c in [(35.0, 23.0, 84.0, 20.0), (0.0, 0.0, 180.0, 0.0), (10.0, 10.0, 10.0, 10.0),
          (-71.06, 42.36, 139.65, 35.68), (0.0, 90.0, 0.0, -90.0), (179.9, 0.0, -179.9, 0.0)]:
    job("haversine.anglesep_meeus", *c)
    job("haversine.anglesep", *c)
job("haversine.anglesep", 0.6, 0.4, 1.4, 0.3, "deg=False")
for t in [0.0, 1.0, 3.141592653589793, -2.5, 100.0]:
    job("haversine.haversine", t)

VPAIRS = [(42.0, -82.0, 41.0, -81.0), (-41.32, 174.81, 40.96, -5.5),
          (0.0, 0.0, 0.0, 179.5), (0.0, 0.0, 0.5, 179.7), (0.0, 0.0, 0.0, 180.0),
          (90.0, 0.0, -90.0, 0.0), (89.99999999999, 0.0, 10.0, 10.0), (10.0, 10.0, 10.0, 10.0),
          (-33.9, 18.4, 51.5, -0.13), (30.0, 0.0, -30.0, 179.9), (91.0, 0.0, 0.0, 0.0),
          (0.0, 0.0, -95.0, 0.0), (0.0, 0.0, 0.0, 1e-9), (60.0, 359.0, 60.0, 1.0),
          (0.0, 0.0, 0.0, float("nan")), (0.0, 0.0, 0.0, float("inf")), (0.0, 0.0, 0.1, 179.9)]
for c in VPAIRS:
    job("vincenty.vdist", *c)
job("vincenty.vdist", 0.7, -1.4, 0.71, -1.39, "deg=False")
job("vincenty.vdist", 42.0, -82.0, 41.0, -81.0, "ell=mars")
job("vincenty.vdist", 42.0, -82.0, 41.0, -81.0, "ell=wgs84_mean")
for c in [(42.0, -82.0, 1000.0, 45.0), (-41.32, 174.81, 19959679.0, 161.07),
          (0.0, 0.0, 0.0, 0.0), (89.0, 10.0, 500000.0, 180.0), (90.0, 0.0, 1000.0, 90.0),
          (10.0, 170.0, 3000000.0, 90.0), (10.0, 10.0, -1.0, 0.0), (95.0, 10.0, 1.0, 0.0),
          (-60.0, -60.0, 1e7, 300.0), (0.0, 0.0, 20003930.0, 90.0)]:
    job("vincenty.vreckon", *c)
job("vincenty.vreckon", 0.7, -1.4, 10000.0, 0.5, "deg=False")
job("vincenty.vreckon", 42.0, -82.0, 1000.0, 45.0, "ell=moon")
for _ in range(15):
    job("vincenty.vdist", rlat(), rlon(), rlat(), rlon())
    job("vincenty.vreckon", rlat(), rlon(), R.uniform(0.0, 2e7), R.uniform(0.0, 360.0))
job("vincenty.track2", 40.0, -80.0, 65.0, 148.0, "npts=2")
job("vincenty.track2", 40.0, -80.0, 65.0, 148.0, "npts=1")
job("vincenty.track2", 40.0, -80.0, 65.0, 148.0, "npts=5")
job("vincenty.track2", 0.0, 0.0, 0.0, 180.0, "npts=5")

# ------------------------------------------------------------ lox
for lat in [0.0, 45.0, -45.0, 90.0, 30.5]:
    job("lox.meridian_dist", lat)
job("lox.meridian_dist", 0.5, "deg=False", "ell=moon")
for c in [(0.0, 90.0), (-90.0, 90.0), (45.0, 46.0), (10.0, -20.0)]:
    job("lox.meridian_arc", *c)
for c in [(40.0, -80.0, 65.0, -148.0), (0.0, 0.0, 0.0, 90.0), (0.0, 0.0, 10.0, 0.0),
          (10.0, 20.0, 10.0, -30.0), (40.0, 30.0, 40.0, 30.0), (89.9, 0.0, -89.9, 10.0),
          (90.0, 0.0, 80.0, 0.0), (-90.0, 0.0, 90.0, 0.0), (35.0, 140.0, -35.0, -40.0)]:
    job("lox.loxodrome_inverse", *c)
job("lox.loxodrome_inverse", 0.7, -1.4, 0.2, 0.3, "deg=False")
job("lox.loxodrome_inverse", 40.0, -80.0, 65.0, -148.0, "ell=jupyter")
for c in [(40.0, -80.0, 10000.0, 30.0), (0.0, 0.0, 1000000.0, 90.0), (0.0, 0.0, 1000000.0, 270.0),
          (10.0, 10.0, 0.0, 45.0), (40.0, -80.0, 5e6, 180.0), (40.0, -80.0, 5e6, -45.0),
          (40.0, -80.0, -1.0, 0.0), (91.0, 0.0, 1.0, 0.0), (-30.0, 150.0, 2e6, 450.0)]:
    job("lox.loxodrome_direct", *c)
job("lox.loxodrome_direct", 0.7, -1.4, 10000.0, 1.0, "deg=False")
job("lox.loxodrome_direct", 40.0, -80.0, 10000.0, 30.0, "ell=mars")
for c in [(0.0, 90.0, 0.0), (-80.0, 100.0, 45.0), (10.0, 370.0, 60.0), (0.0, 0.0, 90.0)]:
    job("lox.departure", *c)
job("lox.departure", 0.1, 0.4, 0.5, "deg=False")
job("lox.meanm", 10.0, 20.0)

# ------------------------------------------------------------ lookAtSpheroid
for c in [(42.0, -82.0, 1000.0, 0.0, 0.0), (42.0, -82.0, 1000.0, 45.0, 30.0),
          (42.0, -82.0, 1000.0, 45.0, 90.0), (42.0, -82.0, 1000.0, 45.0, 120.0),
          (0.0, 0.0, 35786000.0, 0.0, 5.0), (0.0, 0.0, 35786000.0, 90.0, 9.0),
          (-41.28, 174.77, 10.0, 180.0, 60.0), (42.0, -82.0, -1.0, 0.0, 0.0),
          (89.0, 0.0, 400000.0, 270.0, 45.0), (10.0, 20.0, 0.0, 0.0, 0.0)]:
    job("lookAtSpheroid", *c)
job("lookAtSpheroid", 0.7, -1.4, 1000.0, 0.5, 0.3, "deg=False")
job("lookAtSpheroid", 42.0, -82.0, 1000.0, 45.0, 30.0, "ell=mars")

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(jobs) + "\n")
print(len(jobs), "jobs")
