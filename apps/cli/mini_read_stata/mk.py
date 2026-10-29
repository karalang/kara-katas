"""Writes data/: the .dta files the jobs read, each shaped like a file a
real program wrote, and data/jobs.txt, one job per line. oracle.py runs
each job on pandas' read_stata and StataReader, mini_read_stata.kara on
its own port.

Some files are written by pandas' to_stata, as a Python pipeline would
write them. The rest are written here byte by byte, as Stata itself and
the older tools wrote them: every format pandas reads (104 to 119), both
byte orders, the extended missing values .a to .z that pandas never
writes, value labels with their text out of order, strLs in binary and
text, and expansion fields to skip. Every timestamp is fixed, so the
bytes are the same on every run.

Run: python3 -s -P -B mk.py"""
import datetime
import gzip
import io
import os
import shutil
import struct
import warnings
import zipfile

import numpy as np
import pandas as pd

warnings.simplefilter("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
shutil.rmtree(DATA, ignore_errors=True)
os.makedirs(DATA)

STAMP = datetime.datetime(2024, 10, 1, 9, 30)


def put(name, data):
    with open(os.path.join(DATA, name), "wb") as f:
        f.write(data)


# ---------------------------------------------------------------- a writer
# Missing values: k = 0 is ".", k = 1..26 are ".a" to ".z".


def miss(k=0):
    return ("miss", k)


def enc_num(typ, v, bo, version):
    if isinstance(v, tuple) and v[0] == "miss":
        k = v[1]
        if version <= 111:
            # the old formats have one missing value, just past the range
            ints = {"b": 127, "h": 32767, "l": 2147483647}
            if typ in ints:
                v = ints[typ]
            elif typ == "f":
                return struct.pack(bo + "I", 0x7F000000)
            elif version <= 105:
                return struct.pack(bo + "d", 2.0 ** 333)
            else:
                return struct.pack(bo + "Q", 0x7FE0000000000000)
        else:
            if typ == "b":
                v = 101 + k
            elif typ == "h":
                v = 32741 + k
            elif typ == "l":
                v = 2147483621 + k
            elif typ == "f":
                return struct.pack(bo + "I", 0x7F000000 + k * 0x800)
            else:
                return struct.pack(bo + "Q", 0x7FE0000000000000 + k * 0x10000000000)
    if isinstance(v, tuple) and v[0] == "bits":
        return struct.pack(bo + ("I" if typ == "f" else "Q"), v[1])
    code = {"b": "b", "h": "h", "l": "i", "f": "f", "d": "d"}[typ]
    return struct.pack(bo + code, v)


def pad(b, n):
    assert len(b) <= n, (b, n)
    return b + b"\x00" * (n - len(b))


class Var:
    def __init__(self, name, typ, fmt, label="", lbl=""):
        self.name, self.typ, self.fmt, self.label, self.lbl = name, typ, fmt, label, lbl


def old_typecode(typ, version):
    if isinstance(typ, int):
        return typ + 127 if version < 111 else typ
    if version < 111:
        return {"b": 98, "h": 105, "l": 108, "f": 102, "d": 100}[typ]
    return {"b": 251, "h": 252, "l": 253, "f": 254, "d": 255}[typ]


def row_bytes(vars, row, bo, version, codec, strl_keys=None):
    out = b""
    for j, (v, x) in enumerate(zip(vars, row)):
        if isinstance(v.typ, int):
            raw = x if isinstance(x, bytes) else x.encode(codec)
            out += pad(raw, v.typ)
        elif v.typ == "L":
            out += strl_keys[j]
        else:
            out += enc_num(v.typ, x, bo, version)
    return out


def old_value_labels(tables, bo, version, codec):
    out = b""
    for name, pairs, order in tables:
        if version <= 105:
            out += struct.pack(bo + "H", len(pairs))
            out += pad(name.encode(codec), 9) + b"\x00"
            out += b"".join(struct.pack(bo + "h", k) for k, _ in pairs)
            # the old tables hold 8 bytes a label: Stata cut longer ones
            out += b"".join(pad(t.encode(codec)[:8], 8) for _, t in pairs)
        else:
            out += new_label_table(name, pairs, order, bo, 9 if version == 108 else 33, codec)
    return out


def new_label_table(name, pairs, order, bo, namelen, codec):
    # `order` is the order the texts are stored in; the offsets say where
    # each one starts, so a reader must not assume they ascend.
    texts = {}
    blob = b""
    for i in order:
        texts[i] = len(blob)
        blob += pairs[i][1].encode(codec) + b"\x00"
    n = len(pairs)
    body = struct.pack(bo + "i", n) + struct.pack(bo + "i", len(blob))
    body += b"".join(struct.pack(bo + "i", texts[i]) for i in range(n))
    body += b"".join(struct.pack(bo + "i", pairs[i][0]) for i in range(n))
    body += blob
    return struct.pack(bo + "i", len(body)) + pad(name.encode(codec), namelen) + b"\x00" * 3 + body


def old_dta(version, bo, label, stamp, vars, rows, tables=(), expansion=(), filetype=1):
    codec = "latin-1"
    b = struct.pack("B", version)
    b += struct.pack("B", 1 if bo == ">" else 2) + struct.pack("B", filetype) + b"\x00"
    b += struct.pack(bo + "H", len(vars))
    b += struct.pack(bo + "I", len(rows))
    b += pad(label.encode(codec), 81 if version > 105 else 32)
    if version >= 105:
        b += pad(stamp.encode(codec), 18)
    b += bytes(old_typecode(v.typ, version) for v in vars)
    nl = 33 if version > 108 else 9
    b += b"".join(pad(v.name.encode(codec), nl) for v in vars)
    b += b"\x00" * (2 * (len(vars) + 1))
    fl = 49 if version > 113 else (12 if version > 104 else 7)
    b += b"".join(pad(v.fmt.encode(codec), fl) for v in vars)
    b += b"".join(pad(v.lbl.encode(codec), nl) for v in vars)
    vl = 81 if version > 105 else 32
    b += b"".join(pad(v.label.encode(codec), vl) for v in vars)
    if version > 104:
        for typ, data in expansion:
            b += struct.pack("b", typ)
            b += struct.pack(bo + ("i" if version > 108 else "h"), len(data)) + data
        b += b"\x00" + (b"\x00" * (4 if version > 108 else 2))
    for row in rows:
        b += row_bytes(vars, row, bo, version, codec)
    b += old_value_labels(tables, bo, version, codec)
    return b


def new_dta(version, bo, label, stamp, vars, rows, tables=(), strls=None, chars=b""):
    codec = "utf-8" if version >= 118 else "latin-1"
    nl = 129 if version >= 118 else 33
    o = io.BytesIO()
    pos = {}

    def w(x):
        o.write(x if isinstance(x, bytes) else x.encode("latin-1"))

    def mark(k):
        pos[k] = o.tell()

    w("<stata_dta><header><release>")
    w(str(version))
    w("</release><byteorder>")
    w("MSF" if bo == ">" else "LSF")
    w("</byteorder><K>")
    w(struct.pack(bo + ("I" if version == 119 else "H"), len(vars)))
    w("</K><N>")
    w(struct.pack(bo + ("I" if version == 117 else "Q"), len(rows)))
    w("</N><label>")
    lab = label.encode(codec)
    w(struct.pack(bo + ("B" if version == 117 else "H"), len(lab)) + lab)
    w("</label><timestamp>")
    st = stamp.encode(codec)
    w(struct.pack("B", len(st)) + st)
    w("</timestamp></header>")
    mark("map")
    w("<map>")
    map_at = o.tell()
    w(b"\x00" * (8 * 14))
    w("</map>")
    mark("variable_types")
    w("<variable_types>")
    codes = {"b": 65530, "h": 65529, "l": 65528, "f": 65527, "d": 65526, "L": 32768}
    for v in vars:
        w(struct.pack(bo + "H", v.typ if isinstance(v.typ, int) else codes[v.typ]))
    w("</variable_types>")
    mark("varnames")
    w("<varnames>")
    for v in vars:
        w(pad(v.name.encode(codec), nl))
    w("</varnames>")
    mark("sortlist")
    w("<sortlist>")
    w(b"\x00" * ((4 if version == 119 else 2) * (len(vars) + 1)))
    w("</sortlist>")
    mark("formats")
    w("<formats>")
    for v in vars:
        w(pad(v.fmt.encode(codec), 57 if version >= 118 else 49))
    w("</formats>")
    mark("value_label_names")
    w("<value_label_names>")
    for v in vars:
        w(pad(v.lbl.encode(codec), nl))
    w("</value_label_names>")
    mark("variable_labels")
    w("<variable_labels>")
    for v in vars:
        w(pad(v.label.encode(codec), 321 if version >= 118 else 81))
    w("</variable_labels>")
    mark("characteristics")
    w("<characteristics>")
    w(chars)
    w("</characteristics>")
    mark("data")
    w("<data>")
    # strL keys: (v, o) is (variable, observation), both 1-based
    gso = []
    for i, row in enumerate(rows):
        keys = {}
        for j, (v, x) in enumerate(zip(vars, row)):
            if v.typ != "L":
                continue
            if x is None:
                vv, oo = 0, 0
            elif isinstance(x, tuple) and x[0] == "ref":
                vv, oo = x[1], x[2]
            else:
                vv, oo = j + 1, i + 1
                gso.append((vv, oo, x))
            if version == 117:
                keys[j] = struct.pack(bo + "II", vv, oo)
            elif bo == "<":
                vs = 2 if version == 118 else 3
                keys[j] = struct.pack("<Q", vv | (oo << (8 * vs)))
            else:
                vs = 2 if version == 118 else 3
                keys[j] = struct.pack(">Q", (vv << (8 * (8 - vs))) | oo)
        w(row_bytes(vars, row, bo, version, codec, keys))
    w("</data>")
    mark("strls")
    w("<strls>")
    for vv, oo, x in gso:
        w("GSO")
        if version == 117:
            w(struct.pack(bo + "II", vv, oo))
        else:
            w(struct.pack(bo + "IQ", vv, oo))
        if isinstance(x, bytes):
            w(struct.pack("B", 129) + struct.pack(bo + "I", len(x)) + x)
        else:
            t = x.encode(codec) + b"\x00"
            w(struct.pack("B", 130) + struct.pack(bo + "I", len(t)) + t)
    w("</strls>")
    mark("value_labels")
    w("<value_labels>")
    for name, pairs, order in tables:
        w("<lbl>")
        w(new_label_table(name, pairs, order, bo, nl, codec))
        w("</lbl>")
    w("</value_labels>")
    mark("end")
    w("</stata_dta>")
    mark("eof")
    order = ["map", "variable_types", "varnames", "sortlist", "formats",
             "value_label_names", "variable_labels", "characteristics", "data",
             "strls", "value_labels", "end", "eof"]
    o.seek(map_at)
    o.write(struct.pack(bo + "Q", 0))
    for k in order:
        o.write(struct.pack(bo + "Q", pos[k]))
    return o.getvalue()


# ---------------------------------------------------------------- 1
# hh_survey_w3.dta: a household survey's third wave as Stata 15 saves it
# (format 118, UTF-8): value labels for region, sex, education and the
# yes/no questions, with the codes .a "refused" and .b "don't know" in
# every numeric type, a float income, an interview date (%td), the
# moment the tablet synced (%tc), and names with accents.

YESNO = [(0, "No"), (1, "Yes")]
REGION = [(1, "North"), (2, "South"), (3, "East"), (4, "West"), (5, "Capital")]
SEX = [(1, "Male"), (2, "Female")]
EDUC = [(1, "None"), (2, "Primary"), (3, "Secondary"), (4, "Tertiary")]

hh_vars = [
    Var("hhid", "l", "%12.0g", "Household ID"),
    Var("region", "b", "%8.0g", "Region of residence", "region"),
    Var("head_name", 24, "%24s", "Name of household head"),
    Var("head_sex", "b", "%8.0g", "Sex of head", "sex"),
    Var("head_age", "b", "%8.0g", "Age of head (years)"),
    Var("educ", "b", "%8.0g", "Highest level completed", "educ"),
    Var("hhsize", "h", "%8.0g", "Household size"),
    Var("income", "f", "%9.0g", "Monthly income (local currency)"),
    Var("water", "b", "%8.0g", "Piped water in dwelling", "yesno"),
    Var("weight", "d", "%10.0g", "Sampling weight"),
    Var("int_date", "l", "%td", "Interview date"),
    Var("synced", "d", "%tc", "Tablet sync time"),
]


def td(y, m, d):
    return (datetime.date(y, m, d) - datetime.date(1960, 1, 1)).days


def tc(*a):
    return int((datetime.datetime(*a) - datetime.datetime(1960, 1, 1)).total_seconds() * 1000)


hh_rows = [
    (10101, 1, "José Álvarez", 1, 47, 3, 5, 1250.5, 1, 312.75, td(2024, 3, 4), float(tc(2024, 3, 4, 18, 2, 11) + 250)),
    (10102, 1, "Amaru Quispe", 1, 62, 2, 7, 640.0, 0, 312.75, td(2024, 3, 4), float(tc(2024, 3, 4, 18, 2, 11) + 250)),
    (10203, 2, "Lucía Ñahui", 2, 35, 4, 3, 2310.25, 1, 288.1, td(2024, 3, 5), float(tc(2024, 3, 6, 7, 45, 0))),
    (10204, 2, "Rosa Mamani", 2, miss(1), 2, 4, miss(1), 1, 288.1, td(2024, 3, 5), float(tc(2024, 3, 6, 7, 45, 0))),
    (10305, 3, "Ewa Kowalczyk", 2, 29, miss(2), 2, miss(2), miss(1), 301.4, td(2024, 3, 7), miss()),
    (10306, 3, "Thắng Nguyễn", 1, 51, 3, miss(1), 980.0, 1, 301.4, td(2024, 3, 7), float(tc(2024, 3, 8, 12, 0, 0))),
    (10407, 4, "Søren Dahl", 1, 70, 1, 1, 410.75, miss(2), 275.0, miss(), float(tc(2024, 3, 9, 9, 15, 30) + 5)),
    (10408, 4, "Zainab Bello", 2, 44, 3, 6, 1875.0, 1, 275.0, td(2024, 3, 9), float(tc(2024, 3, 9, 9, 15, 30) + 5)),
    (10509, 5, "Chen Wei", 1, 38, 4, 4, 5120.5, 1, 260.25, td(2024, 3, 11), float(tc(2024, 3, 11, 20, 59, 59) + 999)),
    (10510, 5, "Ana-María Oyarzún", 2, miss(1), miss(1), 3, miss(1), 0, 260.25, td(2024, 3, 11), float(tc(2024, 3, 11, 20, 59, 59) + 999)),
    (10511, 9, "Unknown", miss(), 0, 9, 0, 0.0, 9, 1.0, td(2024, 3, 12), miss(1)),
]

put("hh_survey_w3.dta", new_dta(
    118, "<", "Household Survey Wave 3 (2024), public use", "01 Oct 2024 09:30",
    hh_vars, hh_rows,
    tables=[("region", REGION, [4, 0, 2, 1, 3]), ("sex", SEX, [0, 1]),
            ("educ", EDUC, [3, 2, 1, 0]), ("yesno", YESNO, [1, 0])]))

# ---------------------------------------------------------------- 2
# clinic_visits.dta: a clinic's visit log exported by pandas to_stata
# (format 117, big-endian, as a Python ETL job on a POWER box would
# write it), with the index written, a categorical diagnosis, a strL
# for free-text notes, dates as %td and %tc, int64 ids that fit int32,
# a bool, and NaN in float columns.

visits = pd.DataFrame({
    "visit_id": np.array([900001, 900002, 900003, 900004, 900005, 900006], dtype=np.int64),
    "patient": ["P-0193", "P-0045", "P-0193", "P-0310", "P-0045", "P-0777"],
    "seen": pd.to_datetime(["2024-07-01 08:15", "2024-07-01 09:40", "2024-07-02 14:05",
                            "2024-07-03 10:30", "2024-07-08 16:55", "2024-07-09 11:20"]),
    "dob": pd.to_datetime(["1958-02-11", "1990-12-30", "1958-02-11", "2019-06-01",
                           "1990-12-30", "1944-09-17"]),
    "dx": pd.Categorical(["hypertension", "asthma", "hypertension", "otitis",
                          "asthma", "copd"]),
    "sbp": np.array([152, 118, 147, 96, 121, 139], dtype=np.int16),
    "temp_c": np.array([36.8, 37.1, np.nan, 38.4, 36.9, 37.0], dtype=np.float32),
    "bmi": [31.2, 22.85, 30.9, np.nan, 23.0, 19.75],
    "followup": [True, False, True, True, False, True],
    "notes": ["BP still high; increase amlodipine to 10 mg.",
              "Inhaler technique reviewed.",
              "",
              "Left ear, amoxicillin 7 days. Parent informed about \"red flags\".",
              "No wheeze today.",
              "Spirometry booked; FEV1/FVC 0.62 last time. " * 5],
})
visits.index = pd.RangeIndex(100, 106)
buf = io.BytesIO()
visits.to_stata(buf, version=117, byteorder="big", time_stamp=STAMP,
                convert_dates={"seen": "tc", "dob": "td"}, convert_strl=["notes"],
                data_label="Clinic visits, July 2024",
                variable_labels={"sbp": "Systolic BP (mmHg)", "temp_c": "Temperature (C)",
                                 "dx": "Primary diagnosis"})
put("clinic_visits.dta", buf.getvalue())

# ---------------------------------------------------------------- 3
# cpi_regions.dta: a statistics office's price index by region, written
# by pandas as format 114 (Stata 10-12) little-endian without the index:
# monthly (%tm), quarterly (%tq) and yearly (%ty) dates, value labels
# given as a dict for a numeric column, and a float32 index.

months = pd.date_range("2023-01-01", periods=8, freq="MS")
cpi = pd.DataFrame({
    "region": np.array([1, 1, 2, 2, 3, 3, 1, 2], dtype=np.int8),
    "month": months,
    "quarter": months,
    "year": months,
    "cpi": np.array([101.3, 101.9, 99.8, 100.4, 103.75, 104.2, 102.6, 100.9], dtype=np.float32),
    "basket": ["food", "food", "fuel", "fuel", "rent", "rent", "food", "fuel"],
    "weight": [0.31, 0.31, 0.12, 0.12, 0.27, 0.27, 0.31, 0.12],
})
buf = io.BytesIO()
cpi.to_stata(buf, version=114, write_index=False, time_stamp=STAMP, byteorder="little",
             convert_dates={"month": "tm", "quarter": "tq", "year": "ty"},
             value_labels={"region": {1: "Coast", 2: "Highlands", 3: "Amazon"}},
             data_label="CPI by region (2020=100)")
put("cpi_regions.dta", buf.getvalue())

# ---------------------------------------------------------------- 4
# trade_119.dta: customs records saved as format 119 (Stata 15+ for
# very wide data), little-endian, with strLs shared between rows (the
# same (v, o) key in two observations), a binary strL, an empty strL,
# weekly (%tw) and half-yearly (%th) dates, and int8 flags at the edge
# of the valid range (-127 and 100).

trade_vars = [
    Var("decl", "l", "%12.0g", "Declaration number"),
    Var("hs6", 6, "%6s", "HS 2017 subheading"),
    Var("partner", "L", "%9s", "Partner country"),
    Var("flow", "b", "%8.0g", "Flow", "flow"),
    Var("week", "h", "%tw", "Week of clearance"),
    Var("half", "h", "%th", "Half-year"),
    Var("kg", "d", "%10.0g", "Net mass (kg)"),
    Var("fob_usd", "d", "%12.2f", "FOB value (USD)"),
    Var("adj", "b", "%8.0g", "Adjustment code"),
    Var("scan", "L", "%9s", "Scanned form"),
]
trade_rows = [
    (5500101, "090111", "Germany", 2, 3328, 128, 18000.0, 61250.4, 0, b"%PDF-1.4\x00\xff"),
    (5500102, "090111", ("ref", 3, 1), 2, 3328, 128, 9000.0, 30400.0, 100, None),
    (5500103, "270900", "Ecuador", 1, 3330, 128, 120000.5, 64800.0, -127, ""),
    (5500104, "847130", "China", 1, 3331, 128, 350.25, 98000.0, miss(), None),
    (5500105, "090111", ("ref", 3, 1), 2, 3352, 129, 4500.0, 15600.75, 1, b"\x89PNG"),
    (5500106, "080390", "Panama", 2, miss(), miss(), miss(), 22000.0, 0, None),
]
put("trade_119.dta", new_dta(
    119, "<", "Customs declarations, sample", "01 Oct 2024 09:30", trade_vars, trade_rows,
    tables=[("flow", [(1, "Import"), (2, "Export")], [0, 1])]))

# ---------------------------------------------------------------- 5
# The older formats, as Stata 4 to 12 and the tools of their day wrote
# them. Each holds the same small labour-force extract.

lf_rows = [
    (1, 34, 1, 42.5, 1520.0, "Smith", 2),
    (2, 51, 2, 38.0, 1890.25, "García", 1),
    (3, 19, 1, miss(3), 640.0, "O'Neil", 3),
    (4, miss(1), 2, 40.0, miss(24), "Müller", 2),
    (5, 66, 3, 0.0, 0.0, "Ito", miss(26)),
]


def lf_vars(version, wide):
    nm = (lambda s: s) if wide else (lambda s: s[:8])
    return [
        Var(nm("person"), "h", "%8.0g", "Person number"),
        Var(nm("age"), "b", "%8.0g", "Age"),
        Var(nm("status"), "b", "%8.0g", "Employment status", "status"),
        Var(nm("hours"), "f", "%9.0g", "Usual weekly hours"),
        Var(nm("earnings"), "d", "%10.0g", "Monthly earnings"),
        Var(nm("surname"), 10, "%10s", "Surname"),
        Var(nm("sector"), "l", "%12.0g", "Sector", "sector"),
    ]


STATUS = [(1, "Employed"), (2, "Unemployed"), (3, "Inactive")]
SECTOR = [(1, "Public"), (2, "Private"), (3, "Own account")]
for version, bo in [(104, "<"), (105, ">"), (108, "<"), (110, ">"), (111, "<"),
                    (113, ">"), (114, "<"), (115, ">")]:
    wide = version > 108
    vars = lf_vars(version, wide)
    if version <= 105:
        for v in vars:
            v.label = v.label[:31]
    stamp = "" if version < 105 else " 1 Oct 1999 09:30"
    label = f"Labour force, format {version}"
    exp = [(1, b"\x00" * 10 + b"note0" + b"\x00")] if version > 104 else []
    put(f"lfs_{version}.dta", old_dta(
        version, bo, label, stamp, vars, lf_rows,
        tables=[("status", STATUS, [2, 0, 1]), ("sector", SECTOR, [0, 1, 2])],
        expansion=exp))

# ---------------------------------------------------------------- 6
# Edge cases a reader meets in the wild.

# ward_census_117.dta: format 117 with a value label whose texts repeat
# ("Other" twice), so read_stata cannot make a categorical of it, and a
# second column whose values are only partly labelled.
ward_vars = [
    Var("ward", "h", "%8.0g", "Ward"),
    Var("tenure", "b", "%8.0g", "Tenure", "tenure"),
    Var("rooms", "b", "%8.0g", "Rooms", "rooms"),
    Var("rent", "f", "%9.0g", "Monthly rent"),
]
ward_rows = [
    (1, 1, 2, 350.0), (1, 2, 3, 0.0), (2, 3, 1, 410.5), (2, 4, 5, miss(3)),
    (3, 1, 9, 275.25), (3, 2, miss(), 0.0),
]
put("ward_census_117.dta", new_dta(
    117, "<", "Ward census", "01 Oct 2024 09:30", ward_vars, ward_rows,
    tables=[("tenure", [(1, "Owned"), (2, "Rented"), (3, "Other"), (4, "Other")], [0, 1, 2, 3]),
            ("rooms", [(1, "One room"), (2, "Two rooms"), (3, "Three or more")], [2, 1, 0])],
    chars=b"<ch>" + struct.pack("<I", 12) + b"_dta\x00note1\x00\x00" + b"</ch>"))

# empty_118.dta: the variables of a file but no observations.
put("empty_118.dta", new_dta(
    118, ">", "", "01 Oct 2024 09:30",
    [Var("id", "l", "%12.0g"), Var("name", 8, "%8s"), Var("score", "d", "%10.0g"),
     Var("grade", "b", "%8.0g", "", "grade")],
    [], tables=[("grade", [(1, "A"), (2, "B")], [0, 1])]))

# A pandas file with a column of nothing but missing values.
nan_df = pd.DataFrame({"k": np.array([1, 2, 3], dtype=np.int8),
                       "v": np.array([np.nan, np.nan, np.nan]),
                       "w": np.array([np.nan, 1.5, np.nan], dtype=np.float32)})
buf = io.BytesIO()
nan_df.to_stata(buf, version=118, write_index=False, time_stamp=STAMP)
put("allnan_118.dta", buf.getvalue())

# Compressed copies, inferred from the extension as pandas does.
with open(os.path.join(DATA, "cpi_regions.dta"), "rb") as f:
    cpi_bytes = f.read()
gz = io.BytesIO()
with gzip.GzipFile(fileobj=gz, mode="wb", mtime=0, filename="") as g:
    g.write(cpi_bytes)
put("cpi_regions.dta.gz", gz.getvalue())
zb = io.BytesIO()
with zipfile.ZipFile(zb, "w") as z:
    info = zipfile.ZipInfo("cpi_regions.dta", (2024, 10, 1, 9, 30, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(info, cpi_bytes)
put("cpi_regions.zip", zb.getvalue())

# Files that are not what they claim.
put("release_116.dta", b"<stata_dta><header><release>116</release>" + b"\x00" * 64)
put("v112.dta", bytes([112]) + b"\x02\x01\x00" + b"\x00" * 64)
put("survey.csv.dta", b"hhid,region,income\n10101,1,1250.5\n")

# ---------------------------------------------------------------- jobs

J = []


def R(f, *opts):
    J.append(" ".join(["read", f] + list(opts)))


def M(f):
    J.append(f"meta {f}")


def C(f, n, *opts):
    J.append(" ".join(["chunks", f, str(n)] + list(opts)))


files = ["hh_survey_w3.dta", "clinic_visits.dta", "cpi_regions.dta", "trade_119.dta"]
files += [f"lfs_{v}.dta" for v in (104, 105, 108, 110, 111, 113, 114, 115)]
files += ["ward_census_117.dta", "empty_118.dta", "allnan_118.dta"]
for f in files:
    M(f)
for f in files:
    R(f)

R("hh_survey_w3.dta", "convert_categoricals=False")
R("hh_survey_w3.dta", "convert_missing=True")
R("hh_survey_w3.dta", "convert_missing=True", "convert_dates=False", "convert_categoricals=False")
R("hh_survey_w3.dta", "convert_missing=True", "columns=hhid,head_age,hhsize,income,weight")
R("hh_survey_w3.dta", "convert_missing=True", "preserve_dtypes=False", "columns=hhid,head_age,income")
R("hh_survey_w3.dta", "convert_dates=False", "columns=hhid,int_date,synced")
R("hh_survey_w3.dta", "preserve_dtypes=False", "columns=hhid,head_age,hhsize,income,weight")
R("hh_survey_w3.dta", "order_categoricals=False", "columns=region,educ")
R("hh_survey_w3.dta", "index_col=hhid", "columns=hhid,head_name,region")
R("hh_survey_w3.dta", "columns=income,hhid")
R("hh_survey_w3.dta", "columns=hhid,hhid")
R("hh_survey_w3.dta", "columns=hhid,district")
R("hh_survey_w3.dta", "index_col=nobody")
R("clinic_visits.dta", "convert_dates=False")
R("clinic_visits.dta", "convert_categoricals=False", "columns=index,dx")
R("clinic_visits.dta", "index_col=index", "columns=index,patient,notes")
R("clinic_visits.dta", "preserve_dtypes=False")
R("clinic_visits.dta", "convert_missing=True", "columns=index,temp_c,bmi")
R("cpi_regions.dta", "convert_dates=False")
R("cpi_regions.dta", "convert_categoricals=False", "preserve_dtypes=False")
R("cpi_regions.dta.gz")
R("cpi_regions.zip", "columns=region,cpi")
R("trade_119.dta", "convert_missing=True")
R("trade_119.dta", "convert_missing=True", "columns=decl,half")
R("trade_119.dta", "convert_missing=True", "columns=decl,partner,flow")
R("trade_119.dta", "convert_missing=True", "convert_dates=False", "convert_categoricals=False")
R("trade_119.dta", "convert_dates=False", "convert_categoricals=False")
R("lfs_104.dta", "convert_missing=True")
for v in (104, 105, 108, 111, 113, 114):
    R(f"lfs_{v}.dta", "convert_missing=True", "convert_categoricals=False")
R("lfs_115.dta", "convert_categoricals=False", "preserve_dtypes=False")
R("ward_census_117.dta", "convert_categoricals=False")
R("ward_census_117.dta", "columns=ward,rooms,rent")
R("ward_census_117.dta", "convert_missing=True", "convert_categoricals=False")
R("empty_118.dta", "columns=score,id")
R("allnan_118.dta", "convert_missing=True")
C("hh_survey_w3.dta", 4)
C("hh_survey_w3.dta", 4, "convert_categoricals=False", "columns=hhid,region,income")
C("cpi_regions.dta", 3, "columns=region,month,cpi")
C("clinic_visits.dta", 5, "columns=index,dx,notes")
C("trade_119.dta", 4, "convert_categoricals=False", "columns=decl,partner,flow")
C("lfs_108.dta", 2)
C("empty_118.dta", 2)
C("hh_survey_w3.dta", 0)
for f in ["release_116.dta", "v112.dta", "survey.csv.dta", "nowhere.dta"]:
    R(f)
M("release_116.dta")

with open(os.path.join(DATA, "jobs.txt"), "w") as f:
    f.write("\n".join(J) + "\n")
print(len(J), "jobs,", len(os.listdir(DATA)) - 1, "files")
