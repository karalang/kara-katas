# LeetCode #1170: Compare Strings by Frequency of the Smallest Character --
# the ★ arm's bench in Python: words counted by frequency, the counts summed
# from the top down, each query answered by one look-up.


def f(s):
    smallest = ord('z') + 1
    count = 0
    for b in s.encode():
        if b < smallest:
            smallest = b
            count = 1
        elif b == smallest:
            count += 1
    return count


def num_smaller_by_frequency(queries, words):
    above = [0] * 12
    for w in words:
        above[f(w)] += 1
    for k in range(10, -1, -1):
        above[k] += above[k + 1]
    return [above[f(q) + 1] for q in queries]


seed = 1170


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(letters):
    n = 1 + next_random() % 10
    return ''.join(chr(ord('a') + next_random() % letters) for _ in range(n))


def main():
    rounds = 300
    queries = []
    words = []
    for l in range(16):
        letters = [2, 3, 5, 26][l % 4]
        queries.append([random_word(letters) for _ in range(2000)])
        words.append([random_word(letters) for _ in range(2000)])
    total = 0
    check = 0
    for _ in range(rounds):
        for l in range(16):
            letters = [2, 3, 5, 26][l % 4]
            i = next_random() % 2000
            queries[l][i] = random_word(letters)
            j = next_random() % 2000
            words[l][j] = random_word(letters)
            for x in num_smaller_by_frequency(queries[l], words[l]):
                total += x
                check = (check * 131 + x + 1) % 1000000007
    print(f"{rounds} rounds over 16 lists of 2000 queries and 2000 words: total {total}, checksum {check}")


main()
