# LeetCode #1580 bench: the same usable heights matched smallest first, in
# Python.


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


seed = 1580


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    problems = []
    for _ in range(40):
        boxes = [(next_random() * 32768 + next_random()) % 1000000000 + 1 for _ in range(100000)]
        warehouse = []
        for i in range(100000):
            valley = abs(i - 50000) * 20000
            warehouse.append(valley + (next_random() * 32768 + next_random()) % 1000000)
        problems.append((boxes, warehouse))
    check = 0
    total = 0
    for boxes, warehouse in problems:
        placed = max_boxes_in_warehouse(boxes, warehouse)
        total += placed
        check = mix(check, placed)
    print(f"40 problems of 100000 boxes and rooms: boxes placed {total}, checksum {check}")


main()
