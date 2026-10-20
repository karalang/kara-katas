# Writes data/: validation schemas (JSON) and the documents to check
# against them (JSON Lines), for the places an application validates
# input with Cerberus: an API's signup payload, a service's config file,
# shop orders, deployment manifests, sensor readings, CSV rows coerced to
# types, blog posts with default setters, registry-backed schemas, and
# broken schemas. data/jobs.tsv lists the jobs mini_cerberus.kara and
# oracle.py run.
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def write(rel, text):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def schema(name, s):
    write("schemas/%s.json" % name, json.dumps(s, indent=2, ensure_ascii=False) + "\n")
    return "schemas/%s.json" % name


def docs(name, ds):
    write("docs/%s.jsonl" % name, "".join(json.dumps(d, ensure_ascii=False) + "\n" for d in ds))
    return "docs/%s.jsonl" % name


SIGNUP = {
    "username": {"type": "string", "required": True, "minlength": 3, "maxlength": 16,
                 "regex": "[a-z][a-z0-9_]*"},
    "email": {"type": "string", "required": True, "regex": "[^@ ]+@[^@ ]+\\.[a-z]{2,}"},
    "password": {"type": "string", "required": True, "minlength": 8},
    "age": {"type": "integer", "min": 13, "max": 130},
    "role": {"type": "string", "allowed": ["user", "admin", "editor"], "default": "user"},
    "tags": {"type": "list", "schema": {"type": "string", "maxlength": 10}, "maxlength": 3},
    "newsletter": {"type": "boolean"},
    "referrer": {"type": "string", "nullable": True, "empty": False},
}

SIGNUP_DOCS = [
    {"username": "ada", "email": "ada@example.org", "password": "correct horse"},
    {"username": "Ada", "email": "ada@example", "password": "short"},
    {"username": "grace_h", "email": "grace@navy.mil", "password": "cobol1959", "age": 12,
     "role": "superuser", "newsletter": "yes"},
    {"email": "x@y.io", "password": "12345678", "admin": True},
    {"username": "linus", "email": "linus@kernel.org", "password": "penguins!",
     "tags": ["kernel", "git", "a-very-long-tag", 7], "age": 54.5},
    {"username": "ken", "email": "ken@bell-labs.com", "password": "unix-1969", "referrer": None,
     "tags": []},
    {"username": "dmr", "email": "dmr@bell-labs.com", "password": "c-is-fun!", "referrer": "",
     "age": True, "role": None},
    {"username": "x" * 20, "email": "a b@c.de", "password": 12345678, "tags": "solo"},
    {"username": "bjarne", "email": "bs@cpp.org", "password": "templates", "tags": ["a", "b", "c", "d"]},
    {},
]

CONFIG = {
    "service": {"type": "string", "required": True, "empty": False},
    "port": {"type": "integer", "coerce": "int", "min": 1, "max": 65535, "check_with": "port"},
    "debug": {"type": "boolean", "coerce": "yesno", "default": False},
    "database": {
        "type": "dict",
        "required": True,
        "schema": {
            "host": {"type": "string", "required": True},
            "port": {"type": "integer", "coerce": "int", "default": 5432},
            "name": {"type": "string", "regex": "[a-z_]+"},
            "pool": {"type": "dict", "schema": {
                "min": {"type": "integer", "min": 0},
                "max": {"type": "integer", "min": 1, "max": 100},
            }},
        },
    },
    "log_level": {"type": "string", "coerce": "lower", "allowed": ["debug", "info", "warning", "error"],
                  "default": "info"},
    "features": {"type": "dict", "keysrules": {"type": "string", "regex": "[a-z][a-z0-9_]*"},
                 "valuesrules": {"type": "boolean", "coerce": "yesno"}},
    "workers": {"type": "integer", "check_with": "even"},
    "allowed_hosts": {"type": "list", "coerce": "split", "schema": {"type": "string", "empty": False}},
}

CONFIG_DOCS = [
    {"service": "billing", "port": "8080", "database": {"host": "db.internal", "name": "billing"}},
    {"service": "auth", "port": 443, "debug": "YES", "log_level": "WARNING",
     "database": {"host": "auth-db", "port": "6432", "pool": {"min": 2, "max": 20}},
     "features": {"sso": "yes", "mfa": "no", "beta_ui": True}},
    {"service": "", "port": "eighty", "database": {"port": "x"}, "log_level": "verbose"},
    {"service": "edge", "port": 22, "workers": 3, "database": "postgres://edge",
     "features": {"Legacy-Mode": True, "fast": "sometimes"}},
    {"service": "cron", "port": 70000, "workers": 8, "database": {"host": "db", "pool": {"min": -1, "max": 500}},
     "allowed_hosts": "a.example.com, b.example.com,,c.example.com"},
    {"service": "api", "debug": 7, "database": {"host": "db", "name": "API", "replica": "db2"},
     "allowed_hosts": ["x.io"], "extra": {"k": 1}},
    {"port": None, "database": None, "features": None},
]

ORDER = {
    "id": {"type": "string", "readonly": True},
    "customer": {"type": "dict", "required": True, "schema": "customer"},
    "items": {
        "type": "list", "required": True, "minlength": 1,
        "schema": {"type": "dict", "schema": {
            "sku": {"type": "string", "required": True, "regex": "[A-Z]{3}-[0-9]{4}"},
            "qty": {"type": "integer", "required": True, "min": 1},
            "price": {"type": "number", "min": 0},
        }},
    },
    "currency": {"type": "string", "allowed": ["EUR", "USD", "GBP", "INR"], "required": True},
    "coupon": {"type": "string", "excludes": "discount"},
    "discount": {"type": "float", "min": 0, "max": 0.5, "excludes": "coupon"},
    "shipping": {"type": "string", "allowed": ["standard", "express", "pickup"]},
    "address": {"type": "dict", "schema": "address", "dependencies": {"shipping": ["standard", "express"]}},
    "store": {"type": "string", "dependencies": {"shipping": "pickup"}},
    "gift_note": {"type": "string", "dependencies": ["gift_wrap"], "maxlength": 40},
    "gift_wrap": {"type": "boolean"},
    "card": {"type": "string", "check_with": "luhn"},
}

ORDER_DOCS = [
    {"customer": {"name": "Ana", "email": "ana@shop.example"},
     "items": [{"sku": "ABC-1234", "qty": 2, "price": 9.99}], "currency": "EUR",
     "shipping": "standard", "address": {"street": "Rua Augusta 1", "city": "Lisboa", "zip": "1100-048"},
     "card": "4539 1488 0343 6467"},
    {"id": "ord_1", "customer": {"name": "Bo"}, "items": [], "currency": "SEK"},
    {"customer": {"name": "Cy", "email": "cy@x.y"}, "currency": "USD",
     "items": [{"sku": "abc-1", "qty": 0}, {"qty": 1, "price": -3}, "XYZ-0001"],
     "coupon": "SPRING", "discount": 0.25},
    {"customer": {"name": "Di"}, "items": [{"sku": "DEF-5678", "qty": 1}], "currency": "GBP",
     "shipping": "pickup", "address": {"street": "1 High St", "city": "Leeds"}, "store": "LDS-01",
     "gift_note": "Happy birthday!", "card": "4539 1488 0343 6468"},
    {"customer": {"name": "Ed", "email": "ed@x.y", "vip": True}, "items": [{"sku": "GHI-0000", "qty": 3}],
     "currency": "INR", "store": "BLR", "gift_note": "For you", "gift_wrap": True, "discount": 0.75},
    {"customer": "Fay", "items": {"sku": "JKL-1111"}, "currency": "EUR", "address": {"city": "Paris"}},
]

ADDRESS = {
    "street": {"type": "string", "required": True},
    "city": {"type": "string", "required": True},
    "zip": {"type": "string", "regex": "[0-9]{4,5}(-[0-9]{3,4})?"},
    "country": {"type": "string", "minlength": 2, "maxlength": 2, "default": "PT"},
}

CUSTOMER = {
    "name": {"type": "string", "required": True},
    "email": {"type": "string", "required": True, "regex": "[^@]+@[^@]+"},
}

MANIFEST = {
    "apiVersion": {"type": "string", "allowed": ["apps/v1"], "required": True},
    "kind": {"type": "string", "allowed": ["Deployment", "StatefulSet", "DaemonSet"], "required": True},
    "metadata": {"type": "dict", "required": True, "schema": {
        "name": {"type": "string", "required": True, "regex": "[a-z0-9]([-a-z0-9]*[a-z0-9])?", "maxlength": 63},
        "labels": {"type": "dict", "keysrules": {"type": "string", "regex": "([a-z0-9.-]+/)?[a-zA-Z0-9_.-]+"},
                   "valuesrules": {"type": "string", "maxlength": 63}},
    }},
    "spec": {"type": "dict", "required": True, "schema": {
        "replicas": {"type": "integer", "min": 0, "excludes": "autoscale"},
        "autoscale": {"type": "dict", "schema": {
            "min": {"type": "integer", "min": 1},
            "max": {"type": "integer", "min": 1},
        }},
        "containers": {"type": "list", "required": True, "minlength": 1, "schema": {
            "type": "dict", "schema": {
                "name": {"type": "string", "required": True},
                "image": {"type": "string", "required": True, "regex": "[a-z0-9./-]+(:[A-Za-z0-9._-]+)?"},
                "ports": {"type": "list", "schema": {"type": "dict", "schema": {
                    "containerPort": {"anyof": [{"type": "integer", "min": 1, "max": 65535},
                                                {"type": "string", "regex": "[a-z][a-z0-9-]{0,14}"}]},
                    "protocol": {"type": "string", "allowed": ["TCP", "UDP", "SCTP"], "default": "TCP"},
                }}},
                "resources": {"type": "dict", "schema": {
                    "limits": {"type": "dict", "valuesrules": {"oneof": [
                        {"type": "integer", "min": 0},
                        {"type": "string", "regex": "[0-9]+(m|Mi|Gi)"}]}},
                }},
                "env": {"type": "list", "schema": {"type": "dict", "schema": {
                    "name": {"type": "string", "required": True, "regex": "[A-Z_][A-Z0-9_]*"},
                    "value": {"type": "string", "excludes": "valueFrom"},
                    "valueFrom": {"type": "dict", "excludes": "value"},
                }}},
                "args": {"type": "list", "items": [{"type": "string"}, {"type": "string"}]},
            }}},
    }},
}

MANIFEST_DOCS = [
    {"apiVersion": "apps/v1", "kind": "Deployment",
     "metadata": {"name": "web", "labels": {"app": "web", "tier": "frontend"}},
     "spec": {"replicas": 3, "containers": [{"name": "nginx", "image": "nginx:1.25",
                                             "ports": [{"containerPort": 80}, {"containerPort": "metrics"}],
                                             "resources": {"limits": {"cpu": "500m", "memory": "128Mi"}}}]}},
    {"apiVersion": "v1", "kind": "Pod", "metadata": {"name": "Web_App"},
     "spec": {"containers": []}},
    {"apiVersion": "apps/v1", "kind": "StatefulSet",
     "metadata": {"name": "db", "labels": {"app.kubernetes.io/name": "postgres", "Bad Key": "x"}},
     "spec": {"replicas": 1, "autoscale": {"min": 1, "max": 3},
              "containers": [{"name": "pg", "image": "Postgres:16",
                              "ports": [{"containerPort": 70000}, {"containerPort": "Postgres-Port-Number"},
                                        {"containerPort": 5432, "protocol": "HTTP"}],
                              "resources": {"limits": {"cpu": -1, "memory": "1GB", "pods": 4}},
                              "env": [{"name": "PGDATA", "value": "/data"},
                                      {"name": "lower", "value": "x", "valueFrom": {"secret": "s"}}],
                              "args": ["-c", "max_connections=100", "extra"]}]}},
    {"apiVersion": "apps/v1", "kind": "DaemonSet", "metadata": {"name": "agent"},
     "spec": {"containers": [{"name": "agent", "image": "registry.example.com/agent:v2",
                              "ports": [{"containerPort": True}, {"containerPort": 9100.5}],
                              "args": ["--port", 9100]}]}},
]

SENSOR = {
    "id": {"type": "string", "readonly": True},
    "sensor": {"type": "string", "required": True, "coerce": ["strip", "lower"], "rename": "device"},
    "device": {"type": "string"},
    "temp": {"type": "float", "nullable": True, "min": -40, "max": 85, "coerce": "float"},
    "humidity": {"type": "number", "min": 0, "max": 100, "nullable": True},
    "status": {"type": "string", "allowed": ["ok", "degraded", "offline"], "default": "ok"},
    "readings": {"type": "list", "schema": {"type": "number"}, "check_with": "sorted"},
    "at": {"type": "date", "coerce": "date"},
    "units": {"type": "dict", "default": {}, "purge_unknown": True, "schema": {
        "temp": {"type": "string", "allowed": ["C", "F"]}}},
}

SENSOR_DOCS = [
    {"sensor": "  Kitchen-01 ", "temp": "21.5", "humidity": 40, "at": "2024-03-01", "readings": [1, 2, 3.5]},
    {"sensor": "garage", "temp": None, "humidity": None, "status": None, "at": "2024-02-30"},
    {"sensor": 17, "temp": "hot", "at": "yesterday", "readings": [3, 1, 2]},
    {"id": "s-9", "sensor": "Attic", "temp": 99, "humidity": 120, "units": {"temp": "K", "pressure": "hPa"},
     "battery": 3.1},
    {"sensor": "Porch", "temp": -41.0, "at": "2024-1-2-3", "units": {"temp": "F"}},
    {"device": "Shed", "at": "2024-13-01"},
]

CSV_ROW = {
    "sku": {"type": "string", "required": True, "coerce": "strip", "regex": "[A-Z]{3}-[0-9]{4}"},
    "name": {"type": "string", "required": True, "coerce": "strip", "empty": False},
    "price": {"type": "float", "coerce": "float", "min": 0},
    "stock": {"type": "integer", "coerce": "int", "min": 0},
    "active": {"type": "boolean", "coerce": "yesno"},
    "category": {"type": "string", "coerce": ["strip", "snake"],
                 "allowed": ["kitchen", "garden_tools", "home_office", "outdoor_living"]},
    "launched": {"type": "date", "coerce": "date", "nullable": True},
}

CSV_DOCS = [
    {"sku": "KIT-0001", "name": "Chef's knife", "price": "49.90", "stock": "12", "active": "yes",
     "category": "Kitchen", "launched": "2021-09-14"},
    {"sku": " GAR-0042 ", "name": "Rake", "price": "1e2", "stock": "-3", "active": "Y",
     "category": "GardenTools", "launched": "2022-04-01"},
    {"sku": "OFF-12", "name": "   ", "price": "free", "stock": "3.5", "active": "maybe",
     "category": "Home Office"},
    {"sku": "OUT-7777", "name": "Hammock", "price": "-1", "stock": "", "active": "0",
     "category": "outdoor-living", "launched": "2023-02-29"},
    {"sku": "KIT-0002", "name": "Pan", "price": "inf", "stock": "007", "active": "TRUE",
     "category": "Bathroom", "launched": None},
    {"sku": "KIT-0003", "name": "Lid", "price": None, "stock": None, "active": None},
]

POST = {
    "title": {"type": "string", "required": True},
    "slug": {"type": "string", "default_setter": "slug", "regex": "[a-z0-9-]+"},
    "author": {"type": "string", "default_setter": "author"},
    "owner": {"type": "string", "default_setter": "owner"},
    "items": {"type": "list"},
    "count": {"type": "integer", "default_setter": "count"},
    "views": {"type": "integer", "default": 0, "readonly": True},
    "draft": {"type": "boolean", "default": True},
    "lang": {"type": "string", "rename_handler": "lower"},
    "Body": {"type": "string", "rename_handler": "snake"},
    "body": {"type": "string", "minlength": 1},
}

POST_DOCS = [
    {"title": "Hello World", "author": "ada", "items": [1, 2]},
    {"title": "Second Post", "owner": "grace@example.com"},
    {"title": "No Author"},
    {"slug": "custom", "author": "ken", "views": 5},
    {"title": "Shouting", "author": "linus", "Body": "TEXT", "items": None},
]

TAGS = {
    "tags": {"type": "list", "contains": "release", "forbidden": ["wip"]},
    "level": {"type": "integer", "forbidden": [0, 13], "allowed": [1, 2, 3, 5, 8, 13, 21]},
    "codes": {"type": "list", "contains": [1, 2, 3], "forbidden": [4, 5]},
    "flags": {"type": "dict", "allowed": ["a", "b"]},
    "pair": {"type": "list", "items": [{"type": "string"}, {"type": "integer", "min": 0}]},
    "score": {"noneof": [{"type": "integer", "min": 90}, {"type": "string"}]},
    "ratio": {"allof": [{"type": "float"}, {"min": 0}, {"max": 1}]},
    "id": {"oneof": [{"type": "integer"}, {"type": "string", "regex": "[0-9]+"}]},
    "name": {"anyof_type": ["string", "integer"], "anyof_regex": ["[A-Z].*", "[0-9]+"]},
}

TAGS_DOCS = [
    {"tags": ["release", "v2"], "level": 8, "codes": [1, 2, 3, 6], "flags": {"a": 1}, "pair": ["x", 1],
     "score": 50, "ratio": 0.5, "id": 7, "name": "Alice"},
    {"tags": ["wip", "docs"], "level": 13, "codes": [5, 4, 2], "flags": {"a": 1, "c": 2, "d": 3},
     "pair": ["x"], "score": 95, "ratio": 1.5, "id": "42", "name": "alice"},
    {"tags": [], "level": 0, "codes": [], "pair": [1, -1], "score": "high", "ratio": "half", "id": "x1",
     "name": 7},
    {"level": 4, "codes": [1, 2, 3], "pair": ["a", 1, 2], "id": True, "name": None, "ratio": 0},
]

ANYOF_CORNER = {
    "contact": {"type": "dict", "anyof": [
        {"schema": {"email": {"type": "string", "required": True}}},
        {"schema": {"phone": {"type": "string", "required": True, "regex": "\\+[0-9]{7,15}"}}},
    ]},
    "price": {"anyof": [{"type": "integer", "min": 0}, {"type": "float", "min": 0.0, "max": 1.0}],
              "nullable": True},
    "ids": {"type": "list", "schema": {"oneof": [{"type": "integer", "min": 1}, {"type": "string", "minlength": 3}]}},
}

ANYOF_DOCS = [
    {"contact": {"email": "a@b.c"}, "price": 3, "ids": [1, "abc"]},
    {"contact": {"phone": "+351912345678", "email": "x@y.z"}, "price": 0.5, "ids": [0, "ab", 2.5]},
    {"contact": {"phone": "12345"}, "price": -1.5, "ids": []},
    {"contact": {}, "price": None, "ids": ["abcd", -2]},
]

PRODUCT_REG = {
    "name": {"type": "string", "required": True},
    "price": "money",
    "weight": "positive",
    "dims": {"type": "list", "schema": "positive"},
    "ships_to": {"type": "list", "schema": {"type": "dict", "schema": "address"}},
}

PRODUCT_REG_DOCS = [
    {"name": "Desk", "price": 199.0, "weight": 30, "dims": [120, 60, 75],
     "ships_to": [{"street": "Main St 1", "city": "Porto"}]},
    {"name": "Lamp", "price": -5, "weight": 0, "dims": [10, -1], "ships_to": [{"city": "Faro", "zip": "80"}]},
]

MONEY = {"type": "number", "min": 0, "required": True}
POSITIVE = {"type": "number", "min": 0, "forbidden": [0]}

STRICT = {
    "host": {"type": "string"},
    "port": {"type": "integer"},
    "tls": {"type": "dict", "schema": {"cert": {"type": "string"}, "key": {"type": "string"}}},
}

STRICT_DOCS = [
    {"host": "a", "port": 1, "tls": {"cert": "c"}},
    {"host": "a"},
    {"port": "x", "extra": 1, "tls": {"cert": 1, "ca": "y"}},
    {"host": None, "port": None},
]

UNKNOWN_RULES = {"type": "string", "maxlength": 5}

BROKEN = [
    {"name": {"type": "strin"}},
    {"name": {"typ": "string"}},
    {"age": {"type": "integer", "min": "zero", "max": 10}},
    {"age": "integer"},
    {"tags": {"type": "list", "schema": {"type": "string", "minlength": "3"}}},
    {"tags": {"type": "list", "schema": {"tpye": "string"}}},
    {"role": {"allowed": "admin"}},
    {"role": {"required": "yes", "nullable": 1}},
    {"x": {"coerce": "to_upper"}},
    {"x": {"check_with": "odd"}},
    {"x": {"default_setter": "nowhere"}},
    {"x": {"anyof": {"type": "string"}}},
    {"x": {"anyof": [{"type": "string"}, {"typo": 1}]}},
    {"x": {"oneof_type": ["string", "nope"]}},
    {"x": {"regex": 5}},
    {"x": {"items": [{"type": "string"}, {"tpe": "int"}]}},
    {"x": {"dependencies": 5}},
    {"x": {"dependencies": {"y": 5}}},
    {"x": {"excludes": ["a", {"b": 1}]}},
    {"x": {"keysrules": {"type": "string", "rename": "y"}}},
    {"x": {"valuesrules": {"type": "bogus"}}},
    {"x": {"schema": "no_such_schema"}},
    {"x": "no_such_rules"},
    {"x": {"type": "dict", "schema": {"y": {"type": "dict", "schema": {"z": {"maxlength": -1, "regexx": "a"}}}}}},
    {"x": {"type": ["string", "integer", "colour"]}},
    {"x": {"empty": "no", "readonly": "no", "purge_unknown": 1}},
    {"x": {"min": 1, "max": 2, "meta": {"anything": [1, 2]}}},
    {"x": {"minlength": 1.5, "contains": []}},
    {"x": {"allow_unknown": {"type": "nonsense"}, "type": "dict"}},
    {"x": {"rename": ["not", "hashable"]}},
]


def main():
    if os.path.isdir(DATA):
        shutil.rmtree(DATA)
    jobs = []

    def job(*fields):
        jobs.append(list(fields))

    sg = schema("signup", SIGNUP)
    sd = docs("signup", SIGNUP_DOCS)
    job("validate", sg, sd)
    job("validated", sg, sd)
    job("validate", sg, sd, "update")
    job("validate", sg, sd, "allow_unknown", "require_all")

    cf = schema("config", CONFIG)
    cd = docs("config", CONFIG_DOCS)
    job("validate", cf, cd)
    job("normalized", cf, cd)
    job("validate", cf, cd, "no_normalize")
    job("validate", cf, cd, "ignore_none_values", "purge_unknown")

    job("schema_registry", "address", schema("address", ADDRESS))
    job("schema_registry", "customer", schema("customer", CUSTOMER))
    od = docs("orders", ORDER_DOCS)
    og = schema("order", ORDER)
    job("validate", og, od)
    job("validate", og, od, "purge_readonly", "allow_unknown")

    mf = schema("manifest", MANIFEST)
    md = docs("manifests", MANIFEST_DOCS)
    job("validate", mf, md)

    ss = schema("sensor", SENSOR)
    sdd = docs("sensors", SENSOR_DOCS)
    job("validate", ss, sdd)
    job("normalized", ss, sdd)
    job("validated", ss, sdd, "purge_unknown")
    job("validate", ss, sdd, "purge_readonly", "no_normalize")

    cs = schema("csv_row", CSV_ROW)
    csd = docs("csv_rows", CSV_DOCS)
    job("validate", cs, csd)
    job("validated", cs, csd, "require_all")

    ps = schema("post", POST)
    pd = docs("posts", POST_DOCS)
    job("normalized", ps, pd)
    job("validate", ps, pd)

    ts = schema("tags", TAGS)
    td = docs("tags", TAGS_DOCS)
    job("validate", ts, td)

    an = schema("anyof", ANYOF_CORNER)
    ad = docs("anyof", ANYOF_DOCS)
    job("validate", an, ad)

    job("rules_set_registry", "money", schema("money", MONEY))
    job("rules_set_registry", "positive", schema("positive", POSITIVE))
    pr = schema("product", PRODUCT_REG)
    prd = docs("products", PRODUCT_REG_DOCS)
    job("validate", pr, prd)

    st = schema("strict", STRICT)
    std = docs("strict", STRICT_DOCS)
    job("validate", st, std)
    job("validate", st, std, "allow_unknown")
    job("validate", st, std, "allow_unknown=" + json.dumps(UNKNOWN_RULES))
    job("validate", st, std, "require_all", "ignore_none_values")

    write("broken.jsonl", "".join(json.dumps(b) + "\n" for b in BROKEN))
    job("schemas", "broken.jsonl")

    write("jobs.tsv", "".join("\t".join(j) + "\n" for j in jobs))


main()
