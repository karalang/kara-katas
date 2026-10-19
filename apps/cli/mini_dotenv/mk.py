# Writes data/: the .env files the jobs read and the job list.
import json, os

os.makedirs("data/env", exist_ok=True)
jobs = []


def job(**kw):
    jobs.append(kw)


def env_file(name, text, newline="\n"):
    b = text.replace("\n", newline).encode("utf-8")
    open("data/env/" + name, "wb").write(b)
    return "data/env/" + name


ENVIRON = {"HOME": "/home/ada", "USER": "ada", "LANG": "C.UTF-8", "DB_HOST": "db.internal", "PORT": "9000",
           "DEBUG": "", "STAGE": "prod"}

files = {}
files["app.env"] = '''# Settings for the web app. Copy to .env and edit.
SECRET_KEY=change-me-not-a-real-key
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1,.example.test

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME="shop"
DB_USER='shop_app'
DB_PASSWORD="p@ss word #1"   # quoted, so the hash stays
DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

export REDIS_URL=redis://${REDIS_HOST:-localhost}:6379/0
CACHE_TTL = 300
EMPTY=
EMPTY_QUOTED=""
NO_VALUE
GREETING="Hello,\\nWorld\\t!"
LITERAL='Hello,\\nWorld'
QUOTE_IN_SINGLE='it\\'s fine'
PATH_LIKE=C:\\Program Files\\App
MOTD="Welcome to the shop.
Mind the gap.
  -- the ops team"
UNICODE_NAME=Zoë Ångström
INLINE=value # a comment
HASH_IN_VALUE=abc#def
URL_WITH_FRAGMENT=https://example.test/page#top
'''
files["broken.env"] = '''GOOD=1
"BAD QUOTE=2
=nokey
KEY="unterminated
STILL_GOOD=3
TRAILING="ok" junk here
SPACE IN KEY=4
'SINGLE KEY'=5
''=6
LAST=end'''
files["tricky.env"] = '''export   EXPORTED=1
exportNOT=2
export=3
export
 indented=4
\tTABBED=5
KEY.WITH.DOTS=6
key-with-dashes=7
DUP=first
DUP=second
A=1;B=2
SP_BEFORE  =x
SP_AFTER=   y
TRAIL=z\x20\x20\x20
ESC_DQ="a \\"quoted\\" word"
ESC_BS="back\\\\slash"
ESC_ALL="\\a\\b\\f\\v\\r\\'\\\\"
NOT_ESC="\\u00e9 \\x41 \\0"
SQ_BS='one\\\\two \\n'
EQ_IN_VALUE=a=b=c
#COMMENTED=1
  # indented comment
VALUE_THEN_HASH="x"#y
'''
files["compose.env"] = '''COMPOSE_PROJECT_NAME=shop
IMAGE_TAG=${TAG:-latest}
REGISTRY=${REGISTRY:-registry.example.test}
IMAGE=${REGISTRY}/${COMPOSE_PROJECT_NAME}/web:${IMAGE_TAG}
WEB_PORT=${PORT}
UNSET_REF=${NOPE}
DEFAULT_EMPTY=${NOPE:-}
NESTED=${A:-${B}}
COLON_ONLY=${A:B}
EMPTY_NAME=${}
DOLLAR=$HOME and ${HOME}
SELF=${SELF:-start}-again
LATER=${DEFINED_BELOW}
DEFINED_BELOW=now
STAGE=${STAGE:-dev}
DEBUG=${DEBUG:-off}
'''
files["defaults.env"] = '''PORT=8000
WORKERS=2
LOG_LEVEL=info
FEATURE_X=off
'''
files["local.env"] = '''WORKERS=8
LOG_LEVEL=debug
FEATURE_X=on
EXTRA=${WORKERS}x
'''
files["empty.env"] = ""
files["comments.env"] = "# only\n# comments\n\n   \n"
for name, text in files.items():
    env_file(name, text)
env_file("crlf.env", "A=1\nB=\"two\nlines\"\n# c\nC='3'\n", "\r\n")
env_file("cr.env", "A=1\nB=2\nC=3\n", "\r")
open("data/env/bom.env", "wb").write("\ufeffBOM_KEY=1\nOTHER=2\n".encode("utf-8"))
open("data/env/nonl.env", "wb").write(b"FIRST=1\nSECOND=2")

# ---------------------------------------------------------------- jobs
all_files = sorted(os.listdir("data/env"))
for f in all_files:
    job(kind="parse", file="data/env/" + f)
for s in ["A=1\rB=2", "A=1\r\nB=2\r\n", "A='x\r\ny'\r\nB=2", "\r\n\r\nA=1", "A=\"1\\\"", "X=1\x0bY=2",
          "A=\u00a0b\u00a0 #c", "A=1\u2028B=2", "K \t=\t v", "'K'", "K=\"a\"\"b\"", "#!/bin/sh\nA=1"]:
    job(kind="parse_text", text=s)
for v in ["plain", "${A}", "x${A}y${B:-z}w", "${A:-}", "${:-d}", "${A:B}", "$A", "${A", "${A}}", "${A:-x:y}",
          "${A:-${B}}", "a${}b", "", "${A:-}${B:-b}"]:
    job(kind="vars", value=v)
for f in ["app.env", "compose.env", "tricky.env", "broken.env", "crlf.env", "bom.env"]:
    job(kind="values", file="data/env/" + f, interpolate=True, environ=ENVIRON)
job(kind="values", file="data/env/compose.env", interpolate=False, environ=ENVIRON)
job(kind="values", file="data/env/compose.env", interpolate=True, environ={})
job(kind="values", file="data/env/missing.env", interpolate=True, environ=ENVIRON)
job(kind="values_override", file="data/env/compose.env", override=False, environ=ENVIRON)
for ov in [False, True]:
    job(kind="load", files=["data/env/local.env", "data/env/defaults.env"], override=ov, environ=ENVIRON)
job(kind="load", files=["data/env/defaults.env", "data/env/local.env"], override=True, environ=ENVIRON, interpolate=False)
job(kind="load", files=["data/env/empty.env"], override=False, environ=ENVIRON)
job(kind="load", files=["data/env/tricky.env"], override=False, environ=ENVIRON)
for flag in ["1", "TRUE", "Yes", "y", "t", "0", "off", "", "nope"]:
    e = dict(ENVIRON)
    e["PYTHON_DOTENV_DISABLED"] = flag
    job(kind="load", files=["data/env/defaults.env"], override=False, environ=e)
job(kind="merge", files=["data/env/defaults.env", "data/env/local.env"], environ=ENVIRON)

# Editing: each script copies a file to data/work/ and runs operations on it.
job(kind="edit", start="data/env/app.env", ops=[
    ["set", "DEBUG", "false"],
    ["set", "DB_PASSWORD", "new 'pw' \\ here", "always"],
    ["get", "DB_PASSWORD"],
    ["set", "WORKERS", "4", "never"],
    ["set", "LOG_FORMAT", "json", "auto"],
    ["set", "TAGS", "a,b c", "auto"],
    ["set", "PI", "", "auto"],
    ["set", "NAME", "Zoë", "auto"],
    ["set", "PUBLIC_URL", "https://shop.example.test", "always", True],
    ["unset", "NO_VALUE"],
    ["unset", "MISSING_KEY"],
    ["get", "MISSING_KEY"],
    ["get", "NO_VALUE"],
    ["get", "MOTD"],
    ["set", "BAD", "x", "sometimes"],
])
job(kind="edit", start="data/env/nonl.env", ops=[["set", "THIRD", "3", "never"], ["set", "FIRST", "one", "never"]])
job(kind="edit", start="data/env/broken.env", ops=[["set", "GOOD", "11", "never"], ["unset", "LAST"]])
job(kind="edit", start="data/env/crlf.env", ops=[["set", "B", "2", "never"]])
job(kind="edit", start=None, ops=[["unset", "A"], ["set", "A", "1"], ["set", "B", "it's"], ["get", "B"], ["unset", "A"],
                                  ["unset", "B"], ["get", "B"]])
job(kind="edit", start="data/env/tricky.env", ops=[["set", "DUP", "third", "never"], ["unset", "DUP"], ["set", "export", "4", "never"]])

# The `dotenv` command line.
CLI = [
    ["-f", "data/env/app.env", "list"],
    ["-f", "data/env/compose.env", "list", "--format", "json"],
    ["-f", "data/env/app.env", "list", "--format=shell"],
    ["-f", "data/env/tricky.env", "list", "--format", "export"],
    ["-f", "data/env/app.env", "get", "DATABASE_URL"],
    ["-f", "data/env/app.env", "get", "EMPTY"],
    ["-f", "data/env/app.env", "get", "NOPE"],
    ["-f", "data/env/missing.env", "list"],
    ["-f", "data/env/missing.env", "get", "A"],
    ["--file", "data/work/cli.env", "set", "API_URL", "https://api.example.test/v1"],
    ["--file", "data/work/cli.env", "-q", "never", "set", "RETRIES", "3"],
    ["--file", "data/work/cli.env", "-q", "auto", "-e", "true", "set", "REGION", "eu west"],
    ["--file", "data/work/cli.env", "--quote=auto", "--export", "no", "set", "ZONE", "b"],
    ["--file", "data/work/cli.env", "list", "--format", "export"],
    ["--file", "data/work/cli.env", "unset", "RETRIES"],
    ["--file", "data/work/cli.env", "unset", "RETRIES"],
    ["--file", "data/work/cli.env", "list"],
    ["--version"],
    ["-f", "data/env/app.env", "list", "--format", "xml"],
    ["-f", "data/env/app.env", "-q", "sometimes", "list"],
    ["-f", "data/env/app.env", "get"],
    ["-f", "data/env/app.env", "-e", "maybe", "list"],
    ["-f", "data/env/app.env", "frobnicate"],
]
for args in CLI:
    job(kind="cli", args=args, environ=ENVIRON)

with open("data/jobs.jsonl", "w") as out:
    for j in jobs:
        out.write(json.dumps(j) + "\n")
print(len(jobs), "jobs")
