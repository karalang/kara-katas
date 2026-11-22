# LeetCode #2781: Length of the Longest Valid Substring -- the bench in
# Python: the ★ arm over 10 words of 10^5 letters from a to e, each
# against 10^5 forbidden words of 8 to 10 letters, all drawn first, then
# each answered 5 times, every answer building its own set.


def longest_valid_substring(word, forbidden):
    banned = set(forbidden)
    n = len(word)
    start = 0
    best = 0
    for j in range(n):
        i = j
        while i >= start and i + 10 > j:
            if word[i:j + 1] in banned:
                start = i + 1
                break
            i -= 1
        best = max(best, j + 1 - start)
    return best


seed = 2781


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


def random_words(count, shortest, longest, letters):
    words = []
    for _ in range(count):
        n = shortest + next_random() % (longest - shortest + 1)
        words.append(random_word(n, letters))
    return words


def main():
    count = 10
    rounds = 5
    cases = []
    for _ in range(count):
        word = random_word(100000, 5)
        cases.append((word, random_words(100000, 8, 10, 5)))
    total = 0
    check = 0
    for r in range(rounds):
        for word, forbidden in cases:
            a = longest_valid_substring(word, forbidden)
            total += a
            check = (check * 31 + a + 1 + r) % 1000000007
    print(f"{count} words of 10^5, {rounds} rounds: lengths sum to {total}, checksum {check}")


main()
