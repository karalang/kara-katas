# LeetCode #893 bench: Python mirror of num_special_equiv_groups.kara (the
# union-find arm, every pair of words compared by their counts of letters
# at even and at odd positions) on the same 300 lists of 1000 words.


def num_special_equiv_groups(words):
    n = len(words)
    counts = []
    for word in words:
        count = [0] * 52
        for i, ch in enumerate(word):
            count[ord(ch) - 97 + 26 * (i % 2)] += 1
        counts.append(count)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(n):
        for j in range(i + 1, n):
            if counts[i] == counts[j]:
                a = find(i)
                b = find(j)
                if a != b:
                    parent[a] = b
    return sum(1 for i in range(n) if find(i) == i)


seed = 893


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def shuffled(word):
    b = list(word)
    n = len(b)
    for _ in range(n):
        i = next_random() % n
        j = next_random() % n
        if i % 2 == j % 2:
            b[i], b[j] = b[j], b[i]
    return "".join(b)


def main():
    groups = 0
    check = 0
    for _ in range(300):
        words = []
        for _ in range(1000):
            if len(words) > 0 and next_random() % 2 == 0:
                k = next_random() % len(words)
                words.append(shuffled(words[k]))
            else:
                words.append(random_word(20, 26))
        got = num_special_equiv_groups(words)
        groups += got
        check = (check * 131 + got) % 1000000007
    print(f"300 lists of 1000 words of 20 letters: {groups} groups, checksum {check}")


main()
