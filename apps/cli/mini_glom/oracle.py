#!/usr/bin/env python3
r"""Runs data/jobs.tsv through the vendored glom and prints expected.out.
mini_glom.kara must reproduce this byte-for-byte on every backend.

Each job is `<spec-dsl>\t<json-target>`. The spec DSL is a small textual
encoding — shared by this oracle and the Kara port — of the glom specs the
port supports; `build_spec` turns it into a real glom spec object:

  P <path>                 glom(t, "<path>")           path access
  V <json>                 glom(t, Val(<json>))        a literal value
  D k1=<path>;k2=<path>    glom(t, {k1: "<path>", ...}) dict restructure
  I <path>                 glom(t, ["<path>"])          map a path over a list
  T <outer> | <inner>      glom(t, ("<outer>", ["<inner>"]))  nav + map
  C p1 || p2 [=> <json>]   glom(t, Coalesce(p1, p2, [default=<json>]))

A path is dotted (`a.b.c`, `users.0.name`); a digit segment indexes a list.
A success prints the result via json.dumps' default separators; a GlomError
prints its final (most specific) line — the `glom.core.<Error>: ...` summary.
The multi-line target-spec trace header is out of scope (see README).
"""
import json
import sys

sys.path.insert(0, "vendor")
from glom import glom, Coalesce, Val, GlomError  # noqa: E402


def build_spec(dsl):
    kind = dsl[0]
    rest = dsl[2:] if len(dsl) > 1 else ""
    if kind == "P":
        return rest
    if kind == "V":
        return Val(json.loads(rest))
    if kind == "D":
        d = {}
        for pair in rest.split(";"):
            k, _, p = pair.partition("=")
            d[k] = p
        return d
    if kind == "I":
        return [rest]
    if kind == "T":
        outer, _, inner = rest.partition(" | ")
        return (outer, [inner])
    if kind == "C":
        body, sep, dflt = rest.partition(" => ")
        subs = body.split(" || ")
        if sep:
            return Coalesce(*subs, default=json.loads(dflt))
        return Coalesce(*subs)
    raise ValueError("bad dsl " + dsl)


def run(dsl, target):
    try:
        return json.dumps(glom(target, build_spec(dsl)), separators=(", ", ": "))
    except GlomError as e:
        return str(e).splitlines()[-1]


def main():
    chunks = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().splitlines():
        if not line:
            continue
        dsl, target = line.split("\t")
        chunks.append("== " + dsl + " | " + target + "\n  " + run(dsl, json.loads(target)) + "\n")
    sys.stdout.write("".join(chunks))


if __name__ == "__main__":
    main()
