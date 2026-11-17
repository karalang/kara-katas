# LeetCode #2220: Minimum Bit Flips to Convert Number -- bench mirror of
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


def main():
    # 10^5 pairs up to 10^9
    starts = []
    goals = []
    for _ in range(100000):
        starts.append(wide_random() % 1000000001)
        goals.append(wide_random() % 1000000001)
    check = 0
    for r in range(50):
        # punch: one goal is drawn again before each round
        goals[r * 1999] = wide_random() % 1000000001
        total = 0
        for i in range(100000):
            total += min_bit_flips(starts[i], goals[i])
        check = (check * 31 + total) % 1000000007
    print(f"10^5 pairs, 50 punches: checksum {check}")


main()
