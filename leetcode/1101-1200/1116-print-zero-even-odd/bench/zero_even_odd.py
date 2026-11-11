# LeetCode #1116: Print Zero Even Odd -- the bench's Python mirror: a
# thread per method and three `threading.Semaphore`s as the ★ arm's
# three turn channels, zero's holding one permit; the log behind a lock.
import threading


class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.zero_turn = threading.Semaphore(1)
        self.even_turn = threading.Semaphore(0)
        self.odd_turn = threading.Semaphore(0)

    def zero(self, print_number):
        for i in range(1, self.n + 1):
            self.zero_turn.acquire()
            print_number(0)
            (self.odd_turn if i % 2 == 1 else self.even_turn).release()

    def even(self, print_number):
        for i in range(2, self.n + 1, 2):
            self.even_turn.acquire()
            print_number(i)
            self.zero_turn.release()

    def odd(self, print_number):
        for i in range(1, self.n + 1, 2):
            self.odd_turn.acquire()
            print_number(i)
            self.zero_turn.release()


def run(n, order):
    lock = threading.Lock()
    log = []

    def say(x):
        with lock:
            log.append(str(x))

    z = ZeroEvenOdd(n)
    targets = [z.zero, z.even, z.odd]
    ts = [threading.Thread(target=targets[k], args=(say,)) for k in order]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    return "".join(log)


def main():
    orders = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
    want = "".join(f"0{i}" for i in range(1, 201))
    right = 0
    check = 0
    for r in range(1000):
        out = run(200, orders[r % 6])
        if out == want:
            right += 1
        check = (check * 31 + len(out) + r) % 1000000007
    print(f"1000 runs over 1 to 200: {right} in order, checksum {check}")


main()
