# LeetCode #1328: Break a Palindrome -- Python mirror of the ★ Kāra arm: the
# smallest change is the first letter of the first half that is not an a,
# made an a; a first half of nothing but a leaves the last letter, made a
# b. One letter cannot be broken.


def break_palindrome(palindrome):
    chars = list(palindrome)
    n = len(chars)
    if n == 1:
        return ""
    for i in range(n // 2):
        if chars[i] != "a":
            chars[i] = "a"
            return "".join(chars)
    chars[n - 1] = "b"
    return "".join(chars)


seed = 1328


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def ask(s):
    return f"[{break_palindrome(s)}]"


def main():
    long = break_palindrome("a" * 1000)
    print(f"{ask('abccba')} {ask('a')} {ask('aa')} {ask('aba')} {ask('zzz')} {ask('aabaa')} {len(long)} {'true' if long.endswith('ab') else 'false'}")
    letters = "abcdefghijklmnopqrstuvwxyz"
    empty = 0
    check = 0
    for t in range(600):
        n = 1 + next_random() % 200 if t % 5 == 0 else 1 + next_random() % 12
        k = 1 if t % 3 == 0 else 2 if t % 3 == 1 else 26
        half = [letters[next_random() % k] for _ in range((n + 1) // 2)]
        chars = half + [half[i] for i in reversed(range(n // 2))]
        got = break_palindrome("".join(chars))
        if len(got) == 0:
            empty += 1
        for b in got.encode():
            check = (check * 131 + b) % 1000000007
        check = (check * 131 + 1) % 1000000007
    print(f"600 random palindromes: {empty} left unbroken, checksum {check}")


main()
