# Python mirror of the ★ arm plus harness for kata 835.

def largest_overlap(img1, img2):
    n = len(img1)
    ones1 = []
    ones2 = []
    for r in range(n):
        for c in range(n):
            if img1[r][c] == 1:
                ones1.append((r, c))
            if img2[r][c] == 1:
                ones2.append((r, c))
    width = 2 * n - 1
    votes = [0] * (width * width)
    best = 0
    for r1, c1 in ones1:
        for r2, c2 in ones2:
            k = (r2 - r1 + n - 1) * width + (c2 - c1 + n - 1)
            votes[k] += 1
            if votes[k] > best:
                best = votes[k]
    return best

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_image(n, percent):
    img = []
    for _ in range(n):
        row = []
        for _ in range(n):
            row.append(1 if next_random() % 100 < percent else 0)
        img.append(row)
    return img

def fmt(img):
    return "[" + ", ".join("[" + ", ".join(map(str, row)) + "]" for row in img) + "]"

def show(img1, img2):
    print(f"img1 = {fmt(img1)}, img2 = {fmt(img2)} -> {largest_overlap(img1, img2)}")

def main():
    global seed
    show([[1, 1, 0], [0, 1, 0], [0, 1, 0]], [[0, 0, 0], [0, 1, 1], [0, 0, 1]])
    show([[1]], [[1]])
    show([[0]], [[0]])
    show([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    show([[1, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 1]])
    show([[0, 0, 0], [0, 0, 0], [0, 0, 1]], [[1, 0, 0], [0, 0, 0], [0, 0, 0]])
    show([[1, 0], [0, 1]], [[0, 1], [1, 0]])
    show([[1, 1], [1, 1]], [[0, 0], [0, 0]])
    show([[0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 0]], [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    show([[1, 0, 1], [0, 1, 0], [1, 0, 1]], [[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    seed = 835
    for percent in [50, 5, 95]:
        img1 = random_image(30, percent)
        img2 = random_image(30, percent)
        print(f"30 by 30 at {percent}% ones -> {largest_overlap(img1, img2)}")
    total = 0
    check = 0
    for _ in range(100):
        n = 1 + next_random() % 30
        percent = next_random() % 101
        img1 = random_image(n, percent)
        img2 = random_image(n, percent)
        x = largest_overlap(img1, img2)
        total += x
        check = (check * 1000003 + x) % 1000000007
    print(f"100 random pairs: overlaps total {total}, checksum {check}")

main()
