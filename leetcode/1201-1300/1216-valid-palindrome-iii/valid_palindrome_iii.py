# LeetCode #1216: Valid Palindrome III -- a Python mirror of the ★ arm: the
# longest palindromic subsequence, one row at a time, and the string a
# k-palindrome exactly when the letters outside it number at most k.


def is_valid_palindrome(s, k):
    b = s.encode()
    n = len(b)
    row = [0] * n
    for i in range(n - 1, -1, -1):
        row[i] = 1
        diagonal = 0
        for j in range(i + 1, n):
            below = row[j]
            row[j] = diagonal + 2 if b[i] == b[j] else max(row[j], row[j - 1])
            diagonal = below
    return n - row[n - 1] <= k


seed = 1216


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def least_k(s):
    lo, hi = 0, len(s)
    while lo < hi:
        mid = (lo + hi) // 2
        if is_valid_palindrome(s, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def show(b):
    return "true" if b else "false"


def main():
    cases = [("abcdeca", 2), ("abbababa", 1), ("a", 1), ("ab", 1), ("abc", 1), ("abcd", 2), ("abcd", 3), ("racecar", 1), ("abacdcaba", 1), ("abxcydzba", 2)]
    for s, k in cases:
        print(f"{s} {k}: {show(is_valid_palindrome(s, k))}")
    yes = 0
    check = 0
    for _ in range(1000):
        n = next_random() % 12 + 1
        letters = next_random() % 3 + 2
        s = random_text(n, letters)
        k = next_random() % n + 1
        answer = is_valid_palindrome(s, k)
        yes += answer
        check = (check * 131 + (2 if answer else 1)) % 1000000007
    print(f"1000 small cases: {yes} true, checksum {check}")
    s = random_text(1000, 26)
    k = least_k(s)
    print(f"1000 random letters: the least k {k}, and k - 1 {show(is_valid_palindrome(s, k - 1))}")
    s = random_text(1000, 2)
    print(f"1000 random a and b: the least k {least_k(s)}")
    half = random_text(500, 26)
    print(f"500 letters and their reverse: k 1 {show(is_valid_palindrome(half + half[::-1], 1))}")
    steps = "".join(chr(97 + i % 26) for i in range(1000))
    print(f"a to z over and over, 1000 letters: the least k {least_k(steps)}")


main()
