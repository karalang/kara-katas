"""Benchmark workload for LeetCode #144 — Binary Tree Preorder Traversal (Python; scale lane)."""


def main():
    n = 50000
    passes = 400

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

    stack = [0] * n
    sink = 0
    for p in range(passes):
        idx = p % n
        val[idx] += 1

        sp = 0
        stack[sp] = 0
        sp += 1
        pos = 0
        acc = 0
        while sp > 0:
            sp -= 1
            node = stack[sp]
            acc += val[node] * (pos + 1)
            pos += 1
            r = right[node]
            l = left[node]
            if r >= 0:
                stack[sp] = r
                sp += 1
            if l >= 0:
                stack[sp] = l
                sp += 1
        sink += acc

    print(sink)


main()
