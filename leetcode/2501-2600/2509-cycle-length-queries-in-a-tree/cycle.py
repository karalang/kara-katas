# LeetCode #2509: Cycle Length Queries in a Tree -- Python mirror of the
# ★ arm (cycle.kara): the larger node halved until the two meet, and its
# harness, line for line.


def cycle_length_queries(n, queries):
    answer = []
    for a, b in queries:
        length = 1
        while a != b:
            if a > b:
                a //= 2
            else:
                b //= 2
            length += 1
        answer.append(length)
    return answer


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    hi = next_random()
    return (hi * 32768 + next_random()) % top


def random_queries(n, count):
    size = (1 << n) - 1
    queries = []
    while len(queries) < count:
        a = below(size) + 1
        b = below(size) + 1
        if a != b:
            queries.append([a, b])
    return queries


def fold(check, answers):
    for a in answers:
        check = (check * 31 + a) % 1000000007
    return check


def fmt(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    global seed
    cases = [
        (3, [[5, 3], [4, 7], [2, 3]]),
        (2, [[1, 2]]),
        (2, [[2, 3], [3, 1], [2, 1]]),
        (4, [[8, 15], [8, 9], [1, 15], [14, 7], [12, 13]]),
        (5, [[16, 31], [17, 30], [3, 24], [6, 7]]),
        (30, [[536870912, 1073741823], [1, 1073741823], [1073741822, 1073741823], [2, 3]]),
    ]
    for n, queries in cases:
        print(f"n = {n}, {len(queries)} queries -> {fmt(cycle_length_queries(n, queries))}")
    seed = 2509
    for most in [30, 6]:
        check = 0
        total = 0
        for _ in range(2000):
            n = next_random() % (most - 1) + 2
            count = next_random() % 20 + 1
            answers = cycle_length_queries(n, random_queries(n, count))
            total += sum(answers)
            check = fold(check, answers)
        print(f"2000 random to {most} levels: total {total}, checksum {check}")
    rand = cycle_length_queries(30, random_queries(30, 100000))
    print(f"30 levels, 10^5 random: checksum {fold(0, rand)}")
    edges = [[(1 << 29) + k, (1 << 30) - 1 - k] for k in range(100000)]
    print(f"30 levels, 10^5 between edge leaves: checksum {fold(0, cycle_length_queries(30, edges))}")
    deep = [[1, (1 << (k % 29 + 1)) + k % (1 << (k % 29 + 1))] for k in range(100000)]
    print(f"30 levels, 10^5 from the root: checksum {fold(0, cycle_length_queries(30, deep))}")


main()
