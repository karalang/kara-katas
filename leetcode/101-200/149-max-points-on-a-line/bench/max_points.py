"""Benchmark workload — Max Points on a Line, O(n^2 log n) sort-based variant.

Algorithmic mirror of bench/max_points.kara / .c / .rs / go-seq. See
../README.md § Benchmarks for N / K and the deterministic LCG generator.
"""

from math import gcd


def max_points(xs, ys):
    n = len(xs)
    if n <= 2:
        return n
    best = 1
    for i in range(n):
        slopes = []
        dup = 0
        xi, yi = xs[i], ys[i]
        for j in range(i + 1, n):
            dx = xs[j] - xi
            dy = ys[j] - yi
            if dx == 0 and dy == 0:
                dup += 1
                continue
            g = gcd(abs(dx), abs(dy))
            dx //= g
            dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx = -dx
                dy = -dy
            slopes.append(dx * 4096 + dy)
        slopes.sort()
        local = run = 0
        for k in range(len(slopes)):
            run = 1 if k == 0 or slopes[k] != slopes[k - 1] else run + 1
            if run > local:
                local = run
        cand = local + dup + 1
        if cand > best:
            best = cand
    return best


def main():
    N = 1200
    xs = [0] * N
    ys = [0] * N
    state = 12345
    for i in range(N):
        state = (state * 1103515245 + 12345) & 2147483647
        xs[i] = state & 1023
        state = (state * 1103515245 + 12345) & 2147483647
        ys[i] = state & 1023
    total = 0
    for _ in range(8):
        total += max_points(xs, ys)
    print(total)


main()
