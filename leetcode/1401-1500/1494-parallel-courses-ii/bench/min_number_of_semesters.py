# LeetCode #1494: Parallel Courses II -- the bench in Python, mirroring
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


def main():
    check = 0
    for call in range(300):
        seed = check + call

        def nxt():
            nonlocal seed
            seed = (seed * 1103515245 + 12345) % 2147483648
            return seed // 65536

        dense = nxt() % 8
        k = 2 + nxt() % 4
        relations = []
        for a in range(1, 16):
            for b in range(a + 1, 16):
                if nxt() % 100 < dense:
                    relations.append([a, b])
        check = (check * 31 + min_number_of_semesters(15, relations, k)) % 1000000007
    print(f"300 calls on 15 courses: checksum {check}")


main()
