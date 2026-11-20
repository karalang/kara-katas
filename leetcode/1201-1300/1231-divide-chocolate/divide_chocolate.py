# LeetCode #1231: Divide Chocolate -- Python mirror of the ★ arm: binary
# search on the answer, each test a greedy walk that cuts as soon as the
# piece reaches the sweetness tested.


def pieces(sweetness, m):
    count = 0
    piece = 0
    for s in sweetness:
        piece += s
        if piece >= m:
            count += 1
            piece = 0
    return count


def maximize_sweetness(sweetness, k):
    lo = 1
    hi = sum(sweetness) // (k + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if pieces(sweetness, mid) >= k + 1:
            lo = mid
        else:
            hi = mid - 1
    return lo


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    # LeetCode's three examples, and no cut at all
    print(maximize_sweetness([1, 2, 3, 4, 5, 6, 7, 8, 9], 5))
    print(maximize_sweetness([5, 6, 7, 8, 9, 1, 2, 3, 4], 8))
    print(maximize_sweetness([1, 2, 2, 1, 2, 2, 1, 2, 2], 2))
    print(maximize_sweetness([3, 1, 4], 0))
    # 1000 random bars of 1 to 40 chunks, sweetness up to 100
    seed = [1231]
    check = 0
    for _ in range(1000):
        n = next_random(seed) % 40 + 1
        bar = [next_random(seed) % 100 + 1 for _ in range(n)]
        k = next_random(seed) % n
        check = (check * 131 + maximize_sweetness(bar, k)) % 1000000007
    print(f"1000 random bars: checksum {check}")
    # the constraints' top: 10^4 chunks up to 10^5, 0, 99 and 9999 cuts
    bar = [next_random(seed) % 100000 + 1 for _ in range(10000)]
    print(f"10^4 chunks: {maximize_sweetness(bar, 0)}, {maximize_sweetness(bar, 99)}, {maximize_sweetness(bar, 9999)}")


main()
