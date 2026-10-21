# The TOML files mk.py writes to data/docs/: the kind a project keeps in
# its repository and a service keeps in /etc, written the way people
# write them, with comments, odd spacing and the less common syntax.

DOCS = {}

DOCS["pyproject"] = '''\
# Packaging for the "inkwell" project.
[build-system]
requires = ["poetry-core>=1.8"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "inkwell"
version = "2.3.1"   # bumped by the release script
description = "Render Markdown notebooks to static sites"
authors = ["Ada Byron <ada@example.org>", "Grace H. <grace@example.org>"]
license = "MIT"
readme = "README.md"
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",  # keep sorted
    "Topic :: Text Processing :: Markup",
]
packages = [{ include = "inkwell", from = "src" }]

[tool.poetry.dependencies]
python = "^3.9"
markdown-it-py = { version = "^3.0", extras = ["linkify"] }
jinja2 = "^3.1"
watchdog = { version = ">=3.0", optional = true }

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-cov = "^5.0"
ruff = "0.4.4"

[tool.poetry.extras]
watch = ["watchdog"]

[tool.poetry.scripts]
inkwell = "inkwell.cli:main"

[tool.ruff]
line-length = 100
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "I", "B"]
ignore = [] # nothing yet

[tool.pytest.ini_options]
addopts = "-ra --strict-markers"
testpaths = [
  "tests",
]
'''

DOCS["cargo"] = '''\
[package]
name = "ferrite"
version = "0.9.4"
edition = "2021"
rust-version = "1.74"
authors = ["The Ferrite Developers"]
description = "A tiny embedded key-value store"
keywords = ["kv", "embedded", "storage"]
categories = ["database-implementations"]

[dependencies]
serde = { version = "1.0", features = ["derive"] }
crc32fast = "1.4"
memmap2 = { version = "0.9", optional = true }
log = "0.4"

[dev-dependencies]
tempfile = "3"
proptest = { version = "1.4", default-features = false, features = ["std"] }

[features]
default = ["mmap"]
mmap = ["dep:memmap2"]

[profile.release]
lto = true
codegen-units = 1
opt-level = 3
debug = false

[[bin]]
name = "ferrite-cli"
path = "src/bin/cli.rs"

[[bin]]
name = "ferrite-bench"
path = "src/bin/bench.rs"
required-features = ["mmap"]

[[example]]
name = "basic"
'''

DOCS["workspace"] = '''\
[workspace]
resolver = "2"
members = [
    "crates/core",
    "crates/cli",
    "crates/server",
]
exclude = ["crates/experimental"]

[workspace.package]
version = "1.4.0"
edition = "2021"
license = "Apache-2.0 OR MIT"

[workspace.dependencies]
tokio = { version = "1.37", features = ["rt-multi-thread", "macros"] }
tracing = "0.1"
anyhow = "1"
'''

DOCS["spec"] = '''\
# This is a TOML document

title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00

[database]
enabled = true
ports = [ 8000, 8001, 8002 ]
data = [ ["delta", "phi"], [3.14] ]
temp_targets = { cpu = 79.5, case = 72.0 }

[servers]

[servers.alpha]
ip = "10.0.0.1"
role = "frontend"

[servers.beta]
ip = "10.0.0.2"
role = "backend"
'''

DOCS["netlify"] = '''\
[build]
  base = "site/"
  publish = "public/"
  command = "hugo --gc --minify"

  [build.environment]
    HUGO_VERSION = "0.125.4"
    NODE_ENV = "production"

[context.deploy-preview]
  command = "hugo --buildDrafts --buildFuture -b $DEPLOY_PRIME_URL"

[[redirects]]
  from = "/blog/*"
  to = "/posts/:splat"
  status = 301
  force = false

[[redirects]]
  from = "/api/*"
  to = "https://api.example.net/:splat"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    Content-Security-Policy = "default-src 'self'"
'''

DOCS["hugo"] = '''\
baseURL = "https://notes.example.com/"
languageCode = "en-us"
title = "Field Notes"
theme = "paper"
paginate = 10

[params]
  author = "R. Okafor"
  description = "Notes from the field"
  showReadingTime = true
  [params.social]
    github = "rokafor"
    mastodon = "@rok@hachyderm.io"

[[menu.main]]
  name = "Posts"
  url = "/posts/"
  weight = 1

[[menu.main]]
  name = "Tags"
  url = "/tags/"
  weight = 2

[languages]
  [languages.en]
    languageName = "English"
    weight = 1
  [languages.fr]
    languageName = "Fran\\u00e7ais"
    title = "Carnets de terrain"
    weight = 2

[markup.goldmark.renderer]
  unsafe = false
'''

DOCS["alacritty"] = '''\
# Alacritty terminal configuration
live_config_reload = true

[window]
padding = { x = 6, y = 6 }
opacity = 0.95
decorations = "Buttonless"
dimensions.columns = 120
dimensions.lines = 36

[font]
size = 13.5
normal = { family = "JetBrains Mono", style = "Regular" }
bold.family = "JetBrains Mono"
bold.style = "Bold"

[colors.primary]
background = "#1d1f21"
foreground = "#c5c8c6"

[colors.normal]
black   = "#1d1f21"
red     = "#cc6666"
green   = "#b5bd68"

[[keyboard.bindings]]
key = "N"
mods = "Command"
action = "SpawnNewInstance"

[[keyboard.bindings]]
key = "Return"
mods = "Command|Shift"
action = "ToggleFullscreen"
'''

DOCS["outoforder"] = '''\
# Tables of one parent spread through the file, as TOML allows.
[fruit.apple]
color = "red"

[animal]
legs = 4

[fruit.orange]
color = "orange"

[fruit.apple.texture]
smooth = true
'''

DOCS["dotted"] = '''\
name = "Orange"
physical.color = "orange"
physical.shape = "round"
site."google.com" = true
3.14159 = "pi"
"ʎǝʞ" = "value"
'key2' = "literal key"
a . b . c = 1   # spaces around the dots
"" = "empty quoted key"

[tool]
lint.enabled = true
lint.rules = ["E1", "W2"]
'''

DOCS["strings"] = r'''str1 = "I'm a string. \"You can quote me\". Name\tJos\u00E9\nLocation\tSF."
str2 = """
Roses are red
Violets are blue"""
str3 = """\
       The quick brown \
       fox jumps over \
       the lazy dog.\
       """
str4 = """Here are two quotation marks: "". Simple enough."""
str5 = """Here are fifteen quotation marks: ""\"""\"""\"""\"""\"."""
str6 = """"This," she said, "is just a pointless statement.""""
winpath  = 'C:\Users\nodejs\templates'
quoted   = 'Tom "Dubs" Preston-Werner'
regex    = '<\i\c*\s*>'
regex2 = QQQI [dw]on't need \d{2} applesQQQ
lines  = QQQ
The first newline is
trimmed in raw strings.
   All other whitespace
   is preserved.
QQQ
quot15 = QQQHere are fifteen quotation marks: """""""""""""""QQQ
apos15 = "Here are fifteen apostrophes: QQQQQQQQQQQQQQQ"
emoji = "\U0001F600 and \u00e9"
empty = ""
empty_lit = ''
'''.replace("QQQ", "'" * 3)

DOCS["numbers"] = '''\
int1 = +99
int2 = 42
int3 = 0
int4 = -17
int5 = 1_000
int6 = 5_349_221
int7 = 53_49_221
hex1 = 0xDEADBEEF
hex2 = 0xdead_beef
oct1 = 0o01234567
oct2 = 0o755
bin1 = 0b11010110
flt1 = +1.0
flt2 = 3.1415
flt3 = -0.01
flt4 = 5e+22
flt5 = 1e06
flt6 = -2E-2
flt7 = 6.626e-34
flt8 = 224_617.445_991_228
sf1 = inf
sf2 = +inf
sf3 = -inf
sf4 = nan
sf5 = +nan
sf6 = -nan
zero = -0.0
big = 1e400
odd = +infinity
'''

DOCS["dates"] = '''\
odt1 = 1979-05-27T07:32:00Z
odt2 = 1979-05-27T00:32:00-07:00
odt3 = 1979-05-27T00:32:00.999999-07:00
odt4 = 1979-05-27 07:32:00Z
ldt1 = 1979-05-27T07:32:00
ldt2 = 1979-05-27T00:32:00.999999
ld1 = 1979-05-27
lt1 = 07:32:00
lt2 = 00:32:00.999999
nanos = 2024-02-29T12:00:00.123456789Z
lower = 2024-01-02t03:04:05z
spaced = 2024-03-10   # a date, then a comment
pipe = 2024-03-10T08:00:00|05:30
dates = [ 2024-01-01 , 2024-06-30 ]
'''

DOCS["crlf"] = (
    '# saved on Windows\r\n'
    '[server]\r\n'
    'host = "0.0.0.0"\r\n'
    'port = 8080\r\n'
    '\r\n'
    '[server.tls]\r\n'
    'enabled = false # off in dev\r\n'
    'ciphers = [\r\n'
    '  "TLS_AES_128_GCM_SHA256",\r\n'
    ']\r\n'
)

DOCS["arrays"] = '''\
integers = [ 1, 2, 3 ]
colors = [ "red", "yellow", "green" ]
nested_arrays_of_ints = [ [ 1, 2 ], [3, 4, 5] ]
nested_mixed_array = [ [ 1, 2 ], ["a", "b", "c"] ]
string_array = [ "all", 'strings', """are the same""", \'\'\'type\'\'\' ]
numbers = [ 0.1, 0.2, 0.5, 1, 2, 5 ]
contributors = [
  "Foo Bar <foo@example.com>",
  { name = "Baz Qux", email = "bazqux@example.com", url = "https://example.com/bazqux" }
]
integers2 = [
  1, 2, 3
]
integers3 = [
  1,
  2, # this is ok
]
empty = []
empty_ws = [ ]
commented = [ # opening
  "x", # first
  # alone
  "y"
] # after
'''

DOCS["service"] = '''\
# orders-api: production settings
version = 1
log_level = "info"
log_format = "json"  # json or text

[server]
host = "0.0.0.0"
port = 8443
workers = 8
read_timeout = "15s"

[database]
url = "postgres://orders@db.internal:5432/orders"
pool_size = 20
# Statement timeout in milliseconds.
statement_timeout = 5000

[cache]
backend = "redis"
url = "redis://cache.internal:6379/2"
ttl = 300

[[upstreams]]
name = "payments"
url = "https://payments.internal"
retries = 3

[[upstreams]]
name = "inventory"
url = "https://inventory.internal"
retries = 1
'''

# --- the release program's repository -------------------------------------

REPO = {}

REPO["release.toml"] = '''\
# What the next release changes. Read by scripts/release.
[release]
version = "1.5.0"
date = 2024-06-01
notes = "Faster compaction and a new repair command."
# Crates released together; a path dependency on one of them follows
# the new version.
crates = ["ferrite-core", "ferrite", "ferrite-repair"]

[[release.files]]
path = "Cargo.toml"
kind = "cargo-workspace"

[[release.files]]
path = "crates/core/Cargo.toml"
kind = "cargo"

[[release.files]]
path = "crates/cli/Cargo.toml"
kind = "cargo"

[[release.files]]
path = "python/pyproject.toml"
kind = "poetry"

[[release.files]]
path = "python/ferrite-py/pyproject.toml"
kind = "pep621"
'''

REPO["Cargo.toml"] = '''\
[workspace]
resolver = "2"
members = ["crates/core", "crates/cli"]

[workspace.package]
version = "1.4.0"
edition = "2021"
license = "MIT OR Apache-2.0"
repository = "https://git.example.org/ferrite"

[workspace.dependencies]
ferrite-core = { path = "crates/core", version = "1.4.0" }
serde = { version = "1.0.197", features = ["derive"] }
clap = "4.5"
'''

REPO["crates/core/Cargo.toml"] = '''\
[package]
name = "ferrite-core"
version.workspace = true
edition.workspace = true
license.workspace = true

[dependencies]
serde.workspace = true
crc32fast = "1.4"

[dev-dependencies]
ferrite-testkit = { path = "../testkit", version = "0.3" }
'''

REPO["crates/cli/Cargo.toml"] = '''\
[package]
name = "ferrite"
version = "1.4.0" # keep in step with the workspace
edition = "2021"
description = "Command-line tool for ferrite stores"

[[bin]]
name = "ferrite"
path = "src/main.rs"

[dependencies]
ferrite-core = { path = "../core", version = "=1.4.0" }
clap = { workspace = true }

[dependencies.ferrite-repair]
path = "../repair"
version = "~1.4"
optional = true
'''

REPO["python/pyproject.toml"] = '''\
[tool.poetry]
name = "ferrite-tools"
version = "1.4.0"
description = "Python helpers for ferrite stores"
authors = ["The Ferrite Developers"]

[tool.poetry.dependencies]
python = "^3.10"
'''

REPO["python/ferrite-py/pyproject.toml"] = '''\
[build-system]
requires = ["maturin>=1.5,<2.0"]
build-backend = "maturin"

[project]
name = "ferrite-py"
version = "1.4.0"
requires-python = ">=3.9"
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: Implementation :: CPython",
]
'''

REPO["CHANGELOG.toml"] = '''\
# Release history, newest first.

[[releases]]
version = "1.4.0"
date = 2024-03-12
notes = "Memory-mapped reads."

[[releases]]
version = "1.3.2"
date = 2024-01-20
notes = "Fix a crash on empty logs."
'''

# --- the migrate program's service configs ---------------------------------

ETC = {}

ETC["orders-api.toml"] = DOCS["service"]

ETC["billing-worker.toml"] = (
    '# billing-worker\r\n'
    'version = 1\r\n'
    'log_level = "warn"\r\n'
    '\r\n'
    '[server]\r\n'
    'port = 9100\r\n'
    'shutdown_timeout = "1m30s"\r\n'
    '\r\n'
    '[[upstreams]]\r\n'
    'name = "ledger"\r\n'
    'url = "https://ledger.internal"\r\n'
    'retries = 5\r\n'
)

ETC["search-api.toml"] = '''\
schema = 2

[logging]
level = "info"

[server]
port = 8080
'''

ETC["notifier.toml"] = '''\
version = 1
# Verbose while we chase the duplicate-email bug.
log_level = "debug"
log_format = "text"

[server]
host = "127.0.0.1"
port = 7000
tls = { cert = "/etc/notifier/cert.pem", key = "/etc/notifier/key.pem" }
read_timeout = "250ms"
idle_timeout = "2m"
max_body = "1MB"

[smtp]
relay = "mail.internal"
port = 25
'''
