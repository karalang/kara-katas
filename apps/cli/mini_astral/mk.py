#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, tab-separated, the first field
naming the kind.

  day <lat> <lon> <elev> <date> <tz> <dep> <elevs>
      every sun function for one observer and date, plus moonrise, moonset
      and the moon's phase. <lat>/<lon> go through dms_to_float (a float or
      51°31'N), <elev> is metres or "<height>/<distance>" for an obscuring
      feature, <tz> is "utc" or a fixed offset "+05:30", <dep> is a
      Depression name or a float, and <elevs> lists time_at_elevation calls
      as "<elevation>:<R|S>:<1|0 refraction>".
  pos <lat> <lon> <elev> <datetime> <tz>
      the sun's and the moon's zenith, azimuth and elevation at an instant
      (<tz> may be "naive").
  city <name> <date> <tz>      geocoder lookup, then the location's sun times
  group <region>               geocoder group lookup
  dms <text> <limit|none>      dms_to_float
  h2t <hours>                  hours_to_time
  t2h <h> <m> <s> <us>         time_to_hours, time_to_seconds
  refr <zenith>                refraction_at_zenith
  jd <date or datetime> <lon>  julianday (both calendars), julianday_modified,
                               julianday_2000, the Julian century, gmst, lmst
  jd2dt <jd>                   julianday_to_datetime
  dft <fraction>               day_fraction_to_time
  m2td <minutes>               minutes_to_timedelta
  mpos <jd2000>                the moon's right ascension, declination, distance
  phase <date>                 moon.phase
Run: python3 -s -P -B mk.py"""
import os
import random

R = random.Random(309)
jobs = []


def add(*f):
    jobs.append("\t".join(str(x) for x in f))


def rdate(lo=1900, hi=2100):
    y = R.randint(lo, hi)
    m = R.randint(1, 12)
    d = R.randint(1, 28 if m == 2 else 30)
    return "%04d-%02d-%02d" % (y, m, d)


def rtz():
    k = R.random()
    if k < 0.35:
        return "utc"
    mins = R.choice([-720, -600, -480, -300, -240, -210, -60, 60, 120, 180, 330, 345, 480,
                     540, 570, 600, 765, 840])
    sign = "-" if mins < 0 else "+"
    return "%s%02d:%02d" % (sign, abs(mins) // 60, abs(mins) % 60)


def relevs():
    out = []
    for _ in range(R.randint(1, 3)):
        e = R.choice([R.uniform(-18, 60), R.uniform(90, 175), 0.0, 45.0, 120.0])
        out.append("%r:%s:%d" % (round(e, 3), R.choice("RS"), R.choice([1, 1, 0])))
    return ",".join(out)


DEPS = ["CIVIL", "NAUTICAL", "ASTRONOMICAL", "6.0", "0.833", "15.5", "3"]

# Places from the library's tests and around the globe
PLACES = [
    ("51.4733", "-0.0008333", "0.0"),   # Greenwich, the default Observer
    ("51.5", "-0.1166666", "0.0"),      # London
    ("28.61", "77.2", "0.0"),           # New Delhi
    ("-33.8688", "151.2093", "58.0"),   # Sydney
    ("64.1466", "-21.9426", "0.0"),     # Reykjavik
    ("78.2232", "15.6267", "0.0"),      # Longyearbyen
    ("-77.85", "166.6667", "10.0"),     # McMurdo
    ("69.6492", "18.9553", "100.0"),    # Tromsø
    ("0.0", "0.0", "0.0"),
    ("40.7128", "-74.006", "10.0"),     # New York
    ("35.6762", "139.6503", "40.0"),    # Tokyo
    ("-54.8019", "-68.303", "0.0"),     # Ushuaia
    ("27.9881", "86.925", "8848.0"),    # Everest
    ("52°30'N", "13°25'E", "34.0"),     # Berlin, in the geocoder's form
    ("41°54'N", "12°29'E", "0.0"),
    ("33°55'S", "18°25'E", "0.0"),
    ("89.9", "45.0", "0.0"),            # clipped to 89.8
    ("-90", "-180", "0.0"),
    ("95", "200", "0.0"),               # dms_to_float limits them to ±90/±180
    ("51.5", "-0.1166666", "100/1000"),  # an obscuring feature
    ("51.5", "-0.1166666", "-50/1000"),
    ("51.5", "-0.1166666", "0/1000"),
    ("60.0", "25.0", "0.0"),
    ("-23.5", "-46.6", "760.0"),
]

FIXED_DATES = ["2015-12-01", "2015-12-25", "2016-06-21", "2019-01-01", "2020-03-20",
               "2021-12-21", "2000-01-01", "1900-03-01", "2100-12-31", "2024-02-29"]

for (lat, lon, el) in PLACES:
    for d in R.sample(FIXED_DATES, 3) + [rdate()]:
        add("day", lat, lon, el, d, rtz(), R.choice(DEPS), relevs())

for _ in range(70):
    lat = "%r" % round(R.uniform(-80, 80), 4)
    lon = "%r" % round(R.uniform(-180, 180), 4)
    el = R.choice(["0.0", "0.0", "%r" % round(R.uniform(1, 3000), 1)])
    add("day", lat, lon, el, rdate(), rtz(), R.choice(DEPS), relevs())

# Polar summers and winters, where some events do not happen at all
for lat in ["66.0", "67.5", "70.0", "75.0", "-66.0", "-70.0", "80.0", "-85.0"]:
    for d in ["2021-06-21", "2021-12-21", "2021-03-21", "2021-05-01", "2021-08-10",
              "2021-11-15"]:
        add("day", lat, "%r" % round(R.uniform(-180, 180), 2), "0.0", d, rtz(),
            R.choice(DEPS), relevs())

# The day after the UTC date: events whose local date differs
for d in ["2020-01-01", "2020-06-30", "2020-12-31"]:
    for lon, tz in [("179.9", "-12:00"), ("-179.9", "+14:00"), ("120.0", "-10:00"),
                    ("-150.0", "+12:45")]:
        add("day", "10.0", lon, "0.0", d, tz, "CIVIL", "10.0:R:1")

for _ in range(150):
    lat = "%r" % round(R.uniform(-89, 89), 4)
    lon = "%r" % round(R.uniform(-180, 180), 4)
    el = R.choice(["0.0", "%r" % round(R.uniform(1, 3000), 1), "20/500"])
    d = rdate()
    t = "%02d:%02d:%02d.%06d" % (R.randint(0, 23), R.randint(0, 59), R.randint(0, 59),
                                 R.randint(0, 999999))
    add("pos", lat, lon, el, d + "T" + t, R.choice(["naive", "utc", rtz(), rtz()]))
for t in ["00:00:00.000000", "12:00:00.000000", "23:59:59.999999"]:
    add("pos", "89.95", "0.0", "0.0", "2020-06-21T" + t, "utc")
    add("pos", "-89.95", "0.0", "0.0", "2020-06-21T" + t, "utc")
    add("pos", "0.0", "0.0", "0.0", "2020-03-20T" + t, "naive")

CITIES = ["London", "london", "LONDON", "Abu Dhabi", "Abu Dhabi,UAE",
          "abu dhabi,united arab emirates", "Abu Dhabi,Nowhere", "New Delhi",
          "Birmingham", "Birmingham,USA", "Birmingham,England", "Washington DC",
          "Avarua", "Reykjavik", "'London'", "\"London\",'England'", "London, England",
          "London,england", "nowhere", "", "Wellington", "Ushuaia", "Hobart",
          "san_francisco", "San Francisco", "Europe", "Iqaluit", "Yellowknife", "Apia",
          "Beijing", "Al Jubail", "Astana", "europe"]
for c in CITIES:
    add("city", c, R.choice(FIXED_DATES), "utc")

for g in ["Europe", "europe", "AMERICA", "Asia", "Etc", "Pacific", "Indian", "Antarctica",
          "Australia", "Africa", "Atlantic", "nowhere", "us"]:
    add("group", g)

DMS = ["51°31'N", "51°31'S", "0°06'W", "24°28'N", "51°31′N", "51°31'12\"N", "51°31'12″S",
       "51°", "51°N", "51°n", "51°w", "123°45'E", "180°00'W", "200°E", "1234°", "51°123'N",
       "51°3'N", "51°31'1\"E", "5°5'5\"S", "°31'N", "51°31'", "abc", "", " 51.5 ", "51.5",
       "-0.1166", "1e3", "-1e3", "inf", "-inf", "nan", "1_000", "+12", "12.", ".5", "0x10",
       "51°31'Nonsense", "N51°31'", "51° 31'N", "51°31'X", "999°59'59\"S", "07°32'E"]
for s in DMS:
    for lim in ["none", "90.0", "180.0"]:
        add("dms", s, lim)

for h in [0.0, 1.5, 12.25, 23.999, 23.9999999, 6.123456789, 0.0001, 18.75, 24.0, -1.5, 25.0,
          -0.25, float("nan"), float("inf")] + [round(R.uniform(0, 24), 6) for _ in range(12)]:
    add("h2t", repr(h))
for _ in range(15):
    add("t2h", R.randint(0, 23), R.randint(0, 59), R.randint(0, 59), R.randint(0, 999999))
add("t2h", 0, 0, 0, 0)
add("t2h", 23, 59, 59, 999999)
add("t2h", 24, 0, 0, 0)
add("t2h", 0, 60, 0, 0)
add("t2h", 0, 0, 61, 0)
add("t2h", 0, 0, 0, 1000000)

for z in [0.0, 5.0, 10.0, 45.0, 84.0, 84.99, 85.0, 89.0, 90.0, 90.575, 90.5, 90.833, 91.0,
          95.0, 108.0, 180.0, -10.0] + [round(R.uniform(0, 120), 4) for _ in range(12)]:
    add("refr", repr(z))

for _ in range(20):
    d = rdate(1582, 2400)
    if R.random() < 0.6:
        d += "T%02d:%02d:%02d.%06d" % (R.randint(0, 23), R.randint(0, 59), R.randint(0, 59),
                                      R.randint(0, 999999))
    add("jd", d, "%r" % round(R.uniform(-180, 180), 3))
for d in ["2000-01-01", "2000-01-01T12:00:00.000000", "1582-10-04", "1582-10-15",
          "1858-11-17T00:00:00.000000", "0001-01-01", "0001-01-01T00:00:00.000000",
          "9999-12-31T23:59:59.999999", "1900-02-28T18:00:00.000000", "2024-02-29"]:
    add("jd", d, "-0.1166666")

for jd in [2451545.0, 2451544.5, 2299160.5, 2299161.0, 2299160.0, 2415020.5, 2460000.25,
           2440587.5, 1721425.5, 1721424.5, 0.0, -1.0, 5373484.0, 5373484.4999, 2451545.75,
           2451545.999999, float("nan"), float("inf")] + \
        [round(R.uniform(2200000, 2600000), 6) for _ in range(20)]:
    add("jd2dt", repr(jd))

for f in [0.0, 0.5, 0.25, 0.999999, 0.99999999, 1.0, 1.5, -0.1, 0.123456] + \
        [round(R.random(), 7) for _ in range(8)]:
    add("dft", repr(f))

for m in [0.0, 1.0, 59.99, 720.0, 1439.9999, 1440.0, 1440.5, 2880.25, -1.0, -1440.5, 0.0001,
          123.456789, 10000.123] + [round(R.uniform(0, 3000), 5) for _ in range(10)]:
    add("m2td", repr(m))

for j in [0.0, 1.0, -36525.0, 36525.0, 7305.5, 8000.123, -10000.75] + \
        [round(R.uniform(-40000, 40000), 4) for _ in range(12)]:
    add("mpos", repr(j))

for d in ["2015-01-01", "2015-12-01", "2015-12-02", "2015-12-03", "2015-12-14", "2015-12-15",
          "2015-12-16", "2015-12-26", "2000-01-06", "1999-12-22"] + \
        [rdate(1800, 2200) for _ in range(25)]:
    add("phase", d)

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(jobs) + "\n")
print(len(jobs), "jobs")
