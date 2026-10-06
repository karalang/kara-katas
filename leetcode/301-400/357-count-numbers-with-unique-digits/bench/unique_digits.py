# Benchmark for #357 -- same workload and algorithm as unique_digits.kara.
import sys

sys.setrecursionlimit(100)


def extend(length, n, base, used):
    if length == n:
        return 1
    count = 1
    for d in range(base):
        if length == 0 and d == 0:
            continue
        if used & (1 << d) == 0:
            count += extend(length + 1, n, base, used | (1 << d))
    return count


def main():
    checksum = 0
    for base in range(2, 12):
        count = extend(0, base, base, 0)
        checksum = (checksum * 31 + count) % 1000000007
    print(f"bases 2 to 11: checksum {checksum}")


main()
