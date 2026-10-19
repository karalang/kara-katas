# LeetCode 806 -- Number of Lines To Write String: mirrors the harness
# of number_of_lines.kara with the ★ arm's one pass.
seed = 806
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def number_of_lines(widths, s):
    lines, width = 1, 0
    for ch in s:
        w = widths[ord(ch) - 97]
        if width + w > 100:
            lines += 1
            width = w
        else:
            width += w
    return lines, width


def show(widths, s):
    lines, width = number_of_lines(widths, s)
    print(f'"{s}" -> [{lines}, {width}]')


def main():
    show([10] * 26, LETTERS)
    second = [10] * 26
    second[0] = 4
    show(second, "bbbcccdddaaa")
    show([10] * 26, "a")
    show([10] * 26, "abcdefghij")
    show([10] * 26, "abcdefghijk")
    show([2] * 26, "z" * 50)
    odd = [2] * 26
    odd[25] = 9
    odd[24] = 10
    show(odd, "zy" * 10)
    total_lines = 0
    check = 0
    for i in range(300):
        widths = [2 + next_random() % 9 for _ in range(26)]
        length = 1 + next_random() % 200
        s = "".join(LETTERS[next_random() % 26] for _ in range(length))
        lines, width = number_of_lines(widths, s)
        total_lines += lines
        check = (check * 131 + lines * 101 + width + i) % 1000000007
    print(f"300 random strings: {total_lines} lines in all, checksum {check}")


main()
