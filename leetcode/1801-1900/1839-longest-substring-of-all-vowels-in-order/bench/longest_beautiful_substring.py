# LeetCode #1839: Longest Substring Of All Vowels in Order -- the bench in Python: the ★ arm over
# 1000 calls on 40 words of 10^5 vowels, built once, each vowel the one
# before it again, the next vowel, an `a`, or any vowel, each call's word
# drawn from the checksum so far. The arm reads the word's bytes where they
# are, so no call copies one.


def longest_beautiful_substring(word):
    best = 0
    length = 1
    vowels = 1
    for i in range(1, len(word)):
        if word[i] < word[i - 1]:
            length = 1
            vowels = 1
        else:
            length += 1
            if word[i] > word[i - 1]:
                vowels += 1
        if vowels == 5:
            best = max(best, length)
    return best


def main():
    seed = 1839

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    words = []
    for _ in range(40):
        out = []
        at = 0
        for _ in range(100000):
            roll = next_random() % 10
            if roll < 4:
                pass
            elif roll < 8:
                at = min(at + 1, 4)
            elif roll < 9:
                at = 0
            else:
                at = next_random() % 5
            out.append("aeiou"[at])
        words.append("".join(out))
    check = 0
    for call in range(1000):
        w = words[(check + call) % 40]
        check = (check * 31 + longest_beautiful_substring(w)) % 1000000007
    print(f"1000 calls: checksum {check}")


main()
