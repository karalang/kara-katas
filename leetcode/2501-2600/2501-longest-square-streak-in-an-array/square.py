# LeetCode #2501: Longest Square Streak in an Array -- mirror of the ★
# arm (square.kara): the values in a set, and from every value whose
# square root is not in it, a walk up through the squares while they are.

import math


def longest_square_streak(nums):
    present = set(nums)
    best = 0
    for v in present:
        r = math.isqrt(v)
        if r * r == v and r in present:
            continue
        length = 0
        x = v
        while x in present:
            length += 1
            x = x * x
        best = max(best, length)
    return best if best >= 2 else -1


seed = 2501


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    return (next_random() * 32768 + next_random()) % top


def chained(n):
    # values drawn mostly from squares chains: a base 2 to 20 squared 0 to
    # 3 times, kept to 10^5; one in four any value to 10^5
    out = []
    for _ in range(n):
        if next_random() % 4 == 0:
            out.append(below(99999) + 2)
        else:
            v = next_random() % 19 + 2
            for _ in range(next_random() % 4):
                if v * v <= 100000:
                    v = v * v
            out.append(v)
    return out


def main():
    cases = [
        [4, 3, 6, 16, 8, 2],
        [2, 3, 5, 6, 7],
        [2, 4],
        [2, 2],
        [4, 2, 4, 2],
        [65536, 256, 16, 4, 2],
        [3, 9, 81, 6561, 100000],
        [10, 100, 1000, 10000, 5, 25, 625],
    ]
    for nums in cases:
        print(f"{len(nums)} values -> {longest_square_streak(nums)}")
    for kind in ["to 100", "chained"]:
        check = 0
        none = 0
        for _ in range(2000):
            n = next_random() % 39 + 2
            nums = [next_random() % 99 + 2 for _ in range(n)] if kind == "to 100" else chained(n)
            a = longest_square_streak(nums)
            if a == -1:
                none += 1
            check = (check * 31 + a + 1) % 1000000007
        print(f"2000 random {kind}: {none} without a streak, checksum {check}")
    print(f"the values 2 to 10^5 -> {longest_square_streak(list(range(2, 100001)))}")
    print(f"10^5 twos -> {longest_square_streak([2] * 100000)}")
    big = [below(99999) + 2 for _ in range(100000)]
    print(f"10^5 random to 10^5 -> {longest_square_streak(big)}")
    print(f"10^5 chained -> {longest_square_streak(chained(100000))}")


main()
