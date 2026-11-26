# LeetCode #1486: XOR Operation in an Array -- bench, the Python twin of
# xor_operation.kara.


def xor_operation(n, start):
    x = 0
    for i in range(n):
        x ^= start + 2 * i
    return x


def main():
    check = 0
    for q in range(2000000):
        n = 1 + (check + q) % 1000
        start = (check // 7 + q * 13) % 1001
        check = (check * 31 + xor_operation(n, start)) % 1000000007
    print(f"2000000 calls: checksum {check}")


main()
