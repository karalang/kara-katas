# LeetCode #1560: Most Visited Sector in a Circular Track -- the Python
# mirror of sectors.kara, the ★ arm: the sectors from the first on to the
# last, wrapping past n. Prints byte-identical output.


def most_visited(n, rounds):
    start = rounds[0]
    end = rounds[-1]
    if start <= end:
        return list(range(start, end + 1))
    return list(range(1, end + 1)) + list(range(start, n + 1))


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, legs):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % (most - 1) + 2
        m = next_random() % legs + 1
        rounds = [next_random() % n + 1]
        for _ in range(m):
            at = rounds[-1]
            rounds.append((at - 1 + next_random() % (n - 1) + 1) % n + 1)
        sectors = most_visited(n, rounds)
        total += len(sectors)
        for s in sectors:
            check = mix(check, s)
        check = mix(check, -1)
    print(f"{count} tracks of up to {most} sectors and {legs} legs: {total} sectors, checksum {check}")


def main():
    global seed
    examples = [
        (4, [1, 3, 1, 2]),
        (2, [2, 1, 2, 1, 2, 1, 2, 1, 2]),
        (7, [1, 3, 5, 7]),
        (2, [1, 2]),
        (5, [3, 1]),
        (5, [5, 1]),
        (3, [2, 3, 1, 2]),
        (10, [7, 2, 9, 6]),
    ]
    for n, rounds in examples:
        print(f"n = {n}, rounds {rounds} -> {most_visited(n, rounds)}")
    seed = 1560
    batch(3000, 8, 8)
    batch(300, 100, 100)
    batch(30, 1000, 100)


main()
