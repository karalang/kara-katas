#!/usr/bin/env python3
"""LeetCode #118 — Python mirror of the additive `generate.kara`.

Same algorithm: build each row from the previous (`row[j] = prev[j-1] + prev[j]`, edges 1). Produces
the byte-identical output to the Kara solvers (the oracle for this kata)."""

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
    small = generate(8)
    for r, row in enumerate(small):
        print(f"row {r}: " + " ".join(str(x) for x in row))

    acc = 0
    for n in range(1, 31):
        tri = generate(n)
        h = triangle_hash(tri)
        acc = (acc * 131 + h) % MOD
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
