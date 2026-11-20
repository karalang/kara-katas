# LeetCode #1269 bench, in Python: the ★ arm (the ways to stand on each of
# the first `steps / 2 + 1` cells, a new row per step) on 1000 random cases
# of 1 to 500 steps in 1 to 400 cells or a million, drawn once, 20 rounds;
# every answer folded into a checksum.
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


cases = []
for c in range(1000):
    steps = next_random() % 500 + 1
    arr_len = 1000000 if c % 4 == 0 else next_random() % 400 + 1
    cases.append((steps, arr_len))
check = 0
for rnd in range(20):
    for steps, arr_len in cases:
        check = (check * 131 + num_ways(steps, arr_len) + rnd) % 1000000007
print(f"20 rounds of 1000 cases: checksum {check}")
