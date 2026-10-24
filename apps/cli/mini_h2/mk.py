"""Writes data/jobs.txt: HTTP/2 conversations for oracle.py and mini_h2.kara.

A job is a list of commands, one per line, `<endpoint> <verb> <args>`:
`new client|server [options]`, `initiate`, `upgrade [settings]`,
`headers <sid> [end] [w= d= x=] name=value...`, `data <sid> <payload> [end]
[pad=n]`, `end`, `window <n> [sid]`, `push <sid> <promised> headers...`,
`ping`, `reset <sid> [code]`, `goaway [code= last= data=]`, `settings k=v...`,
`altsvc <field> [origin= | sid=]`, `prio <sid> [w= d= x=]`, `ack <n> <sid>`,
`raw <hex>`, `drop`, `show`, `state`, `windows <sid>`, and `pipe <from> <to>
[n]`, which delivers what one endpoint has sent to the other. In a header
`~s` is a space, `~e` an equals sign, `~c` a comma and `~~` a tilde; `!`
marks a never-indexed header and `%` one given as bytes. A payload is text,
`len=<n>` bytes of a fixed pattern or `hex=<hex>`. The raw frames are built
with the vendored hyperframe and hpack.

Run: python3 -s -P -B mk.py"""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "vendor"))

from hpack.hpack import Encoder  # noqa: E402
from hyperframe.frame import (  # noqa: E402
    ContinuationFrame, DataFrame, GoAwayFrame, HeadersFrame, PingFrame, PriorityFrame,
    PushPromiseFrame, RstStreamFrame, SettingsFrame, WindowUpdateFrame,
)

PREAMBLE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
JOBS = []


def job(title, *lines):
    JOBS.append((title, list(lines)))


def hx(*frames):
    out = b""
    for f in frames:
        out += f if isinstance(f, bytes) else f.serialize()
    return out.hex()


def hdr_frame(enc, sid, headers, flags=("END_HEADERS",), **kw):
    f = HeadersFrame(sid, flags=list(flags), **kw)
    f.data = enc.encode(headers)
    return f


def opening():
    return PREAMBLE + SettingsFrame(0).serialize()


GET = ":method=GET :path=/ :scheme=https :authority=shop.example"
REQ = [(":method", "GET"), (":path", "/"), (":scheme", "https"), (":authority", "shop.example")]


def hello(c="c", s="s", copts="", sopts=""):
    return [f"{c} new client{copts}", f"{s} new server{sopts}", f"{c} initiate", f"{s} initiate",
            f"pipe {c} {s}", f"pipe {s} {c}", f"pipe {c} {s}"]


# ---- ordinary exchanges

job("a GET and its response",
    *hello(),
    f"c headers 1 {GET} user-agent=mini-h2/1.0 accept=text/html end",
    "c state", "pipe c s",
    "s headers 1 :status=200 content-type=text/html;~scharset~eutf-8 content-length=12 server=h2",
    "s data 1 hello~sworld! end",
    "s state", "pipe s c",
    "c ack 12 1", "pipe c s", "c state", "s state")

job("a POST in three DATA frames, acknowledged as it arrives",
    *hello(),
    "c headers 1 :method=POST :path=/orders :scheme=https :authority=shop.example "
    "content-type=application/json content-length=50",
    "c data 1 {\"sku\":~s\"A-17\"~c", "c data 1 ~s\"qty\":~s3~c",
    "c data 1 ~s\"note\":~s\"leave~sat~sdoor\"} end",
    "pipe c s", "s ack 50 1", "s windows 1",
    "s headers 1 :status=201 location=/orders/9 end", "pipe s c", "c state", "s state")

job("two requests on one connection, answered out of order",
    *hello(),
    f"c headers 1 {GET} end",
    "c headers 3 :method=GET :path=/style.css :scheme=https :authority=shop.example end",
    "c headers 5 :method=GET :path=/logo.png :scheme=https :authority=shop.example end",
    "pipe c s", "s state",
    "s headers 5 :status=200 content-type=image/png", "s data 5 hex=89504e470d0a1a0a end",
    "s headers 3 :status=304 end",
    "s headers 1 :status=200 content-type=text/html", "s data 1 <html></html> end",
    "pipe s c", "c state", "s state")

job("header encoding: str headers back out",
    *hello(copts=" encoding=utf-8", sopts=" encoding=utf-8"),
    f"c headers 1 {GET} accept-language=fr-CH~c~sfr;q~e0.9 x-name=café end",
    "pipe c s", "s headers 1 :status=200 x-greeting=grüße end", "pipe s c")

job("sensitive headers and cookies",
    *hello(),
    f"c headers 1 {GET} authorization=Bearer~sabc.def.ghi cookie=a~e1 cookie=session~e0123456789abcdef0123 "
    "!x-api-key=k-5150 %x-raw=bytes~svalue end",
    "pipe c s",
    "s headers 1 :status=200 set-cookie=id~e7;~sPath~e/ end", "pipe s c",
    f"c headers 3 {GET} authorization=Bearer~sabc.def.ghi cookie=a~e1 end", "pipe c s")

job("outbound normalisation: case, spaces and connection headers",
    *hello(),
    f"c headers 1 {GET} User-Agent=~s~sspaced~s~s Connection=keep-alive Keep-Alive=5 X-Mixed=Case end",
    "pipe c s")

job("split outbound cookies",
    *hello(copts=" split_outbound_cookies=1"),
    f"c headers 1 {GET} cookie=a~e1;~sb~e2;~sc~e3 end", "pipe c s")

job("trailers after the body",
    *hello(),
    "c headers 1 :method=POST :path=/upload :scheme=https :authority=shop.example te=trailers",
    "c data 1 part~sone", "c headers 1 x-checksum=1234 x-count=8 end", "pipe c s",
    "s headers 1 :status=200 grpc-encoding=identity", "s data 1 ok",
    "s headers 1 grpc-status=0 grpc-message=done", "s headers 1 grpc-status=0 grpc-message=done end",
    "pipe s c")

job("a 100-continue before the final response",
    *hello(),
    "c headers 1 :method=PUT :path=/big :scheme=https :authority=shop.example expect=100-continue",
    "pipe c s", "s headers 1 :status=100", "s headers 1 :status=103 link=</a.css>;~srel~epreload end",
    "pipe s c", "c data 1 the~sbody end", "pipe c s", "s headers 1 :status=204 end",
    "s headers 1 :status=100", "pipe s c")

job("HEAD and content-length",
    *hello(),
    "c headers 1 :method=HEAD :path=/file :scheme=https :authority=shop.example end",
    "c headers 3 :method=GET :path=/file :scheme=https :authority=shop.example end",
    "c headers 5 :method=GET :path=/short :scheme=https :authority=shop.example end",
    "c headers 7 :method=GET :path=/bad :scheme=https :authority=shop.example end",
    "pipe c s",
    "s headers 1 :status=200 content-length=1000 end",
    "s headers 3 :status=200 content-length=5", "s data 3 12345 end",
    "s headers 5 :status=200 content-length=5", "s data 5 123 end",
    "pipe s c", "c state")

job("content-length as Python's int() reads it",
    *hello(),
    f"c headers 1 {GET} end", f"c headers 3 {GET} end", "pipe c s",
    "s headers 1 :status=200 content-length=~s+0_2~t", "s data 1 hi end",
    "s headers 3 :status=200 content-length=-0", "s data 3 len=0 end", "pipe s c")

job("content-length that is not a number",
    *hello(),
    f"c headers 1 {GET} end", "pipe c s",
    "s headers 1 :status=200 content-length=twelve", "pipe s c", "c state")

job("padding, end_stream on its own, and an empty body",
    *hello(),
    "c headers 1 :method=POST :path=/p :scheme=https :authority=shop.example",
    "c data 1 secret pad=10", "c data 1 len=0 pad=0", "c end 1", "c end 1", "pipe c s",
    "s data 1 x pad=256", "s data 1 x pad=-1", "s headers 1 :status=200 end", "pipe s c")

# ---- flow control

job("filling the stream window and reopening it",
    *hello(),
    f"c headers 1 {GET} end", "pipe c s",
    "s headers 1 :status=200", "s data 1 len=16384", "s data 1 len=16384", "s data 1 len=16384",
    "s data 1 len=16383", "s windows 1", "s data 1 len=2", "s data 1 len=1", "s windows 1",
    "s data 1 len=1",
    "pipe s c", "c state", "c ack 30000 1", "pipe c s", "s windows 1",
    "c ack 35535 1", "pipe c s", "s windows 1", "s data 1 len=20000 end", "pipe s c", "c state")

job("a frame bigger than the peer's maximum",
    *hello(),
    f"c headers 1 {GET} end", "pipe c s", "s headers 1 :status=200",
    "s data 1 len=16385", "s data 1 len=16384", "pipe s c")

job("window increments sent and received",
    *hello(),
    f"c headers 1 {GET} end", "c window 1000", "c window 500 1", "c window 0", "c window 2147483648",
    "pipe c s", "s state", "s headers 1 :status=200", "pipe s c",
    "s window 100 9", "s window 2147483647", "s show")

job("SETTINGS: a smaller window, a bigger frame size and acknowledgements",
    *hello(),
    f"c headers 1 {GET} end", "pipe c s", "s headers 1 :status=200",
    "c settings 4=100 5=20000 1=1024 6=8000", "pipe c s", "s state", "pipe s c",
    "s data 1 len=150", "s data 1 len=100", "s windows 1", "pipe s c",
    "c settings 4=65535", "pipe c s", "s windows 1", "pipe s c", "c state")

job("invalid SETTINGS values",
    *hello(),
    "c settings 2=2", "c settings 4=2147483648", "c settings 5=100", "c settings 6=-1",
    "c settings 8=3", "c settings 99=1", "pipe c s", "pipe s c")

job("a concurrency limit",
    *hello(),
    "s settings 3=2", "pipe s c", "pipe c s",
    f"c headers 1 {GET}", "c headers 3 :method=GET :path=/2 :scheme=https :authority=shop.example",
    "c headers 5 :method=GET :path=/3 :scheme=https :authority=shop.example",
    "c reset 1", "c headers 5 :method=GET :path=/3 :scheme=https :authority=shop.example",
    "c state", "pipe c s", "s state")

# ---- push, priority, alt-svc, ping, reset, goaway

job("server push",
    *hello(),
    f"c headers 1 {GET} end", "pipe c s",
    "s push 1 2 :method=GET :path=/app.js :scheme=https :authority=shop.example",
    "s push 1 4 :method=GET :path=/app.css :scheme=https :authority=shop.example",
    "s headers 1 :status=200", "s data 1 <script~ssrc~e/app.js> end",
    "s headers 2 :status=200 content-type=text/javascript", "s data 2 alert(1) end",
    "s state", "pipe s c", "c state",
    "c reset 4 8", "pipe c s", "s headers 4 :status=200", "s state",
    "s push 2 6 :method=GET :path=/x :scheme=https :authority=shop.example",
    "s push 1 4 :method=GET :path=/y :scheme=https :authority=shop.example",
    "c push 1 3 :method=GET :path=/z :scheme=https :authority=shop.example")

job("push refused by the client",
    *hello(),
    "c settings 2=0", "pipe c s", "pipe s c",
    f"c headers 1 {GET} end", "pipe c s",
    "s push 1 2 :method=GET :path=/a.js :scheme=https :authority=shop.example")

job("priority signals",
    *hello(),
    f"c headers 1 {GET} w=32 d=0 x=1 end",
    "c headers 3 :method=GET :path=/b :scheme=https :authority=shop.example w=200 end",
    "c prio 3 w=1 d=1 x=0", "c prio 5 w=256", "c prio 7", "c prio 3 d=3", "c prio 3 w=0",
    "c headers 9 :method=GET :path=/c :scheme=https :authority=shop.example w=300",
    "pipe c s", "s prio 1 w=10", "s headers 1 :status=200 w=10 end")

job("alternative services",
    *hello(),
    f"c headers 1 {GET} end", "pipe c s",
    "s altsvc h3~e\":443\";~sma~e86400 origin=https://shop.example",
    "s altsvc h3~e\":8443\" sid=1", "s altsvc v sid=1 origin=x",
    "s headers 1 :status=200 end", "s altsvc late sid=1", "pipe s c",
    "c altsvc nope origin=x")

job("ping and pong",
    *hello(),
    "c ping 12345678", "c ping short", "pipe c s", "pipe s c", "s ping hex=0001020304050607",
    "pipe s c", "pipe c s")

job("reset streams in both directions",
    *hello(),
    f"c headers 1 {GET}", "c headers 3 :method=GET :path=/2 :scheme=https :authority=shop.example",
    "pipe c s", "c reset 1 8", "pipe c s",
    "s headers 1 :status=200", "s data 1 late", "s reset 3", "pipe s c",
    "c data 3 after~sreset", "c reset 3", "c reset 11", "c state", "s state")

job("data that arrives after the client reset the stream",
    *hello(),
    f"c headers 1 {GET} end", "pipe c s",
    "s headers 1 :status=200", "s data 1 len=5000", "c reset 1 8", "pipe s c",
    "c show", "pipe c s", "s data 1 more", "s state")

job("GOAWAY",
    *hello(),
    f"c headers 1 {GET} end", "c headers 3 :method=GET :path=/2 :scheme=https :authority=shop.example end",
    "pipe c s",
    "s goaway code=0 last=1 data=shutting~sdown", "s headers 1 :status=200", "pipe s c",
    "c headers 5 :method=GET :path=/3 :scheme=https :authority=shop.example",
    "c goaway code=2", "c state", "s state")

job("closing a connection",
    *hello(),
    "c goaway code=11 data=len=30", "pipe c s", "s goaway", "s show",
    "s new server", "s goaway code=1", "s show")

# ---- local errors

job("calls the state machine refuses",
    "c new client", "s new server",
    "c data 1 x", "c end 1", "c reset 1", "c windows 1", "c ack 10 0", "c ack -1 1",
    "s headers 1 :status=200", "c initiate",
    f"c headers 2 {GET}", f"c headers 1 {GET} end", f"c headers 1 {GET}", "c data 1 x",
    "c headers 1 x-late=1", "c headers 1 :status=200 end",
    "s initiate", "pipe c s", f"s headers 1 :method=GET :path=/ :scheme=https :authority=x",
    "s headers 3 :status=200", "s headers 2 :status=200 end", "c state", "s state")

job("outbound header validation",
    *hello(),
    "c headers 1 :method=GET :path=/ :scheme=https end",
    "c headers 3 :method=GET :path=/ :scheme=https :authority=a host=b end",
    "c headers 5 :method=GET :path= :scheme=https :authority=a end",
    "c headers 7 :method=GET :path=/ :scheme=https :authority=a te=gzip end",
    "c headers 9 :method=GET :path=/ :scheme=https :authority=a :status=200 end",
    "c headers 11 :method=GET :path=/ :scheme=https :authority=a :protocol=websocket end",
    "c headers 13 :method=GET :path=/ :scheme=https :authority=a :foo=bar end",
    "c headers 15 :method=GET :path=/ :scheme=https :authority=a :method=POST end",
    "c headers 17 :method=CONNECT :protocol=websocket :path=/chat :scheme=https :authority=a end",
    "c headers 19 x-early=1 :method=GET :path=/ :scheme=https :authority=a end",
    "c state", "pipe c s")

job("outbound validation turned off",
    *hello(copts=" validate_outbound_headers=0 normalize_outbound_headers=0"),
    "c headers 1 :method=GET :path=/ :scheme=https :authority=a X-Upper=1 end", "pipe c s", "s show")

for i, (label, hs) in enumerate([
        ("an uppercase name", ":method=GET :path=/ :scheme=https :authority=a Accept=x"),
        ("a name with a trailing space", ":method=GET :path=/ :scheme=https :authority=a accept~s=x"),
        ("a value with a leading space", ":method=GET :path=/ :scheme=https :authority=a accept=~sx"),
        ("a connection header", ":method=GET :path=/ :scheme=https :authority=a connection=close"),
        ("TE that is not trailers", ":method=GET :path=/ :scheme=https :authority=a te=chunked"),
        ("TE in capitals", ":method=GET :path=/ :scheme=https :authority=a te=TRAILERS"),
        ("no :path", ":method=GET :scheme=https :authority=a"),
        ("no host at all", ":method=GET :path=/ :scheme=https"),
        ("Host instead of :authority", ":method=GET :path=/ :scheme=https host=a"),
        ("host and :authority disagree", ":method=GET :path=/ :scheme=https :authority=a host=b"),
        ("a duplicate pseudo-header", ":method=GET :method=GET :path=/ :scheme=https :authority=a"),
        ("a pseudo-header after a regular one", ":method=GET :path=/ :scheme=https y=1 :authority=a"),
        ("a custom pseudo-header", ":method=GET :path=/ :scheme=https :authority=a :x=1"),
        ("an empty name", ":method=GET :path=/ :scheme=https :authority=a ~z=1"),
        ("an empty :path", ":method=GET :path= :scheme=https :authority=a"),
        ("CONNECT with :protocol", ":method=CONNECT :protocol=websocket :path=/ :scheme=https :authority=a"),
]):
    job(f"inbound validation: {label}",
        *hello(copts=" validate_outbound_headers=0 normalize_outbound_headers=0"),
        f"c headers 1 {hs} end", "pipe c s", "s show")

job("inbound validation turned off",
    *hello(copts=" validate_outbound_headers=0 normalize_outbound_headers=0",
           sopts=" validate_inbound_headers=0 normalize_inbound_headers=0"),
    "c headers 1 :method=GET :path=/ :scheme=https Accept=x cookie=a cookie=b end", "pipe c s",
    "s headers 1 :status=200 end", "pipe s c")

job("response validation at the client",
    *hello(sopts=" validate_outbound_headers=0 normalize_outbound_headers=0"),
    f"c headers 1 {GET} end", f"c headers 3 {GET} end", "pipe c s",
    "s headers 1 :status=200 :path=/ end", "pipe s c", "c show")

job("trailers that carry a pseudo-header",
    *hello(sopts=" validate_outbound_headers=0"),
    f"c headers 1 {GET} end", "pipe c s",
    "s headers 1 :status=200", "s headers 1 :status=500 end", "pipe s c", "c show")

# ---- upgrade from HTTP/1.1

job("h2c upgrade",
    "c new client", "s new server", "c upgrade",
    "s upgrade " + base64.urlsafe_b64encode(SettingsFrame(0, settings={3: 100, 4: 1000, 6: 65536}).serialize_body()).decode(),
    "c state", "s state", "pipe c s", "pipe s c",
    "s headers 1 :status=200", "s data 1 upgraded end", "pipe s c", "c state", "c headers 1 y=1",
    "c headers 3 :method=GET :path=/2 :scheme=http :authority=a end", "pipe c s")

job("upgrade without a settings header",
    "s new server", "s upgrade", "s state")

# ---- raw frames from a misbehaving peer

E = Encoder()
bad_req = E.encode(REQ)

job("a bad preamble", "s new server", "s raw " + b"PRI * HTTP/1.1\r\n".hex(), "s show")
job("a preamble in pieces", "s new server",
    "s raw " + PREAMBLE[:5].hex(), "s raw " + (PREAMBLE[5:] + SettingsFrame(0).serialize()).hex(),
    "s raw " + hx(PingFrame(0, opaque_data=b"abcdefgh")), "s show")

E = Encoder()
job("headers in CONTINUATION frames",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(HeadersFrame(1, flags=["END_STREAM"], data=E.encode(REQ)[:3]),
                  ContinuationFrame(1, data=E.encode([])), ),
    "s show")

E = Encoder()
blk = E.encode(REQ + [("user-agent", "x" * 40)])
job("a header block split three ways, then interrupted",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(HeadersFrame(1, flags=["END_STREAM"], data=blk[:4]),
                  ContinuationFrame(1, data=blk[4:20]),
                  ContinuationFrame(1, flags=["END_HEADERS"], data=blk[20:])),
    "s raw " + hx(HeadersFrame(3, flags=["END_STREAM"], data=blk[:4]), PingFrame(0, opaque_data=b"12345678")),
    "s show")

E = Encoder()
blk = E.encode(REQ)
job("CONTINUATION on another stream",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(HeadersFrame(1, data=blk[:4]), ContinuationFrame(3, flags=["END_HEADERS"], data=blk[4:])),
    "s show")

job("a naked CONTINUATION",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(ContinuationFrame(1, flags=["END_HEADERS"], data=b"\x82")), "s show")

E = Encoder()
job("data before headers, and on stream 0",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(DataFrame(1, data=b"oops")), "s show",
    "s new server", "s raw " + hx(opening()), "s raw " + hx(b"\x00\x00\x02\x00\x00\x00\x00\x00\x00hi"), "s show")

E = Encoder()
job("a frame over the maximum size, and a frame with a bad padding length",
    "s new server", "s raw " + hx(opening()),
    "s raw " + (b"\x00\x40\x01\x00\x00\x00\x00\x00\x01" + b"\x00" * 16385).hex(), "s show",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(hdr_frame(E, 1, REQ)),
    "s raw " + hx(b"\x00\x00\x03\x00\x08\x00\x00\x00\x01\x05ab"), "s show")

E = Encoder()
job("an unknown frame type and an unknown setting",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(b"\x00\x00\x03\xfa\x07\x00\x00\x00\x05abc"),
    "s raw " + hx(SettingsFrame(0, settings={0x42: 7, 4: 70000})), "s show", "s state")

E = Encoder()
job("stream identifiers out of order",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(hdr_frame(E, 5, REQ, flags=("END_HEADERS", "END_STREAM"))),
    "s raw " + hx(hdr_frame(E, 3, REQ, flags=("END_HEADERS", "END_STREAM"))), "s show",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(hdr_frame(Encoder(), 2, REQ)), "s show")

E = Encoder()
job("headers on a stream that has ended",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(hdr_frame(E, 1, REQ, flags=("END_HEADERS", "END_STREAM"))),
    "s headers 1 :status=200 end", "s state",
    "s raw " + hx(hdr_frame(E, 1, REQ, flags=("END_HEADERS", "END_STREAM"))), "s show")

E = Encoder()
job("headers on a half-closed stream",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(hdr_frame(E, 1, REQ, flags=("END_HEADERS", "END_STREAM"))),
    "s raw " + hx(hdr_frame(E, 1, [("x-more", "1")], flags=("END_HEADERS", "END_STREAM"))),
    "s show", "s state")

E = Encoder()
job("a stream reset, then more frames on it",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(hdr_frame(E, 1, REQ)), "s reset 1 7",
    "s raw " + hx(DataFrame(1, data=b"late"), WindowUpdateFrame(1, window_increment=5)),
    "s raw " + hx(hdr_frame(E, 1, [("x-trailer", "1")], flags=("END_HEADERS", "END_STREAM"))),
    "s show", "s state")

E = Encoder()
job("window updates that are wrong",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(hdr_frame(E, 1, REQ)),
    "s raw " + hx(b"\x00\x00\x04\x08\x00\x00\x00\x00\x01\x00\x00\x00\x00"), "s show",
    "s new server", "s raw " + hx(opening()), "s raw " + hx(hdr_frame(Encoder(), 1, REQ)),
    "s raw " + hx(WindowUpdateFrame(1, window_increment=2147483647)), "s show", "s state",
    "s raw " + hx(WindowUpdateFrame(0, window_increment=2147483647)), "s show")

E = Encoder()
job("RST_STREAM and PRIORITY on idle streams",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(RstStreamFrame(7, error_code=8), PriorityFrame(9, depends_on=1, stream_weight=99, exclusive=True)),
    "s raw " + hx(PriorityFrame(11, depends_on=11)), "s show")

E = Encoder()
job("PUSH_PROMISE sent to a server, and from a client",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(hdr_frame(E, 1, REQ)),
    "s raw " + hx(PushPromiseFrame(1, promised_stream_id=2, data=E.encode(REQ), flags=["END_HEADERS"])), "s show")

E = Encoder()
job("PRIORITY inside HEADERS",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(hdr_frame(E, 1, REQ, flags=("END_HEADERS", "PRIORITY", "END_STREAM"),
                            depends_on=0, stream_weight=41, exclusive=True)),
    "s raw " + hx(hdr_frame(E, 3, REQ, flags=("END_HEADERS", "PRIORITY"), depends_on=3, stream_weight=0)),
    "s show")

job("a broken header block",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(HeadersFrame(1, flags=["END_HEADERS"], data=b"\xff\xff\xff\xff\xff\x7f")), "s show",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(HeadersFrame(1, flags=["END_HEADERS"], data=b"\x00\x01a\x02\xc3\x28")), "s show")

E = Encoder()
blk = E.encode(REQ + [("x-big-%d" % i, "v" * 4000) for i in range(17)])
parts = [blk[i:i + 16000] for i in range(0, len(blk), 16000)]
job("a header list over the limit",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(HeadersFrame(1, data=parts[0]), *[ContinuationFrame(1, data=p) for p in parts[1:-1]],
                  ContinuationFrame(1, flags=["END_HEADERS"], data=parts[-1])), "s show")

E = Encoder()
job("GOAWAY and PING from a raw peer",
    "s new server", "s raw " + hx(opening()),
    "s raw " + hx(PingFrame(0, opaque_data=b"\x00" * 8, flags=["ACK"]),
                  GoAwayFrame(0, last_stream_id=0, error_code=99, additional_data=b"x" * 25)),
    "s show", "s state", f"s headers 2 :status=200")

E = Encoder()
job("a client fed a server's mistakes",
    "c new client", "c initiate", "c raw " + hx(SettingsFrame(0)),
    f"c headers 1 {GET} end",
    "c raw " + hx(HeadersFrame(1, flags=["END_HEADERS"], data=Encoder().encode([(":status", "200")])),
                  DataFrame(1, data=b"abc", flags=["END_STREAM"]),
                  DataFrame(1, data=b"more")),
    "c show", "c state")

E = Encoder()
job("a client fed a push for a reset stream",
    "c new client", "c initiate", "c raw " + hx(SettingsFrame(0)),
    f"c headers 1 {GET} end", "c reset 1", "c drop",
    "c raw " + hx(PushPromiseFrame(1, promised_stream_id=2, data=E.encode(REQ), flags=["END_HEADERS"])),
    "c show",
    "c raw " + hx(PushPromiseFrame(3, promised_stream_id=4, data=E.encode(REQ), flags=["END_HEADERS"])),
    "c show")

# ---- delivery in pieces

job("delivery a few bytes at a time",
    "c new client", "s new server", "c initiate", "s initiate",
    f"c headers 1 {GET} end",
    "pipe c s 10", "pipe c s 30", "pipe c s 7", "pipe c s 1", "pipe c s 100", "pipe c s",
    "pipe s c 20", "pipe s c", "s headers 1 :status=200", "s data 1 abcdefghij end",
    "pipe s c 12", "pipe s c 1", "pipe s c", "c state")

with open(os.path.join(HERE, "data", "jobs.txt"), "w", encoding="utf-8") as fh:
    for title, lines in JOBS:
        fh.write(f"job {title}\n")
        for line in lines:
            fh.write(line + "\n")
print(f"{len(JOBS)} jobs")
