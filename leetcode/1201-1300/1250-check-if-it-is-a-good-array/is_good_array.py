# LeetCode #1250: Check If It Is a Good Array -- the Python mirror of
# is_good_array.kara: Euclid's algorithm folded over the array, stopping
# once the divisor reaches 1.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_array(n, top, factor):
    nums = []
    for _ in range(n):
        r = next_random() * 32768
        r += next_random()
        nums.append(factor * (r % (top // factor) + 1))
    return nums


def b(x):
    return "true" if x else "false"


def main():
    global seed
    print(b(is_good_array([12, 5, 7, 23])), b(is_good_array([29, 6, 10])), b(is_good_array([3, 6])))
    seed = 1250
    good = 0
    check = 0
    for t in range(1500):
        kind = t % 3
        n = next_random() % 6 + 1 if kind == 1 else next_random() % 2000 + 1
        top = 30 if kind == 1 else 1000000000
        factor = next_random() % 8 + 2 if kind == 2 else 1
        nums = random_array(n, top, factor)
        if kind == 2 and next_random() % 2 == 0:
            at = next_random() % n
            nums[at] = random_array(1, 1000000000, 1)[0]
        yes = is_good_array(nums)
        if yes:
            good += 1
        check = (check * 131 + (t + 1 if yes else 0)) % 1000000007
    print(f"1500 random arrays: {good} good, checksum {check}")
    late = [223092870] * 99999 + [29]
    shared = [223092870 * (i % 4 + 1) for i in range(100000)]
    print(f"100000 values: last coprime {b(is_good_array(late))}, all sharing {b(is_good_array(shared))}")


main()
