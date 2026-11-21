# LeetCode #2359: Find Closest Node to Given Two Nodes -- the Python mirror
# of the ★ arm: each start walked along its single edges until a node
# repeats or the path ends, its distances recorded, then every node both
# reach scanned for the least larger distance.


def distances(edges, start):
    dist = [-1] * len(edges)
    node, d = start, 0
    while node != -1 and dist[node] == -1:
        dist[node] = d
        node = edges[node]
        d += 1
    return dist


def closest_meeting_node(edges, node1, node2):
    d1 = distances(edges, node1)
    d2 = distances(edges, node2)
    best, best_dist = -1, -1
    for v in range(len(edges)):
        if d1[v] >= 0 and d2[v] >= 0:
            far = max(d1[v], d2[v])
            if best < 0 or far < best_dist:
                best, best_dist = v, far
    return best


SEED = [2359]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's two examples; one node; two nodes pointing at each other;
    # a chain of 2000 from both ends; a cycle of 2000 started half way
    # round; two paths of 1000 into a shared tail
    print(closest_meeting_node([2, 2, 3, -1], 0, 1))
    print(closest_meeting_node([1, 2, -1], 0, 2))
    print(closest_meeting_node([-1], 0, 0))
    print(closest_meeting_node([1, 0], 0, 1))
    chain = [i + 1 for i in range(1999)] + [-1]
    print(closest_meeting_node(chain, 0, 1999), closest_meeting_node(chain, 1999, 0))
    cycle = [(i + 1) % 2000 for i in range(2000)]
    print(closest_meeting_node(cycle, 0, 1000), closest_meeting_node(cycle, 3, 1500))
    merge = [i + 1 for i in range(999)] + [2000] + [i + 1 for i in range(1000, 1999)] + [2000] + [i + 1 for i in range(2000, 2999)] + [-1]
    print(closest_meeting_node(merge, 0, 1000), closest_meeting_node(merge, 500, 1000))
    # 3000 random graphs of 1 to 30 nodes, each edge -1 with a chance of 1
    # in 1 to 1 in 8, and two random starts
    check = 0
    found = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        odds = 1 + next_random() % 8
        edges = [-1 if next_random() % odds == 0 and odds > 1 else next_random() % n for _ in range(n)]
        a = next_random() % n
        b = next_random() % n
        m = closest_meeting_node(edges, a, b)
        check = (check * 31 + m + 2) % 1000000007
        if m >= 0:
            found += 1
    print(f"3000 graphs: checksum {check}, met in {found}")


main()
