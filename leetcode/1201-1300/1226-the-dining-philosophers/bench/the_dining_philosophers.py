# LeetCode #1226 bench: the ★ arm in Python over the same 3 runs of
# n = 50000 as the Kāra bench: a thread per philosopher, a `threading.Lock`
# for each fork, the lower-numbered fork taken first.

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
    calls = 0
    valid = 0
    for order in [[0, 1, 2, 3, 4], [4, 3, 2, 1, 0], [2, 0, 4, 1, 3]]:
        log = run(50000, order)
        calls += len(log)
        if judge(50000, log) == "valid":
            valid += 1
    print(f"3 runs of n = 50000: {calls} calls, {valid} valid")


main()
