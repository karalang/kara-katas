# LeetCode #1200: Minimum Absolute Difference -- the ★ arm in Python: the
# values sorted, the least difference between neighbours found in one pass
# and the neighbours that have it collected in a second.


def minimum_abs_difference(arr):
    arr = sorted(arr)
    least = min(arr[i] - arr[i - 1] for i in range(1, len(arr)))
    return [[arr[i - 1], arr[i]] for i in range(1, len(arr)) if arr[i] - arr[i - 1] == least]


# ---- test harness ---------------------------------------------------------

seed = 1200


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def distinct(n, span):
    taken = set()
    out = []
    while len(out) < n:
        high = next_random()
        low = next_random()
        v = (high * 32768 + low) % (2 * span + 1) - span
        if v not in taken:
            taken.add(v)
            out.append(v)
    return out


def show(v):
    if isinstance(v, list):
        return "[" + ", ".join(show(x) for x in v) + "]"
    return str(v)


def main():
    cases = [[4, 2, 1, 3], [1, 3, 6, 10, 15], [3, 8, -10, 23, 19, -4, -14, 27], [5, -5], [1000000, -1000000], [0, 2, 4, 6, 8, 7]]
    for c in cases:
        print(f"{show(c)}: {show(minimum_abs_difference(c))}")
    count = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 20 + 2
        span = [10, 100, 1000][next_random() % 3]
        pairs = minimum_abs_difference(distinct(n, span))
        count += len(pairs)
        for p in pairs:
            check = (check * 131 + p[0] + 1000000) % 1000000007
            check = (check * 131 + p[1] + 1000000) % 1000000007
    print(f"1000 random arrays: {count} pairs, checksum {check}")
    evens = [2 * i - 100000 for i in range(100000)]
    pairs = minimum_abs_difference(evens[::-1])
    print(f"100000 evens: {len(pairs)} pairs, first {show(pairs[0])}, last {show(pairs[-1])}")
    wide = minimum_abs_difference(distinct(100000, 1000000))
    print(f"100000 random from -10^6 to 10^6: {len(wide)} pairs, first {show(wide[0])}")


main()
