# LeetCode #1564: Put Boxes Into the Warehouse I -- bench: the ★ arm
# (usable heights, the smallest boxes into the deepest rooms) over 20
# problems of 100000 boxes and 100000 rooms, built once, each asked 10
# times.
# Python mirror of warehouse.kara.


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


seed = 1564


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    top = 1000000000
    problems = []
    for _ in range(20):
        boxes = [(next_random() * 32768 + next_random()) % top + 1 for _ in range(100000)]
        warehouse = [top - (next_random() * 32768 + next_random()) % ((top + 1) // 2) for _ in range(100000)]
        problems.append((boxes, warehouse))
    check = 0
    total = 0
    for _ in range(10):
        for boxes, warehouse in problems:
            placed = max_boxes_in_warehouse(boxes, warehouse)
            total += placed
            check = mix(check, placed)
    print(f"10 passes over 20 problems of 100000 boxes and rooms: {total} boxes, checksum {check}")


main()
