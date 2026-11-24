# LeetCode #1344: Angle Between Hands of a Clock -- Python mirror of the ★
# arm: the hour hand 30 degrees an hour plus half a degree a minute, the
# minute hand 6 degrees a minute, and the smaller of the gap and 360 less
# it.


def angle_clock(hour, minutes):
    hour_hand = (hour % 12) * 30.0 + minutes * 0.5
    minute_hand = minutes * 6.0
    gap = abs(hour_hand - minute_hand)
    return min(gap, 360.0 - gap)


def main():
    print(" ".join(str(angle_clock(h, m)) for h, m in ((12, 30), (3, 30), (3, 15), (12, 0), (6, 0), (1, 5))))
    total = 0.0
    largest = 0.0
    check = 0
    for hour in range(1, 13):
        for minutes in range(60):
            a = angle_clock(hour, minutes)
            total += a
            largest = max(largest, a)
            check = (check * 131 + int(2.0 * a)) % 1000000007
    print(f"720 times: angles total {total}, largest {largest}, checksum {check}")


main()
