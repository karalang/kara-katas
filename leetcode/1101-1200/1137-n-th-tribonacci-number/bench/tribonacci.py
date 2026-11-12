# LeetCode #1137: N-th Tribonacci Number -- the bench, the ★ arm's algorithm:
# three running values.


def tribonacci(n):
    a, b, c = 0, 1, 1
    for _ in range(n):
        a, b, c = b, c, a + b + c
    return a


seed = 1137


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    total = 0
    check = 0
    for _ in range(20000000):
        n = next_random() % 38
        t = tribonacci(n)
        total += t
        check = (check * 31 + t % 1000003) % 1000000007
    print(f"20000000 queries, n from 0 to 37: answers total {total}, checksum {check}")


main()
