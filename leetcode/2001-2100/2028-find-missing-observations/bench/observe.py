# LeetCode #2028: Find Missing Observations -- the ★ arm in Python, the same
# algorithm and workload as observe.kara.


def missing_rolls(rolls, mean, n):
    m = len(rolls)
    need = mean * (m + n) - sum(rolls)
    if need < n or need > 6 * n:
        return []
    q, r = need // n, need % n
    return [q + 1 if i < r else q for i in range(n)]


seed = 2028


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    means = []
    ns = []
    for _ in range(20):
        lists.append([next_random() % 6 + 1 for _ in range(100000)])
        means.append(next_random() % 4 + 2)
        ns.append(next_random() % 100000 + 1)
    calls = rolls = check = 0
    for _ in range(50):
        for a in range(20):
            got = missing_rolls(lists[a], means[a], ns[a])
            calls += 1
            rolls += len(got)
            if got:
                check = (check * 31 + got[0] * 7 + got[-1]) % 1000000007
            else:
                check = (check * 31 + 1) % 1000000007
    print(f"{calls} calls: {rolls} rolls, checksum {check}")


main()
