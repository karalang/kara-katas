# LeetCode #2085: Count Common Words With One Occurrence -- Python mirror
# of the ★ arm's benchmark (common.kara): the same 2500 pairs of lists,
# the same count of both into a dict and walk of the first.

seed = 2085


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def counts(words):
    seen = {}
    for w in words:
        seen[w] = seen.get(w, 0) + 1
    return seen


def count_words(words1, words2):
    one = counts(words1)
    two = counts(words2)
    return sum(1 for w, c in one.items() if c == 1 and two.get(w) == 1)


def random_list(alphabet, letters):
    words = []
    for _ in range(1000):
        n = next_random() % 4 + 1
        words.append("".join(alphabet[next_random() % letters] for _ in range(n)))
    return words


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    total = check = 0
    for t in range(2500):
        letters = 2 + t % 25
        words1 = random_list(alphabet, letters)
        words2 = random_list(alphabet, letters)
        a = count_words(words1, words2)
        total += a
        check = (check * 31 + a) % 1000000007
    print(f"2500 pairs: sum {total}, checksum {check}")


main()
