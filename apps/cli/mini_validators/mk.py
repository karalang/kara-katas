# Writes data/: jobs.tsv, the validator calls, the inputs of the signup
# and webhook reports, and tld.txt, the IANA list validators ships.
import hashlib
import json
import os
import random
import shutil

random.seed(128)
os.makedirs("data", exist_ok=True)
shutil.copy(os.path.join("validators", "_tld.txt"), os.path.join("data", "tld.txt"))

jobs = []


def call(name, *args, **kw):
    jobs.append("call\t%s\t%s\t%s" % (name, json.dumps(list(args), ensure_ascii=False),
                                       json.dumps(kw, ensure_ascii=False)))


def section(title):
    jobs.append("== " + title)


# ---------------------------------------------------------------- numbers with check digits

def luhn_digit(body):
    total = 0
    for i, c in enumerate(reversed(body)):
        d = int(c)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return str((10 - total % 10) % 10)


def card(prefix, length):
    body = prefix + "".join(random.choice("0123456789") for _ in range(length - len(prefix) - 1))
    return body + luhn_digit(body)


def iban(country, bban):
    digits = "".join(c if c.isdigit() else str(ord(c) - 55) for c in bban + country + "00")
    return "%s%02d%s" % (country, 98 - int(digits) % 97, bban)


B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58check(payload):
    raw = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(raw, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    pad = len(raw) - len(raw.lstrip(b"\0"))
    return "1" * pad + out


def es_nif(n):
    return "%08d%s" % (n, "TRWAGMYFPDXBNJZSQVHLCKE"[n % 23])


def fi_ssn(ddmmyy, sep, serial):
    marks = "0123456789ABCDEFHJKLMNPRSTUVWXY"
    return "%s%s%03d%s" % (ddmmyy, sep, serial, marks[int(ddmmyy + "%03d" % serial) % 31])


def fr_ssn(g, yy, mm, dep, town, reg):
    d = dep.replace("2A", "19").replace("2B", "18")
    key = 97 - int(g + yy + mm + d + town + reg) % 97
    return "%s %s %s %s %s %s %02d" % (g, yy, mm, dep, town, reg, key)


def ru_inn10(body):
    w = [2, 4, 10, 3, 5, 9, 4, 6, 8]
    c = sum(int(d) * k for d, k in zip(body, w)) % 11 % 10
    return body + str(c)


def ru_inn12(body):
    w1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    c1 = sum(int(d) * k for d, k in zip(body, w1)) % 11 % 10
    w2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    s = body + str(c1)
    c2 = sum(int(d) * k for d, k in zip(s, w2)) % 11 % 10
    return s + str(c2)


# ---------------------------------------------------------------- the calls

section("email")
for v in ["someone@example.com", "first.last+tag@sub.example.co.uk", "bogus@@", "no-at-sign",
          "", "a@b", "user@localhost", "user@[127.0.0.1]", "user@[::1]", "x@-bad.com",
          "x@bad-.com", "x@exa_mple.com", "\"quoted user\"@example.org", "\"bad\"quote\"@example.org",
          "Ž@example.com", "žluťoučký.kůň@example.com", "user.@example.com", ".user@example.com",
          "us..er@example.com", "a" * 64 + "@example.com", "a" * 65 + "@example.com",
          "x@" + "a" * 63 + ".com", "x@" + "a" * 64 + ".com", "x@" + ".".join(["abcdefghi"] * 25) + ".com",
          "user@example.com.", "user@_srv.example.com", "user@example", "UPPER@EXAMPLE.COM",
          "o'brien@example.ie", "user@xn--80ak6aa92e.com", "user@123.123.123.123", "user@ex ample.com",
          "user@example..com", "user@.example.com", "tab\t@example.com", "user@example.c",
          "user@exam!ple.com", "a@b.c0", "a@b.co", "very.common@example.com"]:
    call("email", v)
call("email", "user@[127.0.0.1]", ipv4_address=True)
call("email", "user@[::1]", ipv6_address=True)
call("email", "user@[2001:db8::1]", ipv6_address=True)
call("email", "user@127.0.0.1", ipv4_address=True)
call("email", "user@localhost", simple_host=True)
call("email", "user@example.com.", rfc_1034=True)
call("email", "user@_srv.example.com", rfc_2782=True)
call("email", "user@[300.1.1.1]", ipv4_address=True)

section("domain and hostname")
for v in ["example.com", "example.com/", "xn----gtbspbbmkef.xn--p1ai", "sub.domain.example.org",
          "-start.com", "end-.com", "under_score.com", "_srv.example.com", "a.b", "a.b1", "123.com",
          "com", "example..com", ".example.com", "example.com.", "ex ample.com", "exa__mple.com",
          "a" * 63 + ".com", "a" * 64 + ".com", ".".join(["a" * 60] * 4) + ".com",
          ".".join(["a" * 61] * 4) + ".com", "example.c-m", "example.1om", "EXAMPLE.COM",
          "x.y.z.w.v.u.example.museum", "localhost"]:
    call("domain", v)
call("domain", "example.com.", rfc_1034=True)
call("domain", "_sip._tcp.example.com", rfc_2782=True)
call("domain", "my__srv.example.com", rfc_2782=True)
for v in ["example.com", "example.dev", "example.zzz", "example.onion", "example.ninja", "example.local",
          "example.COM", "example.org.", "example.xn--p1ai"]:
    call("domain", v, consider_tld=True)
for v in ["ubuntu-pc:443", "this-pc", "xn----gtbspbbmkef.xn--p1ai:65535", "_example.com", "123.5.77.88:31000",
          "12.12.12.12", "[::1]:22", "dead:beef:0:0:0:0000:42:1", "[0:0:0:0:0:ffff:1.2.3.4]:-65538",
          "[0:&:b:c:@:e:f::]:9999", "example.com:0", "example.com:65536", "example.com:080",
          "host:1:2", "-pc", "pc-", "a" * 61, "a" * 62, "my_pc", "example.com:99999", "[::1]",
          "::1", "1.2.3.4:5", "256.1.1.1", "pc.", "10.0.0.1"]:
    call("hostname", v)
call("hostname", "this-pc", maybe_simple=False)
call("hostname", "example.com:443", may_have_port=False)
call("hostname", "12.12.12.12", skip_ipv4_addr=True)
call("hostname", "::1", skip_ipv6_addr=True)
call("hostname", "10.0.0.1", private=True)
call("hostname", "10.0.0.1", private=False)
call("hostname", "8.8.8.8:53", private=False)
call("hostname", "pc.", rfc_1034=True)
call("hostname", "example.dev", consider_tld=True)

section("ip addresses")
for v in ["192.168.0.1", "0.0.0.0", "255.255.255.255", "256.0.0.1", "1.2.3", "1.2.3.4.5", "01.2.3.4",
          "1.2.3.04", "1.2.3.0", "١.2.3.4", "1.2.3.4/24", "1.2.3.0/24", "1.2.3.4/33", "1.2.3.4/255.255.255.0",
          "1.2.3.4/0.0.0.255", "1.2.3.4/255.0.255.0", "1.2.3.4/", "/24", "1.2.3.4//24", " 1.2.3.4",
          "1.2.3.4 ", "1.2.3.4/+24", "1.2.3.4/024", "1.2.3.4/２４"]:
    call("ipv4", v)
call("ipv4", "1.2.3.4/24", cidr=False)
call("ipv4", "1.2.3.4", strict=True)
call("ipv4", "1.2.3.4/24", strict=True)
call("ipv4", "1.2.3.4/24", host_bit=False)
call("ipv4", "1.2.3.0/24", host_bit=False)
for v, p in [("10.1.2.3", True), ("10.1.2.3", False), ("8.8.8.8", False), ("8.8.8.8", True),
             ("172.16.5.4", True), ("172.32.5.4", True), ("224.0.0.1", True), ("169.254.1.1", False),
             ("127.0.0.1", True), ("0.0.0.0", True), ("100.64.0.1", True), ("10.0.0.0/8", True)]:
    call("ipv4", v, private=p)
for v in ["::1", "::", "2001:db8::1", "2001:0db8:0000:0000:0000:ff00:0042:8329", "2001:db8::1::2",
          "1:2:3:4:5:6:7:8", "1:2:3:4:5:6:7:8:9", "1:2:3:4:5:6:7::", "::ffff:1.2.3.4", "::ffff:1.2.3.256",
          "fe80::1%eth0", "fe80::1%", "fe80::1%a%b", "2001:db8::/32", "2001:db8::1/32", "2001:db8::1/129",
          "12345::1", "g::1", ":1:2:3:4:5:6:7", "1:2:3:4:5:6:7:", "1::2:3:4:5:6:7:8", "1:2:3:4:5:6:1.2.3.4",
          "1:2:3:4:5:6:7:1.2.3.4", "::1.2.3.4", "1.2.3.4", "", "[::1]", "::1/0", "::1/ 64",
          "fe80::1%eth0/64", "0:0:0:0:0:0:0:0:0"]:
    call("ipv6", v)
call("ipv6", "2001:db8::1/32", host_bit=False)
call("ipv6", "2001:db8::/32", strict=True)
call("ipv6", "2001:db8::", strict=True)
call("ipv6", "2001:db8::/32", cidr=False)

section("url")
for v in ["http://duck.com", "ftp://foobar.dk", "http://10.0.0.1", "http://example.com/\">user@example.com",
          "https://example.com/path?query=1#frag", "https://user:pass@example.com:8080/p", "http://[::1]:8080/",
          "http://[::1]/", "http://[2001:db8::1]", "http://[::1", "http://::1]/", "http://example.com:65536",
          "http://example.com:0", "http://localhost:8000", "http://exa mple.com", "http://example.com/a b",
          "mailto:someone@example.com", "file:///etc/passwd", "file://localhost/etc/hosts", "file://example.com/x",
          "git://github.com/x/y.git", "ssh://git@github.com:22/x/y", "telnet://192.0.2.16:80/", "gopher://x.com",
          "http://", "http://.com", "http://example.com?a=1&b", "http://example.com?a=1&&b=2", "http://example.com?a=",
          "http://example.com?a=1;b=2", "http://example.com?=1", "http://example.com?a=1&b=2;c", "http://example.com?x=;y",
          "http://example.com#a#b", "http://example.com#a b", "http://example.com#{x}", "http://example.com/😀",
          "http://example.com/日本", "http://example.com/^", "http://u@ser@example.com", "http://user:p@ss@example.com",
          "http://us%40er:pw@example.com", "http://a:b:c@example.com", "http://žluť@example.com", "http://user:pa/ss@example.com",
          "http://_srv.example.com", "http://example.com.", "http://1.2.3.4:80", "http://300.1.1.1",
          "HTTP://EXAMPLE.COM", "http://example.com/%zz", "http://[v1.fe]/", "http://[fe80::1%25eth0]/",
          "http://example.com:8080:90/", "https://xn--80ak6aa92e.com/", "http://example.com/?q=%E2%82%AC",
          "http://localhost/", "http://intranet/", "\x01http://example.com", "http://example.com "]:
    call("url", v)
call("url", "http://localhost:8000", simple_host=True)
call("url", "http://intranet/", simple_host=True)
call("url", "http://example.com?a=1&b", strict_query=False)
call("url", "http://10.0.0.1/", private=False)
call("url", "http://10.0.0.1/", private=True)
call("url", "http://8.8.8.8/", private=False)
call("url", "http://[::1]/", skip_ipv6_addr=True)
call("url", "http://10.0.0.1/", skip_ipv4_addr=True)
call("url", "http://example.com:8080/", may_have_port=False)
call("url", "http://example.com./", rfc_1034=True)
call("url", "http://_srv.example.com/", rfc_2782=True)
call("url", "http://example.dev/", consider_tld=True)
call("url", "http://example.zzz/", consider_tld=True)

section("uri")
for v in ["mailto:example@domain.com", "file:path.txt", "file:///path.txt", "ipfs://bafybeigdyrzt", "ipfs:x",
          "magnet:?xt=urn:btih:abc", "tel:+1-816-555-1212", "data:text/plain,hi", "urn:isbn:0451450523",
          "urc:x", "telnet://192.0.2.16:80/", "telnet://user@host.example.com", "telnet://host.example.com/x",
          "telnet://host.example.com?x", "telnet:", "telnet://host name", "https://example.com",
          "httpx://example.com", "news:comp.lang", "", "mailto:bad@@x"]:
    call("uri", v)

section("formats")
for v in ["01:23:45:67:ab:CD", "01-23-45-67-ab-cd", "01:23-45:67:ab:cd", "0123.4567.89ab", "01:23:45:67:ab",
          "01:23:45:67:ab:cg", "", "01:23:45:67:ab:cd\n"]:
    call("mac_address", v)
for v in ["2bc1c94f-0deb-43e9-92a1-4775189ec9f8", "2bc1c94f 0deb-43e9-92a1-4775189ec9f8",
          "{2bc1c94f-0deb-43e9-92a1-4775189ec9f8}", "urn:uuid:2bc1c94f-0deb-43e9-92a1-4775189ec9f8",
          "2bc1c94f0deb43e992a14775189ec9f8", "2BC1C94F-0DEB-43E9-92A1-4775189EC9F8", "2bc1c94f-0deb-43e9-92a1-4775189ec9f",
          "+bc1c94f-0deb-43e9-92a1-4775189ec9f8", "-bc1c94f-0deb-43e9-92a1-4775189ec9f8", " bc1c94f-0deb-43e9-92a1-4775189ec9f8",
          "0xc1c94f-0deb-43e9-92a1-4775189ec9f8", "2bc1_94f-0deb-43e9-92a1-4775189ec9f8", "2bc1__4f-0deb-43e9-92a1-4775189ec9f8",
          "２bc1c94f-0deb-43e9-92a1-4775189ec9f8", "gbc1c94f-0deb-43e9-92a1-4775189ec9f8", "uuid:{2bc1c94f-0deb-43e9-92a1-4775189ec9f8}",
          "--2bc1c94f0deb43e992a14775189ec9f8--"]:
    call("uuid", v)
for v in ["my-slug-2134", "my.slug", "-my-slug", "my--slug", "MySlug", "slug", "", "a-", "ünïcode"]:
    call("slug", v)
for name, n in [("md5", 32), ("sha1", 40), ("sha224", 56), ("sha256", 64), ("sha384", 96), ("sha512", 128)]:
    h = hashlib.new(name, b"kara").hexdigest()
    call(name, h)
    call(name, h.upper())
    call(name, h[:-1])
    call(name, h[:-1] + "g")
call("sha256", "")
for name, v in [("base16", "a3f4B9"), ("base16", "a3f4g9"), ("base16", ""), ("base32", "MFZWIZLTOQ======"),
                ("base32", "MfZW3zLT9Q======"), ("base32", "MFZW=IZL"), ("base58", "14pq6y9H2DLGahPsM4s7ugsNSD2uxpHsJx"),
                ("base58", "0OIl"), ("base64", "Y2hhcmFjdGVyIHNldA=="), ("base64", "cUSECm5YzcXJwP"), ("base64", "YWJj"),
                ("base64", "YWI="), ("base64", "YQ=="), ("base64", "Y==="), ("base64", "YW Jj")]:
    call(name, v)

section("payments")
cards = {"visa": card("4", 16), "mastercard": card("51", 16), "mastercard2": card("2221", 16),
         "amex": card("37", 15), "unionpay": card("62", 16), "diners": card("36", 14), "diners16": card("38", 16),
         "jcb": card("35", 16), "discover": card("6011", 16), "mir": card("2200", 16)}
plain = list(cards.values()) + ["4242424242424242", "4242424242424241", "378282246310005", "5555555555554444",
                                "2223003122003222", "", "abc", "4242 4242 4242 4242", "４２４２４２４２４２４２４２４２", "0", "00"]
for v in plain:
    call("card_number", v)
for brand in ["visa", "mastercard", "amex", "unionpay", "diners", "jcb", "discover", "mir"]:
    for v in plain[:12] + ["４２４２４２４２４２４２４２４２"]:
        call(brand, v)
ibans = [iban("DE", "100500001061045672"), iban("GB", "NWBK60161331926819"), iban("FR", "20041010050500013M02606"),
         iban("NL", "ABNA0417164300"), iban("CH", "0483" + "0000000000000"[:13])]
for v in ibans + ["DE29100500001061045672", "DE29100500001061045671", "de29100500001061045672", "123456",
                  "DE2910050000106104567", "XX00" + "1" * 31, "DE29 1005 0000 1061 0456 72", ""]:
    call("iban", v)
for name, vals in [("cusip", ["037833100", "037833101", "17275R102", "38259P508", "594918104", "68389X10*", "03783310", "0378331OO"]),
                   ("isin", ["US0378331005", "US0378331006", "GB0002634946", "US38259P5089", "AU0000XVGZA3", "US037833100A", "U10378331005", "us0378331005"]),
                   ("sedol", ["0263494", "0263495", "B0YBKJ7", "B0YBKL9", "B0YBKA7", "026349", "02634941", "b0ybkj7"])]:
    for v in vals:
        call(name, v)
btc = [b58check(b"\x00" + bytes(random.randrange(256) for _ in range(20))) for _ in range(3)]
btc += [b58check(b"\x05" + bytes(random.randrange(256) for _ in range(20)))]
for v in btc + ["1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2", "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN3", "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
                "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq", "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx", "bc1qbbbbbbbbbbbbbbb",
                "bc5qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq", "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN0", "1BvBMSEY", ""]:
    call("btc_address", v)
trx = [b58check(b"\x41" + bytes(random.randrange(256) for _ in range(20))) for _ in range(3)]
for v in trx + ["TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYH", "TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZYX", "T" + "1" * 33,
                b58check(b"\x42" + bytes(20)), "TLyqzVGLV1srkB7dToTAEqgDSfPtXRJZY0"]:
    call("trx_address", v)
for v in ["0x9cc14ba4f9f68ca159ea4ebf2c292a14e5d1fa4e", "0x9CC14BA4F9F68CA159EA4EBF2C292A14E5D1FA4E",
          "0x9cc14ba4f9f68ca159ea4ebf2c292a14e5d1fa4", "9cc14ba4f9f68ca159ea4ebf2c292a14e5d1fa4e", "0x9cc14ba4f9f68ca159ea4ebf2c292a14e5d1fa4g"]:
    call("bsc_address", v)

section("ranges and lengths")
call("between", 5, min_val=2)
call("between", 13.2, min_val=13, max_val=14)
call("between", 500, max_val=400)
call("between", 5, min_val=10, max_val=2)
call("between", "m", min_val="a", max_val="z")
call("between", "M", min_val="a", max_val="z")
call("between", 5, min_val="a")
call("between", 5, min_val="a", max_val=3)
call("between", None, min_val=1)
call("between", True, min_val=0, max_val=1)
call("between", 7)
call("between", 2.5, min_val=2.5, max_val=2.5)
call("length", "something", min_val=2)
call("length", "something", min_val=9, max_val=9)
call("length", "something", max_val=5)
call("length", "something", min_val=-1)
call("length", "something", max_val=-3)
call("length", "žluťoučký", min_val=9, max_val=9)
call("length", "a😀b", max_val=3)
call("length", "", min_val=0)
call("length", 12345, min_val=1)
call("length", "x", min_val=3, max_val=1)

section("cron")
for v in ["*/5 * * * *", "30-31 22/2 1-15,20 */2 1-5", "0 0 1 1 7", "60 * * * *", "* 24 * * *", "* * 0 * *",
          "* * * 13 *", "* * * * 8", "*/0 * * * *", "1-60/5 * * * *", "5-1 * * * *", "* * * *", "* * * * * *",
          "  0  12  *  *  1  ", "a * * * *", "1,2,,3 * * * *", "*/x * * * *", "١ * * * *", "0 0 * * 1-1", "0 0 * * -1",
          "", "1-2-3 * * * *", "*/5/2 * * * *", "0\t0　* * *"]:
    call("cron", v)

section("countries and currencies")
for v, kw in [("GB", {"iso_format": "alpha3"}), ("USA", {}), ("840", {"iso_format": "numeric"}), ("iN", {"iso_format": "alpha2"}),
              ("ZWE", {"iso_format": "alpha3"}), ("in", {"ignore_case": True}), ("usa", {"ignore_case": True}), ("usa", {}),
              ("840", {}), ("8400", {}), ("U", {}), ("ÜS", {}), ("US", {"iso_format": "numeric"}), ("US", {"iso_format": "bogus"}),
              ("004", {}), ("4", {}), ("١٢٣", {}), ("ANT", {}), ("XK", {}), ("U1", {})]:
    call("country_code", v, **kw)
for v in ["+91", "-31", "+1", "+1-264", "+44-1481", "+999", "91", ""]:
    call("calling_code", v)
for v, kw in [("USD", {}), ("ZWX", {}), ("usd", {}), ("usd", {"ignore_case": True}), ("$", {}), ("$", {"skip_symbols": False}),
              ("₹", {"skip_symbols": False}), ("Rs", {"skip_symbols": False}), ("৳", {"skip_symbols": False}),
              ("⃀৳", {"skip_symbols": False}), ("EURO", {}), ("XAU", {}), ("BTC", {})]:
    call("currency", v, **kw)

section("national ids")
for v in ["B25162520", "U4839822F", "B44415919", "J99216582", "A12345674", "P1234567D", "Q1234567X", "X1234567A",
          "B2516252", "BX5162520", "C1234567D", "C12345674"]:
    call("es_cif", v)
for n in [26643189, 12345678, 99999999]:
    call("es_nif", es_nif(n))
for v in ["26643189N", "26643189A", "M2812345C", "K1234567L", "L0000000T", "1234567８Z", "12345678²"]:
    call("es_nif", v)
for v in ["X0095892M", "X8095892N", "Y1234567X", "Z1234567R", "A1234567B", ""]:
    call("es_nie", v)
for v in ["X0095892M", "26643189N", "B25162520", "U4839822F", "Q1234567X", "ZZ"]:
    call("es_doi", v)
for v in ["2336509-6", "1234567-1", "0737546-2", "2336509-7", "2336509", "abcdefg-h"]:
    call("fi_business_id", v)
for args in [("131052", "-", 308), ("010101", "A", 2), ("311299", "+", 950), ("290200", "Y", 123), ("010180", "-", 1)]:
    call("fi_ssn", fi_ssn(*args))
call("fi_ssn", fi_ssn("311299", "+", 950), allow_temporal_ssn=False)
for v in ["131052-308T", "131052-308U", "321052-308T", "130052-308T", "131052*308T", "131052-308t"]:
    call("fi_ssn", v)
for v in ["01", "2A", "2B", "20", "95", "96", "971", "976", "977", "0", "abc", " 75 ", "７５", "+3"]:
    call("fr_department", v)
call("fr_department", 75)
call("fr_department", 0)
call("fr_department", 974)
for args in [("1", "84", "12", "76", "451", "089"), ("2", "70", "01", "2A", "123", "456"), ("1", "55", "05", "971", "12", "345"),
             ("2", "99", "12", "99", "123", "456")]:
    call("fr_ssn", fr_ssn(*args))
for v in ["1 84 12 76 451 089", "1 84 12 76 451 089 47", "3 84 12 76 451 089", "1 84 13 76 451 089", "1 84 12 20 451 089",
          "1 55 05 971 123 345", "1841276451089", "1 84 12 76 451 089 00"]:
    call("fr_ssn", v)
for v in ["3675 9834 6012", "5046 3182 4299", "1234 5678 9012", "367598346012", "3675 9834 601", "３６７５ ９８３４ ６０１２"]:
    call("ind_aadhar", v)
for v in ["ABCDE9999K", "abcde9999k", "ABCD99999K", "ABCDE9999KZ"]:
    call("ind_pan", v)
for v in [ru_inn10("770708389"), ru_inn10("500100732"), ru_inn12("7707083893"), ru_inn12("5001007329"),
          "7830002293", "7830002294", "500100732259", "500100732258", "123", "77070838930", "77О7083893", ""]:
    call("ru_inn", v)

# ---------------------------------------------------------------- the reports

first = ["ana", "bo", "chen", "dmitri", "eva", "farid", "gita", "hugo", "ines", "jon", "kai", "lena", "žofie", "o'neil"]
domains = ["example.com", "mail.example.org", "corp.example.co.uk", "localhost", "exa_mple.com", "example", "xn--80ak6aa92e.com"]
sites = ["https://ana.dev", "http://bo.example.com/blog", "ftp://files.example.net", "http://localhost:3000",
         "https://example.com/ü", "javascript:alert(1)", "https://[::1]/", "https://chen.example.com?x=1&y", "", "http://10.1.1.1/"]
ccs = ["US", "DE", "GB", "IN", "FI", "XX", "us", "DEU", "FR", "ES"]
signups = []


def sometimes_bad(good, bad):
    return random.choice(bad) if random.random() < 0.12 else good


for k in range(40):
    name = random.choice(first)
    clean = name.replace("'", "")
    mail = clean + sometimes_bad(random.choice(["", ".x", "+news"]), ["..", "@", " "]) + "@" + \
        sometimes_bad(random.choice(domains[:3] + domains[6:]), domains[3:6])
    site = sometimes_bad(random.choice(sites[:3] + [""]), sites[3:])
    user = sometimes_bad(random.choice([name, name + "-" + str(k)]), [name.upper(), "-" + name, name + "_x"]).replace("'", "")
    cc = sometimes_bad(random.choice(ccs[:5] + ccs[8:]), ccs[5:8])
    brand = random.choice(["4", "51", "37", "35", "6011", "2200"])
    cardno = sometimes_bad(card(brand, 15 if brand == "37" else 16), ["4242424242424241", "1234", "", "４２４２４２４２４２４２４２４２"])
    acct = sometimes_bad(random.choice(ibans + [""]), ["DE29100500001061045671", "GB00NWBK60161331926819"])
    ip = sometimes_bad(random.choice(["203.0.113.7", "10.0.0.8", "192.168.1.20", "2001:db8::7", "8.8.4.4"]), ["999.1.1.1", "1.2.3", "::g"])
    signups.append([str(1000 + k), user, mail, site, cc, cardno, acct, ip])
with open("data/signups.tsv", "w", encoding="utf-8") as f:
    f.write("# id\tusername\temail\twebsite\tcountry\tcard\tiban\tsignup ip\n")
    for r in signups:
        f.write("\t".join(r) + "\n")

hooks = ["https://hooks.example.com/in/abc", "http://127.0.0.1:8080/admin", "http://10.0.0.5/hook", "https://8.8.8.8/x",
         "http://169.254.169.254/latest/meta-data/", "http://[::1]/hook", "https://api.partner.example.net:8443/cb?sig=1",
         "http://localhost/hook", "https://172.20.1.1/x", "https://172.40.1.1/x", "https://user:pw@example.com/cb",
         "gopher://example.com/x", "https://example.com/cb?a=1&b", "https://exa mple.com/cb", "https://224.0.0.5/x",
         "https://example.com:99999/cb", "https://example.zzz/cb", "https://sub.example.org/cb#frag"]
with open("data/webhooks.tsv", "w", encoding="utf-8") as f:
    f.write("# tenant\tcallback url\n")
    for k, h in enumerate(hooks):
        f.write("tenant-%02d\t%s\n" % (k + 1, h))

jobs.append("== signup form")
jobs.append("signups\tsignups.tsv")
jobs.append("== webhook callbacks")
jobs.append("webhooks\twebhooks.tsv")

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    f.write("\n".join(jobs) + "\n")
