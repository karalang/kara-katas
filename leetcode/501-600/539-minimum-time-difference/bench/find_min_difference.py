# Benchmark for #539: Python mirror of the ★ arm (minutes, sorted); see
# find_min_difference.kara.


def minutes(t):
    return int(t[0:2]) * 60 + int(t[3:5])


def find_min_difference(time_points):
    mins = sorted(minutes(t) for t in time_points)
    best = mins[0] + 1440 - mins[-1]
    for i in range(1, len(mins)):
        best = min(best, mins[i] - mins[i - 1])
    return best


seed = 539


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def clock(minute):
    return f"{minute // 60:02}:{minute % 60:02}"


def main():
    # 300 lists of 20 to 1,440 distinct times, the first places of a
    # shuffle of the whole day, built once. Then the answer for each
    # list is found 100 times.
    lists = 300
    day = list(range(1440))
    all_lists = []
    total_times = 0
    for _ in range(lists):
        size = 20 + next_random() % 1421
        times = []
        for i in range(size):
            j = i + next_random() % (1440 - i)
            day[i], day[j] = day[j], day[i]
            times.append(clock(day[i]))
        total_times += size
        all_lists.append(times)
    total = 0
    checksum = 0
    for _ in range(100):
        for times in all_lists:
            answer = find_min_difference(times)
            total += answer
            checksum = (checksum * 31 + answer) % 1000000007
    print(f"{lists} lists, {total_times} times, 100 times each: total {total}, checksum {checksum}")


main()
