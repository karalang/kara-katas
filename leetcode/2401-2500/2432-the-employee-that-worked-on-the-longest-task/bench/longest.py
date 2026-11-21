# LeetCode #2432: The Employee That Worked on the Longest Task -- the
# bench, the ★ arm: one pass with the last leave time in hand, the best
# replaced by a longer task or an equal one of a smaller id.


def hardest_worker(n, logs):
    best_id = n
    best_time = 0
    start = 0
    for log in logs:
        time = log[1] - start
        if time > best_time or (time == best_time and log[0] < best_id):
            best_time = time
            best_id = log[0]
        start = log[1]
    return best_id


seed = 2432


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for _ in range(2000):
        logs = []
        time = 0
        last = -1
        for _ in range(500):
            id = next_random() % 500
            if id == last:
                id = (id + 1) % 500
            time += 1 + next_random() % 3
            logs.append([id, time])
            last = id
        cases.append(logs)
    check = 0
    for p in range(50):
        for c in range(len(cases)):
            cases[c][499][1] += 1
            check = (check * 31 + hardest_worker(500, cases[c]) + p) % 1000000007
    print(f"50 passes over 2000 cases of 500 logs: checksum {check}")


main()
