# LeetCode 765 — Couples Holding Hands: the ★ arm in Python, same output.


def min_swaps_couples(row):
    row = list(row)
    seat_of = [0] * len(row)
    for i, person in enumerate(row):
        seat_of[person] = i
    swaps = 0
    for i in range(0, len(row), 2):
        partner = row[i] ^ 1
        if row[i + 1] != partner:
            j = seat_of[partner]
            moved = row[i + 1]
            row[j] = moved
            seat_of[moved] = j
            row[i + 1] = partner
            seat_of[partner] = i + 1
            swaps += 1
    return swaps


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(row):
    print(f"{row} -> {min_swaps_couples(row)}")


def main():
    global seed
    for row in [[0, 2, 1, 3], [3, 2, 0, 1], [0, 1], [1, 0], [0, 2, 4, 1, 3, 5],
                [5, 4, 2, 6, 3, 1, 0, 7], [0, 3, 2, 5, 4, 7, 6, 9, 8, 1]]:
        show(row)
    seed = 765
    total = 0
    check = 0
    for _ in range(300):
        couples = 1 + next_random() % 30
        row = list(range(2 * couples))
        for i in range(2 * couples):
            j = i + next_random() % (2 * couples - i)
            row[i], row[j] = row[j], row[i]
        swaps = min_swaps_couples(row)
        total += swaps
        check = (check * 31 + swaps) % 1000000007
    print(f"300 random rows: {total} swaps in all, checksum {check}")


main()
