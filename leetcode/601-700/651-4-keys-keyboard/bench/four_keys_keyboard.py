# Benchmark for #651: the best for every count of presses, as the Kara
# ★ arm.


def max_a(n):
    best = [0] * (n + 1)
    for i in range(1, n + 1):
        best[i] = best[i - 1] + 1
        for j in range(1, i - 2):
            best[i] = max(best[i], best[j] * (i - j - 1))
    return best[n]


def main():
    calls = 200000
    total = 0
    checksum = 0
    for c in range(calls):
        a = max_a(1 + (c * 37) % 150)
        total = (total + a) % 1000000007
        checksum = (checksum * 31 + a % 1000000007) % 1000000007
    print(f"{calls} calls: total {total}, checksum {checksum}")


main()
