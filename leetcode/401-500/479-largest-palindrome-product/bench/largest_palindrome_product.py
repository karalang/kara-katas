# Benchmark for #479: Python mirror of the ★ arm (palindromes from the
# top); see largest_palindrome_product.kara.


def largest_palindrome(n):
    if n == 1:
        return 9
    upper = 10 ** n
    lower = upper // 10
    upper -= 1
    half = upper
    while half >= lower:
        palindrome = half
        rest = half
        while rest > 0:
            palindrome = palindrome * 10 + rest % 10
            rest //= 10
        factor = upper
        while factor * factor >= palindrome:
            if palindrome % factor == 0 and palindrome // factor >= lower:
                return palindrome % 1337
            factor -= 1
        half -= 1
    return -1


def main():
    rounds = 10
    total = 0
    checksum = 0
    for _ in range(rounds):
        for n in range(1, 9):
            got = largest_palindrome(n)
            total += got
            checksum = (checksum * 31 + got) % 1000000007
    print(f"{rounds} rounds of n = 1 to 8: answers add up to {total}, checksum {checksum}")


main()
