# LeetCode #2742: Painting the Walls -- the bench (walls.kara in Python):
# a knapsack over the walls covered.


def paint_walls(cost, time):
    n = len(cost)
    far = (2**63 - 1) // 2
    least = [far] * (n + 1)
    least[0] = 0
    for i in range(n):
        for j in range(n, 0, -1):
            frm = max(j - time[i] - 1, 0)
            least[j] = min(least[j], least[frm] + cost[i])
    return least[n]


def main():
    count, n, rounds = 20, 500, 100
    seed = 2742
    cases = []
    for _ in range(count):
        cost = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            hi = seed // 65536
            seed = (seed * 1103515245 + 12345) % 2147483648
            lo = seed // 65536
            cost.append((hi * 32768 + lo) % 1000000 + 1)
        time = []
        for _ in range(n):
            seed = (seed * 1103515245 + 12345) % 2147483648
            time.append(seed // 65536 % 20 + 1)
        cases.append((cost, time))
    total = check = 0
    for r in range(rounds):
        for cost, time in cases:
            least = paint_walls(cost, time)
            total += least
            check = (check * 31 + least + r) % 1000000007
    print(f"{count} cases of {n} walls, {rounds} rounds: costs sum to {total}, checksum {check}")


main()
