# LeetCode #2509: Cycle Length Queries in a Tree -- benchmark mirror of
# the ★ arm (cycle.kara): 10^5 queries on the tree of 30 levels built
# once from its own generator, then the passes; each sets one query's
# second node from the checksum so far, asks every query, and puts it
# back.


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


seed = 2509


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    hi = next_random()
    return (hi * 32768 + next_random()) % top


def main():
    size = (1 << 30) - 1
    queries = []
    while len(queries) < 100000:
        a = below(size) + 1
        b = below(size) + 1
        if a != b:
            queries.append([a, b])
    passes = 34
    check = 0
    for p in range(passes):
        at = check % len(queries)
        kept = queries[at][1]
        b = (check + p) % size + 1
        if b == queries[at][0]:
            b = b % size + 1
        queries[at][1] = b
        for x in cycle_length_queries(30, queries):
            check = (check * 31 + x + p) % 1000000007
        queries[at][1] = kept
    print(f"{passes} passes over 10^5 queries on 30 levels: checksum {check}")


main()
