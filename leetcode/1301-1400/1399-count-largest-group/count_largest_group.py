# LeetCode #1399: Count Largest Group -- Python mirror of the ★ arm: each
# number's digit sum by peeling off its last digit, the groups' sizes in
# a list indexed by the sum, and the groups of the largest size counted.


def digit_sum(x):
    rest = x
    total = 0
    while rest > 0:
        total += rest % 10
        rest //= 10
    return total


def count_largest_group(n):
    size = [0] * 37
    for x in range(1, n + 1):
        size[digit_sum(x)] += 1
    largest = max(size)
    return sum(1 for s in size if s == largest)


def main():
    print(" ".join(str(count_largest_group(n)) for n in [13, 2, 15, 24]))
    ends = [count_largest_group(n) for n in [10000, 9999, 1000, 999, 100, 99, 10, 9, 1]]
    print(f"ends: {' '.join(str(x) for x in ends)}")
    check = 0
    total = 0
    for n in range(1, 10001):
        got = count_largest_group(n)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"n = 1 to 10^4: {total} in all, checksum {check}")


main()
