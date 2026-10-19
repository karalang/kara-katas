# LeetCode 799 -- Champagne Tower: mirrors the harness of
# champagne_tower.kara with the ★ arm, one row at a time.
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


def show(poured, query_row, query_glass):
    got = champagne_tower(poured, query_row, query_glass)
    print(f"poured = {poured}, glass ({query_row}, {query_glass}) -> {got:.5f}")


def main():
    show(1, 1, 1)
    show(2, 1, 1)
    show(100000009, 33, 17)
    show(0, 0, 0)
    show(1, 0, 0)
    show(4, 2, 1)
    show(4, 2, 0)
    show(25, 6, 0)
    show(1000000000, 99, 0)
    show(1000000000, 99, 49)
    total = 0.0
    check = 0
    for i in range(300):
        if i % 2 == 0:
            poured = next_random() % 200
        else:
            hi = next_random()
            poured = (hi * 32768 + next_random()) % 1000000001
        query_row = next_random() % 100
        query_glass = next_random() % (query_row + 1)
        got = champagne_tower(poured, query_row, query_glass)
        total += got
        check = (check * 31 + int(got * 1000000.0)) % 1000000007
    print(f"300 random glasses: {total:.5f} cups in all, checksum {check}")


main()
