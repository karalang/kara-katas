# LeetCode #1136: Parallel Courses -- the Python mirror of the ★ arm:
# Kahn's algorithm a semester at a time. The courses with no prerequisite
# left are this semester's; taking them lowers the counts of the courses
# that follow, and those that reach 0 are next semester's. A course never
# taken means a cycle.


def minimum_semesters(n, relations):
    after = [[] for _ in range(n + 1)]
    need = [0] * (n + 1)
    for prev, nxt in relations:
        after[prev].append(nxt)
        need[nxt] += 1
    now = [c for c in range(1, n + 1) if need[c] == 0]
    semesters = 0
    taken = 0
    while now:
        semesters += 1
        taken += len(now)
        upcoming = []
        for c in now:
            for d in after[c]:
                need[d] -= 1
                if need[d] == 0:
                    upcoming.append(d)
        now = upcoming
    return semesters if taken == n else -1


seed = 1136


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(rs):
    return "[" + ", ".join(f"[{a}, {b}]" for a, b in rs) + "]"


def random_relations(n, m, acyclic):
    order = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    seen = set()
    out = []
    while len(out) < m:
        a = next_random() % n
        b = next_random() % (n - 1)
        if b >= a:
            b += 1
        if acyclic and a > b:
            a, b = b, a
        pair = (order[a], order[b])
        if pair not in seen:
            seen.add(pair)
            out.append([order[a], order[b]])
    return out


def main():
    cases = [
        (3, [[1, 3], [2, 3]]),
        (3, [[1, 2], [2, 3], [3, 1]]),
        (1, []),
        (4, [[1, 2], [2, 3], [3, 4]]),
        (4, [[4, 3], [3, 2], [2, 1], [1, 4]]),
        (5, [[1, 5], [2, 5], [3, 5], [4, 5]]),
        (6, [[1, 2], [1, 3], [2, 4], [3, 4], [4, 5], [3, 6]]),
        (5, [[1, 2], [3, 4], [4, 3]]),
    ]
    for n, rs in cases:
        print(f"{n}, {show(rs)} -> {minimum_semesters(n, rs)}")
    total = 0
    cycles = 0
    check = 0
    for i in range(2000):
        n = next_random() % 11 + 2
        m = next_random() % min(15, n * (n - 1) // 2) + 1
        rs = random_relations(n, m, i % 2 == 0)
        r = minimum_semesters(n, rs)
        if r == -1:
            cycles += 1
        else:
            total += r
        check = (check * 31 + r + 1) % 1000000007
    print(f"2000 random plans: semesters total {total}, {cycles} with a cycle, checksum {check}")
    order = list(range(1, 5001))
    for i in range(4999, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    chain = [[order[i], order[i + 1]] for i in range(4999)]
    print(f"5000 courses in one chain: {minimum_semesters(5000, chain)}")
    dag = random_relations(5000, 5000, True)
    print(f"5000 courses and 5000 random relations without a cycle: {minimum_semesters(5000, dag)}")
    ring = chain + [[order[4999], order[0]]]
    print(f"5000 courses in one ring: {minimum_semesters(5000, ring)}")


main()
