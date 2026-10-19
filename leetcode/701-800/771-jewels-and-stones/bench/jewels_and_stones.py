# LeetCode 771 — Jewels and Stones: benchmark, the ★ arm in Python.
# 256 random pairs of 50 jewels and 50 stones, built once; ROUNDS rounds
# each count the next pair.

ROUNDS = 1000000


def num_jewels_in_stones(jewels, stones):
    kinds = set()
    for c in jewels:
        kinds.add(c)
    count = 0
    for c in stones:
        if c in kinds:
            count += 1
    return count


seed = 771


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_letters(n, kinds):
    out = []
    for _ in range(n):
        k = next_random() % kinds
        base = 97 if k % 2 == 0 else 65
        out.append(chr(base + k // 2))
    return "".join(out)


def main():
    jewels, stones = [], []
    for _ in range(256):
        jewels.append(random_letters(50, 52))
        stones.append(random_letters(50, 52))
    total = 0
    check = 0
    for r in range(ROUNDS):
        k = r % 256
        count = num_jewels_in_stones(jewels[k], stones[k])
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"{ROUNDS} rounds of 50 jewels and 50 stones: {total} jewels in all, checksum {check}")


main()
