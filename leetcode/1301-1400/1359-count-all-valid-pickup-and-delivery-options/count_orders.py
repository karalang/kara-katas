# LeetCode #1359 -- Python mirror of the ★ arm: the product of i (2i - 1)
# for i from 1 to n, modulo 10^9 + 7.
MOD = 1000000007


def count_orders(n):
    count = 1
    for i in range(1, n + 1):
        count = count * i % MOD * (2 * i - 1) % MOD
    return count


def main():
    print(" ".join(str(count_orders(n)) for n in [1, 2, 3, 4, 10, 500]))
    check = 0
    for n in range(1, 501):
        check = (check * 131 + count_orders(n)) % MOD
    print(f"n from 1 to 500: checksum {check}")


main()
