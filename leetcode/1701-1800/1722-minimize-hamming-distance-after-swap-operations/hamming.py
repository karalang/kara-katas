# LeetCode #1722: Minimize Hamming Distance After Swap Operations -- mirrors
# hamming.kara, the ★ arm: the swaps joined into groups with a union-find,
# each group's source values counted, and each target value matched from
# its group's counts.


def find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root


def minimum_hamming_distance(source, target, allowed_swaps):
    n = len(source)
    parent = list(range(n))
    size = [1] * n
    for a, b in allowed_swaps:
        ra, rb = find(parent, a), find(parent, b)
        if ra != rb:
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
    counts = {}
    for i in range(n):
        key = (find(parent, i), source[i])
        counts[key] = counts.get(key, 0) + 1
    distance = 0
    for i in range(n):
        key = (find(parent, i), target[i])
        if counts.get(key, 0) > 0:
            counts[key] -= 1
        else:
            distance += 1
    return distance


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def batch(count, most, top, swaps):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        source = [wide() % top + 1 for _ in range(n)]
        target = [wide() % top + 1 for _ in range(n)]
        m = (next_random() * 32768 + next_random()) % (swaps + 1) if n > 1 else 0
        allowed = []
        for _ in range(m):
            a = wide() % n
            b = wide() % (n - 1)
            if b >= a:
                b += 1
            allowed.append([a, b])
        answer = minimum_hamming_distance(source, target, allowed)
        total += answer
        check = (check * 31 + answer + n + m) % 1000000007
    print(f"{count} problems of up to {most} values up to {top}: distances sum to {total}, checksum {check}")


def main():
    global seed
    # LeetCode's three examples, then one value, and swaps that join
    # everything
    print(minimum_hamming_distance([1, 2, 3, 4], [2, 1, 4, 5], [[0, 1], [2, 3]]))
    print(minimum_hamming_distance([1, 2, 3, 4], [1, 3, 2, 4], []))
    print(minimum_hamming_distance([5, 1, 2, 4, 3], [1, 5, 4, 2, 3], [[0, 4], [4, 2], [1, 3], [1, 4]]))
    print(minimum_hamming_distance([7], [8], []))
    print(minimum_hamming_distance([3, 2, 1], [1, 2, 3], [[0, 1], [1, 2]]))
    seed = 1722
    batch(3000, 8, 4, 6)
    batch(300, 1000, 20, 800)
    batch(10, 100000, 100000, 100000)


main()
