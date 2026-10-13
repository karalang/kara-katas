# Benchmark for #531: Python mirror of the ★ arm (count each row and
# column); see find_lonely_pixel.kara.


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


def main():
    # 20 pictures of 500 by 500 made once, black with a chance of 1 to 20
    # in 1,000; then every picture is answered 200 times.
    seed = 531
    pictures = []
    for p in range(20):
        per_mille = 1 + p
        picture = []
        for _ in range(500):
            row = []
            for _ in range(500):
                seed = (seed * 1103515245 + 12345) % 2147483648
                row.append("B" if seed // 65536 % 1000 < per_mille else "W")
            picture.append(row)
        pictures.append(picture)
    total = checksum = 0
    for _ in range(200):
        for p in range(len(pictures)):
            answer = find_lonely_pixel(pictures[p])
            total += answer
            checksum = (checksum * 31 + answer) % 1000000007
    print(f"20 pictures of 500 by 500, 200 times each: total {total}, checksum {checksum}")


main()
