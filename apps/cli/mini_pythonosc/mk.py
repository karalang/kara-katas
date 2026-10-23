#!/usr/bin/env python3
r"""Writes data/jobs.tsv for mini_pythonosc: the Open Sound Control traffic
of a small theatre rig (a lighting desk, a QLab cue machine, a TouchOSC
tablet and a digital mixer), one job per line, tab-separated, the first
field naming the kind.

Values use a small grammar, space-separated:
  iN  fX  s<hex utf-8>  b<hex>  T  F  N  mA,B,C,D (a 4-tuple)  uA,B,C (a
  3-tuple)  ( ... ) a list;  any value may end in @<type>, a type letter or
  <a,b,...> for a list of types.  An address is "-" for None or "x<hex>".

  build <label> <addr> <args...>   OscMessageBuilder: add_arg each, build()
  bmsg <addr> <value|->            build_msg(address, value), "-" = default
  parse <hex>                      OscMessage(dgram)
  bundle <label> <ts> <labels...>  OscBundleBuilder(ts) over earlier labels
  bparse <hex>                     OscBundle(dgram)
  packet <now> <hex>               OscPacket(dgram) with the clock at <now>
  ntp <op> <arg>                   tontp <ts> | tosys <hex> | parse <u64>
  slip <op> <hex>                  enc | dec | valid
  match <maps> <pattern>           which mapped addresses a pattern reaches
  serve <mode> <now> <setup> <in>  a server: udp (datagrams split on ","),
                                   tcp10 (length-prefixed) or tcp11 (SLIP)
Lists inside a field are split on \x1f. A timestamp is imm, iN or fX.
Run: python3 -s -P -B mk.py"""
import os
import struct

US = "\x1f"
jobs = []


def add(*f):
    jobs.append("\t".join(str(x) for x in f))


def a(s):
    return "-" if s is None else "x" + s.encode("utf-8").hex()


def s(t):
    return "s" + t.encode("utf-8").hex()


def b(bs):
    return "b" + bytes(bs).hex()


def osc_str(t):
    d = t.encode("utf-8")
    return d + b"\x00" * (4 - len(d) % 4)


def raw(addr, tags=None, payload=b""):
    d = osc_str(addr)
    if tags is not None:
        d += osc_str(tags)
    return (d + payload).hex()


# ---- building messages, explicit and inferred types
B = [
    ("go", "/cue/12/go", []),
    ("fader", "/mixer/ch/3/fader", ["f0.75"]),
    ("mute", "/mixer/ch/3/mute", ["T"]),
    ("unmute", "/mixer/ch/3/mute", ["F"]),
    ("dimmer", "/light/dimmer/7", ["i255"]),
    ("name", "/cue/12/name", [s("Act 2 — Storm")]),
    ("rgb", "/light/led/1/color", ["i4278255360@r"]),
    ("note", "/midi/out", ["m0,144,60,100"]),
    ("xy", "/touchosc/xy1", ["f0.1", "f-0.5"]),
    ("all", "/test/all", ["i-7", "f3.25", s("ok"), b([1, 2, 3]), "T", "F", "N", "m1,2,3,4",
                          "f2.5@d", "i9000000000", "i-2147483648", "i2147483647"]),
    ("arr", "/scene/recall", ["( i1 i2 ( f1.5 s" + "ab".encode().hex() + " ) )", "i3"]),
    ("typed", "/scene/levels", ["( i1 f2 s" + "x".encode().hex() + " )@<f,d,s>"]),
    ("chars", "/osc/chars", [s("hey") + "@<s,s>"]),
    ("short", "/osc/zip", ["( i1 i2 i3 )@<i,f>"]),
    ("blob", "/data/blob", [b(range(1, 6))]),
    ("blob4", "/data/blob4", [b([9, 8, 7, 6])]),
    ("emptys", "/data/empty", [s("")]),
    ("pad3", "/abc", [s("xyz")]),
    ("pad4", "/abcd", [s("wxyz")]),
    ("utf8", "/titles/ünïcode", [s("日本語"), s("🎭")]),
    ("dbl", "/clock/drift", ["f0.1@d", "i3@d", "T@d"]),
    ("ints", "/counter", ["f2.0@i"]),
    (None, "/bad/int", ["i2147483648@i"]),
    (None, "/bad/int2", [s("12") + "@i"]),
    (None, "/bad/rgba", ["i-1@r"]),
    (None, "/bad/rgba2", ["i4294967296@r"]),
    ("rgbaok", "/rgba/ok", ["T@r", "i0@r"]),
    (None, "/bad/float", [s("x") + "@f"]),
    (None, "/bad/float2", ["f1e300"]),
    ("fl", "/float/edge", ["f3.4028234663852886e+38", "f1e-46", "f-0.0", "finf", "fnan", "f16777217.0",
                           "f0.30000000000000004", "i16777217@f"]),
    (None, "/bad/double", ["N@d"]),
    (None, "/bad/string", ["i5@s"]),
    (None, "/bad/string2", ["N@s"]),
    (None, "/bad/string3", ["( i1 )@s"]),
    (None, "/bad/blob", [b([]) ]),
    (None, "/bad/blob2", [s("") + "@b"]),
    (None, "/bad/blob3", ["i0@b"]),
    (None, "/bad/blob4", ["i5@b"]),
    (None, "/bad/blob5", [s("abc") + "@b"]),
    (None, "/bad/blob6", ["( i1 )@b"]),
    (None, "/bad/midi", ["u1,2,3"]),
    (None, "/bad/midi2", ["u1,2,3@m"]),
    (None, "/bad/midi3", ["i5@m"]),
    (None, "/bad/midi4", [s("abcd") + "@m"]),
    ("midib", "/midi/bytes", [b([0x90, 0x3C, 0x64, 0x00]) + "@m", "( i1 i300 i-1 i2 )@m"]),
    (None, "/bad/type", ["i1@t"]),
    (None, "/bad/type2", ["i1@<i,x>"]),
    (None, "/bad/iter", ["i5@<i>"]),
    ("emptyty", "/empty/type", ["i5@<>"]),
    ("nested", "/a/b", ["( ( ( N ) ) )"]),
    ("emptyl", "/list/empty", ["( )"]),
    ("nul", "/nul/inside", [s("a\x00bcdefg")]),
    (None, None, ["i1"]),
    (None, "", ["i1"]),
    ("comma", ",", []),
    ("bang", "/bang", ["N", "N"]),
]
for label, addr, args in B:
    add("build", label or "-", a(addr), " ".join(args))

# build_msg, as SimpleUDPClient.send_message calls it
for addr, val in [("/cue/1/go", "-"), ("/v", "i5"), ("/v", s("text")), ("/v", b([1, 2])), ("/v", "( i1 f2.5 )"),
                  ("/v", "m1,2,3,4"), ("/v", "N"), ("/v", s("")), ("/v", "( )"), ("/v", "( ( i1 ) )"),
                  ("/v", "T"), ("/v", "u1,2,3"), ("", "i1")]:
    add("bmsg", a(addr), val)

# ---- parsing raw datagrams, including what other senders put on the wire
P = [
    raw("/cue/5/go"),
    raw("/x", ","),
    raw("/x", ",i", struct.pack(">i", -42)),
    raw("/x", ",ihfd", struct.pack(">iqfd", 1, 2**40, 0.5, 1e-3)),
    raw("/x", ",sb", osc_str("hi") + struct.pack(">i", 3) + b"\x01\x02\x03\x00"),
    raw("/x", ",rm", struct.pack(">II", 0xFF8000C0, 0x0190407F)),
    raw("/x", ",TFN"),
    raw("/x", ",[i[f]]", struct.pack(">if", 7, 2.0)),
    raw("/x", ",t", struct.pack(">II", 3913056000, 0x80000000)),
    raw("/x", ",t", struct.pack(">II", 0, 1)),
    raw("/x", ",t", struct.pack(">II", 0xFFFFFFFF, 0xFFFFFFFF)),
    raw("/x", ",f", b"\x3f\x80"),              # Reaktor's short float
    raw("/x", ",f"),                          # nothing at all
    raw("/x", ",i", b"\x00\x01"),
    raw("/x", ",d", b"\x00" * 7),
    raw("/x", ",h", b"\x00" * 4),
    raw("/x", ",s", b"abc"),
    raw("/x", ",s", b"abcd"),
    raw("/x", ",b", struct.pack(">i", 8) + b"\x01\x02"),
    raw("/x", ",bf", struct.pack(">i", 1) + b"\x07"),
    raw("/x", ",bi", struct.pack(">i", -20) + struct.pack(">ii", 5, 6)),
    raw("/x", ",bd", struct.pack(">i", -12) + b"\x00" * 8),
    raw("/x", "i", struct.pack(">i", 1)),
    raw("/x", ",ii[", struct.pack(">ii", 1, 2)),
    raw("/x", ",i]", struct.pack(">i", 1)),
    raw("/x", ",qi", struct.pack(">i", 9)),
    raw("/x", ",cS", b""),
    raw("/titles/café", ",s", osc_str("crème")),
    "2f61",
    "",
    "2f616263",
    raw("/x") + "00000000",
    raw("/x", ",f", struct.pack(">I", 0x7F800000)),
    raw("/x", ",ff", struct.pack(">II", 0x00000001, 0x80000000)),
    raw("/x", ",f", struct.pack(">I", 0x7FC00000)),
]
for h in P:
    add("parse", h or "-")


# ---- bundles
BUN = [
    ("b1", "imm", ["go", "fader"]),
    ("b2", "f1700000000.25", ["mute", "b1"]),
    ("b3", "i1700000010", ["dimmer"]),
    ("b4", "f0.0", ["go"]),
    ("b5", "i0", []),
    ("b6", "f1.5", ["b2", "b3", "name"]),
    (None, "f-2208988801.0", ["go"]),
    (None, "fnan", ["go"]),
    (None, "finf", ["go"]),
    (None, "f1e20", ["go"]),
    ("b7", "f-2208988800.0", ["go"]),
    ("b8", "f2085978495.9999998", ["go"]),
]
for label, ts, items in BUN:
    add("bundle", label or "-", ts, " ".join(items))

BP = [
    b"#bundle\x00".hex() + "0000000000000001",
    b"#bundle\x00".hex() + "00000000",
    b"#bundle\x00".hex(),
    b"#bundle\x00".hex() + "0000000000000001" + "0000000c" + raw("/a", ",i", struct.pack(">i", 1)),
    b"#bundle\x00".hex() + "0000000000000001" + "00000008" + "2f61000000000000",
    b"#bundle\x00".hex() + "0000000000000001" + "00000008" + "7a7a7a7a7a7a7a7a",
    b"#bundle\x00".hex() + "0000000000000001" + "0000",
    b"#bundle\x00".hex() + "0000000000000001" + "00000040" + raw("/a"),
    b"#bundle\x00".hex() + "0000000000000001" + "00000010" + b"#bundle\x00".hex() + "0000",
    b"#bundle\x00".hex() + "0000000000000001" + "00000008" + raw("/a", "i"),
    b"#bundle\x00".hex() + "e8a8f8c040000000" + "00000008" + raw("/b"),
]
for h in BP:
    add("bparse", h)

NOW = "1700000005.5"
for h in [raw("/cue/1/go"), "", "7a7a", b"#bundle\x00".hex() + "0000000000000001" + "00000008" + raw("/a", "i"),
          raw("/x", ",i", b"\x00")]:
    add("packet", NOW, h or "-")

# ---- NTP and SLIP helpers
for ts in ["imm", "i0", "f1700000000.5", "i-2208988800", "i-2208988801", "f2085978495.0", "f2085978496.0",
           "fnan", "f-inf", "f1e-10", "f123.456"]:
    add("ntp", "tontp", ts)
for h in ["0000000000000000", "8000000000000000", "e8a8f8c040000000", "ffffffffffffffff", "0102", "-"]:
    add("ntp", "tosys", h)
for n in ["0", "1", "4294967296", "18446744073709551615", "16827547062009102336"]:
    add("ntp", "parse", n)

for h in ["", "010203", "c0", "db", "c0db", "68656c6c6fc0776f726c64db", "dbdc"]:
    add("slip", "enc", h or "-")
for h in ["c00102c0", "c0dbdcdbddc0", "c0c0c0", "", "c0dbc0", "dbdb", "c0db", "0102", "c001c002c0",
          "c0c001c0c0", "dbdddbdc", "c0dbddc0c0"]:
    add("slip", "dec", h or "-")
    add("slip", "valid", h or "-")

# ---- address pattern matching
MAPS = ["/mixer/ch/1/fader", "/mixer/ch/2/fader", "/mixer/ch/10/fader", "/mixer/ch/1/mute",
        "/mixer/bus/a", "/light/dimmer/7", "/cue/12/go", "/cue/12/name", "/a.b", "a/b",
        "/odd-name", "/x+y"]
WILD = ["/mixer/*", "/cue/*/go", "/light/dim+er/7", "/a.c", "/opt?/x"]
for pat in ["/mixer/ch/1/fader", "/mixer/ch/?/fader", "/mixer/ch/*/fader", "/mixer/ch/1*",
            "/mixer/ch/[12]/fader", "/mixer/ch/[!1]/fader", "/mixer/ch/[0-9]/fader",
            "/mixer/ch/[0-9][0-9]/fader", "/mixer/{ch,bus}/*", "/mixer/ch/{1,10}/fader",
            "/cue/12/{go,name}", "/*/*/*", "/*", "*", "/mixer/ch/1/*e*", "/a.b", "/a?b", "/a[.]b",
            "/odd-name", "/odd[-]name", "/x+y", "/[a-c].b", "/mixer/ch/[]/fader", "/mixer/ch/[z-a]/fader",
            "/mixer/ch/[!]/fader", "/cue/{}/go", "/cue/{12,}/go", "/mixer/ch/[1-]/fader",
            "/light/dimmer/7", "/light/dimmmer/7", "/opt/x", "/op/x", "/mixer/bus/a/b", "/a.c", "/abc",
            "/mixer/ch/1/fader/", "/mixer/ch/[\\]/fader", "/[^m]ixer/bus/a", "/mixer/b(us)/a",
            "/mixer/b$/a", "/cue/12/go?"]:
    add("match", US.join(MAPS + WILD), pat)

# ---- servers: a dispatcher, the clock at <now>, and what arrives
SETUP = US.join([
    "map /mixer/ch/*/fader log",
    "map /mixer/ch/1/fader echo",
    "map /cue/*/go ack",
    "map /cue/12/go log i1 " + s("stage-left"),
    "mapr /who who",
    "map /bad bad",
    "map /empty empty",
    "default log",
])


def msg(addr, *args):
    from_tags = "".join(t for t, _ in args)
    payload = b"".join(p for _, p in args)
    return raw(addr, "," + from_tags, payload)


def i32(v):
    return ("i", struct.pack(">i", v))


def f32(v):
    return ("f", struct.pack(">f", v))


def bundle(ts_hex, *contents):
    out = b"#bundle\x00".hex() + ts_hex
    for c in contents:
        out += "%08x" % (len(c) // 2) + c
    return out


def ntp_hex(t):
    return "%016x" % int((t + 2208988800) * 2**32)


UDP_IN = ",".join([
    msg("/mixer/ch/1/fader", f32(0.5)),
    msg("/mixer/ch/4/fader", f32(0.25)),
    msg("/cue/12/go"),
    msg("/cue/3/go"),
    msg("/unknown/addr", i32(1)),
    msg("/who", i32(2)),
    msg("/mixer/ch/[1-2]/fader", f32(1.0)),
    msg("/mixer/*/1/fader", f32(0.0)),
    "7a7a7a7a",
    bundle("0000000000000001", msg("/cue/12/go"), msg("/mixer/ch/1/fader", f32(0.125))),
    bundle(ntp_hex(1700000007.5), msg("/cue/3/go"), bundle(ntp_hex(1700000006.0), msg("/mixer/ch/2/fader", f32(0.5))),
           msg("/mixer/ch/1/fader", f32(0.75))),
    bundle(ntp_hex(1600000000.0), msg("/cue/7/go")),
    msg("/bad"),
    msg("/mixer/ch/1/fader", ("s", osc_str("x"))),
    msg("/empty"),
    msg("/cue/12/go", ("i", b"\x00")),
    "",
])
add("serve", "udp", "1700000005.0", SETUP, UDP_IN)

SETUP2 = US.join(["strict 0"] + SETUP.split(US))
add("serve", "udp", "1700000005.0", SETUP2,
    bundle(ntp_hex(1700000009.0), msg("/cue/3/go"), msg("/mixer/ch/1/fader", f32(0.5))))

SETUP3 = US.join(["map /cue/1/go log", "unmap /cue/1/go log", "unmap /cue/9/go log", "unmap /never ack",
                  "default ack", "map /m log", "map /m log", "unmap /m log"])
add("serve", "udp", "1700000005.0", SETUP3, ",".join([msg("/cue/1/go"), msg("/cue/9/go"), msg("/never"),
                                                       msg("/other"), msg("/m", i32(1))]))
add("serve", "udp", "1700000005.0", US.join(["map /a log", "default -"]), ",".join([msg("/a"), msg("/b")]))

tcp10 = ""
for m in [msg("/mixer/ch/1/fader", f32(0.5)), msg("/cue/12/go"), msg("/who")]:
    tcp10 += "%08x" % (len(m) // 2) + m
add("serve", "tcp10", "1700000005.0", SETUP, tcp10)
add("serve", "tcp10", "1700000005.0", SETUP, tcp10 + "000000" )
add("serve", "tcp10", "1700000005.0", SETUP, "%08x" % 40 + msg("/cue/12/go"))
add("serve", "tcp10", "1700000005.0", SETUP, "00000008" + msg("/bad") + "%08x" % 12 + msg("/cue/12/go"))


def slip_enc(h):
    d = bytes.fromhex(h)
    return (b"\xc0" + d.replace(b"\xdb", b"\xdb\xdd").replace(b"\xc0", b"\xdb\xdc") + b"\xc0").hex()


tcp11 = "".join(slip_enc(m) for m in [msg("/mixer/ch/1/fader", f32(0.5)), msg("/cue/3/go"),
                                       msg("/who", ("b", struct.pack(">i", 2) + b"\xc0\xdb\x00\x00"))])
add("serve", "tcp11", "1700000005.0", SETUP, tcp11)
add("serve", "tcp11", "1700000005.0", SETUP, slip_enc(msg("/cue/12/go")) + "c0dbc0")
add("serve", "tcp11", "1700000005.0", SETUP, slip_enc(msg("/cue/12/go"))[:-2])
add("serve", "tcp11", "1700000005.0", SETUP, "c0c0" + slip_enc(msg("/mixer/ch/1/fader", f32(0.5))))
add("serve", "tcp11", "1700000005.0", SETUP, slip_enc(msg("/bad")) + slip_enc(msg("/cue/12/go")))

os.makedirs("data", exist_ok=True)
with open("data/jobs.tsv", "w", encoding="utf-8") as fh:
    fh.write("\n".join(jobs) + "\n")
print(len(jobs), "jobs")
