# LeetCode #2485: Find the Pivot Integer -- bench, Python mirror of
# pivot.kara.

import math


def pivot_integer(n):
    total = n * (n + 1) // 2
    x = int(round(math.sqrt(total)))
    return x if x * x == total else -1


def main():
    check = 0
    for p in range(24000):
        start = check % 1000
        for i in range(1000):
            n = 1 + (start + i) % 1000
            check = (check * 31 + pivot_integer(n) + 2 + p) % 1000000007
    print(f"24000 passes over every count from 1 to 1000: checksum {check}")


main()
