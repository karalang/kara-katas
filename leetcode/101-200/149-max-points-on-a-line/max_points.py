"""LeetCode 149 — Max Points on a Line (Python mirror / oracle).

O(n^2): anchor each point, count points sharing an exact reduced-integer slope
`(dx/g, dy/g)` with a normalized sign (mirroring the Kāra version's Map[str,int]
of slope keys), add coincident duplicates. No floating point.
"""


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def max_points(pts):
    n = len(pts)
    if n <= 2:
        return n
    best = 1
    for i in range(n):
        slopes = {}
        dup = 0
        local = 0
        for j in range(i + 1, n):
            dx = pts[j][0] - pts[i][0]
            dy = pts[j][1] - pts[i][1]
            if dx == 0 and dy == 0:
                dup += 1
                continue
            g = gcd(abs(dx), abs(dy))
            dx //= g
            dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx = -dx
                dy = -dy
            key = f"{dx}/{dy}"
            c = slopes.get(key, 0)
            slopes[key] = c + 1
            if c + 1 > local:
                local = c + 1
        if local + dup + 1 > best:
            best = local + dup + 1
    return best


def run(pts):
    print(max_points(pts))


def main():
    run([[1, 1], [2, 2], [3, 3]])
    run([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]])
    run([[0, 0]])
    run([[0, 0], [1, 1]])
    run([[1, 1], [1, 1], [2, 2]])
    run([[1, 1], [1, 2], [1, 3], [2, 1]])


main()
