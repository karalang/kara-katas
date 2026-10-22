#!/usr/bin/env python3
r"""Replays data/jobs.tsv against the vendored boltons.iterutils and writes
expected.out. Each op calls the real iterutils function with the key/predicate
its mode names, so the port is checked against the library's own behaviour. See
mk.py for the op table."""
import sys
sys.path.insert(0, "vendor")
from boltons import iterutils as IU  # noqa: E402

MODES_KEY = {
    "mod3": lambda x: x % 3,
    "even": lambda x: x % 2 == 0,
}
MODES_PRED = {
    "truthy": lambda x: x != 0,
    "even": lambda x: x % 2 == 0,
    "gt40": lambda x: x > 40,
}


def fl(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def fll(xss):
    return "[" + ", ".join(fl(xs) for xs in xss) + "]"


def fpairs(ps):
    return "[" + ", ".join("(" + ", ".join(str(x) for x in p) + ")" for p in ps) + "]"


def v_or_none(v):
    return "None" if v is None else str(v)


regs = []
out = []


def mkreg(xs):
    regs.append(list(xs))
    return "reg %d = %s" % (len(regs) - 1, fl(xs))


for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
    if not line:
        continue
    f = line.split("\t")
    op = f[0]
    if op == "new":
        out.append(mkreg([int(x) for x in f[1:]]))
    elif op == "split":
        out.append(fll(IU.split(regs[int(f[1])], int(f[2]))))
    elif op == "lstrip":
        out.append(fl(IU.lstrip(regs[int(f[1])], int(f[2]))))
    elif op == "rstrip":
        out.append(fl(IU.rstrip(regs[int(f[1])], int(f[2]))))
    elif op == "strip":
        out.append(fl(IU.strip(regs[int(f[1])], int(f[2]))))
    elif op == "chunked":
        out.append(fll(IU.chunked(regs[int(f[1])], int(f[2]))))
    elif op == "chunkfill":
        out.append(fll(IU.chunked(regs[int(f[1])], int(f[2]), fill=int(f[3]))))
    elif op == "cranges":
        isz, csz, off, ovl, align = (int(x) for x in f[1:6])
        out.append(fpairs(list(IU.chunk_ranges(isz, csz, input_offset=off,
                                               overlap_size=ovl, align=bool(align)))))
    elif op == "pairwise":
        out.append(fpairs(IU.pairwise(regs[int(f[1])])))
    elif op == "pairend":
        out.append(fpairs(IU.pairwise(regs[int(f[1])], end=int(f[2]))))
    elif op == "windowed":
        out.append(fpairs(IU.windowed(regs[int(f[1])], int(f[2]))))
    elif op == "winfill":
        out.append(fpairs(IU.windowed(regs[int(f[1])], int(f[2]), fill=int(f[3]))))
    elif op == "bucket":
        bk = IU.bucketize(regs[int(f[1])], key=MODES_KEY[f[2]])
        if f[2] == "even":
            disp = {k: v for k, v in bk.items()}
            out.append("{" + ", ".join("%s: %s" % ("True" if k else "False", fl(v))
                                       for k, v in disp.items()) + "}")
        else:
            out.append("{" + ", ".join("%s: %s" % (k, fl(v)) for k, v in bk.items()) + "}")
    elif op == "part1":
        parts = IU.partition(regs[int(f[1])], MODES_PRED[f[2]])
        out.append("(" + ", ".join(fl(p) for p in parts) + ")")
    elif op == "part2":
        parts = IU.partition(regs[int(f[1])], lambda i: i > 0, lambda i: i < 0)
        out.append("(" + ", ".join(fl(p) for p in parts) + ")")
    elif op == "unique":
        out.append(fl(IU.unique(regs[int(f[1])])))
    elif op == "redund":
        out.append(fl(IU.redundant(regs[int(f[1])])))
    elif op == "redundg":
        out.append(fll(IU.redundant(regs[int(f[1])], groups=True)))
    elif op == "one":
        out.append(v_or_none(IU.one(regs[int(f[1])], key=MODES_PRED[f[2]])))
    elif op == "first":
        out.append(v_or_none(IU.first(regs[int(f[1])], key=MODES_PRED[f[2]])))
    elif op == "same":
        out.append("yes" if IU.same(regs[int(f[1])]) else "no")
    elif op == "sameref":
        out.append("yes" if IU.same(regs[int(f[1])], ref=int(f[2])) else "no")
    else:
        raise SystemExit("unknown op %r" % op)

sys.stdout.write("\n".join(out) + "\n")
