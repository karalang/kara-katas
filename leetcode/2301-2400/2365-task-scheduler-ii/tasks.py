# LeetCode #2365: Task Scheduler II -- the Python mirror of the ★ arm: the
# day goes forward one for each task, and jumps to the day after the
# type's last run plus `space` when that is later; a dict keeps each
# type's last day.


def task_scheduler_ii(tasks, space):
    last = {}
    day = 0
    for task in tasks:
        day += 1
        if task in last:
            day = max(day, last[task] + space + 1)
        last[task] = day
    return day


SEED = [2365]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # LeetCode's two examples; one task; 10^5 tasks of one type with a
    # space of 10^5; 10^5 tasks of two types in turn with a space of 1 and
    # of 2; 10^5 distinct tasks; then 2000 random lists of 1 to 40 tasks of
    # 1 to 6 types, with a space of 0 to 8
    print(task_scheduler_ii([1, 2, 1, 2, 3, 1], 3))
    print(task_scheduler_ii([5, 8, 8, 5], 2))
    print(task_scheduler_ii([1000000000], 100000))
    print(task_scheduler_ii([7] * 100000, 100000))
    pair = [1 + i % 2 for i in range(100000)]
    print(f"{task_scheduler_ii(pair, 1)} {task_scheduler_ii(pair, 2)}")
    print(task_scheduler_ii([1000000000 - i for i in range(100000)], 100000))
    check = 0
    idle = 0
    for _ in range(2000):
        n = 1 + next_random() % 40
        kinds = 1 + next_random() % 6
        space = next_random() % 9
        tasks = [1 + next_random() % kinds for _ in range(n)]
        days = task_scheduler_ii(tasks, space)
        check = (check * 31 + days) % 1000000007
        idle += days - n
    print(f"2000 lists: checksum {check}, {idle} idle days")


if __name__ == "__main__":
    main()
