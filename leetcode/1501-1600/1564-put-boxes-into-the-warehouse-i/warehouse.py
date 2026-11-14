# LeetCode #1564: Put Boxes Into the Warehouse I -- the Python mirror of
# warehouse.kara, the ★ arm: each room's usable height the least up to it,
# the smallest boxes into the deepest rooms. Prints byte-identical output.


def max_boxes_in_warehouse(boxes, warehouse):
    usable = list(warehouse)
    for i in range(1, len(usable)):
        usable[i] = min(usable[i], usable[i - 1])
    ordered = sorted(boxes)
    placed = 0
    for room in reversed(usable):
        if placed < len(ordered) and ordered[placed] <= room:
            placed += 1
    return placed


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
        warehouse = [top - (next_random() * 32768 + next_random()) % ((top + 1) // 2) for _ in range(m)]
        placed = max_boxes_in_warehouse(boxes, warehouse)
        total += placed
        check = mix(check, placed)
    print(f"{count} problems of up to {most} boxes and rooms of up to {top}: {total} boxes, checksum {check}")


def main():
    global seed
    examples = [
        ([4, 3, 4, 1], [5, 3, 3, 4, 1]),
        ([1, 2, 2, 3, 4], [3, 4, 1, 2]),
        ([1, 2, 3], [1, 2, 3, 4]),
        ([5], [4]),
        ([4], [4]),
        ([1, 1, 1], [9]),
        ([3, 2, 1], [1, 9, 9]),
        ([2, 2, 2], [9, 9, 1]),
    ]
    for boxes, warehouse in examples:
        print(f"boxes {boxes}, warehouse {warehouse} -> {max_boxes_in_warehouse(boxes, warehouse)}")
    seed = 1564
    batch(3000, 6, 10)
    batch(300, 1000, 1000)
    batch(30, 100000, 1000000000)


main()
