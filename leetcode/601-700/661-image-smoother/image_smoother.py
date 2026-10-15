# LeetCode #661: Image Smoother -- each cell's 3x3 window.
# Mirrors the ★ arm (image_smoother.kara) and its test harness.


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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(img):
    out = image_smoother(img)
    rows = ",".join("[" + ",".join(map(str, row)) + "]" for row in out)
    print(f"{len(img)}x{len(img[0])} -> [{rows}]")


def random_image(m, n):
    return [[next_random() % 256 for _ in range(n)] for _ in range(m)]


def checksum(out):
    h = 0
    for row in out:
        for v in row:
            h = (h * 31 + v) % 1000000007
    return h


def main():
    global seed
    show([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    show([[100, 200, 100], [200, 50, 200], [100, 200, 100]])
    show([[7]])
    show([[0, 10, 20, 255]])
    show([[3], [4], [200]])
    show([[1, 2], [3, 5]])
    show([[255] * 4 for _ in range(3)])
    seed = 661
    s = 0
    for _ in range(200):
        m = 1 + next_random() % 12
        n = 1 + next_random() % 12
        s = (s * 7 + checksum(image_smoother(random_image(m, n)))) % 1000000007
    print(f"200 random images: checksum {s}")
    once = image_smoother(random_image(200, 200))
    print(f"200x200 random: checksum {checksum(once)}")
    print(f"smoothed twice: checksum {checksum(image_smoother(once))}")


main()
