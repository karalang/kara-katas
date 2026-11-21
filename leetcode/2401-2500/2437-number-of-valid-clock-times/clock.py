# LeetCode #2437: Number of Valid Clock Times -- the Python mirror of the
# ★ arm: the hours that fit the first two characters times the minutes
# that fit the last two.

seed = 2437


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fits(pattern, value):
    tens = str(value // 10)
    units = str(value % 10)
    return (pattern[0] == "?" or pattern[0] == tens) and (pattern[1] == "?" or pattern[1] == units)


def count_time(time):
    hours = sum(1 for h in range(24) if fits(time[0:2], h))
    minutes = sum(1 for m in range(60) if fits(time[3:5], m))
    return hours * minutes


def masked(minute_of_day, mask):
    shown = f"{minute_of_day // 60:02}:{minute_of_day % 60:02}"
    out = []
    digit = 0
    for c in shown:
        if c == ":":
            out.append(c)
        else:
            out.append("?" if (mask >> digit) & 1 == 1 else c)
            digit += 1
    return "".join(out)


def main():
    for t in ["?5:00", "0?:0?", "??:??", "23:59", "?3:15", "?4:15", "1?:30", "2?:30", "12:?9", "12:5?"]:
        print(f"{t}: {count_time(t)}")
    check = 0
    total = 0
    for _ in range(3000):
        at = next_random() % 1440
        answer = count_time(masked(at, next_random() % 16))
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
