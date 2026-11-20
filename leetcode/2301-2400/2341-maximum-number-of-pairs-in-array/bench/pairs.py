# LeetCode #2341: Maximum Number of Pairs in Array -- the bench, the ★ arm
# in Python: each value counted in a table of 101, the pairs every count's
# half and the leftovers its parity.


def number_of_pairs(nums):
    counts = [0] * 101
    for x in nums:
        counts[x] += 1
    pairs = 0
    left = 0
    for c in counts:
        pairs += c // 2
        left += c % 2
    return [pairs, left]


def scrambled(index):
    return index * 2654435761 % 2147483647


def main():
    arrays = [[scrambled(a * 100000 + i) % 101 for i in range(100000)] for a in range(10)]
    check = 0
    for p in range(50):
        for nums in arrays:
            answer = number_of_pairs(nums)
            check = (check * 31 + answer[0] * 101 + answer[1] + p) % 1000000007
    print(f"50 passes over 10 arrays of 10^5 values: checksum {check}")


main()
