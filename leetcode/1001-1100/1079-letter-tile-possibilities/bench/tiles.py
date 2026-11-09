# LeetCode #1079 bench: the Python mirror of tiles.kara, the same walk
# over a list of 26 counts and the same workload.


def sequences(counts):
    total = 0
    for letter in range(26):
        if counts[letter] > 0:
            counts[letter] -= 1
            total += 1 + sequences(counts)
            counts[letter] += 1
    return total


def num_tile_possibilities(tiles):
    counts = [0] * 26
    for b in tiles.encode():
        counts[b - 65] += 1
    return sequences(counts)


seed = 1079


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 200
    sets = []
    for _ in range(200):
        d = next_random() % 7 + 1
        alphabet = []
        while len(alphabet) < d:
            c = 65 + next_random() % 26
            if c not in alphabet:
                alphabet.append(c)
        sets.append("".join(chr(alphabet[next_random() % d]) for _ in range(7)))
    n = len(sets)
    total = 0
    check = 0
    for r in range(rounds):
        for j in range(n):
            count = num_tile_possibilities(sets[(j * 7 + r) % n])
            total += count
            check = (check * 31 + count) % 1000000007
    print(f"{rounds} rounds of {n} sets of 7 tiles: {total} sequences, checksum {check}")


main()
