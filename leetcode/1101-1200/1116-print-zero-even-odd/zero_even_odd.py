# LeetCode #1116: Print Zero Even Odd -- mirrors the ★ arm: three
# one-slot queues hold the turns, zero's filled when the printer is made.
import queue
import threading


class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.zero_turn = queue.Queue(1)
        self.even_turn = queue.Queue(1)
        self.odd_turn = queue.Queue(1)
        self.zero_turn.put(())

    def zero(self, print_number):
        for i in range(1, self.n + 1):
            self.zero_turn.get()
            print_number(0)
            (self.odd_turn if i % 2 == 1 else self.even_turn).put(())

    def even(self, print_number):
        for i in range(2, self.n + 1, 2):
            self.even_turn.get()
            print_number(i)
            self.zero_turn.put(())

    def odd(self, print_number):
        for i in range(1, self.n + 1, 2):
            self.odd_turn.get()
            print_number(i)
            self.zero_turn.put(())


state = [1116]


def next_random():
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def run(n, order):
    log = []
    lock = threading.Lock()

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


def expected(n):
    return "".join(f"0{i}" for i in range(1, n + 1))


def checksum(s, check=0):
    for b in s.encode():
        check = (check * 131 + b) % 1000000007
    return check


def yes(b):
    return "true" if b else "false"


orders = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
print(f"n = 2 -> {run(2, orders[0])}")
print(f"n = 5 -> {run(5, orders[0])}")
print(f"n = 1, odd started first -> {run(1, orders[4])}")
print(f"n = 6, even started first -> {run(6, orders[3])}")
right = 0
check = 0
for _ in range(2000):
    n = next_random() % 15 + 1
    order = orders[next_random() % 6]
    out = run(n, order)
    if out == expected(n):
        right += 1
    check = checksum(out, check)
print(f"2000 runs of up to 15 numbers: {right} in order, checksum {check}")
out = run(1000, orders[5])
print(f"n = 1000: {len(out)} characters, in order {yes(out == expected(1000))}, checksum {checksum(out)}")
