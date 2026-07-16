#!/usr/bin/env python3
"""LeetCode #118 — Python bench mirror (smaller K, timed separately, NOT cross-checked).
Same additive algorithm as generate.kara; K = 4000 (pure-Python is ~20x slower per rep). Its
wall-clock is not comparable to the compiled mirrors."""

MOD = 1000000007


def generate(num_rows):
    tri = []
    for i in range(num_rows):
        row = []
        for j in range(i + 1):
            if j == 0 or j == i:
                row.append(1)
            else:
                row.append(tri[i - 1][j - 1] + tri[i - 1][j])
        tri.append(row)
    return tri


def triangle_hash(tri):
    h = 1
    for row in tri:
        for x in row:
            h = (h * 131 + x) % MOD
        h = (h * 31 + len(row) + 7) % MOD
    return h


def main():
    acc = 0
    for _ in range(4000):
        rows = 30 + (acc % 16)
        tri = generate(rows)
        h = triangle_hash(tri)
        acc = (acc * 131 + h) % MOD
    print(acc)


if __name__ == "__main__":
    main()
