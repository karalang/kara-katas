# LeetCode #1583: Count Unhappy Friends -- the Python mirror of the ★ arm:
# a table of ranks and each friend's partner; `x` paired with `y` is unhappy
# when some `u` it lists before `y` ranks `x` above its own partner. O(n^2)


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


# ---- the harness: the same in every arm

seed = 0


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


def batch(count, most):
    check = 0
    total = 0
    for _ in range(count):
        n = 2 * (next_random() % most + 1)
        preferences = []
        for x in range(n):
            order = shuffled(n)
            preferences.append([f for f in order if f != x])
        line = shuffled(n)
        pairs = [[line[2 * k], line[2 * k + 1]] for k in range(n // 2)]
        unhappy = unhappy_friends(n, preferences, pairs)
        total += unhappy
        check = mix(check, unhappy)
    print(f"{count} problems of up to {2 * most} friends: unhappy {total}, checksum {check}")


def show(rows):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in r) + "]" for r in rows) + "]"


def main():
    global seed
    examples = [
        (4, [[1, 2, 3], [3, 2, 0], [3, 1, 0], [1, 2, 0]], [[0, 1], [2, 3]]),
        (2, [[1], [0]], [[1, 0]]),
        (4, [[1, 3, 2], [2, 3, 0], [1, 3, 0], [0, 2, 1]], [[1, 3], [0, 2]]),
        (4, [[1, 2, 3], [0, 2, 3], [3, 0, 1], [2, 0, 1]], [[0, 1], [2, 3]]),
        (6, [[1, 4, 3, 2, 5], [0, 5, 4, 3, 2], [3, 0, 1, 5, 4], [2, 1, 4, 0, 5], [2, 1, 0, 3, 5], [3, 4, 2, 0, 1]], [[3, 1], [2, 0], [5, 4]]),
    ]
    for n, preferences, pairs in examples:
        print(f"{n} {show(preferences)} {show(pairs)} -> {unhappy_friends(n, preferences, pairs)}")
    seed = 1583
    batch(3000, 3)
    batch(300, 30)
    batch(3, 250)


main()
