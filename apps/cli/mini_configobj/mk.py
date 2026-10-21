# Writes data/: the config files and configspecs the jobs load, and
# jobs.tsv, the operations run on them.
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def write(rel, text, newline="\n"):
    path = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(text.replace("\n", newline).encode("utf-8"))


FILES = {}

FILES["etc/webapp.ini"] = '''\
# webapp.ini: settings for the shop front end
# edit with care, the deploy tool rewrites this file

name = shop-frontend
version = 2.14.0
owners = alice@example.com, bob@example.com
debug = off   # never on in production
motd = """Welcome to the shop.
Orders placed after 18:00 ship the next day."""

# the HTTP server
[server]
host = 0.0.0.0
port = 8080
workers = 8
allowed_hosts = shop.example.com, www.shop.example.com, "localhost, 127.0.0.1"
timeout = 30.5
    # keep-alive in seconds
    keepalive = 5

[database]
engine = postgresql
    [[primary]]
    host = db1.internal
    port = 5432
    user = shop
    password = 's3cr3t#with#hashes'
    [[replica]]
    host = db2.internal
    port = 5433
    options = sslmode=require, connect_timeout=10,

[logging]
level = INFO
format = '%(asctime)s %(levelname)s %(message)s'
    [[handlers]]
        [[[console]]]
        class = StreamHandler
        stream = ext://sys.stdout
        [[[file]]]
        class = RotatingFileHandler
        filename = /var/log/shop/app.log
        maxBytes = 10485760
        backupCount = 5
[cache]
backend = redis
servers = ,
ttl =
# end of file
'''

FILES["etc/interp.ini"] = '''\
home = /srv/shop
user = shop
log_dir = %(home)s/logs
pid = %(home)s/run/%(user)s.pid
loop_a = %(loop_b)s
loop_b = %(loop_a)s
self_ref = %(self_ref)s
broken = %(nothing_here)s
percent = 100%
hosts = a, b
uses_list = %(hosts)s
plain_list = %(home)s/a, %(user)s/b
[DEFAULT]
region = eu-west-1
bucket = shop-%(region)s
[storage]
path = %(home)s/storage
url = s3://%(bucket)s/%(user)s
[[nested]]
home = /opt/other
path = %(home)s/nested
deep = %(path)s/deeper
[[[DEFAULT]]]
region = us-east-1
[[[leaf]]]
where = %(region)s in %(bucket)s
[workers]
count = 4
cmd = run --workers=%(count)s --log=%(log_dir)s
odd = %(count)
empty = %()s
'''

FILES["etc/template.ini"] = '''\
root = /srv/app
env = staging
data = $root/data
logs = ${root}/logs/${env}
price = $$5 per seat
dollar = costs $ 5
digits = $1abc
mixed = $ROOT and $Root
unknown = $nope
braced_bad = ${not closed
nested = $data/cache
[DEFAULT]
tier = gold
[service]
name = api-$env
tier_note = tier $tier
path = $data/$name
'''

FILES["etc/broken.ini"] = '''\
# a config with several mistakes in it
good = 1
this line has no equals sign
good = 2
[section]
x = "unclosed
y = 'mixed"
[[child]]
z = 1
[[[[too deep]]]]
[section]
[a]]
w = """never closed
'''

FILES["etc/broken_one.ini"] = '''\
[server]
port = 80
port = 81
'''

FILES["etc/nesting.ini"] = '''\
[one]
[[two]]
[[[three]]]
[two_again]]
'''

FILES["etc/dropback.ini"] = '''\
[a]
[[b]]
[[[c]]]
leaf = 1
[[d]]
x = 2
[e]
y = 3
    [[f]]
        [[[g]]]
        z = 4
[h]
'''

FILES["etc/badmulti.ini"] = '''\
a = """one""" """two"""
b = """x"""y"""
c = """line one
line two""" trailing
d = 1
'''

FILES["etc/quotes.ini"] = '''\
plain = hello world
spaced = "  padded  "
hash = "has # inside"
both = """it's "quoted" here"""
single_item = alpha,
empty_list = ,
empty_quoted = ""
empty =
commas = "a, b", c
nested_quotes = "it's", 'say "hi"'
tab = "a\tb"
trailing_comma = a, b, c,
"key with = sign" = yes
'quoted key' = 1
key#hash = value
spaces in key = fine
multi = \'\'\'first
second\'\'\'
multi_double = """a
b
c"""  # inline after multiline
oneline_triple = \'\'\'just one\'\'\'  # comment
'''

FILES["etc/crlf.ini"] = '''\
# windows line endings
a = 1
[s]
b = two words
'''

FILES["etc/unicode.ini"] = '''\
# café settings
greeting = Grüße, 世界
name = Zoë
[ünïcode]
key = naïve
'''

FILES["etc/nolist.ini"] = '''\
a = 1, 2, 3
b = "quoted, still one"  # comment
c = 'single' # c
d =
e = value # trailing
f = "unclosed, list
'''

FILES["etc/indent.ini"] = '''\
top = 1
[a]
\tx = 1
\t[[b]]
\t\ty = 2
'''

# ---- validation

FILES["etc/app.ini"] = '''\
# application settings
name = inventory
port = 8443
workers = 12
debug = Yes
ratio = 0.75
admin_ip = 10.0.0.1
hosts = alpha.example.com, beta.example.com
log_level = WARNING
retry = 3, 0.5
unexpected = 1
[database]
url = postgres://inv@db/inv
pool = 20
[[replicas]]
    [[[east]]]
    host = db-east
    port = 5433
    [[[west]]]
    host = db-west
[features]
search = on
export = maybe
beta = 0
[extra_section]
x = 1
'''

FILES["etc/app.spec"] = '''\
# the settings an inventory service understands
name = string(min=3, max=32)
port = integer(1, 65535)
workers = integer(min=1, max=64, default=4)
timeout = float(default=30.0)
debug = boolean(default=False)
ratio = float(0, 1)
admin_ip = ip_addr
hosts = string_list(min=1)
log_level = option('DEBUG', 'INFO', 'WARNING', 'ERROR', default='INFO')
tags = force_list(default=list())
retry = mixed_list('integer', 'float')
owner = string(default=None)
greeting = string(default="hello, world")
[database]
url = string
pool = integer(min=1, default=5)
backup = boolean(default=no)
[[replicas]]
[[[__many__]]]
host = string
port = integer(default=5432)
[features]
__many__ = boolean
[metrics]
enabled = boolean(default=True)
interval = integer(default=60)
'''

FILES["etc/app_bad.ini"] = '''\
name = x
port = 70000
workers = zero
debug = sometimes
ratio = 1.5
admin_ip = 10.0.0.300
hosts = single.example.com
log_level = TRACE
retry = 1, 2, 3
[database]
pool = 0
[features]
search = 2
[metrics]
'''

FILES["etc/app_bad2.ini"] = '''\
name = ok
port = 1
ratio = 0.1
admin_ip = 127.1
hosts = a,
retry = 1, 2
[metrics]
enabled = no
[database]
url = x
'''

FILES["etc/scalar_section.ini"] = '''\
name = svc
port = 1
ratio = 0
admin_ip = 1.2.3.4
hosts = a, b
retry = 1, 1.5
features = all
[database]
url = x
[[replicas]]
[[[one]]]
port = 1
[metrics]
'''

FILES["etc/broken.spec"] = '''\
a = integer(min=abc)
'''

FILES["etc/unknown.spec"] = '''\
a = frobnicate(1, 2)
b = integer(default=nope)
c = string(default=list('x', 'y'))
d = integer(default=None)
e = string(default='None')
f = pass(default=raw)
'''

FILES["etc/kwarg.spec"] = '''\
a = integer(foo=1)
'''

FILES["etc/tiny.ini"] = '''\
a = 5
b = 6
c = 7
d = 8
e = 9
f = 10
'''

FILES["etc/empty.ini"] = ''

# ---- merging: shipped defaults, then the environment, then local edits

FILES["etc/merge/base.ini"] = '''\
# shipped defaults
app = billing
debug = false
[server]
host = 127.0.0.1
port = 8000
[[tls]]
enabled = false
cert = /etc/ssl/billing.pem
[queues]
names = invoices, reminders
[old]
kept = yes
'''

FILES["etc/merge/production.ini"] = '''\
# production overrides
[server]
host = 0.0.0.0
[[tls]]
enabled = true
[queues]
names = invoices, reminders, dunning
workers = 16
[audit]
sink = syslog
old = scalar now
'''

FILES["etc/merge/local.ini"] = '''\
debug = true
old = replaced by a value
[server]
port = 9000
[audit]
sink = file
[[file]]
path = /tmp/audit.log
'''

FILES["etc/rename.ini"] = '''\
# client template
[XXXXsection]
XXXXkey = XXXXvalue
other = keep XXXX here
[[XXXXsub]]
list = XXXXa, b
'''

FILES["etc/ints.ini"] = '''\
a = 10
b = -3
c = 1_000
d = 0x10
e = abc
f = 1, 2
[s]
g = ' 42 '
h = 4.0
'''

FILES["etc/bools.ini"] = '''\
a = Yes
b = off
c = TRUE
d = 0
e = maybe
f = 1, 2
g = 1.5
h = 2e3
i = inf
j = -nan
k = 1_0.5
l = .5
m = 5.
n = 1e
o = ٣.٥
'''

for rel, text in FILES.items():
    write(rel, text, "\r\n" if rel == "etc/crlf.ini" else "\n")


# ---- the jobs
J = []


def esc(s):
    return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


def job(*parts):
    J.append("\t".join(esc(p if isinstance(p, str) else json.dumps(p)) for p in parts))


def group(name):
    J.append("== " + name)


group("load and repr")
for f in ["webapp", "quotes", "crlf", "unicode", "dropback", "indent", "empty", "missing"]:
    job("load", f, "etc/%s.ini" % f, "{}")
    job("repr", f)
job("get", "webapp", "server/port")
job("get", "webapp", "server/allowed_hosts")
job("get", "webapp", "database/replica/options")
job("get", "webapp", "logging/format")
job("get", "webapp", "logging/handlers/file")
job("get", "webapp", "cache/servers")
job("get", "webapp", "cache/ttl")
job("get", "webapp", "nope")
job("get", "webapp", "server/nope")
job("keys", "webapp")
job("keys", "webapp", "database")
job("items", "webapp", "database/primary")
job("dict", "webapp", "database")
job("comments", "webapp")
job("comments", "webapp", "server")
job("comments", "quotes")

group("write")
for f in ["webapp", "quotes", "crlf", "dropback", "indent", "empty"]:
    job("write", f)
job("write", "unicode")
job("load", "unicode8", "etc/unicode.ini", json.dumps({"encoding": "utf-8"}))
job("write", "unicode8")
job("repr", "unicode8")
job("load", "ind2", "etc/webapp.ini", json.dumps({"indent_type": "\t"}))
job("write", "ind2", "database")
job("load", "wev", "etc/webapp.ini", json.dumps({"write_empty_values": True}))
job("write", "wev", "cache")

group("errors")
for f in ["broken", "broken_one", "nesting", "badmulti"]:
    job("load", f, "etc/%s.ini" % f, "{}")
    job("load", f + "_r", "etc/%s.ini" % f, json.dumps({"raise_errors": True}))
job("load", "nolist", "etc/nolist.ini", json.dumps({"list_values": False}))
job("repr", "nolist")
job("write", "nolist")
job("load", "nolist2", "etc/nolist.ini", "{}")

group("interpolation")
job("load", "ip", "etc/interp.ini", "{}")
for path in ["log_dir", "pid", "loop_a", "self_ref", "broken", "percent", "uses_list",
             "plain_list", "storage/path", "storage/url", "storage/nested/path",
             "storage/nested/deep", "storage/nested/leaf/where", "workers/cmd",
             "workers/odd", "workers/empty", "DEFAULT/bucket", "hosts"]:
    job("get", "ip", path)
job("repr", "ip", "storage")
job("repr", "ip")
job("write", "ip", "workers")
job("load", "ipoff", "etc/interp.ini", json.dumps({"interpolation": False}))
job("get", "ipoff", "pid")
job("get", "ipoff", "loop_a")
job("load", "tp", "etc/template.ini", json.dumps({"interpolation": "template"}))
for path in ["data", "logs", "price", "dollar", "digits", "mixed", "unknown", "braced_bad",
             "nested", "service/name", "service/tier_note", "service/path"]:
    job("get", "tp", path)
job("load", "tp2", "etc/template.ini", json.dumps({"interpolation": "Template"}))
job("get", "tp2", "logs")
job("load", "tpbad", "etc/template.ini", json.dumps({"interpolation": "jinja"}))
job("get", "tpbad", "logs")
job("get", "tpbad", "data")
job("load", "cp", "etc/template.ini", json.dumps({"interpolation": "configparser"}))
job("get", "cp", "logs")

group("as_ helpers")
job("load", "ints", "etc/ints.ini", "{}")
for k in ["a", "b", "c", "d", "e", "f", "s/g", "s/h", "s", "zz"]:
    job("as_int", "ints", k)
job("load", "bools", "etc/bools.ini", "{}")
for k in "abcdefghijklmno":
    job("as_bool", "bools", k)
    job("as_float", "bools", k)
for k in ["a", "f", "s"]:
    job("as_list", "ints", k)

group("editing")
job("load", "ed", "etc/webapp.ini", "{}")
job("set", "ed", "server/port", json.dumps("9090"))
job("set", "ed", "server/aliases", json.dumps(["shop", "store"]))
job("set", "ed", "newsec", json.dumps({"a": "1", "inner": {"b": "2"}}))
job("set", "ed", "server/empty", json.dumps([]))
job("set", "ed", "server/one", json.dumps(["only"]))
job("set", "ed", "server/tricky", json.dumps("it's \"both\""))
job("set", "ed", "server/lead", json.dumps(" leading space"))
job("set", "ed", "server/hashy", json.dumps("a#b"))
job("set", "ed", "server/withnl", json.dumps("line1\nline2"))
job("set", "ed", "server/num", json.dumps(42))
job("set", "ed", "server/flt", json.dumps(0.1))
job("set", "ed", "server/none", json.dumps(None))
job("set", "ed", "server/yes", json.dumps(True))
job("rename", "ed", "server", "workers", "processes")
job("rename", "ed", "", "database", "db")
job("rename", "ed", "server", "missing", "x")
job("del", "ed", "server/keepalive")
job("del", "ed", "cache")
job("pop", "ed", "name")
job("pop", "ed", "name")
job("setdefault", "ed", "server/host", "x")
job("setdefault", "ed", "server/backlog", "128")
job("popitem", "ed", "logging/handlers")
job("write", "ed")
job("load", "bad1", "etc/webapp.ini", "{}")
job("set", "bad1", "server/bad", json.dumps("a'b\"c\nd'''e\"\"\""))
job("write", "bad1", "server")
job("load", "bad2", "etc/webapp.ini", "{}")
job("set", "bad2", "server/both", json.dumps(["it's", "say \"x\""]))
job("write", "bad2", "server")
job("load", "bad3", "etc/webapp.ini", json.dumps({"stringify": False}))
job("set", "bad3", "server/num", json.dumps(42))
job("set", "bad3", "server/nums", json.dumps([1, 2]))
job("set", "bad3", "server/fine", json.dumps(["1", "2"]))
job("write", "bad3", "server")
job("load", "keyq", "etc/empty.ini", "{}")
job("set", "keyq", "a=b", json.dumps("1"))
job("set", "keyq", " spaced", json.dumps("2"))
job("set", "keyq", "both'\"", json.dumps("3"))
job("write", "keyq")
job("load", "keyq2", "etc/empty.ini", "{}")
job("set", "keyq2", "multi\nline", json.dumps("4"))
job("write", "keyq2")

group("merge")
job("load", "base", "etc/merge/base.ini", json.dumps({"interpolation": False}))
job("load", "prod", "etc/merge/production.ini", json.dumps({"interpolation": False}))
job("load", "local", "etc/merge/local.ini", json.dumps({"interpolation": False}))
job("merge", "base", "prod")
job("merge", "base", "local")
job("repr", "base")
job("write", "base")

group("walk")
job("load", "rn", "etc/rename.ini", "{}")
job("walk_rename", "rn", "XXXX", "CLIENT1")
job("repr", "rn")
job("write", "rn")
job("load", "wi", "etc/ints.ini", "{}")
job("walk_int", "wi", "lenient")
job("repr", "wi")
job("load", "wi2", "etc/ints.ini", "{}")
job("walk_int", "wi2", "strict")
job("repr", "wi2")

group("validate")
job("load", "app", "etc/app.ini", json.dumps({"configspec": "etc/app.spec"}))
job("validate", "app", "{}")
job("repr", "app")
job("extra", "app")
job("write", "app")
job("restore_defaults", "app")
job("repr", "app", "database")
job("load", "app_p", "etc/app.ini", json.dumps({"configspec": "etc/app.spec"}))
job("validate", "app_p", json.dumps({"preserve_errors": True}))
job("flatten", "app_p")
job("load", "bad", "etc/app_bad.ini", json.dumps({"configspec": "etc/app.spec"}))
job("validate", "bad", "{}")
job("flatten", "bad")
job("load", "badp", "etc/app_bad.ini", json.dumps({"configspec": "etc/app.spec"}))
job("validate", "badp", json.dumps({"preserve_errors": True}))
job("flatten", "badp")
job("extra", "badp")
job("repr", "badp")
job("load", "bad2", "etc/app_bad2.ini", json.dumps({"configspec": "etc/app.spec"}))
job("validate", "bad2", json.dumps({"preserve_errors": True}))
job("flatten", "bad2")
job("load", "ss", "etc/scalar_section.ini", json.dumps({"configspec": "etc/app.spec"}))
job("validate", "ss", json.dumps({"preserve_errors": True}))
job("flatten", "ss")
job("load", "ss2", "etc/scalar_section.ini", json.dumps({"configspec": "etc/app.spec"}))
job("validate", "ss2", "{}")
job("load", "fresh", "etc/empty.ini", json.dumps({"configspec": "etc/app.spec"}))
job("validate", "fresh", json.dumps({"copy": True}))
job("write", "fresh")
job("load", "fresh2", "etc/empty.ini", json.dumps({"configspec": "etc/app.spec"}))
job("validate", "fresh2", "{}")
job("write", "fresh2")
job("repr", "fresh2")
job("load", "nostr", "etc/app.ini", json.dumps({"configspec": "etc/app.spec", "stringify": False}))
job("validate", "nostr", "{}")
job("repr", "nostr")
job("load", "nospec", "etc/app.ini", "{}")
job("validate", "nospec", "{}")
job("load", "brk", "etc/tiny.ini", json.dumps({"configspec": "etc/broken.spec"}))
job("validate", "brk", "{}")
job("load", "unk", "etc/tiny.ini", json.dumps({"configspec": "etc/unknown.spec"}))
job("validate", "unk", json.dumps({"preserve_errors": True}))
job("repr", "unk")
job("load", "kw", "etc/tiny.ini", json.dumps({"configspec": "etc/kwarg.spec"}))
job("validate", "kw", "{}")
job("load", "nospecfile", "etc/tiny.ini", json.dumps({"configspec": "etc/nothere.spec"}))
job("load", "badspecfile", "etc/tiny.ini", json.dumps({"configspec": "etc/broken.ini"}))

group("checks")
CHECKS = [
    ("integer", "12"), ("integer", " 12 "), ("integer", "-0"), ("integer", "1_000"),
    ("integer", "1__0"), ("integer", "12.0"), ("integer", "0x10"), ("integer", "٣٤"),
    ("integer", ["1"]), ("integer(0, 9)", "10"), ("integer(0, 9)", "-1"),
    ("integer(max=5)", "5"), ("integer(min=x)", "1"), ("integer(1, 2, 3)", "1"),
    ("integer(1, min=2)", "1"), ("integer(bogus=1)", "1"), ("integer()", "7"),
    ("float", "1.5"), ("float", "1e400"), ("float", "-inf"), ("float", "nan"),
    ("float", "1_000.25"), ("float", ".5e-3"), ("float", "abc"), ("float(0.5, 2)", "0.25"),
    ("float(max=1e2)", "101"), ("float(min='1')", "0"), ("float", "  2  "),
    ("boolean", "YES"), ("boolean", "On"), ("boolean", "nah"), ("boolean", ["1"]),
    ("boolean(1)", "1"), ("ip_addr", "192.168.1.1"), ("ip_addr", " 10.1 "),
    ("ip_addr", "0x7f.1"), ("ip_addr", "017.0.0.1"), ("ip_addr", "08.1.1.1"),
    ("ip_addr", "1.2.3.4 junk"), ("ip_addr", "1.2.65536"), ("ip_addr", "4294967295"),
    ("ip_addr", "4294967296"), ("ip_addr", "1.2.3."), ("ip_addr", "0x"), ("ip_addr", ["1"]),
    ("string", "abc"), ("string(2, 3)", "abcd"), ("string(min=5)", "abc"), ("string", ["a"]),
    ("string(max=3)", "日本語"), ("list", ["a", "b"]), ("list", "a"), ("list(min=3)", ["a"]),
    ("list(max=1)", ["a", "b"]), ("tuple", ["a", "b"]), ("tuple", []),
    ("int_list", ["1", "2"]), ("int_list", ["1", "x"]), ("int_list(min=1)", []),
    ("float_list", ["1", "2.5"]), ("bool_list", ["yes", "no"]), ("bool_list", ["yes", "x"]),
    ("string_list", ["a", "b"]), ("string_list", "a"), ("ip_addr_list", ["1.2.3.4", "5.6.7.8"]),
    ("ip_addr_list", ["1.2.3.4", "x"]), ("force_list", "solo"), ("force_list", ["a"]),
    ("force_list(min=2)", "solo"), ("mixed_list('integer', 'string', 'boolean')", ["1", "x", "yes"]),
    ("mixed_list('integer', 'string')", ["1"]), ("mixed_list('integer')", ["1", "2"]),
    ("mixed_list('integer')", "7"), ("mixed_list('integer', 'nope')", ["1", "2"]),
    ("mixed_list(integer, float)", ["1", "2"]), ("mixed_list('ip_addr', 'float')", ["1.2.3.4", "x"]),
    ("option('a', 'b')", "a"), ("option('a', 'b')", "c"), ("option('a', 'b')", ["a"]),
    ("option(a, \"b c\", 'd,e')", "b c"), ("option(a, \"b c\", 'd,e')", "d,e"),
    ("pass", "anything"), ("", "blank"), ("pass(1)", "x"), ("nope", "1"), ("nope(1)", "1"),
    ("  integer", "1"), ("integer(default=3)", None), ("integer", None),
    ("string(default=None)", None), ("string(default='None')", None),
    ("string(default=\"None\")", None), ("integer(default=x)", None),
    ("list(default=list('a', 'b c', \"d\"))", None), ("list(default=list())", None),
    ("int_list(default=list(1, 2))", None), ("integer(default=4, min=5)", None),
    ("option('x', 'y', default='y')", None), ("string(default='it''s')", None),
    ("string(default=\"a, b\")", None), ("integer(default=1) # comment", None),
    ("integer(min=1,max=3)", "2"), ("integer( min = 1 , max = 3 )", "4"),
    ("string(default=list(a, b), min=1)", None), ("float(default=-1.5e3)", None),
    ("boolean(default=On)", None),
]
for spec, value in CHECKS:
    job("check", spec, json.dumps(value))
for spec in ["integer(default=3)", "string", "string(default=None)", "list(default=list(x))",
             "integer(default=abc)", "nope(default=1)"]:
    job("default", spec)

write("jobs.tsv", "\n".join(J) + "\n")
