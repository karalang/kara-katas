# Benchmark for #390: mirror of last_remaining.kara (follow the head).


def last_remaining(n):
    head, step, left, from_left = 1, 1, n, True
    while left > 1:
        if from_left or left % 2 == 1:
            head += step
        left //= 2
        step *= 2
        from_left = not from_left
    return head


def main():
    seed = 390
    total = 0
    checksum = 0
    for _ in range(10000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        hi = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        n = hi * 32768 + seed // 65536 + 1
        r = last_remaining(n)
        total += r
        checksum = (checksum * 31 + r) % 1000000007
    print(f"10000000 values of n, sum {total}, checksum {checksum}")


main()
