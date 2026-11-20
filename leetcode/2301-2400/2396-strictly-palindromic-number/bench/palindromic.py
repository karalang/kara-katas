# LeetCode #2396: Strictly Palindromic Number -- the bench, the ★ arm in
# Python: every base tried, each base's digits taken into a list and
# checked from both ends.


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


def main():
    check = 0
    total = 0
    for n in range(4, 10001):
        count = 0
        for b in range(2, n - 1):
            if palindrome_in_base(n, b):
                count += 1
        total += count
        check = (check * 31 + count + (1 if is_strictly_palindromic(n) else 0)) % 1000000007
    print(f"every base of every n from 4 to 10000: checksum {check}, {total} palindromes")


main()
