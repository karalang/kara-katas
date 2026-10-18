#!/usr/bin/env python3
"""Writes data/: tables as JSON in data/tables/, text files for the
command-line tool in data/text/, and data/jobs.jsonl, one job per line.
See README.md for the jobs."""
import json
import os
import shutil

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/tables")
os.makedirs("data/text")

FORMATS = ['asciidoc', 'colon_grid', 'double_grid', 'double_outline',
           'fancy_grid', 'fancy_outline', 'github', 'grid', 'heavy_grid',
           'heavy_outline', 'html', 'jira', 'latex', 'latex_booktabs',
           'latex_longtable', 'latex_raw', 'mediawiki', 'mixed_grid',
           'mixed_outline', 'moinmoin', 'orgtbl', 'outline', 'pipe', 'plain',
           'presto', 'pretty', 'psql', 'rounded_grid', 'rounded_outline',
           'rst', 'simple', 'simple_grid', 'simple_outline', 'textile', 'tsv',
           'unsafehtml', 'youtrack']

jobs = []


def table(name, value):
    with open("data/tables/" + name + ".json", "w") as f:
        f.write(json.dumps(value, ensure_ascii=True, indent=1) + "\n")


def text(name, body):
    with open("data/text/" + name, "w") as f:
        f.write(body.lstrip("\n"))


def job(**kw):
    jobs.append(json.dumps(kw, ensure_ascii=True))


SEP = "\u0001"

# ------------------------------------------------------------ tables

table("planets", [
    ["Planet", "R (km)", "mass (x 10^29 kg)"],
    ["Sun", 696000, 1989100000],
    ["Earth", 6371, 5973.6],
    ["Moon", 1737, 73.5],
    ["Mars", 3390, 641.85],
])

table("servers", [
    {"host": "web-01", "region": "eu-west-1", "cpu": 0.734, "mem_gb": 15.6,
     "uptime_days": 412, "healthy": True},
    {"host": "web-02", "region": "eu-west-1", "cpu": 0.08, "mem_gb": 15.6,
     "uptime_days": 3, "healthy": True, "note": "rebooted after kernel patch"},
    {"host": "db-primary", "region": "us-east-2", "cpu": 0.9125,
     "mem_gb": 251.9, "uptime_days": 1088, "healthy": False,
     "note": "replication lag 41s"},
    {"host": "cache-7", "region": "ap-south-1", "cpu": None, "mem_gb": 3.75,
     "healthy": None},
    {"region": "us-east-2", "cpu": 0.5, "uptime_days": 0, "host": "batch-3",
     "owner": "data-eng"},
])

table("invoice", [
    ["SKU", "Item", "Qty", "Unit", "Total"],
    ["KB-104", "Mechanical keyboard", 2, "1,299.00", "2,598.00"],
    ["MS-220", "Wireless mouse", 10, "24.5", "245"],
    ["CB-USB-C", "USB-C cable, 2 m", 25, "7.99", "199.75"],
    ["DK-3", "Docking station", 1, "18,450.10", "18,450.10"],
    ["", "Shipping", None, None, "35"],
])

table("quarters", {
    "region": ["North", "South", "East", "West", "Online"],
    "Q1": [12034.5, 9800, 15020.25, 7710.0, 30111.75],
    "Q2": [13100.0, 10250.5, 14800, 8020.4],
    "Q3": [12950.75, 11003.0, 16210.0],
    "growth": ["+7.6%", "+12.3%", "-1.5%", "+4.0%", "n/a"],
})

MIXED = [
    ["ints as text", "12", "-7", " 42 ", "1_000", "+5", "007"],
    ["floats as text", "3.5", "1e5", "-0.25", ".5", "5.", "1_000.5"],
    ["thousands", "1,234", "12,345,678", "1,234.5", "1,23", "1000", ",5"],
    ["special", "inf", "-inf", "nan", "NaN", "1.5", "2"],
    ["overflow", "1e999", "+inf", "12", "-Infinity", "3", "4"],
    ["booleans", "True", "False", True, False, "True", None],
    ["bool and int", True, 3, "False", 0, -1, ""],
    ["odd", "0x10", "1__0", "_1", "1e", "--1", "1.2.3"],
    ["empty", "", None, " ", "", None, ""],
    ["numbers", 1, 2.5, "3", -4, "5.25", 1e100],
]
# One column per kind of value, so each column's type is inferred.
table("mixed", [list(r) for r in zip(*MIXED)])

table("numbers", [
    ["id", "name", "count", "ratio", "amount"],
    [1, "alpha", 1500, 0.5, 1234567.891],
    [2, "beta", -42, 0.333333333333, -0.001],
    [3, "gamma", 1234567890123, 1.0, 100.0],
    [4, "delta", 0, 12.75, 1e21],
    [5, "epsilon", 7, 0.0001234, 2.675],
    [6, "zeta", 2 ** 62, 1e-7, -0.0],
])

table("status", [
    ["service", "state", "p99 ms", "link"],
    ["api", "\u001b[32mup\u001b[0m", "\u001b[33m412\u001b[0m",
     "\u001b]8;;https://status.example.com/api\u001b\\details\u001b]8;;\u001b\\"],
    ["worker", "\u001b[1;31mdown\u001b[0m", "\u001b[31m9001\u001b[0m", "-"],
    ["search", "\u001b[33mdegraded\u001b[0m", "88", "\u001b[4mrunbook\u001b[0m"],
    ["billing", "up", "1234567", ""],
])

table("releases", [
    ["version", "date", "notes"],
    ["2.4.0", "2024-03-01", "Adds streaming uploads\nDrops Python 3.8"],
    ["2.3.2", "2024-01-15", "Fixes a crash on empty input"],
    ["2.3.1", "2023-12-02", "Security fix\n(CVE-2023-0001)\nUpgrade advised"],
    ["2.3.0", "2023-11-20\nyanked", ""],
])

table("articles", [
    {"title": "Zero-downtime Postgres migrations",
     "summary": "How we moved a 4 TB table to a new schema without locking writes, using triggers, a shadow table and a backfill that throttles itself on replication lag.",
     "words": 2140, "rating": 4.75},
    {"title": "Why our p99 doubled on Tuesdays",
     "summary": "A cron job, a cold cache and a load balancer that thought it knew better. A post-mortem in five acts, with graphs.",
     "words": 1310, "rating": 4.2},
    {"title": "Supercalifragilisticexpialidocious-identifiers considered harmful",
     "summary": "Long names are not documentation.\nShort ones are not either.",
     "words": 640, "rating": 3.9},
    {"title": "", "summary": "", "words": None, "rating": None},
])

table("markup", [
    ["", "50% off & free shipping", "<b>bold</b>"],
    ["costs", "$5 #1 item_name", "it's \"quoted\""],
    ["   ", "{braces} ~tilde^ back\\slash", "a < b > c"],
    [None, "plain", "x"],
])

table("incidents", [
    ["date", "service", "minutes"],
    ["2024-05-01", "api", 12],
    ["2024-05-03", "db", 47],
    [SEP],
    ["2024-06-11", "api", 5],
    ["2024-06-19", "cdn", 130],
    [SEP],
    ["2024-07-02", "db", 9],
])

table("flags", [
    ["feature", "enabled", "rollout"],
    ["dark-mode", "False", "0%"],
    ["new-checkout", "True", "25%"],
    ["legacy-api", False, "100%"],
])

table("empty", [])

table("onecol", [["only"], ["one"], ["column"]])

table("ragged", [
    ["a", 1],
    ["b", 2, "extra"],
    ["c"],
    ["d", 4.5, None, "more", 9],
])

table("cities", [
    ["city", "country", "population"],
    ["Zürich", "Schweiz", 421878],
    ["São Paulo", "Brasil", 11451245],
    ["Москва", "Россия", 13010112],
    ["Αθήνα", "Ελλάδα", 643452],
    ["東京", "日本", 13960000],
])

table("bigints", [
    ["what", "value"],
    ["max i64", 9223372036854775807],
    ["min i64", -9223372036854775808],
    ["2^53+1", 9007199254740993],
    ["bytes", 1099511627776],
    ["zero", 0],
])

table("metrics", [
    ["metric", "value"],
    ["rps", 1523.333333],
    ["error rate", 0.00012],
    ["p50", 12.5],
    ["p999", 1048.0],
    ["bytes out", 98765432101.0],
    ["tiny", 5e-324],
    ["huge", 1.7976931348623157e308],
    ["neg", -273.15],
])

# ------------------------------------------------------------ text files

text("df.txt", """
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme0n1p2  468G  201G  244G  46% /
tmpfs            16G  2.1M   16G   1% /dev/shm
/dev/nvme0n1p1  511M  6.1M  505M   2% /boot/efi
/dev/sdb1       3.6T  2.9T  580G  84% /srv/backup
""")

text("passwd", """
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
postgres:x:113:120:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
deploy:x:1001:1001::/home/deploy:/bin/sh
""")

text("prices.csv", """
symbol,open,close,volume
ACME,101.25,99.80,1203400
GLOBX,5.5,5.75,98000123
INITECH,0.0451,0.0449,12
UMBR,1200,1250.5,4500

""")

text("ps.txt", """
  PID USER      %CPU %MEM COMMAND
    1 root       0.0  0.1 /sbin/init
  812 postgres   2.5  4.3 postgres
 1534 www-data  12.0  1.8 nginx
23001 deploy     0.3  0.0 sleep
""")

text("latency.tsv", "endpoint\tp50\tp95\tp99\n/login\t12\t48.5\t120\n/search\t35.25\t210\t1999.9\n/health\t1\t1\t2\n")

text("pipes.txt", """
name|role|since
ada|admin|2019
grace||2021
|guest|
""")

# ------------------------------------------------------------ jobs

# Every format on the README's planets table.
for f in FORMATS:
    job(table="planets", headers="firstrow", tablefmt=f)

# Every format on a list of dicts with missing keys and None.
for f in FORMATS:
    job(table="servers", headers="keys", tablefmt=f, missingval="?")

# Multiline cells in the formats that fold them, and some that do not.
for f in ["simple", "grid", "fancy_grid", "pipe", "psql", "rst", "pretty",
          "orgtbl", "plain", "presto", "colon_grid", "rounded_outline",
          "jira", "github", "html", "latex", "tsv", "mediawiki", "nosuch"]:
    job(table="releases", headers="firstrow", tablefmt=f)
job(table="releases", headers="firstrow", tablefmt="grid", rowalign="bottom")
job(table="releases", headers="firstrow", tablefmt="grid", rowalign="center")
job(table="releases", headers="firstrow", tablefmt="grid",
    rowalign=["bottom", "top", "center"])
job(table="releases", headers="firstrow", tablefmt="simple",
    colalign=["right", "center", "right"])
job(table="releases", headers=["v\nersion", "date", "notes\n(short)"],
    tablefmt="psql")

# Separating lines.
for f in ["simple", "grid", "pipe", "plain", "html", "github", "psql",
          "fancy_outline", "latex"]:
    job(table="incidents", headers="firstrow", tablefmt=f)
job(table="incidents", headers="firstrow", tablefmt="simple", showindex=True)
job(table="incidents", headers="firstrow", tablefmt="grid", showindex="always")

# Column types, number parsing and alignment.
job(table="mixed", headers="firstrow")
job(table="mixed", headers="firstrow", tablefmt="grid")
job(table="mixed", headers="firstrow", tablefmt="grid", disable_numparse=True)
job(table="mixed", headers="firstrow", tablefmt="grid", disable_numparse=[1, 3])
job(table="mixed", headers="firstrow", tablefmt="pipe", numalign="right", stralign="center")
job(table="mixed", headers="firstrow", tablefmt="pipe", numalign=None, stralign=None)
job(table="mixed", headers="firstrow", tablefmt="psql", preserve_whitespace=True)
job(table="mixed", headers="firstrow", tablefmt="simple", floatfmt=".2f", missingval="N/A")
job(table="invoice", headers="firstrow", tablefmt="psql")
job(table="invoice", headers="firstrow", tablefmt="psql", floatfmt=",.2f")
job(table="invoice", headers="firstrow", tablefmt="pipe",
    colalign=["left", "left", "right", "decimal", "decimal"])
job(table="invoice", headers="firstrow", tablefmt="github",
    colglobalalign="center", colalign=["global", "right"])
job(table="invoice", headers="firstrow", tablefmt="rst")
job(table="numbers", headers="firstrow")
job(table="numbers", headers="firstrow", tablefmt="grid", intfmt=",")
job(table="numbers", headers="firstrow", tablefmt="grid",
    floatfmt=["", "", "", ".1%", ",.2f"], intfmt=["03d", "", "_"])
job(table="numbers", headers="firstrow", floatfmt=".3e")
job(table="numbers", headers="firstrow", floatfmt="")
job(table="numbers", headers="firstrow", floatfmt=".3")
job(table="numbers", headers="firstrow", floatfmt="#.4g")
job(table="numbers", headers="firstrow", floatfmt="+010.2f", intfmt="+")
job(table="numbers", headers="firstrow", floatfmt="z.1f")
job(table="numbers", headers="firstrow", floatfmt="d")
job(table="numbers", headers="firstrow", intfmt="x")
job(table="numbers", headers="firstrow", intfmt="#b")
job(table="numbers", headers="firstrow", intfmt=".2")
job(table="numbers", headers="firstrow", intfmt=",.2f")
job(table="numbers", headers="firstrow", intfmt="*^9,")
job(table="numbers", headers="firstrow", tablefmt="pretty")
job(table="bigints", headers="firstrow", tablefmt="psql", intfmt=",")
job(table="bigints", headers="firstrow", tablefmt="psql", floatfmt=".4g")
job(table="metrics", headers="firstrow", tablefmt="rounded_grid")
job(table="metrics", headers="firstrow", tablefmt="rounded_grid",
    floatfmt=".6f")
job(table="metrics", headers="firstrow", tablefmt="simple", floatfmt=",.3f")
job(table="metrics", headers="firstrow", tablefmt="simple", floatfmt=".2E")
job(table="metrics", headers="firstrow", tablefmt="simple", floatfmt="n")
job(table="metrics", headers="firstrow", tablefmt="simple", floatfmt="G")

# Headers and indexes.
job(table="planets")
job(table="planets", headers="keys")
job(table="planets", headers=["name", "radius"], tablefmt="grid")
job(table="planets", headers=["a", "b", "c", "d", "e"], tablefmt="grid")
job(table="planets", headers=[1, None, 2.5, True], tablefmt="pipe")
job(table="planets", headers="firstrow", showindex=True)
job(table="planets", headers="firstrow", showindex="always", tablefmt="psql")
job(table="planets", headers="firstrow", showindex="never")
job(table="planets", headers="firstrow", showindex=["a", "b", "c", "d"],
    tablefmt="github")
job(table="planets", headers="firstrow", showindex=["a", "b"])
job(table="planets", headers="firstrow", showindex=False)
job(table="servers")
job(table="servers", headers="firstrow", tablefmt="psql")
job(table="servers", headers={"host": "Host", "cpu": "CPU", "healthy": "OK?"},
    tablefmt="psql")
job(table="servers", headers=["x", "y"])
job(table="servers", headers="keys", showindex="always", tablefmt="simple")
job(table="quarters", headers="keys", tablefmt="psql")
job(table="quarters", headers="keys", tablefmt="psql", floatfmt=",.0f",
    missingval="-")
job(table="quarters", headers="keys", tablefmt="psql",
    missingval=["", "?", "??", "???"])
job(table="quarters", tablefmt="simple")
job(table="quarters", headers="firstrow", tablefmt="simple")
job(table="empty", headers=["a", "b", "c"], tablefmt="grid")
job(table="empty", headers=["a", "b", "c"], tablefmt="pipe")
job(table="empty", headers=["a", "b", "c"], tablefmt="html")
job(table="empty", headers="keys", tablefmt="grid")
job(table="empty", headers="firstrow")
job(table="empty")
job(table="onecol", headers="firstrow", tablefmt="fancy_grid")
job(table="onecol", tablefmt="latex_booktabs")
job(table="ragged", tablefmt="grid")
job(table="ragged", headers=["k", "v"], tablefmt="grid", missingval="--")
job(table="ragged", headers="firstrow", tablefmt="psql")
job(table="cities", headers="firstrow", tablefmt="fancy_outline")
job(table="cities", headers="firstrow", tablefmt="pipe", intfmt=",")

# Header alignment.
job(table="planets", headers="firstrow", tablefmt="pipe",
    headersglobalalign="center")
job(table="planets", headers="firstrow", tablefmt="pipe",
    headersalign=["right", "same", "left"])
job(table="planets", headers="firstrow", tablefmt="grid",
    colalign=["center", "left"], headersalign=["same", "global", "center"])
job(table="planets", headers="firstrow", tablefmt="latex",
    headersalign=["right", "center"])
job(table="ragged", headers=["only"], tablefmt="grid",
    headersalign=["right", "center"])

# Escaping.
for f in ["html", "unsafehtml", "latex", "latex_raw", "rst", "mediawiki",
          "moinmoin", "textile", "asciidoc", "jira", "youtrack", "tsv"]:
    job(table="markup", tablefmt=f)
job(table="markup", headers=["", "offer", "html"], tablefmt="rst")

# ANSI colour codes and hyperlinks.
for f in ["simple", "grid", "pipe", "psql", "html", "pretty"]:
    job(table="status", headers="firstrow", tablefmt=f)
job(table="status", headers="firstrow", tablefmt="grid", intfmt=",")
job(table="status", headers="firstrow", tablefmt="grid", maxcolwidths=4)

# Wrapping to a column width.
job(table="articles", headers="keys", tablefmt="grid", maxcolwidths=[None, 30])
job(table="articles", headers="keys", tablefmt="grid", maxcolwidths=[12, 24])
job(table="articles", headers="keys", tablefmt="simple", maxcolwidths=16,
    missingval="(none)")
job(table="articles", headers="keys", tablefmt="grid", maxcolwidths=[12, 24],
    break_long_words=False)
job(table="articles", headers="keys", tablefmt="grid", maxcolwidths=[12, 24],
    break_on_hyphens=False)
job(table="articles", headers="keys", tablefmt="fancy_grid",
    maxcolwidths=[20, 40], maxheadercolwidths=3)
job(table="articles", headers="keys", tablefmt="grid", maxcolwidths=[8],
    maxheadercolwidths=[2, None, 3], rowalign="bottom")
job(table="articles", headers="keys", tablefmt="grid", maxcolwidths=[0])
job(table="flags", headers="firstrow", tablefmt="grid")
job(table="flags", headers="firstrow", tablefmt="grid", maxcolwidths=10)
job(table="mixed", headers="firstrow", tablefmt="grid", maxcolwidths=3)
job(table="mixed", headers="firstrow", tablefmt="grid", maxcolwidths=3, disable_numparse=True)
job(table="numbers", headers="firstrow", tablefmt="grid", maxcolwidths=2)

# Float formatting on its own, as tabulate's floatfmt does it.
VALUES = [0.0, -0.0, 1.0, 0.5, 1.5, 2.5, 2.675, 0.125, 0.1, 1e-5, 123.456,
          1234567.891, 1e16, 1e22, 12345678.0, 100000.0, 5e-324,
          1.7976931348623157e308, -273.15, 0.0001234, 9007199254740993, 7, -42]
for spec in ["g", "", ".3", ".0", "#.3", ".2f", ".0f", "#.0f", ".25f",
             ".3e", "E", "#.0e", ".2%", "%", "G", "#g", ".10g", "+,.2f",
             "=+15,.3f", "*^14.1f", "012.3e", "z.1f", " .2f", "_.1f",
             ",", "_", ">12", "<12g", "^12.4", "n", "d", ".2s", "q", "+-.2f",
             ",_f", ".f"]:
    job(format=spec, values=VALUES)
job(format="08.2f", values=["inf", "-inf", "nan", "1e999", "-1_000.5", " 2 "])
job(format=".3g", values=["inf", "nan", "Infinity", "+inf", "1,000", "0x1"])

# The command-line tool.
job(cli=["data/text/df.txt"])
job(cli=["-1", "-f", "psql", "data/text/df.txt"])
job(cli=["-1", "-s", ":", "-f", "grid", "data/text/passwd"])
job(cli=["--header", "--sep=,", "--format", "pipe", "-F", ".2f",
         "data/text/prices.csv"])
job(cli=["-1", "-s", ",", "-I", ",", "-f", "github", "data/text/prices.csv"])
job(cli=["-1", "-f", "simple", "data/text/ps.txt"])
job(cli=["-1", "-s", "\\t", "-f", "rst", "data/text/latency.tsv"])
job(cli=["-1", "-s", "\\|", "-f", "outline", "data/text/pipes.txt"])
job(cli=["-1", "--colalign", "right left center", "-f", "grid",
         "data/text/latency.tsv"])
job(cli=["-1", "-f", "plain", "data/text/ps.txt", "data/text/df.txt"])
job(cli=["-f", "nosuch", "data/text/df.txt"])
job(cli=["-C", "right", "data/text/df.txt"])
job(cli=["-h"])

with open("data/jobs.jsonl", "w") as f:
    f.write("\n".join(jobs) + "\n")
