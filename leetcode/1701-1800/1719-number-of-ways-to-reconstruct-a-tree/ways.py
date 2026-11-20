# LeetCode #1719: Number Of Ways To Reconstruct A Tree -- mirrors ways.kara,
# the ★ arm: the nodes by degree, most first, each hung under the last
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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(most):
    k = 2 + next_random() % (most - 1)
    labels = list(range(1, 501))
    for i in range(k):
        j = i + next_random() % (500 - i)
        labels[i], labels[j] = labels[j], labels[i]
    have = [[False] * k for _ in range(k)]
    if next_random() % 2 == 0:
        parent = [-1] * k
        for i in range(1, k):
            parent[i] = next_random() % i
        for i in range(1, k):
            a = parent[i]
            while a >= 0:
                have[i][a] = True
                have[a][i] = True
                a = parent[a]
        mode = next_random() % 3
        i = next_random() % k
        j = next_random() % k
        if i != j:
            if mode == 1:
                have[i][j] = False
                have[j][i] = False
            elif mode == 2:
                have[i][j] = True
                have[j][i] = True
    else:
        for i in range(k):
            for j in range(i + 1, k):
                if next_random() % 2 == 0:
                    have[i][j] = True
                    have[j][i] = True
    pairs = []
    for i in range(k):
        for j in range(i + 1, k):
            if have[i][j]:
                pairs.append([min(labels[i], labels[j]), max(labels[i], labels[j])])
    if not pairs:
        pairs.append([min(labels[0], labels[1]), max(labels[0], labels[1])])
    return pairs


def batch(count, most):
    total = 0
    check = 0
    for _ in range(count):
        pairs = draw(most)
        answer = check_ways(pairs)
        total += answer
        check = (check * 31 + answer + len(pairs)) % 1000000007
    print(f"{count} problems of up to {most} nodes: answers sum to {total}, checksum {check}")


def main():
    global seed
    # LeetCode's three examples, then one pair, and a star whose centre is
    # the only root
    print(check_ways([[1, 2], [2, 3]]))
    print(check_ways([[1, 2], [2, 3], [1, 3]]))
    print(check_ways([[1, 2], [2, 3], [2, 4], [1, 5]]))
    print(check_ways([[1, 500]]))
    print(check_ways([[1, 2], [1, 3], [1, 4]]))
    seed = 1719
    batch(3000, 6)
    batch(300, 50)
    batch(10, 500)


main()
