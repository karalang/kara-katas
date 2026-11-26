# Mirror of process_queries.kara: P itself, each query moved to the front.


def process_queries(queries, m):
    p = list(range(1, m + 1))
    answer = []
    for q in queries:
        at = p.index(q)
        answer.append(at)
        p[:at + 1] = [p[at]] + p[:at]
    return answer


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def drawn(n, m):
    return [1 + next_random() % m for _ in range(n)]


def shown(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    global seed
    print(" ".join(shown(process_queries(q, m)) for q, m in [([3, 1, 2, 1], 5), ([4, 1, 2, 2], 4), ([7, 5, 5, 8, 3], 8),
                                                              ([1], 1), ([5, 4, 3, 2, 1], 5)]))
    seed = 1409
    big = process_queries(drawn(1000, 1000), 1000)
    print(f"m = 10^3: {sum(process_queries([1000] * 1000, 1000))} {sum(process_queries(list(range(1, 1001)), 1000))} {sum(big)}")
    check = 0
    total = 0
    for _ in range(2000):
        m = 1 + next_random() % 40
        n = 1 + next_random() % m
        for x in process_queries(drawn(n, m), m):
            total += x
            check = (check * 131 + x) % 1000000007
    print(f"2000 random cases: {total} in all, checksum {check}")


main()
