# LeetCode #1782: Count Pairs Of Nodes -- the ★ arm in Python: two pointers
# over the sorted degrees, less each joined pair that only passes by
# counting its shared edges twice.


def count_pairs(n, edges, queries):
    degree = [0] * (n + 1)
    shared = {}
    for e in edges:
        a, b = min(e), max(e)
        degree[a] += 1
        degree[b] += 1
        shared[(a, b)] = shared.get((a, b), 0) + 1
    ordered = sorted(degree[1:])
    answers = []
    for q in queries:
        count = 0
        lo, hi = 0, len(ordered) - 1
        while lo < hi:
            if ordered[lo] + ordered[hi] > q:
                count += hi - lo
                hi -= 1
            else:
                lo += 1
        for (a, b), c in shared.items():
            s = degree[a] + degree[b]
            if s > q and s - c <= q:
                count -= 1
        answers.append(count)
    return answers


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_edges(n, m):
    edges = []
    for _ in range(m):
        a = 1 + next_random() % n
        b = 1 + (a + next_random() % (n - 1)) % n
        edges.append([a, b])
    return edges


def digest(answers):
    check = 0
    for a in answers:
        check = (check * 31 + a + 1) % 1000000007
    return check


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    print(f"{show(count_pairs(4, [[1, 2], [2, 4], [1, 3], [2, 3], [2, 1]], [2, 3]))} {show(count_pairs(5, [[1, 5], [1, 5], [3, 4], [2, 5], [1, 3], [5, 1], [2, 3], [2, 5]], [1, 2, 3, 4, 5]))}")
    print(f"{show(count_pairs(2, [[1, 2]], [0, 1]))} {show(count_pairs(2, [[1, 2], [2, 1], [1, 2]], [0, 2, 3]))} {show(count_pairs(4, [[1, 2]], [0]))} {show(count_pairs(5, [[1, 2], [1, 3], [1, 4], [1, 5]], [1, 3]))}")
    seed = 1782
    wide = random_edges(20000, 100000)
    close = random_edges(50, 100000)
    queries = [k * k * 11 for k in range(20)]
    many = [k * 400 for k in range(20)]
    print(f"the most: {digest(count_pairs(20000, wide, queries))} {digest(count_pairs(20000, close, many))}")
    check = 0
    for _ in range(3000):
        n = 2 + next_random() % 9
        m = 1 + next_random() % 15
        edges = random_edges(n, m)
        k = 1 + next_random() % 5
        qs = [next_random() % m for _ in range(k)]
        check = (check * 31 + digest(count_pairs(n, edges, qs))) % 1000000007
    print(f"3000 random cases: checksum {check}")


main()
