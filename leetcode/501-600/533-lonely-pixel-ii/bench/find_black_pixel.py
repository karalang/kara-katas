# Benchmark for #533: Python mirror of the ★ arm (count each kind of
# row); see find_black_pixel.kara.


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


def main():
    # 20 pictures 200 wide made once, the p-th with 20 rows planted for a
    # target of 1 + p % 8 and 80 more black with a chance of 1%; then
    # each picture is answered for every target from 1 to 8, in 100
    # rounds.
    pictures = [random_picture(200, 1 + p % 8, 20, 80, 1) for p in range(20)]
    total = checksum = 0
    for _ in range(100):
        for p in range(len(pictures)):
            for target in range(1, 9):
                answer = find_black_pixel(pictures[p], target)
                total += answer
                checksum = (checksum * 31 + answer) % 1000000007
    print(f"20 pictures 200 wide, targets 1 to 8, 100 rounds: total {total}, checksum {checksum}")


main()
