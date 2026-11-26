# LeetCode #1494: Parallel Courses II -- the Python mirror of
# min_number_of_semesters.kara: a DP over the sets of courses taken.

INF = 2**31 - 1


def min_number_of_semesters(n, relations, k):
    pre = [0] * n
    for a, b in relations:
        pre[b - 1] |= 1 << (a - 1)
    full = (1 << n) - 1
    semesters = [INF] * (full + 1)
    semesters[0] = 0
    for taken in range(full):
        if semesters[taken] == INF:
            continue
        open_ = 0
        for i in range(n):
            if taken & (1 << i) == 0 and pre[i] & taken == pre[i]:
                open_ |= 1 << i
        nxt = semesters[taken] + 1
        if bin(open_).count("1") <= k:
            semesters[taken | open_] = min(semesters[taken | open_], nxt)
            continue
        pick = open_
        while pick > 0:
            if bin(pick).count("1") == k:
                semesters[taken | pick] = min(semesters[taken | pick], nxt)
            pick = (pick - 1) & open_
    return semesters[full]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_relations(n, dense):
    order = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    relations = []
    for i in range(n):
        for j in range(i + 1, n):
            if next_random() % 100 < dense:
                relations.append([order[i], order[j]])
    return relations


def main():
    global seed
    first = min_number_of_semesters(4, [[2, 1], [3, 1], [1, 4]], 2)
    second = min_number_of_semesters(5, [[2, 1], [3, 1], [4, 1], [1, 5]], 2)
    print(f"{first} {second}")
    chain = [[c, c + 1] for c in range(1, 15)]
    wide = [[1, c] for c in range(2, 8)]
    deep = [[1, 2], [2, 3], [4, 5], [6, 7], [8, 9]]
    print(f"{min_number_of_semesters(1, [], 1)} {min_number_of_semesters(15, [], 1)} {min_number_of_semesters(15, [], 15)} {min_number_of_semesters(15, chain, 3)} {min_number_of_semesters(7, wide, 2)} {min_number_of_semesters(9, deep, 2)}")
    seed = 1494
    most = []
    for dense in [5, 15, 40]:
        for k in [2, 3, 4]:
            most.append(min_number_of_semesters(15, random_relations(15, dense), k))
    print(f"15 courses: [{', '.join(map(str, most))}]")
    check = 0
    for _ in range(1000):
        n = 1 + next_random() % 11
        dense = next_random() % 50
        k = 1 + next_random() % n
        relations = random_relations(n, dense)
        check = (check * 31 + min_number_of_semesters(n, relations, k)) % 1000000007
    print(f"1000 random cases: checksum {check}")


main()
