# LeetCode #2240: Number of Ways to Buy Pens and Pencils -- the
# benchmark's Python mirror of ways.kara: for each number of pens, the
# pencils the rest buys plus none, summed.


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


def main():
    check = 0
    for _ in range(300):
        # the money at 10^6, a pen from 1 to 10, a pencil up to 10^6
        cost1 = next_random() % 10 + 1
        cost2 = wide_random() % 1000000 + 1
        check = (check * 31 + ways_to_buy_pens_pencils(1000000, cost1, cost2)) % 1000000007
    print(f"300 cases of 10^6 money: checksum {check}")


main()
