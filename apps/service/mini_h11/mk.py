#!/usr/bin/env python3
"""Writes data/: the connection scripts in data/scripts/ and the captured
traffic in data/captures/ that some of them feed in pieces. A script line
is one call on an h11 Connection; see README.md for the commands."""
import gzip
import os
import shutil

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/scripts")
os.makedirs("data/captures")


def capture(name, data):
    with open("data/captures/" + name, "wb") as f:
        f.write(data)


def script(name, text):
    with open("data/scripts/" + name + ".h11", "w") as f:
        f.write(text.strip("\n") + "\n")


# ---------------------------------------------------------------- captures

capture("curl-get.bin",
        b"GET /api/v1/users?page=2&per_page=50 HTTP/1.1\r\n"
        b"Host: api.example.com\r\n"
        b"User-Agent: curl/8.5.0\r\n"
        b"Accept: */*\r\n"
        b"Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.e30.ZRrHA1JJJW8opsbCGfG_HACGpVUMN_a9IV7pAx_Zmeo\r\n"
        b"\r\n")

capture("browser-post.bin",
        b"POST /login HTTP/1.1\r\n"
        b"Host: shop.example.org\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 40\r\n"
        b"Cache-Control: max-age=0\r\n"
        b"Origin: https://shop.example.org\r\n"
        b"Content-Type: application/x-www-form-urlencoded\r\n"
        b"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36\r\n"
        b"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
        b"Referer: https://shop.example.org/login?next=%2Fcart\r\n"
        b"Accept-Encoding: gzip, deflate, br, zstd\r\n"
        b"Accept-Language: en-GB,en;q=0.9,de;q=0.8\r\n"
        b"Cookie: csrftoken=Zx81Kq; _ga=GA1.1.1234567890.1700000000\r\n"
        b"\r\n"
        b"username=grace&password=hunter2&next=%2F")

body = gzip.compress(b'{"items":[{"sku":"A-1","qty":2},{"sku":"B-7","qty":1}],"total":"41.50"}\n' * 3, mtime=0)
chunks = [body[:40], body[40:41], body[41:]]
capture("nginx-chunked.bin",
        b"HTTP/1.1 200 OK\r\n"
        b"Server: nginx/1.24.0\r\n"
        b"Date: Sat, 18 Oct 2026 12:00:00 GMT\r\n"
        b"Content-Type: application/json\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Encoding: gzip\r\n"
        b"Vary: Accept-Encoding\r\n"
        b"\r\n"
        + b"".join(b"%x;len=%d\r\n%s\r\n" % (len(c), len(c), c) for c in chunks)
        + b"0\r\nServer-Timing: db;dur=53\r\nX-Checksum: 9f3a\r\n\r\n")

CSV1 = b"region,quarter,revenue\nEU,"
CSV2 = b"Q1,1200\nUS,Q1,3400\nAPAC,Q1,9\n"
capture("upload-head.bin",
        b"PUT /uploads/report.csv HTTP/1.1\r\n"
        b"Host: files.internal:8443\r\n"
        b"Content-Type: text/csv\r\n"
        b"Transfer-Encoding: chunked\r\n"
        b"Expect: 100-continue\r\n"
        b"\r\n")
capture("upload-body.bin",
        b"%x\r\n%s\r\n" % (len(CSV1), CSV1)
        + b"%X\r\n%s\r\n" % (len(CSV2), CSV2)
        + b"00\r\n\r\n")

capture("pipelined.bin",
        b"GET /a.css HTTP/1.1\r\nHost: cdn.example.net\r\n\r\n"
        b"GET /b.js HTTP/1.1\r\nHost: cdn.example.net\r\n\r\n"
        b"GET /c.png HTTP/1.1\r\nHost: cdn.example.net\r\nConnection: close\r\n\r\n")

capture("http10-response.bin",
        b"HTTP/1.0 200 OK\r\nServer: SimpleHTTP/0.6 Python/3.13.0\r\nContent-type: text/plain\r\n\r\n"
        b"line one\nline two\n")

capture("tls-hello.bin", bytes.fromhex(
    "16030100f4010000f00303a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f6"
    "0718293a4b5c6d7e8f9000003e130213031301c02cc030009fcca9cca8ccaac02b"))

# ---------------------------------------------------------------- server

script("srv-01-get-keepalive", r"""
# A plain GET, answered with a body, then a second request on the same connection.
role server
recv GET /index.html HTTP/1.1\r\nHost: www.example.com\r\nAccept: text/html\r\n\r\n
response 200 1.1 OK | Content-Type: text/html; charset=utf-8 | Content-Length: 13
data <h1>Hi</h1>\n
data .
eom
cycle
recv GET /favicon.ico HTTP/1.1\r\nHost: www.example.com\r\n\r\n
response 404 1.1 Not Found | Content-Length: 0
eom
cycle
""")

script("srv-02-curl-bytewise", r"""
# curl's request arriving one byte at a time, then answered with JSON.
role server
recvfile captures/curl-get.bin 40
response 200 1.1 OK | Content-Type: application/json | Content-Length: 2
data []
eom
""")

script("srv-03-browser-post", r"""
role server
recvfile captures/browser-post.bin 97
response 303 1.1 See Other | Location: /cart | Set-Cookie: session=7c1f; HttpOnly; Secure | Content-Length: 0
eom
cycle
""")

script("srv-04-chunked-upload", r"""
# A chunked PUT that waits for 100 Continue, with chunk sizes in mixed case.
role server
recvfile captures/upload-head.bin 64
info 100 1.1 Continue
recvfile captures/upload-body.bin 16
response 201 1.1 Created | Location: /uploads/report.csv
data stored\n
eom
cycle
""")

script("srv-05-pipelined", r"""
# Three requests in one read: h11 hands over one and pauses on the rest.
role server
recvfile captures/pipelined.bin 4096
response 200 1.1 OK | Content-Length: 4
data a{}\n
eom
cycle
drain
response 200 1.1 OK | Content-Length: 3
data ;\n\n
eom
cycle
drain
response 200 1.1 OK | Content-Type: image/png
data \x89PNG
eom
next
eof
""")

script("srv-06-http10-client", r"""
# An HTTP/1.0 client: no Host needed, and a response without a length is closed.
role server
recv GET / HTTP/1.0\r\n\r\n
response 200 1.1 OK | Content-Type: text/plain | Content-Length: 5
data hello
eom
cycle
""")

script("srv-07-http10-unframed", r"""
role server
recv GET /stream HTTP/1.0\r\nUser-Agent: Wget/1.21\r\n\r\n
response 200 1.1 OK | Content-Type: text/event-stream | Transfer-Encoding: chunked
data event: tick\n\n
data event: tick\n\n
eom
close
""")

script("srv-08-chunked-response", r"""
# A 1.1 client and a streamed reply: h11 adds Transfer-Encoding and drops Content-Length.
role server
recv GET /events HTTP/1.1\r\nHost: feed.example\r\nConnection: Keep-Alive\r\n\r\n
response 200 1.1 OK | Cache-Control: no-cache
data id: 1\ndata: first\n\n
data
data id: 2\ndata: second\n\n
eom | X-Stream-End: clean | Server-Timing: total;dur=12
cycle
""")

script("srv-09-connection-close", r"""
role server
recv DELETE /items/42 HTTP/1.1\r\nHost: api\r\nConnection: Close, TE\r\n\r\n
response 204 1.1 No Content | Connection: keep-alive
eom
cycle
recv GET / HTTP/1.1\r\nHost: api\r\n\r\n
eof
close
""")

script("srv-10-head", r"""
# HEAD: the response keeps its Content-Length and sends no body.
role server
recv HEAD /big.iso HTTP/1.1\r\nHost: mirror.example\r\n\r\n
response 200 1.1 OK | Content-Length: 4700000000 | Accept-Ranges: bytes
data x
eom
""")

script("srv-11-head-unframed", r"""
role server
recv HEAD /live HTTP/1.1\r\nHost: tv\r\n\r\n
response 200 1.1 OK | Content-Type: video/mp2t
eom
cycle
""")

script("srv-12-websocket-upgrade", r"""
# An Upgrade to WebSocket: after 101 the connection belongs to the new protocol.
role server
recv GET /chat HTTP/1.1\r\nHost: ws.example.com\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n\x81\x85\x37\xfa\x21\x3d\x7f\x9f\x4d\x51\x58
next
info 101 1.1 Switching Protocols | Upgrade: websocket | Connection: Upgrade | Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
next
""")

script("srv-13-upgrade-declined", r"""
role server
recv GET /chat HTTP/1.1\r\nHost: ws\r\nUpgrade: h2c\r\nConnection: Upgrade, HTTP2-Settings\r\nHTTP2-Settings: AAMAAABkAAQAoAAAAAIAAAAA\r\n\r\n
next
response 200 1.1 OK | Content-Length: 3
data ok
data k
eom
cycle
""")

script("srv-14-connect", r"""
role server
recv CONNECT db.internal:5432 HTTP/1.1\r\nHost: db.internal:5432\r\n\r\n
response 200 1.1 Connection established
next
recv \x00\x00\x00\x08\x04\xd2\x16\x2f
""")

script("srv-15-connect-refused", r"""
role server
recv CONNECT evil.example:25 HTTP/1.1\r\nHost: evil.example:25\r\nContent-Length: 0\r\n\r\n
response 403 1.1 Forbidden | Content-Length: 0
eom
cycle
""")

script("srv-16-obs-fold", r"""
# Obsolete line folding joins continuation lines with one space.
role server
recv POST /soap HTTP/1.1\r\nHost: legacy\r\nSOAPAction: "urn:\r\n\t  getQuote"\r\nX-Long: a\r\n b\r\n  c\r\nContent-Length: 0\r\n\r\n
""")

script("srv-17-header-forms", r"""
# Values are trimmed of spaces and tabs; empty values and odd bytes are fine.
role server
recv GET / HTTP/1.1\r\nHost:example.com\r\nX-Empty:\r\nX-Spaces: \t a  b \t \r\nX-Ctl: a\x01b\r\nX-Obs: caf\xc3\xa9\r\nACCEPT: */*\r\n\r\n
""")

script("srv-18-lf-only", r"""
# Bare LF line endings are accepted too.
role server
recv GET /lf HTTP/1.1\nHost: x\nContent-Length: 3\n\nabc
""")

script("srv-19-content-length-forms", r"""
role server
recv POST /a HTTP/1.1\r\nHost: x\r\nContent-Length: 5, 5,5\r\n\r\nhello
response 200 1.1 OK | Content-Length: 0
eom
cycle
recv POST /b HTTP/1.1\r\nHost: x\r\nContent-Length: 3\r\ncontent-length: 3\r\n\r\nabc
""")

script("srv-20-chunked-trailers", r"""
role server
recv POST /ingest HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: Chunked\r\n\r\n
recv 4;name="first"; ext\r\nWiki\r\n5 \t\r\npedia\r\nE\r\n in\r\n\r\nchunks.\r\n
recv 0;done\r\nContent-MD5: 1B2M2Y8AsgTpgAmY7PhCfg==\r\nX-Trailer:   x  \r\n\r\n
""")

script("srv-21-chunk-split", r"""
# A chunk whose data and CRLF arrive in separate reads.
role server
recv POST /x HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: chunked\r\n\r\n6\r\nhel
recv lo!
recv \r
recv \n
recv 0\r\n
recv \r\n
""")

script("srv-22-eof-mid-body", r"""
role server
recv POST /upload HTTP/1.1\r\nHost: x\r\nContent-Length: 10\r\n\r\n12345
eof
next
""")

script("srv-23-eof-mid-chunked", r"""
role server
recv POST /upload HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: chunked\r\n\r\n5\r\nabc
eof
""")

script("srv-24-eof-mid-headers", r"""
role server
recv GET / HTTP/1.1\r\nHost: x\r\n
eof
recv more
""")

script("srv-25-eof-idle", r"""
role server
eof
next
recv late
""")

script("srv-26-keepalive-then-close", r"""
role server
recv GET / HTTP/1.1\r\nHost: x\r\n\r\n
response 200 1.1 OK | Content-Length: 0
eom
cycle
eof
""")

script("srv-27-data-after-close-request", r"""
role server
recv GET / HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\nGET /again HTTP/1.1\r\n\r\n
response 200 1.1 OK | Content-Length: 1
data !
eom
next
""")

# ---------------------------------------------------------------- server errors

script("err-01-tls", r"""
# A TLS ClientHello sent to a plain-HTTP port fails before a line ends.
role server
recvfile captures/tls-hello.bin 16
""")

script("err-02-bad-request-lines", r"""
role server
recv GET  / HTTP/1.1\r\n\r\n
next
""")

script("err-03-no-request-line", r"""
role server
recv \r\nGET / HTTP/1.1\r\nHost: x\r\n\r\n
""")

script("err-04-version", r"""
role server
recv GET / HTTP/1.11\r\nHost: x\r\n\r\n
""")

script("err-05-lowercase-http", r"""
role server
recv GET / http/1.1\r\nHost: x\r\n\r\n
""")

script("err-06-missing-host", r"""
role server
recv GET / HTTP/1.1\r\nUser-Agent: x\r\n\r\n
""")

script("err-07-two-hosts", r"""
role server
recv GET / HTTP/1.1\r\nHost: a\r\nhost: b\r\n\r\n
""")

script("err-08-space-before-colon", r"""
role server
recv GET / HTTP/1.1\r\nHost : evil\r\n\r\n
""")

script("err-09-fold-at-start", r"""
role server
recv GET / HTTP/1.1\r\n Host: x\r\n\r\n
""")

script("err-10-conflicting-length", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nContent-Length: 5\r\nContent-Length: 6\r\n\r\n
""")

script("err-11-length-list", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nContent-Length: 5, 6\r\n\r\n
""")

script("err-12-bad-length", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nContent-Length: -1\r\n\r\n
""")

script("err-13-huge-length", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nContent-Length: 123456789012345678901\r\n\r\n
""")

script("err-14-gzip-te", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: gzip, chunked\r\n\r\n
""")

script("err-15-two-te", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: chunked\r\nTransfer-Encoding: chunked\r\n\r\n
""")

script("err-16-bad-chunk-header", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: chunked\r\n\r\nzz\r\nab\r\n
""")

script("err-17-chunk-footer", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: chunked\r\n\r\n3\r\nabcde\r\n
""")

script("err-18-chunk-size-too-long", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: chunked\r\n\r\n000000000000000000005\r\nhello\r\n
""")

script("err-19-buffer-too-long", r"""
role server max 64
recv GET / HTTP/1.1\r\nHost: x\r\nCookie: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
next
""")

script("err-20-garbage-after-done", r"""
role client
request GET / 1.1 | Host: x
eom
recv HTTP/1.1 200 OK\r\nContent-Length: 0\r\nConnection: close\r\n\r\nextra
""")

script("err-21-header-value-ctl", r"""
role server
recv GET / HTTP/1.1\r\nHost: x\r\nX-Bad: a\rb\r\n\r\n
""")

script("err-22-target-space", r"""
role server
recv GET /a b HTTP/1.1\r\nHost: x\r\n\r\n
""")

script("err-23-method-chars", r"""
role server
recv G(ET / HTTP/1.1\r\nHost: x\r\n\r\n
""")

script("err-24-bad-trailer", r"""
role server
recv POST / HTTP/1.1\r\nHost: x\r\nTransfer-Encoding: chunked\r\n\r\n0\r\nbad trailer\r\n\r\n
""")

# ---------------------------------------------------------------- client

script("cli-01-get", r"""
role client
request GET /api/v1/status 1.1 | Host: api.example.com | Accept: application/json
eom
recv HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 15\r\n\r\n{"status":
recv "up"}
cycle
""")

script("cli-02-nginx-chunked", r"""
role client
request GET /cart.json 1.1 | Host: shop.example.org | Accept-Encoding: gzip
eom
recvfile captures/nginx-chunked.bin 23
cycle
""")

script("cli-03-http10-server", r"""
# No framing in the response: the body runs until the server closes.
role client
request GET /notes.txt 1.1 | Host: localhost:8000
eom
recvfile captures/http10-response.bin 50
eof
""")

script("cli-04-post-json", r"""
role client
request POST /v1/charges 1.1 | Host: api.stripe.example | Content-Type: application/json | Content-Length: 27 | Idempotency-Key: 5f2b
data {"amount":2000,
data "cur":"eur"}
eom
recv HTTP/1.1 402 Payment Required\r\nContent-Length: 0\r\n\r\n
""")

script("cli-05-continue", r"""
role client
request PUT /big 1.1 | Host: s3.example | Content-Length: 4 | Expect: 100-continue
recv HTTP/1.1 100 Continue\r\n\r\n
data abcd
eom
recv HTTP/1.1 200 OK\r\nETag: "d41d8"\r\nContent-Length: 0\r\n\r\n
""")

script("cli-06-informational", r"""
role client
request GET / 1.1 | Host: x
eom
recv HTTP/1.1 103 Early Hints\r\nLink: </style.css>; rel=preload; as=style\r\n\r\nHTTP/1.1 102\r\n\r\nHTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nhi
""")

script("cli-07-no-body-statuses", r"""
role client
request GET /cached 1.1 | Host: x | If-None-Match: "abc"
eom
recv HTTP/1.1 304 Not Modified\r\nETag: "abc"\r\nContent-Length: 1234\r\n\r\n
cycle
request HEAD /file 1.1 | Host: x
eom
recv HTTP/1.1 200 OK\r\nContent-Length: 1234\r\n\r\n
cycle
request DELETE /x 1.1 | Host: x
eom
recv HTTP/1.1 204 No Content\r\nTransfer-Encoding: chunked\r\n\r\n
""")

script("cli-08-status-lines", r"""
role client
request GET / 1.1 | Host: x
eom
recv HTTP/1.1 200\r\nContent-Length: 0\r\n\r\n
cycle
request GET / 1.1 | Host: x
eom
recv HTTP/1.1 418 I'm a "teapot"\t(RFC 2324)\r\nContent-Length: 0\r\n\r\n
cycle
request GET / 1.1 | Host: x
eom
recv HTTP/1.1 500 \r\nContent-Length: 0\r\n\r\n
""")

script("cli-09-bad-status", r"""
role client
request GET / 1.1 | Host: x
eom
recv HTTP/1.1 20 OK\r\n\r\n
next
""")

script("cli-10-connect-tunnel", r"""
role client
request CONNECT db.internal:5432 1.1 | Host: db.internal:5432
eom
recv HTTP/1.1 200 Connection established\r\n\r\n\x16\x03\x01
next
""")

script("cli-11-connect-denied", r"""
role client
request CONNECT db.internal:5432 1.1 | Host: db.internal:5432
eom
recv HTTP/1.1 407 Proxy Authentication Required\r\nProxy-Authenticate: Basic realm="corp"\r\nContent-Length: 0\r\n\r\n
cycle
""")

script("cli-12-upgrade-refused", r"""
role client
request GET /socket 1.1 | Host: x | Connection: upgrade | Upgrade: websocket
eom
recv HTTP/1.1 426 Upgrade Required\r\nContent-Length: 0\r\n\r\n
cycle
""")

script("cli-13-switching", r"""
role client
request GET /socket 1.1 | Host: x | Connection: upgrade | Upgrade: websocket
eom
recv HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n\x81\x02hi
next
""")

script("cli-14-early-response", r"""
# The server answers before the upload is finished.
role client
request POST /upload 1.1 | Host: x | Content-Length: 1000000
data first part
recv HTTP/1.1 413 Payload Too Large\r\nConnection: close\r\nContent-Length: 0\r\n\r\n
data second part
""")

script("cli-15-server-closes", r"""
role client
request GET / 1.1 | Host: x
eom
recv HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Length: 2\r\n\r\nok
eof
cycle
close
""")

script("cli-16-truncated", r"""
role client
request GET / 1.1 | Host: x
eom
recv HTTP/1.1 200 OK\r\nContent-Length: 20\r\n\r\nonly ten b
eof
""")

# ---------------------------------------------------------------- sending errors

script("snd-01-length", r"""
role client
request POST / 1.1 | Host: x | Content-Length: 3
data abcd
data ab
""")

script("snd-02-too-little", r"""
role client
request POST / 1.1 | Host: x | Content-Length: 3
data ab
eom
data c
""")

script("snd-03-trailers-with-length", r"""
role client
request POST / 1.1 | Host: x | Content-Length: 0
eom | X-Foo: bar
""")

script("snd-04-wrong-state", r"""
role client
data too early
eom
request GET / 1.1 | Host: x
request GET / 1.1 | Host: x
""")

script("snd-05-versions", r"""
role client
request GET / 1.0
request GET / 1.0 | Host: x
""")

script("snd-06-events", r"""
role server
response 99 1.1 Low
info 200 1.1 OK
response 1000 1.1 Huge
request GET /x 1.1 | Host: a | Host: b
request GET /a\x20b 1.1 | Host: x
request G(ET / 1.1 | Host: x
""")

script("snd-07-header-validation", r"""
role server
recv GET / HTTP/1.1\r\nHost: x\r\n\r\n
response 200 1.1 OK | Bad Name: x
response 200 1.1 OK | X-Nul: a\x00b
response 200 1.1 OK | X-Newline: a\r\nInjected: yes
response 200 1.1 OK | Content-Length: 12abc
response 200 1.1 OK | Transfer-Encoding: identity
response 200 1.1 OK | Content-Length: 2 | Content-Length: 3
response 200 1.1 OK | X-Tail: trailing space 
""")

script("snd-08-chunked-trailers", r"""
role client
request POST /logs 1.1 | Host: logs.example | Transfer-Encoding: chunked | Trailer: X-Count
data 2026-10-18T12:00:00Z GET /a 200\n
data
data 2026-10-18T12:00:01Z GET /b 404\n
eom | X-Count: 2
""")

script("snd-09-response-cleanup", r"""
# h11 rewrites response framing for what the client can read.
role server
recv GET / HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n
response 200 1.1 OK | Connection: keep-alive, Upgrade | Content-Type: text/plain
data streamed
eom
""")

script("snd-10-cycle-errors", r"""
role server
cycle
recv GET / HTTP/1.1\r\nHost: x\r\n\r\n
cycle
response 200 1.1 OK | Content-Length: 0
cycle
eom
cycle
cycle
""")

script("snd-11-after-error", r"""
role server
recv GET / HTTP/1.1\r\nHost: x\r\n\r\n
response 200 1.1 OK | Content-Length: 1
data too long
data x
eom
recv more
""")

script("snd-12-send-failed", r"""
role client
request GET / 1.1 | Host: x
failed
eom
recv HTTP/1.1 200 OK\r\n\r\n
""")

script("snd-13-host-first", r"""
# The Host header goes first on the wire, whatever order it was given in.
role client
request OPTIONS * 1.1 | User-Agent: probe/1.0 | Accept: */* | HOST: Example.COM:8080
eom
""")
