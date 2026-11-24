# LeetCode #1317: Convert Integer to the Sum of Two No-Zero Integers --
# Python mirror of the ★ Kāra arm: the first number tried from 1 up, each
# pair's digits read off by `% 10` and `// 10`, until neither number has a
# 0. The answer is the pair with the smallest first number.


def has_zero(x):
    while x > 0:
        if x % 10 == 0:
            return True
        x //= 10
    return False


def get_no_zero_integers(n):
    a = 1
    while has_zero(a) or has_zero(n - a):
        a += 1
    return [a, n - a]


def main():
    asks = [2, 11, 10, 100, 1010, 9999, 10000]
    print(" ".join(",".join(str(x) for x in get_no_zero_integers(n)) for n in asks))
    total = 0
    check = 0
    for n in range(2, 10001):
        v = get_no_zero_integers(n)
        total += v[0]
        check = (check * 31 + v[0] * 10007 + v[1]) % 1000000007
    print(f"every n from 2 to 10^4: first numbers total {total}, checksum {check}")


main()
