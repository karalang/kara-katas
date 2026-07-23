"""Benchmark workload for LeetCode #148 — Sort List (Python; scale lane)."""

import sys


def split_mid(nxt, head):
    slow = head
    fast = nxt[head]
    while fast != -1:
        fast = nxt[fast]
        if fast != -1:
            slow = nxt[slow]
            fast = nxt[fast]
    mid = nxt[slow]
    nxt[slow] = -1
    return mid


def merge(val, nxt, a, b):
    ai, bi = a, b
    head = -1
    tail = -1
    while ai != -1 and bi != -1:
        if val[ai] <= val[bi]:
            if head == -1:
                head = ai
            else:
                nxt[tail] = ai
            tail = ai
            ai = nxt[ai]
        else:
            if head == -1:
                head = bi
            else:
                nxt[tail] = bi
            tail = bi
            bi = nxt[bi]
    rest = ai if ai != -1 else bi
    if tail != -1:
        if rest == -1:
            nxt[tail] = -1
        else:
            nxt[tail] = rest
    return head


def sort_chain(val, nxt, head):
    if head == -1:
        return -1
    if nxt[head] == -1:
        return head
    mid = split_mid(nxt, head)
    left = sort_chain(val, nxt, head)
    right = sort_chain(val, nxt, mid)
    return merge(val, nxt, left, right)


def main():
    sys.setrecursionlimit(1000000)
    n = 20000
    passes = 180
    vr = 100000
    val = [0] * n
    nxt = [-1] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        val[i] = state % vr

    sink = 0
    for _p in range(passes):
        state = (state * 1103515245 + 12345) & 2147483647
        idx = state % n
        state = (state * 1103515245 + 12345) & 2147483647
        val[idx] = state % vr

        for i in range(n - 1):
            nxt[i] = i + 1
        nxt[n - 1] = -1

        head = sort_chain(val, nxt, 0)

        cur = head
        pos = 1
        while cur != -1:
            sink += pos * val[cur]
            pos += 1
            cur = nxt[cur]
    print(sink)


main()
