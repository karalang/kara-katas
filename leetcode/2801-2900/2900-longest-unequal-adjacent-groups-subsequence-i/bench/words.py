# LeetCode #2900: Longest Unequal Adjacent Groups Subsequence I -- the
# bench's Python mirror (words.kara): the same draw, the first word of
# each run.


def get_longest_subsequence(words, groups):
    chosen = []
    for i in range(len(words)):
        if i == 0 or groups[i] != groups[i - 1]:
            chosen.append(words[i])
    return chosen


seed = 2900
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 10000, 20, 100
    cases = []
    for _ in range(count):
        words = [LETTERS[next_random() % 26] + LETTERS[i % 26] + LETTERS[i // 26] for i in range(n)]
        groups = []
        group = next_random() % 2
        while len(groups) < n:
            run = next_random() % 5 + 1
            for _ in range(run):
                if len(groups) < n:
                    groups.append(group)
            group = 1 - group
        cases.append((words, groups))
    total = 0
    check = 0
    for r in range(rounds):
        for words, groups in cases:
            chosen = get_longest_subsequence(words, groups)
            total += len(chosen)
            check = (check * 31 + len(chosen) + r) % 1000000007
            for word in chosen:
                check = (check * 31 + len(word)) % 1000000007
            check = (check * 31 + ord(chosen[-1][0])) % 1000000007
    print(f"{count} cases of {n}, {rounds} rounds: {total} words chosen, checksum {check}")


main()
