# LeetCode #2447: Number of Subarrays With GCD Equal to K -- the bench,
# the ★ arm: from each start the running GCD, the walk stopped once it
# is no multiple of `k`.


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


seed = 2447


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw():
    v = 6 * (1 + next_random() % 1000)
    return v + 1 if next_random() % 40 == 0 else v


def main():
    arrays = [[draw() for _ in range(1000)] for _ in range(20)]
    check = 0
    for p in range(90):
        for c in range(len(arrays)):
            arrays[c][(37 * p + c) % 1000] = draw()
            check = (check * 31 + subarray_gcd(arrays[c], 6) + p) % 1000000007
    print(f"90 passes over 20 arrays of 1000 values: checksum {check}")


main()
