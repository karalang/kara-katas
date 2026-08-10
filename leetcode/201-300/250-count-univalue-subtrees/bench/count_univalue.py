"""Benchmark workload for LeetCode #250 — Count Univalue Subtrees (Python; scale lane)."""


def main():
    nodes_n = 2000000
    passes = 40
    alphabet = 3

    val = []
    state = 250250
    for _ in range(nodes_n):
        state = (state * 1103515245 + 12345) & 2147483647
        val.append((state // 65536) % alphabet)

    uni = [False] * nodes_n

    sink = 0
    for _ in range(passes):
        total = 0
        for j in range(nodes_n - 1, -1, -1):
            left = 2 * j + 1
            right = 2 * j + 2
            ok = True
            if left < nodes_n:
                if not uni[left] or val[left] != val[j]:
                    ok = False
            if right < nodes_n:
                if not uni[right] or val[right] != val[j]:
                    ok = False
            uni[j] = ok
            if ok:
                total += 1
        sink = (sink + total) % 1000000007
    print(sink)


main()
