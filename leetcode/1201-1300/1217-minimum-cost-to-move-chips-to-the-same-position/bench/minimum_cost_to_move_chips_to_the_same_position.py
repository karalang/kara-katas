# LeetCode #1217 bench, in Python: the ★ arm (the odd and the even chips
# counted, the lesser count the cost) on 20000 sets of 100 chips at
# positions up to 10^9, drawn once; then 20 rounds over the sets, every
# answer folded into a checksum.

seed = 1217


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def min_cost_to_move_chips(position):
    odd = 0
    even = 0
    for p in position:
        if p % 2 == 1:
            odd += 1
        else:
            even += 1
    return min(odd, even)


def main():
    sets = []
    for _ in range(20000):
        sets.append([(next_random() * 32768 + next_random()) % 1000000000 + 1 for _ in range(100)])
    check = 0
    for rnd in range(20):
        for chips in sets:
            check = (check * 131 + min_cost_to_move_chips(chips) + rnd) % 1000000007
    print(f"20 rounds over 20000 sets of 100 chips: checksum {check}")


main()
