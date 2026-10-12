# Benchmark for #401: mirror of binary_watch.kara (try every time).
import sys


def ones(x):
    count = 0
    y = x
    while y > 0:
        count += y % 2
        y = y // 2
    return count


def read_binary_watch(turned_on):
    times = []
    for h in range(12):
        for m in range(60):
            if ones(h) + ones(m) == turned_on:
                times.append(f"{h}:{m:02}")
    return times


def main():
    calls = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
    times_total = 0
    chars = 0
    for c in range(calls):
        times = read_binary_watch(c % 11)
        times_total += len(times)
        for t in times:
            chars += len(t)
    print(f"{calls} calls: {times_total} times, {chars} characters")


main()
