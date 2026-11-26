# LeetCode #1492: The kth Factor of n -- the Python mirror of the ★ arm:
# every i from 1 to n tried in order, counting those that divide n.


def kth_factor(n, k):
    left = k
    for i in range(1, n + 1):
        if n % i == 0:
            left -= 1
            if left == 0:
                return i
    return -1


seed = 1492


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"{kth_factor(12, 3)} {kth_factor(7, 2)} {kth_factor(4, 4)}")
    print(f"{kth_factor(1, 1)} {kth_factor(1000, 16)} {kth_factor(1000, 17)} {kth_factor(997, 2)} {kth_factor(900, 14)} {kth_factor(720, 30)} {kth_factor(720, 31)}")
    check = 0
    found = 0
    for n in range(1, 201):
        for k in range(1, n + 1):
            f = kth_factor(n, k)
            if f > 0:
                found += 1
            check = (check * 31 + f + 2) % 1000000007
    print(f"n up to 200: {found} factors found, checksum {check}")
    check = 0
    for _ in range(20000):
        n = 1 + next_random() % 1000
        k = 1 + next_random() % min(n, 40)
        check = (check * 31 + kth_factor(n, k) + 2) % 1000000007
    print(f"20000 random pairs: checksum {check}")


main()
