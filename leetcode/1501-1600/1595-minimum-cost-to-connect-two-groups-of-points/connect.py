# LeetCode #1595: Minimum Cost to Connect Two Groups of Points -- mirrors connect.kara.

INF = 2**31 - 1


def connect_two_groups(cost):
    first, second = len(cost), len(cost[0])
    full = 1 << second
    cheapest = [min(cost[i][j] for i in range(first)) for j in range(second)]
    best = [INF] * full
    best[0] = 0
    for i in range(first):
        nxt = [INF] * full
        for mask in range(full):
            if best[mask] == INF:
                continue
            for j in range(second):
                joined = mask | 1 << j
                nxt[joined] = min(nxt[joined], best[mask] + cost[i][j])
        best = nxt
    answer = INF
    for mask in range(full):
        if best[mask] == INF:
            continue
        total = best[mask] + sum(cheapest[j] for j in range(second) if mask >> j & 1 == 0)
        answer = min(answer, total)
    return answer


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, seed):
    check = 0
    total = 0
    for _ in range(count):
        first = next_random(seed) % most + 1
        second = next_random(seed) % first + 1
        cost = [[next_random(seed) % 101 for _ in range(second)] for _ in range(first)]
        answer = connect_two_groups(cost)
        total += answer
        check = mix(check, answer)
    print(f"{count} problems of up to {most} by {most}: total {total}, checksum {check}")


def show(cost):
    return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in cost) + "]"


def main():
    examples = [
        [[15, 96], [36, 2]],
        [[1, 3, 5], [4, 1, 1], [1, 5, 3]],
        [[2, 5, 1], [3, 4, 7], [8, 1, 2], [6, 2, 4], [3, 8, 8]],
        [[7]],
        [[0, 100], [100, 0], [50, 50]],
        [[1] * 12 for _ in range(12)],
        [[5] for _ in range(12)],
    ]
    for cost in examples:
        shown = f"[[{cost[0][0]}; {len(cost[0])}]; {len(cost)}]" if len(cost) > 5 else show(cost)
        print(f"{shown} -> {connect_two_groups(cost)}")
    seed = [1595]
    batch(3000, 4, seed)
    batch(300, 8, seed)
    batch(10, 12, seed)


main()
