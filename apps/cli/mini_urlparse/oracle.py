# The reference: the same report, made with Python 3.13's urllib.parse.
import os
from urllib.parse import (urlsplit, urlparse, urlunsplit, urljoin, urldefrag,
                          quote, quote_plus, unquote, unquote_plus, parse_qsl,
                          parse_qs, urlencode)


def unescape(line):
    out = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            n = line[i + 1]
            if n == "t":
                out.append("\t"); i += 2; continue
            if n == "n":
                out.append("\n"); i += 2; continue
            if n == "r":
                out.append("\r"); i += 2; continue
            if n == "\\":
                out.append("\\"); i += 2; continue
            if n == "x":
                out.append(chr(int(line[i + 2:i + 4], 16))); i += 4; continue
        out.append(c)
        i += 1
    return "".join(out)


def lines(path):
    return open(path, encoding="utf-8").read().splitlines()


def err(e):
    return f"Error: {type(e).__name__}: {e}"


def show_split():
    print("== split")
    for raw in lines("data/urls.txt"):
        url = unescape(raw)
        print(repr(url))
        try:
            s = urlsplit(url)
        except ValueError as e:
            print("  " + err(e))
            continue
        print(f"  split {s!r}")
        print(f"  parse {urlparse(url)!r}")
        try:
            port = repr(s.port)
        except ValueError as e:
            port = err(e)
        print(f"  username={s.username!r} password={s.password!r} hostname={s.hostname!r} port={port}")
        print(f"  unsplit {urlunsplit(s)!r}")
        print(f"  defrag {urldefrag(url)!r}")


def show_join():
    print("== join")
    base = ""
    for line in lines("data/joins.txt"):
        if line == "base" or line.startswith("base "):
            base = line[5:]
            print(f"-- base {base!r}")
            continue
        rel = "" if line == "<empty>" else line
        print(f"  {rel!r} -> {urljoin(base, rel)!r}")


def show_quote():
    print("== quote")
    for t in lines("data/quotes.txt"):
        print(repr(t))
        print(f"  quote {quote(t)!r}")
        print(f"  quote safe='' {quote(t, safe='')!r}")
        print(f"  quote_plus {quote_plus(t)!r}")
        print(f"  unquote {unquote(t)!r}")
        print(f"  unquote_plus {unquote_plus(t)!r}")


def show_query():
    print("== query")
    for line in lines("data/queries.txt"):
        q = "" if line == "<empty>" else line
        print(repr(q))
        print(f"  qsl {parse_qsl(q)!r}")
        kept = parse_qsl(q, keep_blank_values=True)
        print(f"  qsl blank {kept!r}")
        try:
            print(f"  qsl strict {parse_qsl(q, keep_blank_values=True, strict_parsing=True)!r}")
        except ValueError as e:
            print("  qsl strict " + err(e))
        print(f"  qsl ';' {parse_qsl(q, separator=';')!r}")
        d = parse_qs(q, keep_blank_values=True)
        print(f"  qs {d!r}")
        print(f"  encode {urlencode(kept)!r}")
        print(f"  encode doseq {urlencode(d, doseq=True)!r}")
        print(f"  encode quote {urlencode(kept, safe='/', quote_via=quote)!r}")


SITE = "https://shop.example.com/"
DEFAULT_PORTS = {"http": 80, "https": 443}


def canonical(url):
    s = urlsplit(url)
    host = s.hostname or ""
    if ":" in host:
        host = "[" + host + "]"
    port = s.port
    netloc = host if port is None or DEFAULT_PORTS.get(s.scheme) == port else f"{host}:{port}"
    path = quote(unquote(s.path), safe="/") or "/"
    pairs = sorted(parse_qsl(s.query, keep_blank_values=True), key=lambda kv: kv[0])
    return urlunsplit((s.scheme, netloc, path, urlencode(pairs), ""))


def parse_log_line(line):
    q = line.split('"')
    head = q[0].split()
    request = q[1].split(" ")
    tail = q[2].split()
    return {"ip": head[0], "user": head[2], "method": request[0], "target": request[1],
            "status": int(tail[0]), "referer": q[3]}


def bump(d, k):
    d[k] = d.get(k, 0) + 1


def show_report():
    print("== report")
    pages, hosts, terms, params = {}, {}, {}, {}
    out = []
    for line in lines("data/access.log"):
        r = parse_log_line(line)
        url = urljoin(SITE, r["target"])
        s = urlsplit(url)
        where = "site" if s.netloc == "shop.example.com" else "OFFSITE"
        c = canonical(url)
        print(f"{r['ip']} {r['method']} {r['status']} {where} {c}")
        if where == "site" and r["status"] < 400:
            bump(pages, urlsplit(c).path)
        for k, v in parse_qsl(s.query, keep_blank_values=True):
            bump(params, k)
            if k == "q" and s.path == "/search":
                bump(terms, v)
        ref = r["referer"]
        if ref == "-":
            continue
        try:
            rs = urlsplit(ref)
            rc = canonical(ref)
        except ValueError as e:
            print(f"  referer {ref!r}: {err(e)}")
            continue
        print(f"  referer {rc}")
        rh = rs.hostname
        if rh.startswith("www."):
            rh = rh[4:]
        bump(hosts, rh)
        if rh in ("google.com", "bing.com"):
            for k, v in parse_qsl(rs.query):
                if k == "q":
                    bump(terms, v)
    os.makedirs("data/out", exist_ok=True)
    rows = sorted(pages.items(), key=lambda kv: (-kv[1], kv[0]))
    with open("data/out/pages.txt", "w") as f:
        for p, n in rows:
            f.write(f"{n} {urljoin(SITE, quote(p, safe='/'))}\n")
    with open("data/out/terms.txt", "w") as f:
        for t, n in sorted(terms.items(), key=lambda kv: (-kv[1], kv[0])):
            f.write(urlencode([("q", t), ("n", n)]) + "\n")
    for name in ["pages.txt", "terms.txt"]:
        print(f"-- data/out/{name}")
        for line in lines(f"data/out/{name}"):
            print(line)
    print("-- referers")
    for h, n in sorted(hosts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{n} {h}")
    print("-- params")
    for k, n in sorted(params.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{n} {k!r}")
    print("-- terms read back")
    for line in lines("data/out/terms.txt"):
        d = dict(parse_qsl(line))
        print(f"{d['n']} {d['q']!r}")


show_split()
show_join()
show_quote()
show_query()
show_report()
