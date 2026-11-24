# LeetCode #1344 bench in Python: the ★ arm (the hour hand 30 degrees an
# hour plus half a degree a minute, the minute hand 6 a minute, and the
# smaller of the gap and 360 less it) on the same 3 * 10^7 times.


def angle_clock(hour, minutes):
    hour_hand = (hour % 12) * 30.0 + minutes * 0.5
    minute_hand = minutes * 6.0
    gap = abs(hour_hand - minute_hand)
    return min(gap, 360.0 - gap)


def main():
    check = 0
    for i in range(30000000):
        since = (i + check) % 720
        hour = since // 60
        if hour == 0:
            hour = 12
        a = angle_clock(hour, since % 60)
        check = (check * 31 + int(2.0 * a)) % 1000000007
    print(f"3 * 10^7 times: checksum {check}")


main()
