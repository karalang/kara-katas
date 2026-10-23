# LeetCode #916: Word Subsets -- Python mirror of the folded need in
# word_subsets.kara, with the same test harness.


def counts(word):
    count = [0] * 26
    for b in word.encode():
        count[b - 97] += 1
    return count


def word_subsets(words1, words2):
    need = [0] * 26
    for b in words2:
        count = counts(b)
        for c in range(26):
            need[c] = max(need[c], count[c])
    universal = []
    for a in words1:
        count = counts(a)
        if all(count[c] >= need[c] for c in range(26)):
            universal.append(a)
    return universal


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def join(words):
    return ",".join(f'"{w}"' for w in words)


def show(words1, words2):
    print(f"words1 = [{join(words1)}], words2 = [{join(words2)}]: [{join(word_subsets(words1, words2))}]")


def random_word(longest, letters):
    n = 1 + next_random() % longest
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def random_words(count, longest, letters):
    seen = set()
    words = []
    while len(words) < count:
        w = random_word(longest, letters)
        if w not in seen:
            seen.add(w)
            words.append(w)
    return words


def fold(check, words):
    h = check
    for w in words:
        for b in w.encode():
            h = (h * 31 + b) % 1000000007
        h = (h * 31 + 7) % 1000000007
    return h


def main():
    global seed
    show(["amazon", "apple", "facebook", "google", "leetcode"], ["e", "o"])
    show(["amazon", "apple", "facebook", "google", "leetcode"], ["l", "e"])
    show(["amazon", "apple", "facebook", "google", "leetcode"], ["e", "oo"])
    show(["amazon", "apple", "facebook", "google", "leetcode"], ["lo", "eo"])
    show(["a", "b", "ab", "ba", "aab"], ["a", "a"])
    show(["a", "b", "ab", "ba", "aab"], ["aa"])
    show(["abc"], ["z"])
    seed = 916
    kept = 0
    check = 0
    for c in range(400):
        letters = 3 if c % 3 == 0 else 6 if c % 3 == 1 else 26
        n1 = 1 + next_random() % 300
        n2 = 1 + next_random() % 5
        words1 = random_words(n1, 10, letters)
        words2 = [random_word(4, letters) for _ in range(n2)]
        got = word_subsets(words1, words2)
        kept += len(got)
        check = fold(check, got)
    print(f"400 cases: {kept} universal words, checksum {check}")
    words1 = random_words(10000, 10, 26)
    words2 = [random_word(1, 26) for _ in range(10000)]
    wide = word_subsets(words1, words2)
    print(f"10000 words against every single letter: {len(wide)} universal")
    words1 = random_words(10000, 10, 4)
    words2 = [random_word(3, 2) for _ in range(10000)]
    narrow = word_subsets(words1, words2)
    print(f"10000 words of 4 letters against 10000 of 2: {len(narrow)} universal, checksum {fold(0, narrow)}")


main()
