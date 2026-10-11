# LeetCode #375: Guess Number Higher or Lower II -- mirror of money_amount.kara.


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
    print(f"example 1: {get_money_amount(10)}")
    print(f"example 2: {get_money_amount(1)}")
    print(f"example 3: {get_money_amount(2)}")
    first = [get_money_amount(n) for n in range(1, 21)]
    print(f"n = 1 to 20: {first}")
    print(f"n = 100: {get_money_amount(100)}")
    print(f"n = 200, the largest: {get_money_amount(200)}")
    checksum = 0
    for n in range(1, 61):
        checksum = (checksum * 1009 + get_money_amount(n)) % 1000000007
    print(f"n = 1 to 60: checksum {checksum}")


main()
