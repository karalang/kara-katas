# Writes data/: the JSON documents a tool would query (data/docs/*.json)
# and the jobs (data/jobs.tsv). oracle.py and mini_jsonpath.kara both
# read them.
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

DOCS = {}

DOCS["store"] = {
    "store": {
        "book": [
            {"category": "reference", "author": "Nigel Rees", "title": "Sayings of the Century", "price": 8.95},
            {"category": "fiction", "author": "Evelyn Waugh", "title": "Sword of Honour", "price": 12.99},
            {"category": "fiction", "author": "Herman Melville", "title": "Moby Dick", "isbn": "0-553-21311-3", "price": 8.99},
            {"category": "fiction", "author": "J. R. R. Tolkien", "title": "The Lord of the Rings", "isbn": "0-395-19395-8", "price": 22.99},
        ],
        "bicycle": {"color": "red", "price": 19.95},
    },
    "expensive": 10,
}

DOCS["pods"] = {
    "apiVersion": "v1",
    "kind": "PodList",
    "items": [
        {
            "metadata": {
                "name": "web-7d4b9c-x2kfp",
                "namespace": "shop",
                "labels": {"app.kubernetes.io/name": "web", "tier": "frontend"},
            },
            "spec": {
                "nodeName": "node-a",
                "containers": [
                    {"name": "nginx", "image": "nginx:1.27", "ports": [{"containerPort": 80}, {"containerPort": 443}]},
                    {"name": "log-shipper", "image": "fluent-bit:3.1", "ports": []},
                ],
            },
            "status": {"phase": "Running", "restartCount": 0, "podIP": "10.1.4.17"},
        },
        {
            "metadata": {
                "name": "api-5f6c8d-qq9zt",
                "namespace": "shop",
                "labels": {"app.kubernetes.io/name": "api", "tier": "backend"},
            },
            "spec": {
                "nodeName": "node-b",
                "containers": [
                    {"name": "api", "image": "shop-api:2.4.0", "ports": [{"containerPort": 8080}]},
                ],
            },
            "status": {"phase": "CrashLoopBackOff", "restartCount": 7, "podIP": None},
        },
        {
            "metadata": {
                "name": "worker-0",
                "namespace": "batch",
                "labels": {"tier": "backend"},
            },
            "spec": {
                "nodeName": "node-b",
                "containers": [
                    {"name": "worker", "image": "shop-worker:2.4.0", "ports": []},
                ],
            },
            "status": {"phase": "Pending", "restartCount": 2},
        },
    ],
}

DOCS["issues"] = [
    {"number": 1412, "title": "Crash when config file is empty", "state": "open",
     "labels": [{"name": "bug"}, {"name": "p1"}], "assignee": {"login": "mira"}, "comments": 12,
     "user": {"login": "tdavis"}},
    {"number": 1415, "title": "Add --json flag to status", "state": "open",
     "labels": [{"name": "enhancement"}], "assignee": None, "comments": 3,
     "user": {"login": "kofi"}},
    {"number": 1398, "title": "Docs: fix typo in install guide", "state": "closed",
     "labels": [{"name": "docs"}, {"name": "good first issue"}], "assignee": {"login": "kofi"}, "comments": 1,
     "user": {"login": "lena"}},
    {"number": 1420, "title": "Timeout talking to registry", "state": "open",
     "labels": [], "assignee": None, "comments": 0, "user": {"login": "mira"}},
]

DOCS["orders"] = {
    "orders": [
        {"id": "A-1001", "customer": {"name": "Ana Lima", "tier": "gold"}, "status": "paid",
         "lines": [{"sku": "TEA-01", "qty": 2, "price": 4.5}, {"sku": "MUG-02", "qty": 1, "price": 12.0}],
         "discount": 0.1},
        {"id": "A-1002", "customer": {"name": "Ben Ode", "tier": "silver"}, "status": "shipped",
         "lines": [{"sku": "TEA-01", "qty": 10, "price": 4.5}], "discount": 0},
        {"id": "A-1003", "customer": {"name": "Chen Wu", "tier": "gold"}, "status": "cancelled",
         "lines": [], "discount": None},
        {"id": "A-1004", "customer": {"name": "Dara Kim", "tier": "bronze"}, "status": "paid",
         "lines": [{"sku": "POT-07", "qty": 1, "price": 30.25}, {"sku": "TEA-03", "qty": 3, "price": 6.0},
                   {"sku": "SPOON", "qty": 4, "price": 1.25}], "discount": 0.05},
    ],
    "currency": "EUR",
}

DOCS["package"] = {
    "name": "@acme/dashboard",
    "version": "3.2.1",
    "private": True,
    "scripts": {"build": "vite build", "test": "vitest run", "lint": "eslint src"},
    "dependencies": {"react": "^18.3.1", "react-dom": "^18.3.1", "zod": "^3.23.8"},
    "devDependencies": {"vite": "^5.4.0", "vitest": "^2.0.5", "eslint": "^9.9.0"},
    "keywords": ["dashboard", "charts", "admin"],
    "engines": {"node": ">=20"},
}

DOCS["geo"] = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "id": "trail-1",
         "geometry": {"type": "LineString", "coordinates": [[-122.48, 37.83], [-122.47, 37.81], [-122.45, 37.80]]},
         "properties": {"name": "Coastal Trail", "length_km": 4.2, "surface": "dirt"}},
        {"type": "Feature", "id": "cafe-9",
         "geometry": {"type": "Point", "coordinates": [-122.42, 37.77]},
         "properties": {"name": "Blue Door Cafe", "rating": 4.6, "open": True}},
        {"type": "Feature", "id": "park-3",
         "geometry": {"type": "Polygon", "coordinates": [[[-122.51, 37.77], [-122.45, 37.77], [-122.45, 37.76], [-122.51, 37.77]]]},
         "properties": {"name": "Golden Gate Park", "area_ha": 412}},
    ],
}

DOCS["org"] = {
    "name": "Ruth Okafor", "title": "CEO", "salary": 250000,
    "reports": [
        {"name": "Sam Patel", "title": "CTO", "salary": 210000,
         "reports": [
             {"name": "Ivy Chen", "title": "Engineer", "salary": 140000, "reports": []},
             {"name": "Omar Haddad", "title": "Engineer", "salary": 135000,
              "reports": [{"name": "Lea Rossi", "title": "Intern", "salary": 40000, "reports": []}]},
         ]},
        {"name": "Grace Mwangi", "title": "CFO", "salary": 205000,
         "reports": [{"name": "Tom Berg", "title": "Accountant", "salary": 90000, "reports": []}]},
    ],
}

DOCS["metrics"] = {
    "host": "db-01",
    "samples": [
        {"ts": 1700000000, "cpu": 0.42, "mem": 6144, "disk": "71"},
        {"ts": 1700000060, "cpu": 0.91, "mem": 6400, "disk": "72"},
        {"ts": 1700000120, "cpu": 0.37, "mem": 6016, "disk": "n/a"},
        {"ts": 1700000180, "cpu": 0.88, "mem": 7168, "disk": " 74 "},
    ],
    "thresholds": {"cpu": 0.85, "mem": 7000},
}

DOCS["config"] = {
    "service": "checkout",
    "@type": "deployment",
    "max-connections": 512,
    "features": {"new_ui": True, "beta.pricing": False, "dark_mode": True},
    "environments": {
        "staging": {"replicas": 2, "url": "https://staging.example.test", "db": {"host": "db-stg", "port": 5432}},
        "production": {"replicas": 6, "url": "https://shop.example.test", "db": {"host": "db-prd", "port": 5432}},
    },
    "allowed_origins": ["https://shop.example.test", "https://admin.example.test"],
    "retry": {"attempts": 3, "backoff": [100, 200, 400]},
}

DOCS["log"] = {
    "lines": [
        {"level": "INFO", "msg": "GET /api/cart 200 12ms", "tags": "http,cart"},
        {"level": "WARN", "msg": "GET /api/cart 200 812ms", "tags": "http,cart,slow"},
        {"level": "ERROR", "msg": "POST /api/pay 502 30001ms", "tags": "http,pay"},
        {"level": "INFO", "msg": "cache warm 1532 keys", "tags": "cache"},
    ],
}

# kind, parser, expression, document, argument
JOBS = []


def J(kind, parser, expr, doc="", arg=""):
    JOBS.append([kind, parser, expr, doc, arg])


def H(title):
    JOBS.append(["==", title])


H("parse: the base grammar")
for e in ["$.store.book[0].title", "store.book[*].author", "$..author", "$.store.*",
          "$.store..price", "$..book[2]", "$..book[-1:]", "$..book[0,1]", "$..book[:2]",
          "$.store.book[1:3]", "$.store.book[::2]", "$['store']['bicycle']",
          "$.store.book[?(@.isbn)]", "foo.bar | foo.baz", "a where b", "a wherenot b",
          "(a.b).c", "a.`this`.b", "a.`parent`", "a & b", "'quoted.key'.x", '"dq key"[3]',
          "items[*].metadata.labels.'app.kubernetes.io/name'", "a.b,c.d", "1.2", "@", "$.store.book[",
          "$..", "a.`len`", "`foo`", "a.'unterminated", "$.store.book[0]]", "a\n.b \t. c",
          "a\n.]", "a.b#c", "$[*]", "[*]", "[1:]", "*.x", "a..b..c"]:
    J("parse", "base", e)

H("parse: the extended grammar")
for e in ["$.store.book[?(@.price < 10)].title", "$.store.book[?price > 10]",
          "$.store.book[?(@.category == 'fiction' & @.price > 10)]", "$.items[?status.phase = Running]",
          "$.store.book[\\price]", "$.store.book[/price,\\title]", "$.store.book[\\category, /price]",
          "$.orders[*].lines[*].qty * $.orders[*].lines[*].price", "$.a + 2", "3 - 1", "1.5 * 2.0",
          "$.a / 2", "a.`len`", "a.`keys`", "a.`path`", "a.`sorted`", "a.`split(-, 0, -1)`",
          "a.`sub(/(\\d+)ms/, \\1 ms)`", "a.`str()`", "a.`split(x)`", "a.`nope`",
          "$.trueValue", "$.falseStart", "$[?(@.x =~ 'ab+c')]", "$[?(@.a == true)]", "$[?(@.a != 1.5)]",
          "$[?(@.a >= -3)]", "$[?(@.a <= b)]", "$[?(@.a)]", "$[?((@.a) & (@.b))]", "$[?@.a > ]",
          "$..[?(@.name)]", "$.a.@b", "$.a-b", "$.a - b", "x - y", "$.a[?(@.b == \"q\")]",
          "$.a[?]", "$[?(@ > 1)]", "a | b + 1", "a + b . c", "$.a[?(@.b > 1)].c[\\d]"]:
    J("parse", "ext", e)

H("find: the bookstore")
for e in ["$.store.book[*].author", "$..author", "$.store.*", "$.store..price", "$..book[2]",
          "$..book[-1:]", "$..book[0,1]", "$..book[:2]", "$..book[1:]", "$.store.book[::2].title",
          "$.store.book[::-1].title", "$..book[?(@.isbn)].title", "$..*", "$.store.book[10]",
          "$.store.bicycle[0]", "$.store.bicycle[*]", "$.expensive[*]", "$.store.book[0].title[*]",
          "$.store.book[*].category | $.store.bicycle.color", "$.store.book[*] where isbn",
          "$.store.book[*] wherenot isbn", "$.store.book[0].`this`.title", "$.store.book[0].title.`parent`.author",
          "$.store.book[0].title.`parent`.`parent`[1].title", "$.store.book[0] & $.store.book[1]",
          "$.store.book.author", "$.store.book[0]..price", "$..price..price", "store.book[3].isbn",
          "$.store['bicycle','book'][0]", "$.store.book[0]['title','price','nope']", "$.store.book[-1]"]:
    J("find", "base", e, "store")
for e in ["$.store.book[?(@.price < 10)].title", "$.store.book[?price > 10].title",
          "$.store.book[?(@.category == 'fiction' & @.price > 10)].title",
          "$.store.book[?(@.category = fiction)].author", "$.store.book[?(@.price == 8)].title",
          "$.store.book[?(@.isbn =~ '^0-3')].isbn", "$.store.book[?(@.author =~ 'M.l+')].author",
          "$.store.book[\\price]", "$.store.book[/category,\\price]", "$.store.book[\\author]",
          "$.store.book[\\price]", "$.store.book[/category,\\price]", "$.store.book[\\author]",
          "$.store.book[\\price].title", "$.store.book[/price].price", "$.store.book[/category,\\price].title",
          "$.store.book[\\category, /title].title", "$.store.book.`len`", "$.store.`keys`", "$.store.book[*].`keys`",
          "$.store.book[0].price * 2", "$.store.book[*].price + 1", "$.store.bicycle.price - $.store.book[0].price",
          "$.store.book[*].price * $.store.book[*].price", "$.store.book[*].price * $.store.bicycle.price",
          "$.store.book[*].title + ' (2nd ed.)'", "$.store.book[*].author.`split( , -1, -1)`",
          "$.store.book[*].isbn.`split(-, 1, 2)`", "$.store.book[*].isbn.`split(-, *, 1)`",
          "$.store.book[*].title.`sub(/^The /, A )`", "$.store.book[*].price.`str()`", "$.expensive.`str()`",
          "$.store.book[*].title.`path`", "$.store.book[0].`path`", "$.store.`sorted`", "$.store.book[*].category.`sorted`",
          "$.store.book[?(@.price > $.expensive)].title", "$.store.book[?(@.price > 10.5)].title",
          "$.store.book[?(@.isbn)].isbn", "$.store[?(@.color)]", "$.store.bicycle[?(@ == red)]",
          "$.store.book[?(@.price > 10)].`len`", "$..book[?(@.price < 9)].`path`"]:
    J("find", "ext", e, "store")

H("find: kubernetes pods")
for e in ["$.items[*].metadata.name", "items[*].metadata.labels.'app.kubernetes.io/name'",
          "$.items[*].spec.containers[*].image", "$..containerPort", "$.items[*].status.podIP",
          "$..ports[*].containerPort", "$.items[1:].metadata.namespace", "$..labels.tier",
          "$.items[*].spec.containers[*] where ports", "$..containers[*].ports[0]"]:
    J("find", "base", e, "pods")
for e in ["$.items[?(@.status.phase != 'Running')].metadata.name",
          "$.items[?(@.status.restartCount > 1)].metadata.name",
          "$.items[?(@.spec.nodeName == 'node-b' & @.metadata.namespace == 'shop')].metadata.name",
          "$.items[*].spec.containers.`len`", "$.items[*].spec.containers[*].ports.`len`",
          "$.items[?(@.metadata.labels.tier == backend)].status.restartCount",
          "$.items[\\status.restartCount].metadata.name", "$.items[*].metadata.labels.`keys`",
          "$.items[*].spec.containers[*].image.`split(:, 1, -1)`",
          "$.items[?(@.status.podIP =~ '^10\\.1\\.')].metadata.name",
          "$.items[?(@.status.podIP)].metadata.name", "$..[?(@.containerPort > 100)].containerPort",
          "$.items[*].status.restartCount + 1", "$.items[?(@.status.podIP == None)].metadata.name"]:
    J("find", "ext", e, "pods")

H("find: issues")
for e in ["$[*].title", "[*].number", "$[?(@.state == 'open')].number", "$[?(@.assignee)].assignee.login",
          "$[?(@.comments > 2)].title", "$[*].labels[*].name", "$[?(@.labels[*].name == 'bug')].number",
          "$[\\comments].number", "$[/user.login,\\number].number", "$[*].labels.`len`",
          "$[?(@.state == open & @.assignee)].number", "$.`len`", "$[0].`keys`",
          "$[?(@.user.login == 'mira')].title.`sub(/ /, _)`"]:
    J("find", "ext", e, "issues")
for e in ["$[*].user.login", "$[0:2].number", "$..login", "$[*].assignee.login", "$[*] wherenot assignee"]:
    J("find", "base", e, "issues")

H("find: orders")
for e in ["$.orders[*].lines[*].qty * $.orders[*].lines[*].price", "$.orders[0].lines[*].qty * $.orders[0].lines[*].price",
          "$.orders[?(@.customer.tier == gold)].id", "$.orders[?(@.discount > 0)].id",
          "$.orders[?(@.discount)].discount", "$.orders[*].lines.`len`", "$.orders[\\lines[0].qty].id",
          "$.orders[?(@.status == 'paid')].lines[*].sku", "$..lines[?(@.qty >= 3)].sku",
          "$.orders[*].customer.name.`split( , 0, -1)`", "$.orders[*].customer.name.`split( , 1, -1)`",
          "$.orders[*].id.`sub(/A-(\\d+)/, order-\\1)`", "$.orders[?(@.lines[*].sku == 'TEA-01')].id",
          "$.orders[*].discount * 100", "$.currency.`len`", "$.orders[?(@.discount < 0.1)].id"]:
    J("find", "ext", e, "orders")

H("find: package.json")
for e in ["$.dependencies.`keys`", "$.devDependencies.*", "$.scripts.test", "$.keywords[*]",
          "$['dependencies','devDependencies'].react", "$.name", "$.engines.node", "$..vite", "$.keywords.`sorted`",
          "$.private", "$.dependencies.react-dom", "$.dependencies.`len`", "$.version.`split(., 0, -1)`",
          "$.version.`split(., *, -1)`", "$.version.`split(., 2, 1)`", "$.version.`split(\".\", 1, -1)`",
          "$.name.`sub(/^@[^/]+\\//, )`", "$.scripts[?(@ =~ 'vite')]", "$.keywords[?(@ > c)]"]:
    J("find", "ext", e, "package")

H("find: geojson")
for e in ["$.features[*].id", "$.features[*].geometry.type", "$.features[0].geometry.coordinates[*][0]",
          "$.features[1].geometry.coordinates[1]", "$..coordinates", "$.features[*].properties.name",
          "$.features[2].geometry.coordinates[0][1:3]"]:
    J("find", "base", e, "geo")
for e in ["$.features[?(@.geometry.type == Point)].properties.name",
          "$.features[?(@.properties.rating > 4)].id", "$.features[?(@.properties.open == true)].id",
          "$.features[*].geometry.coordinates.`len`", "$.features[*].properties.`keys`",
          "$.features[\\properties.name].id", "$.features[?(@.properties.length_km)].properties.length_km * 1000"]:
    J("find", "ext", e, "geo")

H("find: the org chart")
for e in ["$..name", "$.reports[*].name", "$..reports[*].title", "$.reports[0].reports[1].reports[0].name",
          "$..reports[0].name", "$.reports..salary", "name", "$..reports[*] where reports[0]"]:
    J("find", "base", e, "org")
for e in ["$..reports[?(@.salary > 150000)].name", "$..reports[?(@.title == Engineer)].name",
          "$..reports[?(@.reports.`len` > 0)].name", "$..[?(@.title =~ '^C')].name", "$.reports[\\salary].name",
          "$..reports[?(@.salary < 100000)].`path`", "$..salary.`sorted`"]:
    J("find", "ext", e, "org")

H("find: metrics")
for e in ["$.samples[?(@.cpu > $.thresholds.cpu)].ts", "$.samples[?(@.cpu > 0.85)].ts",
          "$.samples[?(@.disk > 71)].ts", "$.samples[?(@.disk == 72)].disk", "$.samples[?(@.mem >= 7000)].ts",
          "$.samples[?(@.cpu == 0)].ts", "$.samples[*].cpu * 100", "$.samples[*].mem / 1024",
          "$.samples[*].mem - $.samples[*].mem", "$.samples[\\cpu].ts", "$.samples[/disk].disk",
          "$.samples[*].ts - 1700000000", "$.samples.`len`", "$.thresholds.`keys`",
          "$.samples[?(@.cpu > 0.5 & @.mem > 6200)].ts", "$.samples[*].disk.`str()`", "$.host + '.internal'",
          "$.samples[?(@.ts == true)].ts"]:
    J("find", "ext", e, "metrics")

H("find: service config")
for e in ["$.'@type'", "$.max-connections", "$.features.'beta.pricing'", "$.environments.*.url",
          "$.environments.*.db.host", "$..port", "$.retry.backoff[1:]", "$.environments['staging','production'].replicas",
          "$.features.*", "$.allowed_origins[0]", "$..db"]:
    J("find", "base", e, "config")
for e in ["$.environments[?(@.replicas > 3)].url", "$.environments.`keys`", "$.features[?(@ == true)]",
          "$.features[?(@ == false)]", "$.retry.backoff[?(@ > 150)]", "$.retry.backoff.`sorted`",
          "$.environments.*.replicas * 2", "$.@type", "$[?(@.replicas)]",
          "$.allowed_origins[*].`sub(/https:\\/\\//, )`", "$.allowed_origins[*].`split(., 0, -1)`",
          "$.retry.attempts * $.retry.backoff[0]", "$.environments.*.db.port.`str()`", "$.service.`sorted`"]:
    J("find", "ext", e, "config")

H("find: log lines")
for e in ["$.lines[?(@.level == ERROR)].msg", "$.lines[?(@.msg =~ '[0-9]{3,}ms')].msg",
          "$.lines[*].msg.`sub(/(\\d+)ms/, \\1 ms)`", "$.lines[*].msg.`sub(/^(\\w+) (\\S+).*/, \\2 via \\1)`",
          "$.lines[*].tags.`split(\",\", *, -1)`", "$.lines[*].tags.`split(',', 0, -1)`",
          "$.lines[*].tags.`split(\",\", -1, -1)`", "$.lines[*].msg.`split( , 2, -1)`",
          "$.lines[?(@.level != INFO)].level", "$.lines[/level].level", "$.lines[*].level.`sorted`",
          "$.lines[?(@.tags =~ 'slow')].msg", "$.lines[*].msg.`sub(/\\d+ keys/, many keys)`",
          "$.lines[*].msg.`sub(/x/, y)`", "$.lines[*].msg.`sub(/(\\\\d+)ms/, \\\\1 ms)`",
          "$.lines[*].msg.`sub(/^(\\\\w+) (\\\\S+).*/, \\\\2 via \\\\1)`",
          "$.lines[0].msg.`sub(/(?P<verb>[A-Z]+) /, \\\\g<verb>: )`", "$.lines[*].level.`sub(/^(.)(.*)$/, \\\\1)`",
          "$.lines[*].msg.`sub(/[aeiou]/, *)`", "$.lines[*].tags.`sub(/,/, ;)`", "$.lines[0].msg.`sub(/(?P<verb>GET)/, \\g<verb>!)`"]:
    J("find", "ext", e, "log")

H("update")
J("update", "base", "$.store.book[*].price", "store", "10")
J("update", "base", "$.store.bicycle.color", "store", '"blue"')
J("update", "base", "$..price", "store", "0")
J("update", "base", "$.store.book[0]", "store", '{"title": "Replaced"}')
J("update", "base", "$.store.book[1:3].title", "store", '"(checked out)"')
J("update", "base", "$.store.nope", "store", "1")
J("update", "base", "$.store.book[9]", "store", "1")
J("update", "base", "$", "store", '"everything"')
J("update", "base", "$.store.book[*] where isbn", "store", '"has isbn"')
J("update", "base", "$.store.*", "store", "null")
J("update", "base", "$.items[*].status.phase", "pods", '"Unknown"')
J("update", "base", "$.environments.*.replicas", "config", "1")
J("update", "base", "$.retry.backoff[0]", "config", "50")
J("update", "base", "$..reports[*].salary", "org", "1")
J("update", "ext", "$.store.book[?(@.price > 10)].price", "store", "9.99")
J("update", "ext", "$.store.book[?(@.category == reference)]", "store", '"gone"')
J("update", "ext", "$.orders[?(@.status == 'cancelled')].status", "orders", '"archived"')
J("update", "ext", "$.features[?(@ == true)]", "config", "false")
J("update", "ext", "$.samples[*].disk", "metrics", '"0"')

H("update with a function")
J("updatefn", "base", "$.store.book[*].price", "store", "double")
J("updatefn", "base", "$.store.book[*].title", "store", "upper")
J("updatefn", "base", "$.items[*].status.restartCount", "pods", "inc")
J("updatefn", "base", "$.retry.backoff[2]", "config", "double")
J("updatefn", "base", "$.retry.backoff[*]", "config", "double")
J("updatefn", "base", "$..salary", "org", "inc")
J("updatefn", "ext", "$.orders[*].lines[?(@.qty > 2)]", "orders", "mark")
J("updatefn", "base", "$.keywords[1]", "package", "upper")
J("updatefn", "base", "$.store.book[0].title", "store", "label")

H("update_or_create")
J("create", "base", "$.store.book[0].edition", "store", "2")
J("create", "base", "$.store.magazine.title", "store", '"Byte"')
J("create", "base", "a.b.c", "{}", "1")
J("create", "base", "a[2].b", "{}", '"x"')
J("create", "base", "a[0]", "{}", "true")
J("create", "base", "$.retry.backoff[4]", "config", "800")
J("create", "base", "$.environments.dev.replicas", "config", "1")
J("create", "base", "$.environments.*.region", "config", '"eu-west-1"')
J("create", "base", "spec.containers[1].name", "{}", '"sidecar"')
J("create", "base", "a.b", '{"a": 5}', "1")
J("create", "base", "[1]", "[]", "7")
J("create", "base", "x[0][1]", "{}", '"y"')

H("find_or_create")
J("findcreate", "base", "a.b[1].c", "{}")
J("findcreate", "base", "$.store.book[0].tags", "store")
J("findcreate", "base", "$.metadata.labels", "pods")

H("filter")
J("filter", "base", "$.store.book[*].isbn", "store", "any")
J("filter", "base", "$.store.book[*]", "store", "cheap")
J("filter", "base", "$.store.book[*].price", "store", "cheap")
J("filter", "base", "$.store.*", "store", "is_list")
J("filter", "base", "$..price", "store", "cheap")
J("filter", "base", "$[*]", "issues", "unassigned")
J("filter", "base", "$[*].assignee", "issues", "is_none")
J("filter", "base", "$.retry.backoff[1]", "config", "any")
J("filter", "base", "$.retry.backoff[0:2]", "config", "any")
J("filter", "base", "$.retry.backoff[*]", "config", "big")
J("filter", "ext", "$.orders[?(@.status == cancelled)]", "orders", "any")
J("filter", "ext", "$.features[?(@ == false)]", "config", "any")
J("filter", "ext", "$.samples[?(@.disk == 'n/a')]", "metrics", "any")
J("filter", "base", "$.store.book[*] where isbn", "store", "any")
J("filter", "base", "$.items[*].metadata.labels.tier", "pods", "any")

H("the command line")
J("cli", "base", "$..author", "", "docs/store.json")
J("cli", "base", "store.bicycle", "", "docs/store.json")
J("cli", "base", "items[*].metadata.name", "", "docs/pods.json docs/store.json docs/missing.json")
J("cli", "base", "$..login", "", "docs/issues.json")
J("cli", "base", "name", "", "docs/package.json docs/org.json")
J("cli", "base", "$.keywords", "", "docs/package.json")
J("cli", "base", "features[*].properties.rating", "", "docs/geo.json")
J("cli", "base", "$.nope", "", "docs/geo.json")
J("cli", "base", "$.private", "", "docs/package.json")


def main():
    os.makedirs(os.path.join(DATA, "docs"), exist_ok=True)
    for name, doc in DOCS.items():
        with open(os.path.join(DATA, "docs", name + ".json"), "w") as f:
            f.write(json.dumps(doc, indent=2) + "\n")
    with open(os.path.join(DATA, "jobs.tsv"), "w") as f:
        for row in JOBS:
            for col in row:
                assert "\t" not in col and "\n" not in col or row[0] == "parse", row
            f.write("\t".join(c.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t") for c in row) + "\n")


if __name__ == "__main__":
    main()
