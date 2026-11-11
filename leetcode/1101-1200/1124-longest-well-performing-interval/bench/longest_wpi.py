# LeetCode #1124: Longest Well-Performing Interval -- the bench, the same
# workload as longest_wpi.kara: the ★ arm over 16 schedules of 10^4 days,
# built once, each of 300 rounds turning one day in every schedule from
# tiring to not or back and solving it again.
seed = 1124


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def longest_wpi(hours):
    first = {}
    score = 0
    best = 0
    for i, h in enumerate(hours):
        score += 1 if h > 8 else -1
        if score > 0:
            best = i + 1
        else:
            j = first.get(score - 1)
            if j is not None:
                best = max(best, i - j)
            if score not in first:
                first[score] = i
    return best


def main():
    schedules = [[next_random() % 17 for _ in range(10000)] for _ in range(16)]
    total = 0
    check = 0
    for rnd in range(300):
        for j, hours in enumerate(schedules):
            at = (rnd * 7919 + j * 104729) % 10000
            h = hours[at]
            hours[at] = h - 9 if h > 8 else 9 + h % 8
            answer = longest_wpi(hours)
            total += answer
            check = (check * 31 + answer) % 1000000007
    print(f"300 rounds over 16 schedules of 10^4 days: answers total {total}, checksum {check}")


main()
