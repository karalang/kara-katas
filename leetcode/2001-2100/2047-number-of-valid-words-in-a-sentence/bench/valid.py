# LeetCode #2047 -- the ★ arm as a benchmark; mirror of valid.kara.


def is_valid(token):
    n = len(token)
    hyphens = 0
    for i, c in enumerate(token):
        if c.isdigit():
            return False
        if c == "-":
            hyphens += 1
            if hyphens > 1 or i == 0 or i == n - 1:
                return False
            if not token[i - 1].islower() or not token[i + 1].islower():
                return False
        if c in "!.," and i != n - 1:
            return False
    return True


def count_valid_words(sentence):
    count = 0
    for token in sentence.split():
        if is_valid(token):
            count += 1
    return count


def main():
    symbols = "abcdefgh--!.,9"
    seed = 2047

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    sentences = []
    for _ in range(2000):
        s = []
        for _ in range(1000):
            r = next_random() % 100
            if r < 70:
                s.append(symbols[next_random() % 8])
            elif r < 85:
                s.append(" ")
            else:
                s.append(symbols[next_random() % len(symbols)])
        sentences.append("".join(s))
    calls = words = check = 0
    for r in range(100):
        for s in sentences:
            n = count_valid_words(s[r % 7:])
            calls += 1
            words += n
            check = (check * 31 + n) % 1000000007
    print(f"{calls} calls: {words} valid words, checksum {check}")


main()
