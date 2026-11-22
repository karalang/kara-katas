# LeetCode #2895: Minimum Processing Time -- the bench, as
# processing.kara: 20 cases of 25000 processors and 10^5 tasks, each
# answered 20 times by the sorting arm, each sorting fresh copies.


def min_processing_time(processor_time, tasks):
    free = sorted(processor_time)
    longest = sorted(tasks, reverse=True)
    finish = 0
    for i, p in enumerate(free):
        finish = max(finish, p + longest[4 * i])
    return finish


seed = 2895


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count, rounds, n = 20, 20, 25000
    cases = []
    for _ in range(count):
        processors = [wide() % 1000000000 for _ in range(n)]
        tasks = [wide() % 1000000000 + 1 for _ in range(4 * n)]
        cases.append((processors, tasks))
    total = 0
    check = 0
    for r in range(rounds):
        for processors, tasks in cases:
            time = min_processing_time(processors, tasks)
            total += time
            check = (check * 31 + time + r) % 1000000007
    print(f"{count} cases of {n}, {rounds} rounds: times total {total}, checksum {check}")


main()
