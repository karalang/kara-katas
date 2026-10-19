# Writes data/: the jobs (data/jobs.tsv), the Public Suffix List snapshot
# tldextract ships (data/public_suffix_list.dat), the three report inputs,
# and idna's tables and Python's unicodedata for the characters the
# Punycode labels in the jobs decode to (data/unicode.txt, uts46.txt,
# idnadata.txt), as mini_idna writes them.
import bisect
import json
import os
import random
import shutil
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from idna import idnadata  # noqa: E402
from idna.uts46data import uts46_replacements, uts46_starts, uts46_statuses  # noqa: E402

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data")
random.seed(129)

shutil.copy("tldextract/.tld_set_snapshot", "data/public_suffix_list.dat")

jobs = []
strings = []


def section(name):
    jobs.append("== " + name)


def extract(url, private=None):
    strings.append(url)
    flag = "" if private is None else ("private" if private else "public")
    jobs.append("extract\t%s\t%s" % (url, flag))


def extractor(**kw):
    jobs.append("extractor\t%s" % json.dumps(kw, ensure_ascii=False))


section("urls and hosts")
for u in [
    "http://forums.news.cnn.com/",
    "http://forums.bbc.co.uk/",
    "http://www.worldbank.org.kg/",
    "https://www.google.com:443/search?q=x",
    "google.com",
    "google.notavalidsuffix",
    "http://127.0.0.1:8080/deployed/",
    "http://[2001:db8::1]:8443/path",
    "[::1]",
    "[fe80::1%25eth0]",
    "[not-an-ip]",
    "https://user:pass@sub.example.co.uk:8443/a?b#c",
    "ftp://mirror.kernel.org/pub",
    "//cdn.example.com/lib.js",
    "mailto:someone@example.com",
    "example.com.",
    "EXAMPLE.CO.UK",
    "WWW.Example.COM",
    "a.b.c.d.example.com",
    "localhost",
    "localhost:5000",
    "",
    "   ",
    "http://",
    "http://.example.com",
    "http://example..com",
    "com",
    "co.uk",
    ".co.uk",
    "http://foo.bar.com\\x",
    "s3.amazonaws.com",
    "mybucket.s3.amazonaws.com",
    "ec2-1-2-3-4.compute-1.amazonaws.com",
    "ip-10-0-0-1.us-west-2.compute.amazonaws.com",
    "myapp.herokuapp.com",
    "user.github.io",
    "github.io",
    "www.blogspot.com",
    "someone.blogspot.co.uk",
    "my-site.netlify.app",
    "abc.pages.dev",
    "www.ck",
    "city.kawasaki.jp",
    "foo.city.kawasaki.jp",
    "foo.bar.kawasaki.jp",
    "bar.kawasaki.jp",
    "kawasaki.jp",
    "a.b.example.bd",
    "example.bd",
    "x.school.sch.uk",
    "news.bbc.co.uk",
    "www.parliament.uk",
    "test.k12.ca.us",
    "www.ox.ac.uk",
    "shop.example.com.au",
    "www.city.yokohama.jp",
    "www.example.co.jp",
    "例子.中国",
    "www.例子.公司.cn",
    "www.xn--fiqs8s",
    "www.example.xn--fiqs8s",
    "www.EXAMPLE.XN--FIQS8S",
    "foo.xn--55qx5d.cn",
    "www.xn--bcher-kva.example",
    "www.example.xn--",
    "www.example.xn--zz",
    "www.example.xn--a-ecp.ru",
    "xn--mgbaam7a8h.xn--mgbaam7a8h",
    "bücher.de",
    "www.食狮.公司.cn",
    "www。example。com",
    "www．example．co．uk",
    "www｡example｡org",
    "example.com。",
    "1.2.3.4",
    "1.2.3.4.5",
    "01.2.3.4",
    "256.1.1.1",
    "1.2.3",
    "١.2.3.4",
    "http://1.2.3.4/",
    "http://user@1.2.3.4:80/",
    "1.2.3.com",
    "http://www.example.com#frag",
    "http://www.example.com?q=1",
    "https://www.example.com/path/to/page.html",
    "https:/www.example.com",
    "1http://www.example.com",
    "git+ssh://git@github.com/org/repo.git",
    "a b.example.com",
    " http://example.com ",
    "_dmarc.example.com",
    "-bad-.example.com",
    "xn--.com",
    "uk",
    "jp",
    "zz",
    "www.gov.uk",
    "service.gov.uk",
    "a.service.gov.uk",
]:
    extract(u)

section("private domains per call")
for u in ["user.github.io", "github.io", "www.blogspot.com", "s3.amazonaws.com", "mybucket.s3.amazonaws.com",
          "ip-10-0-0-1.us-west-2.compute.amazonaws.com", "foo.bar.compute.amazonaws.com",
          "abc.pages.dev", "x.on-acorn.io", "on-acorn.io", "y.x.on-acorn.io", "myapp.herokuapp.com",
          "www.example.com", "co.uk"]:
    extract(u, private=True)
    extract(u, private=False)

section("an extractor with private domains on")
extractor(include_psl_private_domains=True)
for u in ["user.github.io", "www.google.com", "a.b.blogspot.com", "s3.amazonaws.com", "foo.city.kawasaki.jp"]:
    extract(u)
extract("user.github.io", private=False)

section("extra suffixes")
extractor(extra_suffixes=["internal", "corp.example.com", "*.svc.cluster.local"])
for u in ["api.internal", "db.prod.internal", "wiki.corp.example.com", "corp.example.com", "www.example.com",
          "web.default.svc.cluster.local", "svc.cluster.local", "x.cluster.local", "internal"]:
    extract(u)
extractor(extra_suffixes=["github.io"], include_psl_private_domains=False)
extract("user.github.io")
extractor()

section("random hosts")
labels = ["www", "api", "mail", "cdn", "shop", "blog", "dev", "a1", "x-y", "static", "img", "m"]
names = ["example", "acme", "contoso", "foo", "my-site", "news", "data", "widgets"]
suffixes = ["com", "co.uk", "org", "com.au", "jp", "co.jp", "github.io", "blogspot.com", "herokuapp.com",
            "kawasaki.jp", "ck", "s3.amazonaws.com", "ac.uk", "gov.uk", "net.br", "xn--fiqs8s", "公司.cn",
            "edu.cn", "museum", "appspot.com", "nom.br", "invalidtld"]
for _ in range(60):
    n = random.randint(0, 3)
    host = ".".join(random.sample(labels, n) + [random.choice(names), random.choice(suffixes)])
    if random.random() < 0.2:
        host = host.upper()
    scheme = random.choice(["", "http://", "https://", "//"])
    port = random.choice(["", "", ":8080"])
    path = random.choice(["", "/", "/a/b?c=d", "#top"])
    extract(scheme + host + port + path, private=random.choice([None, True, False]))

section("the tldextract command")
for args in [["forums.bbc.co.uk"], ["-j", "http://user.github.io/x", "例子.中国"], ["-p", "user.github.io"],
             ["--private_domains", "--json", "s3.amazonaws.com"], ["--include_psl_private_domains", "a.b.c"],
             ["[::1]", "127.0.0.1"], ["-j", "[2001:db8::1]", "1.2.3.4"], []]:
    strings.extend(args)
    jobs.append("cli\t%s" % json.dumps(args, ensure_ascii=False))

section("suffix list")
jobs.append("tlds")

# ------------------------------------------------------------ the reports

refs = ["-", "https://www.google.com/search?q=widgets", "https://www.google.co.uk/", "https://news.ycombinator.com/item?id=1",
        "https://alice.github.io/blog/post", "https://bob.github.io/", "https://t.co/abc", "https://www.reddit.com/r/x",
        "https://old.reddit.com/r/y", "http://someblog.blogspot.com/2024/01/", "https://other.blogspot.com/",
        "https://mail.yahoo.co.jp/", "https://search.yahoo.co.jp/", "https://duckduckgo.com/", "https://例子.中国/",
        "https://www.xn--fiqs8s/", "http://192.168.1.10:8000/admin", "https://[2001:db8::7]/", "android-app://com.slack",
        "https://l.facebook.com/l.php", "https://m.facebook.com/", "https://www.bing.com/search", "https://myapp.herokuapp.com/",
        "https://docs.python.org/3/", "https://pypi.org/project/x/"]
pages = ["/", "/pricing", "/docs/start", "/blog/launch", "/signup"]
with open("data/access.log", "w") as f:
    f.write("# combined log format, the referer is the second quoted field\n")
    for i in range(120):
        ip = "%d.%d.%d.%d" % (random.randint(1, 223), random.randint(0, 255), random.randint(0, 255), random.randint(1, 254))
        ref = random.choice(refs)
        strings.append(ref)
        f.write('%s - - [19/Oct/2026:%02d:%02d:%02d +0000] "GET %s HTTP/1.1" 200 %d "%s" "Mozilla/5.0"\n'
                % (ip, 8 + i // 30, (i * 7) % 60, (i * 13) % 60, random.choice(pages), random.randint(200, 9000), ref))
section("referrers in an access log")
jobs.append("referrers\taccess.log")

cookies = [
    ("www.example.com", "example.com"), ("www.example.com", ".example.com"), ("www.example.com", "www.example.com"),
    ("www.example.com", "com"), ("www.example.co.uk", "co.uk"), ("www.example.co.uk", "example.co.uk"),
    ("alice.github.io", "github.io"), ("alice.github.io", "alice.github.io"), ("bob.github.io", "alice.github.io"),
    ("shop.example.com", "other.com"), ("shop.example.com", "ample.com"), ("a.b.example.com", "b.example.com"),
    ("foo.city.kawasaki.jp", "city.kawasaki.jp"), ("foo.bar.kawasaki.jp", "bar.kawasaki.jp"),
    ("x.y.bar.kawasaki.jp", "y.bar.kawasaki.jp"), ("app.herokuapp.com", "herokuapp.com"),
    ("www.EXAMPLE.com", "Example.COM"), ("1.2.3.4", "1.2.3.4"), ("1.2.3.4", "2.3.4"), ("localhost", "localhost"),
    ("www.例子.中国", "例子.中国"), ("www.例子.中国", "中国"), ("www.xn--fiqs8s", "xn--fiqs8s"),
    ("bucket.s3.amazonaws.com", "s3.amazonaws.com"), ("a.www.ck", "www.ck"), ("a.foo.ck", "foo.ck"),
]
with open("data/cookies.tsv", "w") as f:
    f.write("# request host, Domain attribute of its Set-Cookie\n")
    for h, d in cookies:
        strings.extend([h, d])
        f.write("%s\t%s\n" % (h, d))
section("cookie domains")
jobs.append("cookies\tcookies.tsv")

pairs = [
    ("https://www.example.com/", "https://api.example.com/v1"), ("https://alice.github.io/", "https://bob.github.io/"),
    ("https://example.co.uk/", "https://example.com/"), ("https://a.example.co.uk", "http://b.example.co.uk:8080"),
    ("https://foo.blogspot.com", "https://bar.blogspot.com"), ("https://news.bbc.co.uk", "https://www.bbc.com"),
    ("http://1.2.3.4/", "http://1.2.3.4:81/"), ("https://localhost", "https://localhost:3000"),
    ("https://例子.中国/", "https://www.xn--fsqu00a.xn--fiqs8s/"), ("https://a.foo.ck", "https://b.foo.ck"),
    ("https://www.ck", "https://a.www.ck"), ("https://mail.google.com", "https://accounts.google.com"),
]
with open("data/samesite.tsv", "w") as f:
    f.write("# two URLs\n")
    for a, b in pairs:
        strings.extend([a, b])
        f.write("%s\t%s\n" % (a, b))
section("same site")
jobs.append("samesite\tsamesite.tsv")

with open("data/jobs.tsv", "w") as f:
    f.write("\n".join(jobs) + "\n")

# ------------------------------------------------------------ the tables, as mini_idna writes them


def row(cp):
    return cp if cp < 256 else bisect.bisect_right(uts46_starts, cp) - 1


covered = set(range(0x80))


def punycode_chars(s):
    out = set()
    for label in s.replace("。", ".").replace("．", ".").replace("｡", ".").split("."):
        b = label.lower()
        if b.startswith("xn--") and b.isascii():
            try:
                out.update(ord(c) for c in b[4:].encode().decode("punycode"))
            except Exception:
                pass
    return out


for s in strings:
    covered |= punycode_chars(s)


def decomp(cp):
    d = unicodedata.decomposition(chr(cp))
    if not d or d.startswith("<"):
        return []
    return [int(x, 16) for x in d.split()]


composites = {}
for cp in range(0x110000):
    if 0xD800 <= cp < 0xE000:
        continue
    d = decomp(cp)
    if len(d) == 2 and unicodedata.normalize("NFC", chr(cp)) == chr(cp):
        composites.setdefault(d[0], []).append((d[1], cp))
for li in range(19):
    for vi in range(21):
        lv = 0xAC00 + (li * 21 + vi) * 28
        composites.setdefault(0x1100 + li, []).append((0x1161 + vi, lv))
        for ti in range(1, 28):
            composites.setdefault(lv, []).append((0x11A7 + ti, lv + ti))

while True:
    more = set()
    for cp in covered:
        if 0xD800 <= cp < 0xE000:
            continue
        rep = uts46_replacements[row(cp)]
        if rep:
            more.update(ord(c) for c in rep)
        more.update(decomp(cp))
        for second, comp in composites.get(cp, []):
            if second in covered:
                more.add(comp)
    more -= covered
    if not more:
        break
    covered |= more

with open("data/unicode.txt", "w") as f:
    f.write("# cp;ccc;canonical decomposition;flags (p not printable, n no name, c primary composite);bidi;category\n")
    for cp in sorted(covered):
        ch = chr(cp)
        if 0xD800 <= cp < 0xE000:
            f.write("%x;0;;pn;%s;%s\n" % (cp, unicodedata.bidirectional(ch), unicodedata.category(ch)))
            continue
        d = decomp(cp)
        flags = ("p" if not ch.isprintable() else "") + ("n" if not unicodedata.name(ch, "") else "")
        if len(d) == 2 and unicodedata.normalize("NFC", ch) == ch:
            flags += "c"
        f.write("%x;%d;%s;%s;%s;%s\n" % (cp, unicodedata.combining(ch), " ".join("%x" % x for x in d), flags,
                                         unicodedata.bidirectional(ch), unicodedata.category(ch)))

rows = sorted({row(cp) for cp in covered})
with open("data/uts46.txt", "w") as f:
    f.write("# start;status;replacement\n")
    for i in rows:
        rep = uts46_replacements[i]
        f.write("%x;%s;%s\n" % (uts46_starts[i], chr(uts46_statuses[i]),
                                " ".join("%x" % ord(c) for c in rep) if rep else ""))


def ranges(name, rs):
    return ["%s %x %x" % (name, r >> 32, r & 0xFFFFFFFF) for r in rs]


with open("data/idnadata.txt", "w") as f:
    f.write("# set start end (end exclusive)\n")
    for k, v in idnadata.codepoint_classes.items():
        f.write("\n".join(ranges(k, v)) + "\n")
    for k, v in idnadata.scripts.items():
        f.write("\n".join(ranges("script:" + k, v)) + "\n")
    for k, v in idnadata.joining_types.items():
        f.write("\n".join(ranges("joining:" + k, v)) + "\n")

print(len(jobs), "jobs,", len(covered), "characters,", len(rows), "UTS #46 rows")
