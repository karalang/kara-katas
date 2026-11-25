# LeetCode #1395 bench, Python mirror of the ★ arm.


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


seed = 1395


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    n = 1000
    rating = [v * 97 for v in range(1, n + 1)]
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        rating[i], rating[j] = rating[j], rating[i]
    check = 0
    for _ in range(300):
        seed = (seed + check) % 2147483648
        a = next_random() % n
        b = next_random() % n
        rating[a], rating[b] = rating[b], rating[a]
        check = (check * 131 + num_teams(rating)) % 1000000007
    print(f"300 rounds over 1000 soldiers: checksum {check}")


main()
