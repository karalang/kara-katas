# LeetCode #2309: Greatest English Letter in Upper and Lower Case -- the
# ★ arm in Python. Two 26-bit masks, one of the lowercase letters seen
# and one of the uppercase; their & holds the letters seen both ways, and
# its highest bit is the answer.


def greatest_letter(s):
    lower = 0
    upper = 0
    for ch in s:
        b = ord(ch)
        if b >= ord("a"):
            lower |= 1 << (b - ord("a"))
        else:
            upper |= 1 << (b - ord("A"))
    both = lower & upper
    for i in range(25, -1, -1):
        if (both >> i) & 1 == 1:
            return chr(ord("A") + i)
    return ""


seed = 2309


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for s in ["lEeTcOdE", "arRAzFif", "AbCdEfGhIjK", "qQ", "zabcdefghijklmnopqrstuvwxyZ", "Aa", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]:
        letter = greatest_letter(s)
        print(f'"{s}": "{letter}"')
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    check = 0
    found = 0
    for _ in range(2000):
        pool = next_random() % 24 + 1
        src = [letters[next_random() % 52] for _ in range(pool)]
        s = "".join(src[next_random() % pool] for _ in range(next_random() % 60 + 1))
        letter = greatest_letter(s)
        code = ord(letter) if letter else 0
        check = (check * 31 + code) % 1000000007
        if code > 0:
            found += 1
    print(f"2000 strings: checksum {check}, {found} with a letter in both cases")


main()
