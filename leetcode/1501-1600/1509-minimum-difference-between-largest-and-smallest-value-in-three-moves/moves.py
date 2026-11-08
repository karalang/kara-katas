# LeetCode #1509: Minimum Difference Between Largest and Smallest Value in
# Three Moves -- the Python mirror of the ★ arm: sort, and of the four ways
# to take three numbers off the two ends, keep the narrowest rest.


def min_difference(nums):
    n = len(nums)
    if n <= 4:
        return 0
    s = sorted(nums)
    best = s[n - 1] - s[0]
    for low in range(4):
        best = min(best, s[n - 4 + low] - s[low])
    return best


seed = 1509


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x % 1000000007 + 1) % 1000000007


def batch(count, most, span):
    check = 0
    for _ in range(count):
        n = next_random() % most + 1
        nums = []
        for _ in range(n):
            wide = next_random() * 32768
            wide += next_random()
            nums.append(wide % (2 * span + 1) - span)
        check = mix(check, min_difference(nums))
    return check


print(f"[5, 3, 2, 4] -> {min_difference([5, 3, 2, 4])}")
print(f"[1, 5, 0, 10, 14] -> {min_difference([1, 5, 0, 10, 14])}")
print(f"[3, 100, 20] -> {min_difference([3, 100, 20])}")
print(f"[6, 6, 0, 1, 1, 4, 6] -> {min_difference([6, 6, 0, 1, 1, 4, 6])}")
print(f"[1, 5, 6, 14, 15] -> {min_difference([1, 5, 6, 14, 15])}")
print(f"[-1000000000, 0, 0, 0, 1000000000] -> {min_difference([-1000000000, 0, 0, 0, 1000000000])}")
print(f"3000 arrays of 1 to 10 numbers within 50: checksum {batch(3000, 10, 50)}")
print(f"300 arrays of 1 to 1000 numbers within 10^9: checksum {batch(300, 1000, 1000000000)}")
print(f"3 arrays of 1 to 100000 numbers within 10^9: checksum {batch(3, 100000, 1000000000)}")
