# LeetCode #1079: Letter Tile Possibilities -- the Python mirror of the
# ★ arm (tiles.kara): same algorithm, same harness, same output.


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
        counts[b - ord("A")] += 1
    return sequences(counts)


seed = 1079


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_tiles(n, k):
    return "".join(chr(ord("A") + next_random() % k) for _ in range(n))


def main():
    examples = ["AAB", "AAABBC", "V", "AB", "ABC", "AAAAAAA", "ABCDEFG", "AABBCCD", "ZZYYX", "QQQQQQZ"]
    for tiles in examples:
        print(f"{tiles} -> {num_tile_possibilities(tiles)}")
    total = check = 0
    for _ in range(300):
        n = next_random() % 7 + 1
        k = next_random() % 7 + 1
        count = num_tile_possibilities(random_tiles(n, k))
        total += count
        check = (check * 31 + count) % 1000000007
    print(f"300 random tile sets: {total} sequences in all, checksum {check}")
    sets = everything = 0
    for n in range(1, 5):
        for code in range(3 ** n):
            letters = []
            rest = code
            for _ in range(n):
                letters.append(rest % 3)
                rest //= 3
            if letters == sorted(letters):
                sets += 1
                everything += num_tile_possibilities("".join(chr(ord("A") + x) for x in letters))
    print(f"every multiset of 1 to 4 tiles over A to C: {sets} sets, {everything} sequences")


main()
