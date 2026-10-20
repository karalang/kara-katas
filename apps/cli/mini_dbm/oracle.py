# Runs data/jobs.tsv through Python 3.13's own dbm.dumb and dbm.whichdb
# and prints what expected.out holds. Run it from the app directory,
# after mk.py.
import os
import shutil
import dbm
import dbm.dumb as dumb

BASE = "data/db/"
ALPHA = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def unesc(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            if s[i + 1] == "\\":
                out.append("\\")
                i += 2
                continue
            if s[i + 1] == "x":
                out.append(chr(int(s[i + 2:i + 4], 16)))
                i += 4
                continue
            if s[i + 1] == "n":
                out.append("\n")
                i += 2
                continue
        out.append(s[i])
        i += 1
    return "".join(out)


def arg(t):
    # b:... bytes (each character one byte), i:... an int, r:c:n a str of
    # n copies of c, anything else a str
    if t.startswith("b:"):
        return unesc(t[2:]).encode("latin-1")
    if t.startswith("i:"):
        return int(t[2:])
    if t.startswith("r:"):
        _, c, n = t.split(":")
        return c * int(n)
    return unesc(t)


def show(v):
    if isinstance(v, (bytes, bytearray)) and len(v) > 40:
        return f"<{len(v)} bytes: {bytes(v[:12])!r}...>"
    if isinstance(v, str) and len(v) > 40:
        return f"<{len(v)} chars: {v[:12]!r}...>"
    return repr(v)


def err(e):
    return f"{type(e).__name__}: {e}"


def files(name):
    p = BASE + name
    out = []
    try:
        with open(p + ".dir", "rb") as f:
            lines = f.read().decode("latin-1").split("\n")[:-1]
        out.append(f"  {name}.dir: {len(lines)} lines")
        for l in lines:
            out.append(f"    {l}")
    except OSError:
        out.append(f"  {name}.dir: missing")
    try:
        out.append(f"  {name}.dat: {os.path.getsize(p + '.dat')} bytes")
    except OSError:
        out.append(f"  {name}.dat: missing")
    try:
        with open(p + ".bak", "rb") as f:
            n = len(f.read().decode("latin-1").split("\n")) - 1
        out.append(f"  {name}.bak: {n} lines")
    except OSError:
        out.append(f"  {name}.bak: missing")
    return out


def run_job(name, lines):
    print(f"== {name}")
    db = None
    for line in lines:
        f = line.split("\t")
        op = f[0]
        try:
            if op == "open":
                print(f"open({f[1]!r}, {f[2]!r})", end="")
                db = dumb.open(BASE + f[1], f[2])
                print()
            elif op == "set":
                k, v = arg(f[1]), arg(f[2])
                print(f"db[{show(k)}] = {show(v)}", end="")
                db[k] = v
                print()
            elif op == "get":
                k = arg(f[1])
                print(f"db[{show(k)}]", end="")
                r = db[k]
                print(f" = {show(r)}")
            elif op == "del":
                k = arg(f[1])
                print(f"del db[{show(k)}]", end="")
                del db[k]
                print()
            elif op == "has":
                k = arg(f[1])
                print(f"{show(k)} in db", end="")
                r = k in db
                print(f" = {r}")
            elif op == "len":
                print("len(db)", end="")
                r = len(db)
                print(f" = {r}")
            elif op == "keys":
                print("db.keys()", end="")
                r = db.keys()
                print(f" = [{', '.join(show(k) for k in r)}]")
            elif op == "items":
                print("db.items()", end="")
                r = db.items()
                print(f" = [{', '.join(f'({show(k)}, {show(v)})' for k, v in r)}]")
            elif op == "sync":
                print("db.sync()", end="")
                db.sync()
                print()
            elif op == "close":
                print("db.close()", end="")
                db.close()
                print()
            elif op == "files":
                print(f"files {f[1]}:")
                for l in files(f[1]):
                    print(l)
            else:
                raise SystemExit("bad op " + op)
        except Exception as e:
            print(f" -> {err(e)}")


# ------------------------------------------------------------ programs

def stats(name):
    db = dumb.open(BASE + name, "r")
    live = sum(siz for pos, siz in db._index.values())
    n = len(db)
    db.close()
    size = os.path.getsize(BASE + name + ".dat")
    return f"{n} keys, {live} live bytes in a {size}-byte .dat ({size - live} padding or dead)"


def base62(n):
    s = ""
    while True:
        s = ALPHA[n % 62] + s
        n //= 62
        if n == 0:
            return s


def data_lines(path):
    with open("data/" + path, encoding="utf-8") as f:
        return [l for l in f.read().split("\n") if l.strip() and not l.startswith("#")]


def prog_shortener():
    print("== program: URL shortener")
    db = dumb.open(BASE + "short", "n")
    db["next"] = "1"
    for url in data_lines("shortener/urls.txt"):
        k = "url:" + url
        if k in db:
            print(f"  {db[k].decode()} <- {url} (already short)")
            continue
        n = int(db["next"])
        code = base62(n)
        db["code:" + code] = url
        db[k] = code
        db["next"] = str(n + 1)
        print(f"  {code} <- {url}")
    db.close()
    print("restarted")
    db = dumb.open(BASE + "short", "c")
    for c in data_lines("shortener/visits.txt"):
        k = "code:" + c
        if k not in db:
            print(f"  /{c}: 404")
            continue
        h = "hits:" + c
        hits = int(db[h]) + 1 if h in db else 1
        db[h] = str(hits)
        print(f"  /{c}: 301 {db[k].decode()}")
    codes = sorted(k.decode()[5:] for k in db.keys() if k.startswith(b"code:"))
    for c in codes:
        h = "hits:" + c
        hits = int(db[h]) if h in db else 0
        print(f"  {c} {hits} {show(db['code:' + c].decode())}")
    db.close()
    print(f"  {stats('short')}")


def prog_sessions():
    print("== program: session store")
    db = dumb.open(BASE + "sessions", "n")
    for l in data_lines("sessions/events.txt"):
        w = l.split()
        t = int(w[0])
        if w[1] == "login":
            db[w[2]] = f"{w[3]}|{t + 600}"
            print(f"  {t} login {w[2]} {w[3]}, expires {t + 600}")
        elif w[1] == "touch":
            if w[2] in db:
                user = db[w[2]].decode().split("|")[0]
                db[w[2]] = f"{user}|{t + 600}"
                print(f"  {t} touch {w[2]}, expires {t + 600}")
            else:
                print(f"  {t} touch {w[2]}: no such session")
        elif w[1] == "logout":
            del db[w[2]]
            print(f"  {t} logout {w[2]}")
        elif w[1] == "sweep":
            gone = []
            for k in db.keys():
                if int(db[k].decode().split("|")[1]) <= t:
                    del db[k]
                    gone.append(k.decode())
            print(f"  {t} sweep: removed {gone}, {len(db)} left")
    print(f"  left: {[(k.decode(), db[k].decode()) for k in db.keys()]}")
    db.close()
    for l in files("sessions"):
        print(l)
    print(f"  {stats('sessions')}")


def body(url, i, n):
    b = f"{url}#{i}".encode()
    return b + b"." * (n - len(b))


def prog_httpcache():
    print("== program: HTTP response cache")
    db = dumb.open(BASE + "httpcache", "n")
    for l in data_lines("httpcache/responses.txt"):
        w = l.split()
        url = w[0]
        for i, n in enumerate(w[1:]):
            n = int(n)
            before = db._index.get(url.encode())
            db[url] = body(url, i, n)
            pos, siz = db._index[url.encode()]
            how = "new" if before is None else ("in place" if before[0] == pos else "moved")
            print(f"  {url} fetch {i + 1}: {siz} bytes at {pos} ({how})")
    db.close()
    print(f"  before compaction: {stats('httpcache')}")
    src = dumb.open(BASE + "httpcache", "r")
    dst = dumb.open(BASE + "httpcache-compact", "n")
    for k in src.keys():
        dst[k] = src[k]
    src.close()
    dst.close()
    print(f"  after compaction: {stats('httpcache-compact')}")
    a = dumb.open(BASE + "httpcache", "r")
    b = dumb.open(BASE + "httpcache-compact", "r")
    same = all(a[k] == b[k] for k in a.keys()) and len(a) == len(b)
    a.close()
    b.close()
    print(f"  same contents: {same}")


def snapshot(name, copy):
    for ext in (".dir", ".dat", ".bak"):
        if os.path.exists(BASE + name + ext):
            shutil.copyfile(BASE + name + ext, BASE + copy + ext)


def prog_crash():
    print("== program: a crash between updates")
    db = dumb.open(BASE + "crash", "n")
    db["a"] = "x" * 100
    db["b"] = "y" * 600
    db.close()
    db = dumb.open(BASE + "crash", "c")
    db["a"] = "X" * 400
    db["b"] = "Y" * 1100
    db["c"] = "new"
    snapshot("crash", "crash-snap")
    db.close()
    for l in files("crash-snap"):
        print(l)
    for l in files("crash"):
        print(l)
    for name in ("crash-snap", "crash"):
        db = dumb.open(BASE + name, "r")
        print(f"  {name}: {', '.join(f'{k.decode()}={show(db[k])}' for k in db.keys())}")
        db.close()


def prog_fsck():
    print("== program: index checker")
    for name in ("notes", "cache", "handmade", "damaged", "httpcache", "crash-snap"):
        db = dumb.open(BASE + name, "r")
        index = dict(db._index)
        db.close()
        size = os.path.getsize(BASE + name + ".dat")
        problems = []
        for k, (pos, siz) in index.items():
            if pos % 512 != 0:
                problems.append(f"{k.decode('latin-1')!r} starts at {pos}, not on a 512-byte block")
            if pos + siz > size:
                problems.append(f"{k.decode('latin-1')!r} ends at {pos + siz}, past the end ({size})")
        order = sorted(index.items(), key=lambda kv: (kv[1][0], kv[0]))
        end = 0
        last = None
        for k, (pos, siz) in order:
            if siz == 0:
                continue
            if last is not None and pos < end:
                problems.append(f"{k.decode('latin-1')!r} overlaps {last.decode('latin-1')!r}")
            if pos + siz > end:
                end = pos + siz
                last = k
        live = sum(siz for pos, siz in index.values())
        verdict = "clean" if not problems else f"{len(problems)} problems"
        print(f"  {name}: {len(index)} entries, {live} live bytes, .dat {size} bytes: {verdict}")
        for p in problems:
            print(f"    {p}")


PROGRAMS = {"shortener": prog_shortener, "sessions": prog_sessions,
            "httpcache": prog_httpcache, "crash": prog_crash, "fsck": prog_fsck}


def main():
    jobs = open("data/jobs.tsv", encoding="utf-8").read().split("\n")[:-1]
    i = 0
    while i < len(jobs):
        f = jobs[i].split("\t")
        if f[0] == "job":
            body_ = []
            i += 1
            while i < len(jobs) and jobs[i].split("\t")[0] not in ("job", "whichdb", "program"):
                body_.append(jobs[i])
                i += 1
            run_job(f[1], body_)
            continue
        if f[0] == "whichdb":
            print(f"whichdb({f[1]!r}) = {dbm.whichdb('data/' + f[1])!r}")
        elif f[0] == "program":
            PROGRAMS[f[1]]()
        i += 1


main()
