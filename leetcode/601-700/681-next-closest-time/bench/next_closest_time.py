# LeetCode #681: Next Closest Time -- step a minute at a time. Bench.


def digits_of(minutes):
    h, m = divmod(minutes, 60)
    return (h // 10, h % 10, m // 10, m % 10)


def next_closest_time(time):
    h = (ord(time[0]) - 48) * 10 + ord(time[1]) - 48
    m = (ord(time[3]) - 48) * 10 + ord(time[4]) - 48
    allowed = [False] * 10
    for d in digits_of(h * 60 + m):
        allowed[d] = True
    now = h * 60 + m
    while True:
        now = (now + 1) % 1440
        ok = True
        for d in digits_of(now):
            if not allowed[d]:
                ok = False
        if ok:
            return f"{now // 600}{now // 60 % 10}:{now % 60 // 10}{now % 10}"


def main():
    rounds = 300
    times = [f"{t // 60:02d}:{t % 60:02d}" for t in range(1440)]
    total = 0
    wrapped = 0
    for r in range(rounds):
        for k in range(1440):
            at = (k * 7 + r) % 1440
            a = next_closest_time(times[at])
            then = ((ord(a[0]) - 48) * 10 + ord(a[1]) - 48) * 60 + (ord(a[3]) - 48) * 10 + ord(a[4]) - 48
            if then <= at:
                wrapped += 1
            total = (total * 1441 + then + 1) % 1000000007
    print(f"{1440 * rounds} times: {wrapped} answers on the next day, checksum {total}")


main()
