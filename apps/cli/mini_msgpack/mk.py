#!/usr/bin/env python3
"""Writes data/: JSON documents to pack in data/json/, MessagePack files
to unpack in data/bin/ (made with the real msgpack, by hand for unusual
encodings, and broken on purpose), and data/jobs.tsv, one job per line.
See README.md for the jobs."""
import json
import os
import shutil
import struct

import msgpack
from msgpack import ExtType, Timestamp

shutil.rmtree("data", ignore_errors=True)
os.makedirs("data/json")
os.makedirs("data/bin")

jobs = []


def doc(name, text):
    with open("data/json/" + name + ".json", "w") as f:
        f.write(text.strip("\n") + "\n")


def binf(name, data):
    with open("data/bin/" + name + ".mp", "wb") as f:
        f.write(data)


def job(line):
    jobs.append(line)


P = msgpack.packb

# ------------------------------------------------------------ JSON to pack

doc("package", """
{
  "name": "@acme/web-dashboard",
  "version": "3.14.1",
  "private": true,
  "description": "Operations dashboard for the \\"acme\\" fleet",
  "main": "dist/index.js",
  "scripts": {"build": "vite build", "test": "vitest run --coverage", "lint": "eslint ."},
  "dependencies": {"react": "^18.3.1", "react-dom": "^18.3.1", "zod": "3.23.8"},
  "engines": {"node": ">=20"},
  "files": [],
  "keywords": ["ops", "dashboard", "fleet"],
  "license": null
}
""")
doc("geojson", """
{"type": "FeatureCollection",
 "features": [
  {"type": "Feature", "id": 1,
   "geometry": {"type": "Point", "coordinates": [-122.4194, 37.7749]},
   "properties": {"name": "San Francisco", "population": 808437, "density": 7272.8}},
  {"type": "Feature", "id": 2,
   "geometry": {"type": "LineString",
                "coordinates": [[2.3522, 48.8566], [4.8357, 45.764], [5.3698, 43.2965]]},
   "properties": {"name": "Paris - Lyon - Marseille", "km": 775, "electrified": true}},
  {"type": "Feature", "id": 3,
   "geometry": {"type": "Polygon",
                "coordinates": [[[139.69, 35.68], [139.77, 35.68], [139.77, 35.72],
                                 [139.69, 35.72], [139.69, 35.68]]]},
   "properties": {"name": "\\u6771\\u4eac", "area_km2": 0.0315, "tags": ["capital", "\\ud83d\\uddfc"]}}
 ]}
""")
doc("ints", """
[0, 1, 127, 128, 255, 256, 65535, 65536, 4294967295, 4294967296,
 9223372036854775807, 9223372036854775808, 18446744073709551615,
 -1, -32, -33, -128, -129, -32768, -32769, -2147483648, -2147483649,
 -9223372036854775808, -0, 1000000007]
""")
doc("floats", """
[0.0, -0.0, 1.0, 0.1, -2.5, 3.141592653589793, 1e300, 2.2250738585072014e-308, 5e-324,
 1.7976931348623157e308, 1e16, 123456789.125, 1e-7, 6.02214076e23, 1e400, -1e400]
""")
doc("strings", """
["", "a", "hello, world", "it's", "say \\"hi\\"", "both ' and \\"", "back\\\\slash",
 "tab\\there", "line\\nbreak\\r\\n", "nul\\u0000and\\u001fus\\u007fdel",
 "caf\\u00e9", "\\u00a0nbsp", "\\u00adshy", "zero\\u200bwidth", "line\\u2028sep",
 "bom\\ufeff", "private\\ue000use", "\\u65e5\\u672c\\u8a9e", "emoji \\ud83d\\ude00\\ud83c\\udf89",
 "Gr\\u00fc\\u00dfe \\u03b1\\u03b2\\u03b3", "c1\\u0085next",
 "exactly thirty-one bytes long!!", "exactly thirty-two bytes long!!!",
 "a string that is longer than thirty-two bytes, so str8 (or raw16 without bin type)"]
""")
doc("dupes", """
{"id": 1, "name": "first", "id": 2, "tags": ["a"], "name": "second"}
""")
doc("special", """
{"blob": {"$bin": "00ff10deadbeef"},
 "empty_blob": {"$bin": ""},
 "ext1": {"$ext": [5, "2a"]},
 "ext2": {"$ext": [6, "0102"]},
 "ext4": {"$ext": [7, "01020304"]},
 "ext8": {"$ext": [8, "0102030405060708"]},
 "ext16": {"$ext": [9, "000102030405060708090a0b0c0d0e0f"]},
 "ext3": {"$ext": [10, "abcdef"]},
 "ext0": {"$ext": [127, ""]},
 "ts32": {"$ts": [1700000000, 0]},
 "ts64": {"$ts": [1700000000, 123456789]},
 "ts96": {"$ts": [-1, 999999999]},
 "ts96b": {"$ts": [17179869184, 5]},
 "point": {"$tuple": [1, 2]}}
""")
doc("big", """
{"str16": {"$repeat": ["ab", 200]},
 "str32": {"$repeat": ["xyz", 22000]},
 "bin16": {"$binrepeat": ["c0ffee", 100]},
 "bin32": {"$binrepeat": ["00", 70000]},
 "array16": {"$range": 16},
 "array32": {"$range": 70000},
 "map16": {"$map": 20}}
""")
doc("nested", """
{"a": {"b": {"c": {"d": {"e": [[[[[{"f": [true, false, null]}]]]]]}}}}}
""")
doc("too-big-int", """
{"ok": 1, "bad": 18446744073709551616}
""")
doc("too-small-int", """
[1, 2, -9223372036854775809]
""")
doc("bad-ext", """
{"x": {"$ext": [200, "00"]}}
""")
doc("bad-ts", """
{"x": {"$ts": [0, 1000000000]}}
""")

for name in ["package", "geojson", "ints", "floats", "strings", "dupes", "special", "nested"]:
    job("pack " + name)
for name in ["package", "ints", "floats", "strings", "special"]:
    job("pack %s bin=0" % name)
job("pack floats single=1")
job("pack geojson single=1")
job("pack big")
job("pack big bin=0")
for name in ["too-big-int", "too-small-int", "bad-ext", "bad-ts"]:
    job("pack " + name)

# ------------------------------------------------------------ files to unpack

binf("scalars", P([None, True, False, 0, 127, -1, -32, 300, -300, 2**40, -2**40, 2**64 - 1,
                   1.5, -0.0, float("inf"), float("nan"), "hi", b"\x00\xffbin"]))
binf("single-floats", P([0.1, 1.5, 3.4e38, 1e-45, -2.5], use_single_float=True))
binf("record", P({"user": "ada", "id": 1815, "roles": ["admin", "dev"],
                  "meta": {"active": True, "score": 99.5, "avatar": b"\x89PNG"}}))
binf("int-keys", P({1: "one", 2: "two", -3: "minus three"}))
binf("mixed-keys", P({None: 0, True: 1, 2.5: 2, b"k": 3, "k": 4, (1, 2): 5}))
binf("equal-keys", bytes([0x84, 0x01, 0xa1, 0x61, 0xc3, 0xa1, 0x62, 0xcb]) + struct.pack(">d", 1.0)
     + bytes([0xa1, 0x63, 0x02, 0xa1, 0x64]))
binf("list-key", bytes([0x81, 0x91, 0x01, 0xa1, 0x78]))
binf("map-key", bytes([0x81, 0x80, 0xa1, 0x78]))
binf("exts", P([ExtType(1, b"a"), ExtType(2, b"ab"), ExtType(3, b"abcd"), ExtType(4, b"\x00" * 8),
                ExtType(5, bytes(range(16))), ExtType(6, b"xyz"), ExtType(7, b""),
                ExtType(127, b"\x7f" * 300)]))
binf("timestamps", P([Timestamp(0), Timestamp(1700000000), Timestamp(1700000000, 500000000),
                      Timestamp(-86400, 1), Timestamp(2**34, 7), Timestamp(2**33 - 1, 999999999)]))
binf("negative-ext-code", bytes([0xd4, 0x80, 0x01, 0xc7, 0x02, 0xfe, 0x01, 0x02]))
binf("raw-strings", P(["short", "x" * 40, "y" * 300], use_bin_type=False))
binf("wide-headers", bytes([0x93, 0xcc, 0x05, 0xcd, 0x00, 0x05, 0xcf]) + (5).to_bytes(8, "big")
     + bytes([0xdc, 0x00, 0x02, 0xd0, 0x7f, 0xd1, 0xff, 0x80])
     + bytes([0xde, 0x00, 0x01, 0xd9, 0x01, 0x6b, 0xc4, 0x01, 0x76])
     + bytes([0xdd, 0x00, 0x00, 0x00, 0x01, 0xdb, 0x00, 0x00, 0x00, 0x02, 0x6f, 0x6b])
     + bytes([0xdf, 0x00, 0x00, 0x00, 0x01, 0xda, 0x00, 0x01, 0x6b, 0xc6, 0x00, 0x00, 0x00, 0x00])
     + bytes([0xc5, 0x00, 0x01, 0x42, 0xc8, 0x00, 0x01, 0x09, 0x41, 0xc9, 0x00, 0x00, 0x00, 0x01, 0x0a, 0x42]))
binf("tuples", P([[1, [2, 3]], [], {"p": [4]}]))
binf("utf8-mix", P(["café", "日本", "\U0001f600", "tab\tq'uote", "\x85\xa0​ ﻿",
                    "it's", 'a"b\'c', "\\", "\x00\x1f\x7f"]))
binf("bytes-quotes", P([b"it's", b'a"b', b"a\"b'c", b"\t\n\r\\", b"\x00\x7f\x80\xff"]))
binf("hex-floats", P([1e16, 1e-5, 0.0001, 123456789012345678.0, 1.0e22, 2.0**53, -1e-300]))
binf("two-docs", P({"a": 1}) + P([2]))

# broken
binf("unknown-header", bytes([0x92, 0x01, 0xc1]))
binf("truncated-array", bytes([0x93, 0x01, 0x02]))
binf("truncated-str", bytes([0xa5, 0x68, 0x65]))
binf("truncated-float", bytes([0xcb, 0x40, 0x09]))
binf("empty", b"")
binf("claims-big-array", bytes([0xdd, 0x00, 0x00, 0x03, 0xe8, 0x01, 0x02]))
binf("claims-big-map", bytes([0x86, 0xa1, 0x61, 0x01]))
binf("claims-big-str", bytes([0xdb, 0x00, 0x01, 0x00, 0x00, 0x61]))
binf("claims-big-bin", bytes([0xc5, 0x10, 0x00, 0x61]))
binf("claims-big-ext", bytes([0xc8, 0x10, 0x00, 0x01, 0x61]))
binf("bad-utf8-start", bytes([0x91, 0xa3, 0x61, 0xff, 0x62]))
binf("bad-utf8-cont", bytes([0xa3, 0xe2, 0x82, 0x28]))
binf("bad-utf8-cont1", bytes([0xa2, 0xe2, 0x28]))
binf("bad-utf8-end", bytes([0xa4, 0x61, 0x62, 0xe2, 0x82]))
binf("bad-utf8-overlong", bytes([0xa2, 0xc0, 0x80]))
binf("bad-utf8-surrogate", bytes([0xa3, 0xed, 0xa0, 0x80]))
binf("bad-utf8-toobig", bytes([0xa4, 0xf4, 0x90, 0x80, 0x80]))
binf("bad-utf8-4end", bytes([0xa5, 0x7a, 0xf0, 0x9f, 0x98, 0x41]))
binf("bad-timestamp", bytes([0xd5, 0xff, 0x00, 0x01]))
binf("extra-data", P([1, 2]) + b"\x03")
binf("key-int", P({1: 2}))
binf("key-float-in-nest", P({"ok": {1.5: "x"}}))
binf("key-list", bytes([0x81, 0x92, 0x01, 0x02, 0xa1, 0x76]))
binf("key-ext", bytes([0x81, 0xd4, 0x01, 0x00, 0x01]))
binf("key-ts", bytes([0x81, 0xd6, 0xff, 0x00, 0x00, 0x00, 0x01, 0x01]))
binf("key-none", bytes([0x81, 0xc0, 0x01]))
binf("key-bool", bytes([0x81, 0xc3, 0x01]))
binf("key-bin", bytes([0x81, 0xc4, 0x01, 0x6b, 0x01]))
binf("key-err-first", bytes([0x81, 0x01, 0xc1]))

for name in ["scalars", "single-floats", "record", "exts", "timestamps", "negative-ext-code",
             "raw-strings", "wide-headers", "tuples", "utf8-mix", "bytes-quotes", "hex-floats",
             "two-docs", "int-keys", "key-bin", "empty"]:
    job("unpack " + name)
job("unpack record raw=1")
job("unpack raw-strings raw=1")
job("unpack tuples list=0")
job("unpack record list=0")
job("unpack timestamps ts=1")
job("unpack timestamps ts=2")
job("unpack int-keys strict=0")
job("unpack mixed-keys strict=0")
job("unpack mixed-keys strict=0 list=0")
job("unpack equal-keys strict=0")
job("unpack list-key strict=0")
job("unpack list-key strict=0 list=0")
job("unpack map-key strict=0")
for name in ["unknown-header", "truncated-array", "truncated-str", "truncated-float",
             "claims-big-array", "claims-big-map", "claims-big-str", "claims-big-bin",
             "claims-big-ext", "bad-utf8-start", "bad-utf8-cont", "bad-utf8-cont1", "bad-utf8-end",
             "bad-utf8-overlong", "bad-utf8-surrogate", "bad-utf8-toobig", "bad-utf8-4end",
             "bad-timestamp", "extra-data", "key-int", "key-float-in-nest", "key-list",
             "key-ext", "key-ts", "key-none", "key-bool", "key-err-first"]:
    job("unpack " + name)
job("unpack bad-utf8-start raw=1")
job("unpack record max_str=3")
job("unpack record max_bin=3")
job("unpack record max_array=1")
job("unpack record max_map=3")
job("unpack exts max_ext=3")
job("unpack exts max_ext=0")

# ------------------------------------------------------------ streams

events = []
for i in range(12):
    events.append({"seq": i, "level": ["info", "warn", "error"][i % 3],
                   "msg": "request %d took %d ms" % (i, 17 * i + 3),
                   "ts": Timestamp(1700000000 + i * 60, i * 1000)})
stream = b"".join(P(e) for e in events)
binf("event-stream", stream)
binf("stream-with-junk", P({"a": 1}) + P([1, 2]) + bytes([0xc1]) + P("after"))
binf("stream-truncated", stream[:200])
for chunk in [1, 7, 64, 100000]:
    job("stream event-stream %d" % chunk)
job("stream event-stream 13 ts=1")
job("stream stream-with-junk 3")
job("stream stream-truncated 50")
job("stream event-stream 40 max_buffer=60")
job("stream event-stream 40 max_buffer=200")
job("stream two-docs 2")

# ------------------------------------------------------------ fluentd forward protocol


def et(sec, nsec):
    return ExtType(0, struct.pack(">II", sec, nsec))


fwd = b""
fwd += P(["app.access", 1700000100, {"method": "GET", "path": "/health", "status": 200}])
fwd += P(["app.access", et(1700000101, 250000000), {"method": "POST", "path": "/login", "status": 302},
          {"chunk": "p8n9gmxTQVC8/nh2wlKKeQ=="}])
fwd += P(["app.worker", [[1700000102, {"job": "resize", "ms": 41}],
                         [et(1700000103, 7), {"job": "thumbnail", "ms": 12}]],
          {"chunk": "Fqd9ftTpSbe3sN7LrBYwJQ==", "size": 2}])
entries = P([1700000104, {"event": "cache-miss", "key": "user:1815"}]) + \
    P([et(1700000105, 999999999), {"event": "cache-hit", "key": "user:7"}])
fwd += P(["app.cache", entries, {"size": 2}])
fwd += P(["app.cache", entries.decode("latin-1")], use_bin_type=False)
fwd += P(["bad.time", "yesterday", {"x": 1}])
fwd += P(["bad.time", 3.5, {"x": 1}])
fwd += P(["bad.shape", 5])
fwd += P(["bad.packed", b"\x92\x01\xc1"])
fwd += P({"not": "an array"})
fwd += P(["bad.eventtime", ExtType(0, b"\x00\x01"), {"x": 1}])
binf("forward", fwd)
job("forward forward 1")
job("forward forward 17")
job("forward forward 4096")

with open("data/jobs.tsv", "w") as f:
    f.write("\n".join(jobs) + "\n")
