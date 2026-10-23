#!/usr/bin/env python3
r"""Replays data/jobs.tsv through the vendored python-constraint library and
writes expected.out. Each line is a CSP spec (see mk.py); for each the oracle
builds the problem with the library's own Problem / BacktrackingSolver,
AllDifferentConstraint and FunctionConstraint, enumerates every solution with
getSolutions(), and prints:

    <job line> => <count>
    <v0 v1 ... v_{V-1}>        one line per solution, values in variable order,
    ...                        in the library's own enumeration order

mini_constraint.kara reproduces this byte-for-byte on every backend. The
solution order is the backtracking solver's, so it exercises the MRV+degree
variable heuristic, forward checking and the domain push/pop state stack, not
just the solution set."""
import sys

sys.path.insert(0, "vendor")
import constraint as C  # noqa: E402


def row(line):
    toks = line.split(" ")
    kind = toks[0]
    p = C.Problem()
    if kind == "queens" or kind == "rooks":
        n = int(toks[1])
        V = n
        for x in range(n):
            p.addVariables([x], list(range(n)))
        for i in range(n):
            for j in range(n):
                if i < j:
                    if kind == "rooks":
                        p.addConstraint(lambda a, b: a != b, [i, j])
                    else:
                        cd = j - i
                        p.addConstraint(
                            (lambda cd: (lambda a, b: abs(a - b) != cd and a != b))(cd),
                            [i, j])
    elif kind == "color":
        V = int(toks[1])
        k = int(toks[2])
        for x in range(V):
            p.addVariables([x], list(range(k)))
        for tok in toks[3:]:
            a, b = tok.split("-")
            p.addConstraint(lambda x, y: x != y, [int(a), int(b)])
    else:  # alldiff
        V = int(toks[1])
        for x in range(V):
            dom = [int(z) for z in toks[2 + x].split(",")]
            p.addVariables([x], dom)
        p.addConstraint(C.AllDifferentConstraint())

    sols = p.getSolutions()
    out = [line + " => " + str(len(sols))]
    for s in sols:
        out.append(" ".join(str(s[v]) for v in range(V)))
    return "\n".join(out)


def main():
    out = []
    for line in open("data/jobs.tsv", encoding="utf-8").read().split("\n"):
        if line == "":
            continue
        out.append(row(line))
    sys.stdout.write("\n".join(out) + "\n")


main()
