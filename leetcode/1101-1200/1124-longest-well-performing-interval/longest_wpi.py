# LeetCode #1124: Longest Well-Performing Interval -- Python mirror of the
# ★ arm.
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
            if score - 1 in first:
                best = max(best, i - first[score - 1])
            if score not in first:
                first[score] = i
    return best


def random_hours(n, tilt):
    hours = []
    for _ in range(n):
        r = next_random() % 100
        if (tilt and r < 52) or (not tilt and r < 40):
            h = 9 + next_random() % 8
        else:
            h = next_random() % 9
        hours.append(h)
    return hours


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    cases = [
        [9, 9, 6, 0, 6, 6, 9],
        [6, 6, 6],
        [9, 10, 12],
        [0, 1, 2, 3],
        [6],
        [9],
        [9, 6, 9, 6, 9],
        [6, 6, 6, 6, 9, 9, 9],
        [8, 9, 8, 9, 8],
    ]
    for c in cases:
        print(f"{show(c)} -> {longest_wpi(c)}")
    total = 0
    check = 0
    for t in range(2000):
        n = next_random() % 10000 + 1
        hours = random_hours(n, t % 2 == 1)
        answer = longest_wpi(hours)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"2000 random schedules: answers total {total}, checksum {check}")


main()
