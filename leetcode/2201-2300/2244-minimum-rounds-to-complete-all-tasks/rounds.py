# LeetCode #2244: Minimum Rounds to Complete All Tasks -- the Python
# mirror of rounds.kara: the tasks of each difficulty counted; one task
# alone can never be done, and any other count c takes ceil(c / 3)
# rounds, summed.


def minimum_rounds(tasks):
    counts = {}
    for t in tasks:
        counts[t] = counts.get(t, 0) + 1
    rounds = 0
    for c in counts.values():
        if c == 1:
            return -1
        rounds += (c + 2) // 3
    return rounds


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    high = next_random()
    return high * 32768 + next_random()


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    global seed
    examples = [
        [2, 2, 3, 3, 2, 4, 4, 4, 4, 4],
        [2, 3, 3],
        [7],
        [5, 5],
        [1, 1, 1, 1],
        [9, 9, 9, 9, 9, 9, 9, 1000000000, 1000000000],
    ]
    for tasks in examples:
        print(f"{show(tasks)} -> {minimum_rounds(tasks)}")
    seed = 2244
    possible = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 60 + 1
        kinds = next_random() % 20 + 1
        tasks = [next_random() % kinds + 1 for _ in range(n)]
        rounds = minimum_rounds(tasks)
        if rounds >= 0:
            possible += 1
        check = (check * 31 + rounds + 1) % 1000000007
    print(f"3000 lists: {possible} possible, checksum {check}")
    tasks = []
    while len(tasks) < 99997:
        d = wide_random() % 1000000000 + 1
        for _ in range(next_random() % 2 + 2):
            tasks.append(d)
    while len(tasks) < 100000:
        tasks.append(tasks[0])
    print(f"100000 tasks: {minimum_rounds(tasks)}")
    tasks[99999] = 1000000001
    print(f"one lone task among them: {minimum_rounds(tasks)}")


main()
