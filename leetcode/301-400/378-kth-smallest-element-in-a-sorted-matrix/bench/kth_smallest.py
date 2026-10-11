# Benchmark for #378: mirror of kth_smallest.kara.


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


def main():
    n = 300
    seed = 378
    checksum = 0
    for _ in range(10):
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                seed = (seed * 1103515245 + 12345) % 2147483648
                d = (seed // 65536) % 10000
                if i == 0 and j == 0:
                    v = -1000000000
                elif i == 0:
                    v = row[j - 1] + d
                elif j == 0:
                    v = matrix[i - 1][0] + d
                else:
                    v = max(matrix[i - 1][j], row[j - 1]) + d
                row.append(v)
            matrix.append(row)
        for _ in range(10000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            k = 1 + (seed // 65536) % (n * n)
            checksum = (checksum * 1009 + kth_smallest(matrix, k) + 1000000000) % 1000000007
    print(f"checksum {checksum}")


main()
