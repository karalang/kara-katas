# LeetCode #1388: Pizza With 3n Slices -- Python mirror of the ★ arm: the
# slices you get are any n of the 3n with no two side by side around the
# circle, so the answer is the better of two straight runs, without the
# last slice and without the first; in each, best[i][j] is the most from
# at most j slices, no two adjacent, among the first i.


def best_in_line(slices, n):
    length = len(slices)
    best = [[0] * (n + 1) for _ in range(length + 1)]
    for i in range(1, length + 1):
        for j in range(1, n + 1):
            skip = best[i - 1][j]
            take = (best[i - 2][j - 1] if i >= 2 else 0) + slices[i - 1]
            best[i][j] = max(skip, take)
    return best[length][n]


def max_size_slices(slices):
    n = len(slices) // 3
    return max(best_in_line(slices[:-1], n), best_in_line(slices[1:], n))


seed = 1388


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def pizza(length, most):
    return [1 + next_random() % most for _ in range(length)]


def main():
    shown = [
        max_size_slices([1, 2, 3, 4, 5, 6]),
        max_size_slices([8, 9, 8, 6, 1, 1]),
        max_size_slices([4, 1, 2]),
        max_size_slices([7, 7, 7, 7, 7, 7]),
        max_size_slices([5, 9, 6, 1, 1, 1]),
    ]
    print(" ".join(str(x) for x in shown))
    big = pizza(498, 1000)
    flat = [1000] * 498
    print(f"498 slices: {max_size_slices(big)}, and {max_size_slices(flat)} when all are 1000")
    check = 0
    total = 0
    for c in range(2000):
        length = 3 * (1 + next_random() % 20)
        most = 1000 if c % 2 == 0 else 3
        slices = pizza(length, most)
        got = max_size_slices(slices)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random pizzas: {total} in all, checksum {check}")


main()
