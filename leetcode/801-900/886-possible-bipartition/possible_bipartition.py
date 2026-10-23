# LeetCode #886: Possible Bipartition -- Python mirror of the
# breadth-first solution in possible_bipartition.kara, with the same test
# harness.
#
# Two people who dislike each other must be in different groups, so the
# split exists exactly when the graph of dislikes can be coloured with two
# colours, no dislike joining two people of one colour. A breadth-first
# search from each person not yet coloured gives the first one colour and
# every neighbour the other; a neighbour already holding the same colour
# as the person it is reached from means no split exists. O(n + E).

from collections import deque


def possible_bipartition(n, dislikes):
    adj = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        adj[a].append(b)
        adj[b].append(a)
    colour = [-1] * (n + 1)
    queue = deque()
    for start in range(1, n + 1):
        if colour[start] >= 0:
            continue
        colour[start] = 0
        queue.append(start)
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if colour[v] < 0:
                    colour[v] = 1 - colour[u]
                    queue.append(v)
                elif colour[v] == colour[u]:
                    return False
    return True


# ---- test harness ----------------------------------------------------------


def text(dislikes):
    if len(dislikes) > 5:
        return f"[[{dislikes[0][0]}, {dislikes[0][1]}], ... ({len(dislikes)} pairs)]"
    return "[" + ", ".join(f"[{a}, {b}]" for a, b in dislikes) + "]"


def show(n, dislikes):
    print(f"n = {n}, dislikes = {text(dislikes)} -> {str(possible_bipartition(n, dislikes)).lower()}")


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# up to m distinct pairs a < b of n people, each across two random sides,
# then up to `extra` more pairs of any two people, which may join a side
def split_graph(n, m, extra):
    side = [next_random() % 2 for _ in range(n + 1)]
    used = set()
    pairs = []
    for k in range(m + extra):
        a = next_random() % n + 1
        b = next_random() % n + 1
        key = min(a, b) * (n + 1) + max(a, b)
        if a != b and key not in used and (k >= m or side[a] != side[b]):
            used.add(key)
            pairs.append([min(a, b), max(a, b)])
    return pairs


def line(n, closed):
    pairs = [[a, a + 1] for a in range(1, n)]
    if closed:
        pairs.append([1, n])
    return pairs


def main():
    global seed
    show(4, [[1, 2], [1, 3], [2, 4]])
    show(3, [[1, 2], [1, 3], [2, 3]])
    show(5, [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]])
    show(1, [])
    show(2, [[1, 2]])
    show(2000, [])
    show(2000, line(2000, False))
    show(2000, line(2000, True))
    show(1999, line(1999, True))
    show(2000, [[1, b] for b in range(2, 2001)])
    # small cases
    seed = 886
    yes = 0
    for _ in range(3000):
        n = next_random() % 8 + 1
        m = next_random() % 14
        extra = next_random() % 6
        if possible_bipartition(n, split_graph(n, m, extra)):
            yes += 1
    print(f"3000 groups of up to 8 people: {yes} can be split")
    # LeetCode's sizes: up to 2000 people and 10^4 dislikes
    yes = 0
    check = 0
    for _ in range(100):
        n = 1000 + next_random() % 1001
        extra = next_random() % 3
        ok = possible_bipartition(n, split_graph(n, 10000 - extra, extra))
        bit = 1 if ok else 0
        yes += bit
        check = (check * 2 + bit) % 1000000007
    print(f"100 groups of up to 2000 people: {yes} can be split, checksum {check}")


main()
