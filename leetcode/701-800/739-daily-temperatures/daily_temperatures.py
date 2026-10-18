# LeetCode #739: Daily Temperatures -- a stack of colder days.
# Mirror of the Kara star arm: walk the days keeping a stack of the days
# still waiting; a day warmer than the top answers it, and every day
# under it that it is warmer than, and then waits itself.


def daily_temperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    waiting = []
    for i in range(n):
        while waiting and temperatures[waiting[-1]] < temperatures[i]:
            j = waiting.pop()
            answer[j] = i - j
        waiting.append(i)
    return answer


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def fmt(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def show(temperatures):
    print(f"{fmt(temperatures)} -> {fmt(daily_temperatures(temperatures))}")


def digest(what, temperatures):
    answer = daily_temperatures(temperatures)
    total = 0
    zeros = 0
    for a in answer:
        total = (total * 131 + a + 1) % 1000000007
        if a == 0:
            zeros += 1
    print(f"{what} -> {zeros} with no warmer day, checksum {total}")


def main():
    show([73, 74, 75, 71, 69, 72, 76, 73])
    show([30, 40, 50, 60])
    show([30, 60, 90])
    show([50])
    show([55, 55, 55, 55])
    show([100, 90, 80, 70, 60, 50, 40, 30])
    show([60, 50, 50, 40, 70, 30, 30, 80])
    show([30, 100, 30, 100, 30, 100])
    seed = [739]
    random = [30 + next_random(seed) % 71 for _ in range(100000)]
    digest("100000 random days", random)
    falling = [99 - i * 70 // 99999 for i in range(99999)] + [100]
    digest("99999 days cooling and then a hot one", falling)
    saw = [30 + i % 71 for i in range(100000)]
    digest("100000 days rising from 30 to 100 again and again", saw)
    total = 0
    waits = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 12
        rng = 1 + next_random(seed) % 6
        days = [30 + next_random(seed) % rng for _ in range(n)]
        for a in daily_temperatures(days):
            waits += a
            total = (total * 131 + a + 1) % 1000000007
        total = (total * 131 + 7) % 1000000007
    print(f"300 random short runs: {waits} days waited in all, checksum {total}")


main()
