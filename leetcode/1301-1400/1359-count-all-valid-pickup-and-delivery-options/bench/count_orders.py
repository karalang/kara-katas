# LeetCode #1359 -- bench, Python: the product of i (2i - 1) for i from 1
# to n, modulo 10^9 + 7.
MOD = 1000000007


def count_orders(n):
    count = 1
    for i in range(1, n + 1):
        count = count * i % MOD * (2 * i - 1) % MOD
    return count


def main():
    # 3 * 10^5 questions, each n from 1 to 500 drawn from the checksum so far,
    # every answer folded into it
    check = 0
    for r in range(300000):
        n = 1 + check % 500
        check = (check * 31 + count_orders(n) + r) % MOD
    print(f"300000 questions: checksum {check}")


main()
