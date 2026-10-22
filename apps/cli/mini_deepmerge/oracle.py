#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored deepmerge and prints expected.out.
mini_deepmerge.kara must reproduce this byte-for-byte on every backend.

Each job is `merge <merger> <base> <nxt>`. The two values are parsed from a
tiny JSON-with-sets grammar, merged with the named deepmerge strategy
configuration, and the result serialized back into the same grammar. A merger
that raises (merge_or_raise on a scalar merge or type conflict) prints RAISE.

Sets are serialized in a canonical order (null < false < true < ints <
strings) so the output does not depend on Python's per-process set ordering.
"""
import sys

sys.path.insert(0, "vendor")
from deepmerge import Merger  # noqa: E402
from deepmerge.exception import InvalidMerge  # noqa: E402

# Strategy configurations, mirrored verbatim in mini_deepmerge.kara.
MERGERS = {
    "always": Merger([(list, "append"), (dict, "merge"), (set, "union")],
                     ["override"], ["override"]),
    "conservative": Merger([(list, "append"), (dict, "merge"), (set, "union")],
                           ["use_existing"], ["use_existing"]),
    "raise": Merger([(list, "append"), (dict, "merge"), (set, "union")], [], []),
    "prepend": Merger([(list, "prepend"), (dict, "override"), (set, "union")],
                      ["override"], ["override"]),
    "unique": Merger([(list, "append_unique"), (dict, "merge"), (set, "union")],
                     ["override"], ["override"]),
    "intersect": Merger([(list, "append"), (dict, "merge"), (set, "intersect")],
                        ["override"], ["override"]),
    "setoverride": Merger([(list, "append"), (dict, "merge"), (set, "override")],
                          ["override"], ["override"]),
    "ifnotempty": Merger([(list, "append"), (dict, "merge"), (set, "union")],
                         ["override"], ["override_if_not_empty"]),
}


# ---- value grammar: parse ----------------------------------------------------
class P:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t":
            self.i += 1

    def value(self):
        self.ws()
        c = self.s[self.i]
        if c == "[":
            return self.seq("[", "]", list)
        if c == "<":
            return self.seq("<", ">", set)
        if c == "{":
            return self.dict()
        if c == '"':
            return self.string()
        return self.atom()

    def seq(self, op, cl, make):
        self.i += 1  # op
        items = []
        self.ws()
        if self.s[self.i] == cl:
            self.i += 1
            return make(items)
        while True:
            items.append(self.value())
            self.ws()
            if self.s[self.i] == ",":
                self.i += 1
                continue
            break
        self.ws()
        assert self.s[self.i] == cl
        self.i += 1
        return make(items)

    def dict(self):
        self.i += 1  # {
        d = {}
        self.ws()
        if self.s[self.i] == "}":
            self.i += 1
            return d
        while True:
            self.ws()
            k = self.string()
            self.ws()
            assert self.s[self.i] == ":"
            self.i += 1
            d[k] = self.value()
            self.ws()
            if self.s[self.i] == ",":
                self.i += 1
                continue
            break
        self.ws()
        assert self.s[self.i] == "}"
        self.i += 1
        return d

    def string(self):
        assert self.s[self.i] == '"'
        self.i += 1
        start = self.i
        while self.s[self.i] != '"':
            self.i += 1
        out = self.s[start:self.i]
        self.i += 1
        return out

    def atom(self):
        start = self.i
        while self.i < len(self.s) and self.s[self.i] not in " \t,]}>":
            self.i += 1
        tok = self.s[start:self.i]
        if tok == "null":
            return None
        if tok == "true":
            return True
        if tok == "false":
            return False
        return int(tok)


def parse(s):
    return P(s).value()


# ---- value grammar: serialize ------------------------------------------------
def _rank(x):
    if x is None:
        return (0, 0, "")
    if isinstance(x, bool):
        return (1, int(x), "")
    if isinstance(x, int):
        return (2, x, "")
    return (3, 0, x)


def ser(x):
    if x is None:
        return "null"
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, int):
        return str(x)
    if isinstance(x, str):
        return '"' + x + '"'
    if isinstance(x, list):
        return "[" + ", ".join(ser(e) for e in x) + "]"
    if isinstance(x, set):
        return "<" + ", ".join(ser(e) for e in sorted(x, key=_rank)) + ">"
    if isinstance(x, dict):
        return "{" + ", ".join('"' + k + '": ' + ser(v) for k, v in x.items()) + "}"
    raise TypeError(type(x))


def run(fields):
    merger = MERGERS[fields[1]]
    base = parse(fields[2])
    nxt = parse(fields[3])
    try:
        return ser(merger.merge(base, nxt))
    except InvalidMerge:
        return "RAISE"


def main():
    chunks = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        f = line.split("\t")
        header = "== " + f[1] + " | " + f[2] + " | " + f[3]
        chunks.append(header + "\n  " + run(f) + "\n")
    sys.stdout.write("".join(chunks))


if __name__ == "__main__":
    main()
