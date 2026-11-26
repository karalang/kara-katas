# LeetCode #1486: XOR Operation in an Array -- the Python mirror of
# xor_operation.kara: each number made in turn, start + 2 * i, and folded
# into the XOR as it comes


def xor_operation(n, start):
    x = 0
    for i in range(n):
        x ^= start + 2 * i
    return x


seed = 1486


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{xor_operation(5, 0)} {xor_operation(4, 3)} {xor_operation(1, 7)} {xor_operation(10, 5)}")
    edges = [(1, 0), (1, 1000), (1000, 0), (1000, 1000), (6, 7), (7, 6)]
    print(" ".join(str(xor_operation(a, b)) for a, b in edges))
    by_n = 0
    for n in range(1, 1001):
        by_n = (by_n * 31 + xor_operation(n, 999)) % 1000000007
    by_start = 0
    for start in range(0, 1001):
        by_start = (by_start * 31 + xor_operation(1000, start)) % 1000000007
    print(f"every n: checksum {by_n} | every start: checksum {by_start}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 1000
        start = next_random() % 1001
        check = (check * 31 + xor_operation(n, start)) % 1000000007
    print(f"3000 random pairs: checksum {check}")


main()
