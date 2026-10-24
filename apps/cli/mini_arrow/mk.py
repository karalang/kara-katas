# Writes data/ for mini_arrow: the job list, the zone files the jobs use
# (copied from the system tzdata), and the inputs of the four tools.
import json, os, shutil

os.makedirs("data/zones", exist_ok=True)
ZONES = ["America/New_York", "America/Los_Angeles", "Europe/London",
         "Europe/Berlin", "Asia/Kolkata", "Australia/Sydney", "Asia/Tokyo",
         "America/Sao_Paulo"]
for z in ZONES:
    os.makedirs(os.path.dirname("data/zones/" + z), exist_ok=True)
    shutil.copyfile("/usr/share/zoneinfo/" + z, "data/zones/" + z)

jobs = []


def job(name, a, *ops):
    jobs.append({"kind": "ops", "n": name, "a": a, "ops": [list(o) for o in ops]})


def get(*args, **kw):
    d = {"get": list(args)}
    if kw:
        d["kw"] = kw
    return d


def new(*vals, tz=None, fold=None):
    d = {"new": list(vals)}
    if tz is not None:
        d["tz"] = tz
    if fold is not None:
        d["fold"] = fold
    return d


NY, LA, LON, BER = "America/New_York", "America/Los_Angeles", "Europe/London", "Europe/Berlin"
KOL, SYD, TOK, SAO = "Asia/Kolkata", "Australia/Sydney", "Asia/Tokyo", "America/Sao_Paulo"

# ---------------------------------------------------------------- construction
job("ctor plain", new(2013, 5, 5, 12, 30, 45), ["repr"], ["info"])
job("ctor micro", new(2024, 2, 29, 23, 59, 59, 999999, tz="+05:30"), ["repr"], ["info"])
job("ctor named zone", new(2024, 7, 4, 9, 0, tz=NY), ["repr"], ["info"], ["tzrepr"])
job("ctor utc names", new(2024, 1, 1, tz="utc"), ["repr"], ["tzrepr"])
job("ctor Z", new(2024, 1, 1, tz="Z"), ["tzrepr"])
job("ctor local", new(2024, 1, 1, tz="local"), ["repr"], ["tzrepr"], ["info"])
job("ctor offset forms", new(2024, 1, 1, tz="-0800"), ["repr"], ["tzrepr"])
job("ctor offset hours only", new(2024, 1, 1, tz="+03"), ["repr"], ["tzrepr"])
job("ctor offset (UTC", new(2024, 1, 1, tz="(UTC+09:30) Adelaide"), ["repr"], ["tzrepr"])
job("ctor bad zone", new(2024, 1, 1, tz="Mars/Olympus_Mons"), ["repr"])
job("ctor bad day", new(2023, 2, 29), ["repr"])
job("ctor bad month", new(2023, 13, 1), ["repr"])
job("ctor bad hour", new(2023, 1, 1, 24), ["repr"])
job("ctor year 0", new(0, 1, 1), ["repr"])
job("ctor fold 1 ambiguous", new(2024, 11, 3, 1, 30, tz=NY, fold=1), ["repr"], ["info"])
job("ctor fold 0 ambiguous", new(2024, 11, 3, 1, 30, tz=NY, fold=0), ["repr"], ["info"])
job("ctor imaginary", new(2024, 3, 10, 2, 30, tz=NY), ["repr"], ["info"])
job("ctor london gap", new(2024, 3, 31, 1, 30, tz=LON), ["repr"], ["info"])
job("ctor london overlap fold", new(2024, 10, 27, 1, 30, tz=LON, fold=1), ["repr"], ["info"])
job("ctor lmt", new(1850, 6, 1, 12, tz=NY), ["repr"], ["info"])
job("ctor kolkata 1941", new(1942, 6, 1, 12, tz=KOL), ["repr"], ["info"])
job("ctor after 2037", new(2040, 7, 1, 12, tz=NY), ["repr"], ["info"])
job("ctor last transition", new(2037, 7, 1, 12, tz=NY), ["repr"], ["info"])
job("ctor sydney dst", new(2024, 1, 15, 8, tz=SYD), ["repr"], ["info"])
job("ctor tokyo", new(2024, 1, 15, 8, tz=TOK), ["repr"], ["info"])
job("ctor sao paulo 2018 midnight gap", new(2018, 11, 4, 0, 30, tz=SAO), ["repr"], ["info"])
job("ctor sao paulo now no dst", new(2024, 11, 4, 0, 30, tz=SAO), ["repr"], ["info"])
job("fromtimestamp utc", {"ts": 1700000000, "tz": "UTC"}, ["repr"])
job("fromtimestamp float", {"ts": 1700000000.123456, "tz": NY}, ["repr"], ["info"])
job("fromtimestamp half micro", {"ts": 1.0000005, "tz": "UTC"}, ["repr"])
job("fromtimestamp negative", {"ts": -1.25, "tz": "UTC"}, ["repr"])
job("fromtimestamp ms", {"ts": 1700000000123, "tz": "UTC"}, ["repr"])
job("fromtimestamp us", {"ts": 1700000000123456, "tz": "UTC"}, ["repr"])
job("fromtimestamp string", {"ts": "1565358758.5", "tz": TOK}, ["repr"])
job("fromtimestamp bad string", {"ts": "15653x", "tz": TOK}, ["repr"])
job("fromtimestamp local", {"ts": 0}, ["repr"], ["tzrepr"])
job("fromtimestamp into overlap", {"ts": 1730615400, "tz": NY}, ["repr"], ["info"])
job("fromtimestamp into overlap 2", {"ts": 1730619000, "tz": NY}, ["repr"], ["info"])
job("utcfromtimestamp", {"uts": 1234567890.75}, ["repr"])
job("fromordinal", {"ord": 738000}, ["repr"])
job("fromordinal 0", {"ord": 0}, ["repr"])

# ---------------------------------------------------------------- get()
job("get iso date", get("2024-03-15"), ["repr"])
job("get iso datetime", get("2024-03-15T08:30:00"), ["repr"])
job("get iso space", get("2024-03-15 08:30"), ["repr"])
job("get iso basic", get("20240315T083000"), ["repr"])
job("get iso tz", get("2024-03-15T08:30:00-05:00"), ["repr"], ["tzrepr"])
job("get iso tz basic", get("2024-03-15T08:30:00+0530"), ["repr"])
job("get iso Z", get("2024-03-15T08:30:00Z"), ["repr"], ["tzrepr"])
job("get iso z lower", get("2024-03-15T08:30:00z"), ["repr"])
job("get iso fraction", get("2024-03-15T08:30:00.123"), ["repr"])
job("get iso fraction long", get("2024-03-15T08:30:00.1234567"), ["repr"])
job("get iso fraction round even", get("2024-03-15T08:30:00.0000025"), ["repr"])
job("get iso fraction round up", get("2024-03-15T08:30:00.9999995"), ["repr"])
job("get iso comma", get("2024-03-15T08:30:00,5"), ["repr"])
job("get iso hour only", get("2024-03-15T08"), ["repr"])
job("get iso 24:00", get("2024-03-15T24:00"), ["repr"])
job("get iso 24:01", get("2024-03-15T24:01"), ["repr"])
job("get iso ordinal", get("2024-075"), ["repr"])
job("get iso ordinal 366 non-leap", get("2023-366"), ["repr"])
job("get iso ordinal 367", get("2023-367"), ["repr"])
job("get iso week", get("2024-W11"), ["repr"])
job("get iso week day", get("2024-W11-5"), ["repr"])
job("get iso week compact", get("2024W115"), ["repr"])
job("get iso week 53 bad", get("2023-W53-1"), ["repr"])
job("get iso week 53 good", get("2020-W53-7"), ["repr"])
job("get iso month", get("2024-03"), ["repr"])
job("get iso year", get("2024"), ["repr"])
job("get iso slashes", get("2024/3/5"), ["repr"])
job("get iso dots", get("2024.03.05 10:00"), ["repr"])
job("get iso two spaces", get("2024-03-05  10:00"), ["repr"])
job("get iso two spaces normalized", get("2024-03-05  10:00", normalize_whitespace=True), ["repr"])
job("get iso T and space", get("2024-03-05T10:00 Z"), ["repr"])
job("get iso bad time", get("2024-03-05T1"), ["repr"])
job("get iso bad", get("March 5th"), ["repr"])
job("get iso with tzinfo kw", get("2024-03-05T10:00", tzinfo=LON), ["repr"])
job("get iso tz replaced not converted", get("2024-03-05T10:00+02:00", tzinfo=NY), ["repr"])
job("get timestamp int", get(1700000000), ["repr"])
job("get timestamp float tz", get(1700000000.5, tzinfo=KOL), ["repr"])
job("get timestamp string is iso", get("1700000000"), ["repr"])
job("get tuple", get({"tuple": [2024, 1, 1]}), ["repr"])
job("get tuple week 53", get({"tuple": [2015, 53, 7]}), ["repr"])
job("get tuple bad week", get({"tuple": [2024, 54, 1]}), ["repr"])
job("get tuple bad day", get({"tuple": [2024, 5, 8]}), ["repr"])
job("get none", get(None), ["repr"])
job("get bool", get(True), ["repr"])
job("get datetime naive", get({"dt": [2024, 5, 6, 7, 8, 9]}), ["repr"])
job("get datetime aware", get({"dt": [2024, 5, 6, 7, 8, 9], "tz": BER}), ["repr"])
job("get datetime and tz", get({"dt": [2024, 5, 6, 7, 8, 9]}, TOK), ["repr"])
job("get datetime and int", get({"dt": [2024, 5, 6]}, 5), ["repr"])
job("get date", get({"date": [2024, 5, 6]}), ["repr"])
job("get date and tz", get({"date": [2024, 5, 6]}, {"tz": SYD}), ["repr"])
job("get str and tzobj", get("2024-05-06", {"tz": "UTC"}), ["repr"])
job("get three args", get(2024, 5, 6, tzinfo=SYD), ["repr"])
job("get with fold kw", get(2024, 11, 3, 1, 30, tzinfo=NY, fold=1), ["repr"], ["info"])
job("get bad locale", get("2024-05-06", locale="xx_YY"), ["repr"])

# ---------------------------------------------------------------- get(string, format)
P = []
P += [("YYYY-MM-DD HH:mm:ss", "2013-05-05 12:30:45"),
      ("MM/DD/YYYY", "05/06/2024"),
      ("M/D/YY", "5/6/24"),
      ("M/D/YY", "5/6/69"),
      ("M/D/YY", "5/6/68"),
      ("DD MMMM YYYY", "06 May 2024"),
      ("DD MMMM YYYY", "06 may 2024"),
      ("D MMM YYYY", "6 Sept 2024"),
      ("D MMM YYYY", "6 Sep 2024"),
      ("dddd, MMMM Do YYYY h:mm a", "Monday, May 6th 2024 3:04 pm"),
      ("dddd, MMMM Do YYYY h:mm A", "Monday, May 6th 2024 3:04 PM"),
      ("h:mm a", "12:15 am"),
      ("h:mm a", "12:15 pm"),
      ("h:mm a", "3:15 Pm"),
      ("h a", "13 am"),
      ("MMMM Do", "March 1st"),
      ("MMMM Do", "March 22nd"),
      ("MMMM Do", "March 13th"),
      ("MMMM Do", "March 21th"),
      ("YYYY-MM-DDTHH:mm:ssZZ", "2024-05-06T10:00:00-07:00"),
      ("YYYY-MM-DD HH:mm Z", "2024-05-06 10:00 +0530"),
      ("YYYY-MM-DD HH:mm ZZZ", "2024-05-06 10:00 Europe/London"),
      ("YYYY-MM-DD HH:mm ZZZ", "2024-05-06 10:00 Asia/Tokyo"),
      ("YYYY-MM-DD HH:mm ZZZ", "2024-05-06 10:00 Nowhere/Land"),
      ("X", "1700000000"),
      ("X", "1700000000.25"),
      ("x", "1700000000123456"),
      ("x", "1700000000123"),
      ("YYYY-MM-DD HH:mm:ss.S", "2024-05-06 10:00:00.5"),
      ("YYYY-MM-DD HH:mm:ss.SSS", "2024-05-06 10:00:00.123"),
      ("YYYY-MM-DD HH:mm:ss.SSSSSSS", "2024-05-06 10:00:00.1234565"),
      ("YYYY-MM-DD HH:mm:ss.S", "2024-05-06 10:00:00.9999999"),
      ("YYYY-DDDD", "2024-060"),
      ("YYYY DDD", "2024 60"),
      ("YYYY MM DDD", "2024 03 60"),
      ("DDDD", "060"),
      ("W", "2024-W01-1"),
      ("ddd YYYY-MM", "Wed 2024-05"),
      ("dddd", "Friday"),
      ("YYYY-MM-DD [at] HH:mm", "2024-05-06 at 10:30"),
      ("[Report for] MMMM YYYY", "Report for June 2024"),
      ("YYYY-MM-DD [.] HH", "2024-05-06 x 10"),
      ("YYYY#MM", "2024#05"),
      ("YYYY-MM-DD", "on 2024-05-06, the"),
      ("YYYY-MM-DD", "id2024-05-06"),
      ("YYYY-MM-DD", "(2024-05-06)."),
      ("YYYY-MM-DD", "2024-05-06x"),
      ("YYYY-MM-DD", "x 2024-05-06!"),
      ("MM-DD", "13-01"),
      ("YYYY YYYY", "2024 2024"),
      ("YYY-MM", "202-05"),
      ("dd MM", "Mo 05"),
      ("YYYY-MM-DD hh:mm", "2024-05-06 24:00"),
      ("YYYY-MM-DD HH:mm", "2024-05-06 24:30"),
      ("HH:mm", "10:30"),
      ("YYYY-MM-DD HH:mm:ss", "2024-05-06 10:30:60"),
     ]
for fmt, s in P:
    job(f"parse {fmt!r} {s!r}", get(s, fmt), ["repr"])
job("parse format list", get("06.05.2024", ["YYYY-MM-DD", "DD.MM.YYYY"]), ["repr"])
job("parse format list none", get("06|05|2024", ["YYYY-MM-DD", "DD.MM.YYYY"]), ["repr"])
job("parse empty format list", get("06|05|2024", []), ["repr"])
job("parse with tzinfo", get("2024-05-06 10:00", "YYYY-MM-DD HH:mm", tzinfo=SAO), ["repr"])
job("parse whitespace", get("2024-05-06   10:00", "YYYY-MM-DD HH:mm", normalize_whitespace=True), ["repr"])
for loc, fmt, s in [("fr", "D MMMM YYYY", "6 mai 2024"),
                    ("fr", "dddd D MMMM YYYY", "lundi 6 mai 2024"),
                    ("fr", "Do MMMM", "1er mars"),
                    ("fr", "Do MMMM", "2e mars"),
                    ("de", "D. MMMM YYYY", "6. März 2024"),
                    ("de", "dddd, D. MMM YYYY", "Montag, 6. Mär 2024"),
                    ("es", "D [de] MMMM [de] YYYY", "6 de mayo de 2024"),
                    ("es", "Do MMMM", "6º mayo"),
                    ("it", "dddd D MMMM", "lunedì 6 maggio"),
                    ("ru", "D MMMM YYYY", "6 мая 2024"),
                    ("ru", "D MMMM YYYY", "6 МАЯ 2024"),
                    ("pl", "D MMMM YYYY", "6 maj 2024"),
                    ("ja", "YYYY年MMMMD日", "2024年5月6日"),
                    ("zh", "YYYY MMMM D", "2024 五月 6"),
                    ("ko", "MMMM D", "5월 6"),
                    ("nl", "D MMMM YYYY", "6 mei 2024"),
                    ("pt", "dddd, D MMMM", "Segunda-feira, 6 Maio"),
                    ("fi", "D. MMMM YYYY", "6. toukokuu 2024"),
                    ("cs", "D. MMMM YYYY", "6. květen 2024"),
                    ("de", "Do MMMM", "6. Mai"),
                    ("fr", "h:mm a", "3:04 pm"),
                    ("de", "h:mm a", "3:04 nachm"),
                    ("ja", "MMM", " 5"),
                    ]:
    job(f"parse {loc} {fmt!r} {s!r}", get(s, fmt, locale=loc), ["repr"])

# ---------------------------------------------------------------- format
base = new(2024, 3, 9, 14, 5, 7, 123456, tz=NY)
FMTS = [None, "YYYY-MM-DD", "YY M D", "MMMM MMM MM M", "DDDD DDD DD D Do", "dddd ddd d",
        "HH H hh h mm m ss s", "S SS SSS SSSS SSSSS SSSSSS", "ZZZ ZZ Z", "a A", "X", "x", "W",
        "[Today is] dddd [at] h:mm a", "[[nested]] YYYY", "[unclosed YYYY", "YYY dd", "YYYYY MMMMM",
        "dddd, DD-MMM-YYYY HH:mm:ss ZZZ", "ddd, DD MMM YY HH:mm:ss Z", "YYYY-MM-DDTHH:mm:ssZZ",
        "Q Qo w ww", "hh:mm A", "年YYYY"]
for f in FMTS:
    job(f"format {f!r}", base, ["fmt", f])
for loc in ["en", "fr", "fr-ca", "de", "de-at", "es", "it", "pt", "pt-br", "nl", "ru", "pl",
            "cs", "fi", "ja", "zh", "ko"]:
    job(f"format locale {loc}", new(2024, 1, 1, 0, 30, tz="UTC"), ["fmt", "dddd D MMMM YYYY, Do ddd MMM, h:mm a A", loc])
job("format hour 0 and 12", new(2024, 1, 1, 0, 0), ["fmt", "hh h a"], ["shift", {"hours": 12}], ["fmt", "hh h a"],
    ["shift", {"hours": 1}], ["fmt", "hh h a"])
job("format lmt offset", new(1850, 6, 1, 12, tz=NY), ["fmt", "ZZ Z ZZZ"], ["iso", "T", "auto"])
job("format offset none name", new(2024, 6, 1, 12, tz="+0530"), ["fmt", "ZZZ|ZZ"])
job("format year 5", new(5, 6, 1), ["fmt", "YYYY YY"])
job("format bad locale", new(2024, 6, 1), ["fmt", "YYYY", "tlh"])
job("format ordinals", new(2024, 1, 1), ["ords"])

# ---------------------------------------------------------------- to(), shift(), replace()
job("to zones", new(2024, 6, 30, 23, 30, tz="UTC"), ["to", NY], ["to", KOL], ["to", SYD], ["to", "+01:00"], ["to", "utc"])
job("to local", new(2024, 6, 30, 23, 30, tz=NY), ["to", "local"], ["tzrepr"])
job("to bad", new(2024, 6, 30, 23, 30, tz=NY), ["to", "Atlantis/Main"])
job("to across fall back", new(2024, 11, 3, 5, 30, tz="UTC"), ["to", NY], ["info"])
job("to across fall back 2", new(2024, 11, 3, 6, 30, tz="UTC"), ["to", NY], ["info"])
job("to round trip fold", new(2024, 11, 3, 1, 30, tz=NY, fold=1), ["to", "UTC"], ["to", NY], ["info"])
job("shift basics", new(2024, 1, 31, 12, tz="UTC"),
    ["shift", {"months": 1}], ["shift", {"months": 1}], ["shift", {"years": -1, "days": 3}],
    ["shift", {"weeks": 2, "hours": -36}], ["shift", {"quarters": 1}], ["shift", {"microseconds": -1}],
    ["shift", {"seconds": 86400 * 3 + 5}], ["shift", {"minutes": -90}])
job("shift weekday", new(2024, 5, 8, tz="UTC"), ["shift", {"weekday": 0}], ["shift", {"weekday": 6}],
    ["shift", {"weekday": 6}], ["shift", {"weekday": 2, "days": 1}])
job("shift bad key", new(2024, 5, 8), ["shift", {"fortnights": 1}])
job("shift singular", new(2024, 5, 8), ["shift", {"day": 1}])
job("shift float months", new(2024, 5, 8), ["shift", {"months": 1.5}])
job("shift dst spring", new(2024, 3, 10, 1, 30, tz=NY), ["shift", {"hours": 1}], ["info"])
job("shift into gap", new(2024, 3, 9, 2, 30, tz=NY), ["shift", {"days": 1}], ["info"])
job("shift over fall", new(2024, 11, 2, 1, 30, tz=NY), ["shift", {"days": 1}], ["info"], ["shift", {"hours": 1}], ["info"])
job("shift leap", new(2024, 2, 29), ["shift", {"years": 1}], ["shift", {"years": 3}])
job("shift overflow", new(9999, 12, 31), ["shift", {"days": 1}])
job("shift underflow", new(1, 1, 1), ["shift", {"microseconds": -1}])
job("replace", new(2024, 5, 8, 10, 20, 30, tz=BER), ["replace", {"hour": 0, "minute": 0}],
    ["replace", {"tzinfo": TOK}], ["replace", {"year": 2023, "month": 2, "day": 28}],
    ["replace", {"tzinfo": "-03:00"}])
job("replace week", new(2024, 5, 8), ["replace", {"week": 2}])
job("replace unknown", new(2024, 5, 8), ["replace", {"hours": 2}])
job("replace bad day", new(2024, 5, 31), ["replace", {"month": 6}])
job("replace fold", new(2024, 11, 3, 1, 30, tz=NY), ["replace", {"fold": 1}], ["info"])
job("replace bad tz", new(2024, 5, 31), ["replace", {"tzinfo": "Gondor/Minas_Tirith"}])

# ---------------------------------------------------------------- span / floor / ceil
mid = new(2024, 5, 15, 14, 37, 22, 456789, tz=BER)
for fr in ["year", "quarter", "month", "week", "day", "hour", "minute", "second", "microsecond", "years", "quarters", "weeks"]:
    job(f"span {fr}", mid, ["span", fr, {}])
job("span count", mid, ["span", "day", {"count": 3}], ["span", "month", {"count": -1}])
for b in ["()", "(]", "[]", "[)", "{}"]:
    job(f"span bounds {b}", mid, ["span", "hour", {"bounds": b}])
job("span exact", mid, ["span", "day", {"exact": True}], ["span", "week", {"exact": True, "bounds": "[]"}])
for ws in [1, 3, 7, 0, 8]:
    job(f"span week start {ws}", mid, ["span", "week", {"week_start": ws}])
job("span bad frame", mid, ["span", "fortnight", {}])
job("floor ceil", mid, ["floor", "hour"], ["ceil", "hour"], ["floor", "quarter"], ["ceil", "year"])
job("span day over spring forward", new(2024, 3, 10, 12, tz=NY), ["span", "day", {}])
job("span day over fall back", new(2024, 11, 3, 12, tz=NY), ["span", "day", {}])
job("span day sao paulo 2018", new(2018, 11, 4, 12, tz=SAO), ["span", "day", {}], ["floor", "day"], ["info"])
job("span month sydney", new(2024, 4, 10, tz=SYD), ["span", "month", {}])

# ---------------------------------------------------------------- range / span_range / interval
job("range hours", new(2024, 5, 1, 22, tz="UTC"), ["range", "hour", new(2024, 5, 2, 2, tz="UTC"), {}])
job("range month end clip", new(2024, 1, 31, tz="UTC"), ["range", "month", new(2024, 7, 31, tz="UTC"), {}])
job("range month end clip 30", new(2024, 1, 30, tz="UTC"), ["range", "month", new(2024, 5, 1, tz="UTC"), {}])
job("range year leap", new(2020, 2, 29), ["range", "year", new(2025, 3, 1), {}])
job("range quarter", new(2024, 2, 15), ["range", "quarter", new(2025, 2, 15), {}])
job("range week limit", new(2024, 5, 1), ["range", "week", None, {"limit": 4}])
job("range limit and end", new(2024, 5, 1), ["range", "day", new(2024, 5, 30), {"limit": 3}])
job("range no end no limit", new(2024, 5, 1), ["range", "day", None, {}])
job("range tz", new(2024, 3, 8, 12, tz="UTC"), ["range", "day", new(2024, 3, 12, 12, tz="UTC"), {"tz": NY}])
job("range over dst", new(2024, 3, 9, 2, 30, tz=NY), ["range", "day", new(2024, 3, 12, tz=NY), {}])
job("range bad frame", new(2024, 5, 1), ["range", "decade", new(2024, 5, 30), {}])
job("range end before start", new(2024, 5, 1), ["range", "day", new(2024, 4, 30), {}])
job("range minutes", new(2024, 5, 1, 10, 0, 30), ["range", "minutes", new(2024, 5, 1, 10, 3), {}])
job("span_range days", new(2024, 5, 1, 15), ["span_range", "day", new(2024, 5, 4, 1), {}])
job("span_range month bounds", new(2024, 1, 15), ["span_range", "month", new(2024, 4, 2), {"bounds": "[]"}])
job("span_range week limit", new(2024, 1, 15), ["span_range", "week", new(2024, 4, 2), {"limit": 3}])
job("span_range exact", new(2024, 1, 15, 6), ["span_range", "day", new(2024, 1, 18, 3), {"exact": True}])
job("span_range exact month", new(2024, 1, 15), ["span_range", "month", new(2024, 3, 20), {"exact": True, "bounds": "[]"}])
job("span_range hour tz", new(2024, 11, 3, 4, tz="UTC"), ["span_range", "hour", new(2024, 11, 3, 8, tz="UTC"), {"tz": NY}])
job("interval", new(2024, 5, 1, 9), ["interval", "hour", new(2024, 5, 1, 17), {"interval": 3}])
job("interval days", new(2024, 5, 1), ["interval", "day", new(2024, 5, 10), {"interval": 4, "bounds": "[]"}])
job("interval zero", new(2024, 5, 1), ["interval", "day", new(2024, 5, 10), {"interval": 0}])

# ---------------------------------------------------------------- humanize / dehumanize
now = new(2024, 5, 15, 12, 0, 0, tz="UTC")
for secs in [0, 9, 10, 44, 59, 60, 119, 120, 3599, 3600, 7199, 7200, 86399, 86400, 172799, 172800,
             604799, 604800, 1209599, 1209600, 2635199, 2635200, 5270400, 31535999, 31536000,
             63071999, 63072000, 315360000]:
    for sign in ([1, -1] if secs else [1]):
        job(f"humanize {sign * secs}s", now, ["shift", {"seconds": sign * secs}], ["humanize", now, {}])
job("humanize months by calendar", new(2024, 1, 31, tz="UTC"), ["humanize", new(2024, 4, 1, tz="UTC"), {}])
job("humanize same tz ignores dst", new(2024, 3, 9, 12, tz=NY),
    ["humanize", new(2024, 3, 10, 12, tz=NY), {"granularity": "hour"}],
    ["humanize", new(2024, 3, 10, 16, tz="UTC"), {"granularity": "hour"}])
job("humanize naive other", now, ["humanize", {"naive": [2024, 5, 15, 9]}, {}])
job("humanize aware other", now, ["humanize", {"aware": [2024, 5, 15, 9], "tz": NY}, {}])
job("humanize bad other", now, ["humanize", "yesterday", {}])
OTHER = new(2022, 2, 3, 4, 5, 6, tz="UTC")
for g in ["second", "minute", "hour", "day", "week", "month", "quarter", "year", "decade",
          ["hour"], ["year", "day"], ["month", "week", "second"], ["day", "hour", "minute"],
          ["year", "decade"], []]:
    job(f"humanize granularity {g}", now, ["humanize", OTHER, {"granularity": g}], ["humanize", OTHER, {"granularity": g, "only_distance": True}])
job("humanize granularity second near", now, ["humanize", new(2024, 5, 15, 12, 0, 1, tz="UTC"), {"granularity": "second"}])
job("humanize granularity minute fraction", now, ["humanize", new(2024, 5, 15, 12, 0, 30, tz="UTC"), {"granularity": "minute"}])
for loc in ["en", "fr", "de", "es", "it", "pt", "pt-br", "nl", "ru", "pl", "cs", "fi", "ja", "zh", "ko"]:
    ops = []
    for d in [{"seconds": -5}, {"seconds": 30}, {"minutes": -1}, {"minutes": 21}, {"hours": -1},
              {"hours": 3}, {"days": 1}, {"days": -2}, {"days": -5}, {"weeks": 1}, {"weeks": -3},
              {"months": 1}, {"months": -11}, {"years": 1}, {"years": -2}, {"years": 22}]:
        ops.append(["humanize_shift", d, {"locale": loc}])
    ops.append(["humanize_shift", {"days": -3}, {"locale": loc, "only_distance": True}])
    ops.append(["humanize_shift", {"seconds": 1}, {"locale": loc, "only_distance": True}])
    ops.append(["humanize_shift", {"days": 400}, {"locale": loc, "granularity": ["year", "day", "hour"]}])
    ops.append(["humanize_shift", {"days": -92}, {"locale": loc, "granularity": "quarter"}])
    ops.append(["humanize_shift", {"days": -15}, {"locale": loc, "granularity": ["week", "day"], "only_distance": True}])
    ops.append(["humanize_shift", {"hours": -26}, {"locale": loc, "granularity": "day"}])
    job(f"humanize locale {loc}", now, *ops)
job("humanize bad locale", now, ["humanize", OTHER, {"locale": "klingon"}])
for loc, s in [("en", "in 5 seconds"), ("en", "2 hours ago"), ("en", "a minute ago"), ("en", "in a year"),
               ("en", "just now"), ("en", "in 2 days and 3 hours"), ("en", "3 weeks ago"),
               ("en", "in 2 quarters"), ("en", "an hour ago"), ("en", "5 hours"), ("en", "soon"),
               ("en_US", "in 4 months"), ("fr", "il y a 3 jours"), ("fr", "dans une heure"),
               ("de", "vor 2 Tagen"), ("de", "in 5 Minuten"), ("es", "hace 2 años"), ("it", "tra 3 ore"),
               ("ru", "через 2 дня"), ("ru", "5 минут назад"), ("pl", "za 3 godziny"), ("ja", "3日前"),
               ("zh", "2小时后"), ("nl", "over 2 weken"), ("pt", "há 4 meses"), ("fi", "3 tuntia sitten"),
               ("cs", "Za 2 dny"), ("ko", "3시간 후"), ("pt-br", "faz 2 dias")]:
    job(f"dehumanize {loc} {s!r}", now, ["dehumanize", s, loc])

# ---------------------------------------------------------------- comparisons and arithmetic
job("cmp same instant other zones", new(2024, 6, 1, 12, tz="UTC"), ["cmp", new(2024, 6, 1, 14, tz=BER)])
job("cmp later", new(2024, 6, 1, 12, tz="UTC"), ["cmp", new(2024, 6, 1, 13, tz=BER)])
job("cmp ambiguous across zones", new(2024, 11, 3, 1, 30, tz=NY), ["cmp", new(2024, 11, 3, 5, 30, tz="UTC")])
job("cmp ambiguous fold 1 across zones", new(2024, 11, 3, 1, 30, tz=NY, fold=1), ["cmp", new(2024, 11, 3, 6, 30, tz="UTC")])
job("cmp same zone folds", new(2024, 11, 3, 1, 30, tz=NY, fold=1), ["cmp", new(2024, 11, 3, 1, 30, tz=NY)])
job("cmp same zone across dst", new(2024, 3, 9, 12, tz=NY), ["cmp", new(2024, 3, 10, 12, tz=NY)])
job("cmp diff zone across dst", new(2024, 3, 9, 12, tz=NY), ["cmp", new(2024, 3, 10, 16, tz="UTC")])
job("arith", new(2024, 2, 28, 23, tz=SYD), ["add", {"days": 1, "hours": 2}], ["add", {"weeks": -1}], ["add", {"microseconds": 1500001}])
job("between", new(2024, 6, 1, 12),
    ["between", new(2024, 6, 1, 12), new(2024, 6, 2), "()"],
    ["between", new(2024, 6, 1, 12), new(2024, 6, 2), "[)"],
    ["between", new(2024, 5, 1), new(2024, 6, 1, 12), "(]"],
    ["between", new(2024, 5, 1), new(2024, 6, 1, 11), "[]"],
    ["between", new(2024, 5, 1), new(2024, 7, 1), "[x"])
job("iso forms", new(2024, 6, 1, 12, 3, 4, 5006, tz=KOL),
    ["iso", "T", "auto"], ["iso", " ", "hours"], ["iso", "T", "minutes"], ["iso", "T", "seconds"],
    ["iso", "T", "milliseconds"], ["iso", "_", "microseconds"], ["iso", "T", "nanoseconds"])
job("iso no micro", new(2024, 6, 1, 12, 3, 4, tz="-02:30"), ["iso", "T", "auto"], ["iso", "T", "milliseconds"])
job("min and max", {"min": 1}, ["repr"], ["fmt", "YYYY-MM-DD dddd W"])
job("max", {"max": 1}, ["repr"], ["shift", {"microseconds": 1}])

# ---------------------------------------------------------------- the four tools
jobs.append({"kind": "logs", "n": "log normalizer"})
jobs.append({"kind": "meetings", "n": "meeting planner"})
jobs.append({"kind": "billing", "n": "billing periods"})
jobs.append({"kind": "feed", "n": "activity feed"})

with open("data/formats.txt", "w") as f:
    f.write("""# service | zone the stamps are written in (- when they carry an offset) | formats tried in order
nginx | - | DD/MMM/YYYY:HH:mm:ss Z
app | - | YYYY-MM-DD HH:mm:ss,SSS | YYYY-MM-DDTHH:mm:ss.SSSZZ
mail | - | ddd, DD MMM YYYY HH:mm:ss Z | ddd, D MMM YYYY HH:mm:ss Z
syslog | America/New_York | MMM D HH:mm:ss | MMM  D HH:mm:ss
audit | - | X
api | - | YYYY-MM-DDTHH:mm:ssZZ
cron | Europe/Berlin | YYYY-MM-DD HH:mm | dddd [at] h:mm a
""")

with open("data/app.log", "w") as f:
    f.write("""nginx 192.0.2.10 - - [09/Mar/2024:23:58:12 -0500] "GET /api/orders HTTP/1.1" 200 512
nginx 192.0.2.11 - - [10/Mar/2024:00:02:40 -0500] "POST /api/cart HTTP/1.1" 201 87
app 2024-03-10 05:03:01,412 INFO worker started
app 2024-03-10T05:07:55.020+00:00 WARN slow query 2312ms
mail Sun, 10 Mar 2024 06:12:09 +0100 delivered msg-8812 to ops@example.org
mail Sun,  10 Mar 2024 06:12:09 +0100 deferred msg-8813
syslog Mar  9 23:59:01 web01 kernel: eth0 link up
syslog Mar 10 01:15:44 web01 sshd[2211]: Accepted publickey for deploy
syslog Mar 10 02:30:00 web01 CRON[2240]: (root) CMD (backup.sh)
syslog Mar 10 03:01:12 web01 sshd[2299]: Disconnected from 198.51.100.7
audit 1710047820 user=ana action=login
audit 1710051420.5 user=ben action=export rows=1200
api ts=2024-03-10T01:20:00-04:00 status=ok latency=18ms
api ts=2024-03-10T07:45:31+05:30 status=error code=502
cron 2024-03-10 09:00 nightly-report finished
cron Sunday at 9:15 am weekly-cleanup started
nginx 192.0.2.12 - - [10/Mar/2024:07:59:59 +0000] "GET /health HTTP/1.1" 200 2
app 2024-03-10 7:59:60,000 ERROR clock skew
unknown 2024-03-10 08:00:00 something
""")

with open("data/meetings.txt", "w") as f:
    f.write("""# title | organizer zone | local start | minutes | repeat | attendee zones
Design review | America/New_York | 2024-03-07 11:00 | 60 | weekly | Europe/London, Europe/Berlin, Asia/Kolkata
Release sync | Europe/Berlin | 2024-03-28 17:30 | 45 | weekly | America/Los_Angeles, America/New_York, Asia/Tokyo
On-call handover | Australia/Sydney | 2024-04-04 09:00 | 30 | weekly | Europe/London, America/Sao_Paulo
Quarterly planning | America/Los_Angeles | 2024-11-03 01:30 | 120 | once | America/New_York, Europe/London
Night maintenance | America/New_York | 2024-03-10 02:30 | 90 | once | UTC, Asia/Kolkata
Customer demo | Asia/Kolkata | 2024-05-15 18:00 | 60 | once | America/Los_Angeles, Australia/Sydney, Asia/Tokyo
Budget call | Europe/London | 2024-02-30 10:00 | 30 | once | Europe/Berlin
Offsite | Moon/Base | 2024-06-01 09:00 | 480 | once | UTC
""")

with open("data/subscriptions.txt", "w") as f:
    f.write("""# id | plan, cents a month | start | cancelled | billing zone
S-1001 | 4900 | 2024-01-31T10:00:00 | - | America/New_York
S-1002 | 1200 | 2024-02-14T00:00:00 | 2024-05-20T12:00:00 | Europe/London
S-1003 | 29900 | 2024-03-01T00:00:00 | 2024-03-31T00:00:00 | Europe/Berlin
S-1004 | 999 | 2023-12-15T08:30:00 | 2024-02-29T23:59:59 | Asia/Kolkata
S-1005 | 7500 | 2024-10-30T18:00:00 | 2025-01-02T00:00:00 | Australia/Sydney
S-1006 | 1500 | 2024-06-31T00:00:00 | - | UTC
""")

with open("data/feed.txt", "w") as f:
    f.write("""# user | locale | zone | when (ISO) | what
amara | en | Europe/London | 2024-05-15T11:59:58+00:00 | pushed 3 commits to main
amara | en | Europe/London | 2024-05-15T10:10:00+00:00 | opened issue #4412
bruno | pt-br | America/Sao_Paulo | 2024-05-14T20:30:00-03:00 | comentou no PR #88
chen | zh | Asia/Tokyo | 2024-05-13T09:00:00+09:00 | 合并了分支 release
dmitri | ru | Europe/Berlin | 2024-05-01T08:00:00+02:00 | закрыл задачу
elise | fr | Europe/Berlin | 2024-05-15T14:30:00+02:00 | a publié la version 2.4
elise | fr | Europe/Berlin | 2023-12-24T18:00:00+01:00 | a rejoint le projet
fumiko | ja | Asia/Tokyo | 2024-05-15T21:00:00+09:00 | レビューを依頼しました
greta | de | Europe/Berlin | 2024-05-16T09:00:00+02:00 | plant das Release-Meeting
hana | ko | Asia/Tokyo | 2024-05-14T12:00:00+09:00 | 이슈를 닫았습니다
ivan | pl | Europe/Berlin | 2024-04-15T12:00:00+02:00 | dodał komentarz
jana | cs | Europe/Berlin | 2024-05-12T12:00:00+02:00 | sloučila větev
kai | fi | Europe/Berlin | 2024-05-15T11:00:00+02:00 | päivitti dokumentaation
lotte | nl | Europe/Berlin | 2024-05-08T12:00:00+02:00 | heeft een release gemaakt
marco | it | Europe/Berlin | 2026-05-15T12:00:00+02:00 | ha pianificato la migrazione
nuria | es | Europe/Berlin | 2024-05-15T12:00:00 | revisó el cambio
omar | tlh | Asia/Kolkata | 2024-05-15T10:00:00+05:30 | commented
""")

with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(jobs), "jobs")
