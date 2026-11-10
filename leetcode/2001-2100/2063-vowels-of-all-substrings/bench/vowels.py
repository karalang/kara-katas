# LeetCode #2063: Vowels of All Substrings -- Python mirror of the ★ arm's
# benchmark (vowels.kara): one text of 140000 letters, each a vowel with
# chance 40 in 100, and 200 windows of 100000 letters cut from it at a
# random place among its first 32768, each answered on its own.


def count_vowels(word):
    n = len(word)
    total = 0
    for i, c in enumerate(word):
        if c in "aeiou":
            total += (i + 1) * (n - i)
    return total


seed = 2063


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    out = []
    for _ in range(140000):
        if next_random() % 100 < 40:
            out.append("aeiou"[next_random() % 5])
        else:
            out.append("bcdxyz"[next_random() % 6])
    text = "".join(out)
    check = 0
    for _ in range(200):
        start = next_random()
        a = count_vowels(text[start:start + 100000])
        check = (check * 31 + a % 1000000007) % 1000000007
    print(f"200 windows: checksum {check}")


main()
