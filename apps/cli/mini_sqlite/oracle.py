# The oracle for mini_sqlite: the same report made through Python's
# sqlite3 (SQLite 3.45). Contents come from SELECTs, page details from
# the dbstat virtual table, and pointer-map entries are derived from
# dbstat's page paths. Run it from this directory after mk.py.
import sqlite3

KINDS = {1: "root", 2: "free", 3: "overflow1", 4: "overflow2", 5: "btree"}


def text(v):
    if v is None:
        return "NULL"
    if isinstance(v, bytes):
        h = v[:16].hex()
        return f"x'{h}'" + (f" +{len(v) - 16}" if len(v) > 16 else "")
    if isinstance(v, str):
        return repr(v[:40]) + (f" +{len(v) - 40}" if len(v) > 40 else "")
    return repr(v)


def row(r):
    return ", ".join(text(v) for v in r)


def report(path, lookups):
    print(f"== {path}")
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        q = lambda s, *a: db.execute(s, a).fetchall()
        size = q("PRAGMA page_size")[0][0]
        count = q("PRAGMA page_count")[0][0]
    except sqlite3.DatabaseError as e:
        print(f"error: {e}")
        return
    v = sqlite3.sqlite_version_info
    av = ["none", "full", "incremental"][q("PRAGMA auto_vacuum")[0][0]]
    print(f"page size {size}, {count} pages, {q('PRAGMA encoding')[0][0]}, auto-vacuum {av}")
    print(f"schema version {q('PRAGMA schema_version')[0][0]}, user version {q('PRAGMA user_version')[0][0]}, "
          f"application id {q('PRAGMA application_id')[0][0]}, written by {v[0] * 1000000 + v[1] * 1000 + v[2]}")
    print(f"{q('PRAGMA freelist_count')[0][0]} free pages")
    schema = q("SELECT type, name, tbl_name, rootpage, sql FROM sqlite_schema")
    print("-- schema")
    for t, n, tb, root, sql in schema:
        print(f"{t} {n} on {tb}, root {root}: {text(sql)}")
    print("-- pages")
    stat = q("SELECT pageno, pagetype, name, path, ncell, payload, unused, mx_payload FROM dbstat")
    by_page = {r[0]: r for r in stat}
    by_path = {(r[2], r[3]): r[0] for r in stat}
    usable = size
    ptrmaps = set()
    if av != "none":
        p = 2
        while p <= count:
            ptrmaps.add(p)
            p += usable // 5 + 1
    for p in range(1, count + 1):
        if p in by_page:
            _, kind, name, pth, n, pay, unused, mx = by_page[p]
            print(f"{p:4} {kind:8} {name} {pth} cells {n}, payload {pay}, unused {unused}, max {mx}")
        else:
            print(f"{p:4} {'ptrmap' if p in ptrmaps else 'free'}")
    if ptrmaps:
        print("-- pointer map")
        ents = []
        for p in range(3, count + 1):
            if p in ptrmaps:
                continue
            if p not in by_page:
                ents.append(f"{p} free 0")
                continue
            _, kind, name, pth, *_ = by_page[p]
            if pth == "/":
                ents.append(f"{p} root 0")
            elif kind == "overflow":
                base, _, k = pth.rpartition("+")
                k = int(k, 16)
                parent = by_path[(name, base[:-3])] if k == 0 else by_path[(name, f"{base}+{k - 1:06x}")]
                ents.append(f"{p} {'overflow1' if k == 0 else 'overflow2'} {parent}")
            else:
                ents.append(f"{p} btree {by_path[(name, pth[:-4])]}")
        for i in range(0, len(ents), 6):
            print("  " + " | ".join(ents[i:i + 6]))
    print("-- tables")
    for t, n, tb, root, sql in schema:
        if t != "table":
            continue
        wr = "WITHOUT ROWID" in sql
        rows = q(f"SELECT * FROM {n} ORDER BY 1") if wr else q(f"SELECT rowid, * FROM {n} ORDER BY rowid")
        print(f"{n}: {len(rows)} rows")
        for r in rows:
            if n == "orders" and r[0] % 20 != 0 and r is not rows[-1]:
                continue
            if wr and str(r[0]).startswith("deleted:"):
                continue
            print(f"  {r[0]}: {row(r[1:])}" if not wr else f"  {row(r)}")
        if wr:
            dl = [r for r in rows if str(r[0]).startswith("deleted:")]
            if dl:
                print(f"  {len(dl)} deleted:* keys, values sum to {sum(r[1] for r in dl)}, "
                      f"first {row(dl[0])}, last {row(dl[-1])}")
    print("-- indexes")
    for t, n, tb, root, sql in schema:
        if t != "index":
            continue
        cols = [r[2] for r in q(f"PRAGMA index_info({n})")]
        c = ", ".join(cols)
        ents = q(f"SELECT {c}, rowid FROM {tb} INDEXED BY {n} ORDER BY {c}, rowid")
        print(f"{n} ({c}): {len(ents)} entries")
        for e in ents[:3] + [None] + ents[-3:]:
            print("  ..." if e is None else f"  {row(e)}")
    if lookups:
        print("-- lookups")
        for l in open(lookups).read().split("\n"):
            if not l or l.startswith("#"):
                continue
            cmd, _, arg = l.partition(" ")
            if cmd == "email":
                r = q("SELECT rowid, * FROM customers WHERE email = ?", arg)
                print(f"email {arg!r}: " + (f"{r[0][0]}: {row(r[0][1:])}" if r else "not found"))
            elif cmd == "orders":
                r = q("SELECT id, placed, total_cents FROM orders WHERE customer_id = ? ORDER BY placed, id", int(arg))
                print(f"orders of {arg}: {len(r)}" + "".join(f"\n  {x[0]} {x[1]} {x[2]}" for x in r))
            else:
                t, a, b = arg.split(" ")
                r = q(f"SELECT rowid, * FROM {t} WHERE rowid BETWEEN ? AND ? ORDER BY rowid", int(a), int(b))
                print(f"{t} rows {a} to {b}: {len(r)}")
                for x in r:
                    print(f"  {x[0]}: {row(x[1:])}")
        print("-- orders by country")
        for c, n, s in q("SELECT c.country, count(*), sum(o.total_cents) FROM orders o JOIN customers c "
                         "ON c.id = o.customer_id WHERE o.total_cents BETWEEN -1000000000000 AND 1000000000000 "
                         "GROUP BY c.country ORDER BY c.country"):
            print(f"{c} {n} {s}")


report("data/shop.db", "data/lookups.txt")
report("data/notes16.db", None)
report("data/bad.db", None)
