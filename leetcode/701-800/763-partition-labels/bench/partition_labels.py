# LeetCode 763 — Partition Labels: benchmark, the ★ arm in Python.
# 100,000 random strings of 500 letters.


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


def main():
    seed = 763

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    rounds = 100000
    letters = "abcdefghijklmnopqrstuvwxyz"
    parts = 0
    check = 0
    for _ in range(rounds):
        width = 1 + next_random() % 4
        s = "".join(letters[min(i * 26 // 500 + next_random() % width, 25)] for i in range(500))
        sizes = partition_labels(s)
        parts += len(sizes)
        for size in sizes:
            check = (check * 31 + size) % 1000000007
    print(f"{rounds} strings of 500 letters: {parts} parts, checksum {check}")


main()
