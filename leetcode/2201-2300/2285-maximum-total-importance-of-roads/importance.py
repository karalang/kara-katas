# LeetCode #2285: Maximum Total Importance of Roads -- the Python mirror
# of the ★ arm, `importance.kara`.


def maximum_importance(n, roads):
    degree = [0] * n
    for a, b in roads:
        degree[a] += 1
        degree[b] += 1
    degree.sort()
    total = 0
    for i, d in enumerate(degree):
        total += d * (i + 1)
    return total


# ---- test harness ---------------------------------------------------------

seed = 2285


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(maximum_importance(5, [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3), (2, 4)]))
    print(maximum_importance(5, [(0, 3), (2, 4), (1, 3)]))
    print(maximum_importance(2, [(0, 1)]))
    complete = [(a, b) for a in range(50) for b in range(a + 1, 50)]
    print(maximum_importance(50, complete))
    path = [(a, a + 1) for a in range(4999)]
    print(maximum_importance(5000, path))
    check = 0
    largest = 0
    for _ in range(2000):
        n = next_random() % 29 + 2
        m = min(next_random() % 60 + 1, n * (n - 1) // 2)
        taken = [False] * (n * n)
        roads = []
        while len(roads) < m:
            a = next_random() % n
            b = next_random() % n
            if a != b and not taken[a * n + b]:
                taken[a * n + b] = True
                taken[b * n + a] = True
                roads.append((a, b))
        answer = maximum_importance(n, roads)
        check = (check * 31 + answer) % 1000000007
        largest = max(largest, answer)
    print(f"2000 graphs: checksum {check}, largest {largest}")


main()
