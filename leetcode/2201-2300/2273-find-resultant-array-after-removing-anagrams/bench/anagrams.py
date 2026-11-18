# LeetCode #2273: Find Resultant Array After Removing Anagrams -- the
# bench, the ★ arm.


def sorted_letters(word):
    return "".join(sorted(word))


def remove_anagrams(words):
    kept = []
    last = ""
    for w in words:
        key = sorted_letters(w)
        if not kept or key != last:
            kept.append(w)
        last = key
    return kept


# ---- bench harness ---------------------------------------------------------

seed = 2273


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(20000):
        words = []
        for i in range(100):
            if i > 0 and next_random() % 2 == 0:
                letters = list(words[i - 1])
                for j in range(9, 0, -1):
                    r = next_random() % (j + 1)
                    letters[j], letters[r] = letters[r], letters[j]
                words.append("".join(letters))
            else:
                words.append("".join(chr(97 + next_random() % 4) for _ in range(10)))
        kept = remove_anagrams(words)
        check = (check * 31 + len(kept) * 1000 + ord(kept[-1][0])) % 1000000007
    print(f"20000 lists of 100: checksum {check}")


main()
