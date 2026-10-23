#!/usr/bin/env python3
"""Replays data/jobs.tsv (see mk.py for the job kinds) through the vendored
sgp4 on its pure-Python path (sgp4.model.Satrec, not the C++ extension) and
writes expected.out. Each job prints a header naming the call, then what the
call returns as repr(), or "<ExceptionType>: <repr of the message>" when it
raises. A verify job prints exactly the lines the library's tests.py
regenerates tcppver.out from, plus an "error ..." line where its error list
grows.
Run: python3 -I -B oracle.py > expected.out"""
import sys
from math import isnan, pi

sys.path.insert(0, "vendor")
from sgp4 import io  # noqa: E402
from sgp4.alpha5 import from_alpha5, to_alpha5  # noqa: E402
from sgp4.earth_gravity import wgs72, wgs72old, wgs84  # noqa: E402
from sgp4.exporter import export_tle  # noqa: E402
from sgp4.ext import invjday, newtonnu, rv2coe  # noqa: E402
from sgp4.ext import jday as ext_jday  # noqa: E402
from sgp4.functions import days2mdhms, jday  # noqa: E402
from sgp4.io import compute_checksum, fix_checksum, verify_checksum  # noqa: E402
from sgp4.model import Satrec  # noqa: E402
from sgp4.propagation import getgravconst, gstime, sgp4  # noqa: E402

assert "sgp4.wrapper" not in sys.modules
GRAV = {"wgs72old": 0, "wgs72": 1, "wgs84": 2}
GOBJ = {"wgs72old": wgs72old, "wgs72": wgs72, "wgs84": wgs84}
rad = 180.0 / pi

STRS = ["satnum_str", "classification", "intldesg", "operationmode", "method", "init",
        "error_message"]
INTS = ["epochyr", "ephtype", "elnum", "revnum", "error", "irez", "isimp"]
FLOATS = [a for a in Satrec.__slots__ if a not in STRS and a not in INTS and a != "epoch"]
SHORT = ["epochdays", "jdsatepoch", "jdsatepochF", "ndot", "nddot", "bstar", "inclo", "nodeo",
         "ecco", "argpo", "mo", "no_kozai", "no_unkozai", "a", "alta", "altp", "gsto"]


def exc(e):
    return "%s: %r" % (type(e).__name__, str(e))


def out(s):
    sys.stdout.write(s + "\n")


def summary(s, full, extra=()):
    items = []
    try:
        items.append("satnum=%r" % s.satnum)
    except Exception as e:  # noqa: BLE001
        items.append("satnum=" + exc(e))
    for a in STRS + INTS + (FLOATS if full else SHORT):
        if hasattr(s, a):
            items.append("%s=%r" % (a, getattr(s, a)))
    items += list(extra)
    for i in range(0, len(items), 6):
        out("  " + " ".join(items[i:i + 6]))


def vec(v):
    return "(%r, %r, %r)" % tuple(v)


def points(s, ts):
    for t in ts:
        e, r, v = s.sgp4_tsince(t)
        line = "  sgp4_tsince(%r) => (%r, %s, %s)" % (t, e, vec(r), vec(v))
        if e:
            line += " " + repr(s.error_message)
        out(line)


def tlist(f):
    return [float(x) for x in f.split(",")]


# ---- tests.py's tcppver.out regeneration
def format_short_line(tsince, r, v):
    return ' %16.8f %16.8f %16.8f %16.8f %12.9f %12.9f %12.9f' % (
        tsince, r[0], r[1], r[2], v[0], v[1], v[2])


def format_long_line(satrec, tsince, mu, r, v):
    short = format_short_line(tsince, r, v)
    jd = satrec.jdsatepoch + satrec.jdsatepochF + tsince / 1440.0
    year, mon, day, hr, minute, sec = invjday(jd)
    (p, a, ecc, incl, node, argp, nu, m, arglat, truelon, lonper) = rv2coe(r, v, mu)
    return short + (
        ' %14.6f %8.6f %10.5f %10.5f %10.5f %10.5f %10.5f'
        ' %5i%3i%3i %2i:%2i:%9.6f'
    ) % (a, ecc, incl * rad, node * rad, argp * rad, nu * rad, m * rad, year, mon, day, hr,
         minute, sec)


def verify(api, grav, ops, line1, line2):
    if api == "legacy":
        satrec = io.twoline2rv(line1, line2, GOBJ[grav], ops)
    else:
        satrec = Satrec.twoline2rv(line1, line2, GRAV[grav])

    def invoke(tsince):
        if api == "legacy":
            r, v = sgp4(satrec, tsince)
            return (satrec.error, satrec.error_message), r, v
        if api == "satrec_jd":
            whole, fraction = divmod(tsince / 1440.0, 1.0)
            return satrec.sgp4(satrec.jdsatepoch + whole, satrec.jdsatepochF + fraction)
        return satrec.sgp4_tsince(tsince)

    out("%ld xx" % (satrec.satnum,))
    mu = wgs72.mu
    e, r, v = invoke(0.0)
    if isnan(r[0]) and isnan(r[1]) and isnan(r[2]):
        out("error %r" % (e,))
        out("(Use previous data line)")
        return
    out(format_short_line(0.0, r, v))
    tstart, tend, tstep = (float(field) for field in line2[69:].split())
    tsince = tstart
    while tsince <= tend:
        if tsince == tstart == 0.0:
            tsince += tstep
            continue
        e, r, v = invoke(tsince)
        if e != 0 and e != (0, None):
            out("error %r" % (e,))
            return
        out(format_long_line(satrec, tsince, mu, r, v))
        tsince += tstep
    if tsince - tend < tstep - 1e-6:
        e, r, v = invoke(tend)
        if e != 0 and e != (0, None):
            out("error %r" % (e,))
            return
        out(format_long_line(satrec, tend, mu, r, v))


def run(f):
    k = f[0]
    if k == "verify":
        out("verify(%s, %s, %s)" % (f[1], f[2], f[3]))
        verify(f[1], f[2], f[3], f[4], f[5])
    elif k == "tle":
        out("tle(%s, %r, %r)" % (f[1], f[2], f[3]))
        try:
            s = Satrec.twoline2rv(f[2], f[3], GRAV[f[1]])
        except ValueError as e:
            out("  " + exc(e))
            return
        summary(s, len(f) > 5)
        points(s, tlist(f[4]))
    elif k == "io":
        out("io(%s, %s, %r, %r)" % (f[1], f[2], f[3], f[4]))
        try:
            s = io.twoline2rv(f[3], f[4], GOBJ[f[1]], f[2])
        except ValueError as e:
            out("  " + exc(e))
            return
        summary(s, False, ["epoch=%r" % s.epoch])
        for t in tlist(f[5]):
            r, v = sgp4(s, t)
            out("  sgp4(%r) => (%s, %s) error=%r %r" % (t, vec(r), vec(v), s.error,
                                                         s.error_message))
    elif k == "export":
        out("export(%s, %r, %r)" % (f[1], f[2], f[3]))
        try:
            out("  => %r" % (export_tle(Satrec.twoline2rv(f[2], f[3], GRAV[f[1]])),))
        except ValueError as e:
            out("  " + exc(e))
    elif k == "init":
        out("init(%s)" % ", ".join(f[1:14]))
        s = Satrec()
        try:
            s.sgp4init(GRAV[f[1]], f[2], int(f[3]), float(f[4]), *[float(x) for x in f[5:14]])
        except ValueError as e:
            out("  " + exc(e))
            return
        summary(s, len(f) > 15)
        points(s, tlist(f[14]))
        try:
            out("  export_tle => %r" % (export_tle(s),))
        except ValueError as e:
            out("  export_tle => " + exc(e))
    else:
        out("%s(%s)" % (k, ", ".join(repr(x) if k in ("checksum", "from_alpha5") else x
                                     for x in f[1:])))
        try:
            if k == "jday":
                r = jday(*[int(x) for x in f[1:6]], float(f[6]))
            elif k == "extjday":
                r = ext_jday(*[int(x) for x in f[1:6]], float(f[6]))
            elif k == "invjday":
                r = invjday(float(f[1]))
            elif k == "gstime":
                r = gstime(float(f[1]))
            elif k == "days2mdhms":
                r = days2mdhms(int(f[1]), float(f[2]))
            elif k == "newtonnu":
                r = newtonnu(float(f[1]), float(f[2]))
            elif k == "rv2coe":
                x = [float(a) for a in f[1:]]
                r = rv2coe(x[0:3], x[3:6], x[6])
            elif k == "checksum":
                line = f[1] if len(f) > 1 else ""
                try:
                    ver = repr(verify_checksum(line))
                except ValueError as e:
                    ver = exc(e)
                out("  => %r %r %s" % (compute_checksum(line), fix_checksum(line), ver))
                return
            elif k == "to_alpha5":
                r = to_alpha5(int(f[1]))
            elif k == "from_alpha5":
                r = from_alpha5(f[1])
            elif k == "getgravconst":
                r = getgravconst(f[1])
            else:
                raise SystemExit("unknown job " + k)
        except (ValueError, IndexError) as e:
            out("  " + exc(e))
            return
        out("  => %r" % (r,))


with open("data/jobs.tsv", encoding="utf-8") as fh:
    for ln in fh:
        run(ln.rstrip("\n").split("\t"))
