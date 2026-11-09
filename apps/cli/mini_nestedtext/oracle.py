#!/usr/bin/env python3
"""Loads every file in data/loads.jsonl, then every case in
data/cases.jsonl, through the vendored NestedText loader (nestedtext 3.8,
nestedtext/nestedtext.py, with inform 1.37 for its messages) and prints the
report mini_nestedtext.kara must reproduce byte for byte (README.md has the
rules).

A loaded value is printed as `json.dumps` writes it (no ASCII escaping); a
NestedTextError as `str(e)` and its line and column numbers.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import json
import os
import sys

sys.path.insert(0, "vendor")
import nestedtext as nt  # noqa: E402


def read(name):
    with open(os.path.join("data", name), encoding="utf-8", newline="") as fh:
        return fh.read()


def normalize(key, keys):
    return key.lower().replace(" ", "_")


def de_dup(key, state):
    # The de-duplicating callback from the loads() documentation.
    if key not in state:
        state[key] = 1
    state[key] += 1
    return f"{key} — #{state[key]}"


def load(text, top, options, keymap=None):
    on_dup = options.get("on_dup")
    return nt.loads(
        text,
        top,
        source=options.get("source"),
        on_dup=de_dup if on_dup == "dedup" else on_dup,
        keymap=keymap,
        normalize_key=normalize if options.get("normalize") else None,
        dialect=options.get("dialect"),
    )


def show_error(e, lead):
    for line in str(e).split("\n"):
        print(f"{lead}{line}" if line else lead.rstrip())
    print(f"{lead}lineno {e.lineno}, colno {e.colno}")


def main():
    print("== files")
    for line in read("loads.jsonl").split("\n"):
        if not line:
            continue
        name, top, options, queries = json.loads(line)
        shown = ", ".join(f"{k}={v}" for k, v in options.items())
        print(f"load {name} as {top}" + (f" ({shown})" if shown else ""))
        keymap = {}
        try:
            value = load(read("files/" + name), top, dict(options, source=name), keymap)
        except nt.NestedTextError as e:
            show_error(e, "  error: ")
            continue
        for text in json.dumps(value, ensure_ascii=False, indent=2).split("\n"):
            print("  " + text)
        for keys, kind in queries:
            print(f"  where {json.dumps(keys, ensure_ascii=False)} {kind}:")
            loc = nt.get_location(keys, keymap)
            if loc is None:
                print("    not found")
                continue
            print(f"    at {loc.as_tuple(kind)}, lines {loc.get_line_numbers(kind, sep='-')}")
            for text in loc.as_line(kind).split("\n"):
                print("    " + text)
    print("== cases")
    for line in read("cases.jsonl").split("\n"):
        if not line:
            continue
        name, top, options, text = json.loads(line)
        try:
            value = load(text, top, options)
        except nt.NestedTextError as e:
            print(f"{name}: error")
            show_error(e, "  ")
            continue
        print(f"{name}: {json.dumps(value, ensure_ascii=False)}")


main()
