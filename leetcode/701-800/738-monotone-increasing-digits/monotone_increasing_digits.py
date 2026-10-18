# LeetCode #738: Monotone Increasing Digits -- one drop, then nines.
# Mirror of the Kara star arm: find the first place where a digit is
# larger than the next, step back over equal digits before it, lower
# that digit by one and make every digit after it a 9.


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


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(n):
    print(f"{n} -> {monotone_increasing_digits(n)}")


def main():
    for n in [10, 1234, 332, 0, 9, 120, 100, 1000000000, 999999999,
              111111110, 123454321, 668841, 77777, 101010101]:
        show(n)
    seed = [738]
    total_sum = 0
    kept = 0
    for _ in range(10000):
        digits = 1 + next_random(seed) % 10
        n = 0
        for _ in range(digits):
            n = n * 10 + next_random(seed) % 10
        if n > 1000000000:
            n = n % 1000000001
        m = monotone_increasing_digits(n)
        if m == n:
            kept += 1
        total_sum = (total_sum * 131 + m % 1000003 + 1) % 1000000007
    print(f"10000 random numbers: {kept} already monotone, checksum {total_sum}")
    total = 0
    for n in range(100000):
        total += monotone_increasing_digits(n)
    print(f"0 to 99999: answers sum to {total}")


main()
