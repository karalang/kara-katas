# LeetCode 765 — Couples Holding Hands: benchmark, the ★ arm in Python.
# 1,000,000 random rows of 60 seats.


def min_swaps_couples(row):
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


def main():
    seed = 765

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    rounds = 1000000
    total = 0
    check = 0
    for _ in range(rounds):
        row = list(range(60))
        for i in range(60):
            j = i + next_random() % (60 - i)
            row[i], row[j] = row[j], row[i]
        swaps = min_swaps_couples(row)
        total += swaps
        check = (check * 31 + swaps) % 1000000007
    print(f"{rounds} rows of 60 seats: {total} swaps in all, checksum {check}")


main()
