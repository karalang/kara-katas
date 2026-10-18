# LeetCode #692: Top K Frequent Words -- bench program, Python mirror of the select arm.

seed = 692


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def top_k_frequent(words, k):
    s = sorted(words)
    distinct = []
    counts = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        distinct.append(s[i])
        counts.append(j - i)
        i = j
    out = []
    for _ in range(k):
        pick = -1
        for d in range(len(distinct)):
            if counts[d] > 0 and (pick < 0 or counts[d] > counts[pick]):
                pick = d
        out.append(distinct[pick])
        counts[pick] = 0
    return out


def main():
    lists = []
    for _ in range(100):
        words = []
        for _ in range(500):
            n = 1 + next_random() % 4
            words.append("".join(chr(97 + next_random() % 6) for _ in range(n)))
        lists.append(words)
    rounds = 60
    checksum = 0
    answers = 0
    for _ in range(rounds):
        for words in lists:
            for w in top_k_frequent(words, 10):
                for b in w.encode():
                    checksum = (checksum * 31 + b) % 1000000007
                checksum = (checksum * 31 + 1) % 1000000007
                answers += 1
    print(f"{rounds} rounds of 100 lists of 500 words: {answers} words answered, checksum {checksum}")


main()
