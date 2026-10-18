#!/usr/bin/env python3
"""Runs data/jobs.tsv with Python's graphlib and prints expected.out."""
from graphlib import CycleError, TopologicalSorter


def graph(spec):
    """'d:b,c;b:a' -> {'d': ['b', 'c'], 'b': ['a']}, in order."""
    g = {}
    if spec == "-":
        return g
    for part in spec.split(";"):
        node, preds = part.split(":")
        g[node] = [p for p in preds.split(",") if p]
    return g


def order(spec):
    try:
        print(f"  {list(TopologicalSorter(graph(spec)).static_order())}")
    except CycleError as e:
        print(f"  CycleError: {e.args[0]} {e.args[1]}")


def waves(spec):
    ts = TopologicalSorter(graph(spec))
    ts.prepare()
    n = 1
    while ts.is_active():
        group = ts.get_ready()
        print(f"  wave {n}: {group}")
        ts.done(*group)
        n += 1


def steps(spec, ops):
    ts = TopologicalSorter(graph(spec))
    for op in ops.split(" "):
        try:
            if op == "prepare":
                ts.prepare()
                print("  prepare")
            elif op == "ready":
                print(f"  ready {ts.get_ready()}")
            elif op == "active":
                print(f"  active {ts.is_active()}")
            elif op.startswith("done:"):
                ts.done(op[5:])
                print(f"  done {op[5:]}")
            elif op.startswith("add:"):
                _, node, pred = op.split(":")
                ts.add(node, pred)
                print(f"  add {node}")
        except CycleError as e:
            print(f"  CycleError: {e.args[0]} {e.args[1]}")
        except ValueError as e:
            print(f"  ValueError: {e}")


def ci(path, workers):
    jobs = {}
    ts = TopologicalSorter()
    for line in open("data/" + path[1:]):
        name, secs, needs = line.rstrip("\n").split("\t")
        jobs[name] = int(secs)
        ts.add(name, *([] if needs == "-" else needs.split(",")))
    ts.prepare()
    queue = []
    running = []  # (finish, start order, name)
    now = 0
    busy = 0
    seq = 0
    while ts.is_active():
        queue.extend(ts.get_ready())
        while queue and len(running) < workers:
            name = queue.pop(0)
            running.append((now + jobs[name], seq, name))
            seq += 1
            print(f"  t={now:>3} start {name}")
        running.sort()
        finish, _, name = running.pop(0)
        busy += jobs[name]
        now = finish
        print(f"  t={now:>3} done  {name}")
        ts.done(name)
    print(f"  {workers} workers: {now}s wall, {busy}s of work, {100 * busy // (now * workers)}% busy")


def install(path, target):
    deps = {}
    for line in open("data/" + path[1:]):
        line = line.rstrip("\n")
        if not line:
            continue
        name, rest = line.split(":", 1)
        deps[name] = [d.strip() for d in rest.split(",") if d.strip()]
    if target not in deps:
        print(f"  error: unknown package {target!r}")
        return
    ts = TopologicalSorter()
    todo = [target]
    seen = set()
    while todo:
        p = todo.pop(0)
        if p in seen:
            continue
        seen.add(p)
        ts.add(p, *deps[p])
        todo.extend(deps[p])
    try:
        order = list(ts.static_order())
        print(f"  install {len(order)}: {' '.join(order)}")
    except CycleError as e:
        print(f"  error: dependency cycle {' -> '.join(reversed(e.args[1]))}")


for raw in open("data/jobs.tsv"):
    f = raw.rstrip("\n").split("\t")
    print("== " + " | ".join(f))
    k = f[0]
    if k == "order":
        order(f[1])
    elif k == "waves":
        waves(f[1])
    elif k == "steps":
        steps(f[1], f[2])
    elif k == "ci":
        ci(f[1], int(f[2]))
    elif k == "install":
        install(f[1], f[2])
