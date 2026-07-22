"""LeetCode 170 — Two Sum III - Data structure design (Python mirror / oracle).

A struct + free functions over a Map[number -> count]: add bumps the count, find
scans the distinct keys and checks for a complement (a self-pair needs count>=2).
Mirrors the Kāra version. Premium.
"""


class TwoSum:
    def __init__(self):
        self.counts = {}


def add(ds, number):
    ds.counts[number] = ds.counts.get(number, 0) + 1


def find(ds, value):
    for k in ds.counts:
        complement = value - k
        if complement == k:
            if ds.counts[k] >= 2:
                return True
        elif complement in ds.counts:
            return True
    return False


def report(ds, value):
    print("true" if find(ds, value) else "false")


def main():
    ds = TwoSum()
    add(ds, 1)
    add(ds, 3)
    add(ds, 5)
    report(ds, 4)   # true
    report(ds, 7)   # false
    report(ds, 6)   # true
    report(ds, 8)   # true

    add(ds, 3)
    report(ds, 6)   # true

    report(ds, 2)   # false

    add(ds, 0)
    report(ds, 0)   # false
    add(ds, 0)
    report(ds, 0)   # true
    report(ds, 10)  # false


main()
