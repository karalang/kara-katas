# LeetCode #363: Max Sum of Rectangle No Larger Than K -- mirror of
# max_sum.kara. A sorted list with bisect stands in for the SortedSet.
from bisect import bisect_left


def max_sum_submatrix(matrix, k):
    rows, cols = len(matrix), len(matrix[0])
    best = -(2**63)
    for top in range(rows):
        sums = [0] * cols
        for bottom in range(top, rows):
            for c in range(cols):
                sums[c] += matrix[bottom][c]
            seen = [0]
            prefix = 0
            for c in range(cols):
                prefix += sums[c]
                at = bisect_left(seen, prefix - k)
                if at < len(seen):
                    best = max(best, prefix - seen[at])
                i = bisect_left(seen, prefix)
                if i == len(seen) or seen[i] != prefix:
                    seen.insert(i, prefix)
    return best


def show(label, matrix, k):
    print(f"{label}: {max_sum_submatrix(matrix, k)}")


def main():
    show("example 1", [[1, 0, 1], [0, -2, 3]], 2)
    show("example 2", [[2, 2, -1]], 3)
    show("one cell equal to k", [[5]], 5)
    show("one cell below k", [[-7]], 0)
    show("only a negative run fits", [[3, -4, 3]], -1)
    show("negative k", [[-2, -3], [-1, -4]], -5)
    show("k above the total", [[1, 2], [3, 4]], 100)
    show("the best fit is not the largest", [[5, -4, -3, 4], [-3, -4, 4, 5], [5, 1, 5, -4]], 10)
    show("one column", [[2], [-1], [3], [-5], [4]], 3)
    show("values at the bounds", [[100, -100], [-100, 100]], 0)
    show("a wide row", [[3 if i % 2 == 0 else -2 for i in range(60)]], 7)

    seed = 363
    checksum = 0
    for _ in range(300):
        seed = (seed * 1103515245 + 12345) % 2147483648
        rows = 1 + (seed // 65536) % 12
        seed = (seed * 1103515245 + 12345) % 2147483648
        cols = 1 + (seed // 65536) % 12
        matrix = []
        least = 100
        for _ in range(rows):
            row = []
            for _ in range(cols):
                seed = (seed * 1103515245 + 12345) % 2147483648
                v = (seed // 65536) % 201 - 100
                least = min(least, v)
                row.append(v)
            matrix.append(row)
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = max(least, (seed // 65536) % 601 - 300)
        checksum = (checksum * 31 + max_sum_submatrix(matrix, k) + 1000000) % 1000000007
    print(f"300 random matrices: checksum {checksum}")


main()
