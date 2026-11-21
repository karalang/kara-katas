# LeetCode #2517: Maximum Tastiness of Candy Basket -- benchmark mirror of
# the ★ arm (tastiness.kara): 20 lists of 10^5 prices built once, then
# the passes, each asking every list with a k the checksum picks.


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


seed = 2517


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    a = next_random()
    b = next_random()
    return (a * 32768 + b) % top


def main():
    lists = [[below(1000000000) + 1 for _ in range(100000)] for _ in range(20)]
    passes = 3
    check = 0
    for p in range(passes):
        for price in lists:
            check = (check * 31 + maximum_tastiness(price, check % 1000 + 2) + p) % 1000000007
    print(f"{passes} passes over 20 lists of 10^5 prices: checksum {check}")


main()
