import os
def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text)

nginx = """user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 768;
    multi_accept off;
}

http {
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    server_tokens on;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;
    gzip_types text/plain text/css application/json;

    upstream app {
        server 127.0.0.1:8000;
    }

    server {
        listen 80;
        server_name shop.example.com;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
        }

        location /static/ {
            alias /srv/shop/static/;
        }
    }
}
"""
nginx2 = nginx.replace("    worker_connections 768;\n    multi_accept off;", "    worker_connections 4096;\n    multi_accept on;")
nginx2 = nginx2.replace("    server_tokens on;\n", "    server_tokens off;\n    client_max_body_size 16m;\n")
nginx2 = nginx2.replace("        server 127.0.0.1:8000;\n", "        server 127.0.0.1:8000;\n        server 127.0.0.1:8001;\n        keepalive 32;\n")
nginx2 = nginx2.replace("            alias /srv/shop/static/;\n", "            alias /srv/shop/static/;\n            expires 7d;\n")

app = """import json
import logging
import os

log = logging.getLogger("shop")

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


def load_config(path):
    with open(path) as f:
        return json.load(f)


def page_size(params):
    size = int(params.get("size", DEFAULT_PAGE_SIZE))
    if size > MAX_PAGE_SIZE:
        size = MAX_PAGE_SIZE
    return size


def list_orders(db, params):
    size = page_size(params)
    offset = int(params.get("offset", 0))
    rows = db.query("SELECT * FROM orders LIMIT ? OFFSET ?", size, offset)
    return [dict(r) for r in rows]


def cancel_order(db, order_id):
    order = db.get("orders", order_id)
    if order is None:
        return False
    db.update("orders", order_id, status="cancelled")
    log.info("cancelled %s", order_id)
    return True


def main():
    config = load_config(os.environ.get("SHOP_CONFIG", "shop.json"))
    log.setLevel(config.get("log_level", "INFO"))
    print("shop starting")


if __name__ == "__main__":
    main()
"""
app2 = app.replace("import os\n", "import os\nimport time\n")
app2 = app2.replace("    if size > MAX_PAGE_SIZE:\n        size = MAX_PAGE_SIZE\n", "    if size < 1:\n        size = 1\n    if size > MAX_PAGE_SIZE:\n        size = MAX_PAGE_SIZE\n")
app2 = app2.replace("""    if order is None:
        return False
    db.update("orders", order_id, status="cancelled")
""", """    if order is None or order["status"] == "shipped":
        return False
    db.update("orders", order_id, status="cancelled", at=time.time())
""")
app2 = app2.replace('    print("shop starting")\n', '    log.info("shop starting on %s", config.get("port", 8000))\n')

readme = """# shop

The order service behind shop.example.com.

## Running

    SHOP_CONFIG=shop.json python3 app.py

## Configuration

`shop.json` holds the log level and the database URL.
"""
readme2 = readme.replace("the log level and the database URL.\n", "the log level, the port and the database URL.\n") + "\nSee deploy.sh for the production rollout."

legacy = """[server]
port = 8000
workers = 2

[db]
url = sqlite:///shop.db
"""
deploy = """#!/bin/sh
set -eu
rsync -a --delete ./ shop@prod:/srv/shop/
ssh shop@prod 'sudo systemctl reload nginx && sudo systemctl restart shop'
"""
schema = """CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    status TEXT NOT NULL DEFAULT 'new',
    total_cents INTEGER NOT NULL
);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL REFERENCES orders(id),
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL
);

CREATE INDEX orders_by_customer ON orders(customer_id);
"""
schema2 = """CREATE TABLE products (
    sku TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    price_cents INTEGER NOT NULL
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    name TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL REFERENCES orders(id),
    sku TEXT NOT NULL REFERENCES products(sku),
    quantity INTEGER NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    status TEXT NOT NULL DEFAULT 'new',
    total_cents INTEGER NOT NULL
);

CREATE INDEX orders_by_customer ON orders(customer_id);
CREATE INDEX orders_by_status ON orders(status);
"""
for t, files in [("before", {"nginx.conf": nginx, "app.py": app, "README.md": readme, "legacy.ini": legacy, "schema.sql": schema}),
                 ("after", {"nginx.conf": nginx2, "app.py": app2, "README.md": readme2, "deploy.sh": deploy, "schema.sql": schema2})]:
    for n, s in files.items():
        w(f"{t}/{n}", s)
# drifted: a local copy someone edited after branching
dn = "# local tuning, see ops ticket 4411\nworker_rlimit_nofile 8192;\n\n" + nginx
da = app.replace('DEFAULT_PAGE_SIZE = 20\n', 'DEFAULT_PAGE_SIZE = 50\n')
da = da.replace('    return [dict(r) for r in rows]\n', '    return [dict(r) for r in rows]\n\n\ndef health(db):\n    return db.ping()\n')
da = da.replace('status="cancelled")', 'status="canceled")')
w("drifted/nginx.conf", dn); w("drifted/app.py", da); w("drifted/README.md", readme); w("drifted/legacy.ini", legacy); w("drifted/schema.sql", schema)
w("patches/bad.patch", "diff -u a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n@@ -1,3 +1,4 @@\n import json\n+import sys\n import logging\nimport os\n")
w("patches/notes.patch", "Release notes for 1.9:\n- faster checkout\n- fewer timeouts\n")
