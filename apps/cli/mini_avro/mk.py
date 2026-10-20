# Writes data/: Avro schemas as services keep them (a Kafka signup
# event, an order with money as fixed decimals, Hadoop's Weather, the
# spec's LongList, a metrics sample, Avro's own interop and handshake
# schemas), evolved versions of them for schema resolution, broken
# schemas, datums to encode, container files (null and deflate codecs,
# and broken ones), every schema example from Avro's own tests, and
# data/jobs.tsv, the jobs mini_avro.kara and oracle.py run.
#
# A datum file holds one JSON value per line. JSON has no bytes,
# decimals, dates or times, so a one-key object stands for one:
# {"$bytes": hex}, {"$decimal": text}, {"$date": "YYYY-MM-DD"},
# {"$time": "HH:MM:SS.ffffff"}, {"$datetime": ISO text with an offset}
# and {"$naive": ISO text without one}.
import io
import json
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
sys.path.insert(0, HERE)

FILES = {}


def schema(rel, obj):
    FILES["schemas/" + rel] = json.dumps(obj, indent=2) + "\n"


schema("user_signup.avsc", {
    "type": "record",
    "name": "UserSignup",
    "namespace": "com.example.events",
    "doc": "Emitted once when an account is created.",
    "fields": [
        {"name": "id", "type": {"type": "string", "logicalType": "uuid"}},
        {"name": "email", "type": "string"},
        {"name": "display_name", "type": ["null", "string"], "default": None},
        {"name": "plan", "type": {"type": "enum", "name": "Plan",
                                  "symbols": ["FREE", "PRO", "TEAM"], "default": "FREE"}},
        {"name": "signed_up_at", "type": {"type": "long", "logicalType": "timestamp-millis"}},
        {"name": "birth_date", "type": ["null", {"type": "int", "logicalType": "date"}], "default": None},
        {"name": "referrer", "type": ["null", {
            "type": "record", "name": "Referrer",
            "fields": [
                {"name": "source", "type": "string"},
                {"name": "campaign", "type": ["null", "string"], "default": None},
            ]}], "default": None},
        {"name": "tags", "type": {"type": "array", "items": "string"}, "default": []},
        {"name": "attributes", "type": {"type": "map", "values": "string"}, "default": {}},
        {"name": "credit", "type": {"type": "bytes", "logicalType": "decimal",
                                    "precision": 10, "scale": 2}},
        {"name": "avatar_md5", "type": ["null", {"type": "fixed", "name": "MD5", "size": 16}],
         "default": None},
    ],
})

schema("user_signup_v2.avsc", {
    "type": "record",
    "name": "UserSignup",
    "namespace": "com.example.events",
    "fields": [
        {"name": "id", "type": {"type": "string", "logicalType": "uuid"}},
        {"name": "email", "type": "string"},
        {"name": "display_name", "type": ["null", "string"], "default": None},
        {"name": "plan", "type": {"type": "enum", "name": "Plan",
                                  "symbols": ["FREE", "PRO", "TEAM", "ENTERPRISE"]}},
        {"name": "signed_up_at", "type": {"type": "long", "logicalType": "timestamp-millis"}},
        {"name": "locale", "type": "string", "default": "en-US"},
        {"name": "marketing_opt_in", "type": "boolean", "default": False},
        {"name": "credit", "type": {"type": "bytes", "logicalType": "decimal",
                                    "precision": 10, "scale": 2}},
    ],
})

schema("user_signup_v0.avsc", {
    "type": "record",
    "name": "UserSignup",
    "namespace": "com.example.events",
    "fields": [
        {"name": "email", "type": "string"},
        {"name": "plan", "type": {"type": "enum", "name": "Plan", "symbols": ["FREE", "PRO"]}},
        {"name": "region", "type": "string"},
    ],
})

schema("order.avsc", {
    "type": "record",
    "name": "Order",
    "namespace": "com.example.shop",
    "fields": [
        {"name": "order_id", "type": "long"},
        {"name": "status", "type": {"type": "enum", "name": "Status",
                                    "symbols": ["PLACED", "PAID", "SHIPPED", "CANCELLED"]}},
        {"name": "placed_at", "type": {"type": "long", "logicalType": "timestamp-micros"}},
        {"name": "ship_to", "type": {
            "type": "record", "name": "Address", "namespace": "com.example.common",
            "fields": [
                {"name": "line1", "type": "string"},
                {"name": "city", "type": "string"},
                {"name": "postcode", "type": ["null", "string"]},
                {"name": "country", "type": {"type": "fixed", "name": "CountryCode", "size": 2}},
            ]}},
        {"name": "bill_to", "type": ["null", "com.example.common.Address"]},
        {"name": "lines", "type": {"type": "array", "items": {
            "type": "record", "name": "LineItem",
            "fields": [
                {"name": "sku", "type": "string"},
                {"name": "qty", "type": "int"},
                {"name": "unit_price", "type": {"type": "fixed", "name": "Money", "size": 8,
                                                "logicalType": "decimal", "precision": 18, "scale": 4}},
            ]}}},
        {"name": "discount", "type": ["null", "double"]},
        {"name": "delivery_window", "type": ["null", {"type": "int", "logicalType": "time-millis"}]},
        {"name": "notes", "type": {"type": "map", "values": ["string", "null"]}},
    ],
})

schema("weather.avsc", {
    "type": "record",
    "name": "Weather",
    "namespace": "test",
    "doc": "A weather reading.",
    "fields": [
        {"name": "station", "type": "string", "order": "ignore"},
        {"name": "time", "type": "long"},
        {"name": "temp", "type": "int"},
    ],
})

schema("weather_reader.avsc", {
    "type": "record",
    "name": "Weather",
    "namespace": "test",
    "fields": [
        {"name": "station", "type": "string"},
        {"name": "temp", "type": "double"},
        {"name": "time", "type": "long"},
        {"name": "elevation_m", "type": ["int", "null"], "default": 0},
        {"name": "source", "type": "bytes", "default": "ÿþ"},
        {"name": "sensor", "type": {"type": "record", "name": "Sensor", "fields": [
            {"name": "model", "type": "string", "default": "WX-1"},
            {"name": "calibrated", "type": "boolean", "default": True},
        ]}, "default": {"model": "WX-9"}},
    ],
})

schema("weather_float.avsc", {
    "type": "record",
    "name": "Weather",
    "namespace": "test",
    "fields": [
        {"name": "temp", "type": "float"},
        {"name": "station", "type": "string"},
        {"name": "humidity", "type": "double", "default": 1},
    ],
})

schema("weather_strict.avsc", {
    "type": "record",
    "name": "Weather",
    "namespace": "test",
    "fields": [
        {"name": "station", "type": "string"},
        {"name": "dew_point", "type": "int"},
    ],
})

schema("weather_renamed.avsc", {
    "type": "record",
    "name": "Reading",
    "namespace": "test",
    "aliases": ["test.Weather"],
    "fields": [{"name": "station", "type": "string"}],
})

schema("long_list.avsc", {
    "type": "record",
    "name": "LongList",
    "aliases": ["LinkedLongs"],
    "fields": [
        {"name": "value", "type": "long"},
        {"name": "next", "type": ["null", "LongList"]},
    ],
})

schema("metric_sample.avsc", {
    "type": "record",
    "name": "Sample",
    "namespace": "io.example.metrics",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "labels", "type": {"type": "map", "values": "string"}},
        {"name": "value", "type": ["long", "double"]},
        {"name": "ts", "type": {"type": "long", "logicalType": "timestamp-micros"}},
        {"name": "kind", "type": ["null", {"type": "enum", "name": "Kind",
                                           "symbols": ["COUNTER", "GAUGE", "HISTOGRAM"]}]},
        {"name": "buckets", "type": ["null", {"type": "array", "items": {
            "type": "record", "name": "Bucket", "fields": [
                {"name": "le", "type": "double"},
                {"name": "count", "type": "long"},
            ]}}]},
    ],
})

schema("value_union.avsc", ["null", "int", "long", "float", "double", "string", "boolean"])
schema("long_reader.avsc", "long")
schema("string_or_long.avsc", ["string", "long"])
schema("plan_reader.avsc", {"type": "enum", "name": "com.example.events.Plan",
                            "symbols": ["FREE", "PRO"]})
schema("bytes_decimal.avsc", {"type": "bytes", "logicalType": "decimal", "precision": 4, "scale": 2})
schema("bytes_decimal_raw.avsc", "bytes")

for name in ("interop.avsc", "HandshakeRequest.avsc", "HandshakeResponse.avsc"):
    with open(os.path.join(HERE, "avro", name), encoding="utf-8") as f:
        FILES["schemas/" + name] = f.read()

BROKEN = {
    "duplicate_field.avsc": {"type": "record", "name": "Account", "fields": [
        {"name": "id", "type": "long"}, {"name": "id", "type": "string"}]},
    "reserved_name.avsc": {"type": "record", "name": "int", "fields": []},
    "space_in_name.avsc": {"type": "fixed", "name": "dr. spaceman", "size": 314},
    "missing_size.avsc": {"type": "fixed", "name": "Hash"},
    "negative_size.avsc": {"type": "fixed", "name": "Hash", "size": -1},
    "enum_bad_default.avsc": {"type": "enum", "name": "Color", "symbols": ["RED", "GREEN"],
                              "default": "BLUE"},
    "enum_dup_symbol.avsc": {"type": "enum", "name": "Color", "symbols": ["RED", "RED"]},
    "enum_symbol_space.avsc": {"type": "enum", "name": "Color", "symbols": ["DARK RED"]},
    "enum_symbols_string.avsc": {"type": "enum", "name": "Status", "symbols": "OK FAIL"},
    "enum_symbol_number.avsc": {"type": "enum", "name": "Status", "symbols": ["OK", 2]},
    "union_dup.avsc": ["null", "string", "null"],
    "union_logical_dup.avsc": ["long", {"type": "long", "logicalType": "timestamp-millis"}],
    "union_nested.avsc": ["null", ["int", "string"]],
    "unknown_type.avsc": {"type": "record", "name": "Event", "fields": [
        {"name": "at", "type": "datetime"}]},
    "undefined_ref.avsc": {"type": "array", "items": "com.example.Missing"},
    "undefined_ref_union.avsc": {"type": "record", "name": "Event", "namespace": "com.example",
                                 "fields": [{"name": "who", "type": ["null", "User"]}]},
    "bad_array_items.avsc": {"type": "record", "name": "Batch", "namespace": "com.example",
                             "fields": [{"name": "rows", "type": {"type": "array",
                                                                  "items": {"type": "rec"}}}]},
    "bad_map_values.avsc": {"type": "map", "values": {"type": "enum", "name": "E"}},
    "fields_not_list.avsc": {"type": "record", "name": "Rainer",
                             "fields": "His vision, from the constantly passing bars"},
    "no_fields.avsc": {"type": "record", "name": "Empty"},
    "field_no_type.avsc": {"type": "record", "name": "Event",
                           "fields": [{"name": "Sponsor"}, {"name": "City", "type": "string"}]},
    "field_no_name.avsc": {"type": "record", "name": "Address",
                           "fields": [{"type": "string"}, {"type": "string", "name": "City"}]},
    "bad_order.avsc": {"type": "record", "name": "Row",
                       "fields": [{"name": "k", "type": "int", "order": "up"}]},
    "name_list.avsc": {"type": "record", "name": ["Tom", "Jerry"], "fields": []},
    "no_type.avsc": {"name": "Thing", "fields": []},
    "type_number.avsc": {"type": 5},
    "type_panther.avsc": {"type": "panther"},
    "empty_namespace_part.avsc": {"type": "record", "name": "com..example.Event", "fields": []},
    "top_level_ref.avsc": "com.example.Event",
    "number_schema.avsc": 42,
    "decimal_too_precise.avsc": {"type": "fixed", "name": "Tiny", "size": 2,
                                 "logicalType": "decimal", "precision": 6, "scale": 2},
}
for rel, obj in BROKEN.items():
    FILES["schemas/broken/" + rel] = json.dumps(obj) + "\n"
FILES["schemas/broken/trailing_comma.avsc"] = '{"type": "enum", "name": "E", "symbols": ["A", "B",]}\n'
FILES["schemas/broken/single_quotes.avsc"] = "{'type': 'string'}\n"
FILES["schemas/broken/empty.avsc"] = ""

DATUMS = {
    "user_signup.jsonl": [
        {"id": "3f2b8c1e-6d4a-4f0e-9b7a-2c5d8e1f4a6b", "email": "ana@example.com",
         "display_name": "Ana", "plan": "PRO", "signed_up_at": {"$datetime": "2026-10-19T07:42:00.123+00:00"},
         "birth_date": {"$date": "1994-03-08"}, "referrer": {"source": "newsletter", "campaign": "fall-26"},
         "tags": ["beta", "eu"], "attributes": {"utm_medium": "email"},
         "credit": {"$decimal": "25.00"}, "avatar_md5": {"$bytes": "9e107d9d372bb6826bd81d3542a419d6"}},
        {"id": "a4818e1c-8e59-11eb-8dcd-0242ac130003", "email": "li@example.org",
         "display_name": None, "plan": "FREE", "signed_up_at": {"$datetime": "2026-10-19T09:15:30.999+02:00"},
         "birth_date": None, "referrer": None, "tags": [], "attributes": {},
         "credit": {"$decimal": "-3.5"}, "avatar_md5": None},
        {"id": "not-a-uuid", "email": "bad@example.com", "plan": "PRO",
         "signed_up_at": {"$datetime": "2026-10-19T07:42:00+00:00"}, "credit": {"$decimal": "1"}},
        {"id": "570feebe-2bbc-4937-98df-285944e1dbbd", "email": "naive@example.com", "plan": "TEAM",
         "signed_up_at": {"$naive": "2026-10-19T07:42:00"}, "tags": [], "attributes": {},
         "credit": {"$decimal": "0"}},
        {"id": "570feebe-2bbc-4937-98df-285944e1dbbd", "email": "x@example.com", "plan": "GOLD",
         "signed_up_at": {"$datetime": "2026-10-19T07:42:00+00:00"}, "tags": [], "attributes": {},
         "credit": {"$decimal": "0"}},
        {"id": "570feebe-2bbc-4937-98df-285944e1dbbd", "email": "x@example.com", "plan": "TEAM",
         "signed_up_at": {"$datetime": "2026-10-19T07:42:00+00:00"}, "tags": [], "attributes": {},
         "credit": {"$decimal": "0.125"}},
        {"id": "570feebe-2bbc-4937-98df-285944e1dbbd", "email": "x@example.com", "plan": "TEAM",
         "signed_up_at": {"$datetime": "2026-10-19T07:42:00+00:00"}, "tags": [], "attributes": {},
         "credit": {"$decimal": "12345678.99"}, "nickname": "extra"},
        {"id": "570feebe-2bbc-4937-98df-285944e1dbbd", "email": "x@example.com", "plan": "TEAM",
         "signed_up_at": {"$datetime": "2026-10-19T07:42:00+00:00"}, "tags": ["ok", 7],
         "attributes": {}, "credit": {"$decimal": "0"}},
        {"id": "570feebe-2bbc-4937-98df-285944e1dbbd", "email": "x@example.com", "plan": "TEAM",
         "signed_up_at": {"$datetime": "2026-10-19T07:42:00+00:00"}, "tags": [],
         "attributes": {"k": None}, "credit": {"$decimal": "0"}, "avatar_md5": {"$bytes": "0102"}},
    ],
    "order.jsonl": [
        {"order_id": 9007199254740993, "status": "PAID",
         "placed_at": {"$datetime": "2026-10-18T23:59:59.999999+00:00"},
         "ship_to": {"line1": "Keizersgracht 123", "city": "Amsterdam", "postcode": "1015 CJ",
                     "country": {"$bytes": "4e4c"}},
         "bill_to": None,
         "lines": [{"sku": "KB-ERGO-01", "qty": 1, "unit_price": {"$decimal": "149.9900"}},
                   {"sku": "USB-C-2M", "qty": 3, "unit_price": {"$decimal": "-12.5"}}],
         "discount": 0.15, "delivery_window": {"$time": "14:30:00"}, "notes": {"gift": "yes", "door": None}},
        {"order_id": -1, "status": "SHIPPED",
         "placed_at": {"$datetime": "1000-01-01T00:00:00+00:00"},
         "ship_to": {"line1": "1 Main St", "city": "Springfield", "postcode": None,
                     "country": {"$bytes": "5553"}},
         "bill_to": {"line1": "PO Box 7", "city": "Shelbyville", "postcode": "62565",
                     "country": {"$bytes": "5553"}},
         "lines": [], "discount": None, "delivery_window": None, "notes": {}},
        {"order_id": 3, "status": "PLACED", "placed_at": {"$datetime": "2000-01-18T02:02:01.123499+10:00"},
         "ship_to": {"line1": "x", "city": "y", "postcode": None, "country": {"$bytes": "5553"}},
         "bill_to": None, "lines": [{"sku": "A", "qty": 1, "unit_price": {"$decimal": "1.23456"}}],
         "discount": 1, "delivery_window": None, "notes": {}},
        {"order_id": 4, "status": "PLACED", "placed_at": {"$datetime": "2026-10-19T00:00:00+00:00"},
         "ship_to": {"line1": "x", "city": "y", "postcode": None, "country": {"$bytes": "5553"}},
         "bill_to": None, "lines": [{"sku": "A", "qty": 2147483648, "unit_price": {"$decimal": "1"}}],
         "discount": None, "delivery_window": None, "notes": {}},
    ],
    "weather.jsonl": [
        {"station": "011990-99999", "time": -619524000000, "temp": 0},
        {"station": "011990-99999", "time": -619506000000, "temp": 22},
        {"station": "011990-99999", "time": -619484400000, "temp": -11},
        {"station": "012650-99999", "time": -655531200000, "temp": 111},
        {"station": "012650-99999", "time": -655509600000, "temp": 78},
    ],
    "long_list.jsonl": [
        {"value": 1, "next": {"value": 2, "next": {"value": 3, "next": None}}},
        {"value": 0, "next": None},
    ],
    "metrics.jsonl": [
        {"name": "http_requests_total", "labels": {"method": "GET", "code": "200"}, "value": 1027,
         "ts": {"$datetime": "2026-10-19T07:42:00.000001+00:00"}, "kind": "COUNTER", "buckets": None},
        {"name": "node_load1", "labels": {}, "value": 0.42,
         "ts": {"$datetime": "2026-10-19T07:42:15+00:00"}, "kind": "GAUGE", "buckets": None},
        {"name": "rpc_duration_seconds", "labels": {"service": "auth"}, "value": 3.0,
         "ts": {"$datetime": "2026-10-19T07:42:30+00:00"}, "kind": "HISTOGRAM",
         "buckets": [{"le": 0.1, "count": 40}, {"le": 1.0, "count": 52}, {"le": float("inf"), "count": 53}]},
        {"name": "up", "labels": {"job": "node"}, "value": True,
         "ts": {"$datetime": "2026-10-19T07:42:45+00:00"}, "kind": None, "buckets": None},
    ],
    "values.jsonl": [None, 0, 7, -2147483648, 2147483648, 9223372036854775807, 9223372036854775808,
                     1.5, -0.0, 1e300, "", "héllo ☃", True, False, [1], {"a": 1},
                     {"$bytes": "00ff"}, "\ud800"],
    "interop.jsonl": [
        {"intField": 12, "longField": 15234324, "stringField": "hey", "boolField": True,
         "floatField": 1234.0, "doubleField": -1234.0, "bytesField": {"$bytes": "3132333435"},
         "nullField": None, "arrayField": [5.0, 0.0, 12.0],
         "mapField": {"a": {"label": "a"}, "bee": {"label": "cee"}},
         "unionField": 12.0, "enumField": "C", "fixedField": {"$bytes": "31323334353637383930313233343536"},
         "recordField": {"label": "blah", "children": [{"label": "inner", "children": []}]}},
        {"intField": 1, "longField": 2, "stringField": "", "boolField": False,
         "floatField": 0.1, "doubleField": 0.1, "bytesField": {"$bytes": ""},
         "nullField": None, "arrayField": [], "mapField": {},
         "unionField": [{"$bytes": "ff"}, {"$bytes": ""}], "enumField": "A",
         "fixedField": {"$bytes": "00000000000000000000000000000000"},
         "recordField": {"label": "", "children": []}},
        {"intField": 1, "longField": 2, "stringField": "", "boolField": False,
         "floatField": 3.4028235e38, "doubleField": float("nan"), "bytesField": {"$bytes": ""},
         "nullField": None, "arrayField": [float("-inf")], "mapField": {},
         "unionField": False, "enumField": "B",
         "fixedField": {"$bytes": "00000000000000000000000000000000"},
         "recordField": {"label": "", "children": []}},
    ],
    "decimals.jsonl": [{"$decimal": "3.14"}, {"$decimal": "-3.14"}, {"$decimal": "99.99"},
                       {"$decimal": "-0.01"}, {"$decimal": "0"}, {"$decimal": "12"},
                       {"$decimal": "1.5E+1"}, {"$decimal": "0.001"}, {"$decimal": "-128"},
                       {"$decimal": "127.99"}, {"$decimal": "-327.68"}],
}
DATUMS["weather_two.jsonl"] = DATUMS["weather.jsonl"][:2]
for rel, rows in DATUMS.items():
    FILES["datums/" + rel] = "".join(json.dumps(r) + "\n" for r in rows)

# Encoded datums written with one schema, for reading with another.
RAW = {
    "plan_enterprise.bin": "06",
    "union_branch_9.bin": "12",
    "enum_index_7.bin": "0e",
    "truncated_string.bin": "0a6869",
    "negative_length.bin": "01",
    "long_blocks.bin": "03" "06" "02" "04" "06" "00",
    "decimal_rounding.bin": "04" "3039",
}

# Container files. The sync marker is fixed so the files can be written
# here; Avro picks 16 random bytes.
SYNC = bytes.fromhex("8e3a5f9c01d24b67a9f0c3e15d7b2846")


def zigzag(n):
    n = (n << 1) ^ (n >> 63)
    out = bytearray()
    while n & ~0x7F:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    out.append(n)
    return bytes(out)


def avro_bytes(b):
    return zigzag(len(b)) + b


def container(schema_text, blocks, codec=None, sync=SYNC, magic=b"Obj\x01", extra_meta=()):
    meta = [("avro.schema", schema_text.encode())]
    if codec is not None:
        meta.append(("avro.codec", codec.encode()))
    meta.extend(extra_meta)
    out = bytearray(magic)
    out += zigzag(len(meta))
    for k, v in meta:
        out += avro_bytes(k.encode()) + avro_bytes(v)
    out += zigzag(0)
    out += sync
    for count, payload, block_sync in blocks:
        out += zigzag(count)
        if codec == "deflate":
            c = zlib.compress(payload)[2:-1]
            out += avro_bytes(c)
        else:
            out += avro_bytes(payload)
        out += block_sync
    return bytes(out)


def weather_record(station, time, temp):
    return avro_bytes(station.encode()) + zigzag(time) + zigzag(temp)


def make_containers():
    wschema = json.dumps({"type": "record", "name": "Weather", "namespace": "test", "fields": [
        {"name": "station", "type": "string"}, {"name": "time", "type": "long"},
        {"name": "temp", "type": "int"}]})
    rows = [("011990-99999", -619524000000, 0), ("011990-99999", -619506000000, 22),
            ("011990-99999", -619484400000, -11), ("012650-99999", -655531200000, 111),
            ("012650-99999", -655509600000, 78)]
    recs = [weather_record(*r) for r in rows]
    files = {}
    files["weather.avro"] = container(wschema, [(5, b"".join(recs), SYNC)])
    files["weather-deflate.avro"] = container(wschema, [(3, b"".join(recs[:3]), SYNC),
                                                       (2, b"".join(recs[3:]), SYNC)], codec="deflate")
    files["weather-null-codec.avro"] = container(wschema, [(2, b"".join(recs[:2]), SYNC)], codec="null",
                                                 extra_meta=[("created.by", b"mk.py")])
    files["empty.avro"] = container(wschema, [])
    files["empty-block.avro"] = container(wschema, [(0, b"", SYNC), (1, recs[0], SYNC)])
    files["broken/snappy.avro"] = container(wschema, [(1, recs[0], SYNC)], codec="snappy")
    files["broken/bad-magic.avro"] = container(wschema, [(1, recs[0], SYNC)], magic=b"Obj\x02")
    files["broken/not-avro.avro"] = b"PAR1\x15\x04\x15\x10\x15\x14L\x15\x02"
    whole = container(wschema, [(5, b"".join(recs), SYNC)])
    files["broken/truncated.avro"] = whole[:-30]
    files["broken/bad-sync.avro"] = container(wschema, [(2, b"".join(recs[:2]), bytes(16)),
                                                       (1, recs[2], SYNC)])
    files["broken/count-too-high.avro"] = container(wschema, [(3, b"".join(recs[:2]), SYNC)])
    files["broken/no-schema.avro"] = (b"Obj\x01" + zigzag(1) + avro_bytes(b"avro.codec")
                                      + avro_bytes(b"null") + zigzag(0) + SYNC)
    # The interop file: every type, as Avro's own interop data carries it.
    with open(os.path.join(HERE, "avro", "interop.avsc"), encoding="utf-8") as f:
        ischema = f.read()
    import avro.io
    import avro.schema
    s = avro.schema.parse(ischema)
    buf = io.BytesIO()
    enc = avro.io.BinaryEncoder(buf)
    datum = {"intField": 12, "longField": 15234324, "stringField": "hey", "boolField": True,
             "floatField": 1234.0, "doubleField": -1234.0, "bytesField": b"12312adf",
             "nullField": None, "arrayField": [5.0, 0.0, 12.0],
             "mapField": {"a": {"label": "a"}, "bee": {"label": "cee"}},
             "unionField": 12.0, "enumField": "C", "fixedField": b"1019181716151413",
             "recordField": {"label": "blah", "children": [{"label": "inner", "children": []}]}}
    avro.io.DatumWriter(s).write(datum, enc)
    files["interop-deflate.avro"] = container(ischema, [(1, buf.getvalue(), SYNC)], codec="deflate")
    return files


JOBS = []
for rel in ["user_signup.avsc", "user_signup_v2.avsc", "order.avsc", "weather.avsc",
            "weather_reader.avsc", "long_list.avsc", "metric_sample.avsc", "value_union.avsc",
            "interop.avsc", "HandshakeRequest.avsc", "HandshakeResponse.avsc",
            "bytes_decimal.avsc", "plan_reader.avsc"]:
    JOBS.append(["schema", "schemas/" + rel])
for rel in sorted(BROKEN) + ["trailing_comma.avsc", "single_quotes.avsc", "empty.avsc"]:
    JOBS.append(["schema", "schemas/broken/" + rel])
JOBS += [
    ["vectors"],
    ["encode", "schemas/user_signup.avsc", "datums/user_signup.jsonl"],
    ["encode", "schemas/order.avsc", "datums/order.jsonl"],
    ["encode", "schemas/weather.avsc", "datums/weather.jsonl"],
    ["encode", "schemas/long_list.avsc", "datums/long_list.jsonl"],
    ["encode", "schemas/metric_sample.avsc", "datums/metrics.jsonl"],
    ["encode", "schemas/value_union.avsc", "datums/values.jsonl"],
    ["encode", "schemas/interop.avsc", "datums/interop.jsonl"],
    ["encode", "schemas/bytes_decimal.avsc", "datums/decimals.jsonl"],
    ["resolve", "schemas/user_signup.avsc", "schemas/user_signup_v2.avsc", "datums/user_signup.jsonl"],
    ["resolve", "schemas/user_signup.avsc", "schemas/user_signup_v0.avsc", "datums/user_signup.jsonl"],
    ["resolve", "schemas/weather.avsc", "schemas/weather_reader.avsc", "datums/weather.jsonl"],
    ["resolve", "schemas/weather.avsc", "schemas/weather_float.avsc", "datums/weather_two.jsonl"],
    ["resolve", "schemas/weather.avsc", "schemas/weather_strict.avsc", "datums/weather_two.jsonl"],
    ["resolve", "schemas/weather.avsc", "schemas/weather_renamed.avsc", "datums/weather_two.jsonl"],
    ["resolve", "schemas/value_union.avsc", "schemas/long_reader.avsc", "datums/values.jsonl"],
    ["resolve", "schemas/value_union.avsc", "schemas/string_or_long.avsc", "datums/values.jsonl"],
    ["resolve", "schemas/bytes_decimal.avsc", "schemas/bytes_decimal_raw.avsc", "datums/decimals.jsonl"],
    ["decode", "schemas/plan_reader.avsc", "raw/plan_enterprise.bin"],
    ["decode", "schemas/value_union.avsc", "raw/union_branch_9.bin"],
    ["decode", "schemas/value_union.avsc", "raw/negative_length.bin"],
    ["decode", "schemas/plan_reader.avsc", "raw/enum_index_7.bin"],
    ["decode", "schemas/value_union.avsc", "raw/truncated_string.bin"],
    ["decode", "schemas/bytes_decimal_raw.avsc", "raw/negative_length.bin"],
    ["decode", "schemas/long_reader.avsc", "raw/long_blocks.bin"],
    ["decode", "schemas/bytes_decimal.avsc", "raw/decimal_rounding.bin"],
    ["read", "files/weather.avro"],
    ["read", "files/weather-deflate.avro"],
    ["read", "files/weather-null-codec.avro"],
    ["read", "files/weather.avro", "schemas/weather_reader.avsc"],
    ["read", "files/weather-deflate.avro", "schemas/weather_strict.avsc"],
    ["read", "files/empty.avro"],
    ["read", "files/empty-block.avro"],
    ["read", "files/interop-deflate.avro"],
]
for rel in ["snappy", "bad-magic", "not-avro", "truncated", "bad-sync", "count-too-high", "no-schema"]:
    JOBS.append(["read", "files/broken/%s.avro" % rel])
JOBS += [
    ["write", "schemas/weather.avsc", "datums/weather.jsonl"],
    ["write", "schemas/user_signup.avsc", "datums/user_signup.jsonl"],
    ["write", "schemas/long_list.avsc", "datums/long_list.jsonl"],
    ["cat", "data/files/weather.avro"],
    ["cat", "--format", "json-pretty", "data/files/weather-deflate.avro"],
    ["cat", "--format", "csv", "--header", "data/files/weather.avro"],
    ["cat", "-f", "csv", "--skip", "1", "--count", "2", "data/files/weather.avro", "data/files/weather-deflate.avro"],
    ["cat", "-f", "csv", "--fields", "temp, station", "data/files/weather.avro"],
    ["cat", "-f", "json-pretty", "--fields", "temp,nope", "-n", "2", "data/files/weather.avro"],
    ["cat", "--print-schema", "data/files/interop-deflate.avro"],
    ["cat", "data/files/interop-deflate.avro"],
    ["cat", "-f", "csv", "data/files/interop-deflate.avro"],
    ["cat", "--header", "data/files/weather.avro"],
    ["cat", "-s", "4", "data/files/weather.avro", "data/files/empty.avro"],
    ["cat", "data/files/broken/bad-magic.avro"],
    ["tool-write", "--schema", "data/schemas/weather.avsc", "data/datums/weather.jsonl"],
    ["tool-write", "-s", "data/schemas/weather.avsc", "data/rows/weather.csv"],
    ["tool-write", "-s", "data/schemas/weather.avsc", "-f", "json", "data/rows/weather.txt"],
    ["tool-write", "-s", "data/schemas/weather.avsc", "data/rows/weather.tsv"],
    ["tool-write", "-s", "data/schemas/weather.avsc", "data/rows/weather-bad.csv"],
    ["tool-write", "-s", "data/schemas/metric_sample.avsc", "-f", "json", "data/datums/metrics.jsonl"],
]

ROWS = {
    "weather.csv": "011990-99999,-619524000000,0\n011990-99999,-619506000000,22\n"
                   "\"012650-99999\",-655531200000, 111\n",
    "weather.txt": '{"station": "011990-99999", "time": 1, "temp": 2}\n\n'
                   '  {"station": "x", "time": 3, "temp": 4}  \n',
    "weather.tsv": "011990-99999\t1\t2\n",
    "weather-bad.csv": "011990-99999,-619524000000,cold\n",
}


def write(rel, data):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def main():
    for rel, text in FILES.items():
        write(rel, text.encode("utf-8"))
    for rel, text in ROWS.items():
        write("rows/" + rel, text.encode("utf-8"))
    for rel, hx in RAW.items():
        write("raw/" + rel, bytes.fromhex(hx))
    for rel, b in make_containers().items():
        write("files/" + rel, b)
    import avro.test.test_schema as t
    vectors = [str(e) for e in t.EXAMPLES + t.OTHER_PROP_EXAMPLES]
    write("vectors.txt", "".join(v + "\n" for v in vectors).encode("utf-8"))
    write("jobs.tsv", "".join("\t".join(j) + "\n" for j in JOBS).encode("utf-8"))


if __name__ == "__main__":
    main()
