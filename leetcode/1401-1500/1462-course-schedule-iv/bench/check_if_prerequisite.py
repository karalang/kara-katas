# LeetCode #1462 bench in Python: the ★ arm (the closure of the
# prerequisites by Floyd-Warshall) on the same 400 cases of 100 courses and
# 10^4 queries.


def check_if_prerequisite(num_courses, prerequisites, queries):
    n = num_courses
    before = [[False] * n for _ in range(n)]
    for u, v in prerequisites:
        before[u][v] = True
    for k in range(n):
        for u in range(n):
            if before[u][k]:
                for v in range(n):
                    if before[k][v]:
                        before[u][v] = True
    return [before[u][v] for u, v in queries]


seed = 1462


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for _ in range(400):
        order = list(range(100))
        for i in range(99, 0, -1):
            j = next_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        pre = []
        for i in range(100):
            for j in range(i + 1, 100):
                if next_random() % 20 == 0:
                    pre.append([order[i], order[j]])
        qs = []
        while len(qs) < 10000:
            u = next_random() % 100
            v = next_random() % 100
            if u != v:
                qs.append([u, v])
        cases.append((pre, qs))
    check = 0
    for pre, qs in cases:
        for a in check_if_prerequisite(100, pre, qs):
            check = (check * 3 + (2 if a else 1)) % 1000000007
    print(f"400 cases of 100 courses and 10^4 queries: checksum {check}")


main()
