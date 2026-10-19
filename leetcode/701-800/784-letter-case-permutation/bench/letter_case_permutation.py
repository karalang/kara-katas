# LeetCode 784 — Letter Case Permutation: the bench, in Python.
# Mirrors letter_case_permutation.kara: backtracking over the same 64
# strings.


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


def main():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    strings = []
    for _ in range(64):
        wanted = 6 + next_random() % 6
        is_letter = [i < wanted for i in range(12)]
        i = 11
        while i > 0:
            j = next_random() % (i + 1)
            is_letter[i], is_letter[j] = is_letter[j], is_letter[i]
            i -= 1
        s = []
        for i in range(12):
            if is_letter[i]:
                s.append(letters[next_random() % 52])
            else:
                s.append(digits[next_random() % 10])
        strings.append("".join(s))
    rounds = 20000
    total = 0
    check = 0
    for r in range(rounds):
        all_ = letter_case_permutation(strings[r % 64])
        total += len(all_)
        for w in all_:
            check = (check * 31 + ord(w[0]) + 7 * ord(w[11])) % 1000000007
    print(f"{rounds} rounds of 12-character strings: {total} permutations, checksum {check}")


main()
