# LeetCode #738: Monotone Increasing Digits -- one drop, then nines.
# Benchmark mirror of the Kara star arm: the digits in a list, the first
# place where a digit is larger than the next, a step back over equal
# digits before it, that digit lowered by one and every digit after it
# made a 9.


def monotone_increasing_digits(n):
    digits = []
    x = n
    while x > 0:
        digits.append(x % 10)
        x //= 10
    digits.reverse()
    i = 0
    while i + 1 < len(digits) and digits[i] <= digits[i + 1]:
        i += 1
    if i + 1 < len(digits):
        while i > 0 and digits[i - 1] == digits[i]:
            i -= 1
        digits[i] -= 1
        for j in range(i + 1, len(digits)):
            digits[j] = 9
    out = 0
    for d in digits:
        out = out * 10 + d
    return out


def main():
    seed = 738
    total = 0
    kept = 0
    for _ in range(3000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        a = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        b = seed // 65536
        n = (a * 32768 + b) % 1000000001
        m = monotone_increasing_digits(n)
        if m == n:
            kept += 1
        total += m
    print(f"3000000 random numbers: {kept} already monotone, answers sum to {total}")


main()
