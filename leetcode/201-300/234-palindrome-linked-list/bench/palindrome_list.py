"""Benchmark workload for LeetCode #234 — Palindrome Linked List (Python; scale lane)."""


def reverse(nxt, head):
    prev = -1
    cur = head
    while cur != -1:
        nx = nxt[cur]
        nxt[cur] = prev
        prev = cur
        cur = nx
    return prev


def is_palindrome(val, nxt, head):
    if head == -1:
        return True

    slow = head
    fast = head
    while nxt[fast] != -1 and nxt[nxt[fast]] != -1:
        slow = nxt[slow]
        fast = nxt[nxt[fast]]

    second = reverse(nxt, nxt[slow])
    p1 = head
    p2 = second
    while p2 != -1:
        if val[p1] != val[p2]:
            return False
        p1 = nxt[p1]
        p2 = nxt[p2]
    return True


def main():
    l = 50000
    passes = 1800
    half = (l + 1) // 2

    fh = []
    state = 12345
    for _ in range(half):
        state = (state * 1103515245 + 12345) & 2147483647
        fh.append(state % 1000)

    val = [0] * l
    nxt = [0] * l
    for j in range(l):
        val[j] = fh[j] if j < half else fh[l - 1 - j]
        nxt[j] = j + 1 if j + 1 < l else -1

    head = 0
    mid = l // 2 - 1
    base_mid = val[mid]

    sink = 0
    for p in range(passes):
        for k in range(l):
            nxt[k] = k + 1 if k + 1 < l else -1
        val[mid] = base_mid + (p % 2)
        if is_palindrome(val, nxt, head):
            sink += 1
    print(sink)


main()
