# LeetCode #2189: Number of Ways to Build House of Cards -- the
# benchmark's Python mirror of cards.kara: a 0/1 knapsack over the row
# widths.


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


seed = 2189


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(20000):
        n = next_random() % 500 + 1
        check = (check * 31 + house_of_cards(n) % 1000000007) % 1000000007
    print(f"20000 solves: checksum {check}")


main()
