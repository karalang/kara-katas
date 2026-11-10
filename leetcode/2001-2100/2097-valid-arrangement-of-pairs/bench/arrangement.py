# LeetCode #2097: Valid Arrangement of Pairs -- Python mirror of the ★
# arm's benchmark (arrangement.kara): the same 100 random walks of 100000
# pairs, each arranged by Hierholzer's walk on an explicit stack.


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
        outs = nxt[top]
        if outs:
            stack.append(outs.pop())
        else:
            path.append(top)
            stack.pop()
    path.reverse()
    return [(path[i - 1], path[i]) for i in range(1, len(path))]


seed = 2097


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


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


total = 0
check = 0
for round_ in range(100):
    pairs = random_pairs(100000, 1000, round_ % 2 == 0)
    got = valid_arrangement(pairs)
    total += len(got)
    for a, _ in got:
        check = (check * 31 + a) % 1000000007
    check = (check * 31 + got[-1][1]) % 1000000007
print(f"100 rounds: {total} pairs, checksum {check}")
