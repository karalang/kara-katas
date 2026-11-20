# LeetCode #2360: Longest Cycle in a Graph -- the Python mirror of the ★
# arm: each node stamped with the time it is first visited, and a walk
# that reaches a node stamped since it began has closed a cycle as long as
# the time between the two visits.


def longest_cycle(edges):
    n = len(edges)
    stamp = [-1] * n
    time = 0
    best = -1
    for start in range(n):
        began = time
        node = start
        while node != -1 and stamp[node] == -1:
            stamp[node] = time
            time += 1
            node = edges[node]
        if node != -1 and stamp[node] >= began:
            best = max(best, time - stamp[node])
    return best


SEED = [2360]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's two examples; two nodes pointing at each other; a cycle of
    # 2000; a chain of 2000 into a cycle of 1000; 1000 cycles of 2 and one
    # of 3 at the end; a chain of 3000 with no cycle
    print(longest_cycle([3, 3, 4, 2, 3]))
    print(longest_cycle([2, -1, 3, 1]))
    print(longest_cycle([1, 0]))
    print(longest_cycle([(i + 1) % 2000 for i in range(2000)]))
    print(longest_cycle([2000 if i == 2999 else i + 1 for i in range(3000)]))
    print(longest_cycle([2000 + (i - 1999) % 3 if i >= 2000 else i ^ 1 for i in range(2003)]))
    print(longest_cycle([i + 1 if i < 2999 else -1 for i in range(3000)]))
    # 3000 random graphs of 2 to 30 nodes, each edge -1 with a chance of 1
    # in 1 to 1 in 8 and otherwise to another node
    check = 0
    cyclic = 0
    for _ in range(3000):
        n = 2 + next_random() % 29
        odds = 1 + next_random() % 8
        edges = []
        for i in range(n):
            if odds > 1 and next_random() % odds == 0:
                edges.append(-1)
            else:
                edges.append((i + 1 + next_random() % (n - 1)) % n)
        m = longest_cycle(edges)
        check = (check * 31 + m + 2) % 1000000007
        if m > 0:
            cyclic += 1
    print(f"3000 graphs: checksum {check}, cycles in {cyclic}")


if __name__ == "__main__":
    main()
