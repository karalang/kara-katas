"""Benchmark workload for LeetCode #160 — Intersection of Two Linked Lists
(Python; scale lane)."""


def list_length(nxt, head):
    n = 0
    cur = head
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
    la = list_length(nxt, head_a)
    lb = list_length(nxt, head_b)
    a = head_a
    b = head_b
    if la > lb:
        a = advance(nxt, a, la - lb)
    else:
        b = advance(nxt, b, lb - la)
    while a != -1 and b != -1:
        if a == b:
            return a
        a = nxt[a]
        b = nxt[b]
    return -1


def main():
    n = 100003
    heads = n // 8
    passes = 280

    order = [0] * n
    for k in range(n):
        order[k] = (k * 48271) % n

    nxt = [-1] * n
    for j in range(n - 1):
        nxt[order[j]] = order[j + 1]

    sink = 0
    for p in range(passes):
        sa = p % heads
        sb = (p * 131 + 7) % heads
        ha = order[sa]
        hb = order[sb]
        idx = intersection(nxt, ha, hb)
        sink += idx
    print(sink)


main()
