# LeetCode #1317 bench, Python mirror of the Kāra bench: the ★ arm (the
# first number tried from 1 up, each pair's digits read off by `% 10` and
# `// 10`, until neither has a 0) on every n from 2 to 10^4; 300 passes,
# each starting its walk through the range at a place chosen by the
# checksum so far and folding both numbers of every answer into it.


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
    check = 0
    for p in range(300):
        start = check % 9999
        for k in range(9999):
            n = 2 + (start + k) % 9999
            v = get_no_zero_integers(n)
            check = (check * 31 + v[0] * 7 + v[1] + p) % 1000000007
    print(f"300 passes over every n from 2 to 10^4: checksum {check}")


main()
