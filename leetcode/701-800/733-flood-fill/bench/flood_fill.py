# LeetCode #733: Flood Fill -- depth first, with a stack of places.
# Benchmark mirror of the Kara star arm: push the start; pop a place,
# and if it still has the old color, paint it and push its four
# neighbours.


def flood_fill(img, sr, sc, color):
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [733]
    size = 1000
    img = []
    for _ in range(size):
        img.append([1 if next_random(seed) % 3 == 0 else 0 for _ in range(size)])
    total = 0
    for _ in range(40):
        r = (next_random(seed) * 32768 + next_random(seed)) % size
        c = (next_random(seed) * 32768 + next_random(seed)) % size
        old = img[r][c]
        img = flood_fill(img, r, c, 2)
        total += sum(1 for v in img[r] if v == 2)
        img = flood_fill(img, r, c, old)
    zeros = sum(1 for row in img for v in row if v == 0)
    print(f"40 rounds on a 1000 x 1000 image: {total} painted in their rows, {zeros} 0s after")


main()
