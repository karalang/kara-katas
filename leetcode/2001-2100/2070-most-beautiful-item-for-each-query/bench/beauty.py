# LeetCode #2070: Most Beautiful Item for Each Query -- Python mirror of
# the ★ arm's benchmark (beauty.kara): 20 shops of 100000 items and 100000
# queries each, prices, beauties and queries up to 10^9.
from bisect import bisect_right


def maximum_beauty(items, queries):
    s = sorted(items, key=lambda item: item[0])
    prices = [item[0] for item in s]
    best = []
    most = 0
    for item in s:
        most = max(most, item[1])
        best.append(most)
    out = []
    for q in queries:
        end = bisect_right(prices, q)
        out.append(0 if end == 0 else best[end - 1])
    return out


def main():
    seed = 2070

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def up_to(top):
        hi = next_random()
        return (hi * 32768 + next_random()) % top + 1

    total = 0
    check = 0
    for _ in range(20):
        items = []
        for _ in range(100000):
            p = up_to(1000000000)
            items.append([p, up_to(1000000000)])
        queries = [up_to(1000000000) for _ in range(100000)]
        for a in maximum_beauty(items, queries):
            total += a
            check = (check * 31 + a) % 1000000007
    print(f"20 shops: sum {total}, checksum {check}")


main()
