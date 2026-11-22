# LeetCode #2895: Minimum Processing Time -- the Python mirror of the ★
# arm (processing.kara): the processor free first takes the four longest
# tasks, and so on.


def min_processing_time(processor_time, tasks):
    free = sorted(processor_time)
    longest = sorted(tasks, reverse=True)
    finish = 0
    for i, p in enumerate(free):
        finish = max(finish, p + longest[4 * i])
    return finish


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    global seed
    print(f"{min_processing_time([8, 10], [2, 2, 3, 1, 8, 7, 4, 5])} {min_processing_time([10, 20], [2, 3, 1, 2, 5, 8, 4, 3])}")
    n = 25000
    print(f"{min_processing_time([0] * n, list(range(1, 4 * n + 1)))} {min_processing_time([1000000000] * n, [1000000000] * (4 * n))}")
    seed = 2895
    total = 0
    check = 0
    for c in range(3100):
        small = c < 3000
        n = next_random() % 3 + 1 if small else wide() % 24751 + 250
        top = 20 if small else 1000000000
        processors = [wide() % top + 1 for _ in range(n)]
        tasks = [wide() % top + 1 for _ in range(4 * n)]
        time = min_processing_time(processors, tasks)
        total += time
        check = (check * 31 + time) % 1000000007
        if c == 2999:
            print(f"3000 small cases: times total {total}, checksum {check}")
            total = 0
            check = 0
    print(f"100 large cases: times total {total}, checksum {check}")


main()
