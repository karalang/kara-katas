# Writes data/: the schemas (data/schemas.json), the documents a service
# would receive (data/docs/*.jsonl, one JSON value per line) and the jobs
# (data/jobs.tsv). oracle.py and mini_marshmallow.kara both read them.
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def F(kind, **opts):
    d = {"type": kind}
    d.update(opts)
    return d


def V(name, **args):
    return [name, args]


ENUMS = {
    "OrderStatus": [["PENDING", "pending"], ["PAID", "paid"], ["SHIPPED", "shipped"], ["CANCELLED", "cancelled"]],
    "Category": [["NEWS", 1], ["TECH", 2], ["LIFE", 3]],
    "Visibility": [["PUBLIC", "public"], ["PRIVATE", "private"], ["DRAFT", 0]],
    "Level": [["DEBUG", 10], ["INFO", 20], ["WARNING", 30], ["ERROR", 40]],
}

SCHEMAS = []


def schema(name, fields, base=None, meta=None, hooks=None, error_messages=None):
    d = {"name": name, "fields": fields}
    if base is not None:
        d["base"] = base
    if meta is not None:
        d["meta"] = meta
    if hooks:
        d["hooks"] = hooks
    if error_messages:
        d["error_messages"] = error_messages
    SCHEMAS.append(d)


def H(tag, fn, **kw):
    d = {"tag": tag, "fn": fn}
    d.update(kw)
    return d


schema("AddressSchema", [
    ["street", F("String", required=True, validate=[V("Length", min=1)], pre_load=["strip"])],
    ["city", F("String", required=True)],
    ["postcode", F("String", validate=[V("Regexp", regex="^\\d{5}(-\\d{4})?$", error="Not a US ZIP code: {input}.")])],
    ["country", F("String", load_default="US", validate=[V("Length", equal=2), V("OneOf", choices=["US", "CA", "GB", "DE", "FR"])], pre_load=["upper"])],
])

schema("UserSchema", [
    ["id", F("Integer", dump_only=True)],
    ["username", F("String", required=True, pre_load=["strip", "lower"],
                   validate=[V("Length", min=3, max=20), V("Regexp", regex="^[a-z0-9_]+$", error="Only lowercase letters, digits and underscores.")])],
    ["email", F("Email", required=True, error_messages={"required": "An email address is required."})],
    ["password", F("String", load_only=True, validate=[V("Length", min=8)])],
    ["age", F("Integer", allow_none=True, validate=[V("Range", min=13, max=130)])],
    ["role", F("String", load_default="member", dump_default="member", validate=[V("OneOf", choices=["admin", "member", "guest"], labels=["Administrator", "Member", "Guest"], error="{input} is not one of {choices} ({labels}).")])],
    ["signup", F("DateTime", data_key="signedUpAt")],
    ["address", F("Nested", nested="AddressSchema")],
    ["tags", F("List", inner=F("String", validate=[V("Length", max=10)]), load_default={"$fn": "new_list"})],
    ["website", F("Url", allow_none=True)],
    ["display", F("Method", serialize="display_name")],
], hooks=[H("validates", "check_username", field_names=["username"]),
          H("pre_load", "unwrap"),
          H("post_dump", "drop_none")])

schema("SignupSchema", [
    ["confirm", F("String", load_only=True, required=True, data_key="confirmPassword")],
    ["terms", F("Boolean", required=True, load_only=True, validate=[V("Equal", comparable=True, error="You must accept the terms.")])],
], base="UserSchema", hooks=[H("validates_schema", "passwords_match"),
                             H("validates_schema", "adult_admin", skip_on_field_errors=False)])

schema("OrderItemSchema", [
    ["sku", F("String", required=True, validate=[V("Regexp", regex="[A-Z]{3}-\\d{4}$")])],
    ["qty", F("Integer", strict=True, load_default=1, validate=[V("Range", min=1, max=99)])],
    ["price", F("Float", required=True, validate=[V("Range", min=0, min_inclusive=False)])],
    ["gift", F("Boolean", load_default=False)],
])

schema("OrderSchema", [
    ["id", F("UUID", required=True)],
    ["customer", F("Pluck", nested="UserSchema", field_name="username")],
    ["watchers", F("Pluck", nested="UserSchema", field_name="username", many=True)],
    ["billing", F("Nested", nested="AddressSchema", unknown="exclude")],
    ["items", F("List", inner=F("Nested", nested="OrderItemSchema"), required=True, validate=[V("Length", min=1, max=5)])],
    ["status", F("Enum", enum="OrderStatus", load_default="PENDING")],
    ["placed", F("DateTime", required=True)],
    ["ship_by", F("Date")],
    ["notes", F("String", allow_none=True, load_default=None)],
    ["total", F("Float", dump_only=True)],
    ["coupon", F("String", validate=[V("NoneOf", iterable=["EXPIRED", "TEST"], error="Coupon {input} cannot be used.")])],
], hooks=[H("validates_schema", "ship_after_placed"),
          H("post_load", "compute_total"),
          H("post_dump", "add_links", pass_original=True)])

schema("EventSchema", [
    ["name", F("String", required=True)],
    ["starts", F("AwareDateTime", required=True, default_timezone=0)],
    ["ends", F("AwareDateTime")],
    ["local", F("NaiveDateTime", timezone=0)],
    ["alarm", F("Time")],
    ["day", F("Date")],
    ["length", F("TimeDelta", precision="minutes")],
    ["timeout", F("TimeDelta", precision="milliseconds")],
    ["every", F("TimeDelta", precision="weeks")],
    ["level", F("Enum", enum="Level", by_value=F("Integer"), load_default=20)],
], hooks=[H("validates_schema", "date_order", skip_on_field_errors=False)])

schema("MetricSchema", [
    ["name", F("String", required=True, validate=[V("Regexp", regex="[a-z][a-z0-9_.]*$", flags=0)])],
    ["value", F("Float", allow_nan=True)],
    ["count", F("Integer", as_string=True)],
    ["ratio", F("Float", as_string=True, validate=[V("Range", min=0, max=1)])],
    ["ts", F("DateTime", format="timestamp")],
    ["ts_ms", F("DateTime", format="timestamp_ms")],
    ["labels", F("Dict", keys=F("String", validate=[V("Regexp", regex="[a-z_]+$")]), values=F("String", validate=[V("Length", max=12)]))],
    ["enabled", F("Boolean")],
    ["flags", F("Dict", values=F("Boolean", truthy=["on", "enabled"], falsy=["off", "disabled"]))],
    ["host", F("Raw")],
    ["buckets", F("Dict", keys=F("Integer"), values=F("Integer"))],
])

schema("ConfigSchema", [
    ["host", F("String", load_default="localhost")],
    ["port", F("Integer", load_default=8080, validate=[V("Range", min=1, max=65535, error="Port {input} is outside {min}..{max}.")])],
    ["debug", F("Boolean", load_default=False)],
    ["mode", F("Constant", constant="production")],
    ["servers", F("List", inner=F("Tuple", tuple_fields=[F("String"), F("Integer", validate=[V("Range", min=1)])]))],
    ["limits", F("Dict", keys=F("String", validate=[V("OneOf", choices=["cpu", "mem", "disk"])]), values=F("Integer", validate=[V("Range", min=0)]))],
    ["retry", F("Nested", nested={"times": F("Integer", load_default=3, validate=[V("Range", min=0, max=10)]),
                                  "backoff": F("Float", load_default=0.5)})],
    ["root", F("String", attribute="paths.root", data_key="root_dir")],
    ["logs", F("String", attribute="paths.logs", data_key="log_dir")],
    ["workers", F("Integer", validate=["even"])],
], meta={"unknown": "include"})

schema("CommentSchema", [
    ["id", F("Integer")],
    ["text", F("String", required=True, validate=["not_blank", V("Length", max=40)])],
    ["author", F("Pluck", nested="UserSchema", field_name="username", required=True)],
    ["replies", F("List", inner=F("Nested", nested="CommentSchema", exclude=["id"]))],
])

schema("ArticleSchema", [
    ["title", F("String", required=True, validate=[V("Length", min=3, max=60)])],
    ["body", F("String", load_default="")],
    ["author", F("Nested", nested="UserSchema", only=["username", "email"], required=True)],
    ["published", F("Date", format="%d/%m/%Y")],
    ["updated", F("DateTime", format="%Y-%m-%d %H:%M")],
    ["category", F("Enum", enum="Category", by_value=True)],
    ["visibility", F("Enum", enum="Visibility", by_value=True, load_default="public")],
    ["coauthors", F("Nested", nested="UserSchema", many=True, only=["username"])],
    ["comments", F("List", inner=F("Nested", nested="CommentSchema"))],
    ["extra", F("Raw")],
    ["slug", F("String", dump_only=True)],
    ["words", F("Function", serialize="word_count")],
], hooks=[H("post_load", "add_slug"), H("pre_dump", "default_title"), H("validates", "check_title", field_names=["title"])])

schema("TreeSchema", [
    ["name", F("String", required=True)],
    ["size", F("Integer", load_default=0)],
    ["children", F("List", inner=F("Nested", nested="TreeSchema"), load_default={"$fn": "new_list"})],
], hooks=[H("post_dump", "total_size")])

schema("ProductSchema", [
    ["sku", F("String", required=True)],
    ["name", F("String", required=True, validate=[V("NoneOf", iterable=["test", "sample"])])],
    ["price", F("Float", required=True, validate=[V("Range", min=0)])],
    ["stock", F("Integer", load_default=0)],
    ["tags", F("List", inner=F("String"), validate=[V("ContainsOnly", choices=["new", "sale", "eco", "limited"])])],
    ["avoid", F("List", inner=F("String"), validate=[V("ContainsNoneOf", iterable=["lead", "bpa"])])],
    ["cents", F("Function", serialize="price_cents", deserialize="to_cents", attribute="price_cents")],
], meta={"many": True, "unknown": "exclude"},
   hooks=[H("validates_schema", "unique_skus", pass_collection=True),
          H("validates_schema", "sale_needs_stock"),
          H("post_dump", "envelope", pass_collection=True)])

schema("ContactSchema", [
    ["email", F("Email")],
    ["homepage", F("Url")],
    ["avatar", F("Url", relative=True)],
    ["mirror", F("Url", schemes=["ftp", "sftp"])],
    ["intranet", F("Url", require_tld=False)],
    ["path", F("Url", relative=True, absolute=False)],
    ["phone", F("String", validate=[V("Regexp", regex="\\+?[0-9 ()-]{7,20}", flags=0)])],
    ["code", F("String", validate=[V("Equal", comparable="XYZ")])],
    ["id", F("UUID")],
    ["kind", F("String", validate=[V("OneOf", choices=["person", "company", 3])])],
])

schema("LegacySchema", [
    ["first", F("String", data_key="firstName", required=True)],
    ["last", F("String", data_key="lastName")],
    ["full", F("Method", serialize="full_name", deserialize="split_name", data_key="fullName")],
    ["born", F("Date")],
    ["shout", F("Function", serialize="upper_first")],
    ["code", F("String", attribute="legacy_code", data_key="CODE", post_load=["upper"])],
    ["tags", F("String", data_key="tagList", post_load=["split_commas"])],
    ["price", F("Float", post_load=["cents"], attribute="price_cents")],
    ["note", F("String", dump_default="(none)")],
], meta={"datetimeformat": "%Y/%m/%d %H:%M:%S", "dateformat": "%Y%m%d"},
   hooks=[H("pre_load", "lower_keys"), H("post_load", "stamp", pass_original=True)])

schema("StrictSchema", [
    ["a", F("Integer")],
    ["b", F("String")],
    ["c", F("Float")],
    ["secret", F("String")],
    ["when", F("DateTime")],
    ["nums", F("List", inner=F("Integer"))],
], meta={"fields": ["a", "b", "c", "secret", "when", "nums"], "exclude": ["c"], "load_only": ["secret"], "index_errors": False,
         "datetimeformat": "%d.%m.%Y"},
   error_messages={"unknown": "Field {0} is not allowed.", "type": "Expected an object."})

schema("EnvelopeSchema", [
    ["id", F("Integer", required=True)],
    ["kind", F("String", load_default="note")],
], hooks=[H("pre_load", "unwrap_many", pass_collection=True), H("pre_load", "unwrap"),
          H("post_load", "number_items", pass_collection=True), H("post_load", "fail_banned")])

# Schemas that cannot be built: the error is the result.
schema("CollidingKeys", [
    ["a", F("String", data_key="x")],
    ["b", F("String", data_key="x")],
])
schema("CollidingAttrs", [
    ["a", F("String", attribute="z")],
    ["b", F("String", attribute="z")],
])
schema("RequiredDefault", [
    ["a", F("String", required=True, load_default="x")],
])
schema("BadPrecision", [
    ["a", F("TimeDelta", precision="fortnights")],
])

DOCS = {}


def doc(name, *values):
    DOCS.setdefault(name, []).extend(values)


# Every document is written with json.dumps, then some raw lines are added
# below for the corners JSON writers don't make.
doc("address",
    {"street": "  1 Main St ", "city": "Springfield", "postcode": "12345"},
    {"street": "9 Elm", "city": "Austin", "postcode": "73301-1234", "country": "us"},
    {"street": "   ", "city": "Paris", "country": "fr", "postcode": "75001"},
    {"city": "Bonn", "country": "Germany", "postcode": "ABCDE"},
    {"street": 12, "city": None, "postcode": "1234", "zip": "1234"},
    ["not", "a", "dict"],
    "just a string",
    {},
    )

doc("users",
    {"username": " Alice_01 ", "email": "alice@example.com", "password": "correct horse", "age": 34,
     "signedUpAt": "2024-03-01T12:30:00+00:00", "address": {"street": "1 Main St", "city": "Springfield"},
     "tags": ["staff", "beta"], "website": "https://alice.example.com/blog"},
    {"username": "bob", "email": "bob@mail.example.org", "age": None, "role": "guest"},
    {"username": "ab", "email": "not-an-email", "age": 12, "role": "owner", "website": "ftp//nowhere"},
    {"username": "Root", "email": "root@localhost", "password": "short", "role": "admin"},
    {"data": {"username": "carol", "email": "carol@example.co.uk", "tags": ["a", "this-tag-is-long", 5]}},
    {"username": "dave", "email": "dave@[192.168.0.1]", "signedUpAt": "yesterday", "address": {"city": "X"}, "extra": 1, "another": True},
    {"username": "eve", "email": "\"eve smith\"@example.com", "age": "41", "website": None, "address": None},
    {"username": "frank", "email": "frank@exa_mple.com", "age": True, "tags": "a,b"},
    {"username": "gina", "email": "gina@münchen.de", "age": 3.9, "website": "http://localhost:8000/x"},
    {"username": "hank", "email": "hank..h@example.com", "age": "1e3", "website": "https://192.168.1.1/admin"},
    {"email": "ivy@example.com"},
    {"username": "jo_jo", "email": "jo@example.com", "age": 4611686018427387904},
    [{"username": "kim", "email": "kim@example.com"}],
    None,
    )

doc("user_lists",
    [{"username": "kim", "email": "kim@example.com"}, {"data": {"username": "lee", "email": "lee@example.com"}}],
    [{"username": "kim", "email": "kim@example"}, "lee", {"username": "x"}],
    [],
    {"username": "kim", "email": "kim@example.com"},
    )

doc("signup",
    {"username": "lena", "email": "lena@example.com", "password": "s3cret-pass", "confirmPassword": "s3cret-pass", "terms": True},
    {"username": "max", "email": "max@example.com", "password": "s3cret-pass", "confirmPassword": "other-pass", "terms": "yes"},
    {"username": "nora", "email": "nora@example.com", "password": "s3cret-pass", "confirmPassword": "s3cret-pass", "terms": False, "role": "admin", "age": 15},
    {"username": "o", "email": "bad", "role": "admin", "age": 14, "terms": "maybe"},
    {"username": "pat", "email": "pat@example.com", "role": "admin", "confirmPassword": "x", "terms": 1},
    )

doc("orders",
    {"id": "12345678-1234-5678-1234-567812345678", "customer": "alice", "placed": "2024-05-01T09:00:00Z",
     "ship_by": "2024-05-03", "watchers": ["bob", "carol"],
     "billing": {"street": "1 Main St", "city": "Springfield", "phone": "555"}, "items": [{"sku": "ABC-1234", "qty": 2, "price": 9.99}, {"sku": "XYZ-0001", "price": 0.5, "gift": "yes"}]},
    {"id": "{12345678-1234-5678-1234-567812345679}", "customer": "bob", "placed": "2024-05-01T09:00:00+02:00", "ship_by": "2024-04-30",
     "status": "PAID", "items": [{"sku": "ABC-1234", "price": 20}], "coupon": "TEST", "watchers": "bob", "billing": {"city": "Rome"}},
    {"id": "urn:uuid:12345678123456781234567812345670", "placed": "2024-05-01", "items": [], "status": "paid", "watchers": [5, "ok", "a"]},
    {"id": "not-a-uuid", "placed": "2024-13-01T00:00:00", "items": [{"sku": "abc-12", "qty": "2", "price": -1}, {"qty": 0, "price": "free"}, "x"]},
    {"id": "1234567812345678123456781234567", "placed": 20240501, "items": {"sku": "ABC-1234"}, "status": "LOST", "notes": None},
    {"id": "0x345678123456781234567812345678", "placed": "2024-05-01T09:00:00.250Z", "items": [{"sku": "ABC-1234", "qty": 100, "price": 1}] * 6, "ship_by": "2024-W18-5"},
    {"id": 1234, "items": [{"sku": "ABC-1234", "qty": 1.0, "price": 1e400}], "customer": 5, "placed": None},
    {"id": "  12345678-1234-5678-1234-56781234567a  ", "placed": "2024-05-01T09:00:00", "items": [{"sku": "ZZZ-9999", "price": 3}]},
    )

doc("events",
    {"name": "launch", "starts": "2024-06-01T10:00:00", "ends": "2024-06-01T12:00:00+02:00", "local": "2024-06-01T10:00:00+05:30",
     "alarm": "09:45", "day": "2024-06-01", "length": 90, "timeout": "2500", "every": 1.5, "level": 30},
    {"name": "standup", "starts": "2024-06-03T09:00:00-04:00", "ends": "2024-06-03T08:00:00-04:00", "alarm": "09:00:00.5", "length": "15.5", "level": "40"},
    {"name": "bad", "starts": "soon", "ends": "2024-06-03T08:00:00", "local": "2024-06-03 08:00", "alarm": "25:00", "day": "2024/06/03",
     "length": "ten", "timeout": True, "every": [1], "level": 50},
    {"name": "edge", "starts": "2024-02-29T23:59:59.999999+14:00", "alarm": "23:59:59.123456+01:00", "day": "20240229", "length": -30,
     "timeout": 0.0004, "every": "0.25", "level": "DEBUG"},
    {"name": "far", "starts": "9999-12-31T23:59:59Z", "length": 1e20, "level": 10.0},
    {"starts": "2024-06-01T10:00:00Z", "local": "2024-06-01T10:00:00", "ends": "2024-06-01T09:00:00Z", "level": None},
    )

doc("metrics",
    {"name": "http.requests", "value": 12.5, "count": 7, "ratio": 0.25, "ts": 1717236000, "ts_ms": 1717236000123,
     "labels": {"method": "get", "path_group": "api"}, "enabled": "on", "flags": {"cache": "enabled", "trace": "off"}, "host": {"a": [1, 2.5, None]}, "buckets": {"10": 3, "20": 5, "30": 9}},
    {"name": "Disk.Free", "value": "nan", "count": "12", "ratio": "1.5", "ts": "1717236000.5", "ts_ms": -5, "enabled": "maybe",
     "labels": {"Bad-Key": "x", "ok": "a value that is long"}, "flags": {"cache": True}},
    {"name": "cpu", "value": "inf", "count": 3.7, "ratio": 1, "ts": -1, "ts_ms": "abc", "enabled": 1, "labels": [], "flags": {"x": "yes"}},
    {"name": "mem", "value": "  -1.5e3  ", "count": " 42 ", "ts": 0.0000015, "ts_ms": 1.5, "enabled": "F", "labels": {"zone": 5}, "buckets": {"010": 1, " 10 ": 2, "1_0": 3, "+inf": 4}},
    {"name": "net", "value": "1_000.5", "count": "1_000", "ts": True, "enabled": 0, "ratio": "0.333333333333333314829616256247390992939472198486328125"},
    {"name": "x", "value": ".5", "count": "-0", "ts": 253402300800, "enabled": [True], "host": "db-1"},
    )

doc("configs",
    {"host": "api.internal", "port": 443, "debug": "true", "servers": [["a.internal", 8000], ["b.internal", "8001"]],
     "limits": {"cpu": 2, "mem": 512}, "retry": {"times": 5}, "root_dir": "/srv/app", "log_dir": "/var/log/app", "workers": 4, "region": "eu-west-1", "replicas": 3},
    {"port": 0, "mode": "dev", "servers": [["c", 1, 2], ["d"], "e", ["f", -1]], "limits": {"gpu": 1, "cpu": -1}, "retry": {"times": 11, "backoff": "x"}, "workers": 3},
    {"port": 70000, "debug": "maybe", "servers": "none", "limits": [], "retry": [], "root_dir": None, "mode": None},
    {},
    {"root_dir": "/a", "workers": "6", "port": "8443", "retry": {"backoff": 2, "jitter": True}},
    )

doc("articles",
    {"title": "Hello world", "body": "First post here.", "author": {"username": "alice", "email": "alice@example.com"}, "coauthors": [{"username": "bob"}, {"username": "carol"}],
     "published": "02/01/2024", "updated": "2024-01-02 03:04", "category": 2, "visibility": "public",
     "comments": [{"id": 1, "text": "Nice!", "author": "bob", "replies": [{"text": "Thanks", "author": "alice"}]}], "extra": {"pinned": True}},
    {"title": "Hi", "author": {"username": "x", "email": "y", "password": "z"}, "coauthors": {"username": "bob"}, "published": "2024-01-02", "updated": "2024-01-02T03:04",
     "category": 9, "visibility": 0, "comments": [{"text": "   ", "author": "bo"}, {"id": "two", "text": "ok", "author": "carl", "replies": [{"id": 3, "text": "x"}]}]},
    {"title": "Banned words here", "author": {"username": "dana", "email": "dana@example.com"}, "published": "31/02/2024", "category": "2", "visibility": "secret"},
    {"title": "Unicode — café ünïcode", "author": {"username": "émile", "email": "emile@example.fr"}, "category": 1.0, "visibility": False,
     "comments": [{"text": "a" * 41, "author": "fred"}], "slug": "ignored", "words": 3},
    {"title": "Done", "author": "alice", "comments": {"text": "x"}, "coauthors": [{"username": "bob", "email": "b@example.com"}, "carol"]},
    )

doc("trees",
    {"name": "root", "size": 1, "children": [{"name": "a", "size": 2, "children": [{"name": "a1", "size": 3}]}, {"name": "b"}]},
    {"name": "solo"},
    {"name": "bad", "children": [{"size": "big"}, {"name": "ok", "children": [{"name": 5}]}]},
    )

doc("products",
    [{"sku": "P-1", "name": "Kettle", "price": 25.0, "stock": 3, "tags": ["new", "eco"], "cents": 2500},
     {"sku": "P-2", "name": "Mug", "price": 7.5, "tags": ["sale"], "cents": "750", "color": "red"}],
    [{"sku": "P-1", "name": "test", "price": -1, "tags": ["new", "hot"], "avoid": ["lead"]},
     {"sku": "P-1", "name": "Spoon", "price": 1, "stock": 0, "tags": ["sale"]}],
    [],
    {"sku": "P-9"},
    [{"sku": "P-3", "name": "Bowl", "price": 12, "cents": "x"}, "nope", None],
    )

doc("contacts",
    {"email": "a.b+tag@sub.example.com", "homepage": "https://example.com", "avatar": "/img/me.png", "mirror": "ftp://files.example.com/pub",
     "intranet": "http://wiki/", "path": "/docs/index.html", "phone": "+1 (555) 123-4567", "code": "XYZ", "id": "12345678123456781234567812345678", "kind": "person"},
    {"email": "@example.com", "homepage": "example.com", "avatar": "img me.png", "mirror": "http://files.example.com", "intranet": "http://wiki",
     "path": "https://example.com/docs", "phone": "123", "code": "xyz", "id": "12345678-1234-5678-1234-56781234567", "kind": "robot"},
    {"email": "user@sub.-bad.com", "homepage": "HTTPS://EXAMPLE.COM:8080/a?b=c#d", "avatar": "https://cdn.example.com/a.png", "mirror": "sftp://host.example.org",
     "intranet": "https://localhost", "path": "?q=1", "phone": "555 1234 ext", "kind": 3},
    {"email": "x@y.z", "homepage": "http://user:pass@example.com/", "avatar": "", "mirror": "ftp://[::1]/x", "intranet": "http://10.0.0.1:99999/",
     "path": "", "kind": 3.0},
    {"email": "first.last@x.example", "homepage": "file:///etc/passwd", "avatar": "#frag", "intranet": "http://my-host/a b", "kind": True},
    {"email": "üser@example.com", "homepage": "http://xn--mnchen-3ya.de/", "avatar": "//cdn.example.com/x.png", "intranet": "http://a.b.c.d.e/",
     "phone": "+44 20 7946 0958 999 999 99", "kind": None},
    )

doc("legacy",
    {"FirstName": "Ada", "LastName": "Lovelace", "fullName": "Ada King Lovelace", "born": "18151210", "CODE": "ab-1", "tagList": "math, poetry ,engines", "price": 19.99},
    {"firstname": "Alan", "fullname": "Turing", "price": "4.125", "code": "x"},
    {"lastName": "Hopper", "born": "1906-12-09", "price": True},
    )

doc("strict",
    {"a": 1, "b": "x", "secret": "s", "when": "01.02.2024"},
    {"a": "x", "c": 1.5, "d": 4, "when": "2024-02-01", "nums": [1, "two", 3, "four"]},
    "scalar",
    )

doc("envelopes",
    {"data": {"id": 1}},
    {"id": 2, "kind": "banned"},
    {"data": [{"id": 3}, {"id": 4, "kind": "task"}]},
    [{"id": 5}, {"data": {"id": 6}}, {"kind": "x"}],
    {"items": [{"id": 7}, {"id": 8, "kind": "banned"}]},
    )

RAW = {
    "metrics": [
        '{"name": "nan.ok", "value": NaN, "count": Infinity}',
        '{"name": "inf", "value": -Infinity, "ratio": NaN}',
    ],
    "users": [
        '{"username": "ünï", "email": "u@example.com"}',
        '{"username": "dup", "username": "dupe2", "email": "d@example.com"}',
    ],
}

JOBS = []


def job(*cols):
    JOBS.append("\t".join(cols))


def J(o):
    return json.dumps(o, separators=(",", ":"))


def title(t):
    JOBS.append("== " + t)


title("address book entries")
job("load", "AddressSchema", "{}", "{}", "address")
title("addresses loaded partially")
job("load", "AddressSchema", "{}", J({"partial": True}), "address")
title("addresses, street and city optional")
job("load", "AddressSchema", J({"partial": ["street"]}), J({"partial": ["city"]}), "address")
title("addresses, validate only")
job("validate", "AddressSchema", "{}", "{}", "address")
title("user accounts")
job("load", "UserSchema", "{}", "{}", "users")
title("user accounts, unknown fields excluded")
job("load", "UserSchema", J({"unknown": "exclude"}), "{}", "users")
title("user accounts, unknown fields kept")
job("load", "UserSchema", "{}", J({"unknown": "include"}), "users")
title("user accounts as a list")
job("load", "UserSchema", J({"many": True}), "{}", "user_lists")
title("user profiles, dumped")
job("dump", "UserSchema", "{}", "{}", "UserSchema", J({"unknown": "exclude"}), "users")
title("user profiles, only some fields")
job("dump", "UserSchema", J({"only": ["username", "address.city", "address.country", "tags"]}), "{}", "UserSchema", J({"unknown": "exclude"}), "users")
title("user profiles without the address street")
job("roundtrip", "UserSchema", J({"exclude": ["address.street", "signup"], "unknown": "exclude"}), "{}", "users")
title("user profiles, address fields load-only")
job("roundtrip", "UserSchema", J({"load_only": ["address.postcode", "age"], "dump_only": ["role"], "unknown": "exclude"}), "{}", "users")
title("signups")
job("load", "SignupSchema", "{}", "{}", "signup")
title("signups, fields")
job("init", "SignupSchema", "{}")
title("orders")
job("load", "OrderSchema", "{}", "{}", "orders")
title("orders, items partial")
job("load", "OrderSchema", J({"partial": ["items.price", "placed"]}), "{}", "orders")
title("order confirmations")
job("dump", "OrderSchema", "{}", "{}", "OrderSchema", J({"partial": True}), "orders")
title("events")
job("roundtrip", "EventSchema", "{}", "{}", "events")
title("metrics")
job("roundtrip", "MetricSchema", "{}", "{}", "metrics")
title("service configs")
job("roundtrip", "ConfigSchema", "{}", "{}", "configs")
title("service configs, unknown raises")
job("load", "ConfigSchema", J({"unknown": "raise"}), "{}", "configs")
title("articles")
job("roundtrip", "ArticleSchema", "{}", "{}", "articles")
title("articles, comment text only")
job("dump", "ArticleSchema", J({"only": ["title", "comments.text", "comments.replies", "author"], "exclude": ["comments.replies"]}), "{}",
    "ArticleSchema", J({"unknown": "exclude"}), "articles")
title("trees")
job("roundtrip", "TreeSchema", "{}", "{}", "trees")
title("product feeds")
job("roundtrip", "ProductSchema", "{}", "{}", "products")
title("product feeds, one at a time")
job("load", "ProductSchema", J({"many": False}), "{}", "products")
title("contacts")
job("roundtrip", "ContactSchema", "{}", "{}", "contacts")
title("legacy records")
job("roundtrip", "LegacySchema", "{}", "{}", "legacy")
title("strict records")
job("roundtrip", "StrictSchema", "{}", "{}", "strict")
title("strict records, fields")
job("init", "StrictSchema", "{}")
job("init", "StrictSchema", J({"only": ["a", "z"]}))
job("init", "StrictSchema", J({"exclude": ["b", "q"]}))
job("init", "StrictSchema", J({"only": ["b", "a", "c"]}))
title("envelopes")
job("load", "EnvelopeSchema", "{}", "{}", "envelopes")
job("load", "EnvelopeSchema", "{}", J({"many": True}), "envelopes")
title("schemas that cannot be built")
job("init", "CollidingKeys", "{}")
job("init", "CollidingAttrs", "{}")
job("init", "RequiredDefault", "{}")
job("init", "BadPrecision", "{}")
job("init", "UserSchema", J({"only": ["username", "address.city"], "exclude": ["email"]}))
job("init", "OrderSchema", J({"exclude": ["items.qty"], "dump_only": ["id"]}))


def main():
    os.makedirs(os.path.join(DATA, "docs"), exist_ok=True)
    with open(os.path.join(DATA, "schemas.json"), "w", encoding="utf-8") as f:
        json.dump({"enums": ENUMS, "schemas": SCHEMAS}, f, indent=1, ensure_ascii=False)
        f.write("\n")
    for name, values in DOCS.items():
        lines = [json.dumps(v, ensure_ascii=False) for v in values]
        lines += RAW.get(name, [])
        with open(os.path.join(DATA, "docs", name + ".jsonl"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    with open(os.path.join(DATA, "jobs.tsv"), "w", encoding="utf-8") as f:
        f.write("\n".join(JOBS) + "\n")


main()
