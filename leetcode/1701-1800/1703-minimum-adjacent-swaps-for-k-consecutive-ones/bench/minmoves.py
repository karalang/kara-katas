# LeetCode #1703: Minimum Adjacent Swaps for K Consecutive Ones -- the
# bench's Python mirror: the ★ arm on 50 random arrays of 100000 values,
# each with a random k, all drawn first, each answered 40 times.


def min_moves(nums, k):
    # each window of k ones about its median, q[j] = p[j] - j, by prefix sums
    q = []
    for i, v in enumerate(nums):
        if v == 1:
            q.append(i - len(q))
    prefix = [0]
    for x in q:
        prefix.append(prefix[-1] + x)
    best = None
    for i in range(len(q) - k + 1):
        end = i + k
        m = i + k // 2
        left = q[m] * (m - i) - (prefix[m] - prefix[i])
        right = (prefix[end] - prefix[m + 1]) - q[m] * (end - m - 1)
        if best is None or left + right < best:
            best = left + right
    return best


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count, rounds, n = 50, 40, 100000
    seed = [1703]
    arrays = []
    for _ in range(count):
        # each value a 1 with a chance of its array's own, 1 to 10 in 10
        lean = next_random(seed) % 10 + 1
        nums = [1 if next_random(seed) % 10 < lean else 0 for _ in range(n)]
        k = next_random(seed) % nums.count(1) + 1
        arrays.append((nums, k))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, k in arrays:
            answer = min_moves(nums, k)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} arrays of {n} values, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
