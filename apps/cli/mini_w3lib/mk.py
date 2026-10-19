# Writes data/: the jobs (calls.jsonl, recorded from w3lib's own test
# suite, plus the extra calls below) and a small web site for the crawl.
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def enc(v):
    if v is None or isinstance(v, bool):
        return v
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return {"f": repr(v)}
    if isinstance(v, str):
        return {"s": v}
    if isinstance(v, (bytes, bytearray)):
        return {"b": bytes(v).hex()}
    if isinstance(v, (tuple, list)):
        return {"l": [enc(x) for x in v]}
    if isinstance(v, dict):
        return {"d": [[enc(k), enc(x)] for k, x in v.items()]}
    raise TypeError(type(v))


EXTRA = []


def call(mod, f, *a, **k):
    EXTRA.append({"m": mod, "f": f, "a": [enc(x) for x in a], "k": {n: enc(x) for n, x in k.items()}})


# Encoding labels, as pages and servers spell them.
LABELS = [
    "utf-8", "UTF8", "utf_8", "U8", "latin1", "latin-1", "ISO-8859-1", "iso_8859-1:1987",
    "l1", "cp1252", "windows-1252", "WINDOWS-1251", "cp1251", "koi8-r", "KOI8_U", "gb2312",
    "GBK", "gb_2312-80", "GB18030", "big5", "Big5-HKSCS", "euc-kr", "EUC_JP", "shift_jis",
    "Shift-JIS", "sjis", "x-sjis", "windows-31j", "iso-2022-jp", "tis-620", "iso-8859-11",
    "windows-874", "iso8859_9", "macintosh", "mac-roman", "us-ascii", "ascii", "ANSI_X3.4-1968",
    "646", "utf-16", "UTF-16LE", "utf-16be", "utf-32", "utf-7", "UTF7", "unicode-1-1-utf-7",
    "zh_cn", "win-1251", "iso-8859-15", "latin9", "hebrew", "greek", "arabic", "cyrillic",
    "cp437", "ibm866", "x-mac-cyrillic", "hz", "euc-tw", "x-user-defined", "none", "",
    "utf 8", "UTF--8", "utf.8", "8859", "iso8859", "rot13", "base64", "idna", "punycode",
    "hex", "zip", "mbcs", "unicode_escape", "raw-unicode-escape", "cp65001", "ks_c_5601-1987",
    "iso-ir-100", "csISOLatin1", "IBM037", "cp500", "utf_16_le", "u16", "utf_32_be", "cp-1250",
]
for lab in LABELS:
    call("encoding", "resolve_encoding", lab)

for ct in [
    "text/html; charset=ISO-8859-4",
    "text/html;charset=\"windows-1251\"",
    "application/xhtml+xml; Charset=UTF-8; q=0.9",
    "text/html; charset=utf-8, text/html; charset=iso-8859-1",
    "text/html; foo=\"charset=latin1\"; charset=koi8-r",
    "text/html; charset=utf-7",
    "text/plain; charset = utf-8",
    "text/html; charset=\"\"",
]:
    call("encoding", "http_content_type_encoding", ct)

for b in [b"\xef\xbb\xbfhi", b"\xfe\xff\x00h", b"\xff\xfe\x00\x00h\x00\x00\x00", b"\xff\xfeh\x00", b"\x00\x00\xfe\xffxx", b"plain", b""]:
    call("encoding", "read_bom", b)

for ct, body in [
    ("text/html; charset=windows-1251", "Привет, мир".encode("cp1251")),
    (None, "<meta charset=\"cp1251\"><p>Новости".encode("cp1251")),
    (None, b"<?xml version=\"1.0\" encoding=\"latin1\"?><r>caf\xe9 \x80</r>"),
    (None, b"<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=us-ascii\"></head>\x93quoted\x94"),
    ("text/html", b"<!-- <meta charset=cp1251> --><meta charset=\"utf-8\">caf\xc3\xa9 \xff\xfe broken"),
    ("text/html; charset=utf-8", b"\xe2\x82 cut \xf0\x9f\x98 cut \xed\xa0\x80 surrogate \xc0\xaf overlong"),
    ("text/html; charset=utf-16-le", "Grüße".encode("utf-16-le") + b"\x00"),
    ("text/html; charset=utf-16", "hi".encode("utf-16-be")),
    (None, b"\xff\xfe" + "BOM wins".encode("utf-16-le")),
]:
    call("encoding", "html_to_unicode", ct, body)

for u, p in [("Aladdin", "open sesame"), ("josé", "pässwörd"), (b"raw", b"bytes:colon")]:
    call("http", "basic_auth_header", u, p)
call("http", "basic_auth_header", "josé", "€uro", encoding="utf-8")
call("http", "headers_raw_to_dict", b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nSet-Cookie: a=1\r\nSet-Cookie: b=2\r\n  X-Spaced :  v  \r\nbroken line\r\n\r\n")
call("http", "headers_dict_to_raw", {b"Content-Type": b"text/html", b"Set-Cookie": [b"a=1", b"b=2"], b"X-Empty": []})

for u in [
    "http://www.example.com/a b?q=x y#frag ment",
    "https://bücher.example/kaufen?titel=Faust",
    "http://ＥＸＡＭＰＬＥ.com/full-width",
    "http://xn--bcher-kva.example/already",
    "http://straße.de/",
    "http://Ⅻ.example/roman",
    "http://example.com:8080/path;params?q#f",
    "http://user:p@ss w0rd@host.example/",
    "http://[2001:DB8::1]:8080/v6",
    "http://例え.テスト/パス?クエリ=値",
    "ftp://ftp.example.org/pub/file name.txt",
    "http://example.com?only=query",
    "http://évil.com\\@good.com/",
    "http://exa\tmple.com/\ttab",
    "http://a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.x.y.z.aa.bb.cc.dd.ee.ff.gg.hh.ii.jj.kk.ll.mm.nn.oo.pp.qq.rr.ss.tt.uu.vv.ww.xx.yy.zz.example/",
    "http://" + "ü" * 70 + ".example/long-label",
    "http://.example.com/empty-label",
    "http://xn--zz.example/bad-ace?",
    "http://мойсайт.рф/страница?параметр=значение",
]:
    call("url", "safe_url_string", u)
call("url", "safe_url_string", "http://example.com/путь?запрос=знач", encoding="cp1251")
call("url", "safe_url_string", "http://example.com/café?café=1", encoding="latin1", path_encoding="latin1")
call("url", "safe_url_string", "http://example.com/€?€=1", encoding="cp1252")
call("url", "safe_url_string", "http://example.com/x?q=ф", encoding="latin1")
call("url", "safe_url_string", "http://example.com/x?q=ф", encoding="ascii")
call("url", "safe_url_string", b"http://example.com/\xe9t\xe9?q=\xff", encoding="utf-8")
call("url", "safe_url_string", b"http://example.com/\xe9t\xe9?q=\xff", encoding="cp1252")
call("url", "safe_url_string", "http://example.com/raw path", quote_path=False)

for u in [
    "http://www.example.com/do?c=3&b=5&b=2&a=50",
    "http://www.example.com/résumé",
    "http://[::0:1]/a/../b",
    "HTTP://Example.COM:/A/./B/../C?z=1&a=&b=2#Frag",
    "http://user:Pass@WWW.Example.com/%7Euser/%2fslash%2F?q=a+b&q=a%20b",
    "http://www.example.com/a%a3do?q=r%E9sum%E9",
    "mailto:a/../b",
    "foo:/a/../b",
    "http://example.com/a;b/c;d?x=1",
    "http://[2001:0db8:0000:0000:0000:ff00:0042:8329]/",
]:
    call("url", "canonicalize_url", u)
call("url", "canonicalize_url", "http://example.com/?q=ф&b=1", encoding="latin1")
call("url", "canonicalize_url", "http://example.com/?q=ф&b=1", encoding="cp1251")
call("url", "canonicalize_url", "http://example.com/?b=;a=2;c", query_separator=";", keep_blank_values=False)
call("url", "canonicalize_url", "http://example.com/p#keep", keep_fragments=True)

for u in [
    "data:,A%20brief%20note",
    "data:text/plain;charset=iso-8859-7,%be%fa%be",
    "data:image/png;base64,iVBORw0KGgo=",
    "data:text/html;charset=utf-8;base64,PGI+aGk8L2I+",
    "data:;base64,SGVs bG8=",
    "data:text/plain;name=\"a\\\"b\";base64,QUJD",
    "data:text/plain;base64,QUJDRA",
    "data:text/plain;base64,QUJDR",
    "data:text/plain;base64,Q===",
    "data:text/plain;base64,QU=JD",
    "DATA:TEXT/PLAIN,upper",
    "data:text/plain;base63,xx",
]:
    call("url", "parse_data_uri", u)

for p in ["/home/user/My Files/report #1.pdf", "/tmp/a/./b//c/", "//server/share/x", "/ünï cödé/ø"]:
    call("url", "path_to_file_uri", p)
for u in ["file:///home/user/My%20Files/report%20%231.pdf", "file://localhost/etc/hosts", "file:///%C3%BC%C3%BF"]:
    call("url", "file_uri_to_path", u)

ENTITIES = [
    "&lt;b&gt; &amp;amp; &quot;q&quot; &apos;a&apos;",
    "&eacute;t&eacute; &Eacute;T&Eacute; &EACUTE; &nbsp;|&nbsp",
    "&#8364; &#x20AC; &#X20ac; &#128; &#x80; &#x81; &#x9F; &#0; &#xD800; &#1114111; &#1114112; &#99999999999999999999;",
    "&notanentity; &notin; &not &am &#; &#x; &#xZZ;",
    "&hellip;&mdash;&lsquo;&rsquo;&ldquo;&rdquo;&trade;&copy;&reg;&deg;&micro;&para;",
]
for t in ENTITIES:
    call("html", "replace_entities", t)
    call("html", "replace_entities", t, keep=["amp", "LT"], remove_illegal=False)

DOC = """<html><head><title>Shop &amp; Co</title>
<script type="text/javascript">if (a < b && c > d) { x = "<b>"; }</script>
<style>p > a { color: red }</style><!-- note <b>hidden</b> --></head>
<body><div class="main"><p>Price: <b>&pound;100</b> <a href="/buy?id=1&amp;q=2" title='a > b'>buy</a></p>
<br/><img src=x.png alt="pic"><![CDATA[ <raw> &amp; ]]><p>tail</body></html>"""
call("html", "remove_tags", DOC)
call("html", "remove_tags", DOC, which_ones=["b", "A", "script"])
call("html", "remove_tags", DOC, keep=["p", "br"])
call("html", "remove_tags_with_content", DOC, which_ones=["script", "style", "b"])
call("html", "remove_tags_with_content", DOC, which_ones=["img", "br"])
call("html", "replace_tags", DOC, " | ")
call("html", "remove_comments", DOC)
call("html", "unquote_markup", DOC)
call("html", "replace_escape_chars", DOC, which_ones=["\n"], replace_by=" ")
call("html", "has_entities", DOC)

PAGE_HEADS = [
    ("<head><base href=\"/root/\"><meta http-equiv=\"refresh\" content=\"2; URL='next.html'\"></head>", "http://site.example/dir/page.html"),
    ("<head><BASE HREF='https://other.example/x/'><meta content=\"0;url=http://other.example/\" http-equiv=Refresh></head>", "http://site.example/"),
    ("<script>document.write('<base href=/fake/>')</script><base href=\"  \">", "http://site.example/a/b"),
    ("<noscript><meta http-equiv=refresh content=\"0;url=/js-off\"></noscript><meta http-equiv=refresh content=\"5\">", "http://site.example/"),
    ("<meta http-equiv=\"refresh\" content=\"0.5;url=café.html\"><base href=café/>", "http://site.example/"),
    ("<meta http-equiv=\"refresh\" content=\"007 ; url = http://x.example/ \">", "http://site.example/"),
    ("<meta http-equiv=\"refresh\" content=\"3.14159265358979323846;url=/pi\">", "http://site.example/"),
    ("<meta http-equiv=\"refresh\" content=\".25;url=/quarter\">", "http://site.example/"),
    ("<meta http-equiv=\"refresh\" content=\"1e3;url=/exp\">", "http://site.example/"),
    ("<meta http-equiv=\"refresh\" content=\"10;url=&quot;/quoted&quot;\">", "http://site.example/"),
]
for text, base in PAGE_HEADS:
    call("html", "get_base_url", text, base)
    call("html", "get_meta_refresh", text, base)
    call("html", "get_meta_refresh", text.encode("utf-8"), base, "utf-8")
    call("html", "get_meta_refresh", text, base, ignore_tags=[])
call("html", "get_base_url", "<base href=\"/ré\">".encode("cp1252"), "http://s.example/", "cp1252")
call("html", "get_meta_refresh", "<meta http-equiv=refresh content=\"0;url=/Привет\">".encode("cp1251"), "http://s.example/", "cp1251")
call("html", "get_meta_refresh", "<meta http-equiv=refresh content=\"0;url=/x\">", "http://s.example/", max_scan=10)
call("html", "get_meta_refresh", "<meta http-equiv=refresh content=\"0;url=/x\">", "http://s.example/", max_scan=0)

for t in [" hello\n", "\t\x0c\r\n x  ", "　wide　"]:
    call("html", "strip_html5_whitespace", t)

for u in ["http://x.example/a?utm_source=nl&id=3&utm_medium=mail&id=4", "http://x.example/?a=1&b=&a=2#top"]:
    call("url", "url_query_cleaner", u, ["utm_source", "utm_medium"], remove=True)
    call("url", "url_query_cleaner", u, "id", unique=False, keep_fragments=True)
    call("url", "url_query_parameter", u, "id")
    call("url", "url_query_parameter", u, "b", "dflt", keep_blank_values=1)
    call("url", "add_or_replace_parameter", u, "id", "9")
    call("url", "add_or_replace_parameters", u, {"z": "ü w", "a": "&"})
    call("url", "safe_download_url", u)
for u in ["http://x.example/files/../../etc/passwd", "http://x.example/a/%2e%2e/%2E./b/./c/", "http://x.example", "http://x.example/a//b/.."]:
    call("url", "safe_download_url", u)
for u in ["www.example.com/x", "//cdn.example.com/y", "example.com", "HTTPS://up.example/", "ftp://f.example", "/relative/path", "mailto:x@y"]:
    call("url", "add_http_if_no_scheme", u)
    if u.startswith("/") or "://" in u:
        call("url", "any_to_uri", u)
    call("url", "is_url", u)
    call("url", "parse_url", u)
call("url", "parse_url", "http://u:p@[::1]:81/p;q?r#s")
call("url", "parse_qsl_to_bytes", "a=1&b=%FF&c+d=e+f&&=x&g", keep_blank_values=True)
call("url", "parse_qsl_to_bytes", "a=1;b=2;c", separator=";")


SITE = {}


def page(url, status, headers, body):
    SITE[url] = (status, headers, body)


page("http://shop.example/", 200, [("Content-Type", "text/html; charset=utf-8"), ("Server", "nginx")], """<!DOCTYPE html>
<html><head><title>Trail &amp; Road | Shop</title>
<link rel="canonical" href="http://shop.example/">
</head><body>
<nav><a href="catalog/?utm_source=nl&amp;id=3&amp;cat=shoes">Shoes</a>
<a href="/catalog/?cat=shoes&id=3">Shoes again</a>
<a href="HTTP://Shop.Example:80/help/./faq/../?b=2&a=1#top">Help</a>
<a href=" /search?q=trail%20shoes ">Search</a>
<a href="&#x2F;about">About</a>
<a href='//cdn.shop.example/img/logo.png'>Logo</a>
<a href="mailto:info@shop.example">Mail</a>
<a href="javascript:void(0)">JS</a>
<a href="https://bücher.example/kaufen?titel=Faust">Bücher</a>
<a href="/ru/">Русский</a> <a href="/fr/">Français</a> <a href="/jp/">日本語</a>
<a href="/old-home">Old home</a> <a href="/blog/">Blog</a> <a href="/admin/">Admin</a>
<a href="/files/../../etc/passwd">sneaky</a> <a href="/missing">Gone</a>
<img src="data:text/plain;base64,SGVsbG8sIHNob3Ah">
</nav></body></html>""".encode("utf-8"))

page("http://shop.example/catalog/?cat=shoes&id=3", 200, [("Content-Type", "text/html")], """<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Catalog</title></head><body>
<a href="?cat=shoes&id=3&page=2">next</a> <a href="item?id=10&amp;color=red&amp;size=">Red</a>
<a href="item?size=&color=red&id=10">Red again</a> <a href="../">up</a>
</body></html>""".encode("utf-8"))

page("http://shop.example/ru/", 200, [("Content-Type", "text/html")], """<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
<title>Магазин — главная</title></head><body>
<a href="/ru/обувь?цвет=красный">Обувь</a> <a href="/ru/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C?%F6%E2%E5%F2=%EA%F0%E0%F1%ED%FB%E9">Обувь (cp1251)</a>
</body></html>""".encode("cp1251"))

page("http://shop.example/fr/", 200, [("Content-Type", "text/html; charset=ISO-8859-1")], """<html><head>
<title>Boutique – café &amp; thé €</title></head><body>
<p>Prix : 12 € “promo”</p>
<a href="/fr/café?q=thé">Café</a>
</body></html>""".encode("cp1252"))

page("http://shop.example/jp/", 200, [("Content-Type", "text/html")], b"\xff\xfe" + """<html><head><title>靴の店</title></head>
<body><a href="/jp/靴?色=赤">靴</a> <a href="http://例え.テスト/">例え</a></body></html>""".encode("utf-16-le"))

page("http://shop.example/old-home", 200, [("Content-Type", "text/html; charset=utf-8")], b"""<html><head>
<meta http-equiv="refresh" content="0; url=/new-home"></head><body>moved</body></html>""")

page("http://shop.example/new-home", 200, [("Content-Type", "application/xhtml+xml")], b"""<?xml version="1.0" encoding="iso-8859-15"?>
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Nouvelle \xa4 maison</title>
<base href="http://static.shop.example/v2/"/></head><body>
<a href="style.css">css</a> <a href="../v1/old.css">old css</a></body></html>""")

page("http://shop.example/blog/", 200, [("Content-Type", "text/html; charset=utf-8")], """<html><head><title>Blog</title>
<base href="/blog/2026/"></head><body>
<!-- <a href="/drafts/">drafts</a> -->
<script>var s = '<a href="/not-a-link">';</script>
<a href="trail-running.html">Trail running</a>
<a href='road?ref=blog&amp;utm_campaign=x'>Road</a>
<a href="/blog/2026/trail-running.html#comments">Comments</a>
</body></html>""".encode("utf-8"))

page("http://shop.example/admin/", 401, [("Content-Type", "text/html"), ("WWW-Authenticate", "Basic realm=\"admin\"")], b"<html><title>Admin</title><a href=\"/admin/orders\">orders</a></html>")


def http_bytes(status, headers, body):
    reason = {200: "OK", 401: "Unauthorized"}[status]
    head = f"HTTP/1.1 {status} {reason}\r\n" + "".join(f"{k}: {v}\r\n" for k, v in headers)
    return head.encode("latin-1") + b"\r\n" + body


def write():
    os.makedirs(os.path.join(DATA, "site"), exist_ok=True)
    with open(os.path.join(DATA, "jobs.jsonl"), "w", encoding="utf-8") as out:
        for line in open(os.path.join(HERE, "calls.jsonl"), encoding="utf-8"):
            out.write(line)
        for e in EXTRA:
            out.write(json.dumps(e, ensure_ascii=False) + "\n")
    index = []
    for i, (url, (status, headers, body)) in enumerate(SITE.items()):
        name = f"r{i:02d}.http"
        index.append(f"{url}\t{name}\n")
        with open(os.path.join(DATA, "site", name), "wb") as f:
            f.write(http_bytes(status, headers, body))
    with open(os.path.join(DATA, "site", "index.tsv"), "w") as f:
        f.write("".join(index))


if __name__ == "__main__":
    write()
