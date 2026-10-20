# Writes data/: header values for werkzeug.http's parsers (headers.txt),
# Set-Cookie jobs for dump_cookie (cookies.txt), the documents a small
# docs server holds (docs.txt and docs/), and the HTTP requests it
# receives, one per file, read in name order. Run it from the app
# directory.
import os
import shutil

if os.path.isdir("data"):
    shutil.rmtree("data")
os.makedirs("data/requests")
os.makedirs("data/docs")

# kind <TAB> header value [<TAB> extra]. An empty value is written as an
# empty field, a missing header as the word NONE.
H = []


def h(kind, value, extra=None):
    H.append(kind + "\t" + value + ("" if extra is None else "\t" + extra))


for v in [
    "a, b, c",
    'token, "quoted value", "with, comma"',
    '  spaced  ,  out , , ,last ',
    '"esc\\"aped", "back\\\\slash", plain"quote',
    'foo="bar, baz", qux',
    '"unterminated, still going',
    "",
    ",,,",
    'a, "", b',
    '"x" , "y"z, w"v"',
]:
    h("list", v)

for v in [
    "a=b, c=d",
    'realm="Login Required", charset=UTF-8',
    'key, other=1, =nokey, empty=',
    'title*=UTF-8\'\'%E2%82%AC%20rates, plain=x',
    'title*=iso-8859-1\'en\'%A3%20pound',
    'title*=bogus\'\'%41%42',
    'name*=noquotes',
    'a="1", a="2", b=3',
    'q="quoted \\"inner\\" text"',
    'x = 1 , y= "2" ,z =3',
    'max-age=0, no-cache, no-store, must-revalidate',
    'username="Mufasa", realm="testrealm@host.com", nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093", uri="/dir/index.html", qop=auth, nc=00000001, cnonce="0a4f113b"',
]:
    h("dict", v)

for v in [
    "text/html; charset=UTF-8",
    "",
    "text/plain",
    'multipart/form-data; boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW"',
    'attachment; filename="report 2024.pdf"; size=1024',
    "attachment; filename*=UTF-8''na%C3%AFve%20file.txt",
    "attachment; filename*=utf-8'en'%E2%82%AC%20rates.csv; filename=\"EURO rates.csv\"",
    "form-data; name*0=\"long\"; name*1=\"-part\"; name*2=\"-name\"",
    "form-data; title*0*=us-ascii'en'This%20is%20even%20more%20; title*1*=%2A%2A%2Afun%2A%2A%2A%20; title*2=\"isn't it!\"",
    'text/html; Charset="utf-8"; LEVEL=1',
    "text/html; charset",
    "text/html; =value; key=; ok=1",
    'text/html; "quoted"=x; next=y',
    'form-data; name="a\\"b"; filename="c\\\\d.txt"',
    'form-data; name="html%22quote"',
    "  text/css  ;  charset = utf-8  ",
    "application/json;;;charset=utf-8",
    'text/plain; a="semi;colon"; b=2',
    'text/plain; a="unterminated; b=2',
    "image/png; name*=bogus''x%20y",
    "message/external-body; access-type=URL; URL*0=\"ftp://\"; URL*1=\"cs.utk.edu/pub/moore/bulk-mailer/bulk-mailer.tar\"",
    "text/plain; x*=''%41",
]:
    h("options", v)

h("accept", "gzip, deflate, br", "gzip,br,identity,compress")
h("accept", "gzip;q=1.0, identity; q=0.5, *;q=0", "gzip,identity,br")
h("accept", "br;q=0.9, gzip;q=0.9, *;q=0.1", "zstd,gzip,br")
h("accept", "deflate;q=2, gzip;q=-1, br;q=abc, identity;q=0.001, x;q=1.50", "deflate,identity")
h("accept", "", "gzip")
h("accept", "*", "anything,else")
h("mime", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
  "text/html,application/json,image/png,text/plain")
h("mime", "application/json, text/plain;q=0.5", "text/html,text/plain,application/json")
h("mime", "text/*;q=0.3, text/html;q=0.7, text/html;level=1, text/html;level=2;q=0.4, */*;q=0.5",
  "text/html,text/html;level=1,text/html;level=2,text/plain,image/jpeg,text/html;level=3")
h("mime", "image/*", "image/png,image/svg+xml,text/plain")
h("mime", "*/*", "application/json,text/html")
h("mime", "text/plain; format=flowed; charset=utf-8", "text/plain;charset=utf-8;format=flowed,text/plain,text/plain;format=fixed")
h("mime", "bogus, */html, application/json;q=0.0", "application/json,text/html")
h("mime", "text/html", "texthtml")
h("mime", "text/html", "*/html")
h("mime", "application/vnd.api+json;q=0.9, application/json", "application/vnd.api+json,application/json,*/*")
h("mime", "", "text/html")
h("lang", "da, en-gb;q=0.8, en;q=0.7", "en-US,en-GB,da,fr")
h("lang", "de-CH, de;q=0.9, *;q=0.5", "fr,de-DE,en")
h("lang", "en-US", "en,de")
h("lang", "en", "en-US,en-GB")
h("lang", "zh-Hant-TW, zh;q=0.8", "zh-TW,zh-Hans,zh-Hant-TW")
h("lang", "pt_BR, pt;q=0.5", "pt-br,es")
h("lang", "fr-CA;q=0.9, es", "de,it")
h("lang", "", "en,de")
h("lang", "*", "ja,ko")
h("charset", "iso-8859-5, unicode-1-1;q=0.8", "utf-8,iso-8859-5")
h("charset", "UTF8, Latin-1;q=0.5, *;q=0.1", "utf-8,iso-8859-1,ascii,cp1252")
h("charset", "us-ascii;q=0.7, windows-1252", "ascii,cp1252,latin9")
h("charset", "x-made-up, Shift_JIS;q=0.2", "sjis,X-MADE-UP,koi8-r")
h("charset", "utf 8, utf_16;q=0.4", "UTF-8,utf16,UTF-16LE")

for v in [
    "max-age=3600, no-cache",
    "no-store",
    "max-stale, min-fresh=60, only-if-cached",
    "max-stale=120, no-transform",
    "max-age=, max-age=abc",
    "max-age=+30, stale-if-error=1_000",
    'max-age="42", private="Set-Cookie", community="UCI"',
    "no-cache=\"set-cookie, set-cookie2\", must-revalidate",
    "",
    "MAX-AGE=10, Max-Age=20",
    "max-age= -5",
]:
    h("cc", v)

for v in [
    "public, max-age=31536000, immutable",
    "private, no-cache, must-revalidate, proxy-revalidate",
    'no-cache="Set-Cookie", private=x, s-maxage=600',
    "s-maxage=abc, stale-while-revalidate=30, must-understand, no-store",
    "max-age=0",
]:
    h("rcc", v)

for v in [
    "default-src 'self'; img-src *; media-src media1.com media2.com; script-src userscripts.example.com",
    "default-src 'none';script-src 'self' 'unsafe-inline';; report-uri /csp-report ;upgrade-insecure-requests",
    "  frame-ancestors   'none'  ;  default-src 'self' ; default-src https:",
]:
    h("csp", v)

for v in [
    'token, "quoted value"',
    "Accept-Encoding, accept-encoding, Origin, User-Agent",
    "",
    'GET, HEAD, "PO\\"ST"',
]:
    h("set", v)

for v, lens in [
    ("bytes=0-499", "1000,300,0"),
    ("bytes=500-999", "1000,700,500"),
    ("bytes=-500", "1000,200"),
    ("bytes=9500-", "10000,9000"),
    ("bytes=0-0,-1", "10"),
    ("bytes=0-99, 100-199", "1000"),
    ("Bytes = 10-20", "100"),
    ("items=0-9", "100"),
    ("bytes=5-1", "10"),
    ("bytes=1-2,0-3", "10"),
    ("bytes=-5,10-20", "100"),
    ("bytes=abc-def", "10"),
    ("bytes=+1-2", "10"),
    ("bytes=", "10"),
    ("bytes", "10"),
    ("bytes=0-", "0,5"),
    ("bytes=-0", "10"),
    ("bytes= 2 - 5 ", "10"),
    ("bytes=0-4,5-9,10-14", "20"),
]:
    h("range", v, lens)

for v in [
    "bytes 0-499/1234",
    "bytes 500-1233/1234",
    "bytes */1234",
    "bytes */*",
    "bytes 0-499/*",
    "bytes 499-0/1234",
    "bytes 0-1234/1234",
    "bytes 10-20",
    "bytes",
    "bytes x-y/10",
    "items 0-9/100",
    "  bytes   21010-47021/47022  ",
    "bytes 0-+5/10",
]:
    h("crange", v)

for v in [
    '"abc123"',
    'W/"weak-one"',
    "Sun, 06 Nov 1994 08:49:37 GMT",
    "Tue, 15 Nov 1994 12:45:26 +0100",
    "not a date and not quoted",
    "",
]:
    h("ifrange", v)

for v, probes in [
    ('"xyzzy"', 'xyzzy,"xyzzy",W/"xyzzy",other'),
    ('"xyzzy", "r2d2xxxx", "c3piozzzz"', "r2d2xxxx,c3piozzzz,xyzzy"),
    ('W/"xyzzy", W/"r2d2xxxx", "c3piozzzz"', 'xyzzy,W/"xyzzy","xyzzy",c3piozzzz'),
    ("*", "anything,W/\"x\""),
    ('"a",W/"b" , "c",w/"d"', "a,b,c,d"),
    ('unquoted, "q", W/raw', "unquoted,q,raw"),
    ('"one", *', "zzz"),
    ('"", W/""', '"",x'),
    ('"alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota"', "eta,kappa"),
    ("", "x"),
]:
    h("etags", v, probes)

for v in [
    "Sun, 06 Nov 1994 08:49:37 GMT",
    "Sunday, 06-Nov-94 08:49:37 GMT",
    "Sun Nov  6 08:49:37 1994",
    "Tue, 15 Nov 1994 12:45:26 +0100",
    "Tue, 15 Nov 1994 12:45:26 -0530",
    "Wed, 21 Oct 2015 07:28:00 EST",
    "Wed, 21 Oct 2015 07:28:00 PDT",
    "21 Oct 2015 07:28 GMT",
    "Wed, 21 Oct 2015 07:28:00",
    "Wed, 21 Oct 2015 07:28:00 -0000",
    "Wed, 21 Oct 2015 07:28:00 XYZ",
    "Thu, 01 Jan 1970 00:00:00 GMT",
    "Mon, 29 Feb 2016 23:59:59 GMT",
    "Tue, 29 Feb 2015 10:00:00 GMT",
    "Wed, 21 Oct 2015 25:28:00 GMT",
    "Wed, 21 Oct 15 07:28:00 GMT",
    "Fri, 31 Dec 99 23:59:59 GMT",
    "Fri, 31 Dec 68 23:59:59 GMT",
    "Wed, 21 October 2015 07:28:00 GMT",
    "Wed, 21 Foo 2015 07:28:00 GMT",
    "Oct 21 2015 07:28:00 GMT",
    "Wed,21 Oct 2015 07:28:00 GMT",
    "21 Oct 2015 07.28.00 GMT",
    "Wed, 21 Oct 2015 07:28:60 GMT",
    "Wed, 21 Oct 2015, 07:28:00 GMT",
    "garbage",
    "   ",
    "",
    "NONE",
    "Sat, 01 Jan 0000 00:00:00 GMT",
    "Fri, 31 Dec 9999 23:59:59 GMT",
    "Tue, 15 Nov 1994 12:45:26 +2500",
]:
    h("date", v)

for v in ["0", "3600", "-1", "12.5", "abc", "", "86400", " 42 ", "1_000", "+7"]:
    h("age", v)

for v in [
    "session=abc123; theme=dark",
    "a=1; b=2; a=3",
    'quoted="hello world"; esc="a\\"b"; oct="\\303\\251t\\303\\251"',
    "  spaced = value ;  other=x  ;",
    "novalue; =onlyvalue; k=",
    'mixed=café; utf8=üñï',
    'semi="a;b"; after=1',
    "",
    'trail="unterminated; next=2',
    'x="\\q\\\\"',
]:
    h("cookie", v)

for v in [
    "simple",
    "with space",
    "",
    'has"quote',
    "back\\slash",
    "token!#$%&'*+-.^_`|~09",
    "comma,semi;",
    '"already quoted"',
    '"esc\\"aped\\\\"',
    '"',
    "café",
]:
    h("quote", v)

for v in ["abc", 'W/"abc"', '"abc"', 'w/"lower"', "  \"spaced\"  ", "W/", 'bad"tag', "", '"', "W/x"]:
    h("etag", v)

for v in [
    "Content-Type, Content-Length, ETag, Expires, Content-Location, X-Custom, Allow, last-modified",
    "Connection, Keep-Alive, Upgrade, TE, X-Forwarded-For, Transfer-Encoding, Trailer, Proxy-Authorization, Content-Type",
]:
    h("strip", v)

with open("data/headers.txt", "w") as f:
    f.write("\n".join(H) + "\n")

# Set-Cookie jobs: | separated fields, flags bare.
C = [
    "k=sid|v=a3fWa|max_age=3600|expires=1445412480|path=/|secure|httponly",
    "k=theme|v=dark mode|path=/settings",
    "k=prefs|v={\"a\":1,\"b\":[2,3]}",
    "k=lang|v=fr-CA|path=/docs/user guide/|domain=.Docs.Example.com:8443|samesite=lax",
    "k=track|v=x,y;z|expires=0|samesite=STRICT",
    "k=t2|v=café \\ \"q\"|samesite=none|partitioned",
    "k=t3|v=|nopath",
    "k=t4|v=ok|samesite=bogus",
    "k=t5|v=tab\there|max_age=0|nosync",
    "k=naïve|v=1",
    "k=t6|v=\x1a\x7f|path=/a;b?c=d#e%20f",
    "k=big|v=" + "x" * 4090,
    "k=t7|v=v|expires=Wed, 09 Jun 2021 10:18:14 GMT|max_age=10",
    "k=t8|v=v|domain=localhost",
    "k=t9|v=v|max_age=120|expires=253402300799",
]
with open("data/cookies.txt", "w") as f:
    f.write("\n".join(C) + "\n")

# The docs: path | modified (Unix time) | languages | types | cache policy.
# Each language's text is docs/<name>.<lang>.txt.
DOCS = [
    ("/guide", 1445412480, ["en", "de", "fr-CA", "pt-BR"], ["text/html", "text/plain", "application/json"], "public, max-age=600"),
    ("/changelog", 1700000000, ["en"], ["text/plain"], "public, max-age=60, must-revalidate"),
    ("/logo.svg", 1600000000, ["en"], ["image/svg+xml"], "public, max-age=31536000, immutable"),
    ("/status", 1700000500, ["en"], ["application/json", "text/plain"], "no-store"),
]
TEXT = {
    ("guide", "en"): "Welcome to the user guide. Start with installation, then configure your first project.",
    ("guide", "de"): "Willkommen im Benutzerhandbuch. Beginnen Sie mit der Installation, dann konfigurieren Sie Ihr erstes Projekt. Grüße!",
    ("guide", "fr-CA"): "Bienvenue dans le guide. Commencez par l'installation, puis configurez votre premier projet. À bientôt!",
    ("guide", "pt-BR"): "Bem-vindo ao guia. Comece pela instalação e depois configure seu primeiro projeto.",
    ("changelog", "en"): "".join(
        f"v1.{i}.0 - fixed issue #{100 + i * 7}, improved startup by {i * 3} ms\n" for i in range(40)
    ),
    ("logo.svg", "en"): '<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64"><circle cx="32" cy="32" r="30" fill="#36c"/></svg>',
    ("status", "en"): "all systems operational",
}
with open("data/docs.txt", "w") as f:
    for p, m, langs, types, cache in DOCS:
        f.write(f"{p}|{m}|{','.join(langs)}|{','.join(types)}|{cache}\n")
for (name, lang), t in TEXT.items():
    with open(f"data/docs/{name}.{lang}.txt", "w") as f:
        f.write(t)

R = []


def req(method, path, headers=(), body=""):
    lines = [f"{method} {path} HTTP/1.1", "Host: docs.example.com"]
    for k, v in headers:
        lines.append(f"{k}: {v}")
    R.append("\r\n".join(lines) + "\r\n\r\n" + body)


req("GET", "/guide")
req("GET", "/guide", [("Accept", "text/plain"), ("Accept-Language", "de-DE,de;q=0.9,en;q=0.8")])
req("GET", "/guide", [("Accept", "application/json"), ("Accept-Language", "pt")])
req("GET", "/guide", [("Accept", "text/html;q=0.1, application/json;q=0.2"), ("Accept-Language", "fr-FR, fr;q=0.9")])
req("GET", "/guide", [("Accept", "image/png")])
req("GET", "/guide", [("Accept", "text/*"), ("Accept-Language", "es, *;q=0.1")])
req("GET", "/guide", [("Accept-Language", "de"), ("Cookie", "lang=pt-BR; session=s1")])
req("GET", "/guide", [("Accept-Language", "de"), ("Cookie", "lang=xx; session=s1")])
req("GET", "/guide", [("Accept-Charset", "iso-8859-1")])
req("GET", "/guide", [("Accept-Charset", "UTF8;q=0.5, *;q=0.1")])
req("HEAD", "/guide", [("Accept", "text/plain")])
req("GET", "/guide", [("If-Modified-Since", "Wed, 21 Oct 2015 07:28:00 GMT")])
req("GET", "/guide", [("If-Modified-Since", "Wed, 21 Oct 2015 07:27:59 GMT")])
req("GET", "/guide", [("If-Modified-Since", "Wednesday, 21-Oct-15 09:28:00 +0200")])
req("GET", "/guide", [("If-Modified-Since", "Wed, 21 Oct 2015 07:28:00 GMT"), ("Cache-Control", "no-cache")])
req("GET", "/guide", [("If-Modified-Since", "Wed, 21 Oct 2015 07:28:00 GMT"), ("Pragma", "no-cache")])
req("GET", "/guide", [("If-Modified-Since", "not a date")])
req("GET", "/changelog", [("Range", "bytes=0-99")])
req("GET", "/changelog", [("Range", "bytes=-120")])
req("GET", "/changelog", [("Range", "bytes=2000-")])
req("GET", "/changelog", [("Range", "bytes=99999-")])
req("GET", "/changelog", [("Range", "bytes=0-9,20-29")])
req("GET", "/changelog", [("Range", "lines=1-2")])
req("GET", "/changelog", [("Range", "bytes=5-1")])
req("HEAD", "/changelog", [("Range", "bytes=10-19")])
req("GET", "/changelog", [("Range", "bytes=0-9"), ("If-Range", "Tue, 14 Nov 2023 22:13:20 GMT")])
req("GET", "/changelog", [("Range", "bytes=0-9"), ("If-Range", "Tue, 14 Nov 2023 22:13:19 GMT")])
req("GET", "/changelog", [("Range", "bytes=0-9"), ("If-Range", '"stale-etag"')])
req("GET", "/changelog", [("If-Range", "Tue, 14 Nov 2023 22:13:20 GMT")])
req("GET", "/logo.svg")
req("GET", "/logo.svg", [("If-None-Match", '"nope", W/"also-nope"')])
req("GET", "/logo.svg", [("If-None-Match", "*")])
req("GET", "/logo.svg", [("If-Match", '"nope"')])
req("GET", "/logo.svg", [("If-Match", "*")])
req("GET", "/status")
req("GET", "/status", [("Accept", "text/plain")])
req("GET", "/missing")
req("DELETE", "/guide")
req("OPTIONS", "/changelog")
req("PUT", "/guide", [("Content-Language", "en"), ("If-Match", '"wrong"')], "Updated guide text.")
req("PUT", "/guide", [("Content-Language", "en")], "Updated guide text, second edition.")
req("GET", "/guide", [("Accept", "text/plain")])
req("PUT", "/guide", [("Content-Language", "it")], "Benvenuti.")
req("PUT", "/guide", [("Content-Language", "de"), ("If-Unmodified-Since", "Wed, 21 Oct 2015 07:28:00 GMT")], "Neu.")
req("GET", "/guide", [("Accept", "text/plain"), ("Accept-Language", "de")])
req("GET", "/prefs?lang=fr-CA")
req("GET", "/prefs?lang=klingon")
req("GET", "/prefs?lang=de&remember=0")
req("GET", "/whoami", [("Cookie", 'session="u\\303\\244ser 42"; lang=de; session=second')])
req("GET", "/whoami")
req("GET", "/proxy/upstream", [("Connection", "keep-alive, X-Trace"), ("Keep-Alive", "timeout=5"), ("X-Trace", "abc"), ("TE", "trailers")])
req("GET", "/negotiate", [("Accept", "application/xhtml+xml;q=0.9, text/html;q=0.9, */*;q=0.1"), ("Accept-Encoding", "gzip;q=0.5, br"), ("Accept-Language", "en-GB")])
req("GET", "/negotiate", [("Accept", "text/html"), ("Accept-Encoding", "identity;q=0"), ("Accept-Language", "")])
req("GET", "/negotiate", [("Accept", "bad"), ("Accept-Encoding", "*;q=0")])
req("GET", "/cache-check", [("Cache-Control", "max-age=0, max-stale=30, no-transform")])
req("GET", "/cache-check", [("Cache-Control", "only-if-cached, min-fresh=5, stale-if-error=abc")])
req("GET", "/csp", [("Content-Security-Policy-Report-Only", "default-src 'self'; script-src https://cdn.example.com; report-uri /r")])

for i, r in enumerate(R):
    with open(f"data/requests/{i:03d}.http", "w") as f:
        f.write(r)
