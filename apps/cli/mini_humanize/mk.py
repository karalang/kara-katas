# Writes data/: the humanize catalogs the jobs load (copied from the
# installed humanize 4.16.0, plus a hand-made big-endian "de" catalog)
# and the job list.
import json, os, shutil, struct

import humanize

SRC = os.path.join(os.path.dirname(humanize.__file__), "locale")
LOCALES = ["ar", "de_DE", "fr_FR", "hu_HU", "it_IT", "ja_JP", "lv", "pl_PL", "pt_BR", "pt_PT", "ru_RU", "sk_SK",
           "sl_SI", "uk_UA", "zh_CN"]
for loc in LOCALES:
    d = "data/locale/%s/LC_MESSAGES" % loc
    os.makedirs(d, exist_ok=True)
    shutil.copyfile(os.path.join(SRC, loc, "LC_MESSAGES", "humanize.mo"), d + "/humanize.mo")


# A .mo file laid out as msgfmt lays it out, in either byte order.
def mo(entries, big):
    e = ">" if big else "<"
    keys = sorted(entries)
    ids = b""
    strs = b""
    offsets = []
    for k in keys:
        offsets.append((len(ids), len(k), len(strs), len(entries[k])))
        ids += k + b"\0"
        strs += entries[k] + b"\0"
    n = len(keys)
    keystart = 7 * 4 + 16 * n
    valuestart = keystart + len(ids)
    koffsets = []
    voffsets = []
    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, o1 + keystart]
        voffsets += [l2, o2 + valuestart]
    out = struct.pack(e + "Iiiiiii", 0x950412de, 0, n, 7 * 4, 7 * 4 + n * 8, 0, 0)
    out += struct.pack(e + "%di" % (2 * n), *koffsets)
    out += struct.pack(e + "%di" % (2 * n), *voffsets)
    return out + ids + strs


header = (b"Project-Id-Version: humanize-de\nMIME-Version: 1.0\n"
          b"Content-Type: text/plain; charset=UTF-8\nPlural-Forms: nplurals=2; plural=n != 1;\n")
de = {
    b"": header,
    b"%d millisecond\0%d milliseconds": "%d Millisekunde\0%d Millisekunden".encode(),
    b"%d microsecond\0%d microseconds": "%d Mikrosekunde\0%d Mikrosekunden".encode(),
    b"%d Byte": b"%d Byte",
    b"%d Bytes": b"%d Bytes",
    b"kB": b"KB",
    b"a moment": "einen Moment".encode(),
    b"googol": "Googol (de)".encode(),
}
os.makedirs("data/locale/de/LC_MESSAGES", exist_ok=True)
open("data/locale/de/LC_MESSAGES/humanize.mo", "wb").write(mo(de, True))
os.makedirs("data/locale/xx_XX/LC_MESSAGES", exist_ok=True)
open("data/locale/xx_XX/LC_MESSAGES/humanize.mo", "wb").write(b"not a catalog\n")

# The locale names the jobs activate.
NAMES = ["de_DE", "de", "de_CH", "de_de", "german", "fr_FR", "fr", "pt", "pt_BR", "ja", "ar", "ru_RU.UTF-8", "pl_PL",
         "sl", "zh", "lv", "hu_HU", "it_IT", "uk_UA", "sk_SK", "xx_XX", "es_ES", "C", "de_AT", "fr_CA@euro"]

jobs = []


def job(**kw):
    jobs.append(kw)


def call(fn, *args, **kw):
    job(kind="call", fn=fn, args=list(args), kw=kw)


def td(days=0, seconds=0, microseconds=0):
    return {"td": [days, seconds, microseconds]}


def dt_(*a):
    return {"dt": list(a) + [0] * (7 - len(a))}


def date(y, m, d):
    return {"date": [y, m, d]}


def big(n):
    return {"big": str(n)}


def fl(s):
    return {"float": s}


WHEN = dt_(2026, 3, 1, 12, 0, 0)

NUMBERS = [0, 1, 2, 3, 4, 11, 12, 13, 21, 22, 23, 101, 102, 111, 112, 1002, -1, -11, -21, 3.7, -2.5, "7", " 42 ", "1_000",
           "3.0", "something", None, True, fl("nan"), fl("inf"), fl("-inf"), "-inf", "NaN"]
SIZES = [0, 1, -1, 2, 300, 999, 1000, 1023, 1024, 3000, 999999, 1000000, 1048575, 1048576, 3000000, 10 ** 9 - 1,
         123456789012, big(10 ** 28), big(3 * 10 ** 34), -4096, 2.5, "4096", "1e6", 1e300]
INTWORDS = [0, 999, 1000, 12400, 999999, 1000000, 1200000, 1250000, 1_999_950, 999_950_000, 1_200_000_000,
            -3_400_000, big(8100000000000000000000000000000000), big(10 ** 33 * 999), big(10 ** 36), "1000000", "12.5",
            "x", None, 2.9e9, fl("nan")]
DELTAS = [0, 0.4, 0.5, 1, 1.5, 30, 59, 60, 89, 90, 119, 120, 3599, 3600, 5400, 7199, 7200, 82800, 86399, 86400, 172800,
          30 * 86400, 31 * 86400, 45 * 86400, 46 * 86400, 364 * 86400, 365 * 86400, 366 * 86400, 395 * 86400,
          396 * 86400, 2 * 365 * 86400, 1234 * 365 * 86400, -90, "12", "1.5", "abc", None, fl("nan"), 1e-4, 0.00125,
          td(1, 2, 3), td(-1), td(0, 0, 999), td(0, 0, 1000), td(0, 0, 1500), td(500, 0, 0), td(729)]
CALLS = []

for loc in [None, "de_DE", "ru_RU", "ar", "fr_FR", "pl_PL", "ja_JP", "lv"]:
    job(kind="activate", locale=loc)
    for n in NUMBERS:
        call("ordinal", n)
    for n in [1, 2, 3, 11, 21]:
        call("ordinal", n, gender="female")
    for n in [0, 5, 9, 10, -1, "7", 7.9, "foo"]:
        call("apnumber", n)
    for v in [100, 1000, 1_000_000, 1_234_567.25, -98765, 0.5, 1e20, 123456.789, "1000", "1,234.5", "1.234,5",
              "14308.40", "1e5", "abc", None, fl("nan"), big(10 ** 30), big(12345678901234567890)]:
        call("intcomma", v)
    for v, n in [(1234.5454545, 2), (14308.40, 1), ("14308.40", 1), (1000, 2), (-0.004, 2), (2.5, 0), (3.5, 0),
                 (1e15, 3), (5, -1)]:
        call("intcomma", v, n)
    for v in INTWORDS:
        call("intword", v)
    call("intword", "1234000", "%0.3f")
    call("intword", 1_999_999, "%d")
    call("intword", 999_999_999, "%.2f")
    for v in SIZES:
        call("naturalsize", v)
        call("naturalsize", v, True)
        call("naturalsize", v, False, True)
    call("naturalsize", 3000, False, True, "%.3f")
    call("naturalsize", 1999, format="%.0f")
    call("naturalsize", "abc")
    for v in DELTAS:
        call("naturaldelta", v)
    for v in [45 * 86400, 400 * 86400]:
        call("naturaldelta", v, months=False)
    for v in [0.0002, 0.0042, 0.5, td(0, 0, 5), 2]:
        call("naturaldelta", v, minimum_unit="milliseconds")
        call("naturaldelta", v, minimum_unit="microseconds")
    call("naturaldelta", 5, minimum_unit="minutes")
    call("naturaldelta", 5, minimum_unit="fortnights")
    call("naturaldelta", fl("inf"))
    for v in [0, 1, 45, 3600, 86400 * 3, -3600, 2.5, 3.5, td(0, 30), td(-1, 86370), dt_(2026, 3, 1, 11, 59, 30),
              dt_(2026, 3, 1, 12, 0, 30), dt_(2025, 12, 25), dt_(2027, 6, 1), "x", None]:
        call("naturaltime", v, when=WHEN)
    call("naturaltime", 3600, future=True)
    call("naturaltime", 0.2, future=True)
    call("naturaltime", td(0, 0, 4000), minimum_unit="milliseconds")
    for v in [0, 1, 1.5, 61, 3725.5, 86400 * 1.25, td(2, 3600, 4), td(0, 0, 1234), 400 * 86400, 731 * 86400 + 5,
              31 * 86400, 30 * 86400 + 86399, 59.999, None]:
        call("precisedelta", v)
    call("precisedelta", td(0, 3725, 5000), minimum_unit="milliseconds")
    call("precisedelta", td(0, 3725, 5000), minimum_unit="microseconds")
    call("precisedelta", 3725.5, minimum_unit="minutes")
    call("precisedelta", 3725.5, minimum_unit="hours", format="%0.1f")
    call("precisedelta", td(800), minimum_unit="months")
    call("precisedelta", td(800), minimum_unit="years")
    call("precisedelta", td(800), minimum_unit="years", format="%d")
    call("precisedelta", td(2, 3725), suppress=["hours"])
    call("precisedelta", td(2, 3725), suppress=["days", "hours"])
    call("precisedelta", td(2, 3725), minimum_unit="hours", suppress=["hours"])
    call("precisedelta", td(40, 3725), suppress=["months"], format="%0.3f")
    call("precisedelta", td(2), minimum_unit="years", suppress=["years"])
    call("precisedelta", 5, suppress=["weeks"])
    call("precisedelta", td(1000 * 365))
    for v in [0.3, 1.3, 1 / 3, 1, 0, 2.0001, -1.5, -0.25, 3.14159265, 1e-3, "0.75", "ten", None, fl("inf")]:
        call("fractional", v)
    for v, p in [(0.3, 2), (500, 2), (-1000, 2), (1000, 1), (1000, 3), ("99", 2), (1.5e-12, 2), (6.02214076e23, 4),
                 (0, 2), ("foo", 2), (None, 2), (fl("-inf"), 2), (1, -1), (9.995, 2)]:
        call("scientific", v, p)
    for v, kw in [(123.456, {}), (0.0001, {"floor": 0.01}), (0.99, {"format": "{:.0%}", "ceil": 0.99}),
                  (0.999, {"format": "{:.0%}", "ceil": 0.99}), (1, {"format": {"fn": "intword"}, "floor": 1e6,
                                                                     "floor_token": "under "}),
                  (None, {}), (5, {"format": "{:.1f} ms"}), (7, {"format": 5}), (fl("nan"), {}),
                  (2_500_000, {"format": {"fn": "naturalsize"}, "ceil": 2_000_000})]:
        call("clamp", v, **kw)
    for v, u, p in [(1500, "V", 3), (2e8, "W", 3), (220e-6, "F", 3), (1e-14, "", 4), (1e40, "", 3), (999.9, "Hz", 3),
                    (999999, "B", 3), (0, "A", 3), (-12345, "m", 2), (0.001234, "°", 3), (1e33, "", 3), (5e-31, "s", 3),
                    (123, "", 1), (fl("inf"), "", 3)]:
        call("metric", v, u, p)
    for items in [[], ["one"], ["one", "two"], ["one", "two", "three"], [1, 2.5, None, "x"]]:
        call("natural_list", items)
    for v in [date(1999, 12, 31), date(2050, 7, 4), dt_(1987, 2, 3, 4, 5, 6), "not a date", None, date(2004, 2, 29)]:
        call("naturalday", v)
        call("naturaldate", v)
    call("naturalday", date(1999, 1, 9), "%A, %d %B %Y (day %j of %y)")
    call("naturalday", date(2051, 8, 15), "%a %m/%d %%")

for name in NAMES:
    job(kind="activate", locale=name)
    call("naturaldelta", 0.0005, minimum_unit="milliseconds")
    call("intcomma", 1234567.891, 2)
    call("intword", 3_000_000)
    call("naturalsize", 1)
job(kind="activate", locale="en_GB")
call("intword", 3_000_000)
# The catalogs stay loaded once read: removing a file afterwards only
# affects a locale that has not been activated yet.
job(kind="remove", path="data/locale/it_IT/LC_MESSAGES/humanize.mo")
job(kind="activate", locale="it_IT")
call("naturaldelta", 7200)
job(kind="remove", path="data/locale/hu_HU/LC_MESSAGES/humanize.mo")
job(kind="activate", locale="hu")
call("naturaldelta", 7200)
job(kind="activate", locale="sk")
call("naturaldelta", 7200)
job(kind="deactivate")
call("naturaldelta", 7200)

with open("data/jobs.jsonl", "w") as out:
    for j in jobs:
        out.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(jobs), "jobs")
