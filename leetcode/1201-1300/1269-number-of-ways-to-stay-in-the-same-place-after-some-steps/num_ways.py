# LeetCode #1269: Number of Ways to Stay in the Same Place After Some Steps
# -- Python mirror of the ★ arm (the ways to stand on each of the first
# `steps // 2 + 1` cells, a row per step), with the same harness.
MOD = 1000000007


def num_ways(steps, arr_len):
    width = min(arr_len, steps // 2 + 1)
    ways = [0] * width
    ways[0] = 1
    for _ in range(steps):
        nxt = [0] * width
        for i in range(width):
            w = ways[i]
            if i > 0:
                w += ways[i - 1]
            if i + 1 < width:
                w += ways[i + 1]
            nxt[i] = w % MOD
        ways = nxt
    return ways[0]


seed = 1269


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


print(f"{num_ways(3, 2)} {num_ways(2, 4)} {num_ways(4, 2)} {num_ways(27, 7)}")
check = 0
for case in range(2000):
    steps = next_random() % 100 + 1
    arr_len = 1000000 if case % 4 == 0 else next_random() % 60 + 1
    check = (check * 131 + num_ways(steps, arr_len)) % 1000000007
print(f"2000 random cases: checksum {check}")
print(f"{num_ways(500, 1000000)} {num_ways(500, 1)} {num_ways(500, 2)} {num_ways(500, 3)} {num_ways(430, 148488)}")
