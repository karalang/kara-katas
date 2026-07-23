"""Benchmark workload for LeetCode #138 — Copy List with Random Pointer (Python; scale lane).

Pointer-graph mirror of copy_random_list.kara: N Node objects (a linear `next`
chain plus one `random` edge each) are built once; the graph is deep-copied K
times, one `random` edge repointed before each copy (the punch) so nothing
hoists. `random` is a plain reference (Python's cyclic GC reclaims the
graph, matching Kāra's weak-random reclamation). Sink = running total of a
checksum over each copy's (val, next-id, random-id).
"""


class Node:
    __slots__ = ("val", "id", "next", "random")

    def __init__(self, val, id):
        self.val = val
        self.id = id
        self.next = None
        self.random = None


def build(vals, rnd):
    n = len(vals)
    nodes = [Node(vals[i], i) for i in range(n)]
    for i in range(n):
        if i + 1 < n:
            nodes[i].next = nodes[i + 1]
        if rnd[i] >= 0:
            nodes[i].random = nodes[rnd[i]]
    return nodes


def deep_copy(orig):
    n = len(orig)
    copies = [Node(orig[i].val, orig[i].id) for i in range(n)]
    for i in range(n):
        if i + 1 < n:
            copies[i].next = copies[i + 1]
        if orig[i].random is not None:
            copies[i].random = copies[orig[i].random.id]
    return copies


def checksum(copies):
    s = 0
    for c in copies:
        next_id = c.next.id if c.next is not None else -1
        rand_id = c.random.id if c.random is not None else -1
        s += c.val + next_id * 7 + rand_id * 13
    return s


def main():
    n = 3000
    k = 4000

    vals = []
    rnd = []
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        vals.append((state >> 16) % 1000)
        state = (state * 1103515245 + 12345) & 2147483647
        r = state >> 16
        rnd.append(-1 if r % 4 == 0 else r % n)

    orig = build(vals, rnd)

    sink = 0
    for p in range(k):
        ii = p % n
        target = (p * 37 + 11) % n
        orig[ii].random = orig[target]
        copies = deep_copy(orig)
        sink += checksum(copies)
    print(sink)


main()
