# LeetCode #1572: Matrix Diagonal Sum -- the Python mirror of the ★ arm:
# each row's two diagonal cells added by index, and the centre, which both
# diagonals share in an odd matrix, taken off once. O(n)


def diagonal_sum(mat):
    n = len(mat)
    total = 0
    for i in range(n):
        total += mat[i][i] + mat[i][n - 1 - i]
    if n % 2 == 1:
        total -= mat[n // 2][n // 2]
    return total


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % most + 1
        mat = [[next_random() % top + 1 for _ in range(n)] for _ in range(n)]
        s = diagonal_sum(mat)
        total += s
        check = mix(check, s)
    print(f"{count} matrices of up to {most} rows: sums total {total}, checksum {check}")


def main():
    global seed
    examples = [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
        [[5]],
        [[1, 2], [3, 4]],
        [[100, 1, 100], [1, 100, 1], [100, 1, 100]],
    ]
    for mat in examples:
        print(f"{mat} -> {diagonal_sum(mat)}")
    seed = 1572
    batch(3000, 5, 3)
    batch(3000, 100, 100)


main()
