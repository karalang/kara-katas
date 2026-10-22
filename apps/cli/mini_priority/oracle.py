#!/usr/bin/env python3
"""Runs data/jobs.tsv through the `priority` library and prints expected.out.

Each job prints "== " and its fields joined by " | ", then two spaces and the
result: `ok`, an `err=<message>` line, or (for `sched`) the list of stream
ids pulled, with the DeadlockError message on its own line if the tree jams.
"""
import sys

sys.path.insert(0, "vendor")
import priority  # noqa: E402

tree = None


def dep(s):
    return None if s == "-" else int(s)


def run(f):
    global tree
    k = f[0]
    if k == "tree":
        tree = priority.PriorityTree(maximum_streams=int(f[1]))
        return ["ok"]
    try:
        if k == "insert":
            tree.insert_stream(int(f[1]), dep(f[2]), int(f[3]), f[4] == "1")
            return ["ok"]
        if k == "reprio":
            tree.reprioritize(int(f[1]), dep(f[2]), int(f[3]), f[4] == "1")
            return ["ok"]
        if k == "remove":
            tree.remove_stream(int(f[1]))
            return ["ok"]
        if k == "block":
            tree.block(int(f[1]))
            return ["ok"]
        if k == "unblock":
            tree.unblock(int(f[1]))
            return ["ok"]
        if k == "sched":
            ids = []
            for _ in range(int(f[1])):
                try:
                    ids.append(tree.next())
                except priority.DeadlockError as e:
                    return [repr(ids), "err=" + str(e)]
            return [repr(ids)]
    except priority.PriorityError as e:
        return ["err=" + str(e)]
    raise SystemExit("unknown job: " + k)


out = []
with open("data/jobs.tsv") as fh:
    for line in fh.read().splitlines():
        f = line.split("\t")
        out.append("== " + " | ".join(f))
        for r in run(f):
            out.append("  " + r)
sys.stdout.write("\n".join(out) + "\n")
