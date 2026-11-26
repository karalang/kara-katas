# LeetCode #1414 bench, Python: the Fibonacci numbers up to k, and the
# largest that fits taken each time, workload and checksum as
# find_min_fibonacci_numbers.kara.


def find_min_fibonacci_numbers(k):
    fib = [1, 1]
    while fib[-1] <= k - fib[-2]:
        fib.append(fib[-1] + fib[-2])
    left = k
    count = 0
    for f in reversed(fib):
        if f <= left:
            left -= f
            count += 1
    return count


def main():
    seed = 1414
    check = 0
    for _ in range(3000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        k = 1 + seed % 1000000000
        check = (check * 131 + find_min_fibonacci_numbers(k)) % 1000000007
    print(f"3 * 10^6 values of k: checksum {check}")


main()
