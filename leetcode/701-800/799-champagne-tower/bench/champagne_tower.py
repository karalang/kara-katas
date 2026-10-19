# LeetCode 799 -- Champagne Tower: the bench, in Python. Mirrors
# champagne_tower.kara: one row at a time.
seed = 799


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def champagne_tower(poured, query_row, query_glass):
    row = [float(poured)]
    for r in range(query_row):
        below = [0.0] * (r + 2)
        for c in range(r + 1):
            if row[c] > 1.0:
                half = (row[c] - 1.0) / 2.0
                below[c] += half
                below[c + 1] += half
        row = below
    got = row[query_glass]
    return 1.0 if got > 1.0 else got


def main():
    questions = []
    for _ in range(4096):
        hi = next_random()
        poured = (hi * 32768 + next_random()) % 1000000001
        row = 50 + next_random() % 50
        glass = next_random() % (row + 1)
        questions.append((poured, row, glass))
    rounds = 81920
    total = 0.0
    check = 0
    for r in range(rounds):
        poured, row, glass = questions[r % 4096]
        got = champagne_tower(poured, row, glass)
        total += got
        check = (check * 31 + int(got * 1000000.0)) % 1000000007
    print(f"{rounds} glasses: {total:.5f} cups in all, checksum {check}")


main()
