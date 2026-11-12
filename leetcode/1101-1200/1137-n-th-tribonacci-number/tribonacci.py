# LeetCode #1137: N-th Tribonacci Number -- the Python mirror of the ★ arm:
# three running values, each step replacing the oldest with the sum of all
# three.


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
    print(f"4 -> {tribonacci(4)}")
    print(f"25 -> {tribonacci(25)}")
    allv = [tribonacci(n) for n in range(38)]
    for start in [0, 8, 16, 24, 32]:
        print(f"{start}..: {' '.join(str(t) for t in allv[start:start + 8])}")
    total = 0
    check = 0
    for _ in range(2000):
        n = next_random() % 38
        t = tribonacci(n)
        total += t
        check = (check * 31 + t % 1000003) % 1000000007
    print(f"2000 random n: answers total {total}, checksum {check}")


main()
