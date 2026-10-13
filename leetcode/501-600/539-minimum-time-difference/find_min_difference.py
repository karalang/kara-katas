# LeetCode #539: Minimum Time Difference -- Python mirror of the ★ arm
# (minutes, sorted); see find_min_difference.kara.


def minutes(t):
    return int(t[0:2]) * 60 + int(t[3:5])


def find_min_difference(time_points):
    mins = sorted(minutes(t) for t in time_points)
    best = mins[0] + 1440 - mins[-1]
    for i in range(1, len(mins)):
        best = min(best, mins[i] - mins[i - 1])
    return best


# ---- test harness ---------------------------------------------------------

seed = 539


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def clock(minute):
    return f"{minute // 60:02}:{minute % 60:02}"


def show(name, times):
    answer = find_min_difference(times)
    if len(times) <= 8:
        print(f"{name}: [{', '.join(times)}] -> {answer}")
    else:
        print(f"{name}: {len(times)} times -> {answer}")


def spread(name, step):
    times = [clock(m) for m in range(0, 1440, step)]
    for i in range(len(times) - 1, 0, -1):
        j = (next_random() * 32768 + next_random()) % (i + 1)
        times[i], times[j] = times[j], times[i]
    show(name, times)


def main():
    show("example 1", ["23:59", "00:00"])
    show("example 2", ["00:00", "23:59", "00:00"])
    show("half a day", ["12:00", "00:00"])
    show("the same time twice", ["07:30", "07:30"])
    show("closest across midnight", ["23:50", "00:05", "12:00"])
    show("closest inside the day", ["01:00", "02:00", "01:59", "23:00"])
    show("hours apart", ["03:00", "09:00", "15:00", "21:00"])
    count = 300
    total = 0
    zeros = 0
    checksum = 0
    for t in range(count):
        size = 2 + next_random() % 59
        span = 1440 if t % 2 == 0 else 120
        times = [clock(next_random() % span) for _ in range(size)]
        total += size
        answer = find_min_difference(times)
        if answer == 0:
            zeros += 1
        checksum = (checksum * 31 + answer) % 1000000007
    print(f"{count} random lists: {total} times, {zeros} with a repeat, checksum {checksum}")
    spread("every third minute", 3)
    spread("every minute", 1)
    times = [clock(next_random() % 1440) for _ in range(20000)]
    show("20000 random times", times)


main()
