# LeetCode 759 — Employee Free Time: Python mirror of the ★ arm and its
# harness (same sort and sweep, same output).


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


def text(intervals):
    return "[" + ", ".join(f"[{a}, {b}]" for a, b in intervals) + "]"


def show(lists):
    schedule = [[(a, b) for a, b in employee] for employee in lists]
    print(f"{' '.join(text(e) for e in schedule)} -> {text(employee_free_time(schedule))}")


def main():
    show([[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]])
    show([[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]])
    show([[[1, 2]]])
    show([[[1, 2], [3, 4], [5, 6]]])
    show([[[1, 2]], [[2, 3]], [[3, 4]]])
    show([[[0, 100000000]], [[5, 6]]])
    show([[[7, 8]], [[1, 2]], [[4, 5]]])
    show([[[1, 10]], [[2, 3], [4, 5], [6, 7]]])
    gaps = 0
    length = 0
    check = 0
    for _ in range(300):
        employees = 1 + next_random() % 50
        spread = 1 + wide_random() % 999990
        schedule = []
        for _ in range(employees):
            count = 1 + next_random() % 50
            employee = []
            t = 0
            for _ in range(count):
                start = t + wide_random() % spread
                end = start + 1 + wide_random() % spread
                employee.append((start, end))
                t = end + 1
            schedule.append(employee)
        free = employee_free_time(schedule)
        gaps += len(free)
        for a, b in free:
            length += b - a
            check = (check * 31 + a) % 1000000007
            check = (check * 31 + b) % 1000000007
    print(f"300 random schedules: {gaps} free intervals, {length} free in all, checksum {check}")


main()
