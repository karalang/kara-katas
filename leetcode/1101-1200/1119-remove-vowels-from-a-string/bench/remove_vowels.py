# LeetCode #1119: Remove Vowels from a String -- the bench in Python, the
# ★ arm over the same 64 texts and 2000 rounds.


def remove_vowels(s):
    return "".join(c for c in s if c not in "aeiou")


seed = 1119


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    letters = "abcdefghijklmnopqrstuvwxyz"
    texts = [[letters[next_random() % 26] for _ in range(1000)] for _ in range(64)]
    kept = check = 0
    for rnd in range(2000):
        for j in range(len(texts)):
            at = (rnd * 7919 + j * 104729) % 1000
            texts[j][at] = letters[(rnd + j) % 26]
            r = remove_vowels("".join(texts[j]))
            kept += len(r)
            check = (check * 31 + len(r) + (ord(r[0]) if r else 0)) % 1000000007
    print(f"2000 rounds over 64 texts of 1000 letters: {kept} letters kept, checksum {check}")


main()
