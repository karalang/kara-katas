# LeetCode #681: Next Closest Time -- step a minute at a time.
# Mirrors the ★ arm (next_closest_time.kara) and its test harness.


def digits_of(minutes):
    h, m = divmod(minutes, 60)
    return [h // 10, h % 10, m // 10, m % 10]


def next_closest_time(time):
    h = int(time[0]) * 10 + int(time[1])
    m = int(time[3]) * 10 + int(time[4])
    allowed = [False] * 10
    for d in digits_of(h * 60 + m):
        allowed[d] = True
    now = h * 60 + m
    while True:
        now = (now + 1) % 1440
        if all(allowed[d] for d in digits_of(now)):
            return f"{now // 600}{now // 60 % 10}:{now % 60 // 10}{now % 10}"


def clock(minutes):
    h, m = divmod(minutes, 60)
    return f"{h // 10}{h % 10}:{m // 10}{m % 10}"


def minutes_of(time):
    return (int(time[0]) * 10 + int(time[1])) * 60 + int(time[3]) * 10 + int(time[4])


def show(time):
    print(f'"{time}" -> "{next_closest_time(time)}"')


def main():
    for t in ["19:34", "23:59", "00:00", "11:11", "13:55", "01:32", "20:48",
              "22:23", "06:59", "23:32", "12:09", "15:55"]:
        show(t)
    checksum = 0
    same = 0
    wrapped = 0
    ahead_total = 0
    farthest = 0
    farthest_at = ""
    for now in range(1440):
        time = clock(now)
        then = minutes_of(next_closest_time(time))
        ahead = (then - now + 1440) % 1440
        if ahead == 0:
            ahead = 1440
            same += 1
        if then <= now:
            wrapped += 1
        ahead_total += ahead
        if ahead < 1440 and ahead > farthest:
            farthest = ahead
            farthest_at = time
        checksum = (checksum * 1441 + then + 1) % 1000000007
    print(f"1440 times: {same} answer themselves, {wrapped} answer on the next day")
    print(f'{ahead_total} minutes ahead in all; farthest but a whole day {farthest}, from "{farthest_at}"')
    print(f"checksum {checksum}")


main()
