# LeetCode #698: Partition to K Equal Sum Subsets -- bench program, Python mirror of the bottom-up arm.

seed = 698


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def can_partition_k_subsets(nums, k):
    n = len(nums)
    total = sum(nums)
    if total % k != 0:
        return False
    target = total // k
    size = 1 << n
    fill = [-1] * size
    fill[0] = 0
    for mask in range(size):
        f = fill[mask]
        if f < 0:
            continue
        for i in range(n):
            nxt = mask | (1 << i)
            if nxt != mask and fill[nxt] < 0 and f + nums[i] <= target:
                fill[nxt] = (f + nums[i]) % target
    return fill[size - 1] == 0


def main():
    problems = []
    ks = []
    for p in range(100):
        k = 1 << (p % 5)
        g = 16 // k
        target = 16 + next_random() % 9985
        nums = []
        for _ in range(k):
            left = target
            for _ in range(g - 1):
                part = 1 + next_random() % (target // g)
                nums.append(part)
                left -= part
            nums.append(left)
        for i in range(16):
            j = i + next_random() % (16 - i)
            nums[i], nums[j] = nums[j], nums[i]
        if p % 2 == 1:
            i = next_random() % 16
            j = (i + 1 + next_random() % 15) % 16
            most = min(nums[j] - 1, 10000 - nums[i])
            if most >= 1:
                d = 1 + next_random() % most
                nums[i] += d
                nums[j] -= d
        problems.append(nums)
        ks.append(k)
    rounds = 2
    yes = 0
    checksum = 0
    for _ in range(rounds):
        for p in range(len(problems)):
            r = can_partition_k_subsets(problems[p], ks[p])
            if r:
                yes += 1
            checksum = (checksum * 3 + (1 if r else 0) + p) % 1000000007
    print(f"{rounds} rounds of 100 problems of 16 values: {yes} answers yes, checksum {checksum}")


main()
