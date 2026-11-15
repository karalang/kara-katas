# benchmark's Python mirror of subsequences.kara (LeetCode #2207, the ★
# arm): one pass counting the first letter so far, each second letter
# adding that count, then the more common letter added.


def maximum_subsequence_count(text, pattern):
    first, second = pattern[0], pattern[1]
    firsts = seconds = pairs = 0
    for ch in text:
        if ch == second:
            pairs += firsts
            seconds += 1
        if ch == first:
            firsts += 1
    return pairs + max(firsts, seconds)


seed = 2207


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    texts = [random_word(100000, [2, 3, 26][t % 3]) for t in range(12)]
    # each pass asks every text about its own pattern
    check = 0
    for p in range(50):
        for t in range(12):
            letters = [2, 3, 26][t % 3]
            pattern = chr(97 + p % letters) + chr(97 + (p * 7 + t) % letters)
            check = (check * 31 + maximum_subsequence_count(texts[t], pattern)) % 1000000007
    print(f"50 passes over 12 texts: checksum {check}")


main()
