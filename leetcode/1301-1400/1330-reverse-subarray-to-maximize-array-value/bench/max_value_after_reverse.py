# LeetCode #1330 bench, Python mirror of the Kāra bench: the ★ arm (the
# prefix, suffix and inside reversals' best gains in one pass) on 20 arrays
# of 3 * 10^4 values, the constraints' longest, within 30000 of 0, built
# once. Then 75 passes, each setting one value of every array from the
# checksum so far, answering it and folding the answer plus the pass into
# the checksum.


def max_value_after_reverse(nums):
    n = len(nums)
    total = 0
    gain = 0
    high_low = -(2**31)
    low_high = 2**31 - 1
    for i in range(n - 1):
        a, b = nums[i], nums[i + 1]
        d = abs(a - b)
        total += d
        gain = max(gain, abs(nums[0] - b) - d)
        gain = max(gain, abs(nums[n - 1] - a) - d)
        high_low = max(high_low, min(a, b))
        low_high = min(low_high, max(a, b))
    if n > 1:
        gain = max(gain, 2 * (high_low - low_high))
    return total + gain


seed = 1330


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    n = 30000
    arrays = [[next_random() % 60001 - 30000 for _ in range(n)] for _ in range(20)]
    check = 0
    for p in range(75):
        for t in range(20):
            arrays[t][check % n] = (check // 7) % 60001 - 30000
            got = max_value_after_reverse(arrays[t])
            check = (check * 31 + got + p) % 1000000007
    print(f"75 passes over 20 arrays of 3 * 10^4: checksum {check}")


main()
