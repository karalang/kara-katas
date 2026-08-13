"""Benchmark workload for LeetCode #255 — Verify Preorder Sequence in BST (Python; scale lane)."""

I64_MIN = -(2**63)


def main():
    n = 200000
    rounds = 250

    val, left, right = [], [], []
    state = 255255
    for _ in range(n):
        state = (state * 1103515245 + 12345) & 2147483647
        v = state
        if not val:
            val.append(v); left.append(-1); right.append(-1)
        else:
            cur = 0
            placed = False
            while not placed:
                if v == val[cur]:
                    placed = True
                elif v < val[cur]:
                    if left[cur] == -1:
                        val.append(v); left.append(-1); right.append(-1)
                        left[cur] = len(val) - 1
                        placed = True
                    else:
                        cur = left[cur]
                else:
                    if right[cur] == -1:
                        val.append(v); left.append(-1); right.append(-1)
                        right[cur] = len(val) - 1
                        placed = True
                    else:
                        cur = right[cur]

    preorder = []
    walk = [0]
    while walk:
        node = walk.pop()
        if node != -1:
            preorder.append(val[node])
            if right[node] != -1:
                walk.append(right[node])
            if left[node] != -1:
                walk.append(left[node])

    m = len(preorder)
    sink = 0
    for _ in range(rounds):
        stack = []
        lower = I64_MIN
        ok = True
        for k in range(m):
            x = preorder[k]
            if x < lower:
                ok = False
            while stack and stack[-1] < x:
                lower = stack.pop()
            stack.append(x)
        sink = (sink * 31 + 1) % 1000000007 if ok else (sink * 31) % 1000000007
        sink = (sink * 131 + (lower % 1000000007)) % 1000000007
    print(m, sink)


main()
