# LeetCode #1074: Number of Submatrices That Sum to Target -- the
# benchmark's Python mirror of submatrix_sum.kara: the same row pairs and
# dict of running totals, over 30 matrices of 100 by 100 built once, each
# counted for three targets.


def num_submatrix_sum_target(matrix, target):
    m, n = len(matrix), len(matrix[0])
    count = 0
    for top in range(m):
        column = [0] * n
        for bottom in range(top, m):
            row = matrix[bottom]
            for c in range(n):
                column[c] += row[c]
            seen = {0: 1}
            total = 0
            for c in range(n):
                total += column[c]
                count += seen.get(total - target, 0)
                seen[total] = seen.get(total, 0) + 1
    return count


seed = 1074


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    matrices = [[[next_random() % 7 - 3 for _ in range(100)] for _ in range(100)] for _ in range(30)]
    total = check = 0
    for matrix in matrices:
        for target in (-5, 0, 7):
            x = num_submatrix_sum_target(matrix, target)
            total += x
            check = (check * 31 + x) % 1000000007
    print(f"90 calls: {total} submatrices, checksum {check}")


main()
