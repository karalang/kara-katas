# LeetCode #2818: Apply Operations to Maximize Score -- the bench's Python
# mirror of the ★ arm: a sieve of prime scores, one monotonic stack for each
# number's stretch, the numbers largest first, each power by squaring.

MOD = 1000000007


def prime_scores(limit):
    score = [0] * (limit + 1)
    for p in range(2, limit + 1):
        if score[p] == 0:
            q = p
            while q <= limit:
                score[q] += 1
                q += p
    return score


def power(base, exp):
    result = 1
    b = base % MOD
    e = exp
    while e > 0:
        if e % 2 == 1:
            result = result * b % MOD
        b = b * b % MOD
        e //= 2
    return result


def maximum_score(nums, k):
    n = len(nums)
    score = prime_scores(max(nums))
    s = [score[v] for v in nums]
    left = [-1] * n
    right = [n] * n
    stack = []
    for i in range(n):
        while stack and s[stack[-1]] < s[i]:
            right[stack.pop()] = i
        if stack:
            left[i] = stack[-1]
        stack.append(i)
    order = sorted(range(n), key=lambda i: -nums[i])
    rest = k
    total = 1
    for i in order:
        if rest == 0:
            break
        take = min((i - left[i]) * (right[i] - i), rest)
        total = total * power(nums[i], take) % MOD
        rest -= take
    return total


seed = 2818


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 20, 3, 100000
    cases = []
    for _ in range(count):
        nums = [wide() % 100000 + 1 for _ in range(n)]
        cases.append((nums, wide() % 1000000000 + 1))
    total = 0
    check = 0
    for r in range(rounds):
        for nums, k in cases:
            a = maximum_score(nums, k)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of {n}, {rounds} rounds: scores sum to {total}, checksum {check}")


main()
