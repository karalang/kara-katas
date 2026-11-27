# LeetCode #1824: Minimum Sideway Jumps -- the ★ arm in Python


def min_side_jumps(obstacles):
    never = len(obstacles) + 1
    jumps = [1, 0, 1]
    for i in range(1, len(obstacles)):
        if obstacles[i] > 0:
            jumps[obstacles[i] - 1] = never
        best = min(jumps) + 1
        for lane in range(3):
            if obstacles[i] != lane + 1:
                jumps[lane] = min(jumps[lane], best)
    return min(jumps)


seed = 1824


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


f = min_side_jumps
print(f([0, 1, 2, 3, 0]), f([0, 1, 1, 3, 3, 0]), f([0, 2, 1, 0, 3, 0]))
print(f([0, 0]), f([0, 2, 2, 2, 0]), f([0, 2, 1, 3, 2, 1, 3, 0]), f([0, 0, 0, 0]))
n = 500000
turns = [0] * (n + 1)
for i in range(1, n):
    turns[i] = 1 + i % 3
print(f"the most: {f(turns)} {f([0] * (n + 1))}")
check = 0
for _ in range(3000):
    n = 1 + next_random() % 20
    road = [0] * (n + 1)
    for i in range(1, n):
        if next_random() % 2 == 0:
            road[i] = 1 + next_random() % 3
    check = (check * 31 + f(road)) % 1000000007
print(f"3000 random roads: checksum {check}")
