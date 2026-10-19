# Writes data/: the two scripts the run reads.
#
# data/stories.txt is a set of HTTP/2 connections, each with its own
# Encoder and Decoder: the header lists a browser, an API client and a
# server send, with the SETTINGS changes that resize the table. Lines:
#   story <title>
#   huffman on|off            how the encoder writes literals
#   encoder-table <n>         Encoder.header_table_size = n
#   decoder-table <n>         Decoder.header_table_size = n
#   decoder-max <n>           Decoder.max_allowed_table_size = n
#   decoder-list-max <n>      Decoder.max_header_list_size = n
#   block <label>             a header list, given as a list of tuples
#   dict <label>              a header list, given as a dict
#   h <name>\t<value>         a header
#   s <name>\t<value>         a sensitive header (NeverIndexedHeaderTuple)
#   end
#
# data/vectors.txt is a set of header blocks for a Decoder alone: the
# RFC 7541 Appendix C examples, hpack's own test blocks and malformed
# ones. Lines:
#   case <title>
#   decoder-table / decoder-max / decoder-list-max <n>
#   hex <bytes>               one header block, decoded in order
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

UA_FIREFOX = "Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0"
UA_SAFARI = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/17.6 Safari/605.1.15")
ACCEPT_HTML = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"


def block(kind, label, headers):
    out = [f"{kind} {label}"]
    for h in headers:
        sens = len(h) > 2 and h[2]
        out.append(("s " if sens else "h ") + h[0] + "\t" + h[1])
    out.append("end")
    return out


def stories():
    s = []

    s.append("story RFC 7541 C.3: requests without Huffman coding")
    s.append("huffman off")
    reqs = [
        [(":method", "GET"), (":scheme", "http"), (":path", "/"), (":authority", "www.example.com")],
        [(":method", "GET"), (":scheme", "http"), (":path", "/"), (":authority", "www.example.com"),
         ("cache-control", "no-cache")],
        [(":method", "GET"), (":scheme", "https"), (":path", "/index.html"),
         (":authority", "www.example.com"), ("custom-key", "custom-value")],
    ]
    for i, r in enumerate(reqs):
        s += block("block", f"C.3.{i + 1}", r)

    s.append("story RFC 7541 C.4: requests with Huffman coding")
    s.append("huffman on")
    for i, r in enumerate(reqs):
        s += block("block", f"C.4.{i + 1}", r)

    resps = [
        [(":status", "302"), ("cache-control", "private"), ("date", "Mon, 21 Oct 2013 20:13:21 GMT"),
         ("location", "https://www.example.com")],
        [(":status", "307"), ("cache-control", "private"), ("date", "Mon, 21 Oct 2013 20:13:21 GMT"),
         ("location", "https://www.example.com")],
        [(":status", "200"), ("cache-control", "private"), ("date", "Mon, 21 Oct 2013 20:13:22 GMT"),
         ("location", "https://www.example.com"), ("content-encoding", "gzip"),
         ("set-cookie", "foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1")],
    ]
    for huff, sec in (("off", "C.5"), ("on", "C.6")):
        s.append(f"story RFC 7541 {sec}: responses, table of 256, Huffman {huff}")
        s.append(f"huffman {huff}")
        s.append("encoder-table 256")
        s.append("decoder-table 256")
        for i, r in enumerate(resps):
            s += block("block", f"{sec}.{i + 1}", r)

    s.append("story a browser loads a shop's home page")
    s.append("huffman on")
    base = [(":method", "GET"), (":scheme", "https"), (":authority", "shop.example.net")]
    common = [("user-agent", UA_FIREFOX), ("accept-language", "en-GB,en;q=0.7,fr;q=0.3"),
              ("accept-encoding", "gzip, deflate, br, zstd")]
    s += block("block", "GET /", base + [(":path", "/")] + [
        ("accept", ACCEPT_HTML)] + common + [
        ("upgrade-insecure-requests", "1"), ("sec-fetch-dest", "document"),
        ("sec-fetch-mode", "navigate"), ("sec-fetch-site", "none"), ("priority", "u=0, i")])
    cookie = "cart=3 items; theme=dark; consent=analytics:no"
    subs = [
        ("/static/css/site.4f1a.css", "text/css,*/*;q=0.1", "style", "u=2"),
        ("/static/js/app.9c03.js", "*/*", "script", "u=1"),
        ("/static/img/logo.svg", "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
         "image", "u=5, i"),
        ("/static/img/hero-autumn.webp", "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
         "image", "u=5, i"),
        ("/api/v2/cart", "application/json", "empty", "u=4"),
        ("/api/v2/recommendations?limit=8&locale=en-GB", "application/json", "empty", "u=4"),
        ("/static/fonts/inter-var.woff2", "application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8",
         "font", "u=2"),
        ("/favicon.ico", "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
         "image", "u=6"),
    ]
    for path, acc, dest, prio in subs:
        s += block("block", f"GET {path}", base + [(":path", path), ("accept", acc)] + common + [
            ("referer", "https://shop.example.net/"), ("cookie", cookie), ("sec-fetch-dest", dest),
            ("sec-fetch-mode", "no-cors" if dest in ("style", "script", "image") else "cors"),
            ("sec-fetch-site", "same-origin"), ("priority", prio)])

    s.append("story the shop's server answers")
    s.append("huffman on")
    s.append("encoder-table 2048")
    s.append("decoder-table 2048")
    date = "Sat, 19 Oct 2024 09:41:{:02d} GMT"
    sec = [("strict-transport-security", "max-age=63072000; includeSubDomains; preload"),
           ("x-content-type-options", "nosniff"), ("server", "envoy")]
    s += block("block", "200 /", [(":status", "200"), ("date", date.format(3)),
                                  ("content-type", "text/html; charset=utf-8"), ("content-length", "48213"),
                                  ("cache-control", "no-cache"),
                                  ("set-cookie", "visit=first; Path=/; Max-Age=1800; Secure; HttpOnly; SameSite=Lax"),
                                  ("vary", "Accept-Encoding"), ("content-encoding", "br")] + sec)
    files = [("200", "text/css", "18337", "\"4f1a-1912bd\"", "public, max-age=31536000, immutable"),
             ("200", "application/javascript", "203111", "\"9c03-8f2e11\"", "public, max-age=31536000, immutable"),
             ("304", "", "", "\"logo-v7\"", "public, max-age=86400"),
             ("200", "image/webp", "381560", "\"hero-0912\"", "public, max-age=604800"),
             ("200", "application/json", "212", "", "private, no-store"),
             ("404", "application/json", "61", "", "private, no-store"),
             ("200", "font/woff2", "348960", "\"inter-4.0\"", "public, max-age=31536000, immutable"),
             ("503", "text/plain", "19", "", "no-store")]
    for i, (status, ctype, clen, etag, cc) in enumerate(files):
        h = [(":status", status), ("date", date.format(4 + i))]
        if ctype:
            h.append(("content-type", ctype))
        if clen:
            h.append(("content-length", clen))
        if etag:
            h.append(("etag", etag))
        h.append(("cache-control", cc))
        if status == "503":
            h.append(("retry-after", "120"))
        h += sec
        s += block("block", f"{status} {subs[i][0]}", h)

    s.append("story an API client with credentials")
    s.append("huffman on")
    for i, (meth, path) in enumerate([("POST", "/v1/orders"), ("GET", "/v1/orders/7731"),
                                      ("GET", "/v1/orders/7731"), ("DELETE", "/v1/orders/7731/hold")]):
        h = [(":method", meth), (":scheme", "https"), (":authority", "api.example.org"), (":path", path),
             ("authorization", "Bearer demo-token-for-docs-only", True),
             ("x-request-id", f"req-{1000 + i}"), ("user-agent", "orders-cli/2.3.1 python-httpx/0.27"),
             ("accept", "application/json")]
        if meth == "POST":
            h += [("content-type", "application/json"), ("content-length", "88"),
                  ("idempotency-key", "a7c1-orders-0001", True)]
        s += block("block", f"{meth} {path}", h)
    # A header first sent as indexable and then marked sensitive is still
    # sent from the table: the encoder finds the perfect match first.
    s += block("block", "a sensitive header already in the table",
               [(":method", "GET"), (":scheme", "https"), (":authority", "api.example.org"),
                (":path", "/v1/whoami"), ("x-request-id", "req-1003", True),
                ("cookie", "region=eu-west", True), ("cookie", "region=eu-west")])

    s.append("story SETTINGS resize the table mid-connection")
    s.append("huffman off")
    s += block("block", "fill the table", [(":method", "GET"), (":scheme", "https"),
                                           (":authority", "cdn.example.com"), (":path", "/a.js"),
                                           ("x-cache-key", "a" * 40), ("x-trace", "t-0001-aaaa")])
    s.append("encoder-table 128")
    s.append("decoder-table 128")
    s += block("block", "after shrinking to 128", [(":method", "GET"), (":scheme", "https"),
                                                     (":authority", "cdn.example.com"), (":path", "/b.js"),
                                                     ("x-trace", "t-0001-aaaa")])
    s.append("encoder-table 0")
    s.append("encoder-table 64")
    s.append("encoder-table 4096")
    s += block("block", "after 0, 64 and 4096 in one SETTINGS round",
               [(":method", "GET"), (":scheme", "https"), (":authority", "cdn.example.com"), (":path", "/c.js")])
    # hpack's maxsize setter overwrites `resized`, so a second change back
    # to the same size hides the pending update until the next real one.
    s.append("encoder-table 512")
    s.append("encoder-table 512")
    s += block("block", "a change to 512, then 512 again", [(":method", "GET"), (":path", "/d.js")])
    s.append("encoder-table 1024")
    s += block("block", "then 1024", [(":method", "GET"), (":path", "/e.js")])

    s.append("story big headers evict and clear the table")
    s.append("huffman on")
    s.append("encoder-table 1024")
    s.append("decoder-table 1024")
    s += block("block", "small headers", [(":status", "200"), ("x-a", "1"), ("x-b", "2"), ("x-c", "3")])
    s += block("block", "a 600-byte header evicts", [(":status", "200"),
                                                    ("x-report", "csp=" + "-".join(f"{i:03d}" for i in range(150)))])
    s += block("block", "a header bigger than the table clears it", [
        (":status", "200"), ("set-cookie", "prefs=" + "z" * 1100), ("x-a", "1")])

    s.append("story a dict of headers is reordered")
    s.append("huffman on")
    s += block("dict", "dict with :path last", [("user-agent", UA_SAFARI), ("accept", "*/*"),
                                                 (":method", "GET"), ("x-debug", "on"), (":scheme", "https"),
                                                 (":authority", "status.example.com"), (":path", "/health")])

    s.append("story non-ASCII values in Huffman")
    s.append("huffman on")
    s += block("block", "a download", [(":status", "200"),
                                      ("content-disposition", "attachment; filename*=UTF-8''résumé.pdf"),
                                      ("x-display-name", "Björk Guðmundsdóttir"),
                                      ("x-city", "東京"), ("x-empty", "")])
    s += block("block", "the same again", [(":status", "200"), ("x-city", "東京"), ("x-empty", "")])

    s.append("story a decoder that limits the header list")
    s.append("huffman on")
    s.append("decoder-list-max 400")
    s += block("block", "a small request", [(":method", "GET"), (":path", "/"), ("x-n", "1")])
    s += block("block", "cookies over the limit", [(":method", "GET"), (":path", "/")] +
               [("cookie", f"c{i}=" + "v" * 30) for i in range(10)])
    s += block("block", "never reached", [(":method", "GET")])

    s.append("story a decoder whose SETTINGS the encoder ignores")
    s.append("huffman off")
    s += block("block", "first", [(":method", "GET"), (":path", "/"), ("x-trace", "one")])
    s.append("decoder-max 1024")
    s += block("block", "the encoder sent no size update", [(":method", "GET"), (":path", "/")])

    s.append("story an encoder that grows past the decoder's limit")
    s.append("huffman off")
    s.append("encoder-table 8192")
    s += block("block", "first", [(":method", "GET"), (":path", "/")])
    return s


RFC = [
    ("RFC 7541 C.2.1 literal with indexing", None,
     ["400a637573746f6d2d6b65790d637573746f6d2d686561646572"]),
    ("RFC 7541 C.2.2 literal without indexing", None, ["040c2f73616d706c652f70617468"]),
    ("RFC 7541 C.2.3 literal never indexed", None, ["100870617373776f726406736563726574"]),
    ("RFC 7541 C.2.4 indexed", None, ["82"]),
    ("RFC 7541 C.3 requests", None,
     ["828684410f7777772e6578616d706c652e636f6d", "828684be58086e6f2d6361636865",
      "828785bf400a637573746f6d2d6b65790c637573746f6d2d76616c7565"]),
    ("RFC 7541 C.4 requests with Huffman", None,
     ["828684418cf1e3c2e5f23a6ba0ab90f4ff", "828684be5886a8eb10649cbf",
      "828785bf408825a849e95ba97d7f8925a849e95bb8e8b4bf"]),
    ("RFC 7541 C.5 responses", 256,
     ["4803333032580770726976617465611d4d6f6e2c203231204f637420323031332032303a31333a323120474d54"
      "6e1768747470733a2f2f7777772e6578616d706c652e636f6d",
      "4803333037c1c0bf",
      "88c1611d4d6f6e2c203231204f637420323031332032303a31333a323220474d54c05a04677a6970"
      "7738666f6f3d4153444a4b48514b425a584f5157454f50495541585157454f49553b206d61782d6167653d"
      "333630303b2076657273696f6e3d31"]),
    ("RFC 7541 C.6 responses with Huffman", 256,
     ["488264025885aec3771a4b6196d07abe941054d444a8200595040b8166e082a62d1bff6e919d29ad171863"
      "c78f0b97c8e9ae82ae43d3",
      "4883640effc1c0bf",
      "88c16196d07abe941054d444a8200595040b8166e084a62d1bffc05a839bd9ab77ad94e7821dd7f2e6c7b3"
      "35dfdfcd5b3960d5af27087f3672c1ab270fb5291f9587316065c003ed4ee5b1063d5007"]),
]


def vectors():
    v = []
    for title, size, blocks in RFC:
        v.append(f"case {title}")
        if size is not None:
            v.append(f"decoder-table {size}")
        for b in blocks:
            v.append("hex " + b)
    ats = (b'\x10\x07:status\x03200@\x06server\tATS/6.0.0'
           b'@\x04date\x1dTue, 31 Mar 2015 08:09:51 GMT'
           b'@\x0ccontent-type\ttext/html@\x0econtent-length\x0542468'
           b'@\rlast-modified\x1dTue, 31 Mar 2015 01:55:51 GMT'
           b'@\x04vary\x0fAccept-Encoding@\x04etag\x0f"5519fea7-a5e4"'
           b'@\x08x-served\x05Nginx@\x14x-subdomain-tryfiles\x04True'
           b'@\x07x-deity\thydra-lts@\raccept-ranges\x05bytes@\x03age\x010'
           b'@\x19strict-transport-security\rmax-age=86400'
           b'@\x03via2https/1.1 ATS (ApacheTrafficServer/6.0.0 [cSsNfU])')
    v += ["case Apache Traffic Server response (hpack issue 110)", "hex " + ats.hex()]
    v += ["case raw bytes in a Huffman-free name", "hex 400a00019930112255218914" + "0d" + b"custom-header".hex()]
    bad = [
        ("an empty block", [""]),
        ("index 0", ["80"]),
        ("index 62 with an empty dynamic table", ["be"]),
        ("an indexed name past the table", ["828684" + "7f0a" + "0f" + b"www.example.com".hex()]),
        ("a big index", ["ffffffffffffffff7f"]),
        ("an integer cut short", ["ff"]),
        ("an integer cut short inside a literal", ["828640"]),
        ("a name cut short", ["4005616263"]),
        ("a value cut short", ["400161056162"]),
        ("a value length cut short", ["400161"]),
        ("EOS inside a Huffman string", ["4084fffffffc0161"]),
        ("padding longer than 7 bits", ["40821fff0161"]),
        ("padding with a zero bit", ["4081000161"]),
        ("an empty Huffman name and value", ["408080", "be"]),
        ("never indexed with an indexed name", ["140c2f73616d706c652f70617468"]),
        ("literal without indexing, name index 58", ["0f2b" + "0a" + b"curl/8.9.1".hex()]),
        ("table size updates at the start", ["203fe11f82", "3f9a0a82"]),
        ("a table size update after a header", ["823fe11f"]),
        ("a table size update above the maximum", ["3fe21f"]),
        ("a table size update between two headers", ["82" + "3fe11f" + "86"]),
        ("invalid UTF-8", ["828684" + "0110" + b"www.".hex() + "07aad795d7a8d794" + b".com".hex()]),
        ("table eviction with size 64", ["3f21" + "4003" + b"abc".hex() + "03" + b"123".hex(), "be",
                                         "4003" + b"def".hex() + "03" + b"456".hex(), "bebf"]),
    ]
    for title, blocks in bad:
        v.append(f"case {title}")
        for b in blocks:
            v.append("hex " + b)
    v += ["case the header list limit", "decoder-list-max 45", "hex 82", "hex 140c2f73616d706c652f70617468"]
    v += ["case a lowered maximum the encoder did not follow", "decoder-max 1024",
          "hex 828684418cf1e3c2e5f23a6ba0ab90f4ff", "hex 3fe10782", "hex 82"]
    v += ["case a raised table with the default maximum", "decoder-table 8000", "hex 82", "hex 3fe11f82"]
    return v


def main():
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "stories.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(stories()) + "\n")
    with open(os.path.join(DATA, "vectors.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(vectors()) + "\n")


if __name__ == "__main__":
    main()
