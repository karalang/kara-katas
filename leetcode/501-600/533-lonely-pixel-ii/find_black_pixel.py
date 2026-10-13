# LeetCode #533: Lonely Pixel II -- Python mirror of the ★ arm (count
# each kind of row); see find_black_pixel.kara. Same algorithm, same
# harness, same output.


def find_black_pixel(picture, target):
    n = len(picture[0])
    cols = [0] * n
    rows = {}
    for row in picture:
        key = ""
        blacks = 0
        for c in range(n):
            key += row[c]
            if row[c] == "B":
                cols[c] += 1
                blacks += 1
        if blacks == target:
            rows[key] = rows.get(key, 0) + 1
    lonely = 0
    for key, count in rows.items():
        if count != target:
            continue
        for c, ch in enumerate(key):
            if ch == "B" and cols[c] == target:
                lonely += target
    return lonely


# ---- test harness ---------------------------------------------------------

seed = 533


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_picture(n, target, planted, extra, percent):
    picture = []
    for _ in range(planted):
        cols = list(range(n))
        row = ["W"] * n
        for i in range(target):
            j = i + next_random() % (n - i)
            cols[i], cols[j] = cols[j], cols[i]
            row[cols[i]] = "B"
        copies = target + 1 if next_random() % 4 == 0 else target
        for _ in range(copies):
            picture.append(row[:])
    for _ in range(extra):
        picture.append(["B" if next_random() % 100 < percent else "W" for _ in range(n)])
    for i in range(len(picture) - 1, 0, -1):
        j = next_random() % (i + 1)
        picture[i], picture[j] = picture[j], picture[i]
    return picture


def show(name, rows, target):
    print(f"{name}: [{', '.join(rows)}], target = {target} -> {find_black_pixel([list(r) for r in rows], target)}")


def main():
    show("example 1", ["WBWBBW", "WBWBBW", "WBWBBW", "WWBWBW"], 3)
    show("example 2", ["WWB", "WWB", "WWB"], 1)
    show("one black", ["B"], 1)
    show("one white", ["W"], 1)
    show("rows differ", ["BB", "BW"], 1)
    show("two equal rows", ["BWB", "WWW", "BWB"], 2)
    show("count is right, rows are not", ["BBW", "BWB", "WBB"], 2)
    total = none = checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 20
        target = 1 + next_random() % min(n, 4)
        planted = next_random() % 4
        extra = 1 + next_random() % 10 if planted == 0 else next_random() % 11
        percent = next_random() % 21
        answer = find_black_pixel(random_picture(n, target, planted, extra, percent), target)
        total += answer
        if answer == 0:
            none += 1
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"300 random pictures: {total} lonely, {none} with none, checksum {checksum}")
    picture = random_picture(200, 5, 20, 80, 1)
    print(f"{len(picture)} by 200: target 5 -> {find_black_pixel(picture, 5)}, 4 -> {find_black_pixel(picture, 4)}")


main()
