# LeetCode #1673: Find the Most Competitive Subsequence -- the bench's Python
# mirror: the ★ arm on 50 arrays of 100000 values up to 10^9, each with a
# random k, all drawn first, each answered 20 times.


def most_competitive(nums, k):
    n = len(nums)
    stack = []
    for i in range(n):
        while stack and stack[-1] > nums[i] and len(stack) - 1 + n - i >= k:
            stack.pop()
        if len(stack) < k:
            stack.append(nums[i])
    return stack


# ---- the harness ----------------------------------------------------------

seed = 1673


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


arrays = 50
n = 100000
rounds = 20
cases = []
for _ in range(arrays):
    nums = [(next_random() * 32768 + next_random()) % 1000000000 for _ in range(n)]
    k = (next_random() * 32768 + next_random()) % n + 1
    cases.append((nums, k))
chosen = 0
check = 0
for r in range(rounds):
    for nums, k in cases:
        answer = most_competitive(nums, k)
        chosen += len(answer)
        check = (check * 31 + answer[0] + answer[-1] + r) % 1000000007
print(f"{arrays} arrays of {n} values, {rounds} rounds: {chosen} chosen, checksum {check}")
