# LeetCode #2224: Minimum Number of Operations to Convert Time -- mirror
# of convert.kara: the gap in minutes cut greedily by 60, 15, 5 and 1.


def minutes_of(time):
    d = [ord(c) - ord('0') for c in time if c != ':']
    return (d[0] * 10 + d[1]) * 60 + d[2] * 10 + d[3]


def convert_time(current, correct):
    gap = minutes_of(correct) - minutes_of(current)
    operations = 0
    for step in [60, 15, 5, 1]:
        operations += gap // step
        gap %= step
    return operations


seed = 2224


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# minutes since midnight as "HH:MM"
def clock(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def show(current, correct):
    print(f"{current} -> {correct}: {convert_time(current, correct)}")


def main():
    # LeetCode's two examples, then four more: no change, the whole
    # day, one of each step, and four of the smallest
    show("02:30", "04:35")
    show("11:00", "11:01")
    show("09:09", "09:09")
    show("00:00", "23:59")
    show("10:00", "11:21")
    show("12:56", "13:00")
    # 3000 random pairs, the earlier one first
    check = 0
    for _ in range(3000):
        a = next_random() % 1440
        b = next_random() % 1440
        low, high = min(a, b), max(a, b)
        check = (check * 31 + convert_time(clock(low), clock(high))) % 1000000007
    print(f"3000 pairs: checksum {check}")
    # every pair of the times 00:00, 00:29, 00:58, ... in order
    total = 0
    pairs = 0
    for a in range(50):
        for b in range(a, 50):
            total += convert_time(clock(a * 29), clock(b * 29))
            pairs += 1
    print(f"{pairs} pairs 29 minutes apart: {total} operations")


main()
