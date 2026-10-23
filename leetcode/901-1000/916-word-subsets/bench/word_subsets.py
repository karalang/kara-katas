# LeetCode #916: Word Subsets -- bench: Python mirror of every word of
# words2 folded into one need in word_subsets.kara.


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
        all_ = True
        for c in range(26):
            if count[c] < need[c]:
                all_ = False
        if all_:
            universal.append(a)
    return universal


seed = 916


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def main():
    rounds = 200
    n = 50000
    words1 = [random_word(10, 8) for _ in range(n)]
    total = 0
    check = 0
    for _ in range(rounds):
        words2 = []
        for _ in range(3):
            length = 1 + next_random() % 3
            words2.append(random_word(length, 8))
        universal = word_subsets(words1, words2)
        total += len(universal)
        for w in universal:
            for b in w.encode():
                check = (check * 31 + b) % 1000000007
    print(f"{rounds} rounds over {n} words: {total} universal, checksum {check}")


main()
