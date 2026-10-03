# Benchmark workload for LeetCode #338 — Python mirror of counting_bits.kara.

TOP_N = 1000000
ROUNDS = 300
MODULUS = 1073741789


def count_bits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans


def main():
    sink = 0
    for r in range(ROUNDS):
        n = TOP_N - r
        ans = count_bits(n)
        picked = ans[n] * 10000 + ans[n // 3] * 100 + ans[(n * 7) // 11]
        sink = (sink * 1000003 + picked + len(ans)) % MODULUS
    print(sink)


main()
