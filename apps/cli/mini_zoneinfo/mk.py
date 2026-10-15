# Writes data/: TZif files copied from the system's tzdata, a few made by
# hand (one per rule and error the loader has), the TZ strings to parse,
# the conversions to make, and the meetings to plan.
import os, shutil, struct
shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/zones")

SYSTEM = ["America/New_York", "Europe/London", "Australia/Lord_Howe", "Asia/Kolkata",
          "America/Sao_Paulo", "Pacific/Apia", "Pacific/Chatham", "UTC",
          "Africa/Casablanca", "America/St_Johns", "Antarctica/Troll"]
for key in SYSTEM:
    os.makedirs(os.path.dirname("data/zones/" + key) or "data/zones", exist_ok=True)
    with open("/usr/share/zoneinfo/" + key, "rb") as f:
        data = f.read()
    with open("data/zones/" + key, "wb") as f:
        f.write(data)

def header(version, isut=0, isstd=0, leap=0, time=0, typ=0, char=0):
    return b"TZif" + version + b"\0" * 15 + struct.pack(">6l", isut, isstd, leap, time, typ, char)

def tzif(version, trans, types, abbrs, footer, v1=False, nl=True, isstd=0):
    # trans: [(utc, idx)], types: [(utoff, isdst, abbr_index)]
    chars = abbrs.encode()
    size = "l" if v1 else "q"
    body = b"".join(struct.pack(">" + size, t) for t, _ in trans)
    body += bytes(i for _, i in trans)
    body += b"".join(struct.pack(">lbb", *t) for t in types)
    body += chars + b"\1" * isstd
    h = header(version, isstd=isstd, time=len(trans), typ=len(types), char=len(chars))
    if v1:
        return h + body
    out = header(version) + h + body + b"\n" + footer.encode()
    return out + (b"\n" if nl else b"")

made = {
    # version 1: four-byte times and no footer
    "Test/Version1": tzif(b"\0", [(-1633280400, 1), (-1615140000, 0), (-1601830800, 1), (-1583690400, 0)],
                          [(-18000, 0, 0), (-14400, 1, 4)], "EST\0EDT\0", "", v1=True),
    # no transitions, everything from the footer
    "Test/FooterOnly": tzif(b"2", [], [(-10800, 0, 0)], "<-03>\0", "<-03>3<-02>,M3.2.0/-1,M11.1.0/24"),
    # Irish time: winter is the daylight time, so DST is negative
    "Test/Eire": tzif(b"2", [(1679792400, 1), (1698541200, 0)], [(0, 1, 0), (3600, 0, 4)],
                      "GMT\0IST\0", "IST-1GMT0,M10.5.0,M3.5.0/1"),
    # Julian and zero-based day rules, an hour past midnight and a negative hour
    "Test/Julian": tzif(b"3", [], [(-3600, 0, 0)], "AAA\0", "AAA1BBB0,J60/25,300/-2"),
    # a zone with standard and standard-wall indicators to skip
    "Test/Indicators": tzif(b"2", [(0, 1), (100000000, 2)], [(3600, 0, 0), (7200, 1, 4), (3600, 0, 0)],
                            "CET\0CEST\0", "CET-1CEST,M3.5.0,M10.5.0/3", isstd=3),
    # a DST type whose DST offset must be guessed: one hour
    "Test/Guess": tzif(b"2", [(0, 1), (1000, 1)], [(0, 0, 0), (5400, 1, 4)], "STD\0DST\0", "STD0"),
    # a fixed zone made of a single type
    "Test/Fixed": tzif(b"2", [], [(19800, 0, 0)], "IST\0", ""),
    # the errors
    "Bad/Magic": b"TZjf" + b"\0" * 40,
    "Bad/Index": tzif(b"2", [(0, 5)], [(0, 0, 0)], "UTC\0", "UTC0"),
    "Bad/NoNewline": tzif(b"2", [], [(0, 0, 0)], "UTC\0", "UTC0", nl=False),
    "Bad/Empty": tzif(b"2", [], [], "", ""),
    "Bad/NoRules": tzif(b"2", [], [(0, 0, 0)], "AAA\0", "AAA3BBB"),
    "Bad/RulesNoDST": tzif(b"2", [], [(0, 0, 0)], "AAA\0", "AAA3,M3.2.0,M11.1.0"),
    "Bad/Week": tzif(b"2", [], [(0, 0, 0)], "AAA\0", "AAA3BBB,M3.6.0,M11.1.0"),
}
for key, data in made.items():
    os.makedirs("data/zones/" + os.path.dirname(key), exist_ok=True)
    with open("data/zones/" + key, "wb") as f:
        f.write(data)

with open("data/tzstrings.txt", "w") as f:
    f.write("\n".join([
        "EST5EDT,M3.2.0,M11.1.0", "GMT0BST,M3.5.0/1,M10.5.0", "<+1030>-10:30<+11>-11,M10.1.0,M4.1.0",
        "NST3:30NDT,M3.2.0,M11.1.0", "<-03>3<-02>,M3.2.0/-1,M11.1.0/24", "IST-1GMT0,M10.5.0,M3.5.0/1",
        "AAA1BBB0,J60/25,300/-2", "AAA-12:45:30BBB-13:45:30,M9.5.0/2:45,M4.1.0/3:45", "UTC0", "IST-5:30",
        "CET-1CEST,M3.5.0,M10.5.0/3", "WART4WARST,J1/0,J365/25", "XXX-3YYY,0/0,J365/25",
        "EST", "EST5EDT", "EST5,M3.2.0,M11.1.0", "EST25EDT,M3.2.0,M11.1.0", "EST5EDT4:60,M3.2.0,M11.1.0",
        "EST5EDT,M13.2.0,M11.1.0", "EST5EDT,M3.2.7,M11.1.0", "EST5EDT,M3.2.0", "EST5EDT,J0,J365",
        "EST5EDT,366,J365", "EST5EDT,M3.2.0/168,M11.1.0", "EST5EDT,M3.2.0/1:2,M11.1.0", "E5EDT,M3.2.0,M11.1.0",
        "EST1234EDT", "<A1>1<B2>,M1.1.0,M12.5.6/167", "", "EST+5EDT-4:30:15,M3.2.0/-1:30,M11.1.0/26:30",
    ]) + "\n")

with open("data/convert.txt", "w") as f:
    f.write("""# utc ZONE TIME: the local time at a UTC instant
# local ZONE TIME FOLD: the offset and UTC instant of a wall time
utc America/New_York 2024-03-10T06:59:59
utc America/New_York 2024-03-10T07:00:00
utc America/New_York 2024-11-03T05:30:00
utc America/New_York 2024-11-03T06:30:00
utc America/New_York 1883-11-18T16:59:59
utc America/New_York 2100-07-04T16:00:00
utc America/New_York 1970-01-01T00:00:00
utc Europe/London 1971-06-01T00:00:00
utc Europe/London 2037-10-25T00:30:00
utc Europe/London 2037-10-25T01:30:00
utc Australia/Lord_Howe 2024-04-06T14:45:00
utc Australia/Lord_Howe 2024-04-06T15:15:00
utc Asia/Kolkata 1941-10-01T00:00:00
utc Asia/Kolkata 2300-01-01T00:00:00
utc Pacific/Apia 2011-12-30T09:59:59
utc Pacific/Apia 2011-12-30T10:00:00
utc Pacific/Chatham 2024-09-28T14:00:00
utc Africa/Casablanca 2024-03-10T01:59:59
utc Africa/Casablanca 2024-03-10T02:00:00
utc Antarctica/Troll 2024-03-31T01:00:00
utc America/Sao_Paulo 2018-11-04T03:00:00
utc UTC 2024-02-29T12:00:00
utc Test/Version1 1918-03-31T07:00:00
utc Test/Version1 1950-01-01T00:00:00
utc Test/FooterOnly 2024-03-10T02:59:59
utc Test/FooterOnly 2024-03-10T03:00:00
utc Test/FooterOnly 2024-11-03T02:00:00
utc Test/Eire 2030-10-27T00:30:00
utc Test/Eire 2030-10-27T01:30:00
utc Test/Eire 2030-03-31T00:59:59
utc Test/Julian 2024-03-01T23:59:59
utc Test/Julian 2024-03-02T00:00:00
utc Test/Guess 1970-01-01T00:20:00
utc Test/Fixed 2024-01-01T00:00:00
local America/New_York 2024-03-10T02:30:00 0
local America/New_York 2024-03-10T02:30:00 1
local America/New_York 2024-11-03T01:30:00 0
local America/New_York 2024-11-03T01:30:00 1
local America/New_York 2024-07-01T12:00:00 1
local America/New_York 1800-01-01T00:00:00 0
local Europe/London 2099-03-29T01:30:00 0
local Europe/London 2099-03-29T01:30:00 1
local Europe/London 2099-10-25T01:30:00 1
local Australia/Lord_Howe 2024-04-07T01:45:00 0
local Australia/Lord_Howe 2024-04-07T01:45:00 1
local Australia/Lord_Howe 2024-10-06T02:15:00 0
local Pacific/Apia 2011-12-30T12:00:00 0
local Pacific/Chatham 2050-09-25T02:50:00 0
local America/St_Johns 2024-11-03T01:15:00 1
local Test/Eire 2030-10-27T01:30:00 0
local Test/Eire 2030-10-27T01:30:00 1
local Test/Eire 2030-03-31T01:30:00 0
local Test/Eire 2030-03-31T01:30:00 1
local Test/FooterOnly 2024-11-03T23:30:00 0
local Test/FooterOnly 2024-11-03T23:30:00 1
local Test/Julian 2025-10-28T22:30:00 1
""")

with open("data/meetings.txt", "w") as f:
    f.write("""# name | organizer zone | first local start | weeks | attendee zones
Release sync | America/New_York | 2024-02-26T09:00:00 | 8 | Europe/London Asia/Kolkata Australia/Lord_Howe Pacific/Chatham
Ops handover | Europe/London | 2024-10-13T01:30:00 | 4 | America/St_Johns Africa/Casablanca UTC
Night batch | America/New_York | 2024-03-03T02:30:00 | 3 | UTC Antarctica/Troll
Pacific call | Pacific/Apia | 2011-12-16T10:00:00 | 4 | America/New_York Pacific/Chatham
""")

with open("data/years.txt", "w") as f:
    f.write("America/New_York 1883 1918 2024 2101\nEurope/London 1968 1971 2024\nAustralia/Lord_Howe 2024\n"
            "Pacific/Apia 2011 2021\nPacific/Chatham 2024\nAfrica/Casablanca 2024 2087\nAntarctica/Troll 2024\n"
            "America/Sao_Paulo 2018 2019 2020\nTest/Eire 2030\nTest/FooterOnly 2024\nTest/Julian 2024 2025\n"
            "Test/Version1 1918 1919\nTest/Guess 1970\n")
