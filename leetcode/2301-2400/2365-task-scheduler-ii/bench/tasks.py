# LeetCode #2365: Task Scheduler II -- the bench, the ★ arm in Python: the
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


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    # list a: 10^5 tasks of 4^(a / 2 + 1) types (at most 10^5) up to
    # 10^9, with a space of 3^a
    lists = []
    space = 1
    for a in range(10):
        kinds = min(1 << (2 * (a // 2 + 1)), 100000)
        types = [1 + wide_random() % 1000000000 for _ in range(kinds)]
        tasks = [types[wide_random() % kinds] for _ in range(100000)]
        lists.append((tasks, space))
        space *= 3
    check = 0
    for p in range(20):
        for tasks, space in lists:
            check = (check * 31 + task_scheduler_ii(tasks, space) % 1000000007 + p) % 1000000007
    print(f"20 passes over 10 lists of 10^5 tasks: checksum {check}")


main()
