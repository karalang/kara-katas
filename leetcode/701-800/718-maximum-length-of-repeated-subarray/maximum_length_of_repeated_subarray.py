# LeetCode #718: Maximum Length of Repeated Subarray -- one rolling row.
#
# A mirror of maximum_length_of_repeated_subarray.kara (the ★ arm) and
# its harness.


def find_length(nums1, nums2):
    m, n = len(nums1), len(nums2)
    run = [0] * (n + 1)
    best = 0
    for i in range(1, m + 1):
        for j in range(n, 0, -1):
            if nums1[i - 1] == nums2[j - 1]:
                run[j] = run[j - 1] + 1
                if run[j] > best:
                    best = run[j]
            else:
                run[j] = 0
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_nums(seed, n, values):
    return [next_random(seed) % values for _ in range(n)]


def show(nums1, nums2):
    print(f"{nums1}, {nums2} -> {find_length(nums1, nums2)}")


def main():
    show([1, 2, 3, 2, 1], [3, 2, 1, 4, 7])
    show([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])
    show([1], [1])
    show([1], [2])
    show([1, 2, 3], [4, 5, 6])
    show([1, 2, 3, 4], [3, 4, 1, 2])
    show([5, 1, 2, 3], [1, 2, 3, 5])
    show([1, 2, 1, 2, 1], [2, 1, 2, 1, 2])
    seed = [718]
    a = random_nums(seed, 1000, 101)
    print(f"1000 numbers against themselves: {find_length(a, a)}")
    print(f"1000 numbers against their reverse: {find_length(a, a[::-1])}")
    b = random_nums(seed, 1000, 101)
    print(f"two 1000-number arrays, values to 100: {find_length(a, b)}")
    c = random_nums(seed, 1000, 2)
    d = random_nums(seed, 1000, 2)
    print(f"two 1000-number arrays, values 0 and 1: {find_length(c, d)}")
    e = random_nums(seed, 1000, 101)
    f = random_nums(seed, 1000, 101)
    for k in range(300):
        e[200 + k] = 7 * k % 101
        f[650 + k] = 7 * k % 101
    print(f"a planted run of 300: {find_length(e, f)}")
    total = 0
    for _ in range(300):
        m = 1 + next_random(seed) % 30
        n = 1 + next_random(seed) % 30
        values = 1 + next_random(seed) % 4
        x = random_nums(seed, m, values)
        y = random_nums(seed, n, values)
        total = (total * 131 + find_length(x, y)) % 1000000007
    print(f"300 random pairs: checksum {total}")


main()
