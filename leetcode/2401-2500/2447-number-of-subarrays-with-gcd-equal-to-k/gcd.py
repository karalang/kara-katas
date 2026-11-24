# LeetCode #2447: Number of Subarrays With GCD Equal to K -- Python mirror
# of the ★ arm (gcd.kara): from each start the running GCD, the walk
# stopped once it is no multiple of k.


def gcd(a, b):
    x, y = a, b
    while y != 0:
        x, y = y, x % y
    return x


def subarray_gcd(nums, k):
    count = 0
    for i in range(len(nums)):
        g = 0
        for j in range(i, len(nums)):
            g = gcd(g, nums[j])
            if g % k != 0:
                break
            if g == k:
                count += 1
    return count


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    r = next_random()
    return r * 32768 + next_random()


def main():
    global seed
    print(f"example 1: {subarray_gcd([9, 3, 1, 2, 6, 3], 3)}")
    print(f"example 2: {subarray_gcd([4], 7)}")
    print(f"one value: {subarray_gcd([5], 5)}")
    print(f"k too large: {subarray_gcd([6, 12, 18], 36)}")
    print(f"k of 10^9: {subarray_gcd([1000000000, 1000000000, 999999999], 1000000000)}")
    n = 1000
    print(f"all equal: {subarray_gcd([1000000000] * n, 1000000000)}")
    seed = 2447
    sixes = [6 * (1 + next_random() % 1000) for _ in range(n)]
    print(f"multiples of 6: {subarray_gcd(sixes, 6)}")
    wide = [1 + wide_random() % 1000000000 for _ in range(n)]
    print(f"wide against 1: {subarray_gcd(wide, 1)}")
    twelves = [18 if i % 100 == 99 else 12 * (1 + next_random() % 1000) for i in range(n)]
    print(f"twelves and eighteens: {subarray_gcd(twelves, 6)}")
    check = 0
    total = 0
    for _ in range(3000):
        length = 1 + next_random() % 12
        nums = [1 + next_random() % 12 for _ in range(length)]
        k = 1 + next_random() % 6
        answer = subarray_gcd(nums, k)
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


main()
