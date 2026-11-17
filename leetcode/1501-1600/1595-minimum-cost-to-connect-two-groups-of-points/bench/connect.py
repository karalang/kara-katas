# LeetCode #1595: Minimum Cost to Connect Two Groups of Points
# -- the bench in Python, mirroring connect.kara: one edge per first
# point over a mask of the second group's points joined, then each point
# still alone takes its cheapest edge; 200 problems of 12 by 12, costs
# from 0 to 100, all drawn first.

INF = 2**31 - 1


def connect_two_groups(cost):
    first, second = len(cost), len(cost[0])
    full = 1 << second
    cheapest = [min(cost[i][j] for i in range(first)) for j in range(second)]
    best = [INF] * full
    best[0] = 0
    for i in range(first):
        nxt = [INF] * full
        row = cost[i]
        for mask in range(full):
            b = best[mask]
            if b == INF:
                continue
            for j in range(second):
                joined = mask | 1 << j
                if b + row[j] < nxt[joined]:
                    nxt[joined] = b + row[j]
        best = nxt
    answer = INF
    for mask in range(full):
        if best[mask] == INF:
            continue
        total = best[mask]
        for j in range(second):
            if mask >> j & 1 == 0:
                total += cheapest[j]
        answer = min(answer, total)
    return answer


def main():
    seed = 1595

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    problems = [[[next_random() % 101 for _ in range(12)] for _ in range(12)] for _ in range(200)]
    check = 0
    total = 0
    for cost in problems:
        answer = connect_two_groups(cost)
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"200 problems of 12 by 12: total {total}, checksum {check}")


main()
