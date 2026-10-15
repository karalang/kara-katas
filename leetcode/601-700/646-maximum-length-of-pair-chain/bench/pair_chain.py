# LeetCode #646: Maximum Length of Pair Chain -- Python mirror of the
# Kāra bench.
#
# The ★ arm's greedy over the same inputs and rounds: the pairs sorted
# by right end into a new list, then every pair kept that starts after
# the last one kept ended.


def find_longest_chain(pairs):
    order = sorted(pairs, key=lambda p: p[1])
    count = 0
    end = 0
    for left, right in order:
        if count == 0 or left > end:
            count += 1
            end = right
    return count


seed = 646


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    inputs = 20
    rounds = 200
    all_inputs = []
    for _ in range(inputs):
        longest = 10 + next_random() % 991
        pairs = []
        for _ in range(10000):
            left = next_random() % 30000
            right = left + 1 + next_random() % longest
            pairs.append([left, right])
        all_inputs.append(pairs)
    total = 0
    checksum = 0
    for r in range(rounds):
        c = find_longest_chain(all_inputs[(r * 7) % inputs])
        total += c
        checksum = (checksum * 31 + c) % 1000000007
    print(f"{inputs} inputs, {rounds} rounds: total {total}, checksum {checksum}")


main()
