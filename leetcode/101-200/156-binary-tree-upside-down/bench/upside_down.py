"""Benchmark workload for LeetCode #156 — Binary Tree Upside Down
(Python; scale lane)."""


def flip(left, right, root):
    cur = root
    prev = -1
    prev_right = -1
    while cur != -1:
        nxt = left[cur]
        left[cur] = prev_right
        prev_right = right[cur]
        right[cur] = prev
        prev = cur
        cur = nxt
    return prev


def main():
    l = 50000
    n = 2 * l
    passes = 1100

    val = [0] * n
    state = 12345
    for c in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        val[c] = state

    left = [-1] * n
    right = [-1] * n

    sink = 0
    for p in range(passes):
        for i in range(l):
            left[i] = i + 1 if i < l - 1 else -1
            right[i] = l + i
        pp = p % l
        right[pp] = l + ((p * 7 + 3) % l)

        new_root = flip(left, right, 0)

        chk = 0
        for j in range(n):
            chk = (chk * 1103515245 + val[j] * 3 + left[j] + 2 + right[j] + 5) & 2147483647
        chk = (chk * 1103515245 + new_root + 1) & 2147483647
        sink = (sink + chk) & 2147483647
    print(sink)


main()
