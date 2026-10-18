#!/usr/bin/env python3
"""Writes data/: four .proto files, messages in text format and JSON,
binary messages made from them by the protobuf library, hand-made binary
files (unknown fields, groups, non-canonical encodings, corrupt input),
and data/jobs.tsv, the jobs mini_protobuf runs."""
import os

import oracle

os.makedirs("data", exist_ok=True)
FILES = {}


def put(name, body):
    FILES[name] = body
    mode = "wb" if isinstance(body, bytes) else "w"
    with open("data/" + name, mode) as f:
        f.write(body)


put("addressbook.proto", '''// The address book from the protobuf tutorial.
syntax = "proto3";

package tutorial;

option java_package = "com.example.tutorial.protos";
option java_outer_classname = "AddressBookProtos";

message Person {
  string name = 1;
  int32 id = 2;  // Unique ID number for this person.
  string email = 3;

  enum PhoneType {
    PHONE_TYPE_UNSPECIFIED = 0;
    PHONE_TYPE_MOBILE = 1;
    PHONE_TYPE_HOME = 2;
    PHONE_TYPE_WORK = 3;
  }

  message PhoneNumber {
    string number = 1;
    PhoneType type = 2;
  }

  repeated PhoneNumber phones = 4;
}

// Our address book file is just one of these.
message AddressBook {
  repeated Person people = 1;
}
''')

put("telemetry.proto", '''/*
 * Metrics from a fleet of edge devices: every scalar type, packed and
 * unpacked repeated fields, maps, a oneof, proto3 optional, and a field
 * with its own JSON name.
 */
syntax = "proto3";

package telemetry.v1;

enum Severity {
  SEVERITY_UNSPECIFIED = 0;
  DEBUG = 1;
  INFO = 2;
  WARN = 3;
  ERROR = 4;
}

message Point {
  double x = 1;
  double y = 2;
}

message Sample {
  int32 i32 = 1;
  int64 i64 = 2;
  uint32 u32 = 3;
  uint64 u64 = 4;
  sint32 s32 = 5;
  sint64 s64 = 6;
  fixed32 f32 = 7;
  fixed64 f64 = 8;
  sfixed32 sf32 = 9;
  sfixed64 sf64 = 10;
  bool flag = 11;
  float ratio = 12;
  double value = 13;
  string label = 14 [json_name = "displayLabel"];
  bytes blob = 15;
  Severity severity = 16;
  repeated int32 counts = 17;
  repeated double readings = 18;
  repeated string tags = 19;
  map<string, int64> attrs = 20;
  optional int32 retries = 21;
  oneof payload {
    string text = 22;
    Point point = 23;
  }
  repeated Severity history = 24;
  map<int32, Point> by_id = 25;
  reserved 26 to 30;
  reserved "legacy_id";
}

message Batch {
  string host = 1;
  repeated Sample samples = 2;
  uint64 seq = 1000;
  map<string, string> labels = 3;
  Point origin = 4;
}
''')

put("legacy.proto", '''// An order service's proto2 schema: required fields, defaults, closed
// enums, unpacked and packed repeated fields.
syntax = "proto2";

package shop.legacy;

message Customer {
  required string name = 1;
  optional string email = 2;
  optional bool vip = 3 [default = false];
}

message Order {
  enum Status {
    PENDING = 1;
    SHIPPED = 2;
    CANCELLED = 3;
  }

  required string id = 1;
  optional int32 quantity = 2 [default = 1];
  repeated int32 lines = 3;
  repeated int32 packed_lines = 4 [packed = true];
  optional Status status = 5 [default = PENDING];
  optional Customer customer = 6;
  optional double total = 7 [default = 0.5];
  repeated string notes = 8;
  optional bytes token = 9;
  optional sint64 balance = 10 [default = -10];
}
''')

put("empty.proto", '''syntax = "proto3";
package empty;
message Empty {}
''')

put("people.txtpb", '''# An address book with three people.
people {
  name: "Ada Lovelace"
  id: 1815
  email: "ada@example.org"
  phones { number: "+44 20 7946 0018" type: PHONE_TYPE_HOME }
  phones { number: "555-0100" type: PHONE_TYPE_MOBILE }
}
people {
  name: "José Martí"
  id: 42
  phones: { number: "07700 900461", type: 3 }
}
people <
  name: 'Ζωή'
  email: "zoe@example.gr";
>
''')

put("sample.txtpb", '''# Every scalar type, written several ways.
i32: -123456
i64: -9223372036854775808
u32: 4294967295
u64: 18446744073709551615
s32: -1
s64: 0x7fffffffffffffff
f32: 0xDEADBEEF
f64: 1_000_000
sf32: -2147483648
sf64: -070
flag: true
ratio: 0.1
value: -2.5e-3
label: "edge-01 \\"north\\" " 'rack\\t7'
blob: "\\x00\\001\\377abc\\n"
severity: WARN
counts: [1, -2, 300, 0]
counts: 70000
readings: [0.5, 1e10, -0.0, inf]
tags: "a"
tags: "b c"
attrs { key: "cpu" value: 93 }
attrs { key: "mem" value: -4096 }
attrs { key: "disk" value: 100 }
retries: 0
text: "rebooted at 03:00 \\u00e9t\\u00e9"
history: [INFO, 2, ERROR]
''')

put("sample2.txtpb", '''# The other member of the oneof, a map of messages, an unknown enum
# number, and float edge values.
point { x: 1.5 y: -2 }
by_id { key: 7 value { x: 0.25 } }
by_id { key: -1 value { } }
by_id { key: 3 value { y: 3 } }
severity: 9
ratio: 3.4028234663852886e+38
value: 1e-300
readings: [nan, -inf, 123456789.125, 1e+22]
history: 7
flag: True
''')

put("batch.txtpb", '''host: "edge-01.fra"
seq: 1000000
samples { i32: 1 label: "first" counts: [1, 2, 3] }
samples { i32: 2 label: "second" attrs { key: "z" value: 1 } attrs { key: "a" value: 2 } }
samples { }
labels { key: "region" value: "eu-central" }
labels { key: "env" value: "prod" }
origin { }
''')

put("order.txtpb", '''id: "ORD-2024-0001"
quantity: 3
lines: [10, 20, 30]
packed_lines: [10, 20, 30]
status: SHIPPED
customer { name: "Grace Hopper" vip: true }
total: 59.97
notes: "leave at door"
notes: "fragile"
token: "\\xca\\xfe"
balance: -1
''')

put("order-defaults.txtpb", '''# Fields left at their defaults, and one set to them explicitly.
id: "ORD-2024-0002"
quantity: 1
''')

put("order-missing.txtpb", '''quantity: 2
customer { email: "nobody@example.com" }
''')

# Text-format errors, one per file.
BAD_TEXT = {
    "bad-field.txtpb": 'i32: 1\nlabell: "x"\n',
    "bad-enum.txtpb": 'severity: FATAL\n',
    "bad-range.txtpb": 'i32: 3000000000\n',
    "bad-uint.txtpb": 'u64: -1\n',
    "bad-int.txtpb": 'i64: 12abc\n',
    "bad-float.txtpb": 'ratio: 1.5.5\n',
    "bad-bool.txtpb": 'flag: yes\n',
    "bad-colon.txtpb": 'i32 5\n',
    "bad-brace.txtpb": 'point {\n  x: 1\n',
    "bad-twice.txtpb": 'i32: 1\ni32: 2\n',
    "bad-oneof.txtpb": 'text: "a"\npoint { x: 1 }\n',
    "bad-quote.txtpb": 'label: "unterminated\n',
    "bad-octal.txtpb": 'value: 012.5\n',
    "bad-list.txtpb": 'counts: [1, 2\n',
    "bad-ext.txtpb": '[telemetry.v1.ext]: 1\n',
    "bad-msg-twice.txtpb": 'point { x: 1 }\npoint { y: 2 }\n',
    "bad-closed-enum.txtpb": 'id: "x"\nstatus: 9\n',
    "bad-string-int.txtpb": 'i32: "5"\n',
    "bad-token.txtpb": 'i32: 1\n}\n',
    "bad-utf8.txtpb": 'label: "ok\\377"\n',
    "bad-hex.txtpb": 'f32: 0xG1\n',
}
for name, body in BAD_TEXT.items():
    put(name, body)

put("sample.json", '''{
  "i32": -7,
  "i64": "-9007199254740993",
  "u32": 4000000000,
  "u64": "18446744073709551615",
  "s32": "12",
  "sf64": 1e3,
  "flag": false,
  "ratio": "Infinity",
  "value": 6.02214076e23,
  "displayLabel": "caf\\u00e9 \\ud83d\\ude80",
  "blob": "SGVsbG8gd29ybGQ_-w",
  "severity": "ERROR",
  "counts": [1, 2.0, "3"],
  "readings": ["NaN", -1.25, "-Infinity"],
  "tags": [],
  "attrs": {"zone": "17", "b": -2},
  "retries": 0,
  "point": {"x": 0.5},
  "history": [1, "WARN"],
  "byId": {"10": {"y": 2}, "-3": {}}
}
''')

put("sample-names.json", '''{"label": "by proto name", "by_id": {"1": {"x": 1}}, "s64": "-5",
 "text": null, "severity": 3, "i32": null}
''')

BAD_JSON = {
    "bad-unknown.json": '{"i32": 1, "nope": 2}',
    "bad-syntax.json": '{"i32": 1,}',
    "bad-dup.json": '{"i32": 1, "i32": 2}',
    "bad-both.json": '{"i32": 1, "displayLabel": "x", "label": "y"}',
    "bad-oneof.json": '{"text": "a", "point": {}}',
    "bad-int.json": '{"i32": 1.5}',
    "bad-intstr.json": '{"i64": "12 34"}',
    "bad-bool.json": '{"flag": "true"}',
    "bad-enum.json": '{"severity": "FATAL"}',
    "bad-nan.json": '{"ratio": "nan"}',
    "bad-big-float.json": '{"ratio": 1e39}',
    "bad-nested.json": '{"point": {"x": "left"}}',
    "bad-map-key.json": '{"byId": {"x": {}}}',
    "bad-bool-int.json": '{"i32": true}',
    "bad-range.json": '{"u32": -1}',
    "bad-null-elem.json": '{"tags": ["a", null]}',
    "bad-empty.json": '',
}
for name, body in BAD_JSON.items():
    put(name, body)

# Binary messages made by the library from the text files.
for proto, msg, src, out in [
        ("addressbook.proto", "tutorial.AddressBook", "people.txtpb", "people.bin"),
        ("telemetry.proto", "telemetry.v1.Sample", "sample.txtpb", "sample.bin"),
        ("telemetry.proto", "telemetry.v1.Sample", "sample2.txtpb", "sample2.bin"),
        ("telemetry.proto", "telemetry.v1.Batch", "batch.txtpb", "batch.bin"),
        ("legacy.proto", "shop.legacy.Order", "order.txtpb", "order.bin"),
        ("legacy.proto", "shop.legacy.Order", "order-defaults.txtpb", "order-defaults.bin")]:
    cls = oracle.message_class(proto, msg)
    m = oracle.text_format.Parse(FILES[src], cls())
    put(out, m.SerializeToString(deterministic=True))


def varint(n):
    n &= (1 << 64) - 1
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def tag(num, wire):
    return varint(num << 3 | wire)


def ld(num, body):
    return tag(num, 2) + varint(len(body)) + body


# A person with fields the schema doesn't know, before and after the known
# ones; a newer client wrote them.
put("person-unknown.bin",
    tag(9, 0) + varint(77) + ld(1, b"Linus") + tag(10, 1) + bytes(range(1, 9))
    + tag(2, 0) + varint(1969) + ld(11, b"\x08\x01\x12\x03abc") + tag(12, 5)
    + b"\x00\x00\x80\x3f" + ld(13, b"") + tag(2, 5) + b"\x01\x00\x00\x00")
put("book-unknown.bin", ld(1, open("data/person-unknown.bin", "rb").read()) + ld(2, b"\xff"))

# Non-canonical but valid encodings: unpacked where packed is the default,
# packed where unpacked is, a repeated singular field, a split sub-message,
# overlong varints, a oneof set twice and an enum value proto2 doesn't know.
put("sample-odd.bin",
    tag(17, 0) + varint(5) + ld(17, varint(6) + varint(-7)) + tag(17, 0) + varint(8)
    + tag(1, 0) + varint(1) + tag(1, 0) + b"\x82\x80\x80\x80\x00"
    + ld(23, tag(1, 1) + b"\x00\x00\x00\x00\x00\x00\xf0\x3f")
    + ld(23, tag(2, 1) + b"\x00\x00\x00\x00\x00\x00\x00\x40")
    + ld(22, b"later wins")
    + tag(11, 0) + varint(9) + tag(3, 0) + varint(1 << 33 | 5)
    + ld(20, ld(1, b"k") + tag(2, 0) + varint(1)) + ld(20, ld(1, b"k") + tag(2, 0) + varint(2))
    + ld(20, tag(2, 0) + varint(3)))
put("order-odd.bin",
    ld(1, b"ORD-X") + ld(3, varint(1) + varint(2)) + tag(4, 0) + varint(3)
    + tag(5, 0) + varint(7) + tag(5, 0) + varint(2) + ld(6, ld(2, b"a@b.c")))

# Raw files for decode_raw-style dumps: groups, nested messages that are
# really strings, and the heuristics' edge cases.
put("raw-mixed.bin",
    tag(1, 0) + varint(150) + tag(2, 5) + b"\x01\x02\x03\x04" + tag(3, 1) + bytes(range(8))
    + ld(4, b"") + ld(4, b"\x08\x01\x10") + ld(4, b"hi") + tag(5, 3) + tag(1, 0)
    + varint(5) + tag(6, 3) + tag(7, 0) + varint(1) + tag(6, 4) + tag(5, 4)
    + ld(6, "é".encode()) + ld(7, ld(1, ld(2, b"deep"))) + tag(0, 0) + varint(1)
    + ld(8, b"\x0c") + ld(9, b"\x80") + ld(10, b"\x0b\x10\x01\x0c") + ld(11, b"\x0d\x01\x02")
    + ld(12, b"\x1a\x05ab") + tag(536870911, 0) + varint(-1))
put("raw-people.bin", open("data/people.bin", "rb").read())

# Corrupt input, each a different way.
put("bad-wiretype.bin", tag(1, 0) + varint(1) + tag(2, 6) + b"\x00")
put("bad-truncated.bin", open("data/people.bin", "rb").read()[:40])
put("bad-varint.bin", tag(2, 0) + b"\xff" * 10 + b"\x01")
put("bad-length.bin", ld(1, b"abc")[:-1])
put("bad-group.bin", tag(5, 3) + tag(1, 0) + varint(1))
put("bad-endgroup.bin", tag(1, 0) + varint(1) + tag(5, 4))
put("bad-utf8.bin", ld(14, b"\xc3\x28"))
put("bad-submsg.bin", ld(23, tag(1, 1) + b"\x00\x00"))
put("bad-group-mismatch.bin", tag(5, 3) + tag(6, 4))

J = []


def job(*f):
    J.append("\t".join(f))


A = ("addressbook.proto", "tutorial.AddressBook")
P = ("addressbook.proto", "tutorial.Person")
S = ("telemetry.proto", "telemetry.v1.Sample")
B = ("telemetry.proto", "telemetry.v1.Batch")
O = ("legacy.proto", "shop.legacy.Order")
for args in [(A, "people.txtpb"), (S, "sample.txtpb"), (S, "sample2.txtpb"),
             (B, "batch.txtpb"), (O, "order.txtpb"), (O, "order-defaults.txtpb")]:
    job("encode", *args[0], args[1])
    job("text", *args[0], args[1])
job("encode", *O, "order-missing.txtpb")
job("text", *O, "order-missing.txtpb")
for name in BAD_TEXT:
    job("text", *(O if "closed" in name else S), name)
for args in [(A, "people.bin"), (S, "sample.bin"), (S, "sample2.bin"),
             (B, "batch.bin"), (O, "order.bin"), (O, "order-defaults.bin"),
             (P, "person-unknown.bin"), (A, "book-unknown.bin"),
             (S, "sample-odd.bin"), (O, "order-odd.bin")]:
    job("decode", *args[0], args[1])
for args in [(A, "people.bin"), (S, "sample.bin"), (S, "sample2.bin"),
             (B, "batch.bin"), (O, "order.bin")]:
    job("json", *args[0], args[1])
job("json", *S, "sample.bin", "names")
job("json", *S, "sample.bin", "ints")
job("json", *A, "people.bin", "defaults")
job("json", *O, "order-defaults.bin", "defaults", "names")
job("json", *S, "sample-odd.bin")
job("json", *O, "order-odd.bin")
for name in ["person-unknown.bin", "book-unknown.bin", "sample-odd.bin", "order-odd.bin",
             "people.bin", "sample.bin", "order.bin"]:
    job("roundtrip", *(P if name.startswith("person") else A if "people" in name or "book" in name
                       else O if "order" in name else S), name)
for name in ["raw-mixed.bin", "raw-people.bin", "sample.bin", "batch.bin"]:
    job("raw", name)
job("fromjson", *S, "sample.json")
job("fromjson", *S, "sample-names.json")
for name in BAD_JSON:
    job("fromjson", *S, name)
for name in ["bad-wiretype.bin", "bad-truncated.bin", "bad-varint.bin", "bad-length.bin",
             "bad-group.bin", "bad-endgroup.bin", "bad-utf8.bin", "bad-submsg.bin",
             "bad-group-mismatch.bin"]:
    job("decode", *(A if name == "bad-truncated.bin" else S), name)
job("raw", "bad-varint.bin")
job("raw", "bad-group-mismatch.bin")
put("jobs.tsv", "\n".join(J) + "\n")
