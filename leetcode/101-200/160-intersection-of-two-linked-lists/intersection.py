"""LeetCode 160 — Intersection of Two Linked Lists (Python mirror / oracle).

Two-pointer length alignment over an index-linked node pool, mirroring the Kāra
version's Vec-owned + weak-next model (a shared suffix = two next-chains that
converge on the same node id).
"""


def next_idx(nxt, i):
    return nxt[i]


def length(nxt, head):
    n, cur = 0, head
    while cur != -1:
        n += 1
        cur = nxt[cur]
    return n


def advance(nxt, head, k):
    cur = head
    for _ in range(k):
        cur = nxt[cur]
    return cur


def intersection(nxt, head_a, head_b):
    la, lb = length(nxt, head_a), length(nxt, head_b)
    a, b = head_a, head_b
    if la > lb:
        a = advance(nxt, a, la - lb)
    else:
        b = advance(nxt, b, lb - la)
    while a != -1 and b != -1:
        if a == b:
            return a
        a, b = nxt[a], nxt[b]
    return -1


def run(vals, nxt, head_a, head_b):
    idx = intersection(nxt, head_a, head_b)
    print("no intersection" if idx == -1 else vals[idx])


def main():
    vals = [4, 1, 5, 6, 1, 8, 4, 5]
    nxt = [-1] * 8
    nxt[0] = 1
    nxt[1] = 5
    nxt[2] = 3
    nxt[3] = 4
    nxt[4] = 5
    nxt[5] = 6
    nxt[6] = 7
    run(vals, nxt, 0, 2)

    vals2 = [2, 3, 1, 4, 5]
    nxt2 = [-1] * 5
    nxt2[0] = 1
    nxt2[2] = 3
    nxt2[3] = 4
    run(vals2, nxt2, 0, 2)


main()
