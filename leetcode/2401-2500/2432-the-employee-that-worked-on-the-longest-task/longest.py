# LeetCode #2432: The Employee That Worked on the Longest Task -- the
# Python mirror of the ★ arm: one pass with the last leave time in hand,
# the best replaced by a longer task or an equal one of a smaller id.

seed = 2432


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def random_logs(n, m, step):
    logs = []
    time = 0
    last = -1
    for _ in range(m):
        id = next_random() % n
        if id == last:
            id = (id + 1) % n
        time += 1 + next_random() % step
        logs.append([id, time])
        last = id
    return logs


def main():
    cases = [
        (10, [[0, 3], [2, 5], [0, 9], [1, 15]]),
        (26, [[1, 1], [3, 7], [2, 12], [7, 17]]),
        (2, [[0, 10], [1, 20]]),
        (5, [[4, 500]]),
        (4, [[3, 1], [1, 2], [2, 3], [0, 4], [3, 5]]),
        (3, [[2, 1], [1, 2], [0, 500]]),
        (9, [[8, 7], [5, 9], [2, 16]]),
    ]
    for n, logs in cases:
        print(f"n = {n}, logs {len(logs)}: {hardest_worker(n, logs)}")
    logs = [[499 - i, i + 1] for i in range(500)]
    print(f"500 logs, one unit each: {hardest_worker(500, logs)}")
    logs[250][1] = 252
    del logs[251]
    print(f"499 logs, one of two units: {hardest_worker(500, logs)}")
    print(f"250 random logs: {hardest_worker(500, random_logs(500, 250, 2))}")
    check = 0
    total = 0
    for _ in range(3000):
        n = 2 + next_random() % 9
        m = 1 + next_random() % 12
        step = 1 + next_random() % 4
        answer = hardest_worker(n, random_logs(n, m, step))
        check = (check * 31 + answer) % 1000000007
        total += answer
    print(f"3000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
