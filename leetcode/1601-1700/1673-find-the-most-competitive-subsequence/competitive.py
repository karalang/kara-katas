# LeetCode #1673: Find the Most Competitive Subsequence -- the Python mirror
# of the ★ arm: a rising stack.


def most_competitive(nums, k):
    n = len(nums)
    stack = []
    for i in range(n):
        while stack and stack[-1] > nums[i] and len(stack) - 1 + n - i >= k:
            stack.pop()
        if len(stack) < k:
            stack.append(nums[i])
    return stack


# ---- the harness: the same as the Kāra arms -------------------------------

seed = 1673


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, longest, most):
    chosen = 0
    check = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % longest + 1
        nums = [(next_random() * 32768 + next_random()) % most for _ in range(n)]
        k = next_random() % n + 1
        answer = most_competitive(nums, k)
        chosen += len(answer)
        for v in answer:
            check = (check * 31 + v + 1) % 1000000007
    print(f"{count} arrays of up to {longest} values below {most}: {chosen} chosen, checksum {check}")


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


print(show(most_competitive([3, 5, 2, 6], 2)))
print(show(most_competitive([2, 4, 3, 3, 5, 4, 9, 6], 4)))
print(show(most_competitive([5, 1, 4], 3)))
print(show(most_competitive([7, 3, 9, 1], 1)))
print(show(most_competitive([1, 2, 3, 4, 5], 3)))
print(show(most_competitive([5, 4, 3, 2, 1], 3)))
batch(3000, 12, 5)
batch(300, 1000, 1000000000)
batch(10, 100000, 10)
