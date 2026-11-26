# LeetCode #1450 Number of Students Doing Homework at a Given Time: a mirror
# of busy_student.kara.


def busy_student(start_time, end_time, query_time):
    # each student's start and end side by side, kept when the query falls
    # between them, and counted
    return sum(1 for s, e in zip(start_time, end_time) if s <= query_time <= e)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def students(n, top):
    start_time, end_time = [], []
    for _ in range(n):
        a = 1 + next_random() % top
        b = 1 + next_random() % top
        start_time.append(min(a, b))
        end_time.append(max(a, b))
    return start_time, end_time


def main():
    global seed
    firsts = [
        busy_student([1, 2, 3], [3, 2, 7], 4),
        busy_student([4], [4], 4),
        busy_student([4], [4], 5),
        busy_student([1], [1000], 500),
        busy_student([1, 5, 9], [5, 9, 13], 5),
        busy_student([1, 5, 9], [5, 9, 13], 9),
    ]
    print(" ".join(str(x) for x in firsts))
    every = busy_student([1] * 100, [1000] * 100, 1000)
    seed = 1450
    start_time, end_time = students(100, 1000)
    asked = sum(busy_student(start_time, end_time, q) for q in range(1, 1001))
    print(f"100 students: {every}, and {asked} over every time")
    total = 0
    check = 0
    for _ in range(2000):
        n = 1 + next_random() % 100
        top = 1 + next_random() % 1000
        start_time, end_time = students(n, top)
        q = 1 + next_random() % top
        got = busy_student(start_time, end_time, q)
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random cases: {total} students, checksum {check}")


main()
