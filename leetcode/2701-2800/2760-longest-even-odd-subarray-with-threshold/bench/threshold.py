# LeetCode #2760: Longest Even Odd Subarray With Threshold -- the bench
# (threshold.kara in Python): one pass with the length of the good run
# ending at each number.


def longest_alternating_subarray(nums, threshold):
    best = run = 0
    for i, x in enumerate(nums):
        if x > threshold:
            run = 0
        elif run > 0 and x % 2 != nums[i - 1] % 2:
            run += 1
        elif x % 2 == 0:
            run = 1
        else:
            run = 0
        if run > best:
            best = run
    return best


seed = 2760


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 100000, 10
    cases = []
    for _ in range(count):
        nums = [next_random() % 100 + 1 for _ in range(100)]
        threshold = next_random() % 100 + 1
        cases.append((nums, threshold))
    total = check = 0
    for r in range(rounds):
        for nums, threshold in cases:
            length = longest_alternating_subarray(nums, threshold)
            total += length
            check = (check * 31 + length + r) % 1000000007
    print(f"{count} arrays of 100, {rounds} rounds: lengths sum to {total}, checksum {check}")


main()
