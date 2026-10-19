# LeetCode 771 — Jewels and Stones: the ★ arm in Python, same output.


def num_jewels_in_stones(jewels, stones):
    kinds = set(jewels)
    return sum(1 for c in stones if c in kinds)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(jewels, stones):
    print(f'"{jewels}" "{stones}" -> {num_jewels_in_stones(jewels, stones)}')


def random_letters(n, kinds):
    out = []
    for _ in range(n):
        k = next_random() % kinds
        base = 97 if k % 2 == 0 else 65
        out.append(chr(base + k // 2))
    return "".join(out)


def main():
    global seed
    show("aA", "aAAbbbb")
    show("z", "ZZ")
    show("abc", "")
    show("", "abc")
    show("zZ", "zZzZzZ")
    show("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "theQuickBrownFoxJumps")
    show("aa", "a")
    seed = 771
    total = 0
    check = 0
    for _ in range(300):
        kinds = 1 + next_random() % 52
        jewels = random_letters(next_random() % 51, kinds)
        stones = random_letters(next_random() % 51, kinds)
        count = num_jewels_in_stones(jewels, stones)
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"300 random pairs: {total} jewels in all, checksum {check}")


main()
