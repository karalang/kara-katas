# Writes data/: the site under data/site/ (pages, assets, robots.txt) and
# data/url-tests.tsv, the URL-library cases the crawler checks first.
import os
def w(path, text):
    path = "data/" + path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)

w("site/robots.txt", """\
# robots.txt for docs.example.com
User-agent: *
Disallow: /drafts/
Disallow: /search
Allow: /drafts/public-roadmap.html
Disallow: /*.pdf$
Crawl-delay: 2

User-agent: kara-crawler
Disallow: /internal/
Allow: /internal/status.html
Disallow: /*?print=
Disallow: /tmp*
Disallow: /%7Euser/
Disallow: /a$b
Crawl-delay: 1
Request-rate: 30/60

User-agent: BadBot
User-agent: EvilScraper
Disallow: /

User-agent: friendly-bot
Disallow:

# merged into the kara-crawler group above
User-agent: kara-crawler
Disallow: /old/
Disallow: /archive/**/old$$
Allow: /search/help

Sitemap: https://docs.example.com/sitemap.xml
sitemap: https://docs.example.com/sitemap-api.xml
this line has no colon
Unknown-field: ignored
""")

w("site/index.html", """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Example Docs &amp; Guides &copy 2026</title>
  <link rel="stylesheet" href="/static/style.css">
  <link rel="icon" href=/static/logo.svg>
  <script src="//cdn.example.net/app.js"></script>
  <script>
    // not a link: document.write('<a href="/fake.html">x</a>');
    var u = "/also-fake.html";
  </script>
</head>
<body>
<!-- <a href="/secret.html">old link</a> -->
<nav>
  <A HREF="guide/">Guide</A>
  <a href='guide/intro.html'>Intro</a>
  <a href="/api">API</a>
  <a href="https://docs.example.com:443/changelog.html">Changes</a>
  <a href="HTTPS://Docs.Example.COM/faq.html#top">FAQ</a>
  <a href="  /faq.html  ">FAQ again</a>
  <a href="#main">Skip to content</a>
  <a href="mailto:docs@example.com">Mail us</a>
  <a href="javascript:void(0)">Menu</a>
  <a href="tel:+1-555-0100">Call</a>
</nav>
<main id="main">
  <img src="/static/logo.svg" alt="logo">
  <a href="/drafts/plan.html">Plan</a>
  <a href="/drafts/public-roadmap.html">Roadmap</a>
  <a href="/internal/admin.html">Admin</a>
  <a href="/internal/status.html">Status</a>
  <a href="search?q=kara&amp;utm_source=home&region=eu">Search</a>
  <a href>No target</a>
  <a href="">This page</a>
  <a rel="nofollow" href="/login.html">Log in</a>
  <a href="/missing.html">Gone</a>
  <a href="https://github.com/example/docs">GitHub</a>
  <a href="http://example.org/blog/">Blog</a>
  <a href="https://github.com/example/docs/issues">Issues</a>
  <a href="http://docs.example.com:8080/">Staging</a>
  <a href="http://docs.example.com:http/">Typo</a>
  <a title="x"href="/faq.html?lang=en&amp;lang=de">FAQ in two languages</a>
</main>
</body>
</html>
""")

w("site/guide/index.html", """\
<html><head><title>Guide</title></head>
<body>
<p>Start with <a href="intro.html">the introduction</a>, then
<a href="./setup.html?print=1">print the setup page</a> or read
<a href="setup.html?utm_campaign=launch&lang=en">setup</a>.</p>
<p><a href="caf%C3%A9.html">Café notes</a> and
<a href="café.html">the same notes</a>.</p>
<a href="../api/">API reference</a>
<a href="/guide/../tmp/cache.html">Cache</a>
</body></html>
""")

w("site/guide/intro.html", """\
<html><head><title>Introduction &mdash; Guide</title></head>
<body>
<a href="../index.html">Home</a>
<a href="setup.html">Setup</a>
<a href="../../../../escape.html">Escape</a>
<a href="/guide/./intro.html#x">Me</a>
<a href="a/b/../../setup.html">Setup again</a>
<a href="%7Euser/notes.html">Notes</a>
<a href="/%7Euser/">User home</a>
<a href="/search/help">Search help</a>
</body></html>
""")

w("site/guide/setup.html", """\
<html><head>
<title>Setup</title>
<META NAME="Robots" CONTENT="NoIndex">
</head>
<body>
<a href="/guide/">Back</a>
<a href="/tmp/cache.html">Cache</a>
<a href="/old/page.html">Old page</a>
<a href="/docs.pdf">PDF</a>
<a href="/archive/2024/old">Archive</a>
<a href="/search?q=setup+guide&page=2">Search</a>
<a href="/old/">Old</a>
</body></html>
""")

w("site/guide/café.html", """\
<html><head><title>Caf&eacute; notes</title></head>
<body><a href="intro.html">Intro</a></body></html>
""")

w("site/guide/~user/notes.html", "<html><head><title>User notes</title></head><body></body></html>\n")

w("site/api/index.html", """\
<html><head>
<title>API v1</title>
<base href="https://docs.example.com/api/v1/">
<link rel="canonical" href="https://docs.example.com/api/">
</head>
<body>
<a href="users.html">Users</a>
<a href="../v2/">Version 2</a>
<a href="/api/v1/users.html?b=2&a=1">Users, sorted</a>
<a href="users.html?utm_source=x&utm_medium=y">Users from a campaign</a>
<a href="orders.html;jsessionid=abc">Orders</a>
<iframe src="/api/v1/playground.html"></iframe>
</body></html>
""")

w("site/api/v1/users.html", """\
<html><head><title>Users</title>
<meta name="robots" content="noindex, nofollow"></head>
<body><a href="orders.html">Orders</a></body></html>
""")

w("site/api/v1/orders.html", "<html><head><title>Orders</title></head><body><a href='../'>Up</a></body></html>\n")
w("site/api/v1/index.html", "<html><head><title>API v1 index</title></head><body><a href=users.html>Users</a></body></html>\n")
w("site/api/v1/playground.html", "<html><head><title>Playground</title></head><body><a href=\"/api/v2/\">v2</a></body></html>\n")
w("site/api/v2/index.html", """\
<html><head><title>API v2 (beta)</title></head>
<body><a href="../v1/">v1</a> <a href="deep/one.html">deeper</a></body></html>
""")
w("site/api/v2/deep/one.html", "<html><head><title>Deep one</title></head><body><a href=\"two.html\">two</a></body></html>\n")
w("site/api/v2/deep/two.html", "<html><head><title>Deep two</title></head><body></body></html>\n")
w("site/changelog.html", "<html><head><title>Changelog</title></head><body><a href=\"/\">Home</a></body></html>\n")
w("site/faq.html", "<html><head><title>FAQ &#8212; &#x27;Questions&#39;</title></head><body><a href=\"index.html\">Home</a></body></html>\n")
w("site/drafts/plan.html", "<html><head><title>Plan</title></head><body></body></html>\n")
w("site/drafts/public-roadmap.html", "<html><head><title>Roadmap</title></head><body></body></html>\n")
w("site/internal/status.html", "<html><head><title>Status: all green</title></head><body></body></html>\n")
w("site/internal/admin.html", "<html><head><title>Admin</title></head><body></body></html>\n")
w("site/login.html", "<html><head><title>Log in</title></head><body></body></html>\n")
w("site/tmp/cache.html", "<html><head><title>Cache</title></head><body></body></html>\n")
w("site/search/help", "help text\n")
w("site/static/style.css", "body { font-family: sans-serif; }\n")
w("site/static/logo.svg", "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\"></svg>\n")
w("site/old/index.html", "<html><head><title>Old</title></head><body></body></html>\n")

# The URL-library cases: an operation and its arguments, tab-separated,
# with a backslash, tab or newline inside one written as \\, \t or \n.
tests = []
def t(*args):
    esc = lambda a: a.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")
    tests.append("\t".join(esc(a) for a in args))
base = "http://a/b/c/d;p?q"
for ref in ["g:h", "g", "./g", "g/", "/g", "//g", "?y", "g?y", "#s", "g#s",
            "g?y#s", ";x", "g;x", "g;x?y#s", "", ".", "./", "..", "../",
            "../g", "../..", "../../", "../../g", "../../../g",
            "../../../../g", "/./g", "/../g", "g.", ".g", "g..", "..g",
            "./../g", "./g/.", "g/./h", "g/../h", "g;x=1/./y", "g;x=1/../y",
            "g?y/./x", "g?y/../x", "g#s/./x", "g#s/../x", "http:g",
            "mailto:x@y", "HTTP://A/g", "//g:80/x"]:
    t("join", base, ref)
t("join", "https://example.com/a/b/", "c/../../d")
t("join", "https://example.com", "x")
t("join", "https://example.com/dir/file.html", "?page=2")
t("join", "mailto:a@b", "c")
t("join", "file:///etc/hosts", "passwd")
for u in ["https://user:pa%20ss@Example.COM:8443/p/a;x?q=1&r=2#frag",
          "http://[2001:DB8::1]:8080/index.html",
          "http://example.com:/empty-port",
          "http://example.com?query-only",
          "HTTP://EXAMPLE.com#frag-only",
          "mailto:user@example.com?subject=Hi",
          "//cdn.example.net/lib.js",
          "relative/path?x#y",
          "  \t https://ex\tample.com/sp ace\n",
          "http://example.com:abc/",
          "http://example.com:70000/",
          "http://@host/",
          "tel:+1-555-0100",
          "1http://not-a-scheme/",
          "a+b.c-d://ok/"]:
    t("split", u)
for s, safe in [("/a b/c?d", "/"), ("café/~user", "/"), ("a+b=c&d", ""),
                ("100% sure!", "!"), ("x/y", "")]:
    t("quote", s, safe)
for s in ["a b&c=d/é", "already+plus"]:
    t("quote_plus", s)
for s in ["%7Euser%2Fdocs", "caf%C3%A9", "100%", "%zz%4", "a+b"]:
    t("unquote", s)
t("unquote_plus", "a+b%2Bc")
for q in ["a=1&b=2&a=3", "x=a+b%20c&empty=&novalue&&y=%3D", "utm_source=x&id=7", ""]:
    t("qsl", q)
t("encode", "q", "kara lang", "path", "/a/b", "sym", "a&b=c", "u", "é")
open("data/url-tests.tsv", "w", encoding="utf-8").write("\n".join(tests) + "\n")
