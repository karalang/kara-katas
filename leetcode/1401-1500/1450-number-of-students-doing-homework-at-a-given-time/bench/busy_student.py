# LeetCode #1450 Number of Students Doing Homework at a Given Time: the
# bench, a mirror of busy_student.kara.


def busy_student(start_time, end_time, query_time):
    # each student's start and end side by side, kept when the query falls
    # between them, and counted
    return sum(1 for s, e in zip(start_time, end_time) if s <= query_time <= e)


def main():
    # 3000 classes of 100 students, the constraints' most, each from a
    # start to an end drawn from 1 to 1000, each class asked at every time
    # from 1 to 1000, the counts folded to a checksum
    seed = 1450
    check = 0
    for _ in range(3000):
        start_time, end_time = [], []
        for _ in range(100):
            seed = (seed * 1103515245 + 12345) % 2147483648
            a = 1 + seed // 65536 % 1000
            seed = (seed * 1103515245 + 12345) % 2147483648
            b = 1 + seed // 65536 % 1000
            start_time.append(min(a, b))
            end_time.append(max(a, b))
        for q in range(1, 1001):
            check = (check * 131 + busy_student(start_time, end_time, q)) % 1000000007
    print(f"3000 classes asked 1000 times: checksum {check}")


main()
