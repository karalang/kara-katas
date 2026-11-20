# LeetCode #1674: Minimum Moves to Make Array Complementary -- the bench's
# Python mirror: the ★ arm on 100 arrays of 100000 values with limits up to
# 100000, all drawn first, each answered 20 times.


def min_moves(nums, limit):
    n = len(nums)
    delta = [0] * (2 * limit + 2)
    for i in range(n // 2):
        a = min(nums[i], nums[n - 1 - i])
        b = max(nums[i], nums[n - 1 - i])
        delta[2] += 2
        delta[a + 1] -= 1
        delta[a + b] -= 1
        delta[a + b + 1] += 1
        delta[b + limit + 1] += 1
    best = n
    moves = 0
    for s in range(2, 2 * limit + 1):
        moves += delta[s]
        best = min(best, moves)
    return best


# ---- the harness ----------------------------------------------------------

seed = 1674


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


arrays = 100
n = 100000
rounds = 20
cases = []
for _ in range(arrays):
    limit = (next_random() * 32768 + next_random()) % 100000 + 1
    nums = [(next_random() * 32768 + next_random()) % limit + 1 for _ in range(n)]
    cases.append((nums, limit))
total = 0
check = 0
for r in range(rounds):
    for nums, limit in cases:
        moves = min_moves(nums, limit)
        total += moves
        check = (check * 31 + moves + r) % 1000000007
print(f"{arrays} arrays of {n} values, {rounds} rounds: {total} moves, checksum {check}")
