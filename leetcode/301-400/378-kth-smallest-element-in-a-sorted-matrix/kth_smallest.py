# LeetCode #378: Kth Smallest Element in a Sorted Matrix -- mirror of
# kth_smallest.kara.


def count_at_most(matrix, x):
    n = len(matrix)
    count = 0
    row = n - 1
    col = 0
    while row >= 0 and col < n:
        if matrix[row][col] <= x:
            count += row + 1
            col += 1
        else:
            row -= 1
    return count


def kth_smallest(matrix, k):
    n = len(matrix)
    lo = matrix[0][0]
    hi = matrix[n - 1][n - 1]
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if count_at_most(matrix, mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def show(label, matrix, k):
    print(f"{label}: {kth_smallest(matrix, k)}")


def main():
    show("example 1", [[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8)
    show("example 2", [[-5]], 1)
    show("k = 1 is the corner", [[1, 2], [3, 4]], 1)
    show("k = n * n is the far corner", [[1, 2], [3, 4]], 4)
    show("rows overlap", [[1, 3, 5], [2, 4, 6], [3, 5, 7]], 5)
    show("all equal", [[7, 7, 7], [7, 7, 7], [7, 7, 7]], 6)
    show("duplicates across rows", [[1, 1, 3], [1, 2, 3], [3, 3, 3]], 4)
    show("negative and extreme values", [[-1000000000, -5], [0, 1000000000]], 3)
    # Random matrices up to 40 by 40: each value is the larger of its upper
    # and left neighbours plus a small step, which keeps rows and columns
    # sorted and makes repeats common.
    seed = 378
    checksum = 0
    for case in range(100):
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = 1 + (seed // 65536) % 40
        step = 3 if case % 2 == 0 else 1000
        seed = (seed * 1103515245 + 12345) % 2147483648
        base = (seed // 65536) % 2001 - 1000
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                seed = (seed * 1103515245 + 12345) % 2147483648
                d = (seed // 65536) % step
                if i == 0 and j == 0:
                    v = base
                elif i == 0:
                    v = row[j - 1] + d
                elif j == 0:
                    v = matrix[i - 1][0] + d
                else:
                    v = max(matrix[i - 1][j], row[j - 1]) + d
                row.append(v)
            matrix.append(row)
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = 1 + (seed // 65536) % (n * n)
        checksum = (checksum * 1009 + kth_smallest(matrix, k) + 1000000) % 1000000007
    print(f"100 random matrices: checksum {checksum}")


main()
