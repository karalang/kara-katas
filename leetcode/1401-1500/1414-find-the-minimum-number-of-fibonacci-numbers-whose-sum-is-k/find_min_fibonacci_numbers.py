# LeetCode #1414, Python mirror of find_min_fibonacci_numbers.kara: the
# Fibonacci numbers up to k, and the largest that fits taken each time.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    f = find_min_fibonacci_numbers
    small = " ".join(str(f(k)) for k in range(1, 13))
    print(f"{f(7)} {f(10)} {f(19)} | {small}")
    print(f"k = 10^9: {f(1000000000)} {f(701408733)} {f(701408732)}")
    seed = 1414
    check = 0
    total = 0
    for i in range(2000):
        top = [1000, 1000000, 1000000000][i % 3]
        a = next_random()
        b = next_random()
        k = 1 + (a * 32768 + b) % top
        x = f(k)
        total += x
        check = (check * 131 + x) % 1000000007
    print(f"2000 random k: {total} in all, checksum {check}")


main()
