# LeetCode #712: Minimum ASCII Delete Sum for Two Strings -- a table
# of prefixes.
#
# A mirror of minimum_ascii_delete_sum_for_two_strings.kara (the ★ arm)
# and its harness.

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def minimum_delete_sum(s1, s2):
    a = s1.encode()
    b = s2.encode()
    m, n = len(a), len(b)
    cost = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        cost[i][0] = cost[i - 1][0] + a[i - 1]
    for j in range(1, n + 1):
        cost[0][j] = cost[0][j - 1] + b[j - 1]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cost[i][j] = cost[i - 1][j - 1]
            else:
                drop_a = cost[i - 1][j] + a[i - 1]
                drop_b = cost[i][j - 1] + b[j - 1]
                cost[i][j] = drop_a if drop_a < drop_b else drop_b
    return cost[m][n]


def random_string(n, k):
    return "".join(chr(97 + next_random() % k) for _ in range(n))


def show(s1, s2):
    print(f'"{s1}", "{s2}" -> {minimum_delete_sum(s1, s2)}')


def main():
    global seed
    show("sea", "eat")
    show("delete", "leet")
    show("a", "a")
    show("a", "b")
    show("abc", "")
    show("", "")
    show("abc", "abc")
    show("abc", "cba")
    show("zzzz", "z")
    show("ab", "ba")
    seed = 712
    x = random_string(1000, 26)
    y = random_string(1000, 26)
    print(f"1000 and 1000 letters: {minimum_delete_sum(x, y)}")
    p = random_string(1000, 3)
    q = random_string(1000, 3)
    print(f"1000 and 1000 of 3 letters: {minimum_delete_sum(p, q)}")
    total = 0
    for _ in range(500):
        k = 1 + next_random() % 26
        s1 = random_string(next_random() % 40, k)
        s2 = random_string(next_random() % 40, k)
        total = (total * 131 + minimum_delete_sum(s1, s2)) % 1000000007
    print(f"500 random pairs: checksum {total}")


main()
