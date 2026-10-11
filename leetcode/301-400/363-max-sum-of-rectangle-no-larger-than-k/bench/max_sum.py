# Benchmark for #363 -- mirror of max_sum.kara (the merge-sort arm).
import sys

MIN = -(2**63)


def best_pair(p, lo, hi, k, scratch):
    if hi - lo < 2:
        return MIN
    mid = (lo + hi) // 2
    best = max(best_pair(p, lo, mid, k, scratch), best_pair(p, mid, hi, k, scratch))
    j = mid
    for i in range(lo, mid):
        while j < hi and p[j] <= p[i] + k:
            j += 1
        if j > mid:
            best = max(best, p[j - 1] - p[i])
    a, b, out = lo, mid, lo
    while a < mid or b < hi:
        if b == hi or (a < mid and p[a] <= p[b]):
            scratch[out] = p[a]
            a += 1
        else:
            scratch[out] = p[b]
            b += 1
        out += 1
    p[lo:hi] = scratch[lo:hi]
    return best


def max_sum_submatrix(matrix, k):
    rows, cols = len(matrix), len(matrix[0])
    best = MIN
    scratch = [0] * (cols + 1)
    for top in range(rows):
        sums = [0] * cols
        for bottom in range(top, rows):
            row = matrix[bottom]
            for c in range(cols):
                sums[c] += row[c]
            prefix = [0] * (cols + 1)
            for c in range(cols):
                prefix[c + 1] = prefix[c] + sums[c]
            best = max(best, best_pair(prefix, 0, cols + 1, k, scratch))
    return best


def main():
    seed = 363
    checksum = 0
    for _ in range(20):
        matrix = []
        least = 100
        for _ in range(100):
            row = []
            for _ in range(100):
                seed = (seed * 1103515245 + 12345) % 2147483648
                v = (seed // 65536) % 201 - 100
                least = min(least, v)
                row.append(v)
            matrix.append(row)
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = max(least, (seed // 65536) % 20001 - 10000)
        checksum = (checksum * 31 + max_sum_submatrix(matrix, k) + 1000000) % 1000000007
    print(f"checksum {checksum}")


main()
