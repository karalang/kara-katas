# LeetCode 832 — Flipping an Image, two pointers in place.
#
# Mirrors flip_and_invert_image.kara: each row is flipped and inverted in
# one walk from both ends, the middle cell of an odd row only inverted;
# the harness below prints the same lines.


def flip_and_invert_image(image):
    img = image
    n = len(img)
    for r in range(n):
        i = 0
        j = n - 1
        while i < j:
            left = img[r][i]
            img[r][i] = 1 - img[r][j]
            img[r][j] = 1 - left
            i += 1
            j -= 1
        if i == j:
            img[r][i] = 1 - img[r][i]
    return img

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_image(n, ones):
    image = []
    for _ in range(n):
        row = []
        for _ in range(n):
            row.append(1 if next_random() % 100 < ones else 0)
        image.append(row)
    return image

def show(image):
    print(f"{image} -> {flip_and_invert_image([row[:] for row in image])}")

def fold(check, image):
    c = check
    for row in image:
        for x in row:
            c = (c * 3 + x) % 1000000007
    return c

def main():
    global seed
    show([[1, 1, 0], [1, 0, 1], [0, 0, 0]])
    show([[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]])
    show([[0]])
    show([[1]])
    show([[1, 0], [0, 1]])
    show([[1, 1], [1, 1]])
    show([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    seed = 832
    for ones in [50, 100, 0]:
        out = flip_and_invert_image(random_image(20, ones))
        count = sum(sum(row) for row in out)
        print(f"20 by 20 at {ones}% ones -> {count} ones, checksum {fold(0, out)}")
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 20
        ones = next_random() % 101
        out = flip_and_invert_image(random_image(n, ones))
        total += len(out)
        check = fold(check, out)
    print(f"300 random images: {total} rows, checksum {check}")

main()
