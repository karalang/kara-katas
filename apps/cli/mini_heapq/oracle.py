#!/usr/bin/env python3
"""Runs data/jobs.tsv with Python's heapq, bisect and sched and prints
expected.out."""
import bisect
import heapq
import os
import sched


class Rec:
    def __init__(self, line):
        p = line.split(" ")
        self.line = line
        self.time, self.host, self.method, self.path = p[0], p[1], p[2], p[3]
        self.status, self.bytes, self.ms = int(p[4]), int(p[5]), int(p[6])


def read_log(name):
    with open(os.path.join("data/logs", name)) as f:
        return [Rec(l.rstrip("\n")) for l in f]


def all_logs():
    out = []
    for name in sorted(os.listdir("data/logs")):
        out.extend(read_log(name))
    return out


def ints(field):
    if field in ("", "-"):
        return []
    return [int(x) for x in field.split(",")]


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


KEYS = {"bytes": lambda r: r.bytes, "ms": lambda r: r.ms, "status": lambda r: r.status,
        "path": lambda r: r.path, "time": lambda r: r.time, "host": lambda r: r.host}


def heap_job(init, ops):
    h = ints(init)
    heapq.heapify(h)
    print(f"  heapify -> {show(h)}")
    for op in ops.split("|"):
        parts = op.split(" ")
        try:
            if parts[0] == "push":
                heapq.heappush(h, int(parts[1]))
                print(f"  {op} -> {show(h)}")
            elif parts[0] == "pop":
                x = heapq.heappop(h)
                print(f"  {op} = {x} -> {show(h)}")
            elif parts[0] == "pushpop":
                x = heapq.heappushpop(h, int(parts[1]))
                print(f"  {op} = {x} -> {show(h)}")
            elif parts[0] == "replace":
                x = heapq.heapreplace(h, int(parts[1]))
                print(f"  {op} = {x} -> {show(h)}")
        except IndexError as e:
            print(f"  {op}: IndexError: {e}")


def top_job(kind, n, key, data):
    f = heapq.nlargest if kind == "nlargest" else heapq.nsmallest
    if data == "@logs":
        for r in f(n, all_logs(), key=KEYS[key]):
            print(f"  {r.line}")
    else:
        print(f"  {show(f(n, ints(data)))}")


def merge_job(key, spec):
    groups = spec.split(";")
    if any(g.endswith(".log") for g in groups):
        logs = [read_log(g) for g in groups]
        if key == "-":
            for line in heapq.merge(*[[r.line for r in l] for l in logs]):
                print(f"  {line}")
        else:
            for r in heapq.merge(*logs, key=KEYS[key]):
                print(f"  {r.line}")
    else:
        print(f"  {show(heapq.merge(*[ints(g) for g in groups]))}")


def route_job(src, dst):
    adj = {}
    with open("data/roads.tsv") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            a, b, w = line.split("\t")
            adj.setdefault(a, []).append((b, int(w)))
            adj.setdefault(b, []).append((a, int(w)))
    dist = {src: 0}
    prev = {}
    seen = set()
    h = [(0, src)]
    while h:
        d, u = heapq.heappop(h)
        if u in seen:
            continue
        seen.add(u)
        if u == dst:
            break
        for v, w in adj.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(h, (nd, v))
    if dst not in seen:
        print(f"  no route ({len(seen)} towns settled)")
        return
    path = [dst]
    while path[-1] != src:
        path.append(prev[path[-1]])
    path.reverse()
    print(f"  {dist[dst]} min: {' -> '.join(path)}")
    print(f"  ({len(seen)} towns settled)")


def sched_job(path):
    clock = [0]
    s = sched.scheduler(lambda: clock[0], lambda d: clock.__setitem__(0, clock[0] + d))
    events = {}
    ran = [0]
    names = {}

    def once(name):
        ran[0] += 1
        print(f"  t={clock[0]} {name}")

    def repeat(name, k, n, every, pri):
        ran[0] += 1
        print(f"  t={clock[0]} {name} ({k}/{n})")
        if k < n:
            events[name] = s.enter(every, pri, repeat, (name, k + 1, n, every, pri))

    def later(name, target, delay, pri):
        ran[0] += 1
        print(f"  t={clock[0]} {name} -> enter {target} at {clock[0] + delay}")
        events[target] = s.enter(delay, pri, once, (target,))

    def cancel(name, target):
        ran[0] += 1
        ev = events.get(target)
        try:
            if ev is None:
                raise ValueError
            s.cancel(ev)
            print(f"  t={clock[0]} {name}: cancelled {target}")
        except ValueError:
            print(f"  t={clock[0]} {name}: {target} is not queued")

    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            p = line.split("\t")
            t, pri, kind, name = int(p[0]), int(p[1]), p[2], p[3]
            if kind == "once":
                ev = s.enterabs(t, pri, once, (name,))
            elif kind == "repeat":
                ev = s.enterabs(t, pri, repeat, (name, 1, int(p[4]), int(p[5]), pri))
            elif kind == "later":
                ev = s.enterabs(t, pri, later, (name, p[4], int(p[5]), pri))
            else:
                ev = s.enterabs(t, pri, cancel, (name, p[4]))
            events[name] = ev
            names[ev.sequence] = name
    print("  queue: " + " ".join(f"{names[e.sequence]}@{e.time}/{e.priority}" for e in s.queue))
    s.run()
    print(f"  done at t={clock[0]}, {ran[0]} events run")


def run(f):
    kind = f[0]
    if kind == "heap":
        heap_job(f[1], f[2])
    elif kind in ("nlargest", "nsmallest"):
        top_job(kind, int(f[1]), f[2], f[3])
    elif kind == "merge":
        merge_job(f[1], f[2])
    elif kind == "bisect":
        fn = bisect.bisect_left if f[1] == "left" else bisect.bisect_right
        print(f"  {fn(ints(f[2]), int(f[3]))}")
    elif kind == "insort":
        a = ints(f[1])
        for x in ints(f[2]):
            bisect.insort(a, x)
            print(f"  insort {x} -> {show(a)}")
    elif kind == "grade":
        print("  " + " ".join("FDCBA"[bisect.bisect([60, 70, 80, 90], s)] for s in ints(f[1])))
    elif kind == "buckets":
        bounds = ints(f[1])
        counts = [0] * (len(bounds) + 1)
        recs = all_logs()
        for r in recs:
            counts[bisect.bisect_left(bounds, r.ms)] += 1
        total = 0
        for i, b in enumerate(bounds):
            total += counts[i]
            print(f"  le={b} {total}")
        total += counts[-1]
        print(f"  le=+Inf {total}")
        print(f"  sum={sum(r.ms for r in recs)} count={len(recs)}")
    elif kind == "route":
        route_job(f[1], f[2])
    elif kind == "sched":
        sched_job("data/" + f[1][1:])


with open("data/jobs.tsv") as fh:
    for raw in fh:
        fields = raw.rstrip("\n").split("\t")
        print("== " + " | ".join(fields))
        run(fields)
