# LeetCode #2818: Apply Operations to Maximize Score -- the Python mirror
# of the ★ arm: a sieve of prime scores, one monotonic stack for each
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


# ---- the harness: the same in every arm --------------------------------

seed = 2818


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    return next_random() * 32768 + next_random()


def main():
    global seed
    print(maximum_score([8, 3, 9, 3, 8], 2))
    print(maximum_score([19, 12, 14, 6, 10, 18], 3))
    print(maximum_score([1], 1))
    print(maximum_score([2, 30, 6, 7], 10))
    print(maximum_score([[2, 3, 5, 7, 11, 13][i % 6] for i in range(2000)], 2001000))
    print(maximum_score([[30030, 2310, 210, 30, 6, 2][i * 6 // 2000] for i in range(2000)], 1999000))
    check = 0
    for _ in range(3000):
        n = next_random() % 10 + 1
        nums = [next_random() % 100 + 1 for _ in range(n)]
        k = next_random() % (n * (n + 1) // 2) + 1
        check = (check * 31 + maximum_score(nums, k)) % 1000000007
    print(f"3000 small arrays: checksum {check}")
    check = 0
    for _ in range(50):
        n = next_random() % 2000 + 1
        nums = [(next_random() * 32768 + next_random()) % 100000 + 1 for _ in range(n)]
        k = wide() % min(n * (n + 1) // 2, 1000000000) + 1
        check = (check * 31 + maximum_score(nums, k)) % 1000000007
    print(f"50 large arrays: checksum {check}")


main()
