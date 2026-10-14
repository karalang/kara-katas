# Benchmark for #546: Python mirror of the ★ arm (memoized, with the
# boxes carried along); see remove_boxes.kara.
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
    return best(boxes, 0, n - 1, 0, [-1] * (n * n * n))


seed = 546


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 40 random rows of 100 boxes (the problem's most), from 2 to 9
    # colours by the row, built once. Then 5 times over every row is
    # answered and the points go into the checksum.
    rows = 40
    all_rows = []
    for g in range(rows):
        colours = 2 + g % 8
        all_rows.append([1 + next_random() % colours for _ in range(100)])
    total = 0
    checksum = 0
    for _ in range(5):
        for t in range(rows):
            points = remove_boxes(all_rows[t])
            total += points
            checksum = (checksum * 31 + points) % 1000000007
    print(f"{rows} rows, 5 times each: {total} points, checksum {checksum}")


main()
