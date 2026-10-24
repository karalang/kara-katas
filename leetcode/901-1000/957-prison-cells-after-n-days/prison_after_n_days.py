# LeetCode #957: Prison Cells After N Days -- a day per state seen.
#
# There are only 2^8 rows of cells, so the days must repeat. Step day by
# day, writing each row's first day in a dict keyed by the row read as
# a number; the first row seen twice closes a cycle, and the days left
# shrink to their remainder modulo its length. O(2^8) steps whatever n.


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


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(cells):
    return "[" + ",".join(str(v) for v in cells) + "]"


def row_of(b):
    return [(b >> (7 - i)) & 1 for i in range(8)]


def main():
    cases = [
        ([0, 1, 0, 1, 1, 0, 0, 1], 7),
        ([1, 0, 0, 1, 0, 0, 1, 0], 1000000000),
        ([0, 1, 0, 1, 1, 0, 0, 1], 0),
        ([0, 1, 0, 1, 1, 0, 0, 1], 1),
        ([0, 0, 0, 0, 0, 0, 0, 0], 1),
        ([1, 1, 1, 1, 1, 1, 1, 1], 1000000000),
        ([1, 0, 1, 0, 1, 0, 1, 0], 14),
        ([1, 0, 1, 0, 1, 0, 1, 0], 15),
        ([0, 0, 1, 0, 0, 1, 0, 0], 999999999),
    ]
    for cells, n in cases:
        print(f"{show(cells)} after {n}: {show(prison_after_n_days(list(cells), n))}")
    seed = [957]
    total = 0
    check = 0
    for _ in range(300):
        cells = row_of(next_random(seed) % 256)
        n = next_random(seed) % 100
        b = code(prison_after_n_days(cells, n))
        total += b
        check = (check * 31 + b) % 1000000007
    print(f"300 random cases after 0 to 99 days: rows adding to {total}, checksum {check}")
    for n in [1000000000, 999999999, 999999986, 536870912]:
        total = 0
        check = 0
        for b in range(256):
            r = code(prison_after_n_days(row_of(b), n))
            total += r
            check = (check * 31 + r) % 1000000007
        print(f"all 256 rows after {n}: rows adding to {total}, checksum {check}")


main()
