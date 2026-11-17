# LeetCode #2220: Minimum Bit Flips to Convert Number -- mirror of
# flips.kara: the 1 bits of start ^ goal, counted by clearing the lowest
# with x & (x - 1).


def min_bit_flips(start, goal):
    differ = start ^ goal
    flips = 0
    while differ != 0:
        differ = differ & (differ - 1)
        flips += 1
    return flips


seed = 2220


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a draw of 30 bits, since one draw stops at 32767
def wide_random():
    return next_random() * 32768 + next_random()


def show(start, goal):
    print(f"{start} -> {goal}: {min_bit_flips(start, goal)}")


def main():
    # LeetCode's two examples, then four more: the same number, 0 to
    # 10^9, 10^9 to one less, and 29 ones to 0
    show(10, 7)
    show(3, 4)
    show(0, 0)
    show(0, 1000000000)
    show(1000000000, 999999999)
    show(536870911, 0)
    # 3000 random pairs up to 10^9; every third goal the start with one
    # to three bits flipped
    check = 0
    for c in range(3000):
        start = wide_random() % 1000000001
        goal = wide_random() % 1000000001
        if c % 3 == 0:
            goal = start
            for _ in range(next_random() % 3 + 1):
                bit = next_random() % 29
                goal = goal ^ (1 << bit)
        check = (check * 31 + min_bit_flips(start, goal)) % 1000000007
    print(f"3000 pairs: checksum {check}")
    # 10^5 pairs up to 10^9, the flips summed
    total = 0
    for _ in range(100000):
        start = wide_random() % 1000000001
        goal = wide_random() % 1000000001
        total += min_bit_flips(start, goal)
    print(f"10^5 random pairs: {total} flips")


main()
