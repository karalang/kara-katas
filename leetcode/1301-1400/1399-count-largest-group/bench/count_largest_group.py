# LeetCode #1399 bench -- Python: each number's digit sum by peeling off
# its last digit, the groups' sizes in a list indexed by the sum, and the
# groups of the largest size counted.


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
    check = 0
    for r in range(6000):
        n = 1 + (check + r * 7919) % 10000
        check = (check * 131 + count_largest_group(n)) % 1000000007
    print(f"6000 rounds of n up to 10^4: checksum {check}")


main()
