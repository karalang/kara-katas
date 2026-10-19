# Runs data/jobs.jsonl through natsort 8.4.0 (the files in natsort/,
# unchanged) and prints what each operation returns. Run mk.py first.
import contextlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import natsort  # noqa: E402
from natsort import ns  # noqa: E402
from natsort.__main__ import main as cli_main  # noqa: E402


def alg_of(names):
    if "BAD" in names:
        return "BAD"
    a = ns.DEFAULT
    for n in names:
        a |= ns[n]
    return a


def run(op):
    names = op.get("alg", [])
    label = "|".join(names) or "DEFAULT"
    if op["op"] == "sort":
        fn, items, rev = op["fn"], op["items"], op.get("reverse", False)
        head = f"-- {fn} {label}" + (" reverse" if rev else "")
        key = None
        if "key" in op:
            head += " key=" + op["key"]
            field = op["key"]
            key = lambda d: d[field]  # noqa: E731
        print(head)
        alg = alg_of(names)
        try:
            if fn == "natsorted":
                out = natsort.natsorted(items, key=key, reverse=rev, alg=alg)
            elif fn == "realsorted":
                out = natsort.realsorted(items, key=key, reverse=rev, alg=alg)
            elif fn == "index_natsorted":
                out = natsort.index_natsorted(items, key=key, reverse=rev, alg=alg)
            elif fn == "index_realsorted":
                out = natsort.index_realsorted(items, key=key, reverse=rev, alg=alg)
            else:
                out = natsort.order_by_index(items, natsort.index_natsorted(items, key=key, reverse=rev, alg=alg))
            print(repr(out))
        except (ValueError, TypeError) as e:
            print(f"error: {type(e).__name__}: {e}")
    elif op["op"] == "key":
        print(f"-- key {label} {op['item']!r}")
        print(repr(natsort.natsort_keygen(alg=alg_of(names))(op["item"])))
    else:
        print("-- cli " + " ".join(repr(a) for a in op["args"]))
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                cli_main(*op["args"])
            sys.stdout.write(buf.getvalue())
        except ValueError as e:
            sys.stdout.write(buf.getvalue())
            print(f"exit: {e}")


with open("data/jobs.jsonl") as f:
    for line in f:
        job = json.loads(line)
        print(f"== {job['name']}")
        for op in job["ops"]:
            run(op)
