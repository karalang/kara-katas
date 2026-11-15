# LeetCode #2176: Count Equal and Divisible Pairs in an Array -- the
# benchmark's Python mirror of pairs.kara.


def count_pairs(nums, k):
    n = len(nums)
    pairs = 0
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j] and i * j % k == 0:
                pairs += 1
    return pairs


seed = 2176


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    row = [next_random() % 5 + 1 for _ in range(100000)]
    check = 0
    for _ in range(20000):
        start = next_random() % 99901
        k = next_random() % 100 + 1
        pairs = count_pairs(row[start:start + 100], k)
        check = (check * 31 + pairs) % 1000000007
    print(f"20000 solves: checksum {check}")


main()
