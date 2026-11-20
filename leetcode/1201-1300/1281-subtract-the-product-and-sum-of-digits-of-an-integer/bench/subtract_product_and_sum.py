# LeetCode #1281 bench, in Python: the ★ arm (the digits by remainders) on
# every n from 1 to 10^5, 2000 rounds, every answer folded into a checksum.


def subtract_product_and_sum(n):
    product = 1
    total = 0
    rest = n
    while rest > 0:
        digit = rest % 10
        product *= digit
        total += digit
        rest //= 10
    return product - total


def main():
    check = 0
    for rnd in range(2000):
        for n in range(1, 100001):
            check = (check * 131 + subtract_product_and_sum(n) + rnd + 1000) % 1000000007
    print(f"2000 rounds of 1 to 100000: checksum {check}")


main()
