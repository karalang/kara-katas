# LeetCode #2240: Number of Ways to Buy Pens and Pencils -- the mirror of
# ways.kara: for each number of pens, the pencils the rest buys plus
# none, summed.


def ways_to_buy_pens_pencils(total, cost1, cost2):
    ways = 0
    pens = 0
    while pens * cost1 <= total:
        ways += (total - pens * cost1) // cost2 + 1
        pens += 1
    return ways


seed = 2240


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(total, cost1, cost2):
    print(f"total {total}, cost1 {cost1}, cost2 {cost2} -> {ways_to_buy_pens_pencils(total, cost1, cost2)}")


def main():
    show(20, 10, 5)
    show(5, 10, 10)
    show(1, 1, 1)
    show(1000000, 1, 1)
    show(1000000, 1000000, 1000000)
    show(7, 2, 3)
    show(999, 1000000, 7)
    check = 0
    for c in range(3000):
        top = [100, 10000, 1000000][c % 3]
        total = wide_random() % top + 1
        cost1 = wide_random() % top + 1
        cost2 = wide_random() % top + 1
        check = (check * 31 + ways_to_buy_pens_pencils(total, cost1, cost2)) % 1000000007
    print(f"3000 cases: checksum {check}")
    for cost2 in [2, 999, 1000000]:
        show(1000000, 1, cost2)


main()
