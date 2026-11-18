# LeetCode #1196 bench: the ★ arm in Python, over the same 200 baskets of
# 10^3 apples and 200 rounds as the Kāra bench.


def max_number_of_apples(weight):
    weight = sorted(weight)
    load = 0
    for i, w in enumerate(weight):
        load += w
        if load > 5000:
            return i
    return len(weight)


def main():
    lows = [1, 1, 300, 1]
    highs = [1000, 20, 1000, 100]
    seed = 1196
    baskets = []
    for k in range(200):
        low = lows[k % 4]
        high = highs[k % 4]
        basket = []
        for _ in range(1000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            basket.append(low + (seed // 65536) % (high - low + 1))
        baskets.append(basket)
    check = 0
    for _ in range(200):
        for basket in baskets:
            apples = max_number_of_apples(basket)
            check = (check * 131 + apples + 1) % 1000000007
    print(f"200 rounds of 200 baskets of 1000 apples: checksum {check}")


main()
