# LeetCode #2485: Find the Pivot Integer -- Python mirror of pivot.kara:
# by the square root.

import math


def pivot_integer(n):
    total = n * (n + 1) // 2
    x = int(round(math.sqrt(total)))
    return x if x * x == total else -1


seed = 2485


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for n in [8, 1, 4, 49, 288, 2, 9, 1000]:
        print(f"{n} -> {pivot_integer(n)}")
    found = []
    for n in range(1, 1001):
        x = pivot_integer(n)
        if x != -1:
            found.append(f"{n}:{x}")
    print(f"1 to 1000 -> {len(found)} with a pivot: {' '.join(found)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 1000
        check = (check * 31 + pivot_integer(n) + 2) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
