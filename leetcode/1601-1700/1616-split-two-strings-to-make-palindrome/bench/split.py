# LeetCode #1616: Split Two Strings to Make Palindrome -- the bench in
# Python, mirroring split.kara: two pointers, a from the front against b
# from the back as far as they agree, then whether the middle left over,
# of a or of b, is a palindrome by itself; then the roles swapped.


def is_palindrome(s, lo, hi):
    i, j = lo, hi
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True


def joins(a, b):
    i, j = 0, len(a) - 1
    while i < j and a[i] == b[j]:
        i += 1
        j -= 1
    return is_palindrome(a, i, j) or is_palindrome(b, i, j)


def check_palindrome_formation(a, b):
    return joins(a, b) or joins(b, a)


seed = 1616


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def pair(n):
    a = []
    b = []
    for _ in range(n):
        a.append(chr(ord("a") + next_random() % 2))
        b.append(chr(ord("a") + next_random() % 2))
    k = next_random() % (n // 2 + 1)
    for j in range(k):
        b[n - 1 - j] = a[j]
    for j in range((n - 2 * k) // 2):
        b[n - k - 1 - j] = b[k + j]
    if next_random() % 2 == 0:
        i = next_random() % n
        b[i] = chr(ord("a") + next_random() % 2)
    return "".join(a), "".join(b)


pairs = [pair(500000) for _ in range(10)]
check = yes = 0
for a, b in pairs:
    for _ in range(30):
        answer = check_palindrome_formation(a, b)
        if answer:
            yes += 1
        check = mix(check, 1 if answer else 0)
print(f"10 pairs of 500000 letters from 2, each checked 30 times: {yes} split, checksum {check}")
