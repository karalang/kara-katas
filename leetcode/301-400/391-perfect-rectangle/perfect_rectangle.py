# LeetCode #391: Perfect Rectangle -- Python mirror of perfect_rectangle.kara.


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
        for p in [(r[0], r[1]), (r[0], r[3]), (r[2], r[1]), (r[2], r[3])]:
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


def tile(x1, y1, x2, y2, pieces, out):
    w = x2 - x1
    h = y2 - y1
    if pieces <= 1 or (w < 2 and h < 2):
        out.append([x1, y1, x2, y2])
        return
    left = 1 + step() % (pieces - 1)
    across = False if w < 2 else True if h < 2 else step() % 2 == 0
    if across:
        cut = x1 + 1 + step() % (w - 1)
        tile(x1, y1, cut, y2, left, out)
        tile(cut, y1, x2, y2, pieces - left, out)
    else:
        cut = y1 + 1 + step() % (h - 1)
        tile(x1, y1, x2, cut, left, out)
        tile(x1, cut, x2, y2, pieces - left, out)


def show(name, rects):
    print(f"{name}: {'true' if is_rectangle_cover(rects) else 'false'}")


def main():
    show("example 1", [[1, 1, 3, 3], [3, 1, 4, 2], [3, 2, 4, 4], [1, 3, 2, 4], [2, 3, 3, 4]])
    show("example 2", [[1, 1, 2, 3], [1, 3, 2, 4], [3, 1, 4, 2], [3, 2, 4, 4]])
    show("example 3", [[1, 1, 3, 3], [3, 1, 4, 2], [1, 3, 2, 4], [2, 2, 4, 4]])
    show("one rectangle", [[-5, -5, 7, 2]])
    show("the same rectangle twice", [[0, 0, 2, 2], [0, 0, 2, 2]])
    show("two pairs on top of each other", [[0, 0, 1, 1], [0, 0, 1, 1], [1, 1, 2, 2], [1, 1, 2, 2]])
    show("an overlap and a gap of the same area", [[0, 0, 2, 1], [1, 0, 3, 1], [0, 1, 2, 2]])
    show("a plus sign over four corners", [[0, 0, 1, 1], [2, 0, 3, 1], [0, 2, 1, 3], [2, 2, 3, 3], [1, 0, 2, 3], [0, 1, 3, 2]])
    show("a row of strips", [[0, 0, 1, 5], [1, 0, 2, 5], [2, 0, 3, 5], [3, 0, 4, 5]])
    covers = 0
    checksum = 0
    for _ in range(2000):
        x1 = step() % 21 - 10
        y1 = step() % 21 - 10
        w = 1 + step() % 12
        h = 1 + step() % 12
        pieces = 1 + step() % 10
        rects = []
        tile(x1, y1, x1 + w, y1 + h, pieces, rects)
        edit = step() % 5
        at = step() % len(rects)
        if edit == 1 and len(rects) > 1:
            rects.pop(at)
        elif edit == 2:
            rects.append(list(rects[at]))
        elif edit == 3:
            rects[at][0] += 1
            rects[at][2] += 1
        elif edit == 4:
            rects[at][3] += 1
        ok = is_rectangle_cover(rects)
        if ok:
            covers += 1
        checksum = (checksum * 3 + (1 if ok else 2)) % 1000000007
    print(f"2000 random cases: {covers} perfect, checksum {checksum}")


main()
