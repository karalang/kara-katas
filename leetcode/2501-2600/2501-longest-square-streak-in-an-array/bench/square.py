# LeetCode #2501: Longest Square Streak in an Array -- benchmark mirror of
# the ★ arm (square.kara): 20 arrays of 10^5 values from squares chains,
# built once, then the passes; each sets one value of every array from
# the checksum so far, asks, and puts it back.
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
    passes = 32
    n = 100000
    arrays = [chained(n) for _ in range(20)]
    check = 0
    for p in range(passes):
        for nums in arrays:
            at = check % n
            was = nums[at]
            nums[at] = (check + p) % 99999 + 2
            check = (check * 31 + longest_square_streak(nums) + 1 + p) % 1000000007
            nums[at] = was
    print(f"{passes} passes over 20 arrays of 10^5: checksum {check}")


main()
