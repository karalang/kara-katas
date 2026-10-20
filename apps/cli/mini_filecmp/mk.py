# Writes data/: jobs.tsv, the calls mini_filecmp runs, and trees/*.tsv,
# the directory trees those calls compare. Each tree line is
#   kind <TAB> path <TAB> mtime <TAB> body
# with kind f (a file whose body is the content, \n \t \\ escaped),
# d (a directory) or l (a symbolic link whose body is the target).
# Both oracle.py and mini_filecmp.kara build the trees under work/.
import os

FILES = {}
T0 = 1760000000


def esc(s):
    return s.replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")


def tree(name, *entries):
    lines = []
    for e in entries:
        kind, path = e[0], e[1]
        if kind == "f":
            body, mtime = e[2], e[3] if len(e) > 3 else T0
            lines.append(f"f\t{path}\t{mtime}\t{esc(body)}")
        elif kind == "d":
            lines.append(f"d\t{path}\t0\t")
        else:
            lines.append(f"l\t{path}\t0\t{e[2]}")
    FILES[f"trees/{name}.tsv"] = "\n".join(lines) + "\n"


INDEX = "<!doctype html>\n<title>Docs</title>\n<h1>Welcome</h1>\n"
CSS = "body { font-family: sans-serif; }\nh1 { color: #333; }\n"
APP_JS = "console.log('v1.4.2');\n"

# A docs site as built for release 1.4.2, and the copy on the server.
tree("release",
     ("f", "index.html", INDEX),
     ("f", "about.html", "<h1>About</h1>\n"),
     ("f", "style.css", CSS),
     ("f", "app.js", APP_JS),
     ("f", "robots.txt", "User-agent: *\nAllow: /\n"),
     ("f", "sitemap.xml", "<urlset>\n  <url>/index.html</url>\n</urlset>\n", T0 + 60),
     ("f", "changelog.txt", "1.4.2: fix search\n1.4.1: new theme\n"),
     ("f", "version.txt", "1.4.2\n"),
     ("f", "build-id", "abc123\n"),
     ("d", "img"),
     ("f", "img/logo.svg", "<svg>logo</svg>\n"),
     ("f", "img/banner.png", "PNG-banner-v2\n"),
     ("d", "api"),
     ("f", "api/index.html", "<h1>API</h1>\n"),
     ("d", "api/v1"),
     ("f", "api/v1/users.html", "<h1>Users</h1>\n"),
     ("f", "api/v1/orders.html", "<h1>Orders, v1.4</h1>\n"),
     ("d", "search"),
     ("f", "search/index.json", "{\"terms\": 412}\n"),
     ("f", "assets", "this is a file here\n"),
     ("d", ".git"),
     ("f", ".git/HEAD", "ref: refs/heads/main\n"),
     ("d", "__pycache__"),
     ("f", "__pycache__/build.cpython-313.pyc", "bytecode\n"),
     ("f", "tags", "index.html\t1\n"),
     ("f", "café.html", "<h1>Café</h1>\n"),
     ("l", "latest", "index.html"),
     ("l", "dangling", "missing-target.html"),
     ("d", "fonts"),
     ("f", "fonts/inter.woff2", "font-bytes\n"),
     )

tree("deployed",
     ("f", "index.html", INDEX),
     ("f", "about.html", "<h1>About</h1>\n", T0 + 3600),
     ("f", "style.css", CSS.replace("#333", "#444")),
     ("f", "app.js", "console.log('v1.4.1');\n"),
     ("f", "robots.txt", "User-agent: *\nAllow: /\n"),
     ("f", "sitemap.xml", "<urlset>\n  <url>/index.html</url>\n</urlset>\n", T0),
     ("f", "changelog.txt", "1.4.1: new theme\n"),
     ("f", "version.txt", "1.4.1\n"),
     ("f", "build-id", "abc999\n"),
     ("d", "img"),
     ("f", "img/logo.svg", "<svg>logo</svg>\n"),
     ("f", "img/banner.png", "PNG-banner-v1\n"),
     ("f", "img/old-logo.svg", "<svg>old</svg>\n"),
     ("d", "api"),
     ("f", "api/index.html", "<h1>API</h1>\n"),
     ("d", "api/v1"),
     ("f", "api/v1/users.html", "<h1>Users</h1>\n"),
     ("f", "api/v1/orders.html", "<h1>Orders, v1.3</h1>\n"),
     ("f", "api/v1/legacy.html", "<h1>Legacy</h1>\n"),
     ("d", "search"),
     ("f", "search/index.json", "{\"terms\": 398}\n"),
     ("d", "assets"),
     ("f", "assets/x.txt", "x\n"),
     ("d", ".git"),
     ("f", ".git/HEAD", "ref: refs/heads/prod\n"),
     ("f", "tags", "other\n"),
     ("f", "café.html", "<h1>Café</h1>\n"),
     ("f", "latest", INDEX),
     ("l", "dangling", "missing-target.html"),
     ("f", "error.log", "GET /x 500\n"),
     ("d", "uploads"),
     ("f", "uploads/avatar-1.png", "avatar\n"),
     ("l", "fonts", "../release/fonts"),
     )

# A small project for the sync program: the source and a stale mirror.
tree("src",
     ("f", "README.md", "# Tool\n\nUsage: tool run\n"),
     ("f", "setup.cfg", "[metadata]\nname = tool\nversion = 2.0\n"),
     ("f", "LICENSE", "MIT License\n"),
     ("d", "tool"),
     ("f", "tool/__init__.py", "__version__ = '2.0'\n"),
     ("f", "tool/cli.py", "def main():\n    print('run')\n"),
     ("f", "tool/util.py", "def clamp(x, lo, hi):\n    return max(lo, min(x, hi))\n"),
     ("d", "tool/plugins"),
     ("f", "tool/plugins/csv.py", "NAME = 'csv'\n"),
     ("f", "tool/plugins/json.py", "NAME = 'json'\n"),
     ("d", "docs"),
     ("f", "docs/index.md", "# Docs\n"),
     ("d", "tests"),
     ("f", "tests/test_cli.py", "def test_main():\n    pass\n"),
     )

tree("mirror",
     ("f", "README.md", "# Tool\n\nUsage: tool run\n"),
     ("f", "setup.cfg", "[metadata]\nname = tool\nversion = 1.9\n"),
     ("d", "tool"),
     ("f", "tool/__init__.py", "__version__ = '1.9'\n"),
     ("f", "tool/cli.py", "def main():\n    print('run')\n", T0 - 86400),
     ("f", "tool/old.py", "# removed in 2.0\n"),
     ("d", "tool/plugins"),
     ("f", "tool/plugins/csv.py", "NAME = 'csv'\n"),
     ("f", "tool/plugins/xml.py", "NAME = 'xml'\n"),
     ("d", "build"),
     ("f", "build/tool.whl", "wheel\n"),
     ("d", "build/lib"),
     ("f", "build/lib/cli.py", "old\n"),
     )

# Nightly backups: three days of a database dump directory.
tree("backup-mon",
     ("f", "users.sql", "INSERT INTO users VALUES (1,'ann');\n"),
     ("f", "orders.sql", "INSERT INTO orders VALUES (1,1,9.99);\n"),
     ("f", "audit.log", "mon\n"),
     )
tree("backup-tue",
     ("f", "users.sql", "INSERT INTO users VALUES (1,'ann');\n"),
     ("f", "orders.sql", "INSERT INTO orders VALUES (1,1,9.99);\n", T0 + 86400),
     ("f", "audit.log", "tue\n"),
     )
tree("backup-wed",
     ("f", "users.sql", "INSERT INTO users VALUES (1,'bob');\n"),
     ("f", "orders.sql", "INSERT INTO orders VALUES (1,1,9.99);\n", T0 + 172800),
     ("f", "audit.log", "wed\n", T0 + 172800),
     ("f", "payments.sql", "INSERT INTO payments VALUES (1);\n"),
     )

# Two empty directories, and one holding only ignored names.
tree("empty1")
tree("empty2", ("d", "CVS"), ("f", "CVS/Root", "x\n"), ("d", "RCS"))

J = []


def job(name, *lines):
    J.append("job\t" + name)
    J.extend(lines)


for t in ["release", "deployed", "src", "mirror", "backup-mon", "backup-tue",
          "backup-wed", "empty1", "empty2"]:
    J.append("build\t" + t)

job("cmp on single files",
    "cmp\trelease/index.html\tdeployed/index.html\tshallow",
    "cmp\trelease/about.html\tdeployed/about.html\tshallow",
    "cmp\trelease/style.css\tdeployed/style.css\tshallow",
    "cmp\trelease/style.css\tdeployed/style.css\tdeep",
    "cmp\trelease/app.js\tdeployed/app.js\tshallow",
    "cmp\trelease/version.txt\tdeployed/version.txt\tshallow",
    "cmp\trelease/build-id\tdeployed/build-id\tshallow",
    "cmp\trelease/build-id\tdeployed/build-id\tdeep",
    "cmp\trelease/changelog.txt\tdeployed/changelog.txt\tshallow",
    "cmp\trelease/latest\tdeployed/latest\tshallow",
    "cmp\trelease/latest\tdeployed/latest\tdeep",
    "cmp\trelease/img\tdeployed/img\tshallow",
    "cmp\trelease/assets\tdeployed/assets\tshallow",
    "cmp\trelease/dangling\tdeployed/dangling\tshallow",
    "cmp\trelease/nope.html\tdeployed/index.html\tshallow",
    "cmp\trelease/index.html\trelease/index.html\tdeep",
    "cmp\trelease/sitemap.xml\tdeployed/sitemap.xml\tshallow",
    )

job("the stat cache",
    "cmp\tbackup-mon/users.sql\tbackup-tue/users.sql\tdeep",
    "write\tbackup-tue/users.sql\tINSERT INTO users VALUES (1,'eve');\\n\t1760000000",
    "cmp\tbackup-mon/users.sql\tbackup-tue/users.sql\tdeep",
    "clear_cache",
    "cmp\tbackup-mon/users.sql\tbackup-tue/users.sql\tdeep",
    "write\tbackup-tue/users.sql\tINSERT INTO users VALUES (1,'ann');\\n\t1760000005",
    "cmp\tbackup-mon/users.sql\tbackup-tue/users.sql\tshallow",
    "cmp\tbackup-mon/users.sql\tbackup-tue/users.sql\tdeep",
    "write\tbackup-tue/users.sql\tINSERT INTO users VALUES (1,'ann');\\n\t1760000000",
    "cmp\tbackup-mon/users.sql\tbackup-tue/users.sql\tshallow",
    )

job("cmpfiles",
    "cmpfiles\trelease\tdeployed\tindex.html,style.css,app.js,img,latest,dangling,nope,café.html\tshallow",
    "cmpfiles\trelease\tdeployed\tindex.html,style.css,build-id,sitemap.xml\tdeep",
    "cmpfiles\tbackup-mon\tbackup-wed\tusers.sql,orders.sql,audit.log,payments.sql\tshallow",
    "cmpfiles\tbackup-mon\tbackup-tue\t\tshallow",
    )

job("dircmp attributes",
    "attrs\trelease\tdeployed\t-\t-\tshallow",
    "attrs\trelease/api\tdeployed/api\t-\t-\tdeep",
    "attrs\trelease\tdeployed\tCVS\t.,..,latest,dangling\tshallow",
    "attrs\tempty1\tempty2\t-\t-\tshallow",
    "attrs\tempty1\tempty2\t\t-\tshallow",
    )

job("reports",
    "report\trelease\tdeployed\t-\t-\tshallow",
    "report\trelease\tdeployed\t-\t-\tdeep",
    "partial\trelease\tdeployed\t-\t-\tshallow",
    "full\trelease\tdeployed\t-\t-\tdeep",
    "full\tsrc\tmirror\t-\t-\tshallow",
    "report\tempty1\tempty2\t-\t-\tshallow",
    "report\tbackup-mon\tbackup-mon\t-\t-\tshallow",
    "report\trelease\tno-such-dir\t-\t-\tshallow",
    "report\trelease/index.html\tdeployed\t-\t-\tshallow",
    )

job("python -m filecmp",
    "demo\trelease/api deployed/api",
    "demo\t-r release/api deployed/api",
    "demo\trelease/api",
    "demo\t-x release deployed",
    "demo\t-r -r backup-mon backup-wed",
    "demo\t--recursive release deployed",
    "demo\tbackup-mon backup-wed -r",
    )

for p in ["drift", "backups", "sync"]:
    J.append("program\t" + p)

FILES["jobs.tsv"] = "\n".join(J) + "\n"

for path, data in FILES.items():
    full = os.path.join("data", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="") as fp:
        fp.write(data)
