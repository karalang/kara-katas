# Benchmark: LeetCode #962 Maximum Width Ramp -- the ★ arm, decreasing
# stack, on 50000 numbers falling overall with noise. Mirrors
# max_width_ramp.kara.


def max_width_ramp(nums):
    n = len(nums)
    stack = []
    for i in range(n):
        if not stack or nums[i] < nums[stack[-1]]:
            stack.append(i)
    best = 0
    j = n - 1
    while j >= 0 and stack:
        while stack and nums[stack[-1]] <= nums[j]:
            best = max(best, j - stack[-1])
            stack.pop()
        j -= 1
    return best


seed = 962


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def falling(n, step, noise):
    return [50000 - noise - p // step + next_random() % (noise + 1) for p in range(n)]


def main():
    rounds = 40
    cases = [falling(50000, 1 + i % 5, 10 * (i // 5)) for i in range(50)]
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(50):
            c = (r + i) % 50
            p = next_random() % 50000
            cases[c][p] = next_random() % 50001
            w = max_width_ramp(cases[c])
            total += w
            check = (check * 31 + w + i) % 1000000007
    print(f"{rounds} rounds over 50 cases of 50000 numbers: the ramps sum to {total}, checksum {check}")


main()
