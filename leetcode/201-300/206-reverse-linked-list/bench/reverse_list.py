"""Benchmark workload for LeetCode #206 — Reverse Linked List (Python; scale lane)."""


def main():
    n = 3000
    passes = 40000
    vrange = 100
    val = [0] * n
    nxt = [-1] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        val[i] = state % vrange
        nxt[i] = -1

    sink = 0
    for p in range(passes):
        hit = p % n
        val[hit] += 1
        for r in range(n):
            nxt[r] = r + 1 if r + 1 < n else -1
        prev = -1
        cur = 0
        while cur != -1:
            saved = nxt[cur]
            nxt[cur] = prev
            prev = cur
            cur = saved
        head = prev
        pass_sum = 0
        idx = 0
        c = head
        while c != -1:
            pass_sum += (idx + 1) * val[c]
            idx += 1
            c = nxt[c]
        sink += pass_sum
    print(sink)


main()
