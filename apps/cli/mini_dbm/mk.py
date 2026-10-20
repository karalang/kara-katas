# Writes data/: jobs.tsv, the calls and programs mini_dbm runs, and the
# hand-made database files they open. The files under data/bin/ hold
# bytes that are not UTF-8; mini_dbm.kara writes those itself (see
# write_binary_data) and gen_kara.py leaves them out.
import os

FILES = {}


def put(path, data):
    FILES[path] = data


# ------------------------------------------------------------ hand-made databases

# A .dir file written by hand: double quotes, spaces, escapes.
put("db/handmade.dir", "".join([
    "'alpha', (0, 5)\n",
    "\"beta\", (512, 4)\n",
    "'gam\\x6da',(1024,3)\n",
    "'tab\\tkey', ( 1536 , 2 )\n",
    "'it\\'s', (2048, 1)\n",
    "'caf\\xc3\\xa9', (2560, 3)\n",
    "'oct\\101l', (3072, 2)\n",
    "'trailing',   (3584, 4)   \n",
]))
put("db/handmade.dat",
    "hello" + "\0" * 507 + "beta" + "\0" * 508 + "ccc" + "\0" * 509 + "TT" + "\0" * 510 +
    "Q" + "\0" * 511 + "XYZ" + "\0" * 509 + "OK" + "\0" * 510 + "last")

# A key that is not Latin-1 once the escape is read.
put("db/euro.dir", "'price', (0, 2)\n'\\u20ac', (512, 1)\n")
put("db/euro.dat", "10" + "\0" * 510 + "E")

# A line that unpacks to three values.
put("db/triple.dir", "'k', (0, 1), 'extra'\n")
put("db/triple.dat", "v")

# Index entries that a checker should complain about.
put("db/damaged.dir", "".join([
    "'ok', (0, 3)\n",
    "'past-end', (1024, 40)\n",
    "'misaligned', (100, 4)\n",
    "'overlap-a', (512, 300)\n",
    "'overlap-b', (700, 10)\n",
    "'empty', (0, 0)\n",
]))
put("db/damaged.dat", "abc" + "\0" * 97 + "MISA" + "\0" * 408 + "A" * 300 + "\0" * 212 + "tail")

# An empty dumb database: whichdb reports it from the empty .dir.
put("which/empty.dir", "")
put("which/empty.dat", "")
# A .dir that does not start with a quote.
put("which/notdumb.dir", "alpha, (0, 1)\n")
put("which/notdumb.dat", "a")
# ndbm's pair of files.
put("which/legacy.pag", "")
put("which/legacy.dir", "")
put("which/short", "ab")
put("which/text.txt", "just some text, nothing magic about it\n")

# ------------------------------------------------------------ jobs

J = []


def job(name, *lines):
    J.append("job\t" + name)
    J.extend(lines)


job("create, set, get and reopen",
    "open\tnotes\tn",
    "set\tgreeting\thello",
    "set\tb:bytes-key\tb:\\x00\\x01\\xff",
    "set\tcolor\tgreen",
    "get\tgreeting",
    "get\tb:bytes-key",
    "get\tmissing",
    "has\tcolor",
    "has\tb:color",
    "has\tnope",
    "len",
    "keys",
    "items",
    "files\tnotes",
    "close",
    "files\tnotes",
    "open\tnotes\tc",
    "keys",
    "get\tcolor",
    "close",
)

job("updates: in place, then past the block",
    "open\tcache\tn",
    "set\tpage\tr:a:100",
    "set\tother\tr:b:10",
    "files\tcache",
    "set\tpage\tr:c:512",
    "get\tpage",
    "files\tcache",
    "set\tpage\tr:d:513",
    "get\tpage",
    "files\tcache",
    "set\tpage\tshort",
    "get\tpage",
    "set\tpage\tr:e:1024",
    "get\tpage",
    "set\tother\t",
    "get\tother",
    "sync",
    "files\tcache",
    "close",
)

job("delete commits the index",
    "open\tdel\tn",
    "set\ta\t1",
    "set\tb\t2",
    "set\tc\t3",
    "files\tdel",
    "del\tb",
    "files\tdel",
    "del\tb",
    "set\tb\tagain",
    "keys",
    "files\tdel",
    "close",
    "files\tdel",
)

job("keys that are not ASCII",
    "open\tintl\tn",
    "set\tcafé\tcoffee",
    "set\t日本\tjapan",
    "set\tb:\\xe9t\\xe9\tlatin-1 bytes",
    "set\tb:new\\nline\tnl",
    "set\tb:\\x7f\\x80\\xa0\\xad\tcontrols",
    "set\tit's\tquote",
    "set\tsay \"hi\"\tdouble",
    "set\tboth ' and \"\tmixed",
    "keys",
    "get\tcafé",
    "get\tb:caf\\xc3\\xa9",
    "close",
    "files\tintl",
    "open\tintl\tr",
    "keys",
    "get\t日本",
    "close",
)

job("flags and errors",
    "open\tabsent\tr",
    "open\tabsent\tw",
    "open\tabsent\tx",
    "open\tro\tn",
    "set\tk\tv",
    "close",
    "open\tro\tr",
    "get\tk",
    "set\tk\tw",
    "del\tk",
    "set\ti:5\tv",
    "close",
    "open\tro\tw",
    "set\tk\tw",
    "set\tnum\ti:7",
    "set\ti:5\tv",
    "get\ti:5",
    "del\tnope",
    "close",
    "get\tk",
    "set\tk\tv",
    "len",
    "keys",
    "has\tk",
    "close",
    "open\tro\tc",
    "items",
    "close",
)

job("hand-made index files",
    "open\thandmade\tr",
    "keys",
    "items",
    "len",
    "close",
    "open\teuro\tr",
    "open\ttriple\tr",
    "open\tdamaged\tr",
    "get\tpast-end",
    "get\tmisaligned",
    "get\toverlap-b",
    "get\tempty",
    "close",
)

job("the n flag starts over",
    "open\tfresh\tn",
    "set\tx\t1",
    "close",
    "open\tfresh\tc",
    "set\ty\t2",
    "close",
    "files\tfresh",
    "open\tfresh\tn",
    "keys",
    "close",
    "files\tfresh",
)

for f in ["which/empty", "which/notdumb", "which/legacy", "which/short", "which/text.txt",
          "bin/gnu.db", "bin/gnu2.db", "bin/sqlite.db", "bin/bdb.db", "which/missing", "db/notes",
          "db/handmade", "db/damaged"]:
    J.append("whichdb\t" + f)

for p in ["shortener", "sessions", "httpcache", "crash", "fsck"]:
    J.append("program\t" + p)

put("jobs.tsv", "\n".join(J) + "\n")

# ------------------------------------------------------------ program inputs

put("shortener/urls.txt", """# long URLs to shorten, in the order they are submitted
https://docs.python.org/3/library/dbm.html#module-dbm.dumb
https://en.wikipedia.org/wiki/DBM_(computing)
https://example.com/blog/2026/10/20/why-we-moved-off-a-dumb-database
https://docs.python.org/3/library/dbm.html#module-dbm.dumb
https://example.com/search?q=key+value+store&page=2
https://example.org/
https://example.com/a/very/long/path/that/keeps/going/and/going/until/it/is/longer/than/most/people/would/ever/type/by/hand/index.html
""")

put("shortener/visits.txt", """# short codes clicked, after a restart
1
2
4
zz
3
1
""")

put("sessions/events.txt", """# time, then what happens: login <sid> <user>, touch <sid>, logout <sid>, sweep
100 login s-7f3a alice
105 login s-91bc bob
110 login s-02de carol
130 touch s-7f3a
160 logout s-91bc
200 login s-55aa dave
700 sweep
760 touch s-02de
900 login s-c0de erin
1300 sweep
1305 touch s-7f3a
2500 sweep
""")

put("httpcache/responses.txt", """# url, then the size of the body served each time it is fetched
/api/prices 180 190 175 600 590 1400 300
/api/news 2000 2100 2050
/static/logo.svg 4096 4096
/api/me 90 95 600
""")

for path, data in FILES.items():
    full = os.path.join("data", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="") as fp:
        fp.write(data)

# Binary files: whichdb's magic numbers.
BIN = {
    "bin/gnu.db": bytes([0xce, 0x9a, 0x57, 0x13]) + bytes(12),
    "bin/gnu2.db": bytes([0xcf, 0x9a, 0x57, 0x13]),
    "bin/sqlite.db": b"SQLite format 3\x00" + bytes(84),
    "bin/bdb.db": bytes(12) + bytes([0x61, 0x15, 0x06, 0x00]),
}
for path, data in BIN.items():
    full = os.path.join("data", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as fp:
        fp.write(data)
