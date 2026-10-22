#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored python-ulid and prints expected.out."""
import sys
import uuid

sys.path.insert(0, "vendor")
from ulid import ULID  # noqa: E402


def run(op, arg):
    try:
        if op == "s2int":
            return "int=" + str(int(ULID.from_str(arg)))
        if op == "s2hex":
            return "hex=" + ULID.from_str(arg).hex
        if op == "ms":
            return "ms=" + str(ULID.from_str(arg).milliseconds)
        if op == "iso":
            return "iso=" + ULID.from_str(arg).datetime.isoformat()
        if op == "uuid":
            return "uuid=" + str(ULID.from_str(arg).to_uuid())
        if op == "uuid4":
            return "uuid4=" + str(ULID.from_str(arg).to_uuid4())
        if op == "uuid7":
            return "uuid7=" + str(ULID.from_str(arg).to_uuid7())
        if op == "uuid7c":
            return "uuid7c=" + str(ULID.from_str(arg).to_uuid7(compliant=True))
        if op == "int2str":
            return "str=" + str(ULID.from_int(int(arg)))
        if op == "hex2str":
            return "str=" + str(ULID.from_hex(arg))
        if op == "fromuuid":
            return "str=" + str(ULID.from_uuid(uuid.UUID(arg)))
        if op == "fromuuid7":
            return "str=" + str(ULID.from_uuid7(uuid.UUID(arg)))
        if op == "parse":
            if len(arg) == 37 and arg.isdigit():
                return "parse=" + str(ULID.parse(int(arg)))
            return "parse=" + str(ULID.parse(arg))
        if op == "sort":
            items = [ULID.from_str(s) for s in arg.split(",")]
            items.sort()
            return "sorted=" + ",".join(str(u) for u in items)
        if op == "cmp":
            a, b = arg.split(",")
            ua, ub = ULID.from_str(a), ULID.from_str(b)
            return "lt=" + str(ua < ub).lower() + " eq=" + str(ua == ub).lower()
    except (ValueError, OverflowError, TypeError) as e:
        return "error=" + str(e)
    raise SystemExit("unknown op: " + op)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        out.append("  " + run(f[0], f[1]))
sys.stdout.write("\n".join(out) + "\n")
