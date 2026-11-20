# LeetCode #1231 bench: the ★ arm in Python, over the same 100 random bars
# and 20 passes as the Kāra bench.


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [1231]
    bars = []
    cuts = []
    for _ in range(100):
        bars.append([next_random(seed) % 100000 + 1 for _ in range(10000)])
        cuts.append(next_random(seed) % 10000)
    check = 0
    for _ in range(20):
        for b in range(100):
            check = (check * 131 + maximize_sweetness(bars[b], cuts[b])) % 1000000007
    print(f"100 bars of 10^4 chunks, 20 passes: checksum {check}")


main()
