# LeetCode #1719: Number Of Ways To Reconstruct A Tree -- the bench
# (ways.kara): the nodes by degree, most first, each hung under the last
# earlier neighbour, which must hold every other neighbour of it.


def check_ways(pairs):
    size = 501
    linked = [[False] * size for _ in range(size)]
    degree = [0] * size
    for x, y in pairs:
        linked[x][y] = True
        linked[y][x] = True
        degree[x] += 1
        degree[y] += 1
    nodes = [v for v in range(size) if degree[v] > 0]
    n = len(nodes)
    nodes.sort(key=lambda v: -degree[v])
    if degree[nodes[0]] != n - 1:
        return 0
    ways = 1
    for i in range(1, n):
        v = nodes[i]
        parent = -1
        for j in range(i - 1, -1, -1):
            if linked[v][nodes[j]]:
                parent = nodes[j]
                break
        if parent < 0:
            return 0
        for u in nodes:
            if u != parent and linked[v][u] and not linked[parent][u]:
                return 0
        if degree[parent] == degree[v]:
            ways = 2
    return ways


seed = 1719


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw():
    k = 500
    labels = list(range(1, 501))
    for i in range(k):
        j = i + next_random() % (500 - i)
        labels[i], labels[j] = labels[j], labels[i]
    have = [[False] * k for _ in range(k)]
    parent = [-1] * k
    for i in range(1, k):
        if next_random() % 2 == 0:
            parent[i] = next_random() % i
        else:
            parent[i] = i - 1 - next_random() % min(i, 4)
    for i in range(1, k):
        a = parent[i]
        while a >= 0:
            have[i][a] = True
            have[a][i] = True
            a = parent[a]
    mode = next_random() % 3
    i = next_random() % k
    j = next_random() % k
    if i != j and mode > 0:
        have[i][j] = mode == 2
        have[j][i] = mode == 2
    pairs = []
    for i in range(k):
        for j in range(i + 1, k):
            if have[i][j]:
                pairs.append((min(labels[i], labels[j]), max(labels[i], labels[j])))
    return pairs


def main():
    count = 50
    rounds = 50
    problems = [draw() for _ in range(count)]
    pairs = sum(len(p) for p in problems)
    total = 0
    check = 0
    for r in range(rounds):
        for p in problems:
            answer = check_ways(p)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of 500 nodes, {pairs} pairs, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
