# Benchmark: LeetCode #1101 The Earliest Moment When Everyone Become
# Friends -- union-find over the logs in time order, as the Kāra ★ arm.
# Mirrors earliest_acq.kara; each call copies every log.


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def earliest_acq(logs, n):
    logs = sorted((log[:] for log in logs), key=lambda log: log[0])
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


def main():
    seed = 1101

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    groups = []
    for _ in range(64):
        times = list(range(4950))
        for i in range(4949, 0, -1):
            j = next_random() % (i + 1)
            times[i], times[j] = times[j], times[i]
        logs = []
        for x in range(100):
            for y in range(x + 1, 100):
                logs.append([times[len(logs)] * 1000, x, y])
        groups.append(logs)
    total = 0
    check = 0
    for rnd in range(20):
        for j in range(64):
            a = (rnd * 7919 + j * 104729) % 4950
            b = (rnd * 31 + j * 17 + 1) % 4950
            g = groups[j]
            g[a][0], g[b][0] = g[b][0], g[a][0]
            moment = earliest_acq(g, 100)
            total += moment
            check = (check * 31 + moment + 2) % 1000000007
    print(f"20 rounds over 64 groups of 100 people: moments sum to {total}, checksum {check}")


main()
