# LeetCode #2392: Build a Matrix With Conditions -- a Python mirror of
# the ★ arm, Kahn's algorithm for the rows and again for the columns.
# Prints the same output as matrix.kara.

from collections import deque

seed = 0


def order(k, edges):
    nxt = [[] for _ in range(k + 1)]
    into = [0] * (k + 1)
    for a, b in edges:
        nxt[a].append(b)
        into[b] += 1
    queue = deque(v for v in range(1, k + 1) if into[v] == 0)
    taken = []
    while queue:
        v = queue.popleft()
        taken.append(v)
        for w in nxt[v]:
            into[w] -= 1
            if into[w] == 0:
                queue.append(w)
    return taken


def build_matrix(k, rows, cols):
    by_row = order(k, rows)
    by_col = order(k, cols)
    if len(by_row) < k or len(by_col) < k:
        return []
    col_of = [0] * (k + 1)
    for c, v in enumerate(by_col):
        col_of[v] = c
    m = [[0] * k for _ in range(k)]
    for r, v in enumerate(by_row):
        m[r][col_of[v]] = v
    return m


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def verdict(k, rows, cols, m):
    if not m:
        return "empty"
    if len(m) != k:
        return "INVALID"
    row_of = [-1] * (k + 1)
    col_of = [-1] * (k + 1)
    for r in range(k):
        if len(m[r]) != k:
            return "INVALID"
        for c in range(k):
            v = m[r][c]
            if v < 0 or v > k or (v > 0 and row_of[v] >= 0):
                return "INVALID"
            if v > 0:
                row_of[v] = r
                col_of[v] = c
    if any(row_of[v] < 0 for v in range(1, k + 1)):
        return "INVALID"
    if any(row_of[a] >= row_of[b] for a, b in rows):
        return "INVALID"
    if any(col_of[a] >= col_of[b] for a, b in cols):
        return "INVALID"
    return "valid"


def conditions(k, count, ordered):
    order_ = list(range(1, k + 1))
    for i in range(1, k):
        j = next_random() % (i + 1)
        order_[i], order_[j] = order_[j], order_[i]
    out = []
    for _ in range(count):
        a = next_random() % k
        b = next_random() % (k - 1)
        if b >= a:
            b += 1
        if ordered:
            out.append([order_[min(a, b)], order_[max(a, b)]])
        else:
            out.append([a + 1, b + 1])
    return out


def main():
    global seed
    examples = [
        (3, [[1, 2], [3, 2]], [[2, 1], [3, 2]]),
        (3, [[1, 2], [2, 3], [3, 1], [2, 3]], [[2, 1]]),
        (2, [], []),
        (4, [[1, 2], [2, 3], [3, 4]], [[4, 3], [3, 2], [2, 1]]),
    ]
    for k, rows, cols in examples:
        print(verdict(k, rows, cols, build_matrix(k, rows, cols)))
    seed = 2392
    rows = conditions(400, 10000, True)
    cols = conditions(400, 10000, True)
    cyclic = cols + [[cols[0][1], cols[0][0]]]
    print(f"k = 400: {verdict(400, rows, cols, build_matrix(400, rows, cols))}, {verdict(400, rows, cyclic, build_matrix(400, rows, cyclic))}")
    empty = 0
    valid = 0
    for _ in range(3000):
        k = 2 + next_random() % 11
        free = next_random() % 3 == 0
        rows = conditions(k, next_random() % (3 * k + 1), not free)
        cols = conditions(k, next_random() % (3 * k + 1), True)
        v = verdict(k, rows, cols, build_matrix(k, rows, cols))
        if v == "empty":
            empty += 1
        elif v == "valid":
            valid += 1
    print(f"3000 cases: {empty} empty, {valid} valid, {3000 - empty - valid} invalid")


if __name__ == "__main__":
    main()
