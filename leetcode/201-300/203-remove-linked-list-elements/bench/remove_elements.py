"""Benchmark workload for LeetCode #203 — Remove Linked List Elements (Python; scale lane)."""


def main():
    n = 3000
    passes = 40000
    vrange = 50
    val = [0] * n
    nxt = [-1] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        val[i] = state % vrange
        nxt[i] = -1

    sink = 0
    for p in range(passes):
        target = p % vrange
        for r in range(n):
            nxt[r] = r + 1 if r + 1 < n else -1
        head = 0
        while head != -1 and val[head] == target:
            head = nxt[head]
        if head != -1:
            prev = head
            cur = nxt[head]
            while cur != -1:
                if val[cur] == target:
                    nxt[prev] = nxt[cur]
                else:
                    prev = cur
                cur = nxt[cur]
        pass_sum = 0
        c = head
        while c != -1:
            pass_sum += val[c]
            c = nxt[c]
        sink += pass_sum
    print(sink)


main()
