# LeetCode #1388 bench -- Python: the ★ arm: the better of two straight
# runs, without the last slice and without the first; in each,
# best[i][j] is the most from at most j slices, no two adjacent, among
# the first i.


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


def main():
    global seed
    length = 498
    slices = [1 + next_random() % 1000 for _ in range(length)]
    check = 0
    for _ in range(1000):
        seed = (seed + check) % 2147483648
        at = next_random() % length
        slices[at] = 1 + next_random() % 1000
        check = (check * 131 + max_size_slices(slices)) % 1000000007
    print(f"1000 rounds over 498 slices: checksum {check}")


main()
