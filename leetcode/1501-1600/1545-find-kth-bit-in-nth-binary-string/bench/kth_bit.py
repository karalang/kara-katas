# LeetCode #1545: Find Kth Bit in Nth Binary String -- bench: the ★ arm (the
# definition's recursion) asked for every place of S_20, two passes. Python
# mirror of kth_bit.kara.


def find_kth_bit(n, k):
    if n == 1:
        return "0"
    middle = 1 << (n - 1)
    if k == middle:
        return "1"
    if k < middle:
        return find_kth_bit(n - 1, k)
    return "1" if find_kth_bit(n - 1, (1 << n) - k) == "0" else "0"


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    check = 0
    ones = 0
    for _ in range(2):
        for k in range(1, 1048576):
            bit = 1 if find_kth_bit(20, k) == "1" else 0
            ones += bit
            check = mix(check, bit)
    print(f"2 passes over every place of S_20: {ones} ones, checksum {check}")


main()
