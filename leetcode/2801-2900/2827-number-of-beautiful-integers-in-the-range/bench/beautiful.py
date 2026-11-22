# LeetCode #2827: Number of Beautiful Integers in the Range -- the
# bench's Python mirror of the ★ arm: a digit DP up to high less one up
# to low - 1, the free started states memoized in a flat list.

import sys

sys.setrecursionlimit(10000)


def walk(digits, pos, diff, rem, tight, started, k, memo):
    n = len(digits)
    if pos == n:
        return 1 if started and diff == 0 and rem == 0 else 0
    key = (pos * (2 * n + 1) + diff + n) * k + rem
    if not tight and started and memo[key] >= 0:
        return memo[key]
    top = digits[pos] if tight else 9
    total = 0
    for d in range(top + 1):
        now = started or d > 0
        next_diff = diff + (1 if d % 2 == 0 else -1) if now else 0
        total += walk(digits, pos + 1, next_diff, (rem * 10 + d) % k, tight and d == top, now, k, memo)
    if not tight and started:
        memo[key] = total
    return total


def count_upto(x, k):
    if x <= 0:
        return 0
    digits = [int(c) for c in str(x)]
    n = len(digits)
    memo = [-1] * (n * (2 * n + 1) * k)
    return walk(digits, 0, 0, 0, True, False, k, memo)


def number_of_beautiful_integers(low, high, k):
    return count_upto(high, k) - count_upto(low - 1, k)


seed = 2827


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds = 2000, 5
    cases = []
    for _ in range(count):
        a = wide() % 1000000000 + 1
        b = wide() % 1000000000 + 1
        cases.append((min(a, b), max(a, b), next_random() % 20 + 1))
    total = 0
    check = 0
    for r in range(rounds):
        for low, high, k in cases:
            a = number_of_beautiful_integers(low, high, k)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} ranges, {rounds} rounds: {total} beautiful, checksum {check}")


main()
