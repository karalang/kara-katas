# LeetCode #2309: Greatest English Letter in Upper and Lower Case -- the
# bench, the ★ arm in Python. A mask of the lowercase letters and one of
# the uppercase; the highest bit of their & is the answer.

seed = 2309


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def greatest_letter(s):
    lower = 0
    upper = 0
    for b in s.encode():
        if b >= 97:
            lower |= 1 << (b - 97)
        else:
            upper |= 1 << (b - 65)
    both = lower & upper
    for i in range(25, -1, -1):
        if (both >> i) & 1 == 1:
            return chr(65 + i)
    return ""


def main():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    strings = []
    for _ in range(1000):
        pool = next_random() % 30 + 1
        src = [letters[next_random() % 52] for _ in range(pool)]
        strings.append("".join(src[next_random() % pool] for _ in range(1000)))
    check = 0
    for _ in range(100):
        for s in strings:
            letter = greatest_letter(s)
            code = ord(letter) if letter else 0
            check = (check * 31 + code) % 1000000007
    print(f"100 passes over 1000 strings of 1000 letters: checksum {check}")


main()
