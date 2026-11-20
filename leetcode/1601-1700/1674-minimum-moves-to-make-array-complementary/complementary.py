# LeetCode #1674: Minimum Moves to Make Array Complementary -- the Python
# mirror of the ★ arm: a difference array over the target sums.


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


# ---- the harness: the same as the Kāra arms -------------------------------

seed = 1674


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, pairs, most):
    total = 0
    check = 0
    for _ in range(count):
        n = 2 * (next_random() % pairs + 1)
        limit = next_random() % most + 1
        nums = [next_random() % limit + 1 for _ in range(n)]
        moves = min_moves(nums, limit)
        total += moves
        check = (check * 31 + moves + n) % 1000000007
    print(f"{count} arrays of up to {pairs} pairs, limits up to {most}: {total} moves, checksum {check}")


print(min_moves([1, 2, 4, 3], 4))
print(min_moves([1, 2, 2, 1], 2))
print(min_moves([1, 2, 1, 2], 2))
print(min_moves([1, 1, 1, 4], 4))
print(min_moves([3, 3], 3))
batch(3000, 6, 6)
batch(300, 100, 100)
batch(10, 1000, 1000)
