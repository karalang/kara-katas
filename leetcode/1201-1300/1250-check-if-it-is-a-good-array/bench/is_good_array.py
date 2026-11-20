# LeetCode #1250 bench, in Python: the ★ arm (Euclid's algorithm folded
# over the array, stopping once the divisor reaches 1) on 50 random
# arrays of 100000 values built once, every value sharing a factor from
# 2 to 1000 and, in half of them, one value of no shared factor put in
# at a random place; each asked 20 times, every answer folded into a
# checksum.


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def is_good_array(nums):
    g = 0
    for x in nums:
        g = gcd(g, x)
        if g == 1:
            return True
    return g == 1


seed = 1250


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big_random():
    r = next_random() * 32768
    return r + next_random()


def main():
    arrays = []
    for t in range(50):
        factor = next_random() % 999 + 2
        nums = [factor * (big_random() % (1000000000 // factor) + 1) for _ in range(100000)]
        if t % 2 == 0:
            nums[big_random() % 100000] = 999999937
        arrays.append(nums)
    check = 0
    for _ in range(20):
        for t, nums in enumerate(arrays):
            yes = is_good_array(nums)
            check = (check * 131 + (t + 1 if yes else 0)) % 1000000007
    print(f"20 rounds of 50 arrays of 100000 values: checksum {check}")


main()
