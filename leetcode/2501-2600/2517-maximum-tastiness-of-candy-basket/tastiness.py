# LeetCode #2517: Maximum Tastiness of Candy Basket -- Python mirror of the
# ★ arm (tastiness.kara): the prices sorted, and the greatest d whose
# greedy pick reaches k bisected; and its harness, line for line.


def maximum_tastiness(price, k):
    s = sorted(price)

    def fits(d):
        count = 1
        last = s[0]
        for p in s:
            if p - last >= d:
                count += 1
                last = p
        return count >= k

    lo = 0
    hi = (s[-1] - s[0]) // (k - 1)
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2
        if fits(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    a = next_random()
    b = next_random()
    return (a * 32768 + b) % top


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    cases = [([13, 5, 1, 8, 21, 2], 3), ([1, 3, 1], 2), ([7, 7, 7, 7], 2), ([1, 2], 2), ([1, 1000000000], 2), ([1, 2, 3, 4, 5], 5), ([5, 4, 3, 2, 1], 3), ([10, 1, 10, 1, 6], 3)]
    for price, k in cases:
        print(f"{show(price)} k {k} -> {maximum_tastiness(price, k)}")
    seed = 2517
    for most, top in [(10, 20), (1000, 1000000000)]:
        total = 0
        check = 0
        for _ in range(2000):
            n = next_random() % (most - 1) + 2
            price = [below(top) + 1 for _ in range(n)]
            k = next_random() % (n - 1) + 2
            a = maximum_tastiness(price, k)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"2000 random of up to {most} prices to {top}: total {total}, checksum {check}")
    price = [below(1000000000) + 1 for _ in range(100000)]
    for k in [2, 1000, 100000]:
        print(f"10^5 random, k {k}: {maximum_tastiness(price, k)}")
    run = list(range(1, 100001))
    for k in [50000, 50001]:
        print(f"1 to 10^5, k {k}: {maximum_tastiness(run, k)}")


main()
