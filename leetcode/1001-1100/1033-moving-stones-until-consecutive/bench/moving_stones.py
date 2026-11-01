# LeetCode #1033: Moving Stones Until Consecutive -- bench
# Mirrors ./moving_stones.kara; see ../README.md § Benchmarks.


def num_moves_stones(a, b, c):
    s = sorted([a, b, c])
    x, y, z = s[0], s[1], s[2]
    if z - x == 2:
        fewest = 0
    elif y - x <= 2 or z - y <= 2:
        fewest = 1
    else:
        fewest = 2
    return [fewest, z - x - 2]


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    count = 1000000
    rounds = 40
    seed = [1033]
    cases = []
    while len(cases) < count:
        a = next_random(seed) % 100 + 1
        b = next_random(seed) % 100 + 1
        c = next_random(seed) % 100 + 1
        if a != b and b != c and a != c:
            cases.append((a, b, c))
    total = 0
    check = 0
    for _ in range(rounds):
        for a, b, c in cases:
            moves = num_moves_stones(a, b, c)
            total += moves[0] + moves[1]
            check = (check * 131 + moves[0] * 101 + moves[1]) % 1000000007
    print(f"{count} triples, {rounds} rounds: sum {total}, checksum {check}")


main()
