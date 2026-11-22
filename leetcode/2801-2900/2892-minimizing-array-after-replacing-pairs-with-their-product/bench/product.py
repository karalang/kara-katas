# LeetCode #2892: Minimizing Array After Replacing Pairs With Their
# Product -- the bench, as
# product.kara: 50 arrays of 10^5 values, each with its k, answered 20
# times by the greedy arm.


def min_array_length(nums, k):
    if 0 in nums:
        return 1
    runs = 1
    product = nums[0]
    for x in nums[1:]:
        if product * x <= k:
            product *= x
        else:
            runs += 1
            product = x
    return runs


seed = 2892


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
        nums = [1 if next_random() % 2 == 0 else next_random() % 1000 + 1 for _ in range(n)]
        if c % 10 == 0:
            nums[n - 1 - c] = 0
        k = wide() % 1000000000 + 1
        cases.append((nums, k))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, k in cases:
            length = min_array_length(nums, k)
            total += length
            check = (check * 31 + length + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: lengths total {total}, checksum {check}")


main()
