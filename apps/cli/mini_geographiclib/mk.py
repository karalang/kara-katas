#!/usr/bin/env python3
"""Writes data/jobs.tsv: one job per line, tab-separated. Inputs are literals
here (the library is not imported); most come from the library's own test
suite (the twenty WGS84 reference geodesics and the GeodSolve / Planimeter
regression cases), the rest are places, edge values and odd ellipsoids.

  geod  A F                          construct Geodesic(A, F)
  inv   ELL LAT1 LON1 LAT2 LON2 MASK Inverse
  dir   ELL LAT1 LON1 AZI1 S12 MASK  Direct
  arc   ELL LAT1 LON1 AZI1 A12 MASK  ArcDirect
  line  ELL KIND P1 P2 P3 P4 CAPS OPS
  poly  ELL POLYLINE OPS
  acc   INIT OPS

ELL is "A,F". MASK and CAPS are capability names joined by "|". KIND is Line
(P4 unused, "-"), DirectLine, ArcDirectLine or InverseLine. OPS are
";"-separated, with ":" between an op and its arguments. Floats are Python
reprs.
Run: python3 -s -P -B mk.py"""
import os

jobs = []


def r(x):
    return repr(float(x))


def ell(a, f):
    return r(a) + "," + r(f)


def job(*f):
    jobs.append("\t".join(str(x) for x in f))


NAN = float("nan")
INF = float("inf")
WGS = ell(6378137.0, 1 / 298.257223563)
SPHERE = ell(6371000.0, 0.0)
PROLATE = ell(6.4e6, -1 / 150.0)
OBLATE = ell(6378137.0, 1 / 50.0)
STD = "STANDARD"
ALL = "ALL"
ALLU = "ALL|LONG_UNROLL"
STDU = "STANDARD|LONG_UNROLL"

# --- the constructor, including every way it refuses an ellipsoid ---
for a, f in [(6378137.0, 1 / 298.257223563), (6371000.0, 0.0), (6.4e6, -1 / 150.0),
             (6378137.0, 1 / 50.0), (89.8, -1.83), (1e6, -3.0), (6.4e6, 0.1),
             (6378137.0, 1 / 298.257222101), (6.4e6, 0.99), (-1.0, 0.0), (0.0, 0.0),
             (NAN, 0.0), (INF, 0.0), (6.4e6, 1.5), (6.4e6, 1.0), (6.4e6, 2.0),
             (6.4e6, 3.0), (6.4e6, NAN), (6.4e6, -INF)]:
    job("geod", r(a), r(f))

# --- the library's twenty WGS84 reference geodesics ---
ref = [
    (35.60777, -139.44815, 111.098748429560326, -11.17491, -69.95921, 8935244.5604818305, 80.50729714281974),
    (55.52454, 106.05087, 22.020059880982801, 77.03196, 197.18234, 4105086.1713924406, 36.892740690445894),
    (-21.97856, 142.59065, -32.44456876433189, 41.84138, 98.56635, 8394328.894657671, 75.62930491011522),
    (-66.99028, 112.2363, 173.73491240878403, -12.70631, 285.90344, 11150344.2312080241, 100.278634181155759),
    (-17.42761, 173.34268, -159.033557661192928, -15.84784, 5.93557, 16076603.1631180673, 144.640108810286253),
    (32.84994, 48.28919, 150.492927788121982, -56.28556, 202.29132, 16727068.9438164461, 150.565799985466607),
    (6.96833, 52.74123, 92.581585386317712, -7.39675, 206.17291, 17102477.2496958388, 154.147366239113561),
    (-50.56724, -16.30485, -105.439679907590164, -33.56571, -94.97412, 6455670.5118668696, 58.083719495371259),
    (-58.93002, -8.90775, 140.965397902500679, -8.91104, 133.13503, 11756066.0219864627, 105.755691241406877),
    (-68.82867, -74.28391, 93.774347763114881, -50.63005, -8.36685, 3956936.926063544, 35.572254987389284),
    (-10.62672, -32.0898, -86.426713286747751, 5.883, -134.31681, 11470869.3864563009, 103.387395634504061),
    (-21.76221, 166.90563, 29.319421206936428, 48.72884, 213.97627, 9098627.3986554915, 81.963476716121964),
    (-19.79938, -174.47484, 71.167275780171533, -11.99349, -154.35109, 2319004.8601169389, 20.896611684802389),
    (-11.95887, -116.94513, 92.712619830452549, 4.57352, 7.16501, 13834722.5801401374, 124.688684161089762),
    (-87.85331, 85.66836, -65.120313040242748, 66.48646, 16.09921, 17286615.3147144645, 155.58592449699137),
    (1.74708, 128.32011, -101.584843631173858, -11.16617, 11.87109, 12942901.1241347408, 116.650512484301857),
    (-25.72959, -144.90758, -153.647468693117198, -57.70581, -269.17879, 9413446.7452453107, 84.664533838404295),
    (-41.22777, 122.32875, 14.285113402275739, -7.57291, 130.37946, 3812686.035106021, 34.34330804743883),
    (11.01307, 138.25278, 79.43682622782374, 6.62726, 247.05981, 11911190.819018408, 107.341669954114577),
    (-29.47124, 95.14681, -163.779130441688382, -27.46601, -69.15955, 13487015.8381145492, 121.294026715742277),
]
for i, (la1, lo1, az1, la2, lo2, s12, a12) in enumerate(ref):
    job("inv", WGS, r(la1), r(lo1), r(la2), r(lo2), ALLU if i % 2 else ALL)
    job("dir", WGS, r(la1), r(lo1), r(az1), r(s12), ALLU if i % 3 else ALL)
    job("arc", WGS, r(la1), r(lo1), r(az1), r(a12), ALL if i % 3 else ALLU)

# --- GeodSolve regression cases (WGS84 unless an ellipsoid is given) ---
for e, la1, lo1, la2, lo2, m in [
    (WGS, 40.6, -73.8, 49.01666667, 2.55, STD),
    (PROLATE, 0.07476, 0, -0.07476, 180, STD), (PROLATE, 0.1, 0, -0.1, 180, STD),
    (WGS, 36.493349428792, 0, 36.49334942879201, 0.0000008, STD),
    (WGS, 88.202499451857, 0, -88.202499451857, 179.981022032992859592, ALL),
    (WGS, 89.262080389218, 0, -89.262080389218, 179.992207982775375662, ALL),
    (WGS, 89.333123580033, 0, -89.333123580032997687, 179.99295812360148422, ALL),
    (WGS, 56.320923501171, 0, -56.320923501171, 179.664747671772880215, ALL),
    (WGS, 52.784459512564, 0, -52.784459512563990912, 179.634407464943777557, ALL),
    (WGS, 48.522876735459, 0, -48.52287673545898293, 179.599720456223079643, ALL),
    (ell(89.8, -1.83), 0, 0, -10, 160, ALL),
    (WGS, 0, 0, 1, NAN, STD),
    (ell(6.4e6, 0), 1, 2, 3, 4, "AREA"),
    (WGS, 0, 539, 0, 181, STD), (WGS, 0, 539, 0, 181, STDU),
    (WGS, 0, 0, 0, 179, ALL), (WGS, 0, 0, 0, 179.5, ALL), (WGS, 0, 0, 0, 180, ALL),
    (WGS, 0, 0, 1, 180, ALL),
    (ell(6.4e6, 0), 0, 0, 0, 179, ALL), (ell(6.4e6, 0), 0, 0, 0, 180, ALL),
    (ell(6.4e6, 0), 0, 0, 1, 180, ALL),
    (ell(6.4e6, -1 / 300.0), 0, 0, 0, 179, ALL), (ell(6.4e6, -1 / 300.0), 0, 0, 0, 180, ALL),
    (ell(6.4e6, -1 / 300.0), 0, 0, 0.5, 180, ALL), (ell(6.4e6, -1 / 300.0), 0, 0, 1, 180, ALL),
    (WGS, NAN, 0, 0, 90, ALL), (WGS, NAN, 0, 90, 9, ALL),
    (WGS, 5, 0.00000000000001, 10, 180, ALL),
    (WGS, 54.1589, 15.3872, 54.1591, 15.3877, ALL),
    (WGS, -(41 + 19 / 60.0), 174 + 49 / 60.0, 40 + 58 / 60.0, -(5 + 30 / 60.0), STD),
    (WGS, 27.2, 0.0, -27.1, 179.5, ALL),
    (WGS, 0, 0, 0, 90, "GEODESICSCALE"), (WGS, 0, 0, 1e-6, 1e-6, "GEODESICSCALE"),
    (WGS, 20.001, 0, 20.001, 0, ALL), (WGS, 90, 0, 90, 180, ALL),
    (WGS, 37.757540000000006, -122.47018, 37.75754, -122.470177, ALL),
    (WGS, 0, 0, NAN, 90, ALL),
    (ell(6378137, 1 / 298.257222101), 0, 0, 60.0832522871723, 89.8492185074635, "AREA"),
    (WGS, 45.0, 0.0, -45.0, 179.572719, ALL),
    (ell(1e6, -3), 30, 0, 30, 180, ALL), (ell(1e6, -3), 30.61, 0, 30.61, 180, ALL),
]:
    job("inv", e, r(la1), r(lo1), r(la2), r(lo2), m)

# --- places, masks and other ellipsoids ---
places = [
    (51.4778, -0.0015, 40.71435, -74.00597),     # Greenwich to New York
    (-33.8568, 151.2153, 35.6812, 139.7671),     # Sydney to Tokyo
    (40.63972222, -73.77888889, 1.35917, 103.98944),  # JFK to Singapore
    (-41.32, 174.81, 40.96, -5.5),               # Wellington to Salamanca
    (64.1466, -21.9426, -77.8463, 166.6683),     # Reykjavik to McMurdo
    (0.0, -0.0, -0.0, 0.0), (90.0, 0.0, -90.0, 0.0), (-90.0, 45.0, -90.0, -135.0),
    (10.0, 720.0, -10.0, -540.5), (89.99999999, 0.0, -89.99999999, 179.99999),
    (91.0, 0.0, 10.0, 10.0), (0.0, 0.0, 1e-300, 0.0), (1e-20, 0.0, -1e-20, 180.0),
]
for e in [WGS, SPHERE, PROLATE, OBLATE, ell(1e6, -3), ell(6.4e6, 0.99)]:
    for la1, lo1, la2, lo2 in places:
        job("inv", e, r(la1), r(lo1), r(la2), r(lo2), ALLU if e != WGS else ALL)
for m in ["EMPTY", "LATITUDE", "LONGITUDE", "AZIMUTH", "DISTANCE", "REDUCEDLENGTH",
          "AREA|LONG_UNROLL", "DISTANCE_IN", "LATITUDE|AZIMUTH|REDUCEDLENGTH"]:
    job("inv", WGS, r(-41.32), r(174.81), r(40.96), r(-5.5), m)
    job("dir", WGS, r(-41.32), r(174.81), r(161.0), r(19959679.0), m)
    job("arc", WGS, r(-41.32), r(174.81), r(161.0), r(179.6), m)

for e, la1, lo1, az1, s12, m in [
    (WGS, 40.63972222, -73.77888889, 53.5, 5850e3, STD),
    (WGS, 0.01777745589997, 30, 0, 10e6, STD),
    (PROLATE, 1, 2, 3, 4, "AREA"),
    (WGS, 40, -75, -10, 2e7, STDU), (WGS, 40, -75, -10, 2e7, STD),
    (ell(6.4e6, 0.1), 1, 2, 10, 5e6, ALL),
    (WGS, 45, 0, -0.000000000000000003, 1e7, STDU),
    (WGS, 90, 10, 180, -1e6, ALL),
    (WGS, 0, 0, 90, INF, ALL), (WGS, 0, 0, 90, NAN, ALL), (WGS, 0, 0, INF, 1000, ALL),
    (WGS, 0, 0, NAN, 1000, ALL), (WGS, 0, INF, 90, 1000, ALL), (WGS, 0, NAN, 90, 1000, ALL),
    (WGS, INF, 0, 90, 1000, ALL), (WGS, NAN, 0, 90, 1000, ALL),
    (WGS, 0, 0, 90, 0, ALL), (WGS, -90, 30, 0, 1e6, ALLU), (WGS, 10, 20, 30, -4e7, ALLU),
    (SPHERE, 10, 20, 30, 1e7, ALLU), (OBLATE, 10, 20, 30, 1e7, ALLU),
    (OBLATE, -60, 170, -170, 3e7, ALLU), (ell(1e6, -3), 30, 0, 45, 5e6, ALLU),
    (ell(6.4e6, 0.99), 30, 0, 45, 1e5, ALLU), (ell(89.8, -1.83), 0, 0, 120, 300, ALL),
]:
    job("dir", e, r(la1), r(lo1), r(az1), r(s12), m)
for e, la1, lo1, az1, a12, m in [
    (WGS, 0, 0, 90, 180, ALL), (WGS, 0, 0, 0, 360, ALLU), (WGS, 45, 45, 45, -720.5, ALLU),
    (WGS, 0, 0, 90, NAN, ALL), (WGS, 0, 0, 90, INF, ALL), (SPHERE, 30, 60, -30, 90, ALL),
    (PROLATE, 30, 60, -30, 90, ALL), (OBLATE, 30, 60, -30, 90, ALL), (ell(1e6, -3), 30, 0, 45, 90, ALLU),
]:
    job("arc", e, r(la1), r(lo1), r(az1), r(a12), m)

# --- GeodesicLine: each constructor, then a list of calls on the line ---
for e, kind, p, caps, ops in [
    (WGS, "Line", (40, -75, -10, None), "STANDARD|DISTANCE_IN",
     ["attrs", "pos:2e7:STANDARD|LONG_UNROLL", "pos:2e7:STANDARD", "arcpos:100:STANDARD"]),
    (WGS, "InverseLine", (45, 0, 80, -0.000000000000000003), "STANDARD|DISTANCE_IN",
     ["attrs", "pos:1e7:STANDARD|LONG_UNROLL"]),
    (WGS, "InverseLine", (30, -0.000000000000000001, -31, 180), "ALL",
     ["attrs", "pos:1e7:ALL|LONG_UNROLL", "pos:2e7:ALL|LONG_UNROLL"]),
    (WGS, "InverseLine", (-5, -0.000000000000002, -10, 180), "STANDARD|DISTANCE_IN",
     ["attrs", "pos:2e7:STANDARD|LONG_UNROLL", "half:STANDARD|LONG_UNROLL"]),
    (WGS, "DirectLine", (1, 2, 45, 1e7), "STANDARD|DISTANCE_IN",
     ["attrs", "half:STANDARD|LONG_UNROLL", "arcpos:-50:ALL"]),
    (WGS, "Line", (1, 2, 90, None), "LATITUDE",
     ["attrs", "pos:1000:EMPTY", "pos:1000:ALL", "arcpos:10:ALL", "setd:5000", "attrs", "seta:5", "attrs"]),
    (WGS, "ArcDirectLine", (10, 20, 30, 100), "ALL",
     ["attrs", "arcpos:50:ALL", "seta:-30", "attrs", "setd:3e6", "attrs", "half:ALL"]),
    (OBLATE, "Line", (10, 20, 30, None), "ALL",
     ["attrs", "pos:5e6:ALL", "pos:-1e7:ALL|LONG_UNROLL", "arcpos:200:ALL", "setd:4e7", "attrs"]),
    (PROLATE, "DirectLine", (-20, 170, 100, 3e7), "ALL|DISTANCE_IN",
     ["attrs", "half:ALL", "pos:0:ALL", "pos:-1:ALL"]),
    (SPHERE, "InverseLine", (0, 0, 0, 90), "ALL",
     ["attrs", "pos:1e6:ALL", "arcpos:45:ALL|LONG_UNROLL"]),
    (ell(1e6, -3), "InverseLine", (30, 0, 30, 180), "ALL",
     ["attrs", "half:ALL", "arcpos:90:ALL"]),
    (WGS, "Line", (90, 0, 180, None), "ALL", ["attrs", "pos:1e6:ALL", "pos:2e7:ALL|LONG_UNROLL"]),
    (WGS, "InverseLine", (20.001, 0, 20.001, 0), "ALL", ["attrs", "pos:10:ALL"]),
]:
    args = [r(x) if x is not None else "-" for x in p]
    job("line", e, kind, *args, caps, ";".join(ops))

# --- PolygonArea ---
def pts(points):
    return ["pt:%s:%s" % (r(la), r(lo)) for la, lo in points]


C = ["compute:False:True"]
CC = ["compute:False:True", "compute:False:False", "compute:True:True", "compute:True:False"]
for polyline, ops in [
    (False, pts([[89, 0], [89, 90], [89, 180], [89, 270]]) + C),
    (False, pts([[-89, 0], [-89, 90], [-89, 180], [-89, 270]]) + C),
    (False, pts([[0, -1], [-1, 0], [0, 1], [1, 0]]) + CC),
    (False, pts([[90, 0], [0, 0], [0, 90]]) + C),
    (True, pts([[90, 0], [0, 0], [0, 90]]) + C),
    (False, pts([[89, 0.1], [89, 90.1], [89, -179.9]]) + C),
    (False, pts([[9, -0.00000000000001], [9, 180], [9, 0]]) + C),
    (False, pts([[9, 0.00000000000001], [9, 0], [9, 180]]) + C),
    (False, pts([[9, 0.00000000000001], [9, 180], [9, 0]]) + C),
    (False, pts([[9, -0.00000000000001], [9, 0], [9, 180]]) + C),
    (False, pts([[66.562222222, 0], [66.562222222, 180], [66.562222222, 360]]) + C),
    (False, pts([[66.562222222, -0.0], [66.562222222, -180], [66.562222222, -360]]) + C),
    (False, pts([[89, -360], [89, -240], [89, -120], [89, 0], [89, 120], [89, 240]]) + C),
    (False, pts([[2, 1], [1, 2]]) + ["testpt:3:3:False:True", "testpt:3:3:False:False",
                                     "testpt:3:3:True:True", "testpt:3:3:True:False",
                                     "testedge:45:157000:False:True", "testedge:45:157000:True:False"]
     + pts([[3, 3]]) + CC),
    (False, C + ["testpt:1:1:False:True", "testedge:90:1000:False:True"] + pts([[1, 1]]) + C + ["num"]),
    (True, C + ["testpt:1:1:False:True", "testedge:90:1000:False:True"] + pts([[1, 1]]) + C
     + ["testedge:90:1000:False:True", "testpt:2:2:False:True", "num"]),
    (False, pts([[45, 60], [45, 180], [45, -60]] * 3 + [[45, 60], [45, 180]])
     + ["testpt:45:-60:False:True", "testpt:45:-60:False:False", "testpt:45:-60:True:True",
        "testpt:45:-60:True:False", "testedge:39.2144607176828184218:8420705.40957178156285:False:True",
        "testedge:39.2144607176828184218:8420705.40957178156285:True:False"] + pts([[45, -60]]) + CC),
    (False, ["pt:0.0:0.0", "edge:90:1000", "edge:0:1000", "edge:-90:1000"] + C + ["num"]),
    (True, ["edge:90:1000", "pt:10.0:20.0", "edge:90:1e6", "edge:180:1e6", "testedge:0:5e5:False:True"] + C + ["num"]),
    (False, ["pt:10.0:20.0", "edge:720:1e6", "edge:-90:2e6", "pt:-10.0:-170.0"] + CC + ["clear", "num"]
     + pts([[0, 0], [0, 120], [0, -120]]) + CC),
    (False, pts([[50.0, -1.5], [51.0, -1.5], [51.0, 0.5], [50.0, 0.5]]) + CC + ["testpt:50.5:-2.0:False:True"]),
    (False, pts([[NAN, 0], [10, 10], [20, 0]]) + C),
]:
    job("poly", WGS, polyline, ";".join(ops))
for e in [SPHERE, PROLATE, OBLATE]:
    job("poly", e, False, ";".join(pts([[0, 0], [0, 90], [90, 0]]) + CC + ["testedge:45:1e6:False:True"]))
    job("poly", e, True, ";".join(pts([[0, 0], [0, 90], [90, 0]]) + C + ["testpt:-10:10:False:True"]))

# --- Accumulator ---
for init, ops in [
    ("0.0", ["add:1e16", "add:1.0", "add:1.0", "sum:0.0", "add:-1e16", "sum:0.0", "sum:0.5"]),
    ("0.1", ["add:0.2", "add:0.3", "sum:0.0", "neg", "sum:0.0", "add:0.6", "sum:0.0"]),
    ("1e20", ["add:3.0", "rem:7.0", "sum:0.0", "set:2.5", "sum:1.0", "add:-2.5", "sum:0.0"]),
    ("-5.5", ["rem:360.0", "add:725.25", "rem:360.0", "sum:0.0", "neg", "sum:-0.0"]),
    ("nan", ["add:1.0", "sum:0.0", "set:inf", "add:-inf", "sum:0.0"]),
]:
    job("acc", init, ";".join(ops))

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(jobs) + "\n")
print(len(jobs), "jobs")
