# LeetCode #1387 bench -- Python: the ★ arm: each value walked only until
# it meets one whose power is known, in a dict that every walk fills on
# its way back; the (power, value) pairs sorted and the k-th read off.


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
    global seed
    check = 0
    for _ in range(4000):
        seed = (seed + check) % 2147483648
        lo = 1 + next_random() % 200
        hi = 800 + next_random() % 201
        k = 1 + next_random() % (hi - lo + 1)
        check = (check * 131 + get_kth(lo, hi, k)) % 1000000007
    print(f"4000 queries over ranges up to 1 to 1000: checksum {check}")


main()
