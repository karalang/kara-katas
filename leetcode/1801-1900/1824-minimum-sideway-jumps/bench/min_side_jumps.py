# LeetCode #1824: Minimum Sideway Jumps -- the bench in Python: the ★ arm
# over 50 calls on roads of 250000 to 499999 steps cut from one road of
# 5 * 10^5 steps with an obstacle at half its points, built once, each
# road's length drawn from the checksum so far and its last point cleared.


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


base = [0] * 500001
for i in range(1, 500000):
    if next_random() % 2 == 0:
        base[i] = 1 + next_random() % 3
check = 0
for call in range(50):
    n = 250000 + (check + call) % 250000
    road = base[:n + 1]
    road[n] = 0
    check = (check * 31 + min_side_jumps(road)) % 1000000007
print(f"50 calls: checksum {check}")
