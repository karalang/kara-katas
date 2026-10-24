# Benchmark: LeetCode #943 Find the Shortest Superstring -- the ★ arm,
# the most letters saved, on sets of 12 words of 20 letters, LeetCode's
# largest. Mirrors shortest_superstring.kara, .c, .rs and go-seq/.


def overlap(a, b):
    k = min(len(a), len(b)) - 1
    while k > 0:
        if a[len(a) - k:] == b[:k]:
            return k
        k -= 1
    return 0


def shortest_superstring(words):
    n = len(words)
    ov = [0] * (n * n)
    for i in range(n):
        for j in range(n):
            if i != j:
                ov[i * n + j] = overlap(words[i], words[j])
    full = (1 << n) - 1
    saved = [-1] * ((full + 1) * n)
    before = [-1] * ((full + 1) * n)
    for mask in range(1, full + 1):
        for last in range(n):
            if (mask >> last) & 1 == 1:
                rest = mask ^ (1 << last)
                if rest == 0:
                    saved[mask * n + last] = 0
                else:
                    for p in range(n):
                        if (rest >> p) & 1 == 1:
                            s = saved[rest * n + p] + ov[p * n + last]
                            if s > saved[mask * n + last]:
                                saved[mask * n + last] = s
                                before[mask * n + last] = p
    last = 0
    for w in range(1, n):
        if saved[full * n + w] > saved[full * n + last]:
            last = w
    order = []
    mask = full
    while last >= 0:
        order.append(last)
        p = before[mask * n + last]
        mask = mask ^ (1 << last)
        last = p
    out = words[order[-1]]
    i = len(order) - 1
    while i > 0:
        a = order[i]
        b = order[i - 1]
        out = out + words[b][ov[a * n + b]:]
        i -= 1
    return out


seed = 943


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, size, length = 10, 40, 12, 20
    sets = []
    for _ in range(count):
        letters = 2 + next_random() % 3
        words = []
        while len(words) < size:
            w = "".join(chr(next_random() % letters + 97) for _ in range(length))
            if w not in words:
                words.append(w)
        sets.append(words)
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            s = shortest_superstring(sets[(r + i) % count])
            total += len(s)
            for c in s.encode():
                check = (check * 31 + c) % 1000000007
    print(f"{rounds} rounds over {count} sets of {size} words of {length} letters: lengths adding to {total}, checksum {check}")


main()
