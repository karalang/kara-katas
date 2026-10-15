# Writes data/: two SQLite databases made with Python's sqlite3, a file
# that is not a database, and the lookups the reader runs.
import os, random, shutil, sqlite3

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data")
rng = random.Random(20261015)

FIRST = ["Ada", "Grace", "Linus", "Zoë", "Jürgen", "Søren", "Amélie", "Hiroshi", "Mei", "Olu",
         "Priya", "Mateo", "Ines", "Kwame", "Lena", "Arjun", "Noor", "Tomás", "Yuki", "Elif"]
LAST = ["Lovelace", "Hopper", "Okafor", "Müller", "Kierkegaard", "Poulain", "東京", "Chen", "Adeyemi",
        "Sharma", "García", "Silva", "Mensah", "Novak", "Rao", "Haddad", "Ferreira", "Sato", "Yılmaz", "Ng"]
COUNTRIES = ["DE", "FR", "GB", "IN", "JP", "NG", "US", "BR", "TR", "DK"]
WORDS = ("order shipped late customer asked refund warehouse parcel tracking invoice discount "
         "loyal returns address changed fragile gift wrap express courier weekend café naïve").split()


def para(n):
    return " ".join(rng.choice(WORDS) for _ in range(n))


db = sqlite3.connect("data/shop.db")
db.execute("PRAGMA page_size = 1024")
db.execute("PRAGMA user_version = 7")
db.execute("PRAGMA application_id = 1262571073")
db.executescript("""
CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT UNIQUE,
                       country TEXT, balance REAL, notes TEXT);
CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL,
                    total_cents INTEGER, placed TEXT, status TEXT, items BLOB);
CREATE INDEX idx_orders_customer ON orders(customer_id, placed);
CREATE TABLE kv(key TEXT PRIMARY KEY, value) WITHOUT ROWID;
CREATE VIEW big_spenders AS
  SELECT customer_id, sum(total_cents) AS spent FROM orders GROUP BY customer_id HAVING spent > 100000;
CREATE TRIGGER orders_audit AFTER DELETE ON orders BEGIN
  INSERT INTO kv(key, value) VALUES ('deleted:' || old.id, old.total_cents);
END;
""")
emails = []
for i in range(1, 121):
    name = f"{FIRST[i % 20]} {LAST[(i * 7) % 20]}"
    email = f"{name.split()[0].lower()}.{i}@example.{COUNTRIES[i % 10].lower()}"
    emails.append(email)
    if i % 17 == 0:
        email = None
    balance = None if i % 11 == 0 else round(rng.uniform(-500, 5000), 2)
    if i % 13 == 0:
        balance = [0.1, 1e100, -2.5e-8, 123456789.125, 3.0][i // 13 % 5]
    if i % 9 == 0:
        notes = para(400 + 37 * (i % 5))
    elif i % 4 == 0:
        notes = None
    else:
        notes = para(3 + i % 6)
    db.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)",
               (i, name, email, COUNTRIES[(i * 3) % 10], balance, notes))
db.execute("ALTER TABLE customers ADD COLUMN tier TEXT DEFAULT 'basic'")
db.execute("ALTER TABLE customers ADD COLUMN visits INTEGER DEFAULT 0")
db.execute("ALTER TABLE customers ADD COLUMN score REAL DEFAULT -1.5")
db.execute("UPDATE customers SET tier = 'gold', visits = id * 3 WHERE id % 10 = 0")
db.execute("UPDATE customers SET visits = NULL, score = 4.25 WHERE id % 25 = 0")

STATUS = ["paid", "shipped", "refunded", "pending", "cancelled"]
totals = [0, 1, 127, 128, -129, 32767, 32768, -8388608, 8388608, 2**31, -2**31 - 1,
          2**47 - 1, 2**47, -2**63, 2**63 - 1]
for i in range(1, 701):
    t = totals[i % len(totals)] if i % 9 == 0 else rng.randrange(-5000, 250000)
    day = 1 + (i * 13) % 28
    month = 1 + (i * 5) % 12
    items = bytes(rng.randrange(256) for _ in range(i % 12)) if i % 3 else None
    status = None if i % 50 == 0 else STATUS[i % 5]
    db.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
               (i, 1 + (i * 31) % 120, t, f"2026-{month:02d}-{day:02d}T{(i * 7) % 24:02d}:00:00Z", status, items))
db.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",
           (2**40, 5, 99, "2026-12-31T23:59:59Z", "paid", b"\x00\xff"))
for i in range(80):
    key = f"{['cfg', 'flag', 'stat', 'note'][i % 4]}:{i:03d}"
    value = [i * 1000, i / 8, f"v{i}", bytes([i, 255 - i]), None, para(30) if i % 20 == 3 else -i][i % 6]
    db.execute("INSERT INTO kv VALUES (?, ?)", (key, value))
db.commit()
db.execute("DELETE FROM orders WHERE id % 7 = 3")
db.execute("UPDATE customers SET notes = NULL WHERE id % 18 = 0")
db.execute("DELETE FROM customers WHERE id IN (111, 112, 113)")
db.commit()
db.close()

db = sqlite3.connect("data/notes16.db")
db.execute("PRAGMA encoding = 'UTF-16le'")
db.execute("PRAGMA page_size = 512")
db.execute("PRAGMA auto_vacuum = FULL")
db.executescript("""
CREATE TABLE notes(id INTEGER PRIMARY KEY, title TEXT, body TEXT, tags TEXT);
CREATE INDEX idx_notes_title ON notes(title);
""")
TITLES = ["Groceries", "Café list 🍰", "Reise nach Köln", "東京 trip", "Ideas", "Ünïcödé", "Bugs 🐛",
          "Books", "Привет", "naïve plan"]
for i in range(1, 41):
    body = para(5 + (i * 11) % 90) if i % 6 else para(200) + " 🎉"
    db.execute("INSERT INTO notes VALUES (?, ?, ?, ?)",
               (i, f"{TITLES[i % 10]} #{i}", body, None if i % 4 == 0 else ",".join(rng.sample(WORDS, 2))))
db.commit()
db.execute("DELETE FROM notes WHERE id % 5 = 2")
db.commit()
db.close()

with open("data/bad.db", "w") as f:
    f.write("id,name\n1,this is a CSV file, not a database\n")

with open("data/lookups.txt", "w") as f:
    f.write("# email lookups through the UNIQUE index, then orders through idx_orders_customer\n")
    for i in [1, 9, 17, 50, 111, 120]:
        f.write(f"email {emails[i - 1]}\n")
    f.write("email nobody@example.com\n")
    f.write("email \n")
    for c in [5, 31, 64, 119, 121]:
        f.write(f"orders {c}\n")
    f.write("rows orders 100 130\n")
    f.write("rows orders 690 1099511627776\n")
    f.write("rows customers 109 115\n")
