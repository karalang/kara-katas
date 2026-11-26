# LeetCode #1462 Course Schedule IV: a mirror of check_if_prerequisite.kara.


def check_if_prerequisite(num_courses, prerequisites, queries):
    n = num_courses
    # before[u][v]: u must come before v, by the prerequisites directly and
    # then through each course in turn as a step between (Floyd-Warshall)
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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, odds):
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            if next_random() % odds == 0:
                out.append([order[i], order[j]])
    return out


def asks(n, q):
    out = []
    while len(out) < q:
        u = next_random() % n
        v = next_random() % n
        if u != v:
            out.append([u, v])
    return out


def show(answers):
    return "[" + ",".join("true" if a else "false" for a in answers) + "]"


def fold(answers):
    yes = 0
    check = 0
    for a in answers:
        if a:
            yes += 1
        check = (check * 3 + (2 if a else 1)) % 1000000007
    return yes, check


def main():
    global seed
    f = check_if_prerequisite
    e1 = f(2, [[1, 0]], [[0, 1], [1, 0]])
    e2 = f(2, [], [[1, 0], [0, 1]])
    e3 = f(3, [[1, 2], [1, 0], [2, 0]], [[1, 0], [1, 2]])
    print(f"{show(e1)} {show(e2)} {show(e3)}")
    chain = [[i, i + 1] for i in range(99)]
    along = [[0, i + 1] for i in range(99)] + [[i + 1, 0] for i in range(99)]
    c1, c2 = fold(f(100, chain, along))
    n1, n2 = fold(f(100, [], along))
    print(f"chain: {c1} of 198, checksum {c2}; none: {n1} of 198, checksum {n2}")
    seed = 1462
    big = draw(100, 20)
    qs = asks(100, 10000)
    b1, b2 = fold(f(100, big, qs))
    print(f"100 courses, {len(big)} prerequisites, 10^4 queries: {b1} true, checksum {b2}")
    total = 0
    check = 0
    for _ in range(1000):
        n = 2 + next_random() % 29
        odds = 1 + next_random() % 10
        pre = draw(n, odds)
        q = 1 + next_random() % 50
        y, c = fold(f(n, pre, asks(n, q)))
        total += y
        check = (check * 131 + c) % 1000000007
    print(f"1000 random cases: {total} true, checksum {check}")


main()
