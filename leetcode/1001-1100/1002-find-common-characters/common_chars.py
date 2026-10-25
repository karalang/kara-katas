# LeetCode #1002: Find Common Characters -- the least count of each letter
#
# Mirrors common_chars.kara, the ★ arm, and its test harness; its output
# is byte-identical.


def common_chars(words):
    least = [1000] * 26
    for word in words:
        count = [0] * 26
        for c in word:
            count[ord(c) - ord('a')] += 1
        for i in range(26):
            least[i] = min(least[i], count[i])
    ans = []
    for i in range(26):
        for _ in range(least[i]):
            ans.append(chr(i + ord('a')))
    return ans


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_words(most, longest, letters, seed):
    count = 1 + next_random(seed) % most
    alphabet = 1 + next_random(seed) % letters
    words = []
    for _ in range(count):
        word = ""
        for _ in range(1 + next_random(seed) % longest):
            word += chr(97 + next_random(seed) % alphabet)
        words.append(word)
    return words


def quoted(xs):
    return "[" + ",".join(f'"{x}"' for x in xs) + "]"


def main():
    examples = [
        ["bella", "label", "roller"],
        ["cool", "lock", "cook"],
        ["a"],
        ["abc", "def"],
        ["aaaa", "aa", "aaa"],
        ["zyx", "xyz", "yzx"],
        ["abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba"],
        ["ab", "ba", "ab", "bab", "c"],
        ["mississippi", "missouri", "simple"],
        ["leetcode", "codeleet", "tecodele", "elee"],
    ]
    for words in examples:
        ans = sorted(common_chars(words))
        print(f"words = {quoted(words)} -> {quoted(ans)}")
    big = [
        ["a" * 100 for _ in range(100)],
        ["b" * 100 if i == 99 else "a" * 100 for i in range(100)],
        ["".join(chr(97 + (i + j) % 26) for j in range(100))
         for i in range(100)],
    ]
    for words in big:
        ans = sorted(common_chars(words))
        print(f'100 words of 100 letters -> {len(ans)} common letters '
              f'"{"".join(ans)}"')
    seed = [1002]
    for count, most, longest, letters in [(300, 3, 5, 3), (3000, 10, 20, 6),
                                          (300, 100, 100, 26)]:
        total = 0
        found = 0
        check = 0
        for _ in range(count):
            words = random_words(most, longest, letters, seed)
            total += len(words)
            ans = sorted(common_chars(words))
            found += len(ans)
            for s in ans:
                for c in s:
                    check = (check * 31 + ord(c)) % 1000000007
            check = (check * 31 + 1) % 1000000007
        print(f"{count} random lists of {total} words: {found} common "
              f"letters, checksum {check}")


main()
