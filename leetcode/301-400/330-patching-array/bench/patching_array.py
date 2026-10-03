# Benchmark workload for LeetCode #330 — mirrors patching_array.kara.

LEN = 100000
PUNCHES = 1500
MODULUS = 1073741789


def min_patches(nums, n):
    miss = 1
    i = 0
    patches = 0
    length = len(nums)
    while miss <= n:
        if i < length and nums[i] <= miss:
            miss += nums[i]
            i += 1
        else:
            miss += miss
            patches += 1
    return patches


def main():
    seed = 330

    def nxt():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    nums = []
    total = 0
    for _ in range(LEN):
        v = nxt() % 1001 + 50
        nums.append(v)
        total += v
    nums.sort()
    sink = 0
    for _ in range(PUNCHES):
        hi = nxt()
        lo = nxt()
        n = (hi * 32768 + lo) % (2 * total) + 1
        answer = min_patches(nums, n)
        sink = (sink * 1000003 + answer * 64 + n % 64) % MODULUS
    print(sink)


main()
