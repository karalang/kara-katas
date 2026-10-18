# LeetCode #733: Flood Fill -- mirror of the star arm.


def flood_fill(image, sr, sc, color):
    img = image
    old = img[sr][sc]
    if old == color:
        return img
    m, n = len(img), len(img[0])
    stack = [(sr, sc)]
    while stack:
        r, c = stack.pop()
        if r < 0 or r >= m or c < 0 or c >= n or img[r][c] != old:
            continue
        img[r][c] = color
        stack.append((r + 1, c))
        stack.append((r - 1, c))
        stack.append((r, c + 1))
        stack.append((r, c - 1))
    return img


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fmt(image):
    return "[" + ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in image) + "]"


def show(image, sr, sc, color):
    before = fmt(image)
    after = flood_fill(image, sr, sc, color)
    print(f"{before} from ({sr}, {sc}) to {color} -> {fmt(after)}")


def digest(what, image, sr, sc, color):
    before = [row[:] for row in image]
    after = flood_fill(image, sr, sc, color)
    changed = 0
    total = 0
    for r in range(len(after)):
        for c in range(len(after[r])):
            if after[r][c] != before[r][c]:
                changed += 1
            total = (total * 131 + after[r][c] + 1) % 1000000007
    print(f"{what} -> changed {changed}, checksum {total}")


def grid(m, n, v):
    return [[v] * n for _ in range(m)]


def main():
    global seed
    show([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2)
    show([[0, 0, 0], [0, 0, 0]], 0, 0, 0)
    show([[5]], 0, 0, 9)
    show([[1, 2, 1], [2, 1, 2], [1, 2, 1]], 1, 1, 3)
    show([[0, 0, 1, 0], [1, 0, 1, 0], [0, 0, 0, 0], [0, 1, 1, 1]], 3, 0, 4)
    show([[2, 2, 2, 2], [2, 3, 3, 2], [2, 3, 3, 2], [2, 2, 2, 2]], 1, 2, 2)
    seed = 733
    random = grid(50, 50, 0)
    for r in range(50):
        for c in range(50):
            random[r][c] = 1 if next_random() % 3 == 0 else 0
    random[25][25] = 0
    digest("50 x 50 random, two thirds 0s, from the middle", random, 25, 25, 2)
    snake = grid(50, 50, 0)
    for r in range(50):
        if r % 2 == 1:
            for c in range(50):
                snake[r][c] = 1
            if r % 4 == 1:
                snake[r][49] = 0
            else:
                snake[r][0] = 0
    digest("50 x 50 winding path, from a corner", snake, 0, 0, 5)
    digest("50 x 50 all one color", grid(50, 50, 7), 49, 49, 3)
    board = grid(50, 50, 0)
    for r in range(50):
        for c in range(50):
            board[r][c] = (r + c) % 2
    digest("50 x 50 checkerboard", board, 10, 20, 2)
    total = 0
    changed = 0
    for _ in range(300):
        m = 1 + next_random() % 8
        n = 1 + next_random() % 8
        kinds = 1 + next_random() % 3
        image = grid(m, n, 0)
        for r in range(m):
            for c in range(n):
                image[r][c] = next_random() % kinds
        sr = next_random() % m
        sc = next_random() % n
        color = next_random() % 4
        before = [row[:] for row in image]
        after = flood_fill(image, sr, sc, color)
        for r in range(m):
            for c in range(n):
                if after[r][c] != before[r][c]:
                    changed += 1
                total = (total * 131 + after[r][c] + 1) % 1000000007
    print(f"300 random images: changed {changed}, checksum {total}")


main()
