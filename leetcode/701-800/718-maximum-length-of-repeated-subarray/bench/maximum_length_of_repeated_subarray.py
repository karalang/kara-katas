# LeetCode #718: Maximum Length of Repeated Subarray -- one rolling row.
# Benchmark mirror of the Kara star arm: the length of the common run
# ending at each pair of places, one row at a time, walked downwards.


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


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


def main():
    seed = [718]
    arrays = [[next_random(seed) % 10 for _ in range(1000)] for _ in range(60)]
    total = 0
    for rnd in range(40):
        for k in range(20):
            total += find_length(arrays[k], arrays[(k + rnd + 1) % 60])
    print(f"40 rounds of 20 pairs of 1000 numbers: sum {total}")


main()
