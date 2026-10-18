#!/usr/bin/env python3
"""Runs data/jobs.tsv with Python's fractions and prints expected.out."""
import math
from fractions import Fraction as F

# Exact unit factors, to a common base unit per dimension.
UNITS = {
    "in": F(254, 10), "mm": F(1), "mi": F(1609344, 1000) * 1000, "km": F(1000000),
    "cup": F("236.5882365"), "ml": F(1), "tbsp": F("14.78676478125"), "tsp": F("4.92892159375"),
}


def show(x):
    return f"{x!r} = {x}"


def mixed(q):
    """A cook's quantity: 1 1/2, 3/4, 2."""
    whole = q.numerator // q.denominator
    rest = q - whole
    if rest == 0:
        return str(whole)
    if whole == 0:
        return str(rest)
    return f"{whole} {rest}"


def parse_mixed(s):
    total = F(0)
    for part in s.split(" "):
        total += F(part)
    return total


def run(f):
    k = f[0]
    if k == "new":
        try:
            print(f"  {show(F(f[1]))}")
        except (ValueError, ZeroDivisionError) as e:
            print(f"  {type(e).__name__}: {e}")
    elif k == "pair":
        try:
            print(f"  {show(F(int(f[1]), int(f[2])))}")
        except ZeroDivisionError as e:
            print(f"  ZeroDivisionError: {e}")
    elif k == "op":
        a, op, b = F(f[1]), f[2], F(f[3])
        try:
            if op == "+": r = a + b
            elif op == "-": r = a - b
            elif op == "*": r = a * b
            elif op == "/": r = a / b
            elif op == "//": r = a // b
            elif op == "%": r = a % b
            elif op == "divmod": r = divmod(a, b)
            elif op == "**": r = a ** int(b)
            elif op == "<": r = a < b
            elif op == "==": r = a == b
            elif op == ">=": r = a >= b
            elif op == "!=": r = a != b
            if isinstance(r, F):
                print(f"  {show(r)}")
            else:
                print(f"  {r!r}")
        except ZeroDivisionError as e:
            print(f"  ZeroDivisionError: {e}")
    elif k == "limit":
        try:
            print(f"  {show(F(f[1]).limit_denominator(int(f[2])))}")
        except ValueError as e:
            print(f"  ValueError: {e}")
    elif k == "round":
        x = F(f[1])
        r = round(x) if f[2] == "-" else round(x, int(f[2]))
        print(f"  {r!r}")
    elif k == "ints":
        x = F(f[1])
        print(f"  floor {math.floor(x)} ceil {math.ceil(x)} trunc {math.trunc(x)} int {int(x)} integer {x.is_integer()} ratio {x.as_integer_ratio()}")
    elif k == "format":
        try:
            print(f"  [{format(F(f[1]), f[2])}]")
        except ValueError as e:
            print(f"  ValueError: {e}")
    elif k == "recipe":
        factor = F(f[2])
        for line in open("data/" + f[1][1:]):
            q, unit, name = line.rstrip("\n").split("\t")
            scaled = parse_mixed(q) * factor
            u = "" if unit == "-" else unit + " "
            print(f"  {mixed(scaled):>6} {u}{name}")
    elif k == "bill":
        tip = F(int(f[2]), 100)
        owed = {}
        total = 0
        for line in open("data/" + f[1][1:]):
            item, cents, who = line.rstrip("\n").split("\t")
            cents = int(cents)
            total += cents
            people = who.split(",")
            for p in people:
                owed[p] = owed.get(p, F(0)) + F(cents, len(people))
        grand = F(total) * (1 + tip)
        exact = {p: v * (1 + tip) for p, v in owed.items()}
        # Largest-remainder rounding to whole cents, so the shares add up.
        floors = {p: math.floor(v) for p, v in exact.items()}
        left = math.floor(grand + F(1, 2)) - sum(floors.values())
        order = sorted(exact, key=lambda p: (-(exact[p] - floors[p]), p))
        for p in order[:left]:
            floors[p] += 1
        for p in sorted(exact):
            c = floors[p]
            print(f"  {p:<4} exact {exact[p]!s:>12}  pays {c // 100}.{c % 100:02d}")
        t = sum(floors.values())
        print(f"  total {total // 100}.{total % 100:02d} + {f[2]}% = {t // 100}.{t % 100:02d}")
    elif k == "convert":
        x = F(f[1]) * UNITS[f[2]] / UNITS[f[3]]
        print(f"  {f[1]} {f[2]} = {x} {f[3]} ~ {x:.4f}")


for raw in open("data/jobs.tsv"):
    fields = raw.rstrip("\n").split("\t")
    print("== " + " | ".join(fields))
    run(fields)
