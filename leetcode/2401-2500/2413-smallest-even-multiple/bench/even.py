# LeetCode #2413: Smallest Even Multiple -- the bench, the ★ arm in
# Python: n when n is even, and 2 n when it is odd.


def smallest_even_multiple(n):
    return n if n % 2 == 0 else 2 * n


def main():
    check = 0
    for p in range(200000):
        for n in range(1, 151):
            check = (check * 31 + smallest_even_multiple(n) + p) % 1000000007
    print(f"200000 passes over n from 1 to 150: checksum {check}")


main()
