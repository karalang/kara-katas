# LeetCode #879 bench: Python mirror of profitable_schemes.kara (the ★ arm,
# a knapsack over members and profit) on the same 600 cases.

def profitable_schemes(n, min_profit, group, profit):
    modulus = 1000000007
    ways = [[0] * (min_profit + 1) for _ in range(n + 1)]
    ways[0][0] = 1
    for g, gain in zip(group, profit):
        for m in range(n, g - 1, -1):
            for p in range(min_profit + 1):
                q = min(p + gain, min_profit)
                ways[m][q] = (ways[m][q] + ways[m - g][p]) % modulus
    total = 0
    for m in range(n + 1):
        total = (total + ways[m][min_profit]) % modulus
    return total


seed = 879


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    total = 0
    check = 0
    for k in range(600):
        n = 50 + next_random() % 51
        min_profit = 50 + next_random() % 51
        wide = k % 2 == 0
        group = []
        profit = []
        for _ in range(100):
            group.append(next_random() % (100 if wide else 10) + 1)
            profit.append(next_random() % (101 if wide else 11))
        answer = profitable_schemes(n, min_profit, group, profit)
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"600 cases of 100 crimes: counts sum to {total}, checksum {check}")


main()
