# LeetCode #2514: Count Anagrams -- Python mirror of the ★ arm
# (anagrams.kara): factorials built once, each word's length factorial
# over its letters' factorials by Fermat inverses, and its harness, line
# for line.
MOD = 1000000007


def count_anagrams(s):
    factorial = [1] * (len(s) + 1)
    for i in range(1, len(s) + 1):
        factorial[i] = factorial[i - 1] * i % MOD
    answer = 1
    for word in s.split(" "):
        counts = [0] * 26
        for ch in word:
            counts[ord(ch) - 97] += 1
        answer = answer * factorial[len(word)] % MOD
        for c in counts:
            answer = answer * pow(factorial[c], MOD - 2, MOD) % MOD
    return answer


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def sentence(words, most, letters):
    out = []
    for w in range(words):
        length = next_random() % most + 1
        out.append("".join(chr(97 + next_random() % letters) for _ in range(length)))
    return " ".join(out)


def main():
    global seed
    cases = ["too hot", "aa", "a", "abc", "aab bba", "abcdefghijklmnopqrstuvwxyz", "zz zz zz y"]
    for s in cases:
        print(f"\"{s}\" -> {count_anagrams(s)}")
    seed = 2514
    for most, letters in [(8, 3), (30, 26)]:
        total = 0
        check = 0
        for _ in range(2000):
            words = next_random() % (6 if letters == 3 else 20) + 1
            a = count_anagrams(sentence(words, most, letters))
            total = (total + a) % MOD
            check = (check * 31 + a) % MOD
        print(f"2000 random of words to {most} letters from {letters}: total {total}, checksum {check}")
    long = "".join(chr(97 + next_random() % 26) for _ in range(100000))
    print(f"one random word of 10^5: {count_anagrams(long)}")
    print(f"10^5 a's: {count_anagrams('a' * 100000)}")
    print(f"20000 words of four: {count_anagrams(sentence(20000, 4, 26))}")
    mixed = ""
    parts = []
    size = 0
    while size < 99000:
        if size > 0:
            size += 1
        length = next_random() % 999 + 1
        parts.append("".join(chr(97 + next_random() % 26) for _ in range(length)))
        size += length
    mixed = " ".join(parts)
    print(f"{len(mixed)} characters of long words: {count_anagrams(mixed)}")


main()
