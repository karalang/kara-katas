# LeetCode #1837: Sum of Digits in Base K -- the bench in Python: the ★ arm over
# 2 * 10^7 calls, each `n` from 1 to 100 and base from 2 to 10 drawn from the
# checksum so far.


def sum_base(n, k):
    left = n
    total = 0
    while left > 0:
        total += left % k
        left //= k
    return total


def main():
    check = 0
    for call in range(20000000):
        n = 1 + (check + call) % 100
        k = 2 + (check // 100 + call) % 9
        check = (check * 31 + sum_base(n, k)) % 1000000007
    print(f"20000000 calls: checksum {check}")


main()
