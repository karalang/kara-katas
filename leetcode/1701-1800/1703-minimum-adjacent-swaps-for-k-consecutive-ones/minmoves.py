# LeetCode #1703: Minimum Adjacent Swaps for K Consecutive Ones -- the
# Python mirror of the ★ arm (minmoves.kara): the window of k ones
# gathered to its median, by prefix sums of q[j] = p[j] - j.


def min_moves(nums, k):
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


def batch(count, most, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random(seed) * 32768 + next_random(seed)) % most + 1
        lean = next_random(seed) % 11
        nums = [1 if next_random(seed) % 10 < lean else 0 for _ in range(n)]
        if all(v == 0 for v in nums):
            nums[next_random(seed) % n] = 1
        ones = nums.count(1)
        k = next_random(seed) % ones + 1
        answer = min_moves(nums, k)
        total += answer
        check = (check * 31 + answer + k) % 1000000007
    print(f"{count} arrays of up to {most} values: answers sum to {total}, checksum {check}")


def main():
    # LeetCode's three examples, then k = 1, and three 1s a gap apart
    print(min_moves([1, 0, 0, 1, 0, 1], 2))
    print(min_moves([1, 0, 0, 0, 0, 0, 1, 1], 3))
    print(min_moves([1, 1, 0, 1], 2))
    print(min_moves([0, 0, 1, 0], 1))
    print(min_moves([1, 0, 1, 0, 1], 3))
    seed = [1703]
    batch(3000, 12, seed)
    batch(300, 1000, seed)
    batch(10, 100000, seed)


main()
