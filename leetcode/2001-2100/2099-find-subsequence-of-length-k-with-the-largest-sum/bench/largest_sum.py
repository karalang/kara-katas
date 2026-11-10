# LeetCode #2099: Find Subsequence of Length K With the Largest Sum -- Python
# mirror of the ★ arm's benchmark (largest_sum.kara): the same 20000 lists
# of 1000 numbers, the positions sorted by value and the chosen put back in
# order.


def max_subsequence(nums, k):
    order = sorted(range(len(nums)), key=lambda i: (-nums[i], i))
    chosen = sorted(order[:k])
    return [nums[i] for i in chosen]


seed = 2099


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


total = 0
check = 0
for _ in range(20000):
    nums = [wide_random() % 200001 - 100000 for _ in range(1000)]
    k = next_random() % 1000 + 1
    got = max_subsequence(nums, k)
    total += len(got)
    for x in got:
        check = (check * 31 + x + 100000) % 1000000007
print(f"20000 answers: {total} numbers, checksum {check}")
