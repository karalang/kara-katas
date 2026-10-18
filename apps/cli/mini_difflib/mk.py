#!/usr/bin/env python3
"""Writes data/: the text files the jobs compare, words.txt and jobs.tsv."""
import os, random

os.makedirs("data", exist_ok=True)

def put(name, text):
    with open(os.path.join("data", name), "w", newline="") as f:
        f.write(text)

put("nginx.conf.orig", """\
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 768;
    # multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
""")
put("nginx.conf", """\
user www-data;
worker_processes 4;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
    worker_connections 1024;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    server_tokens off;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;
    gzip_types text/plain text/css application/json;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
""")
put("cache.py.orig", '''\
import time


class Cache:
    """A cache whose entries expire."""

    def __init__(self, ttl):
        self.ttl = ttl
        self.data = {}

    def get(self, key):
        if key not in self.data:
            return None
        value, stamp = self.data[key]
        if time.time() - stamp > self.ttl:
            del self.data[key]
            return None
        return value

    def put(self, key, value):
        self.data[key] = (value, time.time())

    def size(self):
        return len(self.data)
''')
put("cache.py", '''\
import time
from collections import OrderedDict


class Cache:
    """A cache whose entries expire, holding at most max_size entries."""

    def __init__(self, ttl, max_size=128):
        self.ttl = ttl
        self.max_size = max_size
        self.data = OrderedDict()

    def get(self, key, default=None):
        if key not in self.data:
            return default
        value, stamp = self.data[key]
        if time.monotonic() - stamp > self.ttl:
            del self.data[key]
            return default
        self.data.move_to_end(key)
        return value

    def put(self, key, value):
        self.data[key] = (value, time.monotonic())
        self.data.move_to_end(key)
        while len(self.data) > self.max_size:
            self.data.popitem(last=False)

    def __len__(self):
        return len(self.data)
''')
put("notes.txt.orig", """\
The quick brown fox jumps over the lazy dog.
Python's difflib compares sequences of any hashable items.
	Tabs and  double spaces are character junk to ndiff.
This line stays the same.
The café opens at nine in the morning.
Remember to water the plants on Tuesday.
one two three four five
""")
put("notes.txt", """\
The quick brown cat jumps over the lazy dog!
Python's difflib compares sequences of hashable items.
	Tabs and double  spaces are character junk to ndiff.
This line stays the same.
The cafe opens at ten in the morning.
Remember to water the plant on Thursday.
one two four five six
A new last line.""")
put("empty.txt", "")
put("same.txt", "alpha\nbeta\n")
put("same2.txt", "alpha\nbeta\n")

# A log long enough (>= 200 lines) for SequenceMatcher's autojunk to throw
# out its most common lines.
rng = random.Random(7)
log = []
for i in range(260):
    r = rng.random()
    if r < 0.45:
        log.append("GET /health 200\n")
    elif r < 0.6:
        log.append("\n")
    else:
        log.append(f"GET /api/item/{rng.randrange(40)} {rng.choice([200, 200, 304, 404])}\n")
put("access.log.orig", "".join(log))
log2 = list(log)
del log2[30:34]
log2.insert(100, "POST /api/item 201\n")
log2[150] = "GET /api/item/7 500\n"
log2[200:200] = ["GET /health 503\n", "GET /health 503\n"]
put("access.log", "".join(log2))

put("words.txt", "\n".join("""\
apple ape peach puppy apply ample maple happy appeal applet
python pythonic typhoon pyramid
lambda lambada lamb label
import important impart export imports
return retry rerun ruin turn
while whale wheel wheat white
continue contain continent
""".split()) + "\n")

JOBS = """\
opcodes\tqabxcd\tabycdf
opcodes\tabcd\tbcde
opcodes\t\tabc
opcodes\tabc\t
opcodes\tabc\tabc
blocks\tabxcd\tabcd
blocks\tqabxcd\tabycdf
ratios\tabcd\tbcde
ratios\tqabxcd\tabycdf
ratios\taaaa\taa
ratios\t\t
ratios\tkitten\tsitting
ratios\tprivate Thread currentThread;\tprivate volatile Thread currentThread;
junk\tprivate Thread currentThread;\tprivate volatile Thread currentThread;
junk\t a b c \tabc
longest\t abcd\tabcd abcd
longest\tabcd\tefgh
close\tappel\t3\t0.6
close\twheel\t3\t0.6
close\twheel\t2\t0.8
close\tpythn\t5\t0.6
close\tlamda\t3\t0.6
close\timprt\t1\t0.6
close\tretrun\t3\t0.5
close\tcontinew\t4\t0.6
close\tzzz\t3\t0.6
close\tapple\t3\t1.0
close\tapple\t0\t0.6
close\tapple\t3\t1.5
unified\tnginx.conf.orig\tnginx.conf\t3
unified\tnginx.conf.orig\tnginx.conf\t1
unified\tnginx.conf.orig\tnginx.conf\t0
unified\tcache.py.orig\tcache.py\t3
unified\tnotes.txt.orig\tnotes.txt\t2
unified\tempty.txt\tsame.txt\t3
unified\tsame.txt\tempty.txt\t3
unified\tsame.txt\tsame2.txt\t3
unified\taccess.log.orig\taccess.log\t3
context\tnginx.conf.orig\tnginx.conf\t3
context\tcache.py.orig\tcache.py\t2
context\tnotes.txt.orig\tnotes.txt\t1
context\tempty.txt\tsame.txt\t3
context\taccess.log.orig\taccess.log\t1
ndiff\tnotes.txt.orig\tnotes.txt
ndiff\tnginx.conf.orig\tnginx.conf
ndiff\tcache.py.orig\tcache.py
ndiff_linejunk\tcache.py.orig\tcache.py
ndiff\tempty.txt\tsame.txt
restore\tnotes.txt.orig\tnotes.txt\t1
restore\tnotes.txt.orig\tnotes.txt\t2
restore\tcache.py.orig\tcache.py\t2
restore\tcache.py.orig\tcache.py\t3
line_ratio\taccess.log.orig\taccess.log\ttrue
line_ratio\taccess.log.orig\taccess.log\tfalse
line_ratio\tnginx.conf.orig\tnginx.conf\ttrue
unified\tnginx.conf.orig\tmissing.conf\t3
"""
put("jobs.tsv", JOBS)
