# LeetCode #1101: The Earliest Moment When Everyone Become Friends --
# Python mirror of the ★ arm: union-find over the logs in time order,
# halving the path and hanging the smaller group under the larger. Same
# cases and output as earliest_acq.kara.


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def earliest_acq(logs, n):
    logs = sorted(logs, key=lambda log: log[0])
    parent = list(range(n))
    size = [1] * n
    groups = n
    for log in logs:
        a = find(parent, log[1])
        b = find(parent, log[2])
        if a == b:
            continue
        big, small = (a, b) if size[a] >= size[b] else (b, a)
        parent[small] = big
        size[big] += size[small]
        groups -= 1
        if groups == 1:
            return log[0]
    return -1


seed = 1101


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_logs(n, m):
    used = set()
    times = set()
    logs = []
    while len(logs) < m and len(used) < n * (n - 1) // 2:
        x = next_random() % n
        y = next_random() % n
        if x == y or min(x, y) * n + max(x, y) in used:
            continue
        t = next_random() % 1000000
        while t in times:
            t = next_random() % 1000000
        used.add(min(x, y) * n + max(x, y))
        times.add(t)
        logs.append([t, x, y])
    return logs


def main():
    cases = [
        ([[20190101, 0, 1], [20190104, 3, 4], [20190107, 2, 3], [20190211, 1, 5], [20190224, 2, 4], [20190301, 0, 3], [20190312, 1, 2], [20190322, 4, 5]], 6),
        ([[0, 2, 0], [1, 0, 1], [3, 0, 3], [4, 1, 2], [7, 3, 1]], 4),
        ([[5, 0, 1]], 2),
        ([[5, 0, 1]], 3),
        ([[9, 1, 2], [3, 0, 1]], 3),
        ([[1, 0, 1], [2, 2, 3]], 4),
        ([[1, 0, 1], [2, 0, 2], [3, 1, 2]], 3),
        ([[1000000000, 0, 1], [0, 1, 2]], 3),
        ([[4, 0, 3], [3, 1, 3], [2, 2, 3], [1, 0, 1]], 4),
    ]
    for logs, n in cases:
        print(earliest_acq(logs, n))
    found = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 29 + 2
        m = next_random() % 60 + 1
        logs = random_logs(n, m)
        t = earliest_acq(logs, n)
        if t >= 0:
            found += 1
        check = (check * 31 + t + 2) % 1000000007
    print(f"2000 random groups: {found} come to one, checksum {check}")
    logs = random_logs(100, 4950)
    print(f"100 people, {len(logs)} logs: {earliest_acq(logs, 100)}")
    chain = [[i, i, i + 1] for i in reversed(range(99))]
    print(f"100 people in a chain: {earliest_acq(chain, 100)}")


main()
