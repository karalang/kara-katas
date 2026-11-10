# LeetCode #2097: Valid Arrangement of Pairs -- Python mirror of the ★ arm
# (arrangement.kara): Hierholzer's walk with an explicit stack, starting
# where a node has one more edge out than in, or at the first pair's start.


def valid_arrangement(pairs):
    nxt = {}
    balance = {}
    for a, b in pairs:
        nxt.setdefault(a, []).append(b)
        nxt.setdefault(b, [])
        balance[a] = balance.get(a, 0) + 1
        balance[b] = balance.get(b, 0) - 1
    start = pairs[0][0]
    for v, d in balance.items():
        if d == 1:
            start = v
    stack = [start]
    path = []
    while stack:
        top = stack[-1]
        if nxt[top]:
            stack.append(nxt[top].pop())
        else:
            path.append(top)
            stack.pop()
    path.reverse()
    return [(path[i - 1], path[i]) for i in range(1, len(path))]


# ---- test harness -----------------------------------------------------------

seed = 2097


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def show(pairs):
    return "[" + ",".join(f"[{a},{b}]" for a, b in pairs) + "]"


def is_arrangement(pairs, got):
    if len(got) != len(pairs):
        return False
    for i in range(1, len(got)):
        if got[i - 1][1] != got[i][0]:
            return False
    return sorted(pairs) == sorted(got)


def step(at, values, used):
    k = len(values)
    start = next_random() % k
    for j in range(k):
        v = values[(start + j) % k]
        if v != at and (at, v) not in used:
            return v
    return None


def random_pairs(m, k, closed):
    values = [wide_random() % 1000000001 for _ in range(k)]
    first = values[next_random() % k]
    walk = [first]
    used = set()
    at = first
    while len(walk) <= m + 50:
        if closed and len(walk) >= m and at != first and (at, first) not in used:
            walk.append(first)
            break
        if not closed and len(walk) > m:
            break
        v = step(at, values, used)
        if v is None:
            break
        used.add((at, v))
        walk.append(v)
        at = v
    pairs = [(walk[i - 1], walk[i]) for i in range(1, len(walk))]
    for i in range(len(pairs) - 1, 0, -1):
        j = wide_random() % (i + 1)
        pairs[i], pairs[j] = pairs[j], pairs[i]
    return pairs


def flag(b):
    return "true" if b else "false"


examples = [
    [(5, 1), (4, 5), (11, 9), (9, 4)],
    [(1, 3), (3, 2), (2, 1)],
    [(1, 2), (1, 3), (2, 1)],
    [(0, 1)],
    [(7, 9), (8, 7), (7, 8)],
    [(1000000000, 0), (0, 1000000000)],
]
for pairs in examples:
    print(f"{show(pairs)} -> {show(valid_arrangement(pairs))}")
valid = 0
total = 0
check = 0
for round_ in range(2000):
    m = next_random() % 40 + 1
    k = next_random() % 11 + 2
    pairs = random_pairs(m, k, round_ % 3 == 0)
    got = valid_arrangement(pairs)
    if is_arrangement(pairs, got):
        valid += 1
    total += len(got)
    check = (check * 31 + got[0][0]) % 1000000007
    check = (check * 31 + got[-1][1]) % 1000000007
print(f"2000 walks: {valid} valid, {total} pairs, checksum {check}")
open_ = random_pairs(100000, 1000, False)
got = valid_arrangement(open_)
print(f"100000 pairs over 1000 values: valid {flag(is_arrangement(open_, got))}, from {got[0][0]} to {got[-1][1]}")
closed = random_pairs(100000, 1000, True)
got = valid_arrangement(closed)
print(f"100000 pairs over 1000 values, closed: valid {flag(is_arrangement(closed, got))}, from {got[0][0]} to {got[-1][1]}")
chain = [(i * 7 + 3, i * 7 + 10) for i in range(100000)]
chain.reverse()
got = valid_arrangement(chain)
print(f"a chain of 100000: valid {flag(is_arrangement(chain, got))}, from {got[0][0]} to {got[-1][1]}")
