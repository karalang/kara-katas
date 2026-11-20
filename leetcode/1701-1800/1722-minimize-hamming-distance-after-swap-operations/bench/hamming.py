# LeetCode #1722: Minimize Hamming Distance After Swap Operations -- the
# bench (hamming.kara): the swaps joined into groups with a union-find,
# each group's source values counted, and each target value matched from
# its group's counts.


def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def minimum_hamming_distance(source, target, allowed_swaps):
    n = len(source)
    parent = list(range(n))
    size = [1] * n
    for a, b in allowed_swaps:
        a = find(parent, a)
        b = find(parent, b)
        if a == b:
            continue
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
    counts = {}
    for i in range(n):
        k = (find(parent, i), source[i])
        counts[k] = counts.get(k, 0) + 1
    distance = 0
    for i in range(n):
        k = (find(parent, i), target[i])
        if counts.get(k, 0) > 0:
            counts[k] -= 1
        else:
            distance += 1
    return distance


seed = 1722


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    count = 10
    rounds = 5
    n = 100000
    problems = []
    for _ in range(count):
        source = [wide() % 100000 + 1 for _ in range(n)]
        target = [wide() % 100000 + 1 for _ in range(n)]
        allowed = []
        for _ in range(n):
            a = wide() % n
            b = wide() % (n - 1)
            if b >= a:
                b += 1
            allowed.append((a, b))
        problems.append((source, target, allowed))
    total = 0
    check = 0
    for r in range(rounds):
        for source, target, allowed in problems:
            answer = minimum_hamming_distance(source, target, allowed)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} problems of {n} values and {n} swaps, {rounds} rounds: distances sum to {total}, checksum {check}")


main()
