# LeetCode #1551: Minimum Operations to Make Array Equal -- bench: the ★
# arm (the lower half's distance from the mean, added up place by place)
# for every n from 1 to 10000, in 100 passes. Python mirror of min_operations.kara.


def min_operations(n):
    operations = 0
    for i in range(n // 2):
        operations += n - (2 * i + 1)
    return operations


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    check = 0
    for p in range(100):
        for n in range(1, 10001):
            check = mix(check, min_operations(n) + p)
    print(f"100 passes over n from 1 to 10000: checksum {check}")


main()
