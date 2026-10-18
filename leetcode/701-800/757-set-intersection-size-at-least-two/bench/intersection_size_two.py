# LeetCode 757 — Set Intersection Size At Least Two: benchmark, the ★ arm.


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


def main():
    rounds = 2000
    total = 0
    check = 0
    for _ in range(rounds):
        intervals = []
        for _ in range(3000):
            width = 1 + next_random() % 100000
            a = next_random() * 32768 % (100000000 - width + 1)
            intervals.append([a, a + width])
        answer = intersection_size_two(intervals)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"{rounds} sets of 3000 intervals: {total} points in all, checksum {check}")


main()
