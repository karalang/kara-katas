# LeetCode #2475: Number of Unequal Triplets in Array -- the bench, the ★
# arm in Python: a dict counts the values, and each value of count `c`
# is the middle of `left * c * right` triplets.


def unequal_triplets(nums):
    counts = {}
    for v in nums:
        counts[v] = counts.get(v, 0) + 1
    n = len(nums)
    left = 0
    total = 0
    for c in counts.values():
        total += left * c * (n - left - c)
        left += c
    return total


seed = 2475


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 2000 lists of 100 values from 1 to 50 built once; then 600 passes,
    # each setting one value of every list from the checksum so far, then
    # answering it, folding the count plus the pass into the checksum
    lists = [[1 + next_random() % 50 for _ in range(100)] for _ in range(2000)]
    check = 0
    for p in range(600):
        for a, nums in enumerate(lists):
            nums[(check + a) % 100] = 1 + check % 50
            check = (check * 31 + unequal_triplets(nums) + p) % 1000000007
    print(f"600 passes over 2000 lists of 100: checksum {check}")


main()
