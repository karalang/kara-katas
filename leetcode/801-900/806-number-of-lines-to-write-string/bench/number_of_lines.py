# LeetCode 806 — Number of Lines To Write String: the bench.
#
# 64 strings of 1000 letters, LeetCode's longest, each with widths of
# its own from 2 to 10, are made once; each round counts the lines of
# the next one.
seed = 806


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def number_of_lines(widths, s):
    lines = 1
    width = 0
    for b in s.encode():
        w = widths[b - 97]
        if width + w > 100:
            lines += 1
            width = w
        else:
            width += w
    return lines, width


def main():
    letters = "abcdefghijklmnopqrstuvwxyz"
    all_widths = []
    strings = []
    for _ in range(64):
        all_widths.append([2 + next_random() % 9 for _ in range(26)])
        s = []
        for _ in range(1000):
            s.append(letters[next_random() % 26])
        strings.append("".join(s))
    rounds = 1000000
    total = 0
    check = 0
    for r in range(rounds):
        lines, width = number_of_lines(all_widths[r % 64], strings[r % 64])
        total += lines
        check = (check * 131 + lines * 1000 + width) % 1000000007
    print(f"{rounds} rounds of 1000 letters: {total} lines in all, checksum {check}")


main()
