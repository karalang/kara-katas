# LeetCode #1551: Minimum Operations to Make Array Equal -- the Python
# mirror of min_operations.kara, the ★ arm: how far the lower half sits
# below the mean n. Prints byte-identical output.


def min_operations(n):
    operations = 0
    for i in range(n // 2):
        operations += n - (2 * i + 1)
    return operations


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    for n in [3, 6, 1, 2, 4, 5, 9999, 10000]:
        print(f"n = {n} -> {min_operations(n)}")
    check = 0
    total = 0
    for n in range(1, 10001):
        answer = min_operations(n)
        total += answer
        check = mix(check, answer)
    print(f"n from 1 to 10000: total {total}, checksum {check}")


main()
