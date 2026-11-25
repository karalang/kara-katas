# LeetCode #1395: Count Number of Teams -- Python mirror of the ★ arm:
# each soldier taken as the middle of a team, the smaller and the larger
# ratings counted on each side of it.


def num_teams(rating):
    n = len(rating)
    teams = 0
    for j in range(n):
        less_left = greater_left = less_right = greater_right = 0
        for i in range(j):
            if rating[i] < rating[j]:
                less_left += 1
            else:
                greater_left += 1
        for k in range(j + 1, n):
            if rating[k] < rating[j]:
                less_right += 1
            else:
                greater_right += 1
        teams += less_left * greater_right + greater_left * less_right
    return teams


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n distinct ratings: 1 to n shuffled, each times a scale from 1 to `most`
def drawn(n, most):
    out = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        out[i], out[j] = out[j], out[i]
    scale = 1 + next_random() % most
    return [v * scale for v in out]


def main():
    global seed
    shown = [num_teams(r) for r in [[2, 5, 3, 4, 1], [2, 1, 3], [1, 2, 3, 4], [3, 2, 1], [1, 3, 2]]]
    print(" ".join(str(x) for x in shown))
    seed = 1395
    big = [num_teams(list(range(1, 1001))), num_teams(list(range(100000, 99000, -1))), num_teams(drawn(1000, 100))]
    print("1000 soldiers: " + " ".join(str(x) for x in big))
    check = 0
    total = 0
    for _ in range(2000):
        n = 3 + next_random() % 38
        got = num_teams(drawn(n, 100))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random lines: {total} teams in all, checksum {check}")


main()
