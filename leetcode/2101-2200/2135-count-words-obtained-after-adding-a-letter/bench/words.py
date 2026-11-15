# LeetCode #2135: Count Words Obtained After Adding a Letter -- the
# benchmark, the same algorithm as words.kara.


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


def main():
    seed = [2135]
    starts = []
    targets = []
    for _ in range(4):
        s = []
        t = []
        for _ in range(50000):
            length = next_random(seed) % 6 + 1
            s.append(word(length, 12, seed))
        for _ in range(50000):
            length = next_random(seed) % 6 + 1
            t.append(word(length, 12, seed))
        starts.append(s)
        targets.append(t)
    total = 0
    check = 0
    for rnd in range(25):
        for p in range(4):
            hi = next_random(seed)
            a = (hi * 32768 + next_random(seed)) % 50000
            length = next_random(seed) % 6 + 1
            starts[p][a] = word(length, 12, seed)
            hi = next_random(seed)
            b = (hi * 32768 + next_random(seed)) % 50000
            length = next_random(seed) % 6 + 1
            targets[p][b] = word(length, 12, seed)
            count = word_count(starts[p], targets[p])
            total += count
            check = (check * 31 + count + rnd) % 1000000007
    print(f"100 solves: {total} words in all, checksum {check}")


main()
