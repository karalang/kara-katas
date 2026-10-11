# Benchmark for #375 -- mirror of money_amount.kara.


def get_money_amount(n):
    cost = [[0] * (n + 2) for _ in range(n + 2)]
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            best = None
            for k in range(i, j + 1):
                worse = max(cost[i][k - 1], cost[k + 1][j])
                best = k + worse if best is None else min(best, k + worse)
            cost[i][j] = best
    return cost[1][n]


def main():
    checksum = 0
    for n in range(1, 201):
        checksum = (checksum * 1009 + get_money_amount(n)) % 1000000007
    print(f"checksum {checksum}")


main()
