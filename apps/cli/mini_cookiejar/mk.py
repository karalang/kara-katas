# Writes data/: jobs.tsv (the jar jobs), three cookie files in each of
# the Netscape (cookies.txt) and LWP formats, some of them broken, and
# the exchanges for the two programs. Run it from the app directory.
#
# jobs.tsv, one op per line, fields split by tabs:
#   job NAME                      start a job
#   now T                         the clock (time.time()) from here on
#   jar KIND [key=value...]       a new jar (cookie, lwp or mozilla) with a
#                                 DefaultCookiePolicy; keys are its
#                                 arguments, lists split by commas
#   set URL [OPT...] HEADER...    extract_cookies from a response with those
#                                 headers, for a request to URL
#   get URL [OPT...] [HEADER...]  add_cookie_header to a request for URL
#                                 OPT is origin=HOST or unverifiable=1
#   list | repr | len
#   clear [DOMAIN [PATH [NAME]]] | clear_session | clear_expired
#   save FILE D E | load FILE D E | revert FILE D E
#                                 FILE "-" means none; D and E are
#                                 ignore_discard and ignore_expires
#   fn NAME ARG...                one of the module's functions
import os

jobs = []


def job(name, *ops):
    jobs.append(["job", name])
    for op in ops:
        jobs.append(list(op))


job("dates",
    ("now", "1700000000"),
    ("fn", "http2time", "Wed, 09 Feb 1994 22:23:32 GMT"),
    ("fn", "http2time", "Thursday, 03-Feb-94 00:00:00 GMT"),
    ("fn", "http2time", "03-Feb-30"),
    ("fn", "http2time", "03-Feb-76"),
    ("fn", "http2time", "08-Feb-1994 14:15:29 -0500"),
    ("fn", "http2time", "08-Feb-1994 14:15:29 +05:30"),
    ("fn", "http2time", "08-Feb-1994 14:15:29 +5"),
    ("fn", "http2time", "  Mon,03 Feb 1994 10:00 UT"),
    ("fn", "http2time", "9 Feb 1994 22:23:32 EST"),
    ("fn", "http2time", "09-Feb-1994 22:23 (CET)"),
    ("fn", "http2time", "09/Feb/1994:22:23:32 +0100"),
    ("fn", "http2time", "9 2 1994"),
    ("fn", "http2time", "9 13 1994"),
    ("fn", "http2time", "31 Feb 2024"),
    ("fn", "http2time", "28 Feb 2023 24:00:61"),
    ("fn", "http2time", "Feb 09 1994"),
    ("fn", "http2time", "09 Feb 94 3:30 PM"),
    ("fn", "http2time", "1994-02-09"),
    ("fn", "http2time", "1 Jan 1969"),
    ("fn", "http2time", "1 Jan 12345"),
    ("fn", "http2time", "Sun, 06 Jxx 1994 08:49:37 GMT"),
    ("fn", "http2time", "Sun, 06 Nov 1994 08:49:37 gmt"),
    ("fn", "http2time", "Sunday,06-Nov-94 08:49:37"),
    ("fn", "http2time", ""),
    ("fn", "iso2time", "1994-02-03 14:15:29 -0100"),
    ("fn", "iso2time", "1994-02-03T14:15:29Z"),
    ("fn", "iso2time", "19940203T141529Z"),
    ("fn", "iso2time", "1994-02-03"),
    ("fn", "iso2time", "1994-02-03 14:15:29 +05:30"),
    ("fn", "iso2time", "1994-02-03 14:15:29.5Z"),
    ("fn", "iso2time", "94-02-03"),
    ("fn", "time2isoz", "784111777"),
    ("fn", "time2isoz", "0"),
    ("fn", "time2netscape", "784111777"),
    ("fn", "time2netscape", "2000000000"),
    )

job("headers",
    ("fn", "split_header_words", 'foo="bar"; port="80,81"; discard, bar=baz'),
    ("fn", "split_header_words", 'text/html; charset="iso-8859-1"'),
    ("fn", "split_header_words", r'Basic realm="\"foo\bar\""'),
    ("fn", "split_header_words", "a, b", "c=1;;d = 2 ;  e"),
    ("fn", "split_header_words", "=junk; x=; y=\"open"),
    ("fn", "split_header_words", ",, ,"),
    ("fn", "join_header_words", 'foo="bar"; port="80,81"; discard, bar=baz'),
    ("fn", "join_header_words", r'Basic realm="\"foo\bar\""; x="a b"; y=c/d'),
    ("fn", "parse_ns_headers", "foo=bar; Path=/; Domain=.example.com; Expires=Wed, 09 Feb 1994 22:23:32 GMT; secure; HttpOnly"),
    ("fn", "parse_ns_headers", "=novalue; path=/"),
    ("fn", "parse_ns_headers", "a=b; ; =c; Version=\"1\"; MAX-AGE=60"),
    ("fn", "parse_ns_headers", "lone; expires=\"09-Nov-2033 23:12:40 GMT\"; expires=never"),
    ("fn", "parse_ns_headers", "q=\"quoted; still\"; Comment=hi", "second=2"),
    )

job("domains",
    ("fn", "domain_match", "www.example.com", ".example.com"),
    ("fn", "domain_match", "example.com", ".example.com"),
    ("fn", "domain_match", "a.b.example.com", ".example.com"),
    ("fn", "domain_match", "WWW.Example.COM", "www.example.com"),
    ("fn", "domain_match", "192.168.1.1", ".168.1.1"),
    ("fn", "domain_match", "www.example.com", "example.com"),
    ("fn", "domain_match", "x.y.com", ".com"),
    ("fn", "user_domain_match", "ads.tracker.net", ".tracker.net"),
    ("fn", "user_domain_match", "tracker.net", ".tracker.net"),
    ("fn", "user_domain_match", "10.0.0.1", "10.0.0.1"),
    ("fn", "user_domain_match", "10.0.0.1", ".0.0.1"),
    ("fn", "is_HDN", "example.com"),
    ("fn", "is_HDN", "10.0.0.1"),
    ("fn", "is_HDN", ".example.com"),
    ("fn", "is_HDN", "host9"),
    ("fn", "reach", "www.acme.com"),
    ("fn", "reach", "acme.com"),
    ("fn", "reach", "foo.local"),
    ("fn", "reach", "192.168.0.1"),
    ("fn", "escape_path", "/foo/bar baz/%7e%2fx"),
    ("fn", "escape_path", "/café/a;b=c?d"),
    )

job("netscape cookies",
    ("now", "1700000000"),
    ("jar", "cookie"),
    ("set", "http://www.acme.com/acme/login", "Set-Cookie: CUSTOMER=WILE_E_COYOTE; path=/; expires=Wed, 09-Nov-2033 23:12:40 GMT"),
    ("get", "http://www.acme.com/acme/ammo"),
    ("set", "http://www.acme.com/acme/pickitem", "Set-Cookie: PART_NUMBER=ROCKET_LAUNCHER_0001; path=/"),
    ("set", "http://www.acme.com/acme/shipping", "Set-Cookie: SHIPPING=FEDEX; path=/foo"),
    ("get", "http://www.acme.com/"),
    ("get", "http://www.acme.com/foo/bar"),
    ("set", "http://www.acme.com/acme/login", "Set-Cookie: sid=s1; Domain=acme.com", "Set-Cookie: lang=en"),
    ("get", "http://api.acme.com/acme/x"),
    ("get", "http://www.acme.com/acme/x", "Cookie: preset=1"),
    ("set", "http://www.acme.com/", "Set-Cookie: tld=1; Domain=.com", "Set-Cookie: other=1; Domain=other.org", "Set-Cookie: dots=1; domain=.www.acme.com"),
    ("set", "https://shop.acme.com/cart", "Set-Cookie: cart=3; Secure; HttpOnly; Path=/cart", "Set-Cookie: flag", "Set-Cookie: dup=first; path=/; path=/ignored"),
    ("get", "http://shop.acme.com/cart"),
    ("get", "https://shop.acme.com/cart/checkout"),
    ("set", "http://www.acme.com/", "Set-Cookie: bad=1; Max-Age=soon", "Set-Cookie: short=1; Max-Age=60; Expires=Wed, 09-Nov-2033 23:12:40 GMT"),
    ("set", "http://www.acme.com/", "Set-Cookie: PART_NUMBER=gone; path=/; Max-Age=0"),
    ("set", "http://www.acme.com/acme/", "Set-Cookie: SHIPPING=x; path=/foo; expires=Thu, 01 Jan 1970 00:00:00 GMT"),
    ("list",),
    ("len",),
    ("now", "1700000100"),
    ("get", "http://www.acme.com/"),
    ("list",),
    ("repr",),
    ("clear", "www.acme.com", "/"),
    ("clear", "nowhere.com"),
    ("clear", ".acme.com", "/", "nope"),
    ("clear_session",),
    ("list",),
    )

job("rfc 2965",
    ("now", "1700000000"),
    ("jar", "cookie", "rfc2965=1"),
    ("set", "http://www.acme.com/acme/login", 'Set-Cookie2: Customer="WILE_E_COYOTE"; Version="1"; Path="/acme"'),
    ("get", "http://www.acme.com/acme/pickitem"),
    ("set", "http://www.acme.com/acme/pickitem", 'Set-Cookie2: Part_Number="Rocket Launcher 0001"; Version="1"; Path="/acme"'),
    ("set", "http://www.acme.com/acme/shipping", 'Set-Cookie2: Shipping="FedEx"; Version="1"; Path="/acme"; Port="80,8080"', "Set-Cookie: Shipping=old; path=/acme", "Set-Cookie: legacy=1; path=/"),
    ("get", "http://www.acme.com/acme/process"),
    ("get", "http://www.acme.com:8080/acme/process"),
    ("get", "http://www.acme.com:81/acme/process"),
    ("set", "http://www.acme.com/acme/", 'Set-Cookie2: nover=1; Path="/acme"', 'Set-Cookie2: wrongpath=1; Version=1; Path="/other"', 'Set-Cookie2: nodot=1; Version=1; Domain=".com"', 'Set-Cookie2: prefix=1; Version=1; Domain=".acme.com"'),
    ("set", "http://a.b.acme.com/", 'Set-Cookie2: deep=1; Version=1; Domain=".acme.com"', 'Set-Cookie2: portless=1; Version=1; Port'),
    ("set", "http://www.acme.com/", "Set-Cookie: v1=\"a b\"; Version=1; Path=/"),
    ("get", "http://www.acme.com/acme/x"),
    ("repr",),
    ("jar", "cookie"),
    ("set", "http://www.acme.com/", "Set-Cookie: v1=\"a b\"; Version=1; Path=/", 'Set-Cookie2: ignored=1; Version="1"'),
    ("get", "http://www.acme.com/"),
    ("repr",),
    )

job("policies",
    ("now", "1700000000"),
    ("jar", "cookie", "blocked_domains=.doubleclick.net,ads.acme.com", "strict_ns_unverifiable=1"),
    ("set", "http://ad.doubleclick.net/pixel", "origin=www.news.com", "unverifiable=1", "Set-Cookie: id=1; Domain=.doubleclick.net"),
    ("set", "http://ads.acme.com/x", "Set-Cookie: id=2"),
    ("set", "http://cdn.widgets.io/w.js", "origin=www.news.com", "unverifiable=1", "Set-Cookie: w=1"),
    ("set", "http://img.news.com/a.png", "origin=www.news.com", "unverifiable=1", "Set-Cookie: img=1; Domain=.news.com"),
    ("set", "http://www.news.com/", "Set-Cookie: $dollar=1", "Set-Cookie: page=1"),
    ("list",),
    ("jar", "cookie", "allowed_domains=.news.com", "strict_ns_set_initial_dollar=1", "strict_ns_set_path=1"),
    ("set", "http://www.news.com/a/b", "Set-Cookie: $dollar=1", "Set-Cookie: p=1; path=/a", "Set-Cookie: q=1; path=/z", "Set-Cookie: r=1"),
    ("set", "http://www.blog.org/", "Set-Cookie: s=1"),
    ("list",),
    ("jar", "cookie", "strict_domain=1", "strict_ns_domain=3"),
    ("set", "http://www.bbc.co.uk/", "Set-Cookie: cc=1; Domain=.co.uk", "Set-Cookie: bbc=1; Domain=.bbc.co.uk", "Set-Cookie: host=1"),
    ("set", "http://a.www.example.com/", "Set-Cookie: deep=1; Domain=.example.com"),
    ("get", "http://news.bbc.co.uk/"),
    ("get", "http://www.bbc.co.uk/"),
    ("list",),
    ("jar", "cookie", "netscape=0"),
    ("set", "http://www.acme.com/", "Set-Cookie: off=1"),
    ("len",),
    ("jar", "cookie", "secure_protocols=https"),
    ("set", "wss://chat.acme.com/socket", "Set-Cookie: ws=1; Secure"),
    ("get", "wss://chat.acme.com/socket"),
    ("get", "https://chat.acme.com/socket"),
    ("jar", "cookie"),
    ("set", "http://localhost:8000/app", "Set-Cookie: dev=1", "Set-Cookie: dom=1; Domain=localhost", "Set-Cookie: loc=1; Domain=.localhost.local"),
    ("get", "http://localhost:9000/app/x"),
    ("set", "http://192.168.1.20/", "Set-Cookie: ip=1", "Set-Cookie: ipdom=1; Domain=.168.1.20"),
    ("get", "http://192.168.1.20/"),
    ("list",),
    )

job("files",
    ("now", "1700000000"),
    ("jar", "mozilla"),
    ("load", "data/cookies.txt", "0", "0"),
    ("list",),
    ("save", "work/out.txt", "0", "0"),
    ("save", "work/all.txt", "1", "1"),
    ("get", "https://www.example.com/cart/1"),
    ("jar", "mozilla"),
    ("load", "data/cookies.txt", "1", "1"),
    ("len",),
    ("clear_expired",),
    ("len",),
    ("load", "data/not_cookies.txt", "0", "0"),
    ("load", "data/nope.txt", "0", "0"),
    ("save", "-", "0", "0"),
    ("jar", "mozilla"),
    ("load", "data/bad_cookies.txt", "1", "1"),
    ("list",),
    ("revert", "data/bad_cookies.txt", "1", "1"),
    ("list",),
    ("revert", "data/cookies.txt", "0", "0"),
    ("list",),
    ("jar", "lwp"),
    ("set", "http://www.acme.com/app/login", "Set-Cookie: sid=\"a b\"; path=/app; HttpOnly", "Set-Cookie: lang=en; Domain=.acme.com; Max-Age=86400; Comment=prefs", "Set-Cookie: tok=1; port=80; Expires=Wed, 09-Nov-2033 23:12:40 GMT"),
    ("save", "work/acme.lwp", "1", "0"),
    ("save", "work/acme2.lwp", "0", "0"),
    ("jar", "lwp"),
    ("load", "work/acme.lwp", "1", "0"),
    ("repr",),
    ("load", "data/session.lwp", "0", "0"),
    ("list",),
    ("load", "data/bad.lwp", "1", "1"),
    ("load", "data/cookies.txt", "0", "0"),
    ("jar", "mozilla"),
    ("load", "data/session.lwp", "0", "0"),
    )

cookies_txt = (
    "# Netscape HTTP Cookie File\n"
    "# https://curl.se/docs/http-cookies.html\n"
    "# This file was generated by libcurl! Edit at your own risk.\n"
    "\n"
    ".example.com\tTRUE\t/\tFALSE\t2000000000\ttheme\tdark\n"
    "#HttpOnly_.example.com\tTRUE\t/\tTRUE\t2000000000\tsession\tabc123\n"
    "www.example.com\tFALSE\t/cart\tFALSE\t0\tcart\t3-items\n"
    ".example.com\tTRUE\t/\tFALSE\t1600000000\told\texpired\n"
    "api.example.com\tFALSE\t/\tFALSE\t2000000000\t\tflagonly\n"
    "   \n"
    "$ignored\tline\n"
    "www.example.com\tFALSE\t/\tFALSE\t\tempty\t\n"
)

bad_cookies_txt = (
    "# HTTP Cookie File\n"
    ".example.com\tTRUE\t/\tFALSE\t2000000000\tfirst\t1\n"
    "example.org\tTRUE\t/\tFALSE\t2000000000\tsecond\t2\n"
    ".example.com\tTRUE\t/\tFALSE\t2000000000\tthird\t3\n"
)

not_cookies_txt = "{\"cookies\": []}\n"

session_lwp = (
    "#LWP-Cookies-2.0\n"
    "Set-Cookie3: lang=en; path=\"/\"; domain=\".acme.com\"; path_spec; domain_dot; expires=\"2033-05-18 03:33:20Z\"; version=0\n"
    "# a comment line is skipped\n"
    "Set-Cookie3: cart=\"3 items\"; path=\"/shop\"; domain=\"shop.acme.com\"; path_spec; discard; HttpOnly=None; version=0\n"
    "Set-Cookie3: old=1; path=\"/\"; domain=\".acme.com\"; expires=\"2020-01-01 00:00:00Z\"; version=0\n"
    "Set-Cookie3: v1=x; path=\"/\"; domain=\"www.acme.com\"; port=\"80,8080\"; port_spec; secure; expires=\"20330518T033320Z\"; Comment=\"x\"; version=1\n"
)

bad_lwp = (
    "#LWP-Cookies-2.0\n"
    "Set-Cookie3: ok=1; path=\"/\"; domain=\".acme.com\"; expires=\"2033-05-18 03:33:20Z\"; version=0\n"
    "Set-Cookie3: frac=1; path=\"/\"; domain=\".acme.com\"; expires=\"2033-05-18 03:33:20.5Z\"; version=0\n"
)

# The login program: a request to each URL, then the response's headers.
session = [
    ["GET", "https://shop.example.com/"],
    ["RESP", "Set-Cookie: visitor=v-1001; Domain=example.com; Path=/; Expires=Fri, 01 Jan 2038 00:00:00 GMT",
     "Set-Cookie: csrftoken=t-7; Path=/; Secure"],
    ["GET", "https://shop.example.com/login"],
    ["RESP", "Set-Cookie: sessionid=s-42; Path=/; Secure; HttpOnly",
     "Set-Cookie: csrftoken=t-8; Path=/; Secure"],
    ["GET", "https://shop.example.com/account/orders"],
    ["RESP", "Set-Cookie: recent=o-9,o-8; Path=/account; Max-Age=3600"],
    ["GET", "http://shop.example.com/account/orders"],
    ["RESP"],
    ["SAVE", "work/session.txt"],
    ["RESTART"],
    ["GET", "https://shop.example.com/account/orders"],
    ["RESP", "Set-Cookie: sessionid=; Path=/; Max-Age=0"],
    ["GET", "https://shop.example.com/"],
    ["RESP"],
]

# The audit program: a page and what it pulls in from other hosts.
audit = [
    ["www.news.com", "http://www.news.com/", "Set-Cookie: edition=uk", "Set-Cookie: consent=0; Max-Age=31536000"],
    ["www.news.com", "http://img.news.com/logo.png", "Set-Cookie: cdn=a; Domain=.news.com"],
    ["www.news.com", "http://ad.doubleclick.net/pixel", "Set-Cookie: IDE=x1; Domain=.doubleclick.net; Max-Age=600"],
    ["www.news.com", "http://cdn.widgets.io/w.js", "Set-Cookie: wid=9"],
    ["www.news.com", "http://stats.news.com/hit", "Set-Cookie: hit=1; Domain=.stats.news.com"],
    ["www.shop.com", "http://www.shop.com/", "Set-Cookie: basket=0"],
    ["www.shop.com", "http://pixel.tracker.net/p", "Set-Cookie: tid=5; Domain=.tracker.net"],
]

os.makedirs("data", exist_ok=True)


def write(path, text):
    with open(path, "w", newline="") as f:
        f.write(text)


write("data/jobs.tsv", "".join("\t".join(line) + "\n" for line in jobs))
write("data/cookies.txt", cookies_txt)
write("data/bad_cookies.txt", bad_cookies_txt)
write("data/not_cookies.txt", not_cookies_txt)
write("data/session.lwp", session_lwp)
write("data/bad.lwp", bad_lwp)
write("data/session.tsv", "".join("\t".join(line) + "\n" for line in session))
write("data/audit.tsv", "".join("\t".join(line) + "\n" for line in audit))
