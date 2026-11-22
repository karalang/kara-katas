# LeetCode #2875: Minimum Size Subarray in Infinite Array -- the bench,
# as infinite.kara: 50 arrays of 10^5 values, each with its target,
# answered 20 times by the sliding-window arm.


def min_size_subarray(nums, target):
    n = len(nums)
    total = sum(nums)
    whole = target // total * n
    rest = target % total
    if rest == 0:
        return whole
    best = -1
    s = 0
    left = 0
    for right in range(2 * n):
        s += nums[right % n]
        while s > rest:
            s -= nums[left % n]
            left += 1
        if s == rest and (best < 0 or right - left + 1 < best):
            best = right - left + 1
    return -1 if best < 0 else whole + best


seed = 2875


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 50, 20, 100000
    cases = []
    for c in range(count):
        top = 10 if c % 2 == 1 else 100000
        nums = [wide() % top + 1 for _ in range(n)]
        target = wide() % 1000000000 + 1
        cases.append((nums, target))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, target in cases:
            length = min_size_subarray(nums, target)
            total += length
            check = (check * 31 + length + 1 + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: lengths total {total}, checksum {check}")


main()
