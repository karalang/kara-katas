# LeetCode #546: Remove Boxes -- Python mirror of the ★ arm (memoized,
# with the boxes carried along); see remove_boxes.kara.
import sys

sys.setrecursionlimit(100000)


def best(boxes, l, r, k, memo):
    if l > r:
        return 0
    n = len(boxes)
    key = (l * n + r) * n + k
    if memo[key] >= 0:
        return memo[key]
    i = l
    run = k + 1
    while i < r and boxes[i + 1] == boxes[l]:
        i += 1
        run += 1
    most = run * run + best(boxes, i + 1, r, 0, memo)
    for m in range(i + 2, r + 1):
        if boxes[m] == boxes[l] and boxes[m - 1] != boxes[l]:
            most = max(most, best(boxes, i + 1, m - 1, 0, memo) + best(boxes, m, r, run, memo))
    memo[key] = most
    return most


def remove_boxes(boxes):
    n = len(boxes)
    memo = [-1] * (n * n * n)
    return best(boxes, 0, n - 1, 0, memo)


# ---- test harness ----------------------------------------------------------

seed = 546


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(name, boxes):
    print(f"{name}: [{', '.join(map(str, boxes))}] -> {remove_boxes(boxes)}")


def main():
    show("example 1", [1, 3, 2, 2, 2, 3, 4, 3, 1])
    show("example 2", [1, 1, 1])
    show("example 3", [1])
    show("two colours alternating", [1, 2, 1, 2, 1, 2, 1])
    show("a nest", [1, 2, 3, 2, 1])
    show("worth waiting for", [1, 2, 2, 1, 1, 3, 1])
    count = 300
    boxes_in = total = h = 0
    for t in range(count):
        n = 1 + next_random() % 20
        colours = 3 if t % 3 == 0 else 5 if t % 3 == 1 else 10
        b = [1 + next_random() % colours for _ in range(n)]
        points = remove_boxes(b)
        boxes_in += n
        total += points
        h = (h * 31 + points) % 1000000007
    print(f"{count} random rows: {boxes_in} boxes, {total} points, checksum {h}")
    b = [1 + next_random() % 3 for _ in range(100)]
    print(f"100 boxes from 3 colours: {remove_boxes(b)}")
    b = [1 + next_random() % 100 for _ in range(100)]
    print(f"100 boxes from 100 colours: {remove_boxes(b)}")
    print(f"100 boxes of one colour: {remove_boxes([7] * 100)}")
    print(f"100 boxes, two colours alternating: {remove_boxes([1 + i % 2 for i in range(100)])}")
    print(f"a palindrome of 50 colours: {remove_boxes([1 + i for i in range(50)] + [50 - i for i in range(50)])}")


main()
