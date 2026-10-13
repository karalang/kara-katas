# LeetCode #522: Longest Uncommon Subsequence II -- mirror of the ★ arm
# (longest first); see find_lus_length.kara.


def is_subsequence(small, big):
    i = 0
    for c in big:
        if i < len(small) and small[i] == c:
            i += 1
    return i == len(small)


def find_lus_length(strs):
    order = sorted(range(len(strs)), key=lambda i: -len(strs[i]))
    for i in order:
        if all(j == i or not is_subsequence(strs[i], strs[j]) for j in range(len(strs))):
            return len(strs[i])
    return -1


seed = 522


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def show(strs):
    print(f"[{', '.join(strs)}]: {find_lus_length(strs)}")


def main():
    show(["aba", "cdc", "eae"])
    show(["aaa", "aaa", "aa"])
    show(["a", "b"])
    show(["a", "a"])
    show(["abc", "abc", "ab", "abcd"])
    show(["aabbcc", "aabbcc", "cb"])
    show(["aabbcc", "aabbcc", "c", "e", "aabbcd"])
    none = 0
    checksum = 0
    for _ in range(1000):
        letters = 1 + next_random() % 3
        n = 2 + next_random() % 49
        strs = []
        for k in range(n):
            if k > 0 and next_random() % 3 == 0:
                strs.append(strs[next_random() % k])
            else:
                strs.append(random_word(1 + next_random() % 10, letters))
        answer = find_lus_length(strs)
        if answer == -1:
            none += 1
        checksum = (checksum * 31 + answer + 1) % 1000000007
    print(f"1000 random lists: {none} with none, checksum {checksum}")


main()
