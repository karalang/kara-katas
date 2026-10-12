# Benchmark for #456: mirror of pattern132.kara (the ★ arm, one stack
# from the right) on the same workload.


def find132pattern(nums):
    stack = []
    third = -(2**63)
    for i in range(len(nums) - 1, -1, -1):
        x = nums[i]
        if x < third:
            return True
        while stack and stack[-1] < x:
            third = stack.pop()
        stack.append(x)
    return False


# ---- benchmark --------------------------------------------------------

seed = 456


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = 10
    n = 1000000
    rounds = 5
    all_nums = []
    for _ in range(arrays):
        nums = []
        top = 1000000000
        while len(nums) < n:
            run = min(1 + next_random() % 1000, n - len(nums))
            low = top - run * 10 - 1 - next_random() % 100
            for t in range(run):
                nums.append(low + t * 10 + next_random() % 10)
            top = low
        all_nums.append(nums)
    found = 0
    checksum = 0
    for _ in range(rounds):
        for a in range(arrays):
            hi = next_random()
            lo = next_random()
            at = (hi * 65536 + lo) % n
            old = all_nums[a][at]
            hi = next_random()
            lo = next_random()
            value = (hi * 65536 + lo) % 2000000001 - 1000000000
            if next_random() % 2 == 0:
                all_nums[a][at] = value
            has = find132pattern(all_nums[a])
            all_nums[a][at] = old
            if has:
                found += 1
            checksum = (checksum * 31 + (at + 1 if has else 0)) % 1000000007
    print(f"{rounds} rounds on {arrays} arrays of {n}: {found} with the pattern, checksum {checksum}")


main()
