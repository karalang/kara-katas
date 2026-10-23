#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, fields separated by tabs.

  verify <api> <gravity> <opsmode> <line1> <line2>
      regenerate this satellite's part of the library's tcppver.out check
      (tests.py's generate_satellite_output); <api> is satrec_tsince,
      satrec_jd or legacy, and line2 carries the start/stop/step tail
  tle <gravity> <line1> <line2> <times> [full]   Satrec.twoline2rv, then sgp4_tsince
  io <gravity> <opsmode> <line1> <line2> <times>   the 1.x io.twoline2rv path
  export <gravity> <line1> <line2>             export_tle(Satrec.twoline2rv(...))
  init <gravity> <opsmode> <satnum> <epoch> <bstar> <ndot> <nddot> <ecco>
       <argpo> <inclo> <mo> <no_kozai> <nodeo> <times>   Satrec().sgp4init
  jday | extjday <y> <m> <d> <h> <mi> <s>, invjday <jd>, days2mdhms <y> <days>,
  gstime <jd>, newtonnu <ecc> <nu>, rv2coe <x> <y> <z> <vx> <vy> <vz> <mu>,
  checksum <line>, to_alpha5 <n>, from_alpha5 <s>, getgravconst <name>

<times> is a comma-separated list of minutes since epoch; "full" asks for
every attribute of the satellite record rather than the TLE-level ones. The satellites are
the library's own SGP4-VER.TLE verification set plus the special cases its
tests.py checks; the sgp4init jobs add seeded random orbits, kept only when the
pure-Python library propagates them without an arithmetic error (see
README.md, Scope).
Run: python3 -I -B mk.py"""
import math
import os
import random
import sys

sys.path.insert(0, "vendor")
from sgp4.model import Satrec  # noqa: E402

R = random.Random(308)
GRAV = {"wgs72old": 0, "wgs72": 1, "wgs84": 2}

with open("vendor/sgp4/SGP4-VER.TLE", encoding="ascii") as fh:
    raw = [ln.rstrip("\n").rstrip("\r") for ln in fh]
SATS = []
for i, ln in enumerate(raw):
    if ln.startswith("1"):
        SATS.append((ln, raw[i + 1]))

jobs = []


def times(ts):
    return ",".join(repr(float(t)) for t in ts)


# -- the tcppver.out regeneration, five ways
# (all 33 satellites the way tests.py runs them, then every eighth satellite
# through each other route)
for l1, l2 in SATS:
    jobs.append(["verify", "satrec_tsince", "wgs72", "i", l1, l2])
for k, (api, grav, ops) in enumerate([("satrec_jd", "wgs72", "i"), ("legacy", "wgs72", "i"),
                                      ("legacy", "wgs84", "a"), ("legacy", "wgs72old", "a")]):
    for l1, l2 in SATS[k::8]:
        jobs.append(["verify", api, grav, ops, l1, l2])

LINE1 = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
SPECIAL = [
    (LINE1, LINE2),
    # leading spaces in the satellite number
    ("1  4859U 21001A   21007.63955392  .00000000  00000+0  00000+0 0  9990",
     "2  4859 000.0000 000.0000 0000000 000.0000 000.0000 01.00000000    09"),
    # a 7-character international designator
    ("1 39444U 13066AE  20110.89708219  .00000236  00000-0  35029-4 0  9992",
     "2 39444  97.5597 114.3769 0059573 102.0933 258.6965 14.82098949344697"),
    # no checksums
    ("1 00058U 60013A   97142.85906518  .00000093  00000-0 +10762-4 0  274",
     "2 00058 028.3286 356.4726 0164991 158.6392 202.1128 13.4602145880282"),
    # "2019 plus 366.82 days": December 32nd
    ("1 25544U 98067A   19366.82137887  .00016717  00000-0  10270-3 0  9129",
     "2 25544  51.6392  96.6358 0005156  88.7140 271.4601 15.49497216  6061"),
    # day 0.5 of 2020: January 0th
    ("1 25544U 98067A   20000.50000000  .00016717  00000-0  10270-3 0  9129",
     "2 25544  51.6392  96.6358 0005156  88.7140 271.4601 15.49497216  6061"),
    # an exact leap day, and the last moment of a leap year
    ("1 25544U 98067A   24060.00000000  .00016717  00000-0  10270-3 0  9129",
     "2 25544  51.6392  96.6358 0005156  88.7140 271.4601 15.49497216  6061"),
    ("1 25544U 98067A   24366.99999999  .00016717  00000-0  10270-3 0  9129",
     "2 25544  51.6392  96.6358 0005156  88.7140 271.4601 15.49497216  6061"),
    # a round-trip example from tests.py, negative BSTAR exponent +1
    ("1 44542U 19061A   21180.78220369 -.00000015  00000-0 -66561+1 0  9997",
     "2 44542  54.7025 244.1098 0007981 318.8601 283.5781  1.86231125 12011"),
    # the two OMM examples in tests.py
    ("1 00005U 58002B   20287.20333880 -.00000016  00000-0 -22483-4 0  9998",
     "2 00005  34.2443 225.5254 1845686 162.2516 205.2356 10.84869164218149"),
    ("1 55123U 98067UQ  23115.44827133  .00787702  29408-3  15680-2 0  9999",
     "2 55123  51.6242 216.2930 0014649 331.8976  28.1241 15.99081912 18396"),
    # Alpha-5 satellite numbers
    ("1 A0000U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 A0000  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    ("1 Z9999U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 Z9999  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    ("1 J2931S 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 J2931  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    # an ephemeris type and a 1957 epoch
    ("1 00005U 58002B   57179.78495062  .00000023  00000-0  28098-4 2  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    # an ephemeris type that is not a digit (Satrec's int() fails)
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 X  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    # a revolution number with a space inside
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.824191574 3667"),
    # eccentricity digits with spaces
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 00005  34.2682 348.7242 18596 7 331.7664  19.3264 10.82419157413667"),
    # letters where digits belong
    ("1 00005U 58002B   0A179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    ("1 00005U 58002B   00179.78495062  .000000x3  00000-0  28098-4 0  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    ("1 00005U 58002B   00179.78495062  .00000023  00000-x  28098-4 0  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  47x3",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.8241915741366z"),
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 00005  34.26_2 348.7242 1859667 331.7664  19.3264 10.82419157413667"),
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 1e.82419157413667"),
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 inf.82419157413667"),
    # lines that break the column layout
    (LINE1.replace("23 ", "234"), LINE2),
    (LINE1, LINE2.replace(" 34", "34 ")),
    (LINE1[:60], LINE2),
    (LINE1, LINE2[:66]),
    ("2" + LINE1[1:], LINE2),
    # mismatched satellite numbers
    (LINE1, "2 00007  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413669"),
    # non-ASCII characters
    (LINE1.replace("23 ", "23\xa0"), LINE2),
    (LINE1, LINE2.replace(" 34", "\xa034")),
    (LINE1 + "é", LINE2),
    # trailing whitespace
    (LINE1 + "   ", LINE2 + " "),
    # orbits that fail: a decayed satellite and a hyperbolic eccentricity
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753",
     "2 00005  34.2682 348.7242 9999999 331.7664  19.3264 10.82419157413667"),
    ("1 00005U 58002B   00179.78495062  .00000023  00000-0  99999+2 0  4753",
     "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 16.82419157413667"),
]


def tail_times(l2):
    t0, t1, st = (float(x) for x in l2[69:].split())
    return [0.0, t0, (t0 + t1) / 2.0, t1]


# -- Satrec.twoline2rv
for l1, l2 in SATS:
    jobs.append(["tle", "wgs72", l1, l2, times(tail_times(l2)), "full"])
for grav in ["wgs72old", "wgs84"]:
    for l1, l2 in SATS[:4]:
        jobs.append(["tle", grav, l1, l2, times([0.0, 309.67110720001529, -1440.0])])
for l1, l2 in SPECIAL:
    jobs.append(["tle", "wgs72", l1, l2, times([0.0, 1440.0, -1440.0, 10080.0])])

# -- io.twoline2rv
for l1, l2 in SATS[::3]:
    jobs.append(["io", "wgs72", "i", l1, l2, times(tail_times(l2)[:3])])
    jobs.append(["io", "wgs84", "a", l1, l2, times(tail_times(l2)[1:])])
for l1, l2 in SPECIAL:
    jobs.append(["io", "wgs72old", "a", l1, l2, times([0.0, 720.0])])

# -- export_tle
for l1, l2 in SATS:
    jobs.append(["export", "wgs72", l1, l2[:69]])
for l1, l2 in SPECIAL:
    jobs.append(["export", "wgs84", l1, l2])

# -- sgp4init
VANGUARD = [2.8098e-05, 6.96919666594958e-13, 0.0, 0.1859667, 5.790416027488515,
            0.5980929187319208, 0.3373093125574321, 0.04722944544077857,
            6.08638547138321]
VEPOCH = 18441.78495062


def init_job(grav, ops, satnum, epoch, args, ts):
    return ["init", grav, ops, str(satnum), repr(epoch)] + [repr(float(a)) for a in args] + [times(ts)]


inits = []
for grav in GRAV:
    for ops in "ia":
        inits.append(init_job(grav, ops, 5, VEPOCH, VANGUARD, [0.0, 309.67110720001529, 1440.0]) + ["full"])
for satnum in [100000, 148493, 182931, 234018, 301928, 339999, 340000, 0, 99999]:
    inits.append(init_job("wgs72", "i", satnum, VEPOCH, VANGUARD, [0.0]))
inits.append(init_job("wgs72", "i", 5, VEPOCH - 365.0, VANGUARD, [0.0, 60.0]))
inits.append(init_job("wgs72", "i", 5, 18441.0, VANGUARD, [0.0, 60.0]))
inits.append(init_job("wgs72", "i", 5, 18441.123456789, VANGUARD, [0.0, 60.0]))
for k in [4, 5, 6, 8]:   # argpo, inclo, mo, nodeo out of range for export_tle
    bad = list(VANGUARD)
    bad[k] = -1.0
    inits.append(init_job("wgs84", "i", 5, VEPOCH, bad, [0.0]))
big = list(VANGUARD)
big[5] = 3.5
inits.append(init_job("wgs84", "i", 5, VEPOCH, big, [0.0]))


def propagates(job):
    s = Satrec()
    a = job[3:]
    try:
        s.sgp4init(GRAV[job[1]], job[2], int(a[0]), float(a[1]), *[float(x) for x in a[2:11]])
        for t in a[11].split(","):
            s.sgp4_tsince(float(t))
    except ValueError as e:
        return "339999" in str(e)
    except ArithmeticError:
        return False
    for name in Satrec.__slots__:
        if isinstance(getattr(s, name, 0.0), complex):
            return False
    return True


kept = 0
while kept < 40:
    revs = R.uniform(0.9, 16.5) if R.random() < 0.8 else R.uniform(0.2, 0.9)
    args = [R.uniform(-1e-3, 1e-3), R.uniform(-1e-10, 1e-10), R.choice([0.0, R.uniform(-1e-15, 1e-15)]),
            R.choice([0.0, R.uniform(0.0, 0.05), R.uniform(0.0, 0.95)]),
            R.uniform(0.0, 2 * math.pi), R.uniform(0.0, math.pi), R.uniform(0.0, 2 * math.pi),
            revs * 2 * math.pi / 1440.0, R.uniform(0.0, 2 * math.pi)]
    job = init_job(R.choice(list(GRAV)), R.choice("ia"), R.randrange(0, 340000),
                   round(R.uniform(15000.0, 30000.0), 8), args,
                   [0.0, R.uniform(-2880.0, 2880.0), R.uniform(-20000.0, 20000.0)])
    if propagates(job):
        inits.append(job)
        kept += 1
for job in inits:
    assert propagates(job[:15]), job
jobs += inits

# -- the date helpers and smaller routines
for y, m, d, h, mi, s in [(2020, 2, 11, 13, 57, 0.0), (2000, 1, 1, 12, 0, 0.0), (1957, 10, 4, 19, 28, 34.0),
                          (2024, 2, 29, 23, 59, 59.999999), (1900, 3, 1, 0, 0, 0.0), (2100, 12, 31, 6, 30, 15.5),
                          (1999, 12, 31, 24, 0, 0.0), (2021, 13, 1, 0, 0, 0.0), (2021, 0, 0, 0, 0, -1.0),
                          (1582, 10, 15, 0, 0, 0.0), (9999, 12, 31, 23, 59, 60.0)]:
    jobs.append(["jday", str(y), str(m), str(d), str(h), str(mi), repr(s)])
    jobs.append(["extjday", str(y), str(m), str(d), str(h), str(mi), repr(s)])
for jd in [2451545.0, 2458890.5, 2458890.58125, 2436116.31, 2460000.999999, 2415020.5, 2415021.0,
           2488069.5, 2451544.5, 2451544.4999999, 2433281.5, 2400000.0]:
    jobs.append(["invjday", repr(jd)])
    jobs.append(["gstime", repr(jd)])
for y, d in [(2000, 1.0), (2000, 32.0), (2000, 366.0), (2001, 365.99999999), (2019, 366.82137887),
             (2020, 0.5), (2024, 60.0), (2023, 60.0), (2000, 179.78495062), (2006, 176.82412014),
             (2100, 59.5), (2000, 1.0000000000001), (2000, 1.9999999999), (2000, -1.5)]:
    jobs.append(["days2mdhms", str(y), repr(d)])
for i in range(30):
    y = R.randrange(1957, 2057)
    jobs.append(["days2mdhms", str(y), repr(round(R.uniform(1.0, 366.0), 8))])
    jobs.append(["invjday", repr(R.uniform(2436000.0, 2470000.0))])
for e, nu in [(0.0, 1.0), (1e-9, 2.0), (0.5, 0.5), (0.5, -3.0), (0.99, 3.1), (1.0, 2.9), (1.1, 2.7),
              (1.1, 2.0), (1.5, -1.0), (1.00000001, 1.0), (2.0, 3.0), (1.0, 3.0), (0.3, 7.0)]:
    jobs.append(["newtonnu", repr(e), repr(nu)])
MU = 398600.8
RV = [(-6142.43, 2919.87, 3221.76, -3.95, -5.99, -1.36), (7000.0, 0.0, 0.0, 0.0, 7.5, 0.0),
      (7000.0, 0.0, 0.0, 0.0, 0.0, 7.5), (0.0, 0.0, 7000.0, 7.5, 0.0, 0.0), (7000.0, 0.0, 0.0, 0.0, 9.0, 3.0),
      (7000.0, 0.0, 0.0, 0.0, -7.546, 0.0), (7000.0, 0.0, 0.0, 0.0, 12.0, 1.0), (7000.0, 0.0, 0.0, 7.5, 0.0, 0.0),
      (0.0, 0.0, 0.0, 1.0, 2.0, 3.0), (-7000.0, -10.0, -50.0, 0.1, -7.0, -1.0), (7000.0, 0.0, 0.0, 0.0, 10.68, 0.0)]
VC = math.sqrt(MU / 7000.0)   # circular speed: one equatorial orbit, one inclined
RV += [(7000.0, 0.0, 0.0, 0.0, VC, 0.0), (7000.0, 0.0, 0.0, 0.0, VC * math.cos(0.5), VC * math.sin(0.5)),
       (0.0, -7000.0, 0.0, VC, 0.0, 0.0), (0.0, 0.0, -7000.0, VC * math.cos(2.0), VC * math.sin(2.0), 0.0)]
for _ in range(15):
    RV.append(tuple(R.uniform(-9000.0, 9000.0) for _ in range(3)) + tuple(R.uniform(-9.0, 9.0) for _ in range(3)))
for rv in RV:
    jobs.append(["rv2coe"] + [repr(x) for x in rv] + [repr(MU)])
for ln in [LINE1, LINE2, LINE1[:68] + "0", LINE1[:68], LINE1[:68] + "x", LINE2[:-1] + "9",
           "1 ---------", "", "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.824191574136674"]:
    jobs.append(["checksum", ln])
for l1, l2 in SATS[:8]:
    jobs.append(["checksum", l1])
    jobs.append(["checksum", l2[:69]])
for n in [0, 5, 99999, 100000, 148493, 182931, 234018, 301928, 339999, 340000, 179999, 239999, 189999]:
    jobs.append(["to_alpha5", str(n)])
for s in ["00005", "A0000", "E8493", "J2931", "P4018", "W1928", "Z9999", "H9999", "I1234", "O1234",
          " 4859", "a1234", "+1234", "1_234", "Ax", "12.5"]:
    jobs.append(["from_alpha5", s])
for name in ["wgs72old", "wgs72", "wgs84"]:
    jobs.append(["getgravconst", name])

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    for j in jobs:
        assert not any(c in f for f in j for c in "\t\r\n\\"), j
        fh.write("\t".join(j) + "\n")
print("%d jobs" % len(jobs))
