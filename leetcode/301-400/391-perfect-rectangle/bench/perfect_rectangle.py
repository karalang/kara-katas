# Benchmark for #391: mirror of perfect_rectangle.kara (corners and area).
import sys

sys.setrecursionlimit(100000)


def is_rectangle_cover(rects):
    min_x, min_y, max_x, max_y = rects[0]
    area = 0
    corners = set()
    for r in rects:
        min_x = min(min_x, r[0])
        min_y = min(min_y, r[1])
        max_x = max(max_x, r[2])
        max_y = max(max_y, r[3])
        area += (r[2] - r[0]) * (r[3] - r[1])
        for p in ((r[0], r[1]), (r[0], r[3]), (r[2], r[1]), (r[2], r[3])):
            if p in corners:
                corners.remove(p)
            else:
                corners.add(p)
    return (area == (max_x - min_x) * (max_y - min_y)
            and len(corners) == 4
            and (min_x, min_y) in corners
            and (min_x, max_y) in corners
            and (max_x, min_y) in corners
            and (max_x, max_y) in corners)


seed = 391


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def big():
    hi = step()
    return hi * 32768 + step()


def tile(x1, y1, x2, y2, pieces, out):
    w = x2 - x1
    h = y2 - y1
    if pieces <= 1 or (w < 2 and h < 2):
        out.append([x1, y1, x2, y2])
        return
    left = 1 + step() % (pieces - 1)
    across = False if w < 2 else True if h < 2 else step() % 2 == 0
    if across:
        cut = x1 + 1 + big() % (w - 1)
        tile(x1, y1, cut, y2, left, out)
        tile(cut, y1, x2, y2, pieces - left, out)
    else:
        cut = y1 + 1 + big() % (h - 1)
        tile(x1, y1, x2, cut, left, out)
        tile(x1, cut, x2, y2, pieces - left, out)


def main():
    tilings = []
    for _ in range(50):
        rects = []
        tile(0, 0, 100000, 100000, 20000, rects)
        tilings.append(rects)
    perfect = 0
    checksum = 0
    for rnd in range(300):
        t = rnd % 50
        at = big() % len(tilings[t])
        edit = step() % 3
        r = tilings[t][at]
        if edit == 1:
            r[0] += 1
            r[2] += 1
        elif edit == 2:
            r[3] += 1
        ok = is_rectangle_cover(tilings[t])
        if edit == 1:
            r[0] -= 1
            r[2] -= 1
        elif edit == 2:
            r[3] -= 1
        if ok:
            perfect += 1
        checksum = (checksum * 3 + (1 if ok else 2)) % 1000000007
    print(f"300 rounds over 50 tilings of 20000 pieces: {perfect} perfect, checksum {checksum}")


main()
