# LeetCode 757 — Set Intersection Size At Least Two: Python mirror of the
# ★ arm and its harness (same greedy, same output).


def intersection_size_two(intervals):
    order = sorted(intervals, key=lambda x: (x[1], -x[0]))
    count = 0
    second = -1
    largest = -1
    for start, end in order:
        if start > largest:
            count += 2
            second = end - 1
            largest = end
        elif start > second:
            count += 1
            second = largest
            largest = end
    return count


seed = 757


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(intervals):
    print(f"{len(intervals)} intervals {intervals} -> {intersection_size_two(intervals)}")


def main():
    show([[1, 3], [3, 7], [8, 9]])
    show([[1, 3], [1, 4], [2, 5], [3, 5]])
    show([[1, 2], [2, 3], [2, 4], [4, 5]])
    show([[0, 1]])
    show([[0, 100000000]])
    show([[0, 1], [0, 1], [0, 1]])
    show([[1, 10], [2, 9], [3, 8], [4, 7], [5, 6]])
    show([[0, 2], [2, 4], [4, 6], [6, 8]])
    show([[0, 1], [2, 3], [4, 5], [6, 7]])
    total = 0
    check = 0
    for _ in range(200):
        n = 1 + next_random() % 400
        span = 2 + next_random() % 99999999
        intervals = []
        for _ in range(n):
            width = 1 + next_random() % (span // 20 + 1)
            a = next_random() * 32768 % (span - width + 1)
            intervals.append([a, a + width])
        answer = intersection_size_two(intervals)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"200 random sets of up to 400 intervals: {total} points in all, checksum {check}")


main()
