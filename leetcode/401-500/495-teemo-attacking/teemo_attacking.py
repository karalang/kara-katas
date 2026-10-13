# LeetCode #495: Teemo Attacking -- Python mirror of the ★ arm (each gap,
# capped); see teemo_attacking.kara.


def find_poisoned_duration(time_series, duration):
    total = 0
    for i in range(len(time_series)):
        if i + 1 < len(time_series):
            total += min(time_series[i + 1] - time_series[i], duration)
        else:
            total += duration
    return total


def show(name, time_series, duration):
    print(f"{name}: {time_series} for {duration} -> {find_poisoned_duration(time_series, duration)}")


seed = 495


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("example 1", [1, 4], 2)
    show("example 2", [1, 2], 2)
    show("one attack", [5], 3)
    show("zero duration", [1, 2, 3], 0)
    show("back to back", [0, 1, 2, 3], 1)
    show("exactly touching", [0, 5, 10], 5)
    show("at time zero", [0, 0], 10)
    show("large", [0, 10000000], 10000000)
    # 300 random series of 1 to 30 attacks with gaps of 0 to 9, each
    # with a duration of 0 to 9.
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        size = 1 + next_random() % 30
        series = []
        t = next_random() % 5
        for _ in range(size):
            series.append(t)
            t += next_random() % 10
        duration = next_random() % 10
        poisoned = find_poisoned_duration(series, duration)
        total += poisoned
        checksum = (checksum * 31 + poisoned) % 1000000007
    print(f"{count} random series: {total} poisoned in all, checksum {checksum}")


main()
