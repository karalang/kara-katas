# LeetCode 759 — Employee Free Time: benchmark, the ★ arm.


def employee_free_time(schedule):
    pool = sorted((iv for employee in schedule for iv in employee), key=lambda iv: iv[0])
    free = []
    end = pool[0][1]
    for start, finish in pool:
        if start > end:
            free.append((end, start))
        if finish > end:
            end = finish
    return free


seed = 759


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def main():
    rounds = 3000
    gaps = 0
    length = 0
    check = 0
    for _ in range(rounds):
        schedule = []
        for _ in range(50):
            employee = []
            t = 0
            for _ in range(50):
                start = t + wide_random() % 1000000
                end = start + 1 + wide_random() % 900000
                employee.append((start, end))
                t = end + 1
            schedule.append(employee)
        free = employee_free_time(schedule)
        gaps += len(free)
        for a, b in free:
            length += b - a
            check = (check * 31 + a) % 1000000007
    print(f"{rounds} schedules of 50 x 50 intervals: {gaps} free intervals, {length} free in all, checksum {check}")


main()
