# LeetCode #2099: Find Subsequence of Length K With the Largest Sum -- Python
# mirror of the ★ arm (largest_sum.kara): the positions sorted by value,
# largest first and the earlier of equal values first, the first k taken
# and put back in order.


def max_subsequence(nums, k):
    order = sorted(range(len(nums)), key=lambda i: (-nums[i], i))
    chosen = sorted(order[:k])
    return [nums[i] for i in chosen]


# ---- test harness -----------------------------------------------------------

seed = 2099


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def is_subsequence(nums, sub):
    at = 0
    for x in nums:
        if at < len(sub) and sub[at] == x:
            at += 1
    return at == len(sub)


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def flag(b):
    return "true" if b else "false"


examples = [
    ([2, 1, 3, 3], 2),
    ([-1, -2, 3, 4], 3),
    ([3, 4, 3, 3], 2),
    ([5], 1),
    ([-5, -1, -3], 2),
    ([1, 2, 3, 4, 5], 5),
    ([7, -7, 7, -7, 0], 3),
]
for nums, k in examples:
    print(f"{show(nums)} k={k} -> {show(max_subsequence(nums, k))}")
valid = 0
check = 0
for round_ in range(3000):
    n = next_random() % 30 + 1
    spread = 100000 if round_ % 2 == 0 else 3
    nums = [wide_random() % (2 * spread + 1) - spread for _ in range(n)]
    k = next_random() % n + 1
    got = max_subsequence(nums, k)
    if len(got) == k and is_subsequence(nums, got):
        valid += 1
    check = (check * 31 + sum(got) + 3000000) % 1000000007
print(f"3000 lists: {valid} valid, checksum {check}")
lists = [
    [wide_random() % 200001 - 100000 for _ in range(1000)],
    [-7] * 1000,
    [100000 - 200 * i for i in range(1000)],
]
for nums in lists:
    line = []
    for k in [1, 500, 1000]:
        got = max_subsequence(nums, k)
        line.append(f"k={k} sum {sum(got)} valid {flag(is_subsequence(nums, got))}")
    print(f"1000 numbers from {nums[0]}: {', '.join(line)}")
