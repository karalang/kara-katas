# Benchmark for #495: Python mirror of the ★ arm (each gap, capped); see
# teemo_attacking.kara.


def find_poisoned_duration(time_series, duration):
    total = 0
    for i in range(len(time_series)):
        if i + 1 < len(time_series):
            total += min(time_series[i + 1] - time_series[i], duration)
        else:
            total += duration
    return total


def main():
    # 200 series of 10,000 attacks (the problem's most) with gaps of 0
    # to 99, built once, then each solved for every duration from 0 to
    # 49.
    seed = 495

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    all_series = []
    for _ in range(200):
        series = []
        t = 0
        for _ in range(10000):
            series.append(t)
            t += next_random() % 100
        all_series.append(series)
    total = 0
    checksum = 0
    for series in all_series:
        for duration in range(50):
            poisoned = find_poisoned_duration(series, duration)
            total += poisoned
            checksum = (checksum * 31 + poisoned) % 1000000007
    print(f"200 series of 10000, 50 durations each: {total} poisoned in all, checksum {checksum}")


main()
