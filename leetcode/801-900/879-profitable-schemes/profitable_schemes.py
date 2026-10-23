# LeetCode #879: Profitable Schemes -- Python mirror of the ★ arm (a
# knapsack over members and profit) and its test harness; prints the same
# output as profitable_schemes.kara.


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


# ---- test harness ----------------------------------------------------------

seed = 879


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def text(values):
    parts = [str(v) for v in values]
    if len(parts) > 6:
        return f"[{parts[0]}, {parts[1]}, ... ({len(parts)} crimes)]"
    return "[" + ", ".join(parts) + "]"


def show(n, min_profit, group, profit):
    answer = profitable_schemes(n, min_profit, group, profit)
    print(f"n = {n}, minProfit = {min_profit}, group = {text(group)}, profit = {text(profit)} -> {answer}")


def main():
    show(5, 3, [2, 2], [2, 3])
    show(10, 5, [2, 3, 5], [6, 7, 8])
    show(1, 1, [2], [5])
    show(1, 0, [2], [5])
    show(4, 0, [1, 2, 1], [0, 0, 0])
    show(3, 10, [1, 1, 1], [3, 3, 3])
    ones = [1] * 100
    hundreds = [100] * 100
    show(100, 100, ones, ones)
    show(100, 0, ones, ones)
    show(100, 100, ones, hundreds)
    show(100, 100, hundreds, hundreds)
    total = 0
    for _ in range(3000):
        crimes = next_random() % 10 + 1
        n = next_random() % 12 + 1
        min_profit = next_random() % 15
        group = []
        profit = []
        for _ in range(crimes):
            group.append(next_random() % 5 + 1)
            profit.append(next_random() % 6)
        total = (total + profitable_schemes(n, min_profit, group, profit)) % 1000000007
    print(f"3000 cases of 1 to 10 crimes: counts sum to {total} (mod 10^9 + 7)")
    total = 0
    check = 0
    for k in range(8):
        n = 50 + next_random() % 51
        min_profit = 50 + next_random() % 51
        group = []
        profit = []
        for _ in range(100):
            group.append(next_random() % (100 if k % 2 == 0 else 10) + 1)
            profit.append(next_random() % (101 if k % 2 == 0 else 11))
        answer = profitable_schemes(n, min_profit, group, profit)
        total = (total + answer) % 1000000007
        check = (check * 131 + answer) % 1000000007
    print(f"8 cases of 100 crimes: counts sum to {total} (mod 10^9 + 7), checksum {check}")


main()
