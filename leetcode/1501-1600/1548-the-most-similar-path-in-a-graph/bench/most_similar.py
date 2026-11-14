# LeetCode #1548: The Most Similar Path in a Graph -- bench: the ★ arm (a
# DP over the target's places) over 100 connected graphs of 50 to 100
# cities named from up to 26 names, each with a target of 100 names, built
# once, each asked 20 times. Python mirror of most_similar.kara.

BIG = 2**63 - 1


def most_similar(n, roads, names, target):
    next_to = [[] for _ in range(n)]
    for a, b in roads:
        next_to[a].append(b)
        next_to[b].append(a)
    length = len(target)
    cost = [[BIG] * n for _ in range(length)]
    frm = [[0] * n for _ in range(length)]
    for v in range(n):
        cost[0][v] = 0 if names[v] == target[0] else 1
    for t in range(1, length):
        for v in range(n):
            miss = 0 if names[v] == target[t] else 1
            for u in next_to[v]:
                if cost[t - 1][u] + miss < cost[t][v]:
                    cost[t][v] = cost[t - 1][u] + miss
                    frm[t][v] = u
    last = 0
    for v in range(1, n):
        if cost[length - 1][v] < cost[length - 1][last]:
            last = v
    path = [0] * length
    path[length - 1] = last
    for t in range(length - 1, 0, -1):
        path[t - 1] = frm[t][path[t]]
    return path


seed = 1548


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def name_of(i):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(letters[i // place % 26] for place in (676, 26, 1))


def main():
    graphs = []
    for _ in range(100):
        n = next_random() % 51 + 50
        own = next_random() % 26 + 1
        names = [name_of(next_random() % own) for _ in range(n)]
        joined = [[False] * n for _ in range(n)]
        roads = []
        for v in range(1, n):
            u = next_random() % v
            joined[u][v] = joined[v][u] = True
            roads.append((v, u))
        extra = next_random() % (4 * n)
        for _ in range(extra):
            a = next_random() % n
            b = next_random() % n
            if a != b and not joined[a][b]:
                joined[a][b] = joined[b][a] = True
                roads.append((a, b))
        target = [name_of(next_random() % (own + 1)) for _ in range(100)]
        graphs.append((n, roads, names, target))
    check = 0
    total = 0
    for _ in range(20):
        for n, roads, names, target in graphs:
            path = most_similar(n, roads, names, target)
            distance = 0
            for t, v in enumerate(path):
                check = mix(check, v)
                if names[v] != target[t]:
                    distance += 1
            total += distance
    print(f"20 passes over 100 graphs of up to 100 cities: distance {total}, checksum {check}")


main()
