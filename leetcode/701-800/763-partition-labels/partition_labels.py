# LeetCode 763 — Partition Labels: the ★ arm in Python, same output.


def partition_labels(s):
    last = [0] * 26
    for i, c in enumerate(s):
        last[ord(c) - ord("a")] = i
    sizes = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[ord(c) - ord("a")])
        if i == end:
            sizes.append(end - start + 1)
            start = i + 1
    return sizes


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_letters(n, width):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return "".join(letters[min(i * 26 // n + next_random() % width, 25)] for i in range(n))


def show(s):
    print(f"{s} -> {partition_labels(s)}")


def main():
    global seed
    for s in ["ababcbacadefegdehijhklij", "eccbbbbdec", "a", "abc", "abca",
              "aabbcc", "abacbdcedfeg", "zyxwvutsrqponmlkjihgfedcbaz"]:
        show(s)
    seed = 763
    parts = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 500
        width = 1 + next_random() % 4
        sizes = partition_labels(random_letters(n, width))
        parts += len(sizes)
        for size in sizes:
            check = (check * 31 + size) % 1000000007
    print(f"300 random strings: {parts} parts, checksum {check}")


main()
