# Writes data/: five SQLite databases made with Python's sqlite3 (SQLite
# 3.45), a file that is not a database, an empty file, and data/jobs.txt,
# the jobs oracle.py and mini_read_sql.kara run.
#
# Run from this directory: python3 -s -P -B mk.py
import datetime as dt
import os
import random
import shutil
import sqlite3

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data")
rng = random.Random(20261029)

FIRST = ["Ada", "Grace", "Linus", "Zoë", "Jürgen", "Søren", "Amélie", "Hiroshi", "Mei", "Olu",
         "Priya", "Mateo", "Inès", "Kwame", "Lena", "Arjun", "Noor", "Tomás", "Yuki", "Elif"]
LAST = ["Lovelace", "Hopper", "Okafor", "Müller", "Berg", "Poulain", "Tanaka", "Chen", "Adeyemi",
        "Sharma", "García", "Silva", "Mensah", "Novak", "Rao", "Haddad", "Ferreira", "Sato", "Yılmaz", "Ng"]
PLACES = [("DE", "Berlin"), ("DE", "München"), ("FR", "Lyon"), ("FR", "Paris"), ("GB", "Leeds"),
          ("IN", "Pune"), ("JP", "Ōsaka"), ("NG", "Lagos"), ("US", "Austin"), ("US", "Boston"),
          ("BR", "Recife"), ("TR", "İzmir")]


def connect(name, page_size, encoding=None):
    db = sqlite3.connect(os.path.join("data", name))
    if encoding:
        db.execute(f"PRAGMA encoding = '{encoding}'")
    db.execute(f"PRAGMA page_size = {page_size}")
    return db


# ------------------------------------------------------------ shop.db
db = connect("shop.db", 1024)
db.executescript("""
CREATE TABLE customers(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT COLLATE NOCASE UNIQUE,
  country TEXT,
  city TEXT,
  signup DATE,
  balance REAL,
  vip BOOLEAN DEFAULT 0
);
CREATE TABLE products(
  sku TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  category TEXT,
  price DECIMAL(8,2),
  weight_g INTEGER,
  launched DATE
) WITHOUT ROWID;
CREATE TABLE orders(
  id INTEGER PRIMARY KEY,
  customer_id INTEGER REFERENCES customers(id),
  placed TEXT,
  status TEXT,
  total_cents INTEGER,
  coupon TEXT
);
CREATE TABLE order_items(order_id INTEGER, sku TEXT, qty INTEGER, unit_price REAL);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_items_order ON order_items(order_id);
CREATE VIEW order_totals AS
  SELECT o.id AS order_id, o.customer_id, count(*) AS lines, sum(i.qty * i.unit_price) AS amount
  FROM orders o JOIN order_items i ON i.order_id = o.id
  GROUP BY o.id;
""")
CATS = ["kitchen", "garden", "books", "toys", "audio"]
products = []
for k in range(25):
    sku = f"{CATS[k % 5][:3].upper()}-{100 + k * 7}"
    title = ["Kettle", "Trowel", "Atlas", "Kite", "Speaker", "Teapot", "Hose", "Novel", "Puzzle",
             "Headphones"][k % 10] + (f" {k // 10 + 1}" if k >= 10 else "")
    price = [4.99, 12.5, 19.99, 0.1, 249.0, 33.33, 7.25, 15.0, 2.675, 89.9][k % 10] + (k // 10) * 10
    price = round(price, 3)
    weight = None if k % 8 == 3 else 50 + k * 37
    launched = None if k % 6 == 5 else f"20{19 + k % 7}-{1 + k % 12:02d}-{1 + (k * 5) % 28:02d}"
    products.append((sku, title, CATS[k % 5], price))
    db.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)",
               (sku, title, CATS[k % 5] if k != 17 else None, price, weight, launched))
for i in range(1, 61):
    country, city = PLACES[(i * 5) % 12]
    name = f"{FIRST[i % 20]} {LAST[(i * 7) % 20]}"
    email = f"{name.split()[0].lower()}.{i}@example.com"
    if i % 9 == 0:
        email = email.upper()
    if i % 23 == 0:
        email = None
    signup = (dt.date(2024, 1, 1) + dt.timedelta(days=i * 11)).isoformat()
    if i % 19 == 0:
        signup = None
    balance = None if i % 11 == 0 else round(rng.uniform(-50, 900), 2)
    vip = ["0", "1", "yes", 1, None][i % 5] if i % 3 == 0 else 0
    db.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               (i, name, email, country, city if i % 13 else None, signup, balance, vip))
db.execute("ALTER TABLE customers ADD COLUMN tier TEXT DEFAULT 'basic'")
db.execute("UPDATE customers SET tier = 'gold' WHERE id % 7 = 0")
STATUS = ["paid", "shipped", "delivered", "cancelled", "refunded"]
t0 = dt.datetime(2026, 1, 3, 9, 15)
for o in range(1, 301):
    cust = 1 + int(60 * rng.random() ** 1.6)
    if o % 50 == 0:
        cust = 999  # an order whose customer was deleted
    placed = t0 + dt.timedelta(hours=o * 23 + (o * 7) % 13, minutes=(o * 17) % 60)
    status = STATUS[(o * 3) % 5] if o % 4 else "delivered"
    coupon = ["SPRING10", "spring10", None, None, "VIP", None][o % 6]
    lines = 1 + (o * 13) % 4
    total = 0
    for ln in range(lines):
        k = (o * 7 + ln * 11) % 25
        qty = 1 + (o + ln) % 3
        price = products[k][3]
        total += round(qty * price * 100)
        db.execute("INSERT INTO order_items VALUES (?, ?, ?, ?)", (o, products[k][0], qty, price))
    db.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
               (o, cust, placed.strftime("%Y-%m-%d %H:%M:%S"), status, total, coupon))
db.execute("DELETE FROM orders WHERE id IN (17, 18, 19)")
db.commit()
db.close()

# ------------------------------------------------------------ history.db
# A browser history, laid out like Chromium's: times are microseconds
# since 1601-01-01 UTC.
db = connect("history.db", 1024)
db.executescript("""
CREATE TABLE urls(id INTEGER PRIMARY KEY AUTOINCREMENT, url LONGVARCHAR, title LONGVARCHAR,
  visit_count INTEGER DEFAULT 0 NOT NULL, typed_count INTEGER DEFAULT 0 NOT NULL,
  last_visit_time INTEGER NOT NULL, hidden INTEGER DEFAULT 0 NOT NULL);
CREATE TABLE visits(id INTEGER PRIMARY KEY, url INTEGER NOT NULL, visit_time INTEGER NOT NULL,
  from_visit INTEGER, transition INTEGER DEFAULT 0 NOT NULL, visit_duration INTEGER DEFAULT 0 NOT NULL);
CREATE INDEX visits_url_index ON visits (url);
CREATE INDEX visits_time_index ON visits (visit_time);
""")
SITES = ["https://docs.python.org/3/library/sqlite3.html", "https://pandas.pydata.org/docs/",
         "https://www.sqlite.org/lang_select.html", "https://news.example.org/", "https://mail.example.com/inbox",
         "https://en.wikipedia.org/wiki/B-tree", "https://github.com/karalang/kara", "https://maps.example.com/?q=Lyon",
         "https://www.sqlite.org/datatype3.html", "https://shop.example.com/cart", "https://weather.example.net/lyon",
         "https://en.wikipedia.org/wiki/Julian_day"]
TITLES = ["sqlite3 — DB-API 2.0 interface for SQLite databases", "pandas documentation", "SELECT",
          "Example News", "Inbox (3)", "B-tree - Wikipedia", "karalang/kara", None, "Datatypes In SQLite",
          "Your cart", "Lyon weather", "Julian day - Wikipedia"]
EPOCH_1601 = 11644473600
base = (dt.datetime(2026, 10, 20, 7, 0) - dt.datetime(1970, 1, 1)).total_seconds()
for k, (u, t) in enumerate(zip(SITES, TITLES)):
    db.execute("INSERT INTO urls(url, title, last_visit_time, hidden) VALUES (?, ?, 0, ?)", (u, t, int(k == 7)))
db.execute("DELETE FROM urls WHERE id = 4")
db.execute("INSERT INTO urls(url, title, last_visit_time) VALUES ('https://news.example.org/today', 'Today', 0)")
vid = 0
prev = None
for n in range(320):
    vid += 1
    u = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13][(n * 7 + n // 5 + (n * n) % 5) % 12]
    secs = base + n * 1597 + (n * 7919) % 600
    when = int((secs + EPOCH_1601) * 1_000_000) + (n * 123457) % 1_000_000
    core = [0, 1, 0, 2, 8, 0, 1, 5][n % 8]
    quals = [0x01000000, 0x10000000, 0x20000000, 0x30000000][n % 4]
    duration = 0 if n % 6 == 0 else (n * 2654435761) % 900_000_000
    db.execute("INSERT INTO visits VALUES (?, ?, ?, ?, ?, ?)",
               (vid, u, when, prev if n % 3 else 0, core | quals, duration))
    prev = vid
db.execute("""UPDATE urls SET visit_count = (SELECT count(*) FROM visits WHERE visits.url = urls.id),
  typed_count = (SELECT count(*) FROM visits WHERE visits.url = urls.id AND (transition & 255) = 1),
  last_visit_time = coalesce((SELECT max(visit_time) FROM visits WHERE visits.url = urls.id), 0)""")
db.commit()
db.close()

# ------------------------------------------------------------ sensors.db
db = connect("sensors.db", 512)
db.executescript("""
CREATE TABLE devices(device TEXT PRIMARY KEY, site TEXT NOT NULL, installed TEXT, firmware TEXT);
CREATE TABLE readings(device TEXT NOT NULL, ts INTEGER NOT NULL, temp_c REAL, humidity REAL, battery INTEGER);
""")
DEVS = [("th-01", "greenhouse", "2026-03-14", "1.4.2"), ("th-02", "greenhouse", "2026-03-14", "1.4.2"),
        ("th-03", "cellar", "2026-05-02", "1.5.0"), ("th-04", "attic", None, "1.3.9"),
        ("th-05", "cellar", "2026-07-30", None)]
db.executemany("INSERT INTO devices VALUES (?, ?, ?, ?)", DEVS)
start = int((dt.datetime(2026, 10, 25, 0, 0) - dt.datetime(1970, 1, 1)).total_seconds())
for n in range(960):
    d = n % 4
    dev = DEVS[d][0] if n % 97 else "th-09"
    ts = start + (n // 4) * 1800 + d * 7
    hour = ((n // 4) * 30 // 60) % 24
    temp = [21.0, 22.5, 12.0, 18.0][d] + (hour - 12) * [0.35, 0.3, 0.05, 0.5][d] + ((n * 37) % 11 - 5) / 10
    temp = round(temp, 2)
    if n % 53 == 0:
        temp = None
    if n % 211 == 7:
        temp = -999.0
    hum = round(55 + ((n * 13) % 30) - d * 4 + 0.25 * (n % 3), 1)
    if n % 31 == 0:
        hum = None
    battery = 100 - (n // 4) // 3 - d * 5
    db.execute("INSERT INTO readings VALUES (?, ?, ?, ?, ?)", (dev, ts, temp, hum, battery))
db.commit()
db.close()

# ------------------------------------------------------------ ledger16.db
# A personal-finance export, in UTF-16le, with amounts given as text the
# way a CSV import hands them over.
db = connect("ledger16.db", 1024, "UTF-16le")
db.executescript("""
CREATE TABLE accounts(id INTEGER PRIMARY KEY, name TEXT, currency TEXT);
CREATE TABLE txns(id INTEGER PRIMARY KEY, account_id INTEGER, booked TEXT, amount NUMERIC,
  payee TEXT COLLATE NOCASE, memo TEXT, category TEXT);
""")
db.executemany("INSERT INTO accounts VALUES (?, ?, ?)",
               [(1, "Girokonto", "EUR"), (2, "Visa ✈", "EUR"), (3, "Savings", "GBP")])
PAYEES = ["Café Müller", "café müller", "REWE", "Rewe", "Deutsche Bahn", "Stadtwerke", "Ünal Market",
          "Spotify", "Arbeitgeber GmbH", "Bäckerei Groß", "Amazon", "ÖBB"]
CATEG = {"Café Müller": "eating out", "café müller": "eating out", "REWE": "groceries", "Rewe": "groceries",
         "Deutsche Bahn": "travel", "Stadtwerke": "utilities", "Ünal Market": "groceries", "Spotify": "subscriptions",
         "Arbeitgeber GmbH": "salary", "Bäckerei Groß": "eating out", "Amazon": None, "ÖBB": "travel"}
day = dt.date(2026, 7, 1)
for t in range(1, 151):
    p = PAYEES[(t * 5) % 12]
    acct = 3 if p == "Arbeitgeber GmbH" and t % 2 else 1 + (t * 3) % 2
    if p == "Arbeitgeber GmbH":
        amount = "2850.00" if t % 3 else "2850"
    else:
        cents = 100 + (t * 7919) % 9000
        amount = [f"-{cents // 100}.{cents % 100:02d}", f"-{cents // 100}", f"-{cents / 100:.1f}",
                  f"-1,{cents % 1000:03d}.00"][t % 4 if t % 17 else 3]
    if t % 29 == 0:
        amount = None
    booked = (day + dt.timedelta(days=(t * 2) // 3)).strftime("%Y-%m-%d") if t % 41 else (
        day + dt.timedelta(days=t // 2)).strftime("%d.%m.%Y")
    memo = None if t % 4 else f"Ref {t * 97:06d} – {p.split()[0]}"
    db.execute("INSERT INTO txns VALUES (?, ?, ?, ?, ?, ?, ?)", (t, acct, booked, amount, p, memo, CATEG[p]))
db.commit()
db.close()

# ------------------------------------------------------------ mixed.db
# One column of each declared type, filled with the same values, so the
# affinity rules show; and a table loaded from a CSV with every column TEXT.
db = connect("mixed.db", 4096)
db.executescript("""
CREATE TABLE typed(id INTEGER PRIMARY KEY, label TEXT, anything, n NUMERIC, t TEXT, r REAL, i INTEGER,
  d DATETIME, flag BOOLEAN, price DECIMAL(10,2), code VARCHAR(8), raw BLOB, f FLOATING POINT, ch CHARINT);
CREATE TABLE imported(region TEXT, month TEXT, units TEXT, revenue TEXT);
CREATE TABLE kv(k TEXT PRIMARY KEY, v) WITHOUT ROWID;
""")
VALUES = [("int", 42), ("text int", "42"), ("text real", "3.50"), ("real", 3.5), ("whole real", 7.0),
          ("text exp", "1e3"), ("padded", " 12 "), ("hex text", "0x1A"), ("word", "abc"),
          ("date text", "2026-10-29"), ("compact date", "20261029"), ("blob", b"AB"),
          ("null", None), ("big", 9223372036854775807), ("text big", "9223372036854775808"),
          ("neg zero", -0.0), ("tiny", 1e-7), ("true", "true"), ("comma", "1,5"), ("empty", "")]
for k, (label, v) in enumerate(VALUES, 1):
    db.execute("INSERT INTO typed VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (k, label) + (v,) * 12)
REG = ["North", "South", "East", "West"]
for m in range(1, 13):
    for r in REG:
        units = (m * 37 + len(r) * 11) % 120
        rev = units * [9.99, 12.5, 7.0, 10.25][REG.index(r)]
        db.execute("INSERT INTO imported VALUES (?, ?, ?, ?)",
                   (r, f"2026-{m:02d}", str(units), f"{rev:.2f}" if (m + len(r)) % 9 else ""))
db.executemany("INSERT INTO kv VALUES (?, ?)", [("schema", 3), ("owner", "ops"), ("ratio", 0.75),
                                                ("logo", b"\x89PNG"), ("note", None)])
db.commit()
db.close()

with open("data/notadb.db", "w", encoding="utf-8") as fh:
    fh.write("id,name\n1,Ada\n2,Grace\n" * 40)
open("data/empty.db", "wb").close()

with open("jobs.txt", encoding="utf-8") as fh:
    jobs = fh.read()
with open("data/jobs.txt", "w", encoding="utf-8") as fh:
    fh.write(jobs)
