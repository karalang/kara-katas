# LeetCode #1616: Split Two Strings to Make Palindrome -- the Python mirror
# of split.kara: match a from the front against b from the back as far as
# they agree, then ask whether the middle part left over, of a or of b,
# is a palindrome by itself; then the same with the roles swapped.


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


def random_word(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


def batch(count, most, letters):
    check = chars = yes = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        a = random_word(n, letters)
        b = random_word(n, letters)
        if next_random() % 2 == 0:
            k = next_random() % (n // 2 + 1)
            tail = a[:k][::-1]
            m = n - 2 * k
            half = b[k:k + (m + 1) // 2]
            back = half[::-1][m % 2:]
            b = b[:k] + half + back + tail
            if next_random() % 4 == 0:
                i = next_random() % n
                a = a[:i] + chr(ord("a") + next_random() % letters) + a[i + 1:]
        answer = check_palindrome_formation(a, b)
        if answer:
            yes += 1
        check = mix(check, 1 if answer else 0)
        chars += n
    print(f"{count} pairs of up to {most} letters from {letters}: {chars} letters each side, {yes} can split, checksum {check}")


examples = [("x", "y"), ("xbdef", "xecab"), ("ulacfd", "jizalu"), ("ab", "cd"), ("aba", "xyz"), ("pqrcd", "abcqp")]
for a, b in examples:
    print("true" if check_palindrome_formation(a, b) else "false")
batch(3000, 6, 2)
batch(300, 1000, 3)
batch(30, 20000, 26)
