"""Benchmark workload for LeetCode #145 — Binary Tree Postorder Traversal (Python; scale lane)."""


def main():
    n = 50000
    passes = 250

    val = [0] * n
    left = [-1] * n
    right = [-1] * n

    state = 12345
    for i in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        val[i] = state >> 16

    for i in range(1, n):
        cur = 0
        placed = False
        while not placed:
            if val[i] < val[cur]:
                if left[cur] < 0:
                    left[cur] = i
                    placed = True
                else:
                    cur = left[cur]
            else:
                if right[cur] < 0:
                    right[cur] = i
                    placed = True
                else:
                    cur = right[cur]

    s1 = [0] * n
    s2 = [0] * n
    sink = 0
    for p in range(passes):
        idx = p % n
        val[idx] += 1

        s1p = 0
        s1[s1p] = 0
        s1p += 1
        s2p = 0
        while s1p > 0:
            s1p -= 1
            node = s1[s1p]
            s2[s2p] = node
            s2p += 1
            l = left[node]
            r = right[node]
            if l >= 0:
                s1[s1p] = l
                s1p += 1
            if r >= 0:
                s1[s1p] = r
                s1p += 1
        pos = 0
        acc = 0
        while s2p > 0:
            s2p -= 1
            node = s2[s2p]
            acc += val[node] * (pos + 1)
            pos += 1
        sink += acc

    print(sink)


main()
