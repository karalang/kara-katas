# LeetCode #2242: Maximum Score of a Node Sequence -- the benchmark's
# Python mirror of score.kara: each node's neighbours sorted by score,
# largest first, and cut to three; every edge as the middle one tries the
# nine pairs, all four distinct.


def maximum_score(scores, edges):
    n = len(scores)
    best3 = [[] for _ in range(n)]
    for a, b in edges:
        best3[a].append(b)
        best3[b].append(a)
    for node in range(n):
        best3[node].sort(key=lambda x: -scores[x])
        del best3[node][3:]
    best = -1
    for b, c in edges:
        for a in best3[b]:
            if a == c:
                continue
            for d in best3[c]:
                if d != a and d != b:
                    best = max(best, scores[a] + scores[b] + scores[c] + scores[d])
    return best


seed = 2242


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    n = 50000
    check = 0
    for _ in range(40):
        scores = [wide_random() % 100000000 + 1 for _ in range(n)]
        edges = [(j, (j + 1 + wide_random() % (n // 2 - 2)) % n) for j in range(n)]
        check = (check * 31 + maximum_score(scores, edges)) % 1000000007
    print(f"40 graphs of 50000 nodes: checksum {check}")


main()
