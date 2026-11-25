# LeetCode #1387: Sort Integers by The Power Value -- Python mirror of the
# ★ arm: each value walked only until it meets one whose power is known,
# in a dict that every walk fills on its way back; the (power, value)
# pairs sorted and the k-th read off.


def get_kth(lo, hi, k):
    known = {1: 0}
    keyed = []
    for x in range(lo, hi + 1):
        path = []
        v = x
        while v not in known:
            path.append(v)
            v = v // 2 if v % 2 == 0 else 3 * v + 1
        steps = known[v]
        while path:
            p = path.pop()
            steps += 1
            known[p] = steps
        keyed.append((known[x], x))
    keyed.sort()
    return keyed[k - 1][1]


seed = 1387


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    shown = [
        get_kth(12, 15, 2),
        get_kth(7, 11, 4),
        get_kth(1, 1, 1),
        get_kth(1, 1000, 1),
        get_kth(1, 1000, 1000),
        get_kth(12, 13, 1),
    ]
    print(" ".join(str(x) for x in shown))
    check = 0
    for k in range(1, 1001):
        check = (check * 131 + get_kth(1, 1000, k)) % 1000000007
    print(f"every k over 1 to 1000: checksum {check}")
    check = 0
    for _ in range(2000):
        a = 1 + next_random() % 1000
        b = 1 + next_random() % 1000
        lo, hi = (a, b) if a <= b else (b, a)
        k = 1 + next_random() % (hi - lo + 1)
        check = (check * 131 + get_kth(lo, hi, k)) % 1000000007
    print(f"2000 random ranges: checksum {check}")


main()
