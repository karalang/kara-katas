#!/usr/bin/env python3
"""Runs data/jobs.tsv with the real msgpack (1.2.3): its pure-Python
reference implementation, msgpack.fallback, whose messages the port
follows, checked byte for byte against the C extension wherever it
packs. mini_msgpack.kara prints the same thing."""
import binascii
import json
import struct

import msgpack
from msgpack import ExtType, Timestamp, fallback

LIMIT = 2000


def short(s):
    if len(s) > LIMIT:
        return s[:LIMIT] + "... (%d chars)" % len(s)
    return s


def hexdump(b):
    out = ["  %d bytes" % len(b)]
    shown = b if len(b) <= 256 else b[:64]
    for i in range(0, len(shown), 16):
        out.append("  " + " ".join("%02x" % x for x in shown[i:i + 16]))
    if len(b) > 256:
        out.append("  ...")
        out.append("  " + " ".join("%02x" % x for x in b[-16:]))
    return out


def conv(v):
    """The JSON conventions for what JSON cannot spell."""
    if isinstance(v, list):
        return [conv(x) for x in v]
    if isinstance(v, dict):
        if len(v) == 1:
            (k, a), = v.items()
            if k == "$bin":
                return bytes.fromhex(a)
            if k == "$ext":
                return ExtType(a[0], bytes.fromhex(a[1]))
            if k == "$ts":
                return Timestamp(a[0], a[1])
            if k == "$tuple":
                return tuple(conv(x) for x in a)
            if k == "$repeat":
                return a[0] * a[1]
            if k == "$binrepeat":
                return bytes.fromhex(a[0]) * a[1]
            if k == "$range":
                return list(range(a))
            if k == "$map":
                return {"k%d" % i: i for i in range(a)}
        return {k: conv(x) for k, x in v.items()}
    return v


def opts(words):
    o = {}
    for w in words:
        k, v = w.split("=")
        o[k] = int(v)
    return o


def unpacker_args(o, n=None):
    a = {}
    if n is not None:
        a["max_buffer_size"] = n
    if "max_buffer" in o:
        a["max_buffer_size"] = o["max_buffer"]
    for k, name in [("raw", "raw"), ("list", "use_list"), ("ts", "timestamp"),
                    ("strict", "strict_map_key"), ("max_str", "max_str_len"),
                    ("max_bin", "max_bin_len"), ("max_array", "max_array_len"),
                    ("max_map", "max_map_len"), ("max_ext", "max_ext_len")]:
        if k in o:
            v = o[k]
            a[name] = bool(v) if k in ("raw", "list", "strict") else v
    return a


def err(e):
    msg = str(e)
    name = type(e).__name__
    return "  error: " + name + (": " + msg if msg else "")


def unpackb(data, o):
    u = fallback.Unpacker(None, **unpacker_args(o, len(data)))
    u.feed(data)
    try:
        ret = u._unpack()
    except fallback.OutOfData:
        raise ValueError("Unpack failed: incomplete input")
    if u._got_extradata():
        raise msgpack.ExtraData(ret, u._get_extradata())
    return ret


def run_pack(name, o):
    text = open("data/json/%s.json" % name).read()
    try:
        value = conv(json.loads(text))
        p = fallback.Packer(use_bin_type=bool(o.get("bin", 1)),
                            use_single_float=bool(o.get("single", 0)))
        b = p.pack(value)
    except Exception as e:
        return [err(e)]
    c = msgpack.packb(value, use_bin_type=bool(o.get("bin", 1)),
                      use_single_float=bool(o.get("single", 0)))
    assert b == c, name
    out = hexdump(b)
    try:
        out.append("  = " + short(repr(unpackb(b, {}))))
    except Exception as e:
        out.append("  =" + err(e)[1:])
    return out


def run_unpack(name, o):
    data = open("data/bin/%s.mp" % name, "rb").read()
    try:
        v = unpackb(data, o)
    except Exception as e:
        return [err(e)]
    return ["  " + short(repr(v))]


def stream_objects(name, chunk, o, each):
    data = open("data/bin/%s.mp" % name, "rb").read()
    u = fallback.Unpacker(None, **unpacker_args(o))
    out = []
    try:
        for i in range(0, len(data), chunk):
            u.feed(data[i:i + chunk])
            for obj in u:
                out.extend(each(u, obj))
    except Exception as e:
        out.append(err(e))
        return out
    rest = len(u._buffer) - u._buff_i
    if rest:
        out.append("  rest %d bytes" % rest)
    return out


def run_stream(name, chunk, o):
    return stream_objects(name, chunk, o, lambda u, obj: ["  @%d %s" % (u.tell(), short(repr(obj)))])


def event_time(t):
    if isinstance(t, int):
        return "%d.000000000" % t
    if isinstance(t, ExtType) and t.code == 0 and len(t.data) == 8:
        s, ns = struct.unpack(">II", t.data)
        return "%d.%09d" % (s, ns)
    raise ValueError("bad time %r" % (t,))


def forward(u, obj):
    """One Fluentd forward-protocol message: Message, Forward or
    PackedForward mode."""
    try:
        if not isinstance(obj, list) or len(obj) < 2:
            raise ValueError("not a message: %s" % short(repr(obj)))
        tag = obj[0]
        out = []
        second = obj[1]
        if isinstance(second, list):
            entries, option = second, (obj[2] if len(obj) > 2 else None)
        elif isinstance(second, (bytes, str)):
            raw = second if isinstance(second, bytes) else second.encode("latin-1")
            sub = fallback.Unpacker(None, max_buffer_size=max(len(raw), 1))
            sub.feed(raw)
            entries = list(sub)
            option = obj[2] if len(obj) > 2 else None
        else:
            if len(obj) < 3:
                raise ValueError("not a message: %s" % short(repr(obj)))
            entries, option = [[obj[1], obj[2]]], (obj[3] if len(obj) > 3 else None)
        for e in entries:
            if not isinstance(e, list) or len(e) != 2:
                raise ValueError("bad entry: %s" % short(repr(e)))
            out.append("  %s %s %s" % (tag, event_time(e[0]), short(repr(e[1]))))
        if isinstance(option, dict) and "chunk" in option:
            out.append("  ack %s" % option["chunk"])
        return out
    except ValueError as e:
        return ["  rejected: %s" % e]


for line in open("data/jobs.tsv").read().split("\n"):
    if not line:
        continue
    w = line.split()
    print("== " + line)
    if w[0] == "pack":
        out = run_pack(w[1], opts(w[2:]))
    elif w[0] == "unpack":
        out = run_unpack(w[1], opts(w[2:]))
    elif w[0] == "stream":
        out = run_stream(w[1], int(w[2]), opts(w[3:]))
    elif w[0] == "forward":
        out = stream_objects(w[1], int(w[2]), {}, forward)
    print("\n".join(out))
