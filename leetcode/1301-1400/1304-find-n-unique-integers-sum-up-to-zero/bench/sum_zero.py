# LeetCode #1304 bench in Python: the ★ arm (the pairs i and -i, and 0 when
# n is odd, appended to a fresh list), the same 10^6 calls.


def sum_zero(n):
    out = []
    for i in range(1, n // 2 + 1):
        out.append(i)
        out.append(-i)
    if n % 2 == 1:
        out.append(0)
    return out


def main():
    check = 0
    for call in range(1000000):
        n = 1 + check % 1000
        got = sum_zero(n)
        x = got[(check // 1000) % n]
        check = (check * 31 + x + 1000 + call) % 1000000007
    print(f"1000000 calls: checksum {check}")


main()
