#!/usr/bin/env python3
"""Runs data/jobs.tsv through the vendored bitstring and prints expected.out."""
import sys

sys.path.insert(0, "vendor")
import bitstring  # noqa: E402

B = bitstring.BitArray


def run(op, arg):
    if op in ("slice", "index", "concat", "eq", "count", "find",
              "findall", "unpack"):
        parts = arg.split("|")
    try:
        if op == "bin":
            return B(arg).bin
        if op == "hex":
            return B(arg).hex
        if op == "oct":
            return B(arg).oct
        if op == "uint":
            return str(B(arg).uint)
        if op == "int":
            return str(B(arg).int)
        if op == "len":
            return str(len(B(arg)))
        if op == "str":
            return str(B(arg))
        if op == "reverse":
            b = B(arg)
            b.reverse()
            return b.bin
        if op == "invert":
            b = B(arg)
            b.invert()
            return b.bin
        if op == "tobytes":
            return B(arg).tobytes().hex()
        if op == "all":
            return str(B(arg).all(True))
        if op == "any":
            return str(B(arg).any(True))
        if op == "slice":
            return B(parts[0])[int(parts[1]):int(parts[2])].bin
        if op == "index":
            return str(B(parts[0])[int(parts[1])])
        if op == "concat":
            return (B(parts[0]) + B(parts[1])).bin
        if op == "eq":
            return str(B(parts[0]) == B(parts[1]))
        if op == "count":
            return str(B(parts[0]).count(int(parts[1])))
        if op == "find":
            return str(B(parts[0]).find(parts[1]))
        if op == "findall":
            return str(list(B(parts[0]).findall(parts[1])))
        if op == "unpack":
            return str(B(parts[0]).unpack(parts[1]))
    except Exception as e:
        return "error: " + str(e)
    raise SystemExit("unknown op: " + op)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        arg = f[1] if len(f) > 1 else ""
        out.append("== " + " | ".join(f))
        out.append("  " + run(f[0], arg))
sys.stdout.write("\n".join(out) + "\n")
