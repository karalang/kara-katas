#!/usr/bin/env python3
"""Writes data/ for mini_pprint: six files of Python literals (a service
config, a lock file, an API response, a matrix, a word list and a long
text) and the jobs."""
import ast
import os

os.makedirs("data", exist_ok=True)

FILES = {}

FILES["config.py"] = r'''# checkout service, as loaded from three YAML layers
{
    'service': 'checkout',
    'version': 3,
    'replicas': 4,
    'enabled': True,
    'fallback': None,
    'ports': [8080, 8443, 9090],
    'limits': {'cpu_millis': 1500, 'memory_bytes': 2147483648, 'open_files': 65536},
    'env': {'LOG_LEVEL': 'info', 'REGION': 'eu-central-1', 'DB_URL': 'postgres://checkout@db1.internal:5432/orders'},
    'features': ('beta-cart', 'new-payments', 'gift-cards'),
    'owners': [
        {'name': 'Ada Lovelace', 'email': 'ada@example.com', 'oncall': True},
        {'name': 'Grace Hopper', 'email': 'grace@example.com', 'oncall': False},
    ],
    'retry': {'attempts': 5, 'backoff_ms': [100, 200, 400, 800, 1600], 'jitter': False},
    'notes': 'Checkout talks to payments over mTLS. Do not raise replicas above eight without asking the payments team first, because their rate limiter is per pod.',
    'motd': 'Welcome to checkout.\nDeploys freeze on Fridays.\n',
    'empty_list': [],
    'empty_dict': {},
    'empty_tuple': (),
    'single': ('only',),
    'zones': {3, 1, 2},
    'signature': b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01\x00',
    'tiny': b'ok',
    'quote': "it's",
    'unicode': 'Zürich → Köln 🚆',
    'negative': -1234567,
}
'''

FILES["lock.py"] = r'''{
    'name': 'storefront',
    'lockfileVersion': 3,
    'packages': {
        'node_modules/express': {'version': '4.19.2', 'resolved': 'https://registry.npmjs.org/express/-/express-4.19.2.tgz', 'dependencies': {'accepts': '~1.3.8', 'body-parser': '1.20.2', 'cookie': '0.6.0'}},
        'node_modules/accepts': {'version': '1.3.8', 'dependencies': {'mime-types': '~2.1.34', 'negotiator': '0.6.3'}},
        'node_modules/cookie': {'version': '0.6.0', 'engines': {'node': '>= 0.6'}},
        'node_modules/negotiator': {'version': '0.6.3', 'dev': True},
    },
}
'''

FILES["response.py"] = r'''{'status': 200, 'headers': [('Content-Type', 'application/json'), ('X-Request-Id', 'a1b2c3d4'), ('Cache-Control', 'no-store')], 'body': {'items': [{'id': 101, 'sku': 'A-100', 'qty': 2, 'price_cents': 2450, 'tags': ['coffee', 'beans']}, {'id': 102, 'sku': 'B-220', 'qty': 1, 'price_cents': 18900, 'tags': []}], 'page': {'number': 1, 'size': 2, 'total': 37}, 'next': '/api/v2/orders/9912/items?page=2&size=2'}}
'''

FILES["matrix.py"] = r'''[
    [1, 0, 0, 0, 12, -3, 7, 100, 1000, 10000, 100000, 1000000],
    [0, 1, 0, 0, 5, 8, -13, 21, 34, 55, 89, 144],
    [0, 0, 1, 0, 233, 377, 610, 987, 1597, 2584, 4181, 6765],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [[[[[[1, 2], [3, 4]]]]]],
]
'''

FILES["words.py"] = r'''['alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey', 'x-ray', 'yankee', 'zulu', 'a much longer element that will never share a line', 'end']
'''

FILES["text.py"] = r'''"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam,   quis nostrud exercitation\n\nullamco laboris nisi ut aliquip ex ea commodo consequat. Supercalifragilisticexpialidociousandthensomemoretomakeitlong!\tTabbed end."
'''

for name, text in FILES.items():
    ast.literal_eval(text)  # every file must be a literal
    with open(os.path.join("data", name), "w", encoding="utf-8") as f:
        f.write(text)

# The small-int set reprs are in ascending order in CPython (hash(i) == i);
# the port prints them sorted, so check that here.
assert repr({3, 1, 2}) == "{1, 2, 3}"

JOBS = []
OPTS = [
    "",
    "width=40",
    "width=20",
    "width=1",
    "indent=4",
    "indent=4\twidth=30",
    "indent=0\twidth=30",
    "depth=1",
    "depth=2",
    "depth=3\twidth=50",
    "compact=1",
    "compact=1\twidth=30",
    "sort_dicts=0",
    "underscore_numbers=1",
    "width=60\tsort_dicts=0\tunderscore_numbers=1\tindent=2",
]
for name in sorted(FILES):
    for o in OPTS:
        JOBS.append(("pformat\t@%s\t%s" % (name, o)).rstrip("\t"))
for name in sorted(FILES):
    JOBS.append("saferepr\t@%s" % name)
    JOBS.append("readable\t@%s\tdepth=2" % name)
# Inline literals, written in the job.
for lit in [
    "[]", "()", "{}", "(1,)", "set()", "{5, 3, 4}", "''", "b''", "'x' 'y'",
    "[1, [2, [3, [4, [5]]]]]", "{'b': 1, 'a': {'d': 2, 'c': 3}}", "{2: 'two', 1: 'one', 10: 'ten'}",
    "-0", "0x1F", "1_000_000", "b'\\x00\\xff\\n\\'\"'", "'\\x00\\x7f\\x80\\xa0\\xad\\u00e9'",
    "\"a'b\"", "'a\"b'", "'a\\'b\"c'", "[True, False, None]", "(((1,),),)",
    "{'k': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}",
    "'one two three four five six seven eight nine ten eleven twelve'",
]:
    for o in ["", "width=10", "depth=1\twidth=10", "compact=1\twidth=12"]:
        JOBS.append(("pformat\t%s\t%s" % (lit, o)).rstrip("\t"))
# Constructor errors.
for o in ["indent=-1", "depth=0", "width=0"]:
    JOBS.append("pformat\t[1]\t%s" % o)

with open("data/jobs.tsv", "w", encoding="utf-8") as f:
    for j in JOBS:
        f.write(j + "\n")
