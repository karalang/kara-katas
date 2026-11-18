# LeetCode #1195 bench: the ★ arm in Python (threading.Semaphore), over the
# same 3 runs of n = 200000 as the Kāra bench.
import threading


class FizzBuzz:
    def __init__(self, n):
        self.n = n
        self.fizz_turn = threading.Semaphore(0)
        self.buzz_turn = threading.Semaphore(0)
        self.fizzbuzz_turn = threading.Semaphore(0)
        self.number_turn = threading.Semaphore(1)

    def pass_turn(self, i):
        if i > self.n:
            return
        if i % 15 == 0:
            self.fizzbuzz_turn.release()
        elif i % 3 == 0:
            self.fizz_turn.release()
        elif i % 5 == 0:
            self.buzz_turn.release()
        else:
            self.number_turn.release()

    def fizz(self, print_fizz):
        for i in range(1, self.n + 1):
            if i % 3 == 0 and i % 5 != 0:
                self.fizz_turn.acquire()
                print_fizz()
                self.pass_turn(i + 1)

    def buzz(self, print_buzz):
        for i in range(1, self.n + 1):
            if i % 5 == 0 and i % 3 != 0:
                self.buzz_turn.acquire()
                print_buzz()
                self.pass_turn(i + 1)

    def fizzbuzz(self, print_fizzbuzz):
        for i in range(1, self.n + 1):
            if i % 15 == 0:
                self.fizzbuzz_turn.acquire()
                print_fizzbuzz()
                self.pass_turn(i + 1)

    def number(self, print_number):
        for i in range(1, self.n + 1):
            if i % 3 != 0 and i % 5 != 0:
                self.number_turn.acquire()
                print_number(i)
                self.pass_turn(i + 1)


def run(n, order):
    fb = FizzBuzz(n)
    out = []
    lock = threading.Lock()

    def put(s):
        with lock:
            out.append(s)

    targets = [
        lambda: fb.fizz(lambda: put("fizz")),
        lambda: fb.buzz(lambda: put("buzz")),
        lambda: fb.fizzbuzz(lambda: put("fizzbuzz")),
        lambda: fb.number(lambda i: put(str(i))),
    ]
    threads = [threading.Thread(target=targets[role]) for role in order]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return out


check = 0
for order in [[0, 1, 2, 3], [3, 2, 1, 0], [1, 3, 0, 2]]:
    for line in run(200000, order):
        for b in line.encode():
            check = (check * 131 + b) % 1000000007
        check = (check * 131 + 10) % 1000000007
print(f"3 runs of n = 200000: checksum {check}")
