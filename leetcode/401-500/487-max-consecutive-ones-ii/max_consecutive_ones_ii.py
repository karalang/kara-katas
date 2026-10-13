# LeetCode #487: Max Consecutive Ones II -- mirror of max_consecutive_ones_ii.kara
# (the ★ arm).


def find_max_consecutive_ones(nums):
    best = 0
    before = 0
    run = 0
    for x in nums:
        if x == 1:
            run += 1
        else:
            before = run + 1
            run = 0
        if before + run > best:
            best = before + run
    return best


def show(nums):
    print(f"[{', '.join(str(x) for x in nums)}] -> {find_max_consecutive_ones(nums)}")


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    show([1, 0, 1, 1, 0])
    show([1, 0, 1, 1, 0, 1])
    show([0])
    show([1])
    show([0, 0, 0])
    show([1, 1, 1, 1])
    show([1, 0, 0, 1, 1, 0, 1, 1, 1, 0])
    show([0, 1, 1, 1, 0, 1, 1, 1])
    count = 300
    seed = [487]
    total = 0
    checksum = 0
    for c in range(count):
        odds = 8 if c % 3 == 0 else 12 if c % 3 == 1 else 15
        nums = []
        for _ in range(1 + next_random(seed) % 60):
            nums.append(1 if next_random(seed) % 16 < odds else 0)
        best = find_max_consecutive_ones(nums)
        total += best
        checksum = (checksum * 31 + best + len(nums)) % 1000000007
    print(f"{count} random arrays: runs add up to {total}, checksum {checksum}")


main()
