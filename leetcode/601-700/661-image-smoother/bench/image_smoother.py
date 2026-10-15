# Benchmark for #661: each cell's 3x3 window, as the Kara ★ arm.


def image_smoother(img):
    m, n = len(img), len(img[0])
    out = []
    for i in range(m):
        row = []
        for j in range(n):
            total = 0
            count = 0
            for r in range(max(i - 1, 0), min(i + 2, m)):
                for c in range(max(j - 1, 0), min(j + 2, n)):
                    total += img[r][c]
                    count += 1
            row.append(total // count)
        out.append(row)
    return out


seed = 661


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    size, passes = 1000, 20
    img = [[next_random() % 256 for _ in range(size)] for _ in range(size)]
    for _ in range(passes):
        img = image_smoother(img)
    checksum = 0
    for row in img:
        for v in row:
            checksum = (checksum * 31 + v) % 1000000007
    print(f"{size}x{size}, {passes} passes: checksum {checksum}")


main()
