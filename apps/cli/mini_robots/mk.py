# Writes data/: a small web of test sites under data/web/<host>/ (each
# with a robots.txt, maybe a status for it, and pages.json), extra
# robots.txt files under data/robots/, and data/jobs.jsonl.
import json
import os

W = "data/web"


def put(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)


def page(*links, title="page"):
    body = "<html><head><title>%s</title></head><body>\n" % title
    for l in links:
        body += '<a href="%s">%s</a>\n' % (l, l)
    return body + "</body></html>\n"


def site(host, robots=None, status=None, pages=()):
    if robots is not None:
        put(f"{W}/{host}/robots.txt", robots)
    if status is not None:
        put(f"{W}/{host}/status", str(status))
    put(f"{W}/{host}/pages.json", json.dumps([{"path": p, "status": s, "body": b} for p, s, b in pages], indent=1))


site("shop.test", robots="""# robots.txt for shop.test
User-agent: *
Disallow: /cart
Disallow: /checkout/
Allow: /checkout/help
Disallow: /*?sessionid=
Disallow: /*.pdf$
Disallow: /search
Allow: /search/about$
Crawl-delay: 2
Request-rate: 3/10

User-agent: KaraBot
User-agent: OtherBot
Disallow: /private
Allow: /private/press
Disallow: /tmp/*/cache
Crawl-delay: 1

User-agent: BadBot
Disallow: /

Sitemap: https://shop.test/sitemap.xml
Sitemap: https://shop.test/sitemap-products.xml

user-agent: karabot
Disallow: /drafts
""", pages=[
    ("/", 200, page("/products", "/cart", "/checkout/help", "/checkout/pay", "/search?q=lamp",
                    "/search/about", "/private/press", "/private/stock", "/docs/manual.pdf",
                    "/docs/manual.pdf?v=2", "/item?id=3&sessionid=9", "/item?id=3", "/tmp/a/cache/x",
                    "/drafts/summer", "about.html", "#top", "/products#reviews", "//cdn.test/x.js",
                    "http://blog.test/", "http://private.test/", "http://nohost.test/",
                    "http://flaky.test/", "http://gone.test/", "http://empty.test/", "/robots.txt",
                    "/missing", title="shop")),
    ("/products", 200, page("/", "/item?id=1", "/item?id=2", "/products?page=2", "/products#top",
                            title="products")),
    ("/products?page=2", 200, page("/products", "/item?id=4", title="products 2")),
    ("/item?id=1", 200, page("/products", title="item 1")),
    ("/item?id=2", 200, page("/products", "/item?id=2&sessionid=abc", title="item 2")),
    ("/item?id=3", 200, page(title="item 3")),
    ("/item?id=4", 500, "oops\n"),
    ("/checkout/help", 200, page("/checkout/help/returns", title="help")),
    ("/checkout/help/returns", 200, page(title="returns")),
    ("/search/about", 200, page("/search/about/more", title="about search")),
    ("/private/press", 200, page("/private/press/2026", title="press")),
    ("/private/press/2026", 200, page(title="press 2026")),
    ("/tmp/a/cache/x", 200, page(title="cache")),
    ("/drafts/summer", 200, page(title="drafts")),
    ("/robots.txt", 200, "see robots\n"),
    ("/docs/manual.pdf?v=2", 200, "%PDF\n"),
])

site("blog.test", status=404, pages=[
    ("/", 200, page("/2026/10/hello", "/2026/10/robots", "/tag/kara", "http://shop.test/products",
                    "https://blog.test/secure", "/feed.xml", title="blog")),
    ("/2026/10/hello", 200, page("/", "/tag/kara", title="hello")),
    ("/2026/10/robots", 200, page("/", "/2026/10/hello#comments", title="robots post")),
    ("/tag/kara", 200, page("/2026/10/hello", title="tag")),
    ("/feed.xml", 200, "<rss/>\n"),
])
site("private.test", robots="User-agent: *\nAllow: /\n", status=403, pages=[("/", 200, page(title="private"))])
site("flaky.test", status=503, pages=[("/", 200, page(title="flaky"))])
site("gone.test", status=410, pages=[("/", 200, page("/old", title="gone")), ("/old", 200, page(title="old"))])
site("empty.test", robots="", pages=[("/", 200, page("/a", title="empty")), ("/a", 200, page(title="a"))])

site("intl.test", robots=(
    "User-agent: *\n"
    "Disallow: /café\n"
    "Disallow: /caf%C3%A9-menu\n"
    "Disallow: /%7Euser/\n"
    "Allow: /~user/public\n"
    "Disallow: /a%2fb\n").encode() + b"Disallow: /raw\xff\xfe\n" + (
    "Disallow: /percent%zz\n"
    "Disallow: /q?x=a b&y=ü\n"
    "Disallow: /日本/\n"
    "Disallow: /path;x\n"
    "Disallow: /*%2A\n"
    "Crawl-delay: ٣\n"
    "Sitemap: https://intl.test/sitemap-ü.xml\n").encode(), pages=[
    ("/", 200, page("/café", "/caf%c3%a9", "/caf%C3%A9-menu", "/%7Euser/x", "/~user/public/x",
                    "/a/b", "/raw%FF%FE", "/percent%zz", "/日本/x", "/ok", title="intl")),
    ("/ok", 200, page(title="ok")),
])

site("cr.test", robots=(
    "# CR-only line ends, odd spacing\r"
    "USER-AGENT:\tKaraBot\r"
    "DISALLOW :  /secret \r"
    "Disallow /nocolon\r"
    "Crawl-delay:　５\r"
    "Request-rate: 1 / 5\r"
    " "
    "User-agent: * "
    "Disallow: /\x0b"
    "Allow: /pub\x0c"
    "Disallow: /pub/x\x85"
    "Sitemap:   https://cr.test/map.xml   \r\n").encode(), pages=[
    ("/", 200, page("/secret", "/nocolon", "/pub/a", title="cr")),
    ("/nocolon", 200, page(title="nocolon")),
    ("/pub/a", 200, page(title="pub a")),
])

put("data/robots/bom.txt", "﻿User-agent: *\nDisallow: /\n")
put("data/robots/agents.txt", """User-agent: Googlebot-News
Disallow: /news-only

User-agent: googlebot
Disallow: /g

User-agent:
Disallow: /blank

User-agent: *
Disallow: /star

User-agent: Bad Bot
Disallow: /space
""")
put("data/robots/agents_star.txt", """User-agent: Googlebot-News
Disallow: /news-only

User-agent: *
Disallow: /star

User-agent: googlebot
Disallow: /g
""")
put("data/robots/rules.txt", """User-agent: *
Disallow: /fish*
Allow: /fish*.html$
Disallow: /*.php$
Allow: /*.php?
Disallow: /a**b
Disallow: /end$$
Disallow: /mid$dle
Disallow: /x$*
Allow: /
Disallow: /long/path
Allow: /long/
Disallow:
Disallow: /same
Allow: /same
Disallow: /*/*/deep
Disallow: *nolead
Allow: /p*q*r
Disallow: /p*q*r*$
Disallow: /search?q=*&page=
Disallow: /*?
Allow: /*?ok
""")
put("data/robots/fields.txt", """Sitemap: http://early.test/map.xml
Crawl-delay: 9
Disallow: /before-any-agent
User-agent: a # the first bot
User-agent: b
Crawl-delay: 1.5
Request-rate: 2/3/4
Disallow: /x#frag
user-agent: c
crawl-delay: 4
crawl-delay: 7
request-rate: 1/0
DisAllow: /c-only
User-agent: d
Crawl-delay: -1
Request-rate:  10 / 60
Crawl-delay: 123456789012345678901234567890
Request-rate: 00/007
User-agent: e
User-agent: A
Crawl-delay: 3
Disallow: /e
User-agent: a
Disallow: /a2
Crawl-delay: 5
User-agent: B
Disallow: /b2
Request-rate: 4/5
""")
put("data/robots/empty_rules.txt", "User-agent: *\n\nUser-agent: lonely\n")
put("data/robots/crlf.txt", "User-agent: *\r\nDisallow: /dir/\r\n\r\nAllow: /dir/ok\r\n")

AG = ["KaraBot/1.0", "karabot", "Mozilla/5.0 (compatible; KaraBot/1.0)", "OtherBot", "BadBot/3",
      "Googlebot/2.1", "Googlebot-News", "googlebot-news/1.0", "Bingbot", "", "*", "Bad Bot/1", "a", "B",
      "c/2", "dbot", "E", "lonely"]
URLS = ["/", "", "http://h/fish", "/fish.html", "/fish/salmon.html", "/fishheads/yummy.html",
        "/fish.php", "/x.php?y", "/index.php", "/index.php5", "/ab", "/a123b", "/end", "/end$",
        "/x", "/x$", "/long/path", "/long/pathx", "/long/", "/same", "/a/b/deep", "/a/deep",
        "/some/nolead", "/pXqYr", "/pXqYrZ", "/p/q", "/search?q=x&page=2", "/search?q=x", "/y?ok",
        "/y?no", "http://h/café", "/caf%c3%a9", "/caf%C3%A9-menu", "/%7Euser/x", "/~user/x",
        "/~user/public/x", "/a/b", "/a%2Fb", "/raw%FF%FE", "/raw%ff%fe", "/percent%zz",
        "/percent%25zz", "/q?x=a%20b&y=%C3%BC", "/q?x=a b&y=ü", "/日本/x",
        "/robots.txt", "/robots.txt?x", "//double", "http://h", "/path#frag", "/path?#", "?only",
        "#only", " /lead", "/tab\there", "HTTP://H/UPPER", "mailto:x", "http://[::1/x",
        "/x?a=1&a=2&b", "/%", "/%2", "/path;x", "/news-only", "/g", "/blank", "/star", "/space",
        "/c-only", "/e", "/a2", "/b2", "/x#frag", "/secret", "/pub", "/pub/x", "/pub/y", "/dir/ok",
        "/dir/no", "/cart", "/checkout/help", "/checkout/pay", "/item?id=3&sessionid=9",
        "/docs/a.pdf", "/docs/a.pdf?v", "/search/about", "/search/about/x", "/private/press",
        "/private/x", "/tmp/q/cache", "/tmp/cache", "/drafts", "/*", "/a*b", "/A%2a"]

jobs = []
J = jobs.append

J({"kind": "new", "name": "fresh", "url": "http://shop.test/robots.txt"})
J({"kind": "check", "name": "fresh", "agents": ["KaraBot/1.0"], "urls": ["/", "/cart"]})
J({"kind": "show", "name": "fresh", "agents": ["KaraBot/1.0"]})
for host in ["shop", "blog", "private", "flaky", "gone", "empty", "intl", "cr", "nohost"]:
    J({"kind": "load", "name": host, "url": f"http://{host}.test/robots.txt"})
for f in ["bom", "agents", "agents_star", "rules", "fields", "empty_rules", "crlf"]:
    J({"kind": "parse", "name": f, "file": f"robots/{f}.txt"})
for name in ["shop", "blog", "private", "flaky", "gone", "empty", "intl", "cr", "nohost", "bom", "agents",
             "agents_star", "rules", "fields", "empty_rules", "crlf"]:
    J({"kind": "show", "name": name, "agents": AG})
    J({"kind": "check", "name": name, "agents": AG, "urls": URLS})
J({"kind": "load", "name": "relative", "url": "/robots.txt"})
J({"kind": "load", "name": "shop2", "url": "HTTP://shop.test/robots.txt?x#y"})
J({"kind": "check", "name": "shop2", "agents": ["KaraBot/1.0"], "urls": ["/cart", "/private/x"]})
J({"kind": "crawl", "agent": "KaraBot/1.0 (+https://kara.test/bot)", "start": ["http://shop.test/"], "max": 60})
J({"kind": "crawl", "agent": "Mozilla/5.0 (compatible; KaraBot/1.0)", "start": ["http://shop.test/"], "max": 12})
J({"kind": "crawl", "agent": "BadBot/3", "start": ["http://shop.test/", "http://blog.test/"], "max": 20})
J({"kind": "crawl", "agent": "KaraBot", "start": ["http://intl.test/", "http://cr.test/", "http://gone.test/"],
   "max": 40})

with open("data/jobs.jsonl", "w") as f:
    for j in jobs:
        f.write(json.dumps(j, ensure_ascii=False) + "\n")
