# LeetCode #2437: Number of Valid Clock Times -- the bench, the ★ arm:
# the hours that fit the first two characters times the minutes that
# fit the last two.


def fits(pattern, value):
    tens = 48 + value // 10
    units = 48 + value % 10
    return (pattern[0] == 63 or pattern[0] == tens) and (pattern[1] == 63 or pattern[1] == units)


def count_time(time):
    b = time.encode()
    hours = 0
    for h in range(24):
        if fits(b[0:2], h):
            hours += 1
    minutes = 0
    for m in range(60):
        if fits(b[3:5], m):
            minutes += 1
    return hours * minutes


def main():
    times = []
    for at in range(1440):
        for mask in range(16):
            shown = f"{at // 60:02}:{at % 60:02}"
            out = []
            digit = 0
            for c in shown:
                if c == ":":
                    out.append(c)
                else:
                    out.append("?" if (mask >> digit) & 1 == 1 else c)
                    digit += 1
            times.append("".join(out))
    check = 0
    n = len(times)
    for p in range(120):
        for i in range(n):
            check = (check * 31 + count_time(times[(i * 7 + p) % n]) + p) % 1000000007
    print(f"120 passes over 23040 patterns: checksum {check}")


main()
