# LeetCode #531: Lonely Pixel I -- Python mirror of the ★ arm (count each
# row and column); see find_lonely_pixel.kara. Same algorithm, same
# harness, same output.


def find_lonely_pixel(picture):
    m, n = len(picture), len(picture[0])
    rows = [0] * m
    cols = [0] * n
    for r in range(m):
        for c in range(n):
            if picture[r][c] == "B":
                rows[r] += 1
                cols[c] += 1
    lonely = 0
    for r in range(m):
        for c in range(n):
            if picture[r][c] == "B" and rows[r] == 1 and cols[c] == 1:
                lonely += 1
    return lonely


# ---- test harness ---------------------------------------------------------

seed = 531


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_picture(m, n, per_mille):
    return [["B" if next_random() % 1000 < per_mille else "W" for _ in range(n)] for _ in range(m)]


def show(name, rows):
    print(f"{name}: [{', '.join(rows)}] -> {find_lonely_pixel([list(r) for r in rows])}")


def main():
    show("example 1", ["WWB", "WBW", "BWW"])
    show("example 2", ["BBB", "BBW", "BBB"])
    show("one black", ["B"])
    show("one white", ["W"])
    show("two in a row", ["WBWB", "WWWW", "BWWW"])
    show("two in a column", ["BW", "WW", "BW", "WB"])
    show("all white", ["WWWW", "WWWW", "WWWW"])
    total = none = checksum = 0
    for _ in range(300):
        m = 1 + next_random() % 20
        n = 1 + next_random() % 20
        per_mille = 20 + next_random() % 281
        answer = find_lonely_pixel(random_picture(m, n, per_mille))
        total += answer
        if answer == 0:
            none += 1
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"300 random pictures: {total} lonely, {none} with none, checksum {checksum}")
    print(f"500 by 500: {find_lonely_pixel(random_picture(500, 500, 2))}")


main()
