# LeetCode #957: Prison Cells After N Days -- Python mirror of the Kara
# bench program (a day per state seen).


def next_day(cells):
    out = [0] * 8
    for i in range(1, 7):
        if cells[i - 1] == cells[i + 1]:
            out[i] = 1
    return out


def code(cells):
    c = 0
    for v in cells:
        c = c * 2 + v
    return c


def prison_after_n_days(cells, n):
    seen = {}
    row = cells
    day = 0
    left = n
    while left > 0:
        if code(row) in seen:
            left = left % (day - seen[code(row)])
            seen.clear()
            if left == 0:
                break
        seen[code(row)] = day
        row = next_day(row)
        day += 1
        left -= 1
    return row


def main():
    rounds = 2000
    rows = [[(b >> (7 - i)) & 1 for i in range(8)] for b in range(256)]
    total = 0
    check = 0
    for r in range(rounds):
        for b in range(256):
            c = code(prison_after_n_days(list(rows[b]), 1000000000 - r))
            total += c
            check = (check * 31 + c) % 1000000007
    print(f"{rounds} rounds over all 256 rows: rows adding to {total}, checksum {check}")


main()
