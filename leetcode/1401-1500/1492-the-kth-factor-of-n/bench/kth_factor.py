# LeetCode #1492: The kth Factor of n -- the bench in Python, mirroring
# kth_factor.kara: every i from 1 to n tried in order.


def kth_factor(n, k):
    left = k
    for i in range(1, n + 1):
        if n % i == 0:
            left -= 1
            if left == 0:
                return i
    return -1


def main():
    check = 0
    for p in range(400):
        for n in range(1, 1001):
            k = 1 + (n + p + check) % 40
            check = (check * 31 + kth_factor(n, k) + 2) % 1000000007
    print(f"400 passes over n up to 1000: checksum {check}")


main()
