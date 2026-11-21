# LeetCode #2497: Maximum Star Sum of a Graph -- benchmark mirror of the ★
# arm (star_sum.kara): one graph of 10^5 nodes and 10^5 edges, built
# once, then the passes; each sets one node's value and k from the
# checksum so far, asks, and puts the value back.


def max_star_sum(vals, edges, k):
    n = len(vals)
    beside = [[] for _ in range(n)]
    for a, b in edges:
        beside[a].append(vals[b])
        beside[b].append(vals[a])
    best = -(2**63)
    for centre in range(n):
        beside[centre].sort()
        beside[centre].reverse()
        total = vals[centre]
        taken = 0
        for value in beside[centre]:
            if taken == k or value <= 0:
                break
            total += value
            taken += 1
        best = max(best, total)
    return best


seed = 2497


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    n = 100000
    passes = 125
    vals = [wide() % 20001 - 10000 for _ in range(n)]
    taken = set()
    edges = []
    for _ in range(n):
        a = wide() % n
        b = wide() % n
        if a != b and min(a, b) * n + max(a, b) not in taken:
            taken.add(min(a, b) * n + max(a, b))
            edges.append([a, b])
    check = 0
    for p in range(passes):
        at = check % n
        was = vals[at]
        vals[at] = (check // n + p) % 20001 - 10000
        k = check % 50
        check = (check * 31 + max_star_sum(vals, edges, k) + p) % 1000000007
        vals[at] = was
    print(f"{passes} passes over 10^5 nodes and {len(edges)} edges: checksum {check}")


main()
