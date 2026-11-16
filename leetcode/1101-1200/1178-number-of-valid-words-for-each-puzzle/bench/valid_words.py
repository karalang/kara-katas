# LeetCode #1178: Number of Valid Words for Each Puzzle -- the ★ arm's
# bench in Python: each word's letter set counted in a dict, each puzzle's
# subsets of its other six letters walked with `sub = (sub - 1) & rest`.
# The same words, the same puzzles and the same 20 calls.


def find_num_of_valid_words(words, puzzles):
    count = {}
    for w in words:
        mask = 0
        for c in w:
            mask |= 1 << (c - 97)
        count[mask] = count.get(mask, 0) + 1
    answer = []
    for p in puzzles:
        first = 1 << (p[0] - 97)
        rest = 0
        for c in p[1:]:
            rest |= 1 << (c - 97)
        total = 0
        sub = rest
        while True:
            total += count.get(sub | first, 0)
            if sub == 0:
                break
            sub = (sub - 1) & rest
        answer.append(total)
    return answer


seed = 1178


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def distinct(m, k):
    letters = [97 + i for i in range(m)]
    for i in range(k):
        j = i + next_random() % (m - i)
        letters[i], letters[j] = letters[j], letters[i]
    return letters[:k]


def main():
    words = []
    for _ in range(100000):
        s = distinct(14, 1 + next_random() % 7)
        n = 4 + next_random() % 47
        words.append(bytes(s[next_random() % len(s)] for _ in range(n)))
    puzzles = [bytes(distinct(14, 7)) for _ in range(10000)]
    calls = 20
    check = 0
    for _ in range(calls):
        for a in find_num_of_valid_words(words, puzzles):
            check = (check * 131 + a + 1) % 1000000007
    print(f"{calls} calls: checksum {check}")


main()
