# LeetCode #1135: Connecting Cities With Minimum Cost -- the bench in
# Python, the same algorithm and workload as minimum_cost.kara: each road
# its own list, the roads copied one by one and sorted in every call, the
# same 8 networks and 50 rounds.


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def minimum_cost(n, connections):
    roads = [road[:] for road in connections]
    roads.sort(key=lambda road: road[2])
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    total = 0
    joined = 1
    for road in roads:
        a = find(parent, road[0])
        b = find(parent, road[1])
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]
            total += road[2]
            joined += 1
    return total if joined == n else -1


seed = 1135


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    networks = []
    for _ in range(8):
        roads = []
        for _ in range(10000):
            x = next_random() % 1000 + 1
            y = next_random() % 999 + 1
            if y >= x:
                y += 1
            high = next_random()
            roads.append([x, y, (high * 32768 + next_random()) % 100000 + 1])
        networks.append(roads)
    total = 0
    check = 0
    for rnd in range(50):
        for j in range(8):
            at = (rnd * 7919 + j * 104729) % 10000
            networks[j][at][2] = (networks[j][at][2] * 7 + 13) % 100000 + 1
            r = minimum_cost(1000, networks[j])
            total += r
            check = (check * 31 + r + 1) % 1000000007
    print(f"50 rounds over 8 networks of 1000 cities and 10000 roads: costs total {total}, checksum {check}")


main()
