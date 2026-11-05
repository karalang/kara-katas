# LeetCode #1048: Longest String Chain -- Python mirror of longest_chain.kara.
#
# The same walk: the words shortest first, each one's chain one longer than
# the best chain ending at a word it becomes with one letter taken out.


def longest_str_chain(words):
    chain = {}
    best = 0
    for w in sorted(words, key=len):
        here = 1
        for i in range(len(w)):
            pred = w[:i] + w[i + 1:]
            if pred in chain:
                here = max(here, chain[pred] + 1)
        chain[w] = here
        best = max(best, here)
    return best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_words(count, longest, k):
    words = []
    for _ in range(count):
        n = next_random() % longest + 1
        words.append("".join(chr(ord("a") + next_random() % k) for _ in range(n)))
    return words


def show(words):
    return "[" + ",".join(f'"{w}"' for w in words) + "]"


def main():
    global seed
    examples = [
        ["a", "b", "ba", "bca", "bda", "bdca"],
        ["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"],
        ["abcd", "dbqca"],
        ["a"],
        ["a", "a", "aa"],
        ["ab", "ba", "a"],
        ["abc", "ac", "a", "c"],
        ["a", "ab", "abc", "abcd", "abcde", "x", "xy"],
        ["ksqvsyq", "ks", "kss", "czvh", "zczpzvdhx", "zczpzvh", "zczpzvhx", "zcpzvh", "zczvh", "gr", "grukmj", "ksqvsq", "gruj", "kssq", "ksqsq", "grukkmj", "grukj", "zczpzfvdhx", "gru"],
        ["b", "c", "d", "e"],
    ]
    for words in examples:
        print(f"{show(words)} -> {longest_str_chain(words)}")
    seed = 1048
    total = check = 0
    for _ in range(2000):
        count = next_random() % 12 + 1
        answer = longest_str_chain(random_words(count, 4, 2))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"2000 random lists of a, b: total {total}, checksum {check}")
    total = check = 0
    for _ in range(300):
        count = next_random() % 200 + 1
        answer = longest_str_chain(random_words(count, 8, 4))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"300 random lists of a to d: total {total}, checksum {check}")
    big = random_words(1000, 16, 3)
    print(f"1000 words of a, b, c -> {longest_str_chain(big)}")
    ladder = []
    w = ""
    for i in range(16):
        w += chr(ord("a") + i % 26)
        ladder.append(w)
    ladder.reverse()
    print(f"a ladder of 16 words, longest first -> {longest_str_chain(ladder)}")


main()
