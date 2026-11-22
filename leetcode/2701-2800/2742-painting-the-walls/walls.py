# LeetCode #2742: Painting the Walls -- Python mirror of walls.kara (the
# ★ arm): paying for wall i covers time[i] + 1 walls; a knapsack over
# the walls covered, capped at n.


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


seed = 2742


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(paint_walls([1, 2, 3, 2], [1, 2, 3, 2]))
    print(paint_walls([2, 3, 4, 2], [1, 1, 1, 1]))
    print(paint_walls([7], [3]))
    print(paint_walls([50, 60, 1, 70], [1, 1, 3, 1]))
    print(paint_walls(list(range(1, 11)), [1] * 10))
    total = check = 0
    for c in range(2020):
        if c < 2000:
            n, most_cost, most_time = next_random() % 10 + 1, 100, 10
        else:
            n, most_cost, most_time = 500, 1000000, 20
        cost = []
        for _ in range(n):
            hi = next_random()
            lo = next_random()
            cost.append((hi * 32768 + lo) % most_cost + 1)
        time = [next_random() % most_time + 1 for _ in range(n)]
        least = paint_walls(cost, time)
        total += least
        check = (check * 31 + least) % 1000000007
        if c == 1999:
            print(f"2000 small cases: costs sum to {total}, checksum {check}")
            total = check = 0
    print(f"20 cases of 500 walls: costs sum to {total}, checksum {check}")


main()
