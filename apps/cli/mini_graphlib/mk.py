#!/usr/bin/env python3
"""Writes data/ for mini_graphlib: a CI pipeline, a package index, the jobs."""
import os

os.makedirs("data", exist_ok=True)

# job	seconds	needs (comma-separated)
PIPELINE = """\
checkout	5	-
deps	40	checkout
lint	15	deps
typecheck	25	deps
build-linux	90	deps
build-mac	120	deps
unit	60	build-linux
integration	150	build-linux,typecheck
ui	80	build-mac
docs	30	checkout
package	20	build-linux,build-mac
sign	10	package
release	5	sign,unit,integration,ui,lint,docs
"""

# package: dependencies (Debian-style, one per line)
PACKAGES = """\
app: web-framework, orm, logging, config
web-framework: http, templates, logging
orm: db-driver, logging
db-driver: sockets, tls
http: sockets, tls
tls: crypto
crypto:
sockets:
templates: escaping
escaping:
logging: config
config:
cli: config, logging
broken-a: broken-b
broken-b: broken-c
broken-c: broken-a, logging
"""

JOBS = [
    "order\td:b,c;b:a;c:a",
    "order\ta:;b:;c:",
    "order\tc:a,b;a:;b:a",
    "order\t-",
    "order\tx:x",
    "order\ta:b;b:c;c:a",
    "order\tq:p;p:o;o:n;n:p",
    "order\tz:y;y:x;w:v;v:z",
    "order\tb:a,a;c:b;a:",
    "waves\td:b,c;b:a;c:a;e:a",
    "waves\tlib:base;app:lib,ui;ui:base;tests:app;base:",
    "steps\ta:;b:a\tready ready done:a ready done:b active",
    "steps\ta:;b:a\tdone:a",
    "steps\ta:;b:a\tprepare ready done:b",
    "steps\ta:;b:a\tprepare ready done:a done:a",
    "steps\ta:;b:a\tprepare ready done:zz",
    "steps\ta:;b:a\tprepare add:c:a",
    "steps\ta:;b:a\tprepare prepare",
    "steps\ta:;b:a;c:b\tprepare active ready active done:a active ready done:b ready done:c active ready",
    "steps\ta:b;b:a;c:\tprepare ready done:c ready active",
    "ci\t@pipeline.tsv\t1",
    "ci\t@pipeline.tsv\t3",
    "ci\t@pipeline.tsv\t8",
    "install\t@packages.txt\tapp",
    "install\t@packages.txt\tcli",
    "install\t@packages.txt\tescaping",
    "install\t@packages.txt\tbroken-a",
    "install\t@packages.txt\tnope",
]

with open("data/pipeline.tsv", "w") as f:
    f.write(PIPELINE)
with open("data/packages.txt", "w") as f:
    f.write(PACKAGES)
with open("data/jobs.tsv", "w") as f:
    f.write("\n".join(JOBS) + "\n")
