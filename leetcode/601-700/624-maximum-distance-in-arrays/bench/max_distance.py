# LeetCode #624: Maximum Distance in Arrays -- Python mirror of the Kāra
# bench.
#
# The ★ arm's one pass over the same inputs and rounds.


def max_distance(arrays):
    low = arrays[0][0]
    high = arrays[0][-1]
    best = 0
    for i in range(1, len(arrays)):
        first = arrays[i][0]
        last = arrays[i][-1]
        best = max(best, last - low, high - first)
        low = min(low, first)
        high = max(high, last)
    return best


seed = 624


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_arrays(count, spread):
    arrays = []
    for _ in range(count):
        values = []
        for _ in range(1 + next_random() % 9):
            values.append(next_random() % (2 * spread + 1) - spread)
        values.sort()
        arrays.append(values)
    return arrays


def main():
    inputs = 20
    rounds = 2000
    all_inputs = []
    for _ in range(inputs):
        spread = 1000 + next_random() % 9001
        all_inputs.append(random_arrays(20000, spread))
    total = 0
    checksum = 0
    for r in range(rounds):
        d = max_distance(all_inputs[(r * 7) % inputs])
        total += d
        checksum = (checksum * 31 + d) % 1000000007
    print(f"{inputs} inputs, {rounds} rounds: total {total}, checksum {checksum}")


main()
