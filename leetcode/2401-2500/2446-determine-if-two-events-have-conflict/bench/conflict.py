# LeetCode #2446: Determine if Two Events Have Conflict -- the bench, the
# ★ arm: the four `HH:MM` strings compared as text.


def have_conflict(event1, event2):
    return event1[0] <= event2[1] and event2[0] <= event1[1]


seed = 2446


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def clock(minute):
    return f"{minute // 60:02}:{minute % 60:02}"


def main():
    n = 100000
    events = []
    for _ in range(n):
        a = next_random() % 1440
        b = next_random() % 1440
        events.append([clock(min(a, b)), clock(max(a, b))])
    check = 0
    for p in range(300):
        for i in range(n):
            j = (7 * i + p + 1) % n
            answer = 1 if have_conflict(events[i], events[j]) else 0
            check = (check * 31 + answer + p) % 1000000007
    print(f"300 passes over 10^5 events: checksum {check}")


main()
