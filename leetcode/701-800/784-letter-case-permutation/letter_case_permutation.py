# LeetCode 784 — Letter Case Permutation, backtracking.
# Mirrors letter_case_permutation.kara (the ★ arm) and its harness.


def permute(at, buf, out):
    if at == len(buf):
        out.append("".join(buf))
        return
    c = buf[at]
    if c.isascii() and c.isalpha():
        buf[at] = c.lower()
        permute(at + 1, buf, out)
        buf[at] = c.upper()
        permute(at + 1, buf, out)
        buf[at] = c
    else:
        permute(at + 1, buf, out)


def letter_case_permutation(s):
    out = []
    permute(0, list(s), out)
    return out


seed = 784


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def sorted_permutations(s):
    return sorted(letter_case_permutation(s))


def show(s):
    print(f'"{s}" -> [{", ".join(sorted_permutations(s))}]')


def checksum(words, check):
    for p in words:
        for b in p.encode():
            check = (check * 131 + b) % 1000000007
    return check


def main():
    for s in ["a1b2", "3z4", "12345", "C", "aBc", "Zz9"]:
        show(s)
    words = sorted_permutations("abcdefghijkl")
    check = checksum(words, 0)
    print(f'"abcdefghijkl" -> {len(words)} strings, first {words[0]}, '
          f"last {words[-1]}, checksum {check}")
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    strings = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 12
        s = "".join(alphabet[next_random() % 62] for _ in range(n))
        words = sorted_permutations(s)
        strings += len(words)
        check = checksum(words, check)
    print(f"300 random strings: {strings} permutations, checksum {check}")


main()
