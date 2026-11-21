# LeetCode #2423: Remove Letter To Equalize Frequency -- the bench, the ★
# arm: the 26 letter counts, each held letter taken away once in turn and
# the counts left that are not zero compared.

seed = 2423


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def equal_frequency(word):
    count = [0] * 26
    for b in word:
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


def main():
    words = []
    for _ in range(10000):
        kinds = 1 + next_random() % 20
        times = 1 + next_random() % 5
        bs = [97 + k for k in range(kinds) for _ in range(times)]
        if next_random() % 2 == 0:
            bs.append(97 + next_random() % 26)
        else:
            at = next_random() % len(bs)
            del bs[at]
        for i in range(len(bs) - 1, 0, -1):
            j = next_random() % (i + 1)
            bs[i], bs[j] = bs[j], bs[i]
        while len(bs) < 2:
            bs.append(97)
        words.append(bytes(bs))
    check = 0
    for p in range(200):
        for w in words:
            check = (check * 3 + (1 if equal_frequency(w) else 0) + p) % 1000000007
    print(f"200 passes over 10^4 words: checksum {check}")


main()
