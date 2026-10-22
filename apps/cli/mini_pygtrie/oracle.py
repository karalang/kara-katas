#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored pygtrie.CharTrie and writes
expected.out. Sorted-sibling iteration is enabled so the key order is total and
deterministic (and so it matches on every backend and across languages).

Each op prints one line (see mk.py for the full table):
    s/d -> `len <n>` (or `short` / `miss` for a delete)
    g   -> the value, or `miss`
    hk/hs -> yes / no          hn -> the has_node bit-field (0..3)
    sp/lp -> `<key> <val>`, or `none`
    pf  -> `[(k v), ...]`      ks -> `[k, ...]`, or `nokey`
    ka  -> all keys, sorted    l  -> `len <n>`

The vendored pygtrie is a single pure-Python module, so oracle.py runs exactly
the code mini_pygtrie.kara mirrors.
"""
import sys

sys.path.insert(0, "vendor")
import pygtrie  # noqa: E402


def fmt_step(step):
    # step is falsy (a _NoneStep) when no prefix matched.
    if not step:
        return "none"
    return "%s %d" % (step.key, step.value)


t = pygtrie.CharTrie()
t.enable_sorting(True)
out = []
for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "s":
        k, v = f[1], int(f[2])
        t[k] = v
        out.append("len %d" % len(t))
    elif op == "g":
        k = f[1]
        v = t.get(k, None)
        out.append("miss" if v is None else str(v))
    elif op == "hk":
        out.append("yes" if t.has_key(f[1]) else "no")
    elif op == "hs":
        out.append("yes" if t.has_subtrie(f[1]) else "no")
    elif op == "hn":
        out.append(str(t.has_node(f[1])))
    elif op == "d":
        k = f[1]
        try:
            del t[k]
            out.append("len %d" % len(t))
        except pygtrie.ShortKeyError:
            out.append("short")
        except KeyError:
            out.append("miss")
    elif op == "lp":
        out.append(fmt_step(t.longest_prefix(f[1])))
    elif op == "sp":
        out.append(fmt_step(t.shortest_prefix(f[1])))
    elif op == "pf":
        parts = ["(%s %d)" % (s.key, s.value) for s in t.prefixes(f[1])]
        out.append("[" + ", ".join(parts) + "]")
    elif op == "ks":
        try:
            out.append("[" + ", ".join(t.keys(prefix=f[1])) + "]")
        except KeyError:
            out.append("nokey")
    elif op == "ka":
        out.append("[" + ", ".join(t.keys()) + "]")
    elif op == "l":
        out.append("len %d" % len(t))
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
