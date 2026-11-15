# LeetCode #2189: Number of Ways to Build House of Cards -- the Python
# mirror of cards.kara: a 0/1 knapsack over the row widths, each costing
# 3k - 1 cards.


def house_of_cards(n):
    ways = [0] * (n + 1)
    ways[0] = 1
    k = 1
    while 3 * k - 1 <= n:
        cost = 3 * k - 1
        s = n
        while s >= cost:
            ways[s] += ways[s - cost]
            s -= 1
        k += 1
    return ways[n]


# ---- test harness ---------------------------------------------------------


def show(n):
    print(f"{n} -> {house_of_cards(n)}")


def main():
    show(16)
    show(2)
    show(4)
    show(1)
    show(7)
    show(500)
    total = 0
    check = 0
    built = 0
    for n in range(1, 501):
        ways = house_of_cards(n)
        total += ways
        if ways > 0:
            built += 1
        check = (check * 31 + ways % 1000000007) % 1000000007
    print(f"1 to 500 cards: {built} build a house, {total} houses in all, checksum {check}")


main()
