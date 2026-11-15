# LeetCode #1580: Put Boxes Into the Warehouse II -- the Python mirror of
# the ★ arm: each room's usable height is the larger of its prefix and
# suffix minimum; the rooms and boxes sorted and matched smallest first.
# O(n log n + m log m)


def max_boxes_in_warehouse(boxes, warehouse):
    m = len(warehouse)
    from_left = list(warehouse)
    for i in range(1, m):
        from_left[i] = min(from_left[i], from_left[i - 1])
    usable = list(warehouse)
    for i in range(m - 2, -1, -1):
        usable[i] = min(usable[i], usable[i + 1])
    for i in range(m):
        usable[i] = max(usable[i], from_left[i])
    usable.sort()
    sorted_boxes = sorted(boxes)
    placed = 0
    for room in usable:
        if placed < len(sorted_boxes) and sorted_boxes[placed] <= room:
            placed += 1
    return placed


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        m = (next_random() * 32768 + next_random()) % most + 1
        boxes = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(n)]
        warehouse = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(m)]
        placed = max_boxes_in_warehouse(boxes, warehouse)
        total += placed
        check = mix(check, placed)
    print(f"{count} problems of up to {most} boxes and rooms: boxes placed {total}, checksum {check}")


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    global seed
    examples = [
        ([1, 2, 2, 3, 4], [3, 4, 1, 2]),
        ([3, 5, 5, 2], [2, 1, 3, 4, 5]),
        ([1, 2, 3], [1, 2, 3, 4]),
        ([4, 5, 6], [3, 3, 3, 3, 3]),
        ([5], [1, 9, 1]),
        ([2, 2, 2, 2], [5, 1, 5]),
    ]
    for boxes, warehouse in examples:
        print(f"{show(boxes)} {show(warehouse)} -> {max_boxes_in_warehouse(boxes, warehouse)}")
    seed = 1580
    batch(3000, 6, 6)
    batch(300, 1000, 1000)
    batch(10, 100000, 1000000000)


main()
