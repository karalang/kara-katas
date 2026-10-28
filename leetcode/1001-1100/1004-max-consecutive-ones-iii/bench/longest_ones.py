# Benchmark: LeetCode #1004 Max Consecutive Ones III -- the ★ arm, a
# sliding window, on arrays of 100000 numbers, LeetCode's longest.
# Mirrors longest_ones.kara, .c, .rs and go-seq/.


def longest_ones(nums, k):
    left = 0
    zeros = 0
    best = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    rounds = 30
    n = 100000
    seed = [1004]
    arrays = []
    for t in range(20):
        arrays.append([1 if next_random(seed) % 8 < t % 7 + 1 else 0 for _ in range(n)])
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            t = (r + i) % 20
            k = (r * 37 + t * 101) % 3000
            got = longest_ones(arrays[t], k)
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"{rounds} rounds over 20 arrays of {n} numbers: answers sum to {total}, checksum {check}")


main()
