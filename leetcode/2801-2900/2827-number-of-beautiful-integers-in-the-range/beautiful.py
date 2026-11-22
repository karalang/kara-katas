# LeetCode #2827: Number of Beautiful Integers in the Range -- the Python
# mirror of the ★ arm: a digit DP up to high less one up to low - 1, the
# free started states memoized in a flat list.

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


# ---- the harness: the same in every arm --------------------------------

seed = 2827


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    print(number_of_beautiful_integers(10, 20, 3))
    print(number_of_beautiful_integers(1, 10, 1))
    print(number_of_beautiful_integers(5, 5, 2))
    print(number_of_beautiful_integers(1, 1000000000, 1))
    print(number_of_beautiful_integers(1, 1000000000, 7))
    print(number_of_beautiful_integers(1, 1000000000, 20))
    print(number_of_beautiful_integers(1234, 1234, 2))
    print(number_of_beautiful_integers(100000, 999999, 3))
    check = 0
    for _ in range(300):
        a = wide() % 1000000000 + 1
        b = wide() % 1000000000 + 1
        k = next_random() % 20 + 1
        check = (check * 31 + number_of_beautiful_integers(min(a, b), max(a, b), k)) % 1000000007
    print(f"300 wide ranges: checksum {check}")
    check = 0
    for _ in range(300):
        a = wide() % 1000000000 + 1
        b = min(a + next_random() % 1000, 1000000000)
        k = next_random() % 20 + 1
        check = (check * 31 + number_of_beautiful_integers(a, b, k)) % 1000000007
    print(f"300 narrow ranges: checksum {check}")


main()
