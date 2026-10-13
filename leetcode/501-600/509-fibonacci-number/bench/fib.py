# Benchmark for #509: Python mirror of the ★ arm (two running values);
# see fib.kara.


def fib(n):
    a = 0
    b = 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main():
    # F(n) for n = 0, 1, ..., 30 over and over, 150,000,000 calls, the
    # results added up modulo 10^9 + 7.
    calls = 150000000
    total = 0
    for i in range(calls):
        total = (total + fib(i % 31)) % 1000000007
    print(f"{calls} calls: total {total}")


main()
