"""Benchmark workload for LeetCode #147 — Insertion Sort List (Python; scale lane)."""


def main():
    n = 3000
    passes = 60
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

        head = -1
        for i in range(n):
            v = val[i]
            if head == -1:
                head = i
                nxt[i] = -1
            elif val[head] >= v:
                nxt[i] = head
                head = i
            else:
                prev = head
                scanning = True
                while scanning:
                    np = nxt[prev]
                    if np == -1:
                        scanning = False
                    elif val[np] < v:
                        prev = np
                    else:
                        scanning = False
                nxt[i] = nxt[prev]
                nxt[prev] = i

        cur = head
        pos = 1
        while cur != -1:
            sink += pos * val[cur]
            pos += 1
            cur = nxt[cur]
    print(sink)


main()
