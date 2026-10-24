# Writes data/: jobs.txt (one job per line, kind TAB argument), the .bson
# dump files and the .jsonl import files, and files.txt.
# Run as: python3 -s -P -B mk.py
import datetime
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'vendor'))
import bson  # noqa: E402
from bson import json_util  # noqa: E402

D = os.path.join(HERE, 'data')
files = []
jobs = []


def put(name, data):
    os.makedirs(os.path.dirname(os.path.join(D, name)) or D, exist_ok=True)
    if isinstance(data, str):
        data = data.encode('utf-8')
    with open(os.path.join(D, name), 'wb') as f:
        f.write(data)
    files.append(name)


def job(kind, arg):
    assert '\t' not in arg and '\n' not in arg, arg
    jobs.append(kind + '\t' + arg)


# --- raw BSON builders -------------------------------------------------

def i32(v):
    return struct.pack('<i', v)


def i64(v):
    return struct.pack('<q', v)


def cstr(s):
    return (s.encode() if isinstance(s, str) else s) + b'\x00'


def el(t, name, payload=b''):
    return bytes([t]) + cstr(name) + payload


def doc(*elements, size=None, tail=b'\x00'):
    body = b''.join(elements)
    n = len(body) + 4 + len(tail) if size is None else size
    return i32(n) + body + tail


def string(s):
    b = s.encode() if isinstance(s, str) else s
    return i32(len(b) + 1) + b + b'\x00'


def hexjob(data, kind='hex'):
    job(kind, data.hex())


# --- extended JSON jobs ------------------------------------------------

OID = '5f2b3c4d5e6f708192a3b4c5'
JSON = [
    # integers and the int32 / int64 / overflow edges
    '{"a": 1}',
    '{"a": -2147483648, "b": 2147483647, "c": -2147483647}',
    '{"a": 2147483648, "b": -2147483649}',
    '{"a": 9223372036854775807, "b": -9223372036854775808}',
    '{"a": 9223372036854775808}',
    '{"a": -9223372036854775809}',
    '{"a": 0, "b": -0, "c": 10}',
    # floats
    '{"a": 1.5, "b": -0.0, "c": 1e300, "d": 1e-300, "e": 0.1, "f": 1E5, "g": 1.0}',
    '{"a": NaN, "b": Infinity, "c": -Infinity}',
    '{"a": 123456789012345678901234567890.0, "b": 2.5e-7, "c": 1e16, "d": 1e15}',
    '{"a": 5e-324, "b": 1.7976931348623157e308, "c": 1e400}',
    # strings
    '{"s": "plain", "t": "", "u": "tab\\there", "v": "quote\\"s", "w": "it\'s"}',
    '{"s": "caf\\u00e9", "t": "\\u65e5\\u672c", "u": "\\ud83d\\ude00", "v": "\\u0001\\u001f\\u007f"}',
    '{"s": "café 日本 \U0001f600", "t": "a\\u0000b", "u": "back\\\\slash"}',
    '{"s": "nb\\u00a0sp", "t": "zw\\u200bsp", "u": "line\\u2028sep", "v": "\\u0085\\u00ad"}',
    '{"s": "both \' and \\"", "t": "\\r\\n\\b\\f"}',
    # keys
    '{"": 1, "é": 2, "a.b": 3, "$x": 4}',
    '{"b": 1, "a": 2, "b": 3}',
    '{"a\\u0000b": 1}',
    # booleans, null, nesting
    '{"t": true, "f": false, "n": null}',
    '{"d": {}, "a": [], "n": {"x": {"y": {"z": [1, [2, [3, {}]]]}}}}',
    '{"a": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}',
    '{"_id": 7, "a": 1}',
    '{"a": 1, "_id": {"$oid": "' + OID + '"}}',
    # $oid
    '{"_id": {"$oid": "' + OID + '"}}',
    '{"_id": {"$oid": "5F2B3C4D5E6F708192A3B4C5"}}',
    '{"_id": {"$oid": "5f2b3c4d5e6f708192a3b4c"}}',
    '{"_id": {"$oid": "5f2b3c4d5e6f708192a3b4cz"}}',
    '{"_id": {"$oid": "5f2b 3c4d5e6f708192a3b4c5"}}',
    '{"_id": {"$oid": "5f2b3c4d 5e6f708192a3b4c"}}',
    '{"_id": {"$oid": "5f2b 3c4d 5e6f708192a3b4"}, "x": 1}',
    '{"_id": {"$oid": 12}}',
    '{"_id": {"$oid": "' + OID + '", "x": 1}}',
    '{"_id": {"x": 1, "$oid": "' + OID + '"}}',
    # $date
    '{"d": {"$date": "2020-01-02T03:04:05Z"}}',
    '{"d": {"$date": "2020-01-02T03:04:05.678Z"}}',
    '{"d": {"$date": "2020-01-02T03:04:05.123456Z"}}',
    '{"d": {"$date": "2020-01-02T03:04:05.5"}}',
    '{"d": {"$date": "2020-01-02T03:04:05+05:30"}}',
    '{"d": {"$date": "2020-01-02T03:04:05.250-0800"}}',
    '{"d": {"$date": "2020-01-02T03:04:05+01"}}',
    '{"d": {"$date": "1969-12-31T23:59:59.999Z"}}',
    '{"d": {"$date": "1900-03-01T00:00:00Z"}}',
    '{"d": {"$date": "9999-12-31T23:59:59.999Z"}}',
    '{"d": {"$date": "2020-1-2T3:4:5Z"}}',
    '{"d": {"$date": "2021-02-29T00:00:00Z"}}',
    '{"d": {"$date": "2020-13-01T00:00:00Z"}}',
    '{"d": {"$date": "2020-01-02 03:04:05Z"}}',
    '{"d": {"$date": "2020-01-02T03:04:05Zjunk"}}',
    '{"d": {"$date": "2020-01-02T03:04:05.Z"}}',
    '{"d": {"$date": "x"}}',
    '{"d": {"$date": ""}}',
    '{"d": {"$date": "2020-01-02T03:04:60Z"}}',
    '{"d": {"$date": "0000-01-01T00:00:00Z"}}',
    '{"d": {"$date": "0001-01-01T00:00:00+01:00"}}',
    '{"d": {"$date": "9999-12-31T23:30:00-01:00"}}',
    '{"d": {"$date": "2020-01-02t03:04:05z"}}',
    '{"d": {"$date": "2020-01-02t03:04:05Z"}}',
    '{"d": {"$date": "2020-01-02T03:04:05.5e1Z"}}',
    '{"d": {"$date": "2020-01-02T03:04:05+0a:00"}}',
    '{"d": {"$date": "2020-01-02T03:04:05.9999999Z"}}',
    '{"d": {"$date": "2020-01-02T3:4Z"}}',
    '{"d": {"$date": "2020-12-31T24:00:00Z"}}',
    '{"d": {"$date": 1.5e12}}',
    '{"d": {"$date": null}}',
    '{"d": {"$date": 1e300}}',
    '{"d": {"$date": true}}',
    '{"d": {"$date": {"$numberLong": "1577934245678"}}}',
    '{"d": {"$date": {"$numberLong": "-1"}}}',
    '{"d": {"$date": 1577934245678}}',
    '{"d": {"$date": -62135596800000}}',
    '{"d": {"$date": -62135596800001}}',
    '{"d": {"$date": 253402300800000}}',
    '{"d": {"$date": "2020-01-02T03:04:05Z", "x": 1}}',
    # $numberInt / $numberLong / $numberDouble
    '{"i": {"$numberInt": "42"}, "j": {"$numberInt": "-7"}, "k": {"$numberInt": " 8 "}}',
    '{"i": {"$numberInt": "1_000"}, "j": {"$numberInt": "+5"}}',
    '{"i": {"$numberInt": "abc"}}',
    '{"i": {"$numberInt": 42}}',
    '{"i": {"$numberInt": "4", "x": 1}}',
    '{"l": {"$numberLong": "123"}, "m": {"$numberLong": "-5"}, "n": {"$numberLong": "0"}}',
    '{"l": {"$numberLong": "9223372036854775807"}}',
    '{"l": {"$numberLong": "9223372036854775808"}}',
    '{"l": {"$numberLong": "12x"}}',
    '{"l": {"$numberLong": 77}}',
    '{"f": {"$numberDouble": "1.5"}, "g": {"$numberDouble": "-0.0"}, "h": {"$numberDouble": "1E3"}}',
    '{"f": {"$numberDouble": "NaN"}, "g": {"$numberDouble": "Infinity"}, "h": {"$numberDouble": "-Infinity"}}',
    '{"f": {"$numberDouble": "1e400"}, "g": {"$numberDouble": " 2.5 "}, "h": {"$numberDouble": "inf"}}',
    '{"f": {"$numberDouble": "abc"}}',
    '{"f": {"$numberDouble": 1.5}}',
    # $numberDecimal
    '{"d": {"$numberDecimal": "1.50E+3"}, "e": {"$numberDecimal": "-0.0005"}, "f": {"$numberDecimal": "0"}}',
    '{"d": {"$numberDecimal": "NaN"}, "e": {"$numberDecimal": "-Infinity"}, "f": {"$numberDecimal": "-0E+3"}}',
    '{"d": {"$numberDecimal": "12.3.4"}}',
    '{"d": {"$numberDecimal": 5}}',
    # $binary
    '{"b": {"$binary": {"base64": "AAEC", "subType": "00"}}}',
    '{"b": {"$binary": {"base64": "c3VyZS4=", "subType": "05"}}, "c": {"$binary": {"base64": "", "subType": "80"}}}',
    '{"b": {"$binary": {"base64": "ASNFZ4mrze8BI0VniavN7w==", "subType": "04"}}}',
    '{"b": {"$binary": {"base64": "ASNFZ4mrze8BI0VniavN7w==", "subType": "03"}}}',
    '{"b": {"$binary": {"base64": "AAEC", "subType": "2"}}, "c": {"$binary": {"base64": "AAEC", "subType": "8"}}}',
    '{"b": {"$binary": {"base64": "AAEC", "subType": "100"}}}',
    '{"b": {"$binary": {"base64": "AAEC", "subType": 5}}}',
    '{"b": {"$binary": {"base64": 12, "subType": "00"}}}',
    '{"b": {"$binary": {"base64": "AAEC", "subType": "00", "x": 1}}}',
    '{"b": {"$binary": {"base64": "AAE", "subType": "00"}}}',
    '{"b": {"$binary": {"base64": "AAECA", "subType": "00"}}}',
    '{"b": {"$binary": {"base64": "AA!E Cé", "subType": "00"}}}',
    '{"b": {"$binary": {"base64": "AA==AAEC", "subType": "00"}}}',
    '{"b": {"$binary": "AAEC", "$type": "05"}}',
    '{"b": {"$binary": "AAEC", "$type": 128}}',
    '{"b": {"$binary": "AAEC", "$type": "ffffff80"}}',
    '{"b": {"$binary": "AAEC", "$type": "zz"}}',
    '{"b": {"$binary": "AAEC", "$type": "0x05"}}',
    '{"b": {"$binary": 5, "$type": "00"}}',
    '{"b": {"$binary": {"subType": "00"}}}',
    '{"b": {"$binary": "AAEC"}}',
    '{"b": {"$binary": {"base64": "AAEC", "subType": "-1"}}}',
    '{"b": {"$binary": {"base64": "AAEC", "subType": " 7"}}}',
    # $uuid
    '{"u": {"$uuid": "01234567-89ab-cdef-0123-456789abcdef"}}',
    '{"u": {"$uuid": "{0123456789ABCDEF0123456789ABCDEF}"}}',
    '{"u": {"$uuid": "urn:uuid:01234567-89ab-cdef-0123-456789abcdef"}}',
    '{"u": {"$uuid": "0123"}}',
    '{"u": {"$uuid": 5}}',
    '{"u": {"$uuid": "01234567-89ab-cdef-0123-456789abcdef", "x": 1}}',
    # $code
    '{"c": {"$code": "function() { return 1; }"}}',
    '{"c": {"$code": "f(x)", "$scope": {"x": 1, "y": {"$oid": "' + OID + '"}}}}',
    '{"c": {"$code": "f", "$scope": {}}}',
    '{"c": {"$code": "f", "x": 1}}',
    '{"c": {"$code": 5}}',
    '{"c": {"$code": "f", "$scope": 5}}',
    '{"c": {"$scope": {"a": 1}, "$code": "g"}}',
    # regular expressions
    '{"r": {"$regularExpression": {"pattern": "^a.b$", "options": "imx"}}}',
    '{"r": {"$regularExpression": {"pattern": "x", "options": ""}}, "s": {"$regularExpression": {"pattern": "y", "options": "u"}}}',
    '{"r": {"$regularExpression": {"pattern": "x", "options": "xsmuli"}}}',
    '{"r": {"$regularExpression": {"pattern": "x", "options": "zq"}}}',
    '{"r": {"$regularExpression": {"pattern": "x", "options": 3}}}',
    '{"r": {"$regularExpression": {"pattern": "x"}}}',
    '{"r": {"$regularExpression": {"pattern": 5, "options": "i"}}}',
    '{"r": {"$regularExpression": {"pattern": "x", "flags": "i"}}}',
    '{"r": {"$regex": "a", "x": 1}}',
    '{"r": {"$regex": "ab+c", "$options": "si"}}',
    '{"r": {"$regex": "ab+c"}}',
    '{"r": {"$regex": {"$numberInt": "1"}, "$options": "i"}}',
    '{"r": {"$regex": "a\\u0000b"}}',
    # timestamps, min/max keys, undefined, symbol
    '{"t": {"$timestamp": {"t": 1577934245, "i": 7}}}',
    '{"t": {"$timestamp": {"t": 4294967295, "i": 4294967295}}}',
    '{"t": {"$timestamp": {"t": 4294967296, "i": 0}}}',
    '{"t": {"$timestamp": {"t": "5", "i": 0}}}',
    '{"t": {"$timestamp": {"t": 1, "i": -1}}}',
    '{"t": {"$timestamp": {"t": 1, "i": 1.5}}}',
    '{"hi": {"$maxKey": 2}}',
    '{"lo": {"$minKey": 1}, "hi": {"$maxKey": 1}}',
    '{"lo": {"$minKey": 2}}',
    '{"lo": {"$minKey": true}}',
    '{"hi": {"$maxKey": 1, "x": 2}}',
    '{"u": {"$undefined": true}, "s": {"$symbol": "sym"}}',
    '{"s": {"$symbol": "sym", "x": 1}}',
    '{"s": {"$symbol": 5}, "t": {"$symbol": 1.5}, "u": {"$symbol": null}, "v": {"$symbol": true}}',
    # DBRef and DBPointer
    '{"r": {"$ref": "users", "$id": 7}}',
    '{"r": {"$ref": "users", "$id": {"$oid": "' + OID + '"}, "$db": "app", "note": "x"}}',
    '{"r": {"$ref": "users", "$id": 1, "$db": null}}',
    '{"r": {"$ref": 5, "$id": 1}}',
    '{"r": {"$ref": "users"}}',
    '{"r": {"$ref": "users", "$id": 1, "$db": 3}}',
    '{"p": {"$dbPointer": {"$ref": "c", "$id": {"$oid": "' + OID + '"}}}}',
    '{"p": {"$dbPointer": {"$ref": "c", "$id": 1}}}',
    '{"p": {"$dbPointer": {"$ref": "c", "$id": {"$oid": "' + OID + '"}, "$db": "d"}}}',
    '{"p": {"$dbPointer": {"$ref": "c", "$id": {"$oid": "' + OID + '"}, "z": 1}}}',
    '{"p": {"$dbPointer": 5}}',
    # top-level values that are not documents
    '[1, 2]',
    '"abc"',
    '5',
    '{"$date": 0}',
    '{"$oid": "' + OID + '"}',
    # a realistic mixed document
    '{"_id": {"$oid": "' + OID + '"}, "name": "Ada", "age": 36, "score": 97.5, '
    '"tags": ["math", "engines"], "joined": {"$date": "1843-09-01T00:00:00Z"}, '
    '"balance": {"$numberDecimal": "1234.50"}, "active": true, "manager": null}',
]
for j in JSON:
    job('json', j)

# check_keys=True encoding
for j in ['{"a": 1}', '{"$set": {"a": 1}}', '{"a.b": 1}', '{"x": {"a.b": 1}}', '{"x": [{"$y": 1}]}']:
    job('keys', j)

# --- raw BSON jobs -----------------------------------------------------

oid = bytes.fromhex(OID)
valid = [
    doc(el(1, 'd', struct.pack('<d', 2.5))),
    doc(el(2, 's', string('hi')), el(2, 'e', string(''))),
    doc(el(3, 'o', doc(el(16, 'x', i32(1))))),
    doc(el(4, 'a', doc(el(16, '0', i32(1)), el(16, '1', i32(2))))),
    doc(el(4, 'a', doc(el(16, 'x', i32(1)), el(16, 'y', i32(2))))),
    doc(el(5, 'b', i32(3) + b'\x00abc'), el(5, 'c', i32(2) + b'\x80\xff\x01')),
    doc(el(5, 'u', i32(16) + b'\x04' + bytes(range(16))), el(5, 'v', i32(16) + b'\x03' + bytes(range(16)))),
    doc(el(5, 'p', i32(7) + b'\x02' + i32(3) + b'xyz')),
    doc(el(5, 'm', i32(4) + b'\x05' + b'\xde\xad\xbe\xef'), el(5, 'k', i32(2) + b'\x08' + b'pw')),
    doc(el(6, 'u'), el(10, 'n')),
    doc(el(7, '_id', oid)),
    doc(el(8, 't', b'\x01'), el(8, 'f', b'\x00')),
    doc(el(9, 'd', i64(1577934245678)), el(9, 'e', i64(-1)), el(9, 'z', i64(0))),
    doc(el(9, 'd', i64(253402300799999)), el(9, 'e', i64(-62135596800000))),
    doc(el(11, 'r', cstr('a.c') + cstr('mi')), el(11, 's', cstr('') + cstr('')), el(11, 'q', cstr('x') + cstr('zu'))),
    doc(el(12, 'p', string('coll') + oid)),
    doc(el(13, 'c', string('return 1'))),
    doc(el(14, 's', string('sym'))),
    doc(el(15, 'w', i32(4 + len(string('f')) + 12) + string('f') + doc(el(16, 'x', i32(1))))),
    doc(el(16, 'i', i32(-5)), el(18, 'l', i64(5)), el(18, 'm', i64(-9223372036854775808))),
    doc(el(17, 't', struct.pack('<II', 7, 1577934245))),
    doc(el(19, 'd', bytes.fromhex('96000000000000000000000000004230'))),
    doc(el(19, 'n', bytes.fromhex('000000000000000000000000000000fc')), el(19, 'i', bytes.fromhex('000000000000000000000000000000f8'))),
    doc(el(19, 'z', bytes.fromhex('0000000000000000000000000000403a')), el(19, 'q', bytes.fromhex('01000000000000000000000000002432'))),
    doc(el(19, 'nc', bytes.fromhex('ffffffffffffffffffffffffffff0130'))),
    doc(el(19, 'x', bytes.fromhex('000000000000000000000000000000' + '6c'))),
    doc(el(127, 'hi'), el(255, 'lo')),
    doc(el(3, 'r', doc(el(2, '$ref', string('users')), el(16, '$id', i32(9)), el(2, 'extra', string('e'))))),
    doc(el(3, 'r', doc(el(2, '$ref', string('users')), el(16, '$id', i32(9)), el(2, '$db', string('app'))))),
    doc(el(3, 'r', doc(el(2, '$ref', string('users'))))),
    doc(el(3, 'r', doc(el(16, '$ref', i32(1)), el(16, '$id', i32(9))))),
    doc(el(2, 'k\xc3\xa9'.encode('latin-1').decode('utf-8'), string('vé \U0001f600'))),
    doc(el(2, 's', string(b'a\x00b'))),
    doc(),
]
for v in valid:
    hexjob(v)

good = doc(el(16, 'a', i32(1)), el(2, 'b', string('x')))
malformed = [
    b'',
    b'\x05\x00\x00',
    b'\x05\x00\x00\x00',
    b'\x05\x00\x00\x00\x01',
    b'\x06\x00\x00\x00\x00\x00',
    good[:-1],
    good + b'\x00',
    good[:-1] + b'\x01',
    i32(-5) + b'\x00',
    i32(100) + good[4:],
    doc(el(16, 'a', i32(1)), size=10),
    doc(el(16, 'a', i32(1)), size=15),
    doc(el(20, 'a', i32(1))),
    doc(el(0x2a, 'z')),
    doc(el(8, 'b', b'\x02')),
    doc(el(2, 's', i32(0) + b'\x00')),
    doc(el(2, 's', i32(100) + b'ab\x00')),
    doc(el(2, 's', i32(3) + b'abc')),
    doc(el(2, 's', string(b'\xff'))),
    doc(el(2, 's', string(b'a\xc3'))),
    doc(el(2, 's', string(b'\xe2\x82'))),
    doc(el(2, 's', string(b'\xc3\x28'))),
    doc(el(2, 's', string(b'\xed\xa0\x80'))),
    doc(el(2, 's', string(b'\xf0\x9f\x98'))),
    doc(el(2, 's', string(b'\xc0\xaf'))),
    doc(el(2, 's', string(b'ok\xf8\x88\x80\x80\x80'))),
    doc(el(2, b'\xff', string('v'))),
    doc(el(2, b'k', i32(2))),
    doc(el(5, 'b', i32(100) + b'\x00abc')),
    doc(el(5, 'b', i32(-1) + b'\x00')),
    doc(el(5, 'p', i32(7) + b'\x02' + i32(4) + b'xyz')),
    doc(el(5, 'u', i32(3) + b'\x04' + b'abc')),
    doc(el(3, 'o', doc(el(16, 'x', i32(1)), size=20))),
    doc(el(3, 'o', doc(el(16, 'x', i32(1)), tail=b'\x01'))),
    doc(el(3, 'o', doc(el(16, 'x', i32(1)), size=9))),
    doc(el(4, 'a', doc(el(16, '0', i32(1)), tail=b'\x01'))),
    doc(el(4, 'a', doc(el(16, '0', i32(1)), size=9) + b'\x00\x00\x00')),
    doc(el(15, 'w', i32(30) + string('f') + doc(el(16, 'x', i32(1))))),
    doc(el(15, 'w', i32(4 + len(string('f')) + 12 + 3) + string('f') + doc(el(16, 'x', i32(1))) + b'\x00\x00\x00')),
    doc(el(9, 'd', i64(253402300800000))),
    doc(el(9, 'd', i64(-62135596800001))),
    doc(el(9, 'd', i64(9223372036854775807))),
    doc(el(9, 'd', i64(-9223372036854775808))),
    doc(el(9, 'd', i64(129600000000000000))),
    doc(el(9, 'd', i64(-129600000000000000))),
    doc(el(5, 'b', i32(2) + b'\x00')),
    doc(el(0x80, 'q')),
    doc(el(4, 'a', doc(el(0x99, '0', b'')))),
    doc(el(4, 'a', i32(1000) + b'\x00')),
    doc(el(16, 'i', b'\x01\x02')),
    doc(el(1, 'd', b'\x00\x00')),
    doc(el(7, 'o', b'\x01\x02\x03')),
    doc(el(17, 't', b'\x01')),
    doc(el(19, 'd', b'\x01\x02')),
    doc(el(11, 'r', b'abc')),
    doc(el(12, 'p', string('coll') + b'\x01\x02')),
]
for m in malformed:
    hexjob(m)

# decoding options
opt_docs = [
    doc(el(9, 'd', i64(253402300800000)), el(9, 'e', i64(-62135596800001)), el(9, 'f', i64(1577934245678))),
    doc(el(5, 'u', i32(16) + b'\x04' + bytes(range(16))), el(5, 'v', i32(16) + b'\x03' + bytes(range(16)))),
]
for o in ['datetime=auto', 'datetime=clamp', 'datetime=ms', 'uuid=standard', 'uuid=pythonLegacy',
          'uuid=javaLegacy', 'uuid=csharpLegacy']:
    for d in opt_docs:
        job('opts', o + ' ' + d.hex())

# several documents at once
d1 = doc(el(16, 'n', i32(1)))
d2 = doc(el(2, 's', string('two')))
d3 = doc(el(8, 'b', b'\x01'))
for data in [d1 + d2 + d3, b'', d1, d1 + d2[:-2], d1 + doc(el(8, 'b', b'\x05')) + d3, d1 + i32(100), d1 + b'\x00', d1 + b'\x00\x00\x00']:
    hexjob(data, 'all')

# ObjectId
for s in [OID, '5F2B3C4D5E6F708192A3B4C5', '000000000000000000000000', 'ffffffffffffffffffffffff',
          '5f2b3c4d5e6f708192a3b4c', '5f2b3c4d5e6f708192a3b4cg', '5f2b 3c4d5e6f708192a3b4c5',
          '5f2b3c4d5e6f 708192a3b4c', '5f2b 3c4d 5e6f708192a3b4', '', "it's 24 chars long.....",
          '5f2b3c4d5e6f708192a3b4c\u00e9']:
    job('oid', s)
for s in ['2020-01-02T03:04:05Z', '1970-01-01T00:00:00Z', '2106-02-07T06:28:15Z', '2038-01-19T03:14:08.999Z', '2106-02-07T06:28:16Z', '1969-12-31T23:59:59Z']:
    job('oidtime', s)

# Decimal128
DECS = ['1E+6120', '0E-6200', '1.0E-6176', '-1E-6177', 'INF', 'iNfInItY', 'SNAN', '-sNaN', 'nan', '1E-6143', '1.5e+0', '0e0',
        '0', '-0', '1', '-1', '0.1', '1.50E+3', '1E+3', '1e-6', '0.000001', '0.0000001', '123.456e-10',
        '1E+6144', '1E+6145', '1E-6176', '1E-6177', '0E-6177', '0E+7000', '1E+6112', '12345678901234567890123456789012345',
        '1234567890123456789012345678901234', '1234567890123456789012345678901234.0',
        '9.999999999999999999999999999999999E+6144', 'Infinity', '-inf', 'NaN', '-NaN', 'sNaN', 'NaN12',
        ' 7 ', '1_000', '+.5', '5.', '.', '', 'abc', '1e', '-0.00E-2', '100E-2', '0.001E+5']
for s in DECS:
    job('dec', s)
for h in ['01000000000000000000000000004030', '00000000000000000000000000000000', 'ffffffffffffffffffffffffffff0130',
          '0000000000000000000000000000007e', '000000000000000000000000000000fe', '0100000000000000000000000000607c',
          '00000000000000000000000000007a5f', '0a00000000000000000000000000fe5f',
          '00000000000000000000000000000068', '0000000000000000000000000000c0e8',
          (10 ** 34).to_bytes(16, 'little')[:8].hex() + (((10 ** 34) >> 64) | (6176 << 49)).to_bytes(8, 'little').hex(),
          (10 ** 34 + 1).to_bytes(16, 'little')[:8].hex() + (((10 ** 34 + 1) >> 64) | (6176 << 49)).to_bytes(8, 'little').hex(),
          (1).to_bytes(8, 'little').hex() + ((6120 + 6176) << 49).to_bytes(8, 'little').hex()]:
    job('bid', h)

# --- bsondump files ----------------------------------------------------

people = [
    {'_id': bson.ObjectId('5f2b3c4d5e6f708192a3b4c%x' % i), 'name': n, 'age': a,
     'tags': t, 'score': s}
    for i, (n, a, t, s) in enumerate([
        ('Ada', 36, ['math'], 97.5), ('Grace', 85, ['navy', 'cobol'], 99.0),
        ('Linus', 54, [], 88.25), ('Margaret', 87, ['apollo'], 100.0),
        ('Ken', 81, ['unix', 'go'], 91.0)])
]
put('dump/people.bson', b''.join(bson.encode(p) for p in people))
orders = []
for i in range(6):
    orders.append(bson.encode({'order': i, 'items': [{'sku': 'A%d' % j, 'qty': j + i} for j in range(i % 3 + 1)],
                               'total': bson.Decimal128('%d.%02d' % (10 + i * 7, i * 13 % 100)),
                               'when': datetime.datetime(2024, 5, i + 1, 12, 30, i)}))
put('dump/orders.bson', b''.join(orders))
put('dump/truncated.bson', bson.encode({'a': 1}) + bson.encode({'b': 'two'})[:-3])
put('dump/garbage.bson', bson.encode({'a': 1}) + b'\x07\x00\x00\x00\x2a\x00\x00')
put('dump/empty.bson', b'')

# --- import files ------------------------------------------------------

put('import/events.jsonl', '\n'.join([
    '{"kind": "login", "user": {"$oid": "' + OID + '"}, "at": {"$date": "2024-05-01T08:00:00Z"}}',
    '{"kind": "buy", "amount": {"$numberDecimal": "19.99"}, "count": 2, "at": {"$date": "2024-05-01T08:05:30.250Z"}}',
    '',
    '{"kind": "big", "n": 9007199254740993, "ratio": 0.25}',
    '{"kind": "bad", "id": {"$oid": "nope"}}',
    '{"kind": "huge", "n": 99999999999999999999}',
    '{"kind": "logout", "user": {"$oid": "' + OID + '"}, "ok": true}',
]) + '\n')

put('jobs.txt', '\n'.join(jobs) + '\n')
put('files.txt', '\n'.join(['dump/people.bson', 'dump/orders.bson', 'dump/truncated.bson',
                            'dump/garbage.bson', 'dump/empty.bson', 'import/events.jsonl']) + '\n')
print(len(jobs), 'jobs')
