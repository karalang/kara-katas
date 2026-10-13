# LeetCode #521: Longest Uncommon Subsequence I -- mirror of the ★ arm
# (the whole longer word); see find_lus_length.kara.


def find_lus_length(a, b):
    return -1 if a == b else max(len(a), len(b))


seed = 521


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def show(a, b):
    print(f'a = "{a}", b = "{b}": {find_lus_length(a, b)}')


def main():
    show("aba", "cdc")
    show("aaa", "bbb")
    show("aaa", "aaa")
    show("a", "a")
    show("a", "b")
    show("ab", "abc")
    show("abc", "ab")
    show("ab", "ba")
    show("abcd", "abc")
    none = 0
    checksum = 0
    for i in range(3000):
        letters = 1 + next_random() % 3
        a = random_word(1 + next_random() % 100, letters)
        kind = i % 3
        if kind == 0:
            b = a
        elif kind == 1:
            b = a + chr(97 + next_random() % letters)
        else:
            b = random_word(1 + next_random() % 100, letters)
        n = find_lus_length(a, b)
        if n == -1:
            none += 1
        checksum = (checksum * 31 + n + 1) % 1000000007
    print(f"3000 random pairs: {none} with none, checksum {checksum}")


main()
