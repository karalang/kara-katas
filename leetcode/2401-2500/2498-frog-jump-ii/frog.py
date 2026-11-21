# LeetCode #2498: Frog Jump II -- Python mirror of the ★ arm (frog.kara):
# the first gap, then every span over one stone, the largest kept.


def max_jump(stones):
    cost = stones[1] - stones[0]
    for i in range(2, len(stones)):
        cost = max(cost, stones[i] - stones[i - 2])
    return cost


# ---- test harness -----------------------------------------------------------

seed = 2498


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def random_stones(n, top):
    stones = [0]
    for _ in range(1, n):
        stones.append(stones[-1] + wide() % top + 1)
    return stones


def main():
    cases = [
        [0, 2, 5, 6, 7],
        [0, 3, 9],
        [0, 1],
        [0, 1000000000],
        [0, 1, 2, 3, 4, 5],
        [0, 1, 100],
        [0, 99, 100],
        [0, 10, 11, 12, 30],
        [0, 1, 3, 6, 10, 15, 21],
    ]
    for stones in cases:
        print(f"{len(stones)} stones, last {stones[-1]} -> {max_jump(stones)}")
    for top in (10, 1000000):
        check = 0
        for _ in range(2000):
            n = next_random() % 49 + 2
            check = (check * 31 + max_jump(random_stones(n, top))) % 1000000007
        print(f"2000 random to {top}: checksum {check}")
    n = 100000
    steps = list(range(n))
    random = random_stones(n, 10000)
    spread = [i * 10000 + i % 7 for i in range(n)]
    for name, stones in [("steps", steps), ("random", random), ("spread", spread)]:
        print(f"10^5 {name}, last {stones[n - 1]} -> {max_jump(stones)}")


if __name__ == "__main__":
    main()
