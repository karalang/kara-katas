# LeetCode 744 — Find Smallest Letter Greater Than Target, binary search.
# Mirror of next_greatest_letter.kara (the ★ arm); same output, byte for byte.


def next_greatest_letter(letters, target):
    lo = 0
    hi = len(letters)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if letters[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return letters[0] if lo == len(letters) else letters[lo]


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(text, target):
    letters = list(text)
    print(f"[{', '.join(letters)}], target {target} -> {next_greatest_letter(letters, target)}")


def random_letters(rng, n, first, step):
    letters = []
    c = ord(first)
    for _ in range(n):
        if rng.next() % step == 0 and c < ord('z'):
            c += 1
        letters.append(chr(c))
    if letters[0] == letters[n - 1]:
        letters[n - 1] = chr(ord(letters[0]) + 1)
    return letters


def main():
    show("cfj", 'a')
    show("cfj", 'c')
    show("xxyy", 'z')
    show("cfj", 'd')
    show("cfj", 'g')
    show("cfj", 'j')
    show("ab", 'z')
    show("az", 'y')
    show("eeeeennn", 'e')

    rng = Rng(744)
    big = random_letters(rng, 10000, 'a', 500)
    answers = "".join(next_greatest_letter(big, chr(t + ord('a'))) for t in range(26))
    print(f"10000 letters from {big[0]} to {big[9999]}, every target: {answers}")

    wraps = 0
    check = 0
    for _ in range(300):
        n = 2 + rng.next() % 11
        first = chr(rng.next() % 20 + ord('a'))
        letters = random_letters(rng, n, first, 3)
        target = chr(rng.next() % 26 + ord('a'))
        got = next_greatest_letter(letters, target)
        if got <= target:
            wraps += 1
        check = (check * 31 + ord(got)) % 1000000007
    print(f"300 random lists: {wraps} wrap round, checksum {check}")


main()
