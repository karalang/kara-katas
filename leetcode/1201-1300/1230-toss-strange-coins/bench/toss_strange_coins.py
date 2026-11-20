# LeetCode #1230 bench: the ★ arm in Python, over the same 200 sets of
# 1000 coins as the Kāra bench.


def probability_of_heads(prob, target):
    ways = [0.0] * (target + 1)
    ways[0] = 1.0
    for p in prob:
        for j in range(target, 0, -1):
            ways[j] = ways[j] * (1.0 - p) + ways[j - 1] * p
        ways[0] = ways[0] * (1.0 - p)
    return ways[target]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [1230]
    sets = []
    targets = []
    for _ in range(200):
        sets.append([(next_random(seed) % 1001) / 1000.0 for _ in range(1000)])
        targets.append(next_random(seed) % 1001)
    total = 0.0
    for s in range(200):
        total += probability_of_heads(sets[s], targets[s])
    print(f"200 sets of 1000 coins: total {total:.6f}")


main()
