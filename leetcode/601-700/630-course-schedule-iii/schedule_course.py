# LeetCode #630: Course Schedule III -- Python mirror of the ★ arm.
#
# Courses by last day; a heap of the durations taken, the longest
# dropped whenever the total runs past a last day.

import heapq


def schedule_course(courses):
    order = sorted(courses, key=lambda c: c[1])
    taken = []
    time = 0
    for duration, last in order:
        time += duration
        heapq.heappush(taken, -duration)
        if time > last:
            time += heapq.heappop(taken)
    return len(taken)


seed = 630


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(courses):
    print(f"{courses} -> {schedule_course(courses)}")


def random_courses(count, longest, latest):
    courses = []
    for _ in range(count):
        duration = 1 + next_random() % longest
        last = 1 + next_random() % latest
        courses.append([duration, last])
    return courses


def main():
    show([[100, 200], [200, 1300], [1000, 1250], [2000, 3200]])
    show([[1, 2]])
    show([[3, 2], [4, 3]])
    show([[5, 5], [4, 6], [2, 6]])
    show([[1, 1], [1, 1], [1, 1]])
    show([[2, 5], [2, 5], [2, 5]])
    show([[7, 17], [3, 12], [10, 20], [9, 10], [5, 20], [10, 19], [18, 18]])
    show([[10000, 10000]])
    show([[5, 4]])
    total = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 30
        c = schedule_course(random_courses(n, 100, 1000))
        total += c
        checksum = (checksum * 31 + c) % 1000000007
    print(f"300 random cases: total {total}, checksum {checksum}")
    print(f"2000 courses: {schedule_course(random_courses(2000, 10000, 10000))}")
    print(f"2000 one-day courses: {schedule_course(random_courses(2000, 1, 1000))}")


main()
