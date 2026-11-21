# LeetCode #2423: Remove Letter To Equalize Frequency -- the Python mirror
# of the ★ arm: the 26 letter counts, each held letter taken away once in
# turn, and the counts left that are not zero compared.

seed = 2423


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def equal_frequency(word):
    count = [0] * 26
    for b in word.encode():
        count[b - 97] += 1
    for c in range(26):
        if count[c] == 0:
            continue
        count[c] -= 1
        want = 0
        equal = True
        for k in range(26):
            if count[k] > 0:
                if want == 0:
                    want = count[k]
                elif count[k] != want:
                    equal = False
        count[c] += 1
        if equal:
            return True
    return False


def random_word(n, kinds, stay):
    out = []
    for i in range(n):
        if i > 0 and next_random() % stay == 0:
            out.append(out[i - 1])
        else:
            out.append(97 + next_random() % kinds)
    return bytes(out).decode()


def main():
    for w in ["abcc", "aazz", "ab", "aa", "aabbccc", "abbcc", "aabbcccc", "abcdefghijklmnopqrstuvwxyz"]:
        print(f"{w}: {'true' if equal_frequency(w) else 'false'}")
    trues = 0
    check = 0
    for _ in range(3000):
        n = 2 + next_random() % 99
        kinds = 1 + next_random() % 6
        stay = 1 + next_random() % 3
        a = equal_frequency(random_word(n, kinds, stay))
        trues += a
        check = (check * 2 + a) % 1000000007
    print(f"3000 random: {trues} true, checksum {check}")
    trues = 0
    check = 0
    for _ in range(3000):
        kinds = 1 + next_random() % 5
        times = 1 + next_random() % 4
        bs = [97 + k for k in range(kinds) for _ in range(times)]
        pick = 97 + next_random() % (kinds + 1)
        if next_random() % 2 == 0:
            bs.append(pick)
        else:
            at = next_random() % len(bs)
            del bs[at]
        for i in range(len(bs) - 1, 0, -1):
            j = next_random() % (i + 1)
            bs[i], bs[j] = bs[j], bs[i]
        while len(bs) < 2:
            bs.append(97)
        a = equal_frequency(bytes(bs).decode())
        trues += a
        check = (check * 2 + a) % 1000000007
    print(f"3000 near: {trues} true, checksum {check}")


if __name__ == "__main__":
    main()
