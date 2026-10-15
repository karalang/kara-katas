# The oracle: the same report as mini_csv, made with Python 3.13's csv
# module. Run it from this directory after mk.py.
import csv, io, os

CHARS = {"comma": ",", "tab": "\t", "semicolon": ";", "pipe": "|", "space": " ",
         "colon": ":", "dquote": '"', "squote": "'", "backslash": "\\", "none": None,
         "crlf": "\r\n", "lf": "\n", "cr": "\r"}
QUOTING = {"minimal": csv.QUOTE_MINIMAL, "all": csv.QUOTE_ALL, "nonnumeric": csv.QUOTE_NONNUMERIC,
           "none": csv.QUOTE_NONE, "strings": csv.QUOTE_STRINGS, "notnull": csv.QUOTE_NOTNULL}

def options(words):
    kw = {}
    extra = {}
    for w in words:
        k, v = w.split("=")
        if k in ("delimiter", "quotechar", "escapechar", "lineterminator"):
            kw[k] = CHARS[v]
        elif k in ("doublequote", "skipinitialspace", "strict"):
            kw[k] = v == "1"
        elif k == "quoting":
            kw[k] = QUOTING[v]
        else:
            extra[k] = v
    return kw, extra

def text_of(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()

print("== read")
for line in text_of("data/read-jobs.txt").split("\n")[:-1]:
    words = line.split()
    kw, extra = options(words[1:])
    print(f"-- {line}")
    text = text_of("data/" + words[0])
    src = io.StringIO(text) if extra.get("source") == "text" else io.StringIO(text, newline="")
    csv.field_size_limit(int(extra.get("limit", "131072")))
    try:
        r = csv.reader(src, **kw)
        while True:
            try:
                row = next(r)
            except StopIteration:
                break
            print(f"  {r.line_num} {row!r}")
    except csv.Error as e:
        print(f"  Error: {e} (line {r.line_num})")
csv.field_size_limit(131072)

ROWS = [
    ["id", "name", "note", "amount"],
    [1, "plain", "", 2.5],
    [2, "has,comma", 'say "hi"', -3],
    [3, "multi\nline", "cr\rhere", None],
    [4, " lead space", "back\\slash", 0.1],
    [5, "tab\there", "semi;colon", 10],
    [6, "it's", "a b", "'q'"],
    [""],
    [None],
    [],
]

print("== write")
for line in text_of("data/write-jobs.txt").split("\n")[:-1]:
    kw, _ = options(line.split())
    print(f"-- {line or 'excel'}")
    for row in ROWS:
        buf = io.StringIO(newline="")
        w = csv.writer(buf, **kw)
        try:
            w.writerow(row)
            print(f"  {buf.getvalue()!r}")
        except csv.Error as e:
            print(f"  Error: {e}")

print("== dict")
with open("data/ragged.csv", newline="", encoding="utf-8") as f:
    r = csv.DictReader(f, restkey="_extra", restval="N/A")
    print(f"  fieldnames {r.fieldnames!r}")
    for d in r:
        print(f"  {r.line_num} {d!r}")
with open("data/headerless.csv", newline="", encoding="utf-8") as f:
    r = csv.DictReader(f, fieldnames=["key", "value"])
    for d in r:
        print(f"  {r.line_num} {d!r}")
with open("data/dupcols.csv", newline="", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for d in r:
        print(f"  {r.line_num} {d!r}")
DICTS = [{"id": 1, "name": "Ann"}, {"email": "bo@example.org", "id": 2, "name": "Bo, Jr."},
         {"id": 3, "phone": "555"}, {}]
for action in ("raise", "ignore"):
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, ["id", "name", "email"], restval="-", extrasaction=action)
    w.writeheader()
    for d in DICTS:
        try:
            w.writerow(d)
        except ValueError as e:
            buf.write(f"<{e}>")
    print(f"  {action}: {buf.getvalue()!r}")

print("== sniff")
for name in sorted(os.listdir("data/sniff")):
    sample = text_of("data/sniff/" + name)
    try:
        d = csv.Sniffer().sniff(sample)
    except csv.Error as e:
        print(f"{name}: Error: {e}")
        continue
    try:
        header = csv.Sniffer().has_header(sample)
    except (csv.Error, ValueError) as e:
        header = f"Error: {e}"
    print(f"{name}: delimiter={d.delimiter!r} quotechar={d.quotechar!r} doublequote={d.doublequote} "
          f"skipinitialspace={bool(d.skipinitialspace)} header={header}")
    try:
        for row in csv.reader(io.StringIO(sample), d):
            print(f"  {row!r}")
    except (csv.Error, ValueError) as e:
        print(f"  Error: {e}")

print("== report")
def cents(s):
    neg = s.startswith("-")
    s = s.lstrip("-").replace(".", "")
    euros, _, frac = s.partition(",")
    n = int(euros) * 100 + int((frac + "00")[:2])
    return -n if neg else n

def money(n):
    sign = "-" if n < 0 else ""
    n = abs(n)
    return f"{sign}{n // 100}.{n % 100:02d}"

text = text_of("data/orders.csv")
dialect = csv.Sniffer().sniff(text)
print(f"sniffed delimiter={dialect.delimiter!r} header={csv.Sniffer().has_header(text)}")
rows = list(csv.DictReader(io.StringIO(text, newline=""), dialect=dialect))
os.makedirs("data/out", exist_ok=True)
totals = {}
counts = {}
with open("data/out/orders_clean.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    w.writerow(["order", "date", "country", "customer", "amount", "status"])
    for r in rows:
        c = cents(r["Betrag"])
        w.writerow([int(r["Bestellung"]), r["Datum"], r["Land"], " ".join(r["Kunde"].split()), money(c), r["Status"]])
        if r["Status"] in ("bezahlt", "erstattet"):
            totals[r["Land"]] = totals.get(r["Land"], 0) + c
            counts[r["Land"]] = counts.get(r["Land"], 0) + 1
with open("data/out/summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, ["country", "orders", "revenue"], lineterminator="\n")
    w.writeheader()
    for k in sorted(totals):
        w.writerow({"country": k, "orders": counts[k], "revenue": money(totals[k])})
    w.writerow({"country": "total", "orders": sum(counts.values()), "revenue": money(sum(totals.values()))})
for name in ("orders_clean.csv", "summary.csv"):
    print(f"-- data/out/{name}")
    print(repr(text_of("data/out/" + name)))
    with open("data/out/" + name, newline="", encoding="utf-8") as f:
        back = list(csv.reader(f, quoting=csv.QUOTE_NONNUMERIC if name == "orders_clean.csv" else csv.QUOTE_MINIMAL))
    print(f"  read back: {len(back)} rows, last {back[-1]!r}")
