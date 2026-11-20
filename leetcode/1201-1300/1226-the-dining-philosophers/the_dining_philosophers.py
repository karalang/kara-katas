# LeetCode #1226: The Dining Philosophers -- Python mirror of the ★ arm: a
# `threading.Lock` for each fork, every philosopher taking the
# lower-numbered of their two forks first. Philosopher i's left fork is
# fork i and the right fork is fork (i + 4) % 5.

import threading


class DiningPhilosophers:
    def __init__(self):
        self.forks = [threading.Lock() for _ in range(5)]

    def wantsToEat(self, philosopher, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork):
        left = philosopher
        right = (philosopher + 4) % 5
        with self.forks[min(left, right)], self.forks[max(left, right)]:
            pickLeftFork()
            pickRightFork()
            eat()
            putLeftFork()
            putRightFork()


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def run(n, order):
    table = DiningPhilosophers()
    log = []
    lock = threading.Lock()

    def append(entry):
        with lock:
            log.append(entry)

    def philosopher(p):
        for _ in range(n):
            table.wantsToEat(
                p,
                lambda: append((p, 1, 1)),
                lambda: append((p, 2, 1)),
                lambda: append((p, 0, 3)),
                lambda: append((p, 1, 2)),
                lambda: append((p, 2, 2)),
            )

    threads = [threading.Thread(target=philosopher, args=(p,)) for p in order]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return log


def judge(n, log):
    holder = [-1] * 5
    meals = [0] * 5
    for p, fork, op in log:
        f = p if fork == 1 else (p + 4) % 5
        if op == 1:
            if holder[f] != -1:
                return f"philosopher {p} picks up fork {f}, held by {holder[f]}"
            holder[f] = p
        elif op == 2:
            if holder[f] != p:
                return f"philosopher {p} puts down fork {f}, not holding it"
            holder[f] = -1
        else:
            if holder[p] != p or holder[(p + 4) % 5] != p:
                return f"philosopher {p} eats without both forks"
            meals[p] += 1
    if any(m != n for m in meals):
        return f"meals {meals}"
    if any(h != -1 for h in holder):
        return f"forks left held {holder}"
    return "valid"


def main():
    example = [(4, 2, 1), (4, 1, 1), (0, 1, 1), (2, 2, 1), (2, 1, 1), (2, 0, 3), (2, 1, 2), (2, 2, 2), (4, 0, 3), (4, 1, 2), (0, 2, 1), (4, 2, 2), (3, 2, 1), (3, 1, 1), (0, 0, 3), (0, 1, 2), (0, 2, 2), (1, 2, 1), (1, 1, 1), (3, 0, 3), (3, 1, 2), (3, 2, 2), (1, 0, 3), (1, 1, 2), (1, 2, 2)]
    print(f"LeetCode's example: {len(example)} calls, {judge(1, example)}")
    for n in [1, 2, 60]:
        log = run(n, [0, 1, 2, 3, 4])
        print(f"n={n}: {len(log)} calls, {judge(n, log)}")
    seed = [1226]
    calls = 0
    valid = 0
    for _ in range(1000):
        n = next_random(seed) % 60 + 1
        order = [0, 1, 2, 3, 4]
        for i in range(4, 0, -1):
            j = next_random(seed) % (i + 1)
            order[i], order[j] = order[j], order[i]
        log = run(n, order)
        calls += len(log)
        if judge(n, log) == "valid":
            valid += 1
    print(f"1000 random runs: {calls} calls, {valid} valid")


main()
