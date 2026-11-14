# LeetCode #2140: Solving Questions With Brainpower -- the Python mirror of
# brainpower.kara's ★ arm.


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


def fmt(questions):
    return "[" + ", ".join(f"[{p}, {b}]" for p, b in questions) + "]"


def show(questions):
    print(f"{fmt(questions)} -> {most_points(questions)}")


def main():
    show([[3, 2], [4, 3], [4, 4], [2, 5]])
    show([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])
    show([[7, 0]])
    show([[1, 0], [2, 0], [3, 0]])
    show([[5, 9], [8, 9], [6, 9]])
    show([[1, 1], [1, 1], [100000, 100000]])
    total = 0
    check = 0
    for rnd in range(2000):
        n = next_random() % 12 + 1
        top = [10, 100000][rnd % 2]
        reach = [4, 13][(rnd // 2) % 2]
        questions = []
        for _ in range(n):
            p = next_random() % top + 1
            b = next_random() % reach
            questions.append([p, b])
        points = most_points(questions)
        total += points
        check = (check * 31 + points + n) % 1000000007
    print(f"2000 lists: {total} points in all, checksum {check}")
    none = [[100000 - i % 7, 0] for i in range(100000)]
    most = [[i % 100000 + 1, 100000] for i in range(100000)]
    rand = []
    for _ in range(100000):
        p = next_random() % 100000 + 1
        b = next_random() % 100001
        rand.append([p, b])
    x = most_points(none)
    y = most_points(most)
    z = most_points(rand)
    print(f"100000 questions: {x} with no brainpower, {y} with the most, {z} at random")


main()
