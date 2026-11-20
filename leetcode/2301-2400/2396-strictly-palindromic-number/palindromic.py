# LeetCode #2396: Strictly Palindromic Number -- the Python mirror of the
# ★ arm, every base tried, each base's digits checked from both ends.

seed = 2396


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def palindrome_in_base(n, b):
    digits = []
    m = n
    while m > 0:
        digits.append(m % b)
        m //= b
    i, j = 0, len(digits) - 1
    while i < j:
        if digits[i] != digits[j]:
            return False
        i += 1
        j -= 1
    return True


def is_strictly_palindromic(n):
    for b in range(2, n - 1):
        if not palindrome_in_base(n, b):
            return False
    return True


def show(x):
    return "true" if x else "false"


def main():
    print(f"n = 9: {show(is_strictly_palindromic(9))}")
    print(f"n = 4: {show(is_strictly_palindromic(4))}")
    shown = list(range(4, 61)) + [1000, 65535, 99999, 100000]
    for n in shown:
        count = sum(1 for b in range(2, n - 1) if palindrome_in_base(n, b))
        print(f"{n}: {count} of {n - 3} bases, strictly {show(is_strictly_palindromic(n))}")
    check = 0
    yes = 0
    for t in range(3000):
        b = 2 + next_random() % 30
        n = 1 + next_random() % 2000
        if t % 3 > 0:
            half = 1 + next_random() % 3
            digits = [next_random() % b for _ in range(half)]
            if digits[0] == 0:
                digits[0] = 1
            i = half - 1 - next_random() % 2
            while i >= 0:
                digits.append(digits[i])
                i -= 1
            if t % 3 == 2:
                at = 1 + next_random() % max(len(digits) - 1, 1)
                if at < len(digits):
                    digits[at] = (digits[at] + 1) % b
            n = 0
            for d in digits:
                n = n * b + d
        p = palindrome_in_base(n, b)
        if p:
            yes += 1
        check = (check * 31 + (2 if p else 1)) % 1000000007
    print(f"3000 random: checksum {check}, {yes} palindromes")


main()
