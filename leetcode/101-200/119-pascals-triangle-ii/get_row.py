#!/usr/bin/env python3
"""LeetCode #119 — Python mirror of the in-place rolling `get_row.kara`.
Same algorithm: one row, updated in place right-to-left (`row[j] += row[j-1]`). Produces the
byte-identical output to the Kara solvers (the oracle for this kata)."""

MOD = 1000000007


def get_row(row_index):
    row = [1] * (row_index + 1)
    for i in range(2, row_index + 1):
        for k in range(i - 1, 0, -1):
            row[k] = row[k] + row[k - 1]
    return row


def row_hash(row):
    h = 1
    for x in row:
        h = (h * 131 + x) % MOD
    return (h * 31 + len(row) + 7) % MOD


def main():
    for r in range(7):
        print(f"row {r}: " + " ".join(str(x) for x in get_row(r)))
    acc = 0
    for n in range(34):
        h = row_hash(get_row(n))
        acc = (acc * 131 + h) % MOD
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
