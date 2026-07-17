#!/usr/bin/env python3
"""LeetCode #119 — Python bench mirror (smaller K, timed separately, NOT cross-checked).
Same in-place algorithm as get_row.kara; K = 22000. Its wall-clock is not comparable."""
MOD = 1000000007
def get_row(ri):
    row = [1] * (ri + 1)
    for i in range(2, ri + 1):
        for k in range(i - 1, 0, -1):
            row[k] = row[k] + row[k - 1]
    return row
def row_hash(row):
    h = 1
    for x in row:
        h = (h * 131 + x) % MOD
    return (h * 31 + len(row) + 7) % MOD
def main():
    acc = 0
    for _ in range(22000):
        ri = 30 + (acc % 20)
        acc = (acc * 131 + row_hash(get_row(ri))) % MOD
    print(acc)
if __name__ == "__main__":
    main()
