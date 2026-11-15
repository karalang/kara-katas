# LeetCode #2169: Count Operations to Obtain Zero -- the benchmark's Python
# mirror of operations.kara.


def count_operations(num1, num2):
    a, b = max(num1, num2), min(num1, num2)
    ops = 0
    while b > 0:
        ops += a // b
        a, b = b, a % b
    return ops


def main():
    total = 0
    check = 0
    for a in range(3001):
        for b in range(3001):
            ops = count_operations(a, b)
            total += ops
            check = (check * 31 + ops) % 1000000007
    print(f"9006001 solves: {total} in all, checksum {check}")


main()
