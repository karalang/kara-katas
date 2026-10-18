#!/usr/bin/env python3
"""Python 3.13's json over data/jobs.tsv: writes expected.out's text to
stdout. Run mk.py first."""
import json


def read(name):
    with open("data/" + name, encoding="utf-8", newline="") as f:
        return f.read()


def options(fields):
    kw = {}
    for f in fields:
        k, _, v = f.partition("=")
        if k == "indent":
            kw["indent"] = "\t" if v == "t" else int(v)
        elif k == "compact":
            kw["separators"] = (",", ":")
        else:
            kw[k] = v == "1"
    return kw


def show(text):
    for line in text.split("\n"):
        print("  |" + line)


def main():
    with open("data/jobs.tsv", encoding="utf-8") as f:
        jobs = f.read().splitlines()
    for job in jobs:
        f = job.split("\t")
        print("== " + " | ".join(f))
        text = read(f[1])
        kw = options(f[2:])
        if f[0] == "jsonl":
            for n, line in enumerate(text.split("\n"), 1):
                if not line.strip():
                    continue
                try:
                    print("  %d: %s" % (n, json.dumps(json.loads(line), **kw)))
                except Exception as e:
                    print("  %d: %s: %s" % (n, type(e).__name__, e))
            continue
        try:
            value = json.loads(text)
        except Exception as e:
            print("  %s: %s" % (type(e).__name__, e))
            continue
        try:
            if f[0] == "load":
                print("  " + repr(value))
            elif f[0] == "dump":
                # as writing it to a UTF-8 file would
                show(json.dumps(value, **kw).encode("utf-8").decode("utf-8"))
            elif f[0] == "roundtrip":
                a = json.dumps(value)
                b = json.dumps(json.loads(a))
                c = json.dumps(value, indent=3, sort_keys=True, ensure_ascii=False)
                d = json.dumps(json.loads(c), indent=3, sort_keys=True, ensure_ascii=False)
                print("  compact %d chars, same again %s; pretty %d chars, same again %s"
                      % (len(a), a == b, len(c), c == d))
        except Exception as e:
            print("  %s: %s" % (type(e).__name__, e))


main()
