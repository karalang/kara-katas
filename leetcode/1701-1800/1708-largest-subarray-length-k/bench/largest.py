# LeetCode #1708: Largest Subarray Length K -- the Python mirror of the
# bench (largest.kara): the largest first value among the starts that
# leave room for k, on 50 random arrays of 100000 distinct values, each
# answered 100 times.


def largest_subarray(nums, k):
    best = 0
    for i in range(1, len(nums) - k + 1):
        if nums[i] > nums[best]:
            best = i
    return nums[best:best + k]


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count = 50
    rounds = 100
    n = 100000
    seed = [1708]
    problems = []
    for _ in range(count):
        nums = list(range(n))
        for i in range(n - 1, 0, -1):
            a = next_random(seed)
            j = (a * 32768 + next_random(seed)) % (i + 1)
            nums[i], nums[j] = nums[j], nums[i]
        for i in range(n):
            nums[i] = nums[i] * 10000 + next_random(seed) % 10000
        a = next_random(seed)
        k = (a * 32768 + next_random(seed)) % n + 1
        problems.append((nums, k))
    chosen = 0
    check = 0
    for r in range(rounds):
        for nums, k in problems:
            answer = largest_subarray(nums, k)
            chosen += len(answer)
            check = (check * 31 + len(answer) + answer[0] + answer[-1] + r) % 1000000007
    print(f"{count} arrays of {n} values, {rounds} rounds: {chosen} chosen, checksum {check}")


main()
