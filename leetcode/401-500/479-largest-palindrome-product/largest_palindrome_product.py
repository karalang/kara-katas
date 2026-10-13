# LeetCode #479: Largest Palindrome Product -- Python mirror of the ★ arm
# (largest_palindrome_product.kara): palindromes from the top.


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
    for n in range(1, 9):
        print(f"n = {n} -> {largest_palindrome(n)}")


main()
