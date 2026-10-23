# LeetCode #915: Partition Array into Disjoint Intervals -- bench: Python
# mirror of the largest on the left against the smallest on the right in
# partition_disjoint.kara.


def partition_disjoint(nums):
    n = len(nums)
    least_after = [0] * n
    least_after[n - 1] = nums[n - 1]
    i = n - 1
    while i > 0:
        i -= 1
        least_after[i] = min(nums[i], least_after[i + 1])
    most = nums[0]
    for k in range(1, n):
        if most <= least_after[k]:
            return k
        most = max(most, nums[k])
    return n


seed = 915


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    high = next_random()
    return (high * 32768 + next_random()) % 1000001


def main():
    rounds = 2000
    n = 100000
    nums = []
    for i in range(n):
        v = big() % 500000
        nums.append(v if i < n // 2 else 500000 + v)
    total = 0
    check = 0
    for _ in range(rounds):
        i = big() % n
        old = nums[i]
        nums[i] = big()
        k = partition_disjoint(nums)
        total += k
        check = (check * 1000003 + k) % 1000000007
        nums[i] = old
    print(f"{rounds} rounds over {n} values: left sides summing to {total}, checksum {check}")


main()
