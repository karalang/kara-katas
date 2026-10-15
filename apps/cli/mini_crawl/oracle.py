# The oracle: the same crawler written with Python's html.parser,
# urllib.parse and urllib.robotparser. Run from this directory after
# mk.py; it prints expected.out and writes data/out/ as the Kara
# program does.
import os, re, sys
from html.parser import HTMLParser
from urllib.parse import (urljoin, urlsplit, urlunsplit, urldefrag, quote,
                          quote_plus, unquote, unquote_plus, parse_qsl,
                          urlencode)
from urllib.robotparser import RobotFileParser

def esc(s):
    if s is None:
        return "None"
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t")
    return '"' + s.replace("\n", "\\n").replace("\r", "\\r") + '"'

def unesc(a):
    out, i = [], 0
    while i < len(a):
        if a[i] == "\\" and i + 1 < len(a):
            out.append({"t": "\t", "n": "\n"}.get(a[i + 1], a[i + 1]))
            i += 2
        else:
            out.append(a[i])
            i += 1
    return "".join(out)

# ---------------------------------------------------------------- URL library
print("== URL library")
for line in open("data/url-tests.tsv", encoding="utf-8").read().split("\n")[:-1]:
    op, *args = [unesc(a) for a in line.split("\t")]
    if op == "join":
        print(f"urljoin({esc(args[0])}, {esc(args[1])}) = {esc(urljoin(args[0], args[1]))}")
    elif op == "split":
        p = urlsplit(args[0])
        print(f"urlsplit({esc(args[0])})")
        print(f"  scheme={esc(p.scheme)} netloc={esc(p.netloc)} path={esc(p.path)} query={esc(p.query)} fragment={esc(p.fragment)}")
        try:
            port = p.port
            port = "None" if port is None else str(port)
        except ValueError as e:
            port = f"ValueError({esc(str(e))})"
        print(f"  username={esc(p.username)} password={esc(p.password)} hostname={esc(p.hostname)} port={port}")
        print(f"  unsplit={esc(urlunsplit(p))}")
    elif op == "quote":
        print(f"quote({esc(args[0])}, safe={esc(args[1])}) = {esc(quote(args[0], safe=args[1]))}")
    elif op == "quote_plus":
        print(f"quote_plus({esc(args[0])}) = {esc(quote_plus(args[0]))}")
    elif op == "unquote":
        print(f"unquote({esc(args[0])}) = {esc(unquote(args[0]))}")
    elif op == "unquote_plus":
        print(f"unquote_plus({esc(args[0])}) = {esc(unquote_plus(args[0]))}")
    elif op == "qsl":
        pairs = parse_qsl(args[0], keep_blank_values=True)
        shown = ", ".join(f"({esc(k)}, {esc(v)})" for k, v in pairs)
        print(f"parse_qsl({esc(args[0])}) = [{shown}]")
    elif op == "encode":
        pairs = list(zip(args[0::2], args[1::2]))
        print(f"urlencode({len(pairs)} pairs) = {esc(urlencode(pairs))}")

# ---------------------------------------------------------------- robots.txt
SITE = "https://docs.example.com"
AGENT = "kara-crawler/1.0"
robots_text = open("data/site/robots.txt", encoding="utf-8").read()
rp = RobotFileParser(SITE + "/robots.txt")
rp.parse(robots_text.splitlines())
print()
print("== robots.txt")
print("sitemaps: " + ", ".join(rp.site_maps() or []))
agents = [AGENT, "Googlebot/2.1", "BadBot/3.0", "friendly-bot"]
probes = ["/", "/drafts/x.html", "/drafts/public-roadmap.html",
          "/internal/admin.html", "/internal/status.html",
          "/guide/setup.html?print=1", "/guide/setup.html?lang=en&print=",
          "/tmp", "/tmpfiles/x", "/old/page.html", "/docs.pdf",
          "/docs.pdf?x=1", "/search?q=1", "/search/help", "/robots.txt",
          "/%7Euser/", "/~user/x", "/archive/2024/old", "/archive/2024/old/x",
          "/caf%C3%A9.html", "/a$b"]
for a in agents:
    rate = rp.request_rate(a)
    rate = "None" if rate is None else f"{rate.requests}/{rate.seconds}"
    verdicts = "".join("+" if rp.can_fetch(a, SITE + p) else "-" for p in probes)
    print(f"{a}: crawl-delay={rp.crawl_delay(a)} request-rate={rate} {verdicts}")
print("probes: " + " ".join(probes))

# ---------------------------------------------------------------- the crawl
DEFAULT_PORT = {"http": 80, "https": 443}
URL_ATTRS = {"a": "href", "link": "href", "img": "src", "script": "src",
             "iframe": "src", "source": "src"}
MAX_DEPTH = 3
WS = " \t\n\r\f"

def normalize(url):
    url = urldefrag(url)[0]
    p = urlsplit(url)
    if p.scheme not in ("http", "https"):
        return None, "not http: " + (p.scheme or "no scheme")
    host = p.hostname or ""
    try:
        port = p.port
    except ValueError as e:
        return None, "bad port: " + str(e)
    netloc = host if port in (None, DEFAULT_PORT[p.scheme]) else f"{host}:{port}"
    path = quote(unquote(p.path), safe="/:@!$&'()*+,;=") or "/"
    pairs = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
             if not k.startswith("utm_")]
    return urlunsplit((p.scheme, netloc, path, urlencode(pairs), "")), None

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.base = None
        self.canonical = None
        self.robots = set()
        self.title = None
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        first = {}
        for k, v in attrs:
            first.setdefault(k, v)
        if tag == "title" and self.title is None:
            self.in_title = True
            self.title = ""
        elif tag == "base" and self.base is None and first.get("href") is not None:
            self.base = first["href"]
        elif tag == "meta" and (first.get("name") or "").lower() == "robots":
            for tok in (first.get("content") or "").split(","):
                self.robots.add(tok.strip(WS).lower())
        if tag == "link" and "canonical" in (first.get("rel") or "").lower().split():
            self.canonical = first.get("href")
        if tag in URL_ATTRS and URL_ATTRS[tag] in first:
            rel = (first.get("rel") or "").lower().split()
            self.links.append((tag, first[URL_ATTRS[tag]], "nofollow" in rel))
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title += data

def fetch(url):
    """(status, body or None, location) for a normalized URL."""
    path = unquote(urlsplit(url).path)
    file = "data/site" + path + ("index.html" if path.endswith("/") else "")
    try:
        return 200, open(file, "rb").read(), None
    except (FileNotFoundError, IsADirectoryError):
        pass
    if not path.endswith("/") and os.path.isfile("data/site" + path + "/index.html"):
        p = urlsplit(url)
        return 301, None, urlunsplit((p.scheme, p.netloc, p.path + "/", p.query, ""))
    return 404, None, None

print()
print("== crawl")
start, _ = normalize(SITE + "/")
site_netloc = urlsplit(start).netloc
queue = [(start, 0, "(start)")]
seen = {start}
results = []  # (url, status, note)
referrers = {}
externals = {}
blocked = []
sitemap = []
while queue:
    url, depth, ref = queue.pop(0)
    if not rp.can_fetch(AGENT, url):
        print(f"[robots] {url} (from {ref})")
        blocked.append(url)
        continue
    status, body, location = fetch(url)
    if status == 301:
        print(f"[301] {url} -> {location}")
        if location not in seen:
            seen.add(location)
            queue.append((location, depth, url))
        continue
    if status == 404:
        print(f"[404] {url} (from {ref})")
        results.append((url, 404))
        continue
    if not url.endswith("/") and not url.split("?")[0].endswith(".html"):
        print(f"[200] {url} asset, {len(body)} bytes")
        results.append((url, 200))
        continue
    page = Page()
    page.feed(body.decode("utf-8"))
    page.close()
    title = re.sub(r"[ \t\n\r\f]+", " ", page.title or "").strip(WS)
    flags = sorted(t for t in page.robots if t)
    print(f"[200] {url} depth {depth} {esc(title)}" + (f" robots={','.join(flags)}" if flags else ""))
    results.append((url, 200))
    base = urljoin(url, page.base.strip(WS)) if page.base is not None else url
    if page.base is not None:
        print(f"  base {base}")
    if "noindex" not in page.robots and "none" not in page.robots:
        canon = url
        if page.canonical is not None:
            c, _ = normalize(urljoin(base, page.canonical.strip(WS)))
            if c is not None and urlsplit(c).netloc == site_netloc:
                canon = c
                print(f"  canonical {c}")
        if canon not in sitemap:
            sitemap.append(canon)
    nofollow_page = "nofollow" in page.robots or "none" in page.robots
    for tag, raw, nofollow in page.links:
        if raw is None:
            print(f"  {tag} (no value)")
            continue
        target, why = normalize(urljoin(base, raw.strip(WS)))
        head = f"  {tag} {esc(raw)}"
        if target is None:
            print(f"{head} skipped, {why}")
            continue
        if urlsplit(target).netloc != site_netloc:
            host = urlsplit(target).hostname
            externals[host] = externals.get(host, 0) + 1
            print(f"{head} -> {target} external")
            continue
        referrers.setdefault(target, [])
        if url not in referrers[target]:
            referrers[target].append(url)
        if nofollow or nofollow_page:
            print(f"{head} -> {target} nofollow")
        elif target in seen:
            print(f"{head} -> {target} seen")
        elif depth + 1 > MAX_DEPTH:
            print(f"{head} -> {target} too deep")
        else:
            seen.add(target)
            queue.append((target, depth + 1, url))
            print(f"{head} -> {target} queued")

print()
print("== summary")
ok = sum(1 for _, s in results if s == 200)
print(f"fetched {len(results)} urls: {ok} ok, {len(results) - ok} broken; {len(blocked)} blocked by robots.txt")
for url, s in results:
    if s == 404:
        print(f"broken {url} <- " + ", ".join(referrers.get(url, ["(start)"])))
for host in sorted(externals):
    print(f"external {host} x{externals[host]}")

def xml_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

os.makedirs("data/out", exist_ok=True)
xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sorted(sitemap):
    xml.append(f"  <url><loc>{xml_escape(u)}</loc></url>")
xml.append("</urlset>")
open("data/out/sitemap.xml", "w", encoding="utf-8").write("\n".join(xml) + "\n")
report = ["url\tstatus"] + [f"{u}\t{s}" for u, s in sorted(results)]
open("data/out/report.tsv", "w", encoding="utf-8").write("\n".join(report) + "\n")
print()
print("== data/out/sitemap.xml")
sys.stdout.write(open("data/out/sitemap.xml", encoding="utf-8").read())
