# LeetCode #1583 bench: the same table of ranks, in Python.


def unhappy_friends(n, preferences, pairs):
    rank = [[0] * n for _ in range(n)]
    for x in range(n):
        for r, f in enumerate(preferences[x]):
            rank[x][f] = r
    partner = [0] * n
    for p in pairs:
        partner[p[0]] = p[1]
        partner[p[1]] = p[0]
    unhappy = 0
    for x in range(n):
        y = partner[x]
        for u in preferences[x][: rank[x][y]]:
            if rank[u][x] < rank[u][partner[u]]:
                unhappy += 1
                break
    return unhappy


seed = 1583


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def shuffled(n):
    v = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        v[i], v[j] = v[j], v[i]
    return v


def main():
    n = 500
    problems = []
    for _ in range(40):
        preferences = []
        for x in range(n):
            order = shuffled(n)
            preferences.append([f for f in order if f != x])
        line = shuffled(n)
        pairs = [[line[2 * k], line[2 * k + 1]] for k in range(n // 2)]
        problems.append((preferences, pairs))
    check = 0
    total = 0
    for preferences, pairs in problems:
        unhappy = unhappy_friends(n, preferences, pairs)
        total += unhappy
        check = mix(check, unhappy)
    print(f"40 problems of 500 friends: unhappy {total}, checksum {check}")


main()
