#!/usr/bin/env python3
"""Replays data/jobs.tsv against the vendored ijson 3.3.0 (the pure
Python backend, as the port is) and prints what each job produces.

Run: python3 -I -B oracle.py > expected.out"""
import contextlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "vendor"))
os.environ["IJSON_BACKEND"] = "python"

import ijson  # noqa: E402
import ijson.dump  # noqa: E402
from ijson.backends import python as backend  # noqa: E402
from collections import OrderedDict  # noqa: E402
from decimal import Decimal  # noqa: E402


def out(*parts):
    print("  " + " ".join(str(p) for p in parts))


def err(e):
    cls = type(e)
    name = cls.__qualname__
    if cls.__module__ != "builtins":
        name = cls.__module__ + "." + name
    return "error %s: %s" % (name, e)


def source(spec):
    """=text is inline UTF-8 text, x:hex inline bytes, anything else a path."""
    if spec.startswith("="):
        return io.BytesIO(spec[1:].encode("utf-8"))
    if spec.startswith("x:"):
        return io.BytesIO(bytes.fromhex(spec[2:]))
    return open(spec, "rb")


def raw(spec):
    f = source(spec)
    with f:
        return f.read()


def options(parts):
    o = {}
    rest = []
    for p in parts:
        if "=" in p and p.split("=", 1)[0] in ("buf", "multi", "float", "map", "take",
                                                 "comments", "cuts", "method", "prefix"):
            k, v = p.split("=", 1)
            o[k] = v
        else:
            rest.append(p)
    return o, rest


def config(o):
    c = {}
    if o.get("multi") == "1":
        c["multiple_values"] = True
    if o.get("float") == "1":
        c["use_float"] = True
    if o.get("comments") == "1":
        c["allow_comments"] = True
    return c


def show(it, o):
    take = int(o["take"]) if "take" in o else -1
    n = 0
    for ev in it:
        if n == take:
            out("(stopped after %d)" % take)
            return
        out(repr(ev))
        n += 1


def gen_job(cmd, src, prefix, o):
    kw = config(o)
    if "buf" in o:
        kw["buf_size"] = int(o["buf"])
    if o.get("map") == "od":
        kw["map_type"] = OrderedDict
    f = source(src)
    with f:
        if cmd == "basic":
            show(backend.basic_parse(f, **kw), o)
        elif cmd == "parse":
            show(backend.parse(f, **kw), o)
        elif cmd == "items":
            show(backend.items(f, prefix, **kw), o)
        elif cmd == "kvitems":
            show(backend.kvitems(f, prefix, **kw), o)
        elif cmd == "count":
            out(sum(1 for _ in backend.items(f, prefix, **kw)))


def push(method, src, prefix, o):
    data = raw(src)
    cuts = [int(c) for c in o.get("cuts", "").split(",") if c != ""]
    bounds = [0] + cuts + [len(data)]
    events = ijson.utils.sendable_list()
    kw = config(o)
    if method == "basic_parse":
        coro = backend.basic_parse_coro(events, **kw)
    elif method == "parse":
        coro = backend.parse_coro(events, **kw)
    elif method == "items":
        coro = backend.items_coro(events, prefix, **kw)
    else:
        coro = backend.kvitems_coro(events, prefix, **kw)
    take = int(o["take"]) if "take" in o else -1
    shown = [0]

    def flush():
        for ev in events:
            if shown[0] == take:
                break
            out("  " + repr(ev))
            shown[0] += 1
        del events[:]

    for i in range(len(bounds) - 1):
        chunk = data[bounds[i]:bounds[i + 1]]
        out("send %d bytes" % len(chunk))
        try:
            coro.send(chunk)
        except StopIteration:
            flush()
            out("  finished")
            continue
        except Exception as e:
            flush()
            out("  " + err(e))
            return
        flush()
    out("close")
    try:
        coro.close()
    except Exception as e:
        flush()
        out("  " + err(e))
        return
    flush()


def dump(src, o):
    argv = ["ijson.dump"]
    if "method" in o:
        argv += ["-m", o["method"]]
    if "prefix" in o:
        argv += ["-p", o["prefix"]]
    if o.get("multi") == "1":
        argv.append("-M")
    f = source(src)

    class Stdin:
        buffer = f

    saved = sys.argv, sys.stdin
    sys.argv, sys.stdin = argv, Stdin()
    buf = io.StringIO()
    failure = None
    try:
        with contextlib.redirect_stdout(buf):
            ijson.dump.dump()
    except Exception as e:
        failure = e
    finally:
        sys.argv, sys.stdin = saved
        f.close()
    for ln in buf.getvalue().split("\n")[:-1]:
        out(ln)
    if failure is not None:
        out(err(failure))


def report(src, dest):
    stats = {}
    notes = []
    with open(src, "rb") as f:
        for o in backend.items(f, "orders.item", buf_size=512):
            lines_total = Decimal(0)
            for ln in o["lines"]:
                lines_total += ln["price"] * ln["qty"]
            if lines_total != o["total"]:
                notes.append("order %d: total %s, lines add up to %s"
                             % (o["id"], o["total"], lines_total))
            net = o["total"]
            if "discount" in o:
                net = (net * (1 - o["discount"])).quantize(Decimal("0.01"))
            s = stats.setdefault(o["customer"], {"orders": 0, "revenue": Decimal(0),
                                                 "refunded": Decimal(0), "open": 0})
            s["orders"] += 1
            if o["status"] in ("paid", "shipped"):
                s["revenue"] += net
            elif o["status"] == "refunded":
                s["refunded"] += net
            else:
                s["open"] += 1
    rows = sorted(stats.items(), key=lambda kv: (-kv[1]["revenue"], kv[0]))
    lines = ["%-16s %6s %10s %10s %4s" % ("customer", "orders", "revenue", "refunded", "open")]
    total = Decimal(0)
    for name, s in rows:
        lines.append("%-16s %6d %10s %10s %4d" % (name, s["orders"], s["revenue"],
                                                 s["refunded"], s["open"]))
        total += s["revenue"]
    lines.append("%-16s %6d %10s" % ("all", sum(s["orders"] for s in stats.values()), total))
    lines += notes
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    out("wrote %s (%d customers, %d notes)" % (dest, len(rows), len(notes)))


def latency(src, dest):
    stats = {}
    with open(src, "rb") as f:
        try:
            for ev in backend.items(f, "", multiple_values=True, use_float=True, buf_size=128):
                s = stats.setdefault(ev["type"], [0, 0.0, 0.0])
                s[0] += 1
                s[1] += ev["ms"]
                s[2] = max(s[2], ev["ms"])
        except Exception as e:
            out(err(e))
            out("read %d events; nothing written" % sum(s[0] for s in stats.values()))
            return
    lines = ["type,count,mean_ms,max_ms"]
    for k in sorted(stats):
        n, total, top = stats[k]
        lines.append("%s,%d,%.3f,%r" % (k, n, total / n, top))
    with open(dest, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    out("wrote %s (%d types)" % (dest, len(stats)))


def schema(src):
    counts = {}
    with open(src, "rb") as f:
        for prefix, event, value in backend.parse(f):
            if event in ("map_key", "end_map", "end_array"):
                continue
            key = (prefix, event)
            counts[key] = counts.get(key, 0) + 1
    for (prefix, event), n in sorted(counts.items()):
        out("%-28s %-12s %d" % (prefix or "(root)", event, n))


def extract(src, prefix, dest):
    n = 0
    with open(src, "rb") as f, open(dest, "w", encoding="utf-8") as w:
        for obj in backend.items(f, prefix, use_float=True):
            w.write(json.dumps(obj) + "\n")
            n += 1
    out("wrote %s (%d lines)" % (dest, n))


def cat(path):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError as e:
        out(err(e))
        return
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    out(path, "(%d lines)" % len(lines))
    for ln in lines:
        print("  | " + ln)


def run(parts):
    cmd = parts[0]
    o, rest = options(parts[1:])
    if cmd == "version":
        out(ijson.__version__, backend.backend, ijson.backend)
    elif cmd in ("basic", "parse"):
        gen_job(cmd, rest[0], None, o)
    elif cmd in ("items", "kvitems", "count"):
        gen_job(cmd, rest[0], rest[1], o)
    elif cmd == "push":
        push(rest[0], rest[1], rest[2], o)
    elif cmd == "dump":
        dump(rest[0], o)
    elif cmd == "report":
        report(rest[0], rest[1])
    elif cmd == "latency":
        latency(rest[0], rest[1])
    elif cmd == "schema":
        schema(rest[0])
    elif cmd == "extract":
        extract(rest[0], rest[1], rest[2])
    elif cmd == "cat":
        cat(rest[0])
    else:
        raise SystemExit("unknown job " + cmd)


def main():
    os.makedirs("data/out", exist_ok=True)
    for name in os.listdir("data/out"):
        os.remove(os.path.join("data/out", name))
    with open("data/jobs.tsv", encoding="utf-8") as f:
        jobs = [ln for ln in f.read().split("\n") if ln]
    nerr = 0
    for job in jobs:
        parts = job.split("\t")
        print("> " + " ".join(parts))
        try:
            run(parts)
        except Exception as e:
            out(err(e))
            nerr += 1
    print("%d jobs, %d ended in an error" % (len(jobs), nerr))


main()
