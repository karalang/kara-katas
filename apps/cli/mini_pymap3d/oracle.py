#!/usr/bin/env python3
"""Replays data/jobs.tsv through the vendored pymap3d and writes expected.out.
Each job is one call: "<function>\t<arg>\t...". A bare argument is a float;
"ell=<model>" names a built-in ellipsoid and "ell=<a>:<b>" builds one from its
axes; "deg=False", "method=<m>", "npts=<n>" and "alt=<x>" are the keyword
arguments of the same name. "ellipsoid\t<model>" or "ellipsoid\t<a>:<b>"
prints the Ellipsoid itself. Each line reads "<function>(<args>) => <repr of
the result>", or "<ExceptionType>: <message>" when the call raises.

numpy is blocked, so the library runs on its pure-Python path (math module
scalars), the one a numpy-free install takes.
Run: python3 -I -B oracle.py > expected.out"""
import sys

sys.modules["numpy"] = None
sys.path.insert(0, "vendor")
import pymap3d  # noqa: E402
from pymap3d import ellipsoid, haversine, latitude, lox, rcurve, rsphere  # noqa: E402
from pymap3d import spherical, vincenty  # noqa: E402
from pymap3d.los import lookAtSpheroid  # noqa: E402

# haversine.anglesep switches to astropy when it has been imported.
assert "astropy" not in sys.modules

FUNCS = {}
for name in ["geodetic2ecef", "ecef2geodetic", "ecef2enuv", "ecef2enu", "enu2uvw",
             "uvw2enu", "enu2ecef", "enu2aer", "aer2enu", "enu2geodetic",
             "geodetic2enu", "enu2ecefv", "ecef2aer", "geodetic2aer", "aer2geodetic",
             "aer2ecef", "aer2ned", "ned2aer", "ned2geodetic", "ned2ecef", "ecef2ned",
             "geodetic2ned", "ecef2nedv", "enu2dca", "dca2enu", "dca2ned", "ned2dca",
             "ecef2dca", "dca2ecef", "geodetic2dca", "dca2geodetic", "aer2dca",
             "dca2aer", "geodetic2nvector", "nvector2geodetic", "ecef2nvector",
             "nvector2ecef"]:
    FUNCS[name] = getattr(pymap3d, name)
FUNCS["lookAtSpheroid"] = lookAtSpheroid
for mod, names in [
        (pymap3d.utils, ["cart2pol", "pol2cart", "cart2sph", "sph2cart"]),
        (latitude, ["geoc2geod", "geodetic2geocentric", "geocentric2geodetic",
                    "geodetic2isometric", "isometric2geodetic", "conformal2geodetic",
                    "geodetic2conformal", "geodetic2rectifying", "rectifying2geodetic",
                    "geodetic2authalic", "authalic2geodetic", "geodetic2parametric",
                    "parametric2geodetic"]),
        (rcurve, ["geocentric_radius", "parallel", "meridian", "transverse"]),
        (rsphere, ["eqavol", "authalic", "rectifying", "euler", "curve", "triaxial",
                   "biaxial"]),
        (lox, ["meridian_dist", "meridian_arc", "loxodrome_inverse", "loxodrome_direct",
               "departure", "meanm"]),
        (vincenty, ["vdist", "vreckon", "track2"]),
        (haversine, ["anglesep_meeus", "anglesep", "haversine"]),
        (spherical, ["geodetic2spherical", "spherical2geodetic"])]:
    for name in names:
        FUNCS[mod.__name__.split(".")[-1] + "." + name] = getattr(mod, name)


def ell_of(s):
    if ":" in s:
        a, b = s.split(":")
        return ellipsoid.Ellipsoid(float(a), float(b))
    return ellipsoid.Ellipsoid.from_name(s)


def call(f):
    if f[0] == "ellipsoid":
        return ell_of(f[1])
    args = []
    kw = {}
    for tok in f[1:]:
        if tok.startswith("ell="):
            kw["ell"] = ell_of(tok[4:])
        elif tok == "deg=False":
            kw["deg"] = False
        elif tok.startswith("method="):
            kw["method"] = tok[7:]
        elif tok.startswith("npts="):
            kw["npts"] = int(tok[5:])
        elif tok.startswith("alt="):
            kw["alt"] = float(tok[4:])
        else:
            args.append(float(tok))
    return FUNCS[f[0]](*args, **kw)


out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if line == "":
        continue
    f = line.split("\t")
    try:
        res = repr(call(f))
    except Exception as e:
        res = "%s: %s" % (type(e).__name__, e)
    out.append("%s(%s) => %s" % (f[0], ", ".join(f[1:]), res))
print("\n".join(out))
