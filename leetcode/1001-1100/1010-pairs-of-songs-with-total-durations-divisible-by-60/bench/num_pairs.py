# LeetCode #1010 bench: the ★ arm (remainder counts in one pass) over 20
# playlists of 60,000 songs, drawn once; each of 250 rounds counts the
# pairs of every playlist, starting from a different one, and folds each
# count into a checksum.


def num_pairs(time):
    seen = [0] * 60
    pairs = 0
    for t in time:
        r = t % 60
        pairs += seen[(60 - r) % 60]
        seen[r] += 1
    return pairs


seed = 1010


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds = 20, 250
    playlists = [[1 + next_random() % 500 for _ in range(60000)] for _ in range(count)]
    check = 0
    for r in range(rounds):
        for k in range(count):
            check = (check * 31 + num_pairs(playlists[(r + k) % count])) % 1000000007
    print(f"{rounds} rounds over {count} playlists of 60000 songs: checksum {check}")


main()
