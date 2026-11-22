# LeetCode #2900: Longest Unequal Adjacent Groups Subsequence I -- the
# Python mirror of the ★ arm (words.kara): the first word of each run of
# one group.


def get_longest_subsequence(words, groups):
    return [words[i] for i in range(len(words)) if i == 0 or groups[i] != groups[i - 1]]


seed = 2900
total = 0
check = 0
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw_words(n):
    words = []
    for i in range(n):
        word = LETTERS[next_random() % 26]
        rest = i
        while True:
            word += LETTERS[rest % 26]
            rest //= 26
            if rest == 0:
                break
        words.append(word)
    return words


def digest(chosen):
    global total, check
    total += len(chosen)
    check = (check * 31 + len(chosen)) % 1000000007
    for word in chosen:
        for b in word.encode():
            check = (check * 31 + b) % 1000000007
        check = (check * 31 + 1) % 1000000007


def main():
    global total, check
    one = get_longest_subsequence(["e", "a", "b"], [0, 0, 1])
    two = get_longest_subsequence(["a", "b", "c", "d"], [1, 0, 1, 1])
    print(f"{' '.join(one)} | {' '.join(two)}")
    words = draw_words(100)
    same = get_longest_subsequence(words, [0] * 100)
    turns = get_longest_subsequence(words, [i % 2 for i in range(100)])
    threes = get_longest_subsequence(words, [i // 3 % 2 for i in range(100)])
    print(f"{len(same)} {len(turns)} {len(threes)}: {threes[0]} {threes[33]}")
    total = 0
    check = 0
    for c in range(4000):
        small = c < 3000
        n = next_random() % 8 + 1 if small else 100
        words = draw_words(n)
        groups = []
        group = next_random() % 2
        while len(groups) < n:
            run = 1 if small else next_random() % 5 + 1
            for _ in range(run):
                if len(groups) < n:
                    groups.append(next_random() % 2 if small else group)
            group = 1 - group
        digest(get_longest_subsequence(words, groups))
        if c == 2999:
            print(f"3000 small cases: {total} words chosen, checksum {check}")
            total = 0
            check = 0
    print(f"1000 cases of 100: {total} words chosen, checksum {check}")


main()
