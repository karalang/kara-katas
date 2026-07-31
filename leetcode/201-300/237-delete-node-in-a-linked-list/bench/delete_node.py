"""Benchmark workload for LeetCode #237 — Delete Node in a Linked List (Python; scale lane)."""


def main():
    n = 8000
    cycles = 7000
    val = [0] * n
    nxt = [-1] * n
    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        val[i] = state % 50
        nxt[i] = -1

    sink = 0
    for _ in range(cycles):
        for r in range(n):
            nxt[r] = r + 1 if r + 1 < n else -1
        while nxt[0] != -1:
            cur = 0
            while cur != -1 and nxt[cur] != -1:
                s = nxt[cur]
                val[cur] = val[s]
                nxt[cur] = nxt[s]
                cur = nxt[cur]
            pass_sum = 0
            k = 0
            while k != -1:
                pass_sum += val[k]
                k = nxt[k]
            sink = (sink * 31 + pass_sum) & 1073741823
    print(sink)


main()
