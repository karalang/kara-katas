# LeetCode #2830: Maximize the Profit as the Salesman -- the Python
# mirror of the ★ arm: the offers filed by their last house, and best[i]
# the most gold from the first i houses.


def maximize_the_profit(n, offers):
    ending = [[] for _ in range(n)]
    for s, e, g in offers:
        ending[e].append((s, g))
    best = [0] * (n + 1)
    for i in range(n):
        best[i + 1] = best[i]
        for s, g in ending[i]:
            best[i + 1] = max(best[i + 1], best[s] + g)
    return best[n]


# ---- the harness: the same in every arm --------------------------------

seed = 2830


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def offers_on(n, count, span):
    out = []
    for _ in range(count):
        start = next_random() % n
        end = min(start + next_random() % span, n - 1)
        out.append([start, end, next_random() % 1000 + 1])
    return out


def main():
    print(maximize_the_profit(5, [[0, 0, 1], [0, 2, 2], [1, 3, 2]]))
    print(maximize_the_profit(5, [[0, 0, 1], [0, 2, 10], [1, 3, 2]]))
    print(maximize_the_profit(1, [[0, 0, 7]]))
    singles = [[i, i, i % 1000 + 1] for i in range(1000)]
    singles.append([0, 999, 1000])
    print(maximize_the_profit(1000, singles))
    singles.append([0, 999, 600000])
    print(maximize_the_profit(1000, singles))
    check = 0
    for _ in range(3000):
        n = next_random() % 10 + 1
        count = next_random() % 8 + 1
        check = (check * 31 + maximize_the_profit(n, offers_on(n, count, n))) % 1000000007
    print(f"3000 small streets: checksum {check}")
    check = 0
    for _ in range(50):
        n = next_random() % 2000 + 1
        count = next_random() % 2000 + 1
        check = (check * 31 + maximize_the_profit(n, offers_on(n, count, 50))) % 1000000007
    print(f"50 long streets: checksum {check}")


main()
