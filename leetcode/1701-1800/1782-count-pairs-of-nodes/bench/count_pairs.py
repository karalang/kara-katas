# LeetCode #1782: Count Pairs Of Nodes -- the bench in Python, mirroring
# count_pairs.kara: two pointers over the sorted degrees less the joined
# pairs.


def count_pairs(n, edges, queries):
    degree = [0] * (n + 1)
    shared = {}
    for e in edges:
        a, b = min(e[0], e[1]), max(e[0], e[1])
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


seed = 1782


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    graphs = []
    for g in range(10):
        span = 50 + g * 2216
        edges = []
        for _ in range(100000):
            a = 1 + next_random() % span
            b = 1 + (a + next_random() % (span - 1)) % span
            edges.append([a, b])
        graphs.append(edges)
    check = 0
    for g in range(10):
        top = 400000 // (50 + g * 2216)
        queries = [(check + k * 997) % top for k in range(20)]
        for a in count_pairs(20000, graphs[g], queries):
            check = (check * 31 + a + 1) % 1000000007
    print(f"10 graphs of 100000 edges: checksum {check}")


main()
