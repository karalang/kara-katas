# LeetCode #739: Daily Temperatures -- a stack of colder days.
# Benchmark mirror of the Kara star arm: walk the days keeping a stack
# of the days still waiting; a day warmer than the top answers it, and
# every day under it that it is warmer than, and then waits itself.


def daily_temperatures(temperatures):
    n = len(temperatures)
    answer = []
    for _ in range(n):
        answer.append(0)
    waiting = []
    for i in range(n):
        while waiting and temperatures[waiting[-1]] < temperatures[i]:
            j = waiting.pop()
            answer[j] = i - j
        waiting.append(i)
    return answer


def main():
    seed = 739
    n = 100000

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    t = [30 + next_random() % 71 for _ in range(n)]
    total = 0
    for _ in range(300):
        for _ in range(100):
            a = next_random()
            b = next_random()
            j = (a * 32768 + b) % n
            t[j] = 30 + next_random() % 71
        for a in daily_temperatures(t):
            total += a
    print(f"300 rounds of 100000 days: {total} days waited in all")


main()
