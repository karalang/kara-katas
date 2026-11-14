# LeetCode #1548: The Most Similar Path in a Graph -- the Python mirror of
# most_similar.kara, the ★ arm: a DP over the target's places with the
# cheapest neighbour one place back remembered. Prints byte-identical output.

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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def name_of(i):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "".join(letters[i // place % 26] for place in (676, 26, 1))


def judge(n, roads, names, target, path):
    if len(path) != len(target):
        return -1
    joined = [[False] * n for _ in range(n)]
    for a, b in roads:
        joined[a][b] = True
        joined[b][a] = True
    distance = 0
    for t, v in enumerate(path):
        if v < 0 or v >= n or (t > 0 and not joined[path[t - 1]][v]):
            return -1
        if names[v] != target[t]:
            distance += 1
    return distance


def batch(count, most, pool, longest):
    check = 0
    wrong = 0
    for _ in range(count):
        n = next_random() % (most - 1) + 2
        own = next_random() % pool + 1
        names = [name_of(next_random() % own) for _ in range(n)]
        roads = []
        taken = set()
        for v in range(1, n):
            u = next_random() % v
            roads.append((v, u))
            taken.add((u, v))
        extra = next_random() % n
        for _ in range(extra):
            a = next_random() % n
            b = next_random() % n
            key = (min(a, b), max(a, b))
            if a != b and key not in taken:
                taken.add(key)
                roads.append((a, b))
        length = next_random() % longest + 1
        target = [name_of(next_random() % (own + 1)) for _ in range(length)]
        path = most_similar(n, roads, names, target)
        distance = judge(n, roads, names, target, path)
        if distance < 0:
            wrong += 1
        check = mix(check, distance)
    print(f"{count} graphs of up to {most} cities, targets up to {longest}: checksum {check}, {wrong} not paths")


def example(n, roads, names, target):
    path = most_similar(n, roads, names, target)
    distance = judge(n, roads, names, target, path)
    print(f"{n} cities, target of {len(target)} -> distance {distance}")


def main():
    global seed
    example(5, [(0, 2), (0, 3), (1, 2), (1, 3), (1, 4), (2, 4)],
            ["ATL", "PEK", "LAX", "DXB", "HND"], ["ATL", "DXB", "HND", "LAX"])
    example(4, [(1, 0), (2, 0), (3, 0), (2, 1), (3, 1), (3, 2)],
            ["ATL", "PEK", "LAX", "DXB"], ["ABC", "DEF", "GHI", "JKL", "MNO", "PQR", "STU", "VWX"])
    example(6, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
            ["ATL", "PEK", "LAX", "ATL", "DXB", "HND"], ["ATL", "DXB", "HND", "DXB", "ATL", "LAX", "PEK"])
    example(2, [(0, 1)], ["AAA", "BBB"], ["BBB", "AAA", "BBB", "AAA", "AAA"])
    example(100, [(i - 1, i) for i in range(1, 100)],
            [name_of(i) for i in range(100)], [name_of(i) for i in range(99, -1, -1)])
    example(10, [(0, i) for i in range(1, 10)],
            [name_of(i) for i in range(10)], [name_of(i) for i in [1, 2, 3, 4, 5, 6]])
    seed = 1548
    batch(3000, 6, 4, 8)
    batch(300, 30, 26, 30)
    batch(30, 100, 676, 100)


main()
