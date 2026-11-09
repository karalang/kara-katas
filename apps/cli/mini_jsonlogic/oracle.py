#!/usr/bin/env python3
"""Runs data/flags.json over data/users.json, then every case in
data/cases.jsonl, through the vendored JsonLogic evaluator
(panzi-json-logic 1.0.1, json_logic/apply.py and builtins.py) and prints
the report mini_jsonlogic.kara must reproduce byte for byte (README.md
has the rules).

Every result is printed as `json.dumps` writes it; an exception is printed
as its type and message. The `log` operation writes to stdout itself.

Run from this directory: python3 -I -B oracle.py > expected.out"""
import json
import os
import sys

sys.path.insert(0, "vendor")
from json_logic import jsonLogic  # noqa: E402


def read(name):
    with open(os.path.join("data", name), encoding="utf-8", newline="") as fh:
        return fh.read()


def run(logic, data):
    try:
        return json.dumps(jsonLogic(logic, data))
    except Exception as e:  # noqa: BLE001 - the report shows every failure
        return f"error {type(e).__name__}: {e}"


def main():
    flags = json.loads(read("flags.json"))
    users = json.loads(read("users.json"))
    print("== flags")
    for user in users:
        print(f"user {user['name']}")
        for name, logic in flags.items():
            print(f"  {name}: {run(logic, user)}")
    print("== cases")
    for line in read("cases.jsonl").split("\n"):
        if not line:
            continue
        name, logic, data = json.loads(line)
        print(f"{name}: {run(logic, data)}")


main()
