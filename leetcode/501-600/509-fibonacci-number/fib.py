# LeetCode #509: Fibonacci Number -- two running values. Mirrors
# fib.kara (the star arm) and its harness.


def fib(n):
    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ---- test harness ---------------------------------------------------------

seed = 509


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(f"n = 2: {fib(2)}")
    print(f"n = 3: {fib(3)}")
    print(f"n = 4: {fib(4)}")
    print(f"0 to 30: [{', '.join(str(fib(n)) for n in range(31))}]")
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        n = next_random() % 31
        f = fib(n)
        total += f
        checksum = (checksum * 31 + f) % 1000000007
    print(f"{count} random n: total {total}, checksum {checksum}")


main()
