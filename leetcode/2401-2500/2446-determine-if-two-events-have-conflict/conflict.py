# LeetCode #2446: Determine if Two Events Have Conflict -- Python mirror
# of the ★ arm (conflict.kara): each event starts no later than the other
# ends, the HH:MM strings compared as text.


def have_conflict(event1, event2):
    return event1[0] <= event2[1] and event2[0] <= event1[1]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def clock(minute):
    return f"{minute // 60:02}:{minute % 60:02}"


def random_event():
    a = next_random() % 1440
    b = next_random() % 1440
    return [clock(min(a, b)), clock(max(a, b))]


def show(v):
    return "[" + ", ".join(v) + "]"


def main():
    global seed
    cases = [
        (["01:15", "02:00"], ["02:00", "03:00"]),
        (["01:00", "02:00"], ["01:20", "03:00"]),
        (["10:00", "11:00"], ["14:00", "15:00"]),
        (["09:30", "10:30"], ["09:30", "10:30"]),
        (["14:00", "15:00"], ["10:00", "14:00"]),
        (["00:00", "23:59"], ["12:00", "12:01"]),
        (["05:05", "05:05"], ["05:06", "05:06"]),
        (["05:05", "05:05"], ["05:05", "05:05"]),
    ]
    for a, b in cases:
        print(f"{show(a)} {show(b)}: {'true' if have_conflict(a, b) else 'false'}")
    seed = 2446
    count = 0
    check = 0
    for i in range(3000):
        a = random_event()
        b = random_event()
        if have_conflict(a, b):
            count += 1
            check = (check * 31 + i) % 1000000007
    print(f"3000 random: {count} conflict, checksum {check}")
    count = 0
    check = 0
    for i in range(3000):
        s = next_random() % 1410
        t = next_random() % 1410
        a = [clock(s), clock(s + next_random() % 30)]
        b = [clock(t), clock(t + next_random() % 30)]
        if have_conflict(a, b):
            count += 1
            check = (check * 31 + i) % 1000000007
    print(f"3000 short: {count} conflict, checksum {check}")


main()
