# LeetCode #1195: Fizz Buzz Multithreaded -- the ★ arm in Python: one
# semaphore per printer, `number`'s starting with a permit, and each printer
# handing the turn to the printer of the next number. Four threads per run,
# started in the order the run gives.
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


def expected(n):
    return ["fizzbuzz" if i % 15 == 0 else "fizz" if i % 3 == 0 else "buzz" if i % 5 == 0 else str(i) for i in range(1, n + 1)]


seed = 1195


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


for n in [15, 5, 1, 3, 50]:
    print(f"n={n}: {', '.join(run(n, [0, 1, 2, 3]))}")
right = printed = 0
for _ in range(2000):
    n = next_random() % 50 + 1
    order = [0, 1, 2, 3]
    for i in range(3, 0, -1):
        j = next_random() % (i + 1)
        order[i], order[j] = order[j], order[i]
    got = run(n, order)
    printed += len(got)
    right += got == expected(n)
print(f"2000 random runs: {printed} printed, {right} in order")
