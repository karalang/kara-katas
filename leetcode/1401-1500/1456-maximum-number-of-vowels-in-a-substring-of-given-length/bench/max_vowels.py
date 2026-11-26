# LeetCode #1456 bench mirror: a window of k letters slid along the string,
# its vowels counted as a letter comes in and another goes out.


def max_vowels(s, k):
    letters = list(s)
    count = 0
    for i in range(k):
        if letters[i] in "aeiou":
            count += 1
    best = count
    for i in range(k, len(letters)):
        if letters[i] in "aeiou":
            count += 1
        if letters[i - k] in "aeiou":
            count -= 1
        best = max(best, count)
    return best


def main():
    # 200 strings of 10^5 letters, a vowel one time in 3, drawn once, each
    # asked for windows of 1 to 10^5 letters 5 times, the answers folded to
    # a checksum
    seed = 1456
    vowels = "aeiou"
    others = "bcdfghjklmnpqrstvwxyz"
    texts = []
    for _ in range(200):
        out = []
        for _ in range(100000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            odd = seed // 65536 % 3 == 0
            seed = (seed * 1103515245 + 12345) % 2147483648
            pick = seed // 65536
            out.append(vowels[pick % 5] if odd else others[pick % 21])
        texts.append("".join(out))
    check = 0
    for _ in range(5):
        for s in texts:
            seed = (seed * 1103515245 + 12345) % 2147483648
            k = 1 + seed // 65536 % 100000
            check = (check * 131 + max_vowels(s, k)) % 1000000007
    print(f"1000 windows of 10^5 letters: checksum {check}")


main()
