# LeetCode #2801: Count Stepping Numbers in Range -- the bench in Python:
# the ★ arm over 400 ranges of 100-digit bounds made mostly of steps, all
# drawn first, then each answered 20 times.

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


def number(m):
    d = next_random() % 9 + 1
    s = str(d)
    for _ in range(1, m):
        r = next_random() % 10
        if r < 8:
            d = d - 1 if (r % 2 == 0 and d > 0) or d == 9 else d + 1
        else:
            d = r
        s += str(d)
    return s


def main():
    count = 400
    rounds = 20
    cases = []
    for _ in range(count):
        a = number(100)
        b = number(100)
        cases.append((a, b) if a <= b else (b, a))
    total = 0
    check = 0
    for r in range(rounds):
        for low, high in cases:
            a = count_stepping_numbers(low, high)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} ranges of 100 digits, {rounds} rounds: counts sum to {total}, checksum {check}")


main()
