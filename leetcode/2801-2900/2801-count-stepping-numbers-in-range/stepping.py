# LeetCode #2801: Count Stepping Numbers in Range -- the Python mirror of
# the ★ arm: a digit walk with a memo over place and last digit for the
# untight, started states; the count to high less the count to low, and
# low itself when it steps.
import sys

sys.setrecursionlimit(10000)
MOD = 1000000007


def walk(digits, pos, last, tight, started, memo):
    if pos == len(digits):
        return 1 if started else 0
    free = started and not tight
    if free and memo[pos][last] >= 0:
        return memo[pos][last]
    top = digits[pos] if tight else 9
    ways = 0
    for d in range(top + 1):
        next_tight = tight and d == top
        if not started:
            ways += walk(digits, pos + 1, d, next_tight, d > 0, memo)
        elif abs(d - last) == 1:
            ways += walk(digits, pos + 1, d, next_tight, True, memo)
    ways %= MOD
    if free:
        memo[pos][last] = ways
    return ways


def count_up_to(s):
    digits = [ord(c) - 48 for c in s]
    memo = [[-1] * 10 for _ in digits]
    return walk(digits, 0, 0, True, False, memo)


def steps(s):
    return all(abs(ord(s[i]) - ord(s[i - 1])) == 1 for i in range(1, len(s)))


def count_stepping_numbers(low, high):
    own = 1 if steps(low) else 0
    return ((count_up_to(high) - count_up_to(low) + own) % MOD + MOD) % MOD


seed = 2801


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def number(m, near):
    d = next_random() % 9 + 1
    s = str(d)
    for _ in range(1, m):
        r = next_random() % 10
        if near and r < 8:
            d = d - 1 if (r % 2 == 0 and d > 0) or d == 9 else d + 1
        else:
            d = r
        s += str(d)
    return s


def ordered(a, b):
    if len(a) < len(b) or (len(a) == len(b) and a <= b):
        return a, b
    return b, a


def main():
    print(count_stepping_numbers("1", "11"))
    print(count_stepping_numbers("90", "101"))
    print(count_stepping_numbers("1", "9" * 100))
    one = "10" * 50
    print(count_stepping_numbers(one, one))
    top = "1" + "0" * 99
    print(count_stepping_numbers(top, "9" * 100))
    total = 0
    check = 0
    for _ in range(3000):
        a = next_random() % 10000 + 1
        b = next_random() % 10000 + 1
        low, high = ordered(str(a), str(b))
        ans = count_stepping_numbers(low, high)
        total += ans
        check = (check * 31 + ans) % 1000000007
    print(f"3000 ranges up to 10^4: counts sum to {total}, checksum {check}")
    total = 0
    check = 0
    for t in range(50):
        near = t % 2 == 0
        a = number(next_random() % 100 + 1, near)
        b = number(next_random() % 100 + 1, near)
        low, high = ordered(a, b)
        ans = count_stepping_numbers(low, high)
        total += ans
        check = (check * 31 + ans) % 1000000007
    print(f"50 ranges of up to 100 digits: counts sum to {total}, checksum {check}")


main()
