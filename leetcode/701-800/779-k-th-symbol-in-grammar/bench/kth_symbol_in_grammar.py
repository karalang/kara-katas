# Benchmark for #779: K-th Symbol in Grammar -- mirror of the ★ arm (the
# ones in k - 1), with the same workload as the Kāra program.


def kth_grammar(n, k):
    return bin(k - 1).count("1") % 2


def main():
    x = 779
    ones = 0
    for _ in range(200000000):
        k = 1 + x % 536870912
        answer = kth_grammar(30, k)
        ones += answer
        x = (x * 1103515245 + 12345 + answer) % 2147483648
    print(f"200000000 queries of row 30: {ones} ones, last state {x}")


main()
