# LeetCode #2135: Count Words Obtained After Adding a Letter -- the mirror
# of words.kara: each word as the 26-bit set of its letters, and a target
# obtained when taking away one of its letters leaves a start word's set.


def letters(w):
    mask = 0
    for c in w:
        mask |= 1 << (ord(c) - 97)
    return mask


def word_count(start_words, target_words):
    starts = {letters(w) for w in start_words}
    count = 0
    for w in target_words:
        mask = letters(w)
        for c in w:
            if mask ^ (1 << (ord(c) - 97)) in starts:
                count += 1
                break
    return count


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def word(length, k, seed):
    letters_ = list("abcdefghijklmnopqrstuvwxyz"[:k])
    out = []
    for i in range(length):
        j = i + next_random(seed) % (k - i)
        letters_[i], letters_[j] = letters_[j], letters_[i]
        out.append(letters_[i])
    return "".join(out)


def show(start_words, target_words):
    print(f"[{', '.join(start_words)}] [{', '.join(target_words)}] -> {word_count(start_words, target_words)}")


def main():
    show(["ant", "act", "tack"], ["tack", "act", "acti"])
    show(["ab", "a"], ["abc", "abcd"])
    show(["a"], ["a"])
    show(["ab"], ["ba"])
    show(["ab"], ["bac"])
    show(["a"], ["ab", "ba", "ab"])
    seed = [2135]
    total = 0
    check = 0
    for rnd in range(2000):
        k = [3, 4, 6][rnd % 3]
        s = next_random(seed) % 6 + 1
        t = next_random(seed) % 6 + 1
        starts = []
        for _ in range(s):
            length = next_random(seed) % k + 1
            starts.append(word(length, k, seed))
        targets = []
        for _ in range(t):
            length = next_random(seed) % k + 1
            targets.append(word(length, k, seed))
        count = word_count(starts, targets)
        total += count
        check = (check * 31 + count + s * 7 + t) % 1000000007
    print(f"2000 pairs: {total} words in all, checksum {check}")
    for k in [10, 26]:
        longest = 8 if k == 10 else 26
        starts = []
        targets = []
        for _ in range(50000):
            length = next_random(seed) % longest + 1
            starts.append(word(length, k, seed))
        for _ in range(50000):
            length = next_random(seed) % longest + 1
            targets.append(word(length, k, seed))
        print(f"50000 words of the first {k} letters: {word_count(starts, targets)}")


main()
