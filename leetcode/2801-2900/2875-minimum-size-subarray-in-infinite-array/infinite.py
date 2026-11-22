# LeetCode #2875: Minimum Size Subarray in Infinite Array -- the Python
# mirror of the ★ arm (infinite.kara): the whole copies, then a sliding
# window over nums laid twice for the rest.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    global seed
    print(f"{min_size_subarray([1, 2, 3], 5)} {min_size_subarray([1, 1, 1, 2, 3], 4)} {min_size_subarray([2, 4, 6, 8], 3)}")
    n = 100000
    print(f"{min_size_subarray([1] * n, 1000000000)} {min_size_subarray([100000] * n, 1000000000)} {min_size_subarray([i % 7 + 1 for i in range(n)], 999999999)}")
    seed = 2875
    total = 0
    check = 0
    missing = 0
    for c in range(3100):
        small = c < 3000
        n = next_random() % 6 + 1 if small else wide() % 99001 + 1000
        top = 5 if small else (10 if c % 2 == 1 else 100000)
        nums = [wide() % top + 1 for _ in range(n)]
        target = next_random() % 60 + 1 if small else wide() % 1000000000 + 1
        length = min_size_subarray(nums, target)
        if length < 0:
            missing += 1
        else:
            total += length
        check = (check * 31 + length + 1) % 1000000007
        if c == 2999 or c == 3099:
            print(f"{'3000 short' if small else '100 long'} arrays: {missing} with none, lengths total {total}, checksum {check}")
            total = 0
            check = 0
            missing = 0


main()
