# Writes data/jobs.jsonl, the lists to sort, and data/unicode.txt, the
# character data the port needs, taken from this Python's unicodedata
# (Unicode 15.1 in Python 3.13): for each character that has any,
# its NFD and NFKD forms, casefold and swapcase, whether it is printable,
# white space and in natsort's table of numeric characters, its combining class, and its decimal, digit and numeric
# values.
import json
import os
import random
import shutil
import struct
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from natsort.unicode_numeric_hex import numeric_hex  # noqa: E402

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data")

NUMERIC = set(numeric_hex)

# ------------------------------------------------------------ the jobs

jobs = []


def job(name, ops):
    jobs.append({"name": name, "ops": ops})


def srt(items, *alg, fn="natsorted", reverse=False, key=None):
    o = {"op": "sort", "fn": fn, "items": items, "alg": list(alg)}
    if reverse:
        o["reverse"] = True
    if key is not None:
        o["key"] = key
    return o


def key(item, *alg):
    return {"op": "key", "item": item, "alg": list(alg)}


def cli(*args):
    return {"op": "cli", "args": list(args)}


PHOTOS = ["IMG_10.jpg", "IMG_2.jpg", "IMG_1.jpg", "IMG_100.jpg", "img_3.JPG", "IMG_20.png", "IMG_2 (1).jpg", "IMG_02.jpg"]
VERSIONS = ["1.10.0", "1.2.9", "1.2.10", "1.2.10rc1", "1.2.10-beta.2", "v1.9", "2.0", "1.2", "1.2.0", "10.0.1", "0.9.99"]
LOGS = ["app.log.10.gz", "app.log", "app.log.2.gz", "app.log.1", "app.log.9.gz", "app.log.11.gz", "app.log.3.gz"]
TEMPS = ["-2.5 C", "+3 C", "-10 C", "0 C", "-0.5 C", "12.75 C", "-3.25e1 C", "1e2 C", "+1.5E-1 C"]
WORDS = ["éclair", "eclair", "Eclair", "Éclair", "zebra", "Zebra", "apple", "Apple", "à la carte", "a la carte", "naïve", "naive", "őz", "oz", "Straße", "STRASSE", "strasse"]
CHAPTERS = ["Chapter 10: The End", "Chapter 2: Rising", "chapter 1: Begin", "Chapter 1: Begin", "Chapter 11", "Chapter 1b", "Chapter 1a", "Appendix A", "Appendix B 2"]
UNI = ["item٣", "item٢٠", "item 5", "item²", "item³", "item ½", "item ⅓", "item Ⅶ", "item１０", "item 4", "item ①"]
PATHS = ["Folder (1)/file.txt", "Folder/file.txt", "Folder (10)/file.txt", "Folder (2)/file.txt", "folder/File2.txt", "Folder/file10.txt", "Folder/file2.txt",
         "data/run.1.tar.gz", "data/run.10.tar.gz", "data/run.2.tar.gz", "data/run.tar.gz", "/var/log/a.log", "//srv/x", "./notes.md", "a..b", ".bashrc", ".env.local"]
ADDRS = ["10 Main St", "2 Main St", "100 Main St", "2B Main St", "2A Main St", "2 Main Street", "Apt 3, 2 Main St", "Apt 12, 2 Main St"]
SIZES = ["10 MB", "9.5 MB", "100 KB", "1.5 GB", "1.25 GB", "0.75 GB", "750 MB", ".5 TB", "5. TB"]

job("everyday lists", [
    srt(PHOTOS),
    srt(PHOTOS, "IGNORECASE"),
    srt(PHOTOS, reverse=True),
    srt(VERSIONS),
    srt(VERSIONS, "FLOAT"),
    srt(LOGS),
    srt(LOGS, "PATH"),
    srt(CHAPTERS),
    srt(CHAPTERS, "IGNORECASE"),
    srt(CHAPTERS, "LOWERCASEFIRST"),
    srt(CHAPTERS, "GROUPLETTERS"),
    srt(ADDRS),
    srt(ADDRS, "NUMAFTER"),
    srt(SIZES),
    srt(SIZES, "FLOAT"),
    srt(SIZES, "FLOAT", "NOEXP"),
])

job("signs and exponents", [
    srt(TEMPS),
    srt(TEMPS, "SIGNED"),
    srt(TEMPS, "FLOAT"),
    srt(TEMPS, "REAL"),
    srt(TEMPS, "REAL", "NOEXP"),
    srt(TEMPS, fn="realsorted"),
    srt(TEMPS, fn="realsorted", reverse=True),
    srt(["a-5", "a-10", "a+3", "a5", "a-0", "a+0", "a-inf", "b-nan", "b+inf", "binf", "b inf", "b nan", "inf", "-inf", "nan", "+infinity x", " infinity"], "REAL"),
    srt(["x1e5", "x1e-5", "x1E400", "x1e-400", "x.5", "x5.", "x0.5e1", "x5e", "x5e+", "xe5"], "FLOAT"),
    srt(["x1e5", "x1e-5", "x1E400", "x1e-400", "x.5", "x5.", "x0.5e1", "x5e", "x5e+", "xe5"], "FLOAT", "NOEXP"),
    srt(["v0.1", "v0.10", "v0.01", "v0.100", "v0.1000000000000000055511151231257827", "v0.1000000000000000055511151231257828",
         "v0.30000000000000004", "v0.3", "v9007199254740993", "v9007199254740992", "v123456789012345678901234567890e-10", "v2.2250738585072011e-308", "v4.9e-324", "v2.4e-324", "v2.5e-324"], "FLOAT"),
    srt(["n12345678901234567890123", "n12345678901234567890124", "n0012345678901234567890123", "n9", "n-99999999999999999999", "n-100000000000000000000", "n0", "n-0"], "SIGNED"),
])

job("accents and case", [
    srt(WORDS),
    srt(WORDS, "IGNORECASE"),
    srt(WORDS, "LOWERCASEFIRST"),
    srt(WORDS, "GROUPLETTERS"),
    srt(WORDS, "IGNORECASE", "LOWERCASEFIRST"),
    srt(WORDS, "COMPATIBILITYNORMALIZE", "IGNORECASE"),
    srt(["алфа 2", "Алфа 10", "бета 1", "alpha 3", "αλφα 4", "Αλφα 1", "ạ 5", "ạ 6", "ệ 1", "ệ 2", "ệ 3"]),
    srt(["ệ 1", "ệ 2", "ệ 3", "ệ 0"], "IGNORECASE"),
    srt(["file 10", "file 9", "file 10", "file　 8", "file\t7"]),
    srt(["ﬁle 2", "file 10", "ﬁle 1"], "COMPATIBILITYNORMALIZE"),
    srt(["ﬁle 2", "file 10", "ﬁle 1"]),
])

job("unicode numbers", [
    srt(UNI),
    srt(UNI, "FLOAT"),
    srt(UNI, "REAL"),
    srt(UNI, "COMPATIBILITYNORMALIZE"),
    srt(UNI, "IGNORECASE"),
    srt(["x١٢.٥", "x12.4", "x१२", "x১২.৫০", "x¼", "x¾", "x⅕"], "FLOAT"),
    srt(["x١٢.٥", "x12.4", "x१२", "x১২.৫০"]),
    key("item٣٢ ²", ),
    key("item ½", "FLOAT"),
    key("item ½"),
    key("ⅦⅧ", "IGNORECASE"),
])

job("paths", [
    srt(PATHS),
    srt(PATHS, "PATH"),
    srt(PATHS, "PATH", "IGNORECASE"),
    srt(PATHS, "PATH", "FLOAT"),
    srt(["a/b.tar.gz", "a/b.tgz", "a/b.1.tar.gz", "a/b.v1.2.tar.gz", "a/b.toolong.gz", "a/b.x.y.z", "a/b.x.y", "a/b.", "a/.b", "a/b.tar.gz.tar.gz", "a/b..gz", "/", "", ".", "a/./b", "a//b/"], "PATH"),
    key("Folder (1)/file.10.tar.gz", "PATH"),
    key("/var/log/syslog.2.gz", "PATH"),
    key("a/b.tar.gz.tar.gz", "PATH"),
    key("", "PATH"),
    key(5, "PATH"),
    key(None, "PATH"),
])

job("numbers and none", [
    srt([10, 2.5, -1, "3", "x", None, "nan-skip", 7, 2], fn="natsorted"),
    srt([3, 1.5, None, -2, 1e300, -1e300, 0, -0.0, 2], fn="natsorted"),
    srt([3, 1.5, None, -2, 0, 2], "NANLAST"),
    srt([3, 1.5, None, -2, 0, 2], reverse=True),
    srt([3, 1.5, None, -2, 0, 2], "NANLAST", reverse=True),
    srt(["a5", 5, "5", 5.0, "5.0", "a", "", None], "FLOAT"),
    srt(["a5", 5, "5", 5.0, "a", "", None]),
    srt([12345678901234567890, 12345678901234567889, "12345678901234567891", 1.2345678901234567e19, "x"]),
    srt(["1", 1, 1.0, "01", "1.0"]),
    srt(["1", 1, 1.0, "01", "1.0"], "FLOAT"),
    srt(["inf", "-inf", "x", "nan"], "REAL", "NANLAST"),
    srt(["inf", "-inf", "x", "nan"], "REAL"),
    srt(["nan", None, "x", "-inf"], "REAL"),
    srt(["nan", None, "x", "-inf"], "REAL", "NANLAST"),
    key(None),
    key(None, "NANLAST"),
    key(3.5),
    key("a10b2.5c", "REAL"),
    key("a10b2.5c"),
    key("-12-3.5e2", "REAL"),
    key("x", "NUMAFTER"),
    key("10x", "NUMAFTER"),
])

job("keys, nesting and presort", [
    srt([{"name": "report 10.pdf", "size": 300}, {"name": "report 2.pdf", "size": 1200}, {"name": "Report 1.pdf", "size": 40}, {"name": "report 2.PDF", "size": 7}], key="name"),
    srt([{"name": "report 10.pdf", "size": 300}, {"name": "report 2.pdf", "size": 1200}, {"name": "Report 1.pdf", "size": 40}, {"name": "report 2.PDF", "size": 7}], "IGNORECASE", key="name"),
    srt([{"host": "web10", "ip": "10.0.0.10"}, {"host": "web9", "ip": "10.0.0.9"}, {"host": "db2", "ip": "10.0.1.2"}, {"host": "web10", "ip": "10.0.0.100"}], key="ip"),
    srt([["v", "1.10"], ["v", "1.9"], ["u", "2"], ["v", "1.9a"]]),
    srt([["v", "1.10"], ["v", "1.9"], ["u", "2"], ["v", "1.9a"]], "FLOAT"),
    srt(["a2", "a10", "a1", "A2", "a01", "a001"], "PRESORT"),
    srt(["a2", "a10", "a1", "A2", "a01", "a001"]),
    srt(["a2", "a10", "a1", "A2", "a01", "a001"], "PRESORT", "IGNORECASE"),
    srt(["a2", "a10", "a1", "A2", "a01", "a001"], "PRESORT", reverse=True),
    srt(PHOTOS, fn="index_natsorted"),
    srt(PHOTOS, fn="order_by_index"),
    srt(TEMPS, fn="index_realsorted", reverse=True),
    srt(VERSIONS, "UNGROUPLETTERS"),
    srt(VERSIONS, "BAD"),
])

job("command line", [
    cli("photo10.jpg", "photo2.jpg", "photo1.jpg", "photo11.jpg"),
    cli("-r", "photo10.jpg", "photo2.jpg", "photo1.jpg"),
    cli("-f", "2", "10", "photo10.jpg", "photo2.jpg", "photo1.jpg", "photo11.jpg"),
    cli("-F", "2", "10", "photo10.jpg", "photo2.jpg", "photo1.jpg", "photo11.jpg"),
    cli("-e", "2", "-e", "11", "photo10.jpg", "photo2.jpg", "photo1.jpg", "photo11.jpg"),
    cli("-t", "real", "-f", "-5", "5", "t-10 C", "t-2.5 C", "t+3 C", "t7 C"),
    cli("-t", "float", "-f", "-5", "5", "t-10 C", "t-2.5 C", "t+3 C", "t7 C"),
    cli("-t", "f", "-s", "t-10 C", "t-2.5 C", "t+3 C", "t7 C"),
    cli("-t", "r", "--noexp", "x1e3", "x5", "x1e2"),
    cli("-t", "r", "x1e3", "x5", "x1e2"),
    cli("-p", "Folder (1)/a", "Folder/a", "Folder (10)/a", "Folder (2)/b"),
    cli("Folder (1)/a", "Folder/a", "Folder (10)/a", "Folder (2)/b"),
    cli("-f", "5", "2", "a1", "a3"),
    cli("-F", "5", "5", "a1", "a3"),
    cli("-f", "1", "3", "-f", "8", "9", "a1", "a3", "a5", "a8", "a10"),
    cli("-f", "1", "3", "a²", "a3"),
    cli("-e", "3", "a²", "a4"),
    cli("-e", "3", "a٣", "a4", "a3.0"),
    cli("-t", "f", "-e", "3", "a٣", "a4", "a3.0"),
    cli("  spaced 10  ", "　spaced 9", "spaced 1\n"),
])

# Random lists: file names built from a few parts.
rnd = random.Random(20261019)
STEMS = ["file", "File", "IMG_", "log", "v", "x-", "été", "Ete", "data.", "a b"]
SUFFIX = ["", ".txt", ".tar.gz", ".JPG", " (1)", "-rc1", "e5", ".5"]
ALGS = [[], ["IGNORECASE"], ["FLOAT"], ["REAL"], ["PATH"], ["LOWERCASEFIRST"], ["GROUPLETTERS"],
        ["FLOAT", "NOEXP"], ["SIGNED"], ["NUMAFTER"], ["PATH", "IGNORECASE"], ["REAL", "NANLAST"]]


def rnd_name():
    s = rnd.choice(STEMS)
    for _ in range(rnd.randint(1, 3)):
        k = rnd.random()
        if k < 0.5:
            s += rnd.choice(["0", "1", "2", "9", "10", "11", "99", "100", "007", "1000", "-3", "+4", "1.5", "0.25"])
        elif k < 0.7:
            s += rnd.choice(["/", "-", ".", "_", " "])
        else:
            s += rnd.choice(STEMS)
    return s + rnd.choice(SUFFIX)


# Random numbers, for float() rounding and exact int/float comparison.
def rnd_decimal():
    k = rnd.random()
    digits = "".join(rnd.choice("0123456789") for _ in range(rnd.randint(1, 40)))
    if k < 0.3:
        exp = rnd.choice([rnd.randint(-30, 30), rnd.randint(-345, -300), rnd.randint(290, 312)])
        return digits + "e" + str(exp)
    if k < 0.6:
        p = rnd.randint(0, len(digits))
        return digits[:p] + "." + digits[p:]
    return digits


for n in range(3):
    job(f"random floats {n + 1}", [key("x" + rnd_decimal(), "FLOAT") for _ in range(25)])

for n in range(3):
    items = []
    for _ in range(10):
        base = rnd.choice([2 ** 53, 2 ** 60, 10 ** 17, 10 ** 22, 3 ** 40])
        v = base + rnd.randint(-5, 5)
        items.append(v if rnd.random() < 0.5 else -v)
        f = float(v) * rnd.choice([1, -1])
        items.append(f)
        items.append(f + rnd.choice([0.0, 0.5, -0.5]) if abs(f) < 2 ** 52 else f)
    rnd.shuffle(items)
    job(f"random ints and floats {n + 1}", [srt(items), srt(items, reverse=True)])

for n in range(20):
    ops = []
    for _ in range(4):
        items = [rnd_name() for _ in range(rnd.randint(4, 12))]
        ops.append(srt(items, *rnd.choice(ALGS), reverse=rnd.random() < 0.25))
    job(f"random {n + 1}", ops)

# ------------------------------------------------------------ the table

RANGES = [(0x0000, 0x024F), (0x0300, 0x036F), (0x0370, 0x03FF), (0x0400, 0x04FF),
          (0x1E00, 0x1EFF), (0x2000, 0x206F), (0x3000, 0x3000)]
covered = set()
for a, b in RANGES:
    covered.update(range(a, b + 1))
covered.update(c for c in numeric_hex if c < 0x110000)
covered.add(0x10FFFF)  # the separator NUMAFTER puts before numbers
for j in jobs:
    covered.update(ord(ch) for ch in json.dumps(j, ensure_ascii=False))


def maps(c):
    ch = chr(c)
    return [unicodedata.normalize("NFD", ch), unicodedata.normalize("NFKD", ch),
            ch.casefold(), ch.swapcase()]


# everything a mapping can produce is covered too
while True:
    more = set()
    for c in covered:
        for m in maps(c):
            more.update(ord(x) for x in m)
    more -= covered
    if not more:
        break
    covered |= more


def cps(s):
    return " ".join("%x" % ord(x) for x in s)


rows = []
for c in sorted(covered):
    ch = chr(c)
    nfd, nfkd, fold, swap = maps(c)
    fields = [cps(m) if m != ch else "" for m in (nfd, nfkd, fold, swap)]
    flags = ("p" if not ch.isprintable() else "") + ("w" if ch.isspace() else "") + ("n" if c in NUMERIC else "")
    ccc = unicodedata.combining(ch)
    dec = unicodedata.decimal(ch, None)
    dig = unicodedata.digit(ch, None)
    num = unicodedata.numeric(ch, None)
    vals = ["" if dec is None else str(dec), "" if dig is None else str(dig),
            "" if num is None else "%x" % struct.unpack(">Q", struct.pack(">d", num))[0]]
    if any(fields) or flags or ccc or any(vals):
        rows.append(";".join(["%x" % c] + fields + [flags, str(ccc) if ccc else ""] + vals))
with open("data/unicode.txt", "w") as f:
    f.write("# cp;nfd;nfkd;casefold;swapcase;flags;ccc;decimal;digit;numeric\n")
    for r in rows:
        f.write(r + "\n")

for j in jobs:
    s = json.dumps(j, ensure_ascii=False)
    for ch in s:
        assert ord(ch) in covered, hex(ord(ch))
with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
print(len(jobs), "jobs,", sum(len(j["ops"]) for j in jobs), "operations,", len(rows), "characters")
