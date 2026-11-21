# LeetCode #2392: Build a Matrix With Conditions -- the bench, the ★ arm
# in Python: Kahn's algorithm for the rows and again for the columns.

from collections import deque

seed = 2392


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


def conditions(k, count):
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
        out.append([order_[min(a, b)], order_[max(a, b)]])
    return out


def main():
    cases = []
    for _ in range(20):
        rows = conditions(200, 4000)
        cols = conditions(200, 4000)
        cases.append((rows, cols))
    check = 0
    for p in range(500):
        for rows, cols in cases:
            m = build_matrix(200, rows, cols)
            for r in range(200):
                row = m[r]
                for c in range(200):
                    if row[c] > 0:
                        check = (check * 31 + row[c] * (r * 200 + c) + p) % 1000000007
    print(f"500 passes over 20 matrices of k = 200: checksum {check}")


if __name__ == "__main__":
    main()
