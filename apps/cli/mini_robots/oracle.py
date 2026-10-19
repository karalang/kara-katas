# Runs data/jobs.jsonl (as mk.py writes it) through Python 3.13's real
# urllib.robotparser and prints what mini_robots.kara prints. Only
# urlopen is replaced, by a fake that serves the sites under data/web/.
import io
import json
import os
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser

W = "data/web"


class Page:
    def __init__(self, data):
        self.data = data

    def read(self):
        return self.data


def lookup(url):
    if not urllib.parse.urlsplit(url).scheme:
        raise ValueError("unknown url type: %r" % url)
    parts = urllib.parse.urlsplit(url)
    host = parts.netloc
    if not os.path.isdir(f"{W}/{host}"):
        raise urllib.error.URLError("[Errno -2] Name or service not known")
    if parts.path == "/robots.txt" and (os.path.exists(f"{W}/{host}/robots.txt") or os.path.exists(f"{W}/{host}/status")):
        if os.path.exists(f"{W}/{host}/status"):
            return int(open(f"{W}/{host}/status").read()), b""
        return 200, open(f"{W}/{host}/robots.txt", "rb").read()
    key = parts.path + ("?" + parts.query if parts.query else "")
    for p in json.load(open(f"{W}/{host}/pages.json")):
        if p["path"] == key:
            return p["status"], p["body"].encode()
    return 404, b"not found\n"


def fake_urlopen(url):
    status, body = lookup(url)
    if status != 200:
        raise urllib.error.HTTPError(url, status, "status %d" % status, {}, io.BytesIO(b""))
    return Page(body)


urllib.request.urlopen = fake_urlopen

parsers = {}


def err(e):
    return f"{type(e).__name__}: {e}"


def show(rp, agents):
    text = str(rp)
    print("  str:")
    for line in text.split("\n"):
        print("    " + line if line else "")
    print(f"  site_maps: {rp.site_maps()!r}")
    print(f"  disallow_all={rp.disallow_all} allow_all={rp.allow_all} read={rp.mtime() != 0}")
    for a in agents:
        try:
            print(f"  {a!r}: delay {rp.crawl_delay(a)!r}, rate {rp.request_rate(a)!r}")
        except Exception as e:
            print(f"  {a!r}: {err(e)}")


def links_of(body):
    out = []
    i = 0
    while True:
        i = body.find('href="', i)
        if i < 0:
            return out
        j = body.find('"', i + 6)
        if j < 0:
            return out
        out.append(body[i + 6:j])
        i = j + 1


def resolve(base, link):
    k = link.find("#")
    if k >= 0:
        link = link[:k]
    if link.startswith("http://") or link.startswith("https://"):
        return link
    if link.startswith("//") or not link.startswith("/"):
        return None
    return base + link


def crawl(agent, start, limit):
    print(f"  crawl as {agent!r}")
    queue = list(start)
    seen = set(queue)
    robots = {}
    clock = {}
    fetched = blocked = failed = 0
    elapsed = 0
    while queue and fetched < limit:
        url = queue.pop(0)
        parts = urllib.parse.urlsplit(url)
        base = f"{parts.scheme}://{parts.netloc}"
        if base not in robots:
            rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
            try:
                rp.read()
                state = "disallow all" if rp.disallow_all else "allow all" if rp.allow_all else f"{len(rp.entries)} groups"
                print(f"  robots {base}: {state}, delay {rp.crawl_delay(agent)!r}, rate {rp.request_rate(agent)!r}, "
                      f"sitemaps {rp.site_maps()!r}")
                robots[base] = rp
            except Exception as e:
                print(f"  robots {base}: {err(e)}")
                robots[base] = None
        rp = robots[base]
        if rp is None:
            print(f"  skip {url}")
            failed += 1
            continue
        if not rp.can_fetch(agent, url):
            print(f"  blocked {url}")
            blocked += 1
            continue
        delay = rp.crawl_delay(agent)
        if base in clock and delay:
            wait = clock[base] + delay - elapsed
            if wait > 0:
                print(f"  wait {wait}s")
                elapsed += wait
        clock[base] = elapsed
        status, body = lookup(url)
        fetched += 1
        if status != 200:
            print(f"  get {url}: {status}")
            continue
        found = []
        for l in links_of(body.decode()):
            u = resolve(base, l)
            if u is not None and u not in seen:
                seen.add(u)
                queue.append(u)
                found.append(u)
        print(f"  get {url}: 200, {len(found)} new links")
    print(f"  {fetched} fetched, {blocked} blocked, {failed} skipped, {len(queue)} left, {elapsed}s waited")


def run(j):
    k = j["kind"]
    if k == "new":
        parsers[j["name"]] = urllib.robotparser.RobotFileParser(j["url"])
    elif k == "load":
        rp = urllib.robotparser.RobotFileParser(j["url"])
        parsers[j["name"]] = rp
        rp.read()
    elif k == "parse":
        rp = urllib.robotparser.RobotFileParser()
        raw = open("data/" + j["file"], "rb").read()
        rp.parse(raw.decode("utf-8", "surrogateescape").splitlines())
        parsers[j["name"]] = rp
    elif k == "show":
        show(parsers[j["name"]], j["agents"])
        return
    elif k == "check":
        rp = parsers[j["name"]]
        for a in j["agents"]:
            row = []
            for u in j["urls"]:
                try:
                    row.append("Y" if rp.can_fetch(a, u) else "n")
                except Exception as e:
                    row.append("!")
                    print(f"  {a!r} {u!r}: {err(e)}")
            print(f"  {a!r}: {''.join(row)}")
        return
    elif k == "crawl":
        crawl(j["agent"], j["start"], j["max"])
        return
    print("  ok")


for line in open("data/jobs.jsonl", encoding="utf-8"):
    line = line.rstrip("\n")
    print("== " + line)
    try:
        run(json.loads(line))
    except Exception as e:
        print("  " + err(e))
