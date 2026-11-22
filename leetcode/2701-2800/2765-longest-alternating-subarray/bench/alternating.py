# LeetCode #2765: Longest Alternating Subarray -- the bench
# (alternating.kara in Python): one pass with the length of the
# alternating run ending at each number.


def alternating_subarray(nums):
    best = -1
    run = 1
    for i in range(1, len(nums)):
        if run >= 2 and nums[i] == nums[i - 2]:
            run += 1
        elif nums[i] - nums[i - 1] == 1:
            run = 2
        else:
            run = 1
        if run >= 2:
            best = max(best, run)
    return best


seed = 2765


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 100000, 10
    cases = []
    for _ in range(count):
        top = next_random() % 4 + 2
        cases.append([next_random() % top + 1 for _ in range(100)])
    total = check = 0
    for r in range(rounds):
        for nums in cases:
            length = alternating_subarray(nums)
            total += length
            check = (check * 31 + length + 1 + r) % 1000000007
    print(f"{count} arrays of 100, {rounds} rounds: lengths sum to {total}, checksum {check}")


main()
