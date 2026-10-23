"""Write data/: the furl jobs (one JSON array per line) and the inputs of
the three programs.

Run: python3 -s -P -B mk.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")
os.makedirs(D, exist_ok=True)

D_ = ["dict"]

JOBS = []


def section(title):
    JOBS.append("# " + title)


def job(*parts):
    JOBS.append(json.dumps(list(parts), ensure_ascii=False))


def prog(line):
    JOBS.append("!" + line)


section("parsing: every component, then asdict")
for u in [
    "http://user:pass@www.pumps.com:9000/path/to/file.html?a=1&b=2#frag",
    "https://www.google.com/search?q=furl+python&hl=en",
    "http://wWw.PuMpS.com:9999",
    "HTTP://Example.COM:80/Index.HTML",
    "https://example.com:443/",
    "ftp://ftp.example.org:21/pub/README",
    "unknown://pump.com:99",
    "undefined://www.pumps.com:9000/",
    "",
    "/",
    "//",
    "///",
    "////path",
    "//sup.txt",
    ":",
    "://",
    "a/b/c/",
    "/hi/",
    "sup:",
    "sup://",
    "mailto:",
    "mailto:sup@sprp.ru",
    "mailto:sproop:spraps@sprp.ru",
    "mailto://sup@sprp.ru",
    "tel:+1-555-555-1234",
    "urn:srp.com/ferret?query",
    "scheme:path",
    "none://ignored/lol?sup",
    "+invalid$scheme://lolsup",
    "1http://digits.first/",
    "a_b:weird-scheme",
    "https://www.google.com????",
    "/api/test?url=http://a.com",
    "http://blast.off/?a+b=c+d&two%20tap=cat%20nap%24%21",
    "http://pumps.com/sp%20ace/dir",
    "http://ex.com/a%2Fb/c%3Fd?x=%26&y=%3D#f%23g",
    "http://ex.com/raw space/and%20escape",
    "http://ex.com/?flag&empty=&=novalue&==&a==b",
    "http://ex.com/?a=1&a=2&a=3&b",
    "http://ex.com/?q=caf%C3%A9&r=%E2%82%AC&s=%ZZ",
    "http://ex.com/caf%C3%A9/na%C3%AFve",
    "http://ex.com/ünïcode/路径?ключ=значение#фрагмент",
    "http://sprop.ru#/mrp",
    "http://sprop.ru#mrp",
    "http://spep.ru/#ja",
    "http://ex.com/#a/b?c=d",
    "http://ex.com/#a/b?nodata",
    "http://ex.com/#?x=1",
    "http://ex.com/#k=v&w=z",
    "http://ex.com/#/path%3Fwith?q=1",
    "http://192.168.1.101",
    "http://1.2.3.4.5.6/",
    "http://[2001:db8:85a3:8d3:1319:8a2e:370:7348]/",
    "http://[2001:DB8::1]:8080/x",
    "http://[::1]/",
    "http://[v1.fe]/future",
    "http://user@host.com/",
    "http://user:@host.com/",
    "http://:pass@host.com/",
    "http://@host.com/",
    "http://us%20er:p%40ss@host.com/",
    "http://host.com.:8080/",
    "http://bücher.de/straße",
    "http://xn--bcher-kva.de/",
    "http://www.xn--bcher-kva.de/",
    "http://XN--BCHER-KVA.DE/",
    "http://www.example.com/a/./b/../c//d/",
    "  http://leading.space/",
    "http://tab\tand\nnewline.com/p\ta\nth",
    "wss://slrp.com/",
    "redis://cache.local:6379/0",
    "git://github.com/gruns/furl.git",
    "file:///etc/hosts",
    "file://localhost/etc/hosts",
]:
    job(u, D_)

section("parsing errors")
for u in [
    "http://www.pumps.com:invalid/",
    "http://a.com:/",
    "http://a.com:0/",
    "http://a.com:65536/",
    "http://a.com:65535/",
    "http://a.com:00080/",
    "http://[0:0:0:0:0:0:0:1/",
    "http://0:0:0:0:0:0:0:1]/",
    "http://[0:0:0:0:0:0:0:1:1:1:1:1:1:1:1:9999999999999]/",
    "http://[1.2.3.4]/",
    "http://[vz.x]/",
    "http://[::1]x/",
    "http://x[::1]/",
    "http://a..b/",
    "http://.a/",
    "http://a b/",
    "http://bad*host/",
    "http://a.com:8080:9090/",
    "http://" + "a" * 63 + ".com/",
    "http://" + "a" * 64 + ".com/",
]:
    job(u, D_)

section("the constructor's keyword arguments")
job({"url": "http://a.com/", "args": {"a": "1", "b": ["2", "3"]}}, D_)
job({"url": "http://a.com/x", "path": "y/z", "fragment": "f?g=h"}, D_)
job({"scheme": "https", "host": "API.Example.com", "port": 8443,
     "path": ["v1", "users", ""], "query": "limit=10&offset=20"}, D_)
job({"url": "http://a.com/", "netloc": "u:p@b.com:81", "host": "c.com"}, D_)
job({"url": "http://a.com/", "origin": "https://d.com:444"}, D_)
job({"origin": "e.com"}, D_)
job({"url": "http://a.com/", "fragment_path": "p/q", "fragment_args": {"x": "y"},
     "fragment_separator": False}, D_)
job({"url": "http://a.com/", "username": "al ice", "password": "s3:cr@t"}, D_)
job({"url": "http://a.com/", "port": "nope"})
job({"url": "http://a.com/", "host": "bad host"})
job({"url": "http://a.com/", "query_params": [["k", "v"], ["k", None], ["n", 5]]}, D_)

section("add")
job("http://a.com/", ["add", {"path": "b"}], ["add", {"path": "c/d/"}],
    ["add", {"path": ["e", "f g"]}], ["add", {"path": "/h"}], ["add", {"path": ""}])
job("http://a.com", ["add", {"path": "b"}], ["add", {"path": "/"}],
    ["add", {"path": ["", "c"]}], D_)
job("/", ["add", {"path": "x"}], ["add", {"path": ["", "y"]}])
job("", ["add", {"path": "rel"}], ["add", {"path": "more/"}], ["add", {"path": "/abs"}])
job("a/b", ["add", {"path": ["c", ""]}], ["add", {"path": ["", "d"]}])
job("http://a.com/?x=1", ["add", {"args": {"x": "2", "y": None}}],
    ["add", {"query_params": [["z", ""], ["x", ["3", "4"]]]}],
    ["add", {"args": "w=5&w&v=%20+"}], ["add", {"args": {"e": []}}], D_)
job("http://a.com/", ["add", {"args": {"a": 1}, "query_params": {"b": 2}}])
job("http://a.com/#frag", ["add", {"fragment_path": "more"}],
    ["add", {"fragment_args": {"k": "v"}}], ["add", {"fragment_path": ["", "x"]}], D_)
job("http://a.com/p/", ["add", {"path": "a%2Fb"}], ["add", {"path": "c d%20e"}],
    ["add", {"path": "€"}], D_)

section("set")
job("http://a.com/x?y=1#z", ["set", {"scheme": "https"}], ["set", {"host": "B.com"}],
    ["set", {"port": 8080}], ["set", {"port": None}], ["set", {"path": "/new/path"}],
    ["set", {"query": "q=1&q=2"}], ["set", {"args": {"r": "3"}}],
    ["set", {"query_params": [["s", "4"]]}], ["set", {"fragment": "top"}],
    ["set", {"fragment_path": "f/p", "fragment_args": {"fa": "1"}}],
    ["set", {"fragment_separator": False}], D_)
job("http://a.com/x", ["set", {"netloc": "user:pw@c.com:99"}], ["set", {"username": None}],
    ["set", {"password": "new:pw"}], ["set", {"username": ""}], ["set", {"netloc": None}], D_)
job("http://a.com/x?k=v", ["set", {"origin": "ftp://files.org"}],
    ["set", {"origin": "files.org:2121"}], ["set", {"origin": None}], D_)
job("http://a.com/x?k=v#f", ["set", {"path": "/y", "port": "bad"}], D_)
job("http://a.com/x", ["set", {"host": "[::1]"}], ["set", {"host": "[::1"}],
    ["set", {"host": "a..b"}], ["set", {"host": "xn--bcher-kva.de"}],
    ["set", {"host": "MÜNCHEN.de"}], ["set", {"host": None}], D_)
job("http://a.com:81/", ["set", {"scheme": None}], ["set", {"scheme": ""}],
    ["set", {"scheme": "HTTPS"}], ["set", {"port": 443}], ["set", {"port": "0443"}], D_)
job("http://a.com/", ["set", {"port": 0}], ["set", {"port": 70000}], ["set", {"port": -1}],
    ["set", {"port": "8 0"}])
job("http://a.com/x?y#z", ["set", {"path": None}], ["set", {"query": None}],
    ["set", {"fragment": None}], D_)
job("http://a.com/x", ["set", {"path": ["", "a b", "c/d", ""]}], D_)
job("mailto:", ["set", {"path": "joe@example.com"}], ["set", {"args": {"subject": "Hi there"}}], D_)

section("remove")
job("http://u:p@a.com:81/a/b/c?x=1&y=2&x=3#f/g?h=i",
    ["remove", {"args": ["x"]}], ["remove", {"query": ["y"]}], ["remove", {"port": True}],
    ["remove", {"username": True}], ["remove", {"password": True}],
    ["remove", {"path": "c"}], ["remove", {"fragment_path": "g"}],
    ["remove", {"fragment_args": ["h"]}], D_)
job("http://a.com/a/b/c/?k=1&k=2&k=3&j=1",
    ["remove", {"args": [["k", "2"]]}], ["remove", {"query_params": {"k": "3"}}],
    ["remove", {"args": "j"}], ["remove", {"args": [["k", "9"]]}], D_)
job("http://a.com/a/b/c", ["remove", {"path": "b/c"}], ["path.set", "/a/b/c"],
    ["remove", {"path": "/b/c"}], ["path.set", "/a/b/c/"], ["remove", {"path": "c/"}],
    ["path.set", "/a/b/c/"], ["remove", {"path": "c"}], ["path.set", "/a/b"],
    ["remove", {"path": "x/y/z/w"}], ["remove", {"path": True}], D_)
job("http://a.com/", ["path.remove", ""], ["path.set", "x"], ["path.remove", "x"],
    ["path.set", "/x"], ["path.remove", "/x"], ["path.set", ""], ["path.remove", "/"])
job("http://u:p@a.com:81/p?q=1#f", ["remove", {"netloc": True}], D_)
job("http://u:p@a.com:81/p?q=1#f", ["remove", {"origin": True}], D_)
job("http://a.com/p?q=1#f", ["remove", {"scheme": True}], ["remove", {"host": True}],
    ["remove", {"fragment": True}], ["remove", {"query": True}], D_)
job("http://a.com/?a&b=1", ["remove", {"args": [["a", None]]}],
    ["remove", {"args": {"b": "1"}}], ["remove", {"args": ["missing"]}], D_)
job("http://a.com/#x/y?a=1&b=2", ["remove", {"fragment": "ignored"}],
    ["fragment.remove", {"args": ["a"], "path": "y"}], ["fragment.remove", {"fragment": True}], D_)

section("join")
job("http://www.pumps.com/a/b/c", ["join", "d"], ["join", "../e"], ["join", "/f/g"],
    ["join", "?q=1"], ["join", "#frag"], ["join", "//other.org/x"], ["join", "h/./i/../j"],
    ["join", "https://secure.org:8443/s/"], ["join", "..", "../.."], D_)
job("unknown://pump.com/a/b", ["join", "c"], ["join", "/d"], ["join", "other://x.com/y"],
    ["join", "z"])
job("mailto:a@b.com", ["join", "c@d.com"])
job("", ["join", "http://a.com/x"], ["join", "y"])
job("http://a.com/", ["join", "http://[::1"])
job("http://a.com/b/c?q#f", ["join", ""], ["join", "?"], ["join", "#"], ["join", "."], D_)
job("redis://cache:6379/1", ["join", "2"], D_)

section("division and copies")
job("http://a.com/x/", ["div", "y"], ["div", "z/"], ["div", ["w", "v"]], ["div", "/abs"])
job("http://a.com/x#p?q=1", ["fragment.set", {"separator": False}], ["copy"], D_)
job("http://a.com/x#p?q=1", ["fragment.set", {"separator": False}], ["div", "y"])

section("attribute assignment")
job("http://a.com/p?q=1#f", ["attr", "scheme", "FTP"], ["attr", "host", "B.Org"],
    ["attr", "port", 2121], ["attr", "port", "x"], ["attr", "username", "me"],
    ["attr", "password", "p/w"], ["attr", "path", "/n e/w"], ["attr", "query", "a=b"],
    ["attr", "args", {"c": "d"}], ["attr", "fragment", "new?frag=1"], D_)
job("http://a.com/p", ["attr", "netloc", "x.org:8080"], ["attr", "netloc", "[::1]:9"],
    ["attr", "netloc", "[::1]9"], ["attr", "netloc", "[::1]:"], ["attr", "netloc", "a@b@c.com"],
    ["attr", "origin", "https://[::2]:444"], ["attr", "url", "ws://new.url/x"], D_)
job("http://a.com/p", ["attr", "host", "a.com:80"], ["attr", "host", "a\"b.com"],
    ["attr", "host", "ok-host.com."], ["attr", "host", ""], ["attr", "host", "."])

section("paths")
job("http://a.com/p", ["path.isabsolute", False])
job("http://a.com", ["path.isabsolute", False], ["get", "path.isabsolute"],
    ["path.add", "x"], ["get", "path.isabsolute"])
job("a/b", ["path.isabsolute", True], ["get", "path.isabsolute"], ["path.isabsolute", False],
    ["get", "path"], ["get", "path.segments"], ["get", "path.isdir"], ["get", "path.isfile"])
job("", ["get", "path.isabsolute"], ["get", "path.isdir"], ["get", "path.segments"])
job("http://a.com/", ["get", "path.segments"], ["get", "path.isdir"], ["get", "path.isabsolute"])
for p in ["//a/./b/../c//", "/a/b/..", "a/../..", "/../x", "../x/../../y", "/.", ".",
          "a/b/../", "/a//b///c", "/%2E%2E/x", "/a/b/c/./../../g", "/x/y/../.././../z/"]:
    job({"url": "http://h.com/", "path": p}, ["path.normalize"], ["get", "path.segments"])
job("rel/./a/../b", ["path.normalize"], ["path.set", "x/.."], ["path.normalize"],
    ["get", "path.segments"], ["path.set", "x/../"], ["path.normalize"], ["get", "path.segments"])
job("http://a.com/a%20b/c%25d/e%2Ff", ["get", "path.segments"], ["path.add", "g h"],
    ["path.add", ["i/j", "k?l", "m#n", "o%p"]], ["get", "path.segments"], D_)
job("http://a.com/", ["path.set", ["a", "", "b"]], ["get", "path.segments"],
    ["path.set", [""]], ["get", "path.segments"], ["path.add", "x"], ["get", "path.segments"])

section("queries")
job("http://a.com/?a=1", ["query.set", {"a": "2", "b": "3"}],
    ["query.set", [["a", "4"], ["a", "5"], ["c", "6"]]], ["query.set", {"a": ["7", "8", "9"]}],
    ["query.set", {"a": []}], ["query.set", [["c", "x"], ["c", "y"], ["c", "z"]]], D_)
job("http://a.com/?k=1&k=2&j=1", ["query.set", [["k", "a"], ["j", "b"], ["k", "c"], ["k", "d"]]],
    ["query.set", [["k", []], ["k", "e"]]], ["query.set", [["j", "f"], ["j", []]]], D_)
job("http://a.com/", ["query.load", "a=1&b=2"], ["query.load", {"c": "3"}],
    ["query.load", [["d", "4"], ["d", []]]], ["query.load", ""], ["query.params", "e=5&e=6"],
    ["query.params", [["f", ["7", "8"]]]], ["query.add", "g=9"], ["query.add", [["h", 10]]], D_)
job("http://a.com/?a=1&b=2&a=3", ["query.remove", "a"], ["query.remove", True],
    ["query.add", "x=1&x=2"], ["query.remove", [["x", "1"]]], ["query.remove", {"x": "2"}])
job("http://a.com/?a+b=c+d&e%20f=g%20h&i=j%2Bk&l=%3D&m=%26&n=%23&o=%3F",
    ["query.encode", {}], ["query.encode", {"delimiter": ";"}],
    ["query.encode", {"quote_plus": False}], ["query.encode", {"dont_quote": "=&#?"}],
    ["query.encode", {"dont_quote": True}], ["query.encode", {"dont_quote": False}],
    ["query.encode", {"delimeter": "|"}], ["get", "args"])
job("http://a.com/?=a&==b&=&==&&a", ["query.encode", {}], ["get", "args"], D_)
job("http://a.com/?url=http://b.com/x?y=1&path=/a/b&mail=a@b.com&list=1,2,3&star=*",
    ["query.encode", {}], ["query.encode", {"dont_quote": "/:?@,"}],
    ["tostr", {"query_dont_quote": True}], ["tostr", {"query_quote_plus": False}],
    ["tostr", {"query_delimiter": ";", "query_dont_quote": "/"}])
job("http://a.com/", ["args.set", "a", "1"], ["args.set", "b", ["2", "3"]],
    ["args.add", "a", "4"], ["args.set", "a", ["5", "6", "7"]], ["args.set", "a", ["8"]],
    ["args.get", "a"], ["args.get", "b"], ["args.get", "zz"], ["args.del", "b"],
    ["args.del", "b"], ["args.set", "a", []], ["args.set", "n", None], ["args.set", "i", 42],
    ["args.set", "t", True], ["args.add", "u", ["p", "q"]], ["args.add", "u", []], D_)
job("http://a.com/?q=%E2%98%83&r=%F0%9F%90%8D&bad=%C3&space=a%20b&plus=a+b",
    ["get", "args"], ["query.encode", {}], ["query.encode", {"quote_plus": False}])
job("http://a.com/", ["query.add", {"k": "café", "€": "€uro", "e": "a=b&c"}], ["get", "query"])

section("fragments")
job("http://a.com/#path/to?k=v&k2=v2", ["get", "fragment"], ["get", "fragment.path"],
    ["get", "fragment.query"], ["fragment.set", {"separator": False}], ["get", "fragment"],
    ["fragment.set", {"path": "", "separator": True}], ["get", "fragment"],
    ["fragment.set", {"path": "p", "args": ""}], ["get", "fragment"], D_)
job("http://a.com/", ["fragment.load", "!/hash/bang?x=1"], ["fragment.set", {"separator": False}],
    ["fragment.path.add", "more"], ["fragment.query.add", {"y": "2"}],
    ["fragment.path.isabsolute", True], ["fragment.path.remove", "more"],
    ["fragment.query.remove", ["x"]], D_)
job("http://a.com/", ["fragment.add", {"path": "a?b"}], ["get", "fragment"],
    ["fragment.add", {"args": {"c": "d"}}], ["get", "fragment"], ["fragment.set", {"separator": False}],
    ["get", "fragment"], D_)
job("http://a.com/#a=b?c", ["get", "fragment.path"], ["get", "fragment.query"], D_)
job("http://a.com/#a?b", ["get", "fragment.path"], ["get", "fragment.query"],
    ["fragment.path.isabsolute", True], D_)
job("http://a.com/", ["fragment.set", {"path": ["", "x y", "z"], "args": [["s", "t u"]]}], D_)

section("netloc, origin and ports")
job("http://a.com/", ["get", "netloc"], ["get", "origin"], ["get", "port"],
    ["attr", "scheme", "unknownscheme"], ["get", "port"], ["get", "origin"],
    ["attr", "scheme", None], ["get", "origin"], ["get", "netloc"])
job("https://a.com:8443/", ["attr", "scheme", "http"], ["get", "port"], ["attr", "port", None],
    ["get", "port"], ["attr", "scheme", "https"], ["get", "port"], ["get", "netloc"])
job("http://a.com", ["remove", {"host": True}], ["get", "netloc"], ["get", "origin"],
    ["attr", "port", 8080], ["get", "netloc"], D_)
job("//a.com:8080/x", ["get", "port"], ["get", "origin"], ["attr", "scheme", "http"], D_)
job("http://" + "x" * 64 + ".com/", ["get", "host"], ["get", "netloc"], ["get", "origin"],
    ["set", {"path": "/p"}], ["attr", "host", "short.com"], D_)
job("http://bücher.example/", ["get", "host"], ["get", "netloc"], ["get", "origin"],
    ["attr", "host", "ÉCOLE.fr"], ["get", "host"], ["get", "url"])

prog("canon data/links.txt")
prog("redirects data/redirects.tsv")
prog("api data/api.tsv")

with open(os.path.join(D, "jobs.jsonl"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(JOBS) + "\n")

LINKS = """# links a crawl found on one site
https://Shop.Example.com/products/shoes?utm_source=news&utm_medium=email&size=42
https://shop.example.com/products/shoes?size=42
https://shop.example.com:443/products/./shoes?size=42#reviews
https://shop.example.com/products/hats/../shoes?size=42&fbclid=IwAR0x
https://shop.example.com/products/shoes?size=43
http://shop.example.com/products/shoes?size=42
https://shop.example.com/products/shoes/?size=42
https://shop.example.com/search?q=red+shoes&gclid=abc123&page=2
https://shop.example.com/search?page=2&q=red%20shoes
https://shop.example.com/a%20b/c
https://shop.example.com/a b/c
https://shop.example.com:8443/admin/
https://shop.example.com:/broken
https://user:secret@shop.example.com/account
https://shop.example.com/products//shoes
https://shop.example.com/products/shoes?utm_campaign=fall#top
https://shop.example.com/?
https://shop.example.com
"""
with open(os.path.join(D, "links.txt"), "w", encoding="utf-8") as fh:
    fh.write(LINKS)

REDIRECTS = [
    ["http://example.com/old", "/new", "https://example.com/new", "../final?x=1#top"],
    ["https://a.example/docs/v1/guide", "../v2/guide", "intro", "//cdn.example/static/guide",
     "?lang=en"],
    ["http://shortener.example/abc", "https://target.example:8443/landing?ref=abc",
     "http://target.example:80/landing"],
    ["http://loop.example/a", "b", "c", "/a"],
    ["http://bad.example/start", "http://[broken/"],
]
with open(os.path.join(D, "redirects.tsv"), "w", encoding="utf-8") as fh:
    fh.write("# start URL, then each Location header in turn\n")
    for r in REDIRECTS:
        fh.write("\t".join(r) + "\n")

API = [
    ["https://api.github.com", "repos/gruns/furl/issues", {"state": "open", "labels": "bug,help wanted", "per_page": 50}],
    ["https://api.example.com/v2/", "/search", {"q": "café & bar", "fields": "id,name", "tags": ["a", "b"]}],
    ["https://maps.example.com/api?key=K", "geocode/json", {"address": "1600 Amphitheatre Pkwy, Mountain View", "key": "NEW"}],
    ["http://localhost:8080/base/", "items/", {"filter": "price>10", "sort": "-date", "empty": ""}],
]
with open(os.path.join(D, "api.tsv"), "w", encoding="utf-8") as fh:
    fh.write("# base URL, resource path, parameters\n")
    for a in API:
        fh.write("%s\t%s\t%s\n" % (a[0], a[1], json.dumps(a[2], ensure_ascii=False)))

with open(os.path.join(D, "files.txt"), "w", encoding="utf-8") as fh:
    fh.write("links.txt\nredirects.tsv\napi.tsv\n")
print(len([j for j in JOBS if not j.startswith("#")]), "jobs")
