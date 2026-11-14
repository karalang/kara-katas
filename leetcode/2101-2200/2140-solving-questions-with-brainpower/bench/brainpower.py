# LeetCode #2140: Solving Questions With Brainpower -- the benchmark, the
# same algorithm as brainpower.kara.


def most_points(questions):
    n = len(questions)
    best = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        nxt = min(i + 1 + questions[i][1], n)
        best[i] = max(best[i + 1], questions[i][0] + best[nxt])
    return best[0]


seed = 2140


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for _ in range(10):
        questions = []
        for _ in range(100000):
            points = next_random() % 100000 + 1
            brainpower = next_random() % 21
            questions.append([points, brainpower])
        lists.append(questions)
    total = 0
    check = 0
    for rnd in range(20):
        for l in range(10):
            hi = next_random()
            at = (hi * 32768 + next_random()) % 100000
            lists[l][at][0] = next_random() % 100000 + 1
            lists[l][at][1] = next_random() % 21
            points = most_points(lists[l])
            total += points
            check = (check * 31 + points + rnd) % 1000000007
    print(f"200 solves: {total} points in all, checksum {check}")


main()
