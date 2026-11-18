# LeetCode #2224: Minimum Number of Operations to Convert Time -- the
# benchmark's Python mirror of convert.kara: each time read from its four
# digits, the gap in minutes cut greedily by 60s, 15s, 5s and 1s.


def minutes_of(time):
    d = [ord(c) - ord("0") for c in time if c != ":"]
    return (d[0] * 10 + d[1]) * 60 + d[2] * 10 + d[3]


def convert_time(current, correct):
    gap = minutes_of(correct) - minutes_of(current)
    operations = 0
    for step in (60, 15, 5, 1):
        operations += gap // step
        gap %= step
    return operations


seed = 2224


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # every time of the day as "HH:MM", built once
    times = [f"{m // 60:02}:{m % 60:02}" for m in range(1440)]
    check = 0
    for _ in range(2000000):
        a = next_random() % 1440
        b = next_random() % 1440
        low, high = (a, b) if a <= b else (b, a)
        check = (check * 31 + convert_time(times[low], times[high])) % 1000000007
    print(f"2000000 pairs: checksum {check}")


main()
