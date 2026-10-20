# Writes data/ for mini_pygments: source files to highlight, the jobs
# that drive the highlighter, and a small docs site with fenced code.
import os

FILES = {}

FILES["src/inventory.py"] = '''#!/usr/bin/env python3
"""Inventory service: stock levels and reorder rules."""
from __future__ import annotations

import dataclasses as dc
from collections import defaultdict
from typing import Iterator, Optional

MAX_ITEMS = 1_000
RATE = 0x1F + 0o17 + 0b1010
SCALE = 1.5e-3 + 2j


@dc.dataclass(frozen=True)
class Item:
    sku: str
    qty: int = 0
    café: float = 0.0  # unicode name

    def __repr__(self) -> str:
        return f"Item({self.sku!r}, qty={self.qty:>4d}, {{literal}})"


class Inventory(dict):
    def restock(self, sku, n=1, *args, **kw):
        # TODO: validate n; FIXME negative stock
        if (old := self.get(sku)) is None and n > 0:
            self[sku] = n
        elif not isinstance(n, int):
            raise TypeError("n must be an int, not %s" % type(n).__name__)
        else:
            self[sku] = old + n
        return self[sku]

    async def watch(self) -> Iterator[str]:
        async for event in self.events():
            await event.ack()
            yield event.sku

    def summary(self):
        match self.status:
            case {"state": "ok", **rest}:
                return rb"raw\\bytes" + b'\\x00'
            case [first, *_] if first > 0:
                return lambda x: x ** 2
            case _:
                pass
        print(len(self), sorted(self), sep="\\t", end='')
        return u\'\'\'multi
line\'\'\'


def _private(a, /, b, *, c): return a @ b if c else NotImplemented
'''

FILES["src/deploy.sh"] = '''#!/bin/bash
# Deploy the service to every host in $HOSTS.
set -euo pipefail

readonly APP="inventory"
declare -a HOSTS=(web1 web2 "web 3")
LOG_DIR=${LOG_DIR:-/var/log/$APP}

log() {
    local level=$1; shift
    echo "[$(date +%H:%M:%S)] ${level}: $*" >&2
}

for host in "${HOSTS[@]}"; do
    if ! ssh -o ConnectTimeout=5 "$host" true; then
        log WARN "skipping $host"
        continue
    fi
    count=$(( count + 1 ))
    scp ./build/${APP}.tar.gz "$host":/tmp/ && \\
        ssh "$host" 'tar -xzf /tmp/inventory.tar.gz -C /opt'
done

case "$1" in
    start|restart) systemctl "$1" "$APP" ;;
    stop) systemctl stop "$APP" ;;
    *) echo "usage: $0 {start|stop}" ; exit 2 ;;
esac

cat <<EOF > /etc/motd
Deployed $APP at `date`
EOF
echo $((16#ff)) $? $# ~/bin
'''

FILES["src/settings.ini"] = '''; Service settings
# a hash comment too
[server]
host = 0.0.0.0
port=8080
debug : false

[database]
url = "postgres://db:5432/inventory"
pool size = 10
  continued line
[empty]
'''

FILES["src/fix.diff"] = '''diff --git a/inventory.py b/inventory.py
index 3b18e51..a9c2f7d 100644
--- a/inventory.py
+++ b/inventory.py
@@ -10,7 +10,8 @@ class Inventory(dict):
     def restock(self, sku, n=1):
-        self[sku] = self.get(sku, 0) + n
+        if n <= 0:
+            raise ValueError(n)
+        self[sku] = self.get(sku, 0) + n
         return self[sku]
Only in b: NEWS
! changed line
'''

FILES["src/Cargo.toml"] = '''# Package manifest
[package]
name = "inventory"
version = "0.3.1"
edition = '2021'
authors = ["Ana <ana@example.com>", """Bo"""]
publish = false

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio.version = "1.38"
"quoted.key" = 1_000
hex = 0xDEAD_beef
float = -3.25e+2
inf = inf
released = 1979-05-27T07:32:00Z
local = 07:32:00

[[bin]]
name = "inv"
path = "src/main.rs"
literal = \'\'\'
C:\\Users\\nodejs
\'\'\'
'''

FILES["src/nginx.conf"] = '''user www-data;
worker_processes auto;

http {
    include       mime.types;
    # upstream pool
    upstream app {
        server 127.0.0.1:8080 weight=3;
        server unix:/run/app.sock backup;
    }
    server {
        listen 443 ssl http2;
        server_name example.com *.example.com;
        location ~* \\.(png|jpg)$ {
            expires 30d;
            add_header Cache-Control "public";
        }
        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            return 301 https://$host$request_uri;
        }
    }
}
'''

FILES["src/site.css"] = '''@charset "utf-8";
@import url("reset.css") screen;

/* Layout */
:root { --accent: #0a7; }
body, html {
    margin: 0;
    font: 16px/1.5 "Helvetica Neue", Arial, sans-serif;
    color: rgba(20, 20, 20, .9);
}
a:hover > .icon::before { content: "\\2192"; }
#main .card[data-kind="note"] {
    width: calc(100% - 2em);
    background: url(img/bg.png) no-repeat #fff !important;
    transition: opacity 0.3s ease-in-out;
}
@media (max-width: 600px) and (orientation: portrait) {
    .card { display: none; z-index: -1; }
}
@keyframes fade { from { opacity: 0 } to { opacity: 1 } }
'''

FILES["src/report.sql"] = '''-- Monthly stock report
WITH moves AS (
    SELECT sku, SUM(qty) AS total, COUNT(*) n
    FROM stock_moves
    WHERE moved_at >= DATE '2024-01-01' AND note NOT LIKE '%test%'
    GROUP BY sku
)
select i.sku, i.name, coalesce(m.total, 0) as total
from items i left outer join moves m on m.sku = i.sku
where i.price between 1.5 and 1e3 or i.name = 'O''Brien'
order by total desc limit 10;
/* multi
   line */ INSERT INTO audit VALUES (1, "x", NULL);
'''

FILES["src/Dockerfile"] = '''# syntax=docker/dockerfile:1
FROM python:3.13-slim AS base
ARG VERSION=0.3.1
ENV APP_HOME=/opt/app \\
    PYTHONUNBUFFERED=1
WORKDIR $APP_HOME
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \\
    rm -rf /root/.cache
RUN ["python", "-m", "compileall", "."]
EXPOSE 8080/tcp
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8080/health || exit 1
CMD ["gunicorn", "app:app"]
'''

FILES["src/main.go"] = '''// Package main serves the inventory API.
package main

import (
	"fmt"
	"net/http"
)

type Item struct {
	SKU string `json:"sku"`
	Qty int    `json:"qty"`
}

const maxItems = 1 << 10

func (i *Item) String() string {
	return fmt.Sprintf("%s:%d", i.SKU, i.Qty)
}

func main() {
	items := map[string]*Item{}
	var count uint64 = 0x10
	r := 'x'
	go func() { count++ }()
	http.HandleFunc("/items", func(w http.ResponseWriter, req *http.Request) {
		for k, v := range items {
			fmt.Fprintln(w, k, v, r, 3.14e2, 1i)
		}
	})
	defer fmt.Println(`raw
string`)
	if err := http.ListenAndServe(":8080", nil); err != nil {
		panic(err)
	}
}
'''

FILES["src/lib.rs"] = '''//! Inventory core.
use std::collections::HashMap;

/// A stock-keeping unit.
#[derive(Debug, Clone, PartialEq)]
pub struct Item<'a> {
    pub sku: &'a str,
    qty: u32,
}

pub enum Event { Added(u32), Removed { qty: u32 }, Reset }

impl<'a> Item<'a> {
    pub const MAX: u32 = 1_000;

    pub fn new(sku: &'a str) -> Self {
        Item { sku, qty: 0 }
    }

    pub fn apply(&mut self, e: &Event) -> Result<u32, String> {
        match *e {
            Event::Added(n) if n > 0 => self.qty += n,
            Event::Removed { qty } => self.qty = self.qty.checked_sub(qty).ok_or("underflow")?,
            _ => return Err(format!("bad event {:?}", e)),
        }
        let c = b'x'; let s = r#"raw "str""#; let f = 2.5e-3_f64;
        println!("{} {} {}", c, s, f);
        Ok(self.qty)
    }
}

/* block /* nested */ comment */
fn count(m: &HashMap<String, Vec<i64>>) -> usize { m.values().map(|v| v.len()).sum() }
'''

FILES["src/app.js"] = '''// Front-end for the inventory API
'use strict';
import { render } from './view.js';

const API = "/api/items";
let cache = new Map();

export default class Store extends EventTarget {
    #token = null;

    constructor(base = API) {
        super();
        this.base = base;
    }

    async load(sku) {
        if (cache.has(sku)) return cache.get(sku);
        const res = await fetch(`${this.base}/${encodeURIComponent(sku)}?v=${1 + 2}`);
        const data = await res.json();
        cache.set(sku, data);
        return data;
    }
}

const isSku = /^[A-Z]{3}-\\d+$/i.test(input) && input.length !== 0;
const total = items.reduce((acc, { qty }) => acc + qty, 0) ?? 0;
var x = 0xff, y = 1e-3, z = 10n;
/* done */
render(document.querySelector('#app'), { total, isSku });
'''

FILES["src/inventory.service"] = '''[Unit]
Description=Inventory API
After=network-online.target
Wants=network-online.target

# runtime
[Service]
Type=simple
ExecStart=/usr/bin/inventory --port 8080 \\
    --workers 4
Restart=on-failure
Environment="MODE=prod" LANG=C.UTF-8
; legacy comment

[Install]
WantedBy=multi-user.target
'''

FILES["src/messages.properties"] = '''# Messages
! bang comment
greeting = Hello, {0}!
farewell: Goodbye
key\\ with\\ spaces = value
multi = first \\
        second
empty=
unicode=caf\\u00e9
'''

FILES["src/feed.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE feed>
<!-- Atom feed for the changelog -->
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">
  <title type="text">Inventory &amp; Stock</title>
  <entry id='1'>
    <summary><![CDATA[<b>bold</b> & raw]]></summary>
    <link href="https://example.com/1"/>
  </entry>
</feed>
'''

FILES["src/index.html"] = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Inventory</title>
  <style>
    body { margin: 0; color: #333; }
  </style>
  <script type="text/javascript">
    const n = 1; if (n < 2) { console.log("ok"); }
  </script>
</head>
<body class="main" data-x=3>
  <!-- the app root -->
  <div id="app">Loading&hellip;</div>
  <input disabled>
</body>
</html>
'''

FILES["src/crash.pytb"] = '''Traceback (most recent call last):
  File "/opt/app/inventory.py", line 42, in restock
    self[sku] = old + n
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
'''

FILES["src/stock.c"] = '''#include <stdio.h>
#include "stock.h"
#define MAX_SKU 64
#ifndef NDEBUG
#  define LOG(x) fprintf(stderr, "%s\\n", x)
#endif

/* A stock record. */
typedef struct {
    char sku[MAX_SKU];
    uint32_t qty;
    size_t refs;
} stock_t;

static const char *names[] = { "a", "b", NULL };

int restock(stock_t *s, int n) {
    if (s == NULL || n <= 0) return -1;
    s->qty += (uint32_t)n; // add
    switch (n) {
    case 1: break;
    default: goto out;
    }
out:
    return 'x' + 0x10 + 1.5f + 07 + 10UL;
}
'''

FILES["src/items.json"] = '''{
  "items": [
    {"sku": "ABC-1", "qty": 12, "price": 9.95, "tags": ["new", "sale"]},
    {"sku": "XYZ-\\u00e9", "qty": -3, "price": 1.2e3, "active": true},
    {"sku": "Q\\"T", "qty": 0, "note": null, "ok": false}
  ],
  // comments are allowed
  /* block
     comment */ "count": 3,
  "bad": @
}
'''

FILES["src/notes.txt"] = '''Plain text notes.
	Tabbed line with <angle> & "quotes".
'''

FILES["src/bad.py"] = '''def broken(:
    x = "unterminated
    y = 1 $ 2
\treturn ?
'''

FILES["src/svc.py"] = '''class Shelf:
    """One shelf of stock."""

    def take(self, sku, n=1):
        # TODO: lock the shelf first
        left = self.qty.get(sku, 0) - n
        if left < 0:  # FIXME: raise instead
            print(f"short on {sku!r}")
        return max(left, 0)  # NOTE: never negative
'''

FILES["src/tabs.py"] = '''if True:
\tx = 1\t# tab
\t\ty = "a\tb"
'''

FILES["src/crlf.ini"] = "[a]\r\nk = v\r\n\r\n\r\n"

FILES["src/blank.py"] = "\n\n\nx = 1\n\n\n"

# ---------------------------------------------------------------- jobs
# Each job line: kind|lexer|lexer options|filters|formatter|formatter options|input
# kind is one of: lex (lexer by alias), file (lexer chosen by file name),
# mime (lexer by mimetype). Filters are ';'-separated name:opt=v,opt=v.
J = []


def job(kind, lexer, lopts, filters, fmt, fopts, src):
    J.append("|".join([kind, lexer, lopts, filters, fmt, fopts, src]))


for alias, src in [
    ("python", "inventory.py"), ("bash", "deploy.sh"), ("ini", "settings.ini"),
    ("diff", "fix.diff"), ("toml", "Cargo.toml"), ("nginx", "nginx.conf"),
    ("css", "site.css"), ("sql", "report.sql"), ("docker", "Dockerfile"),
    ("go", "main.go"), ("rust", "lib.rs"), ("javascript", "app.js"),
    ("systemd", "inventory.service"), ("properties", "messages.properties"),
    ("xml", "feed.xml"), ("html", "index.html"), ("pytb", "crash.pytb"),
    ("c", "stock.c"), ("json", "items.json"), ("text", "notes.txt"),
    ("python", "bad.py"),
]:
    job("lex", alias, "", "", "raw", "", src)

# lookups by file name and mimetype
for src in ["inventory.py", "deploy.sh", "Cargo.toml", "Dockerfile", "items.json", "site.css",
            "stock.c", "inventory.service"]:
    job("file", src, "", "", "-", "", src)
job("mime", "text/x-python", "", "", "raw", "", "blank.py")
job("mime", "application/json", "", "", "raw", "", "items.json")
job("mime", "text/x-nothing", "", "", "raw", "", "blank.py")
job("lex", "PYTHON3", "", "", "raw", "", "blank.py")
job("lex", "cobol-free", "", "", "raw", "", "blank.py")
job("lex", "nosuchlang", "", "", "raw", "", "blank.py")
job("file", "unknown.xyz", "", "", "raw", "", "blank.py")

# lexer options
job("lex", "python", "", "", "raw", "", "blank.py")
job("lex", "python", "stripnl=false", "", "raw", "", "blank.py")
job("lex", "python", "stripall=yes", "", "raw", "", "blank.py")
job("lex", "python", "ensurenl=0,stripnl=off", "", "raw", "", "blank.py")
job("lex", "python", "tabsize=4", "", "raw", "", "tabs.py")
job("lex", "ini", "", "", "raw", "", "crlf.ini")
job("lex", "python", "stripnl=maybe", "", "raw", "", "blank.py")
job("lex", "python", "tabsize=four", "", "raw", "", "tabs.py")
job("lex", "c", "stdlibhighlighting=false,c99highlighting=no", "", "raw", "", "stock.c")

# filters
job("lex", "python", "", "keywordcase:case=upper", "raw", "", "tabs.py")
job("lex", "sql", "", "keywordcase:case=capitalize", "raw", "", "report.sql")
job("lex", "python", "", "keywordcase:case=title", "raw", "", "tabs.py")
job("lex", "python", "", "codetagify", "raw", "", "svc.py")
job("lex", "python", "", "codetagify:codetags=FIXME NOTE", "raw", "", "svc.py")
job("lex", "python", "", "highlight:names=self sku print", "raw", "", "svc.py")
job("lex", "python", "", "highlight:names=x y,tokentype=Name.Variable.Magic", "raw", "", "tabs.py")
job("lex", "python", "", "whitespace:spaces=true,tabs=true,newlines=true", "raw", "", "tabs.py")
job("lex", "python", "", "whitespace:spaces=_,tabs=>,tabsize=3,wstokentype=false", "raw", "", "tabs.py")
job("lex", "python", "", "gobble:n=2", "raw", "", "tabs.py")
job("lex", "python", "", "tokenmerge", "raw", "", "svc.py")
job("lex", "python", "", "gobble:n=1;tokenmerge;keywordcase:case=upper", "raw", "", "tabs.py")
job("lex", "python", "", "nosuchfilter", "raw", "", "tabs.py")
job("lex", "python", "", "raiseonerror", "raw", "", "tabs.py")
job("lex", "python", "", "raiseonerror", "raw", "", "bad.py")

# formatters
job("lex", "python", "", "", "html", "", "svc.py")
job("lex", "python", "", "", "html", "linenos=table,hl_lines=3 5 99,linenostart=10,linenostep=2,linenospecial=4", "tabs.py")
job("lex", "bash", "", "", "html", "linenos=inline,anchorlinenos=true,lineanchors=ln,cssclass=code", "deploy.sh")
job("lex", "c", "", "", "html", "nowrap=true", "stock.c")
job("lex", "json", "", "", "html", "noclasses=true,style=monokai,hl_lines=2", "items.json")
job("lex", "css", "", "", "html", "wrapcode=true,linespans=L,classprefix=pg-,filename=site.css", "site.css")
job("lex", "diff", "", "", "html", "full=true,title=The fix,style=friendly", "fix.diff")
job("lex", "html", "", "", "html", "noclasses=yes,nobackground=1,prestyles=margin: 0,cssstyles=border: 1px", "index.html")
job("lex", "python", "", "", "html", "linenos=1,filename=bad.py,noclasses=true", "bad.py")
job("lex", "python", "", "", "html", "debug_token_types=true", "tabs.py")
job("lex", "python", "", "", "terminal", "", "svc.py")
job("lex", "rust", "", "", "terminal", "bg=dark,linenos=true", "lib.rs")
job("lex", "diff", "", "", "console", "", "fix.diff")
job("lex", "python", "", "", "terminal", "bg=sepia", "tabs.py")
job("lex", "go", "", "", "testcase", "", "main.go")
job("lex", "python", "", "", "tokens", "", "tabs.py")
job("lex", "python", "", "", "text", "", "tabs.py")
job("lex", "python", "", "", "nosuchfmt", "", "tabs.py")
job("lex", "python", "", "", "html", "style=nosuchstyle", "tabs.py")
job("lex", "python", "", "", "html", "linenostart=x", "tabs.py")
job("lex", "python", "", "", "raw", "compress=zip", "tabs.py")

# style definitions: style|selector|formatter options
S = []
for style, arg, opts in [
    ("default", ".highlight", ""),
    ("default", "", ""),
    ("monokai", ".code pre", "nobackground=true"),
    ("friendly", "", "cssclass=src"),
    ("emacs", ".a, .b", "classprefix=x-"),
    ("solarized-dark", "body", ""),
    ("bw", ".highlight", ""),
    ("nosuch", "", ""),
]:
    S.append("|".join([style, arg, opts]))

FILES["jobs.txt"] = "\n".join(J) + "\n"
FILES["styles.txt"] = "\n".join(S) + "\n"

# ------------------------------------------------------------- docs site
FILES["docs/index.md"] = '''# Inventory docs

Install the service, then point a client at it.

```bash
pip install inventory && inventory --port 8080
```

A request from Python:

```python {linenos hl_lines="2"}
import httpx
r = httpx.get("http://localhost:8080/items")
print(r.json()["count"])
```

The config file:

```ini
[server]
port = 8080
```
'''

FILES["docs/api.md"] = '''# API

Each item comes back as JSON:

```json
{"sku": "ABC-1", "qty": 12}
```

Unknown fences fall back to plain text:

```klingon
DISPLAY 'HI'.
```

```
no language at all <b>
```

And SQL, numbered from 5:

```sql {linenos linenostart="5"}
SELECT sku FROM items WHERE qty < 3;
```
'''

for path, body in FILES.items():
    full = os.path.join("data", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="") as f:
        f.write(body)
