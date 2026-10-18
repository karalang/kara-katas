#!/usr/bin/env python3
"""Runs data/jobs.tsv with Python's itertools and prints expected.out."""
import csv
import operator
from itertools import (accumulate, batched, chain, combinations,
                       combinations_with_replacement, compress, count, cycle,
                       dropwhile, filterfalse, groupby, islice, pairwise,
                       permutations, product, repeat, takewhile, zip_longest)


def ints(field):
    if field in ("", "-"):
        return []
    return [int(x) for x in field.split(",")]


def lists(field):
    return [ints(g) for g in field.split(";")]


OPS = {"add": operator.add, "mul": operator.mul, "max": max, "min": min}


def report(path):
    with open("data/" + path[1:]) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["units"] = int(r["units"])
        r["price"] = int(r["price"])
    rev = lambda r: r["units"] * r["price"]

    print("  by region:")
    for region, g in groupby(sorted(rows, key=lambda r: r["region"]), key=lambda r: r["region"]):
        g = list(g)
        print(f"    {region}: {len(g)} rows, {sum(r['units'] for r in g)} units, revenue {sum(map(rev, g))}")

    print("  by month:")
    months = [(m, sum(r["units"] for r in g)) for m, g in groupby(rows, key=lambda r: r["month"])]
    for (m, u), run in zip(months, accumulate(u for _, u in months)):
        print(f"    {m} {u} running {run}")
    for (m1, u1), (m2, u2) in pairwise(months):
        print(f"    {m1} -> {m2}: {u2 - u1:+d}")

    print("  pages:")
    for i, page in enumerate(batched(rows, 4), 1):
        print(f"    page {i}: {' '.join(r['product'] for r in page)}")

    print("  bundles:")
    price = {}
    for r in rows:
        price[r["product"]] = max(price.get(r["product"], 0), r["price"])
    for a, b in combinations(sorted(price), 2):
        print(f"    {a} + {b} = {price[a] + price[b]}")

    print("  skus: " + " ".join(f"{s}-{c}" for s, c in product(["S", "M", "L"], ["red", "blue"])))

    kept = list(takewhile(lambda p: p[1] <= 600, zip(rows, accumulate(map(rev, rows)))))
    print(f"  budget 600: {len(kept)} rows, spent {kept[-1][1] if kept else 0}")

    print("  tickets:")
    for (i, r), agent in zip(enumerate(islice(rows, 7), 1), cycle(["ana", "ben", "cy"])):
        print(f"    ticket {i} {r['product']} -> {agent}")

    print("  promo: " + " ".join(r["product"] for r in compress(rows, (r["promo"] == "1" for r in rows))))

    north = [r["units"] for r in rows if r["region"] == "north"]
    south = [r["units"] for r in rows if r["region"] == "south"]
    print(f"  north vs south: {list(zip_longest(north, south, fillvalue=0))}")

    print("  big orders:")
    for n, r in zip(count(1), filterfalse(lambda r: r["units"] < 5, rows)):
        print(f"    {n}. {r['month']} {r['region']} {r['product']} {r['units']}")

    print(f"  from march: {len(list(dropwhile(lambda r: r['month'] < '2026-03', rows)))} rows")


def run(f):
    k = f[0]
    if k == "count":
        r = list(islice(count(int(f[1]), int(f[2])), int(f[3])))
    elif k == "cycle":
        r = list(islice(cycle(ints(f[1])), int(f[2])))
    elif k == "repeat":
        r = list(repeat(int(f[1]), int(f[2])))
    elif k == "accumulate":
        init = None if f[3] == "-" else int(f[3])
        r = list(accumulate(ints(f[1]), OPS[f[2]], initial=init))
    elif k == "batched":
        r = list(batched(ints(f[1]), int(f[2])))
    elif k == "chain":
        r = list(chain(*lists(f[1])))
    elif k == "compress":
        r = list(compress(ints(f[1]), ints(f[2])))
    elif k == "dropwhile":
        r = list(dropwhile(lambda x: x < int(f[2]), ints(f[1])))
    elif k == "takewhile":
        r = list(takewhile(lambda x: x < int(f[2]), ints(f[1])))
    elif k == "filterfalse":
        r = list(filterfalse(lambda x: x % 2 == 1, ints(f[1])))
    elif k == "groupby":
        key = (lambda x: x) if f[2] == "same" else (lambda x: x % 2)
        r = [(k2, list(g)) for k2, g in groupby(ints(f[1]), key)]
    elif k == "islice":
        stop = None if f[3] == "-" else int(f[3])
        r = list(islice(ints(f[1]), int(f[2]), stop, int(f[4])))
    elif k == "pairwise":
        r = list(pairwise(ints(f[1])))
    elif k == "zip_longest":
        r = list(zip_longest(ints(f[1]), ints(f[2]), fillvalue=int(f[3])))
    elif k == "product":
        r = list(product(*lists(f[1]), repeat=int(f[2])))
    elif k == "permutations":
        r = list(permutations(ints(f[1]), None if f[2] == "-" else int(f[2])))
    elif k == "combinations":
        r = list(combinations(ints(f[1]), int(f[2])))
    elif k == "cwr":
        r = list(combinations_with_replacement(ints(f[1]), int(f[2])))
    elif k == "report":
        report(f[1])
        return
    print(f"  {r}")


with open("data/jobs.tsv") as fh:
    for raw in fh:
        fields = raw.rstrip("\n").split("\t")
        print("== " + " | ".join(fields))
        run(fields)
